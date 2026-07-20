#!/usr/bin/env python3
"""Backfill the `learnset` field in references/pokemon/<species-slug>.yaml
files: the full list of moves a species can learn (level-up/TM/egg/tutor
combined), sourced from PokeAPI's per-species `/pokemon/{slug}` moves list.

This is deliberately a *different* field from `moves` (a curated 4-6-move
competitive subset -- see fetch_pokemon_data.py's docstring). `learnset` is
the exhaustive "what could this Pokemon learn" answer, which is exactly the
shape of data PokeAPI already returns, so unlike `moves` it doesn't need
hand curation -- just a live fetch and a confidence caveat, since PokeAPI's
movepool is mainline-game data, not confirmed against the Pokemon Champions
client. A spot-check against gamewith.jp's Champions-specific move-list page
for Garchomp showed Champions' actual learnable moves are a subset of
PokeAPI's mainline list (consistent with Champions already being known to
diverge from mainline itemization -- see references/rules/items-m-b.yaml),
so treat this field as a reliable candidate pool, not a guarantee.

Requires that the target file already has a `learnset:` line (added by a
one-time schema pass across all species files -- see references/pokemon
README.md). This script only ever replaces that one field in place and
appends a caveat paragraph to `data_confidence`; every other field in the
file is left untouched byte-for-byte.

Move display names (spelling/punctuation like "U-turn", "Will-O-Wisp") come
from move_names.json in this directory, a cache of PokeAPI's official
English move names built once via --rebuild-move-names (naive
title-casing gets these wrong, e.g. "u-turn" -> "U Turn" instead of
"U-turn").

Usage:
    # Backfill a batch of species (yaml filenames without .yaml, one per line):
    python3 backfill_learnset.py --species-file batch1.txt

    # Or specific slugs directly:
    python3 backfill_learnset.py --species garchomp blaziken

    # Rebuild move_names.json from PokeAPI (only needed if PokeAPI adds new
    # moves and their proper English names are wanted):
    python3 backfill_learnset.py --rebuild-move-names
"""
import argparse
import json
import os
import sys
import textwrap
import time
import urllib.error
import urllib.request

POKEAPI_BASE = "https://pokeapi.co/api/v2"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOVE_NAMES_PATH = os.path.join(SCRIPT_DIR, "move_names.json")
DEFAULT_POKEMON_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "..", "..", "references", "pokemon")
)

# Species whose YAML filename doesn't resolve directly as a PokeAPI
# pokemon slug -- these are exactly the "cosmetic variants collapsed into
# one file" species called out in references/pokemon/README.md (Aegislash,
# Gourgeist, Maushold, Mimikyu, Morpeko, Palafin) plus Pyroar (PokeAPI only
# exposes pyroar-male/pyroar-mega, no bare "pyroar" variety). Each maps to
# that species' default/base PokeAPI variety.
SLUG_OVERRIDES = {
    "aegislash": "aegislash-shield",
    "gourgeist": "gourgeist-average",
    "maushold": "maushold-family-of-four",
    "mimikyu": "mimikyu-disguised",
    "morpeko": "morpeko-full-belly",
    "palafin": "palafin-zero",
    "pyroar": "pyroar-male",
}

CAVEAT_MARKER = "Full `learnset`"


def fetch_json(url, retries=5, backoff=2.0):
    # Same PokeAPI CDN User-Agent workaround as fetch_pokemon_data.py.
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (backfill_learnset.py)"})
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            code = e.code
            e.close()
            if code == 404:
                return None
            last_err = e
        except urllib.error.URLError as e:
            last_err = e
        time.sleep(backoff * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def rebuild_move_names(out_path=MOVE_NAMES_PATH, sleep=0.05):
    lookup = {}
    if os.path.exists(out_path):
        with open(out_path) as f:
            lookup = json.load(f)
    listing = fetch_json(f"{POKEAPI_BASE}/move?limit=1000")
    results = listing["results"]
    print(f"{len(results)} moves in PokeAPI's move dex ({len(lookup)} already cached)", file=sys.stderr)
    for i, r in enumerate(results):
        slug = r["name"]
        if slug in lookup:
            continue
        data = fetch_json(r["url"])
        en_name = next((n["name"] for n in data.get("names", []) if n["language"]["name"] == "en"), None)
        lookup[slug] = en_name or slug.replace("-", " ").title()
        if i % 50 == 0:
            print(f"  {i}/{len(results)} {slug} -> {lookup[slug]}", file=sys.stderr)
            with open(out_path, "w") as f:
                json.dump(lookup, f, indent=1, sort_keys=True)
        time.sleep(sleep)
    with open(out_path, "w") as f:
        json.dump(lookup, f, indent=1, sort_keys=True)
    print(f"wrote {len(lookup)} move names to {out_path}", file=sys.stderr)


def load_move_names():
    with open(MOVE_NAMES_PATH) as f:
        return json.load(f)


def display_name(slug, move_names):
    return move_names.get(slug) or slug.replace("-", " ").title()


def fetch_learnset(species_slug, move_names):
    api_slug = SLUG_OVERRIDES.get(species_slug, species_slug)
    data = fetch_json(f"{POKEAPI_BASE}/pokemon/{api_slug}")
    if data is None:
        return None, api_slug
    move_slugs = {m["move"]["name"] for m in data["moves"]}
    names = sorted({display_name(s, move_names) for s in move_slugs})
    return names, api_slug


def splice_learnset(path, moves, api_slug):
    """Replace the `learnset:` field in place and append a data_confidence
    caveat paragraph, without disturbing any other field's formatting.
    """
    with open(path) as f:
        text = f.read()
    lines = text.split("\n")

    out = []
    replaced = False
    for line in lines:
        if line.startswith("learnset:"):
            out.append("learnset:")
            for mv in moves:
                out.append(f"  - {mv}")
            replaced = True
            continue
        out.append(line)
    if not replaced:
        raise RuntimeError(f"no 'learnset:' line in {path} -- run the schema-placeholder pass first")

    text = "\n".join(out)

    if CAVEAT_MARKER not in text:
        paragraph = (
            f"Full `learnset` ({len(moves)} moves) fetched from PokeAPI's mainline "
            f"movepool for pokemon/{api_slug} (level-up + TM/HM + egg + tutor moves "
            "combined) by backfill_learnset.py. This is NOT confirmed against the "
            "live Pokemon Champions client -- Champions has already been shown to "
            "diverge from mainline itemization (see items-m-b.yaml), so some listed "
            "moves may not actually be learnable in Champions. Treat as a candidate "
            "pool, not a guarantee."
        )
        wrapped = textwrap.wrap(paragraph, width=76)
        caveat_lines = ["", ""] + [f"  {line}" for line in wrapped]
        text = text.rstrip("\n") + "\n".join(caveat_lines) + "\n"

    with open(path, "w") as f:
        f.write(text)


def slug_for(raw):
    raw = raw.strip()
    if raw.endswith(".yaml"):
        raw = raw[: -len(".yaml")]
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--species", nargs="*", default=[], help="Species yaml filenames (without .yaml), space-separated")
    parser.add_argument("--species-file", help="Path to a text file with one species filename (without .yaml) per line")
    parser.add_argument("--pokemon-dir", default=DEFAULT_POKEMON_DIR, help="Directory containing <slug>.yaml files")
    parser.add_argument("--sleep", type=float, default=0.2, help="Seconds to sleep between API calls")
    parser.add_argument("--rebuild-move-names", action="store_true", help="Rebuild move_names.json from PokeAPI and exit")
    args = parser.parse_args()

    if args.rebuild_move_names:
        rebuild_move_names()
        return

    names = [slug_for(s) for s in args.species]
    if args.species_file:
        with open(args.species_file) as f:
            names += [slug_for(line) for line in f if line.strip() and not line.strip().startswith("#")]
    if not names:
        parser.error("Provide --species and/or --species-file, or --rebuild-move-names")

    move_names = load_move_names()

    ok, failed = [], []
    for species_slug in names:
        path = os.path.join(args.pokemon_dir, f"{species_slug}.yaml")
        if not os.path.exists(path):
            print(f"NOT FOUND: {path}", file=sys.stderr)
            failed.append(species_slug)
            continue
        try:
            moves, api_slug = fetch_learnset(species_slug, move_names)
        except RuntimeError as e:
            print(f"ERROR fetching {species_slug}: {e}", file=sys.stderr)
            failed.append(species_slug)
            continue
        if moves is None:
            print(f"NOT FOUND on PokeAPI: {species_slug} (tried slug '{SLUG_OVERRIDES.get(species_slug, species_slug)}')", file=sys.stderr)
            failed.append(species_slug)
            continue
        try:
            splice_learnset(path, moves, api_slug)
        except RuntimeError as e:
            print(f"ERROR writing {species_slug}: {e}", file=sys.stderr)
            failed.append(species_slug)
            continue
        print(f"{species_slug}: {len(moves)} moves")
        ok.append(species_slug)
        time.sleep(args.sleep)

    print(f"\n{len(ok)} written, {len(failed)} failed.")
    if failed:
        print("Failed: " + ", ".join(failed), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
