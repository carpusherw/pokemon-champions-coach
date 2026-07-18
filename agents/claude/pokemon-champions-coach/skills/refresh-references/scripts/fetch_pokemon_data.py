#!/usr/bin/env python3
"""Bulk-fetch base Pokemon data (types, base stats, abilities) from PokeAPI
and write/update references/pokemon/<species-slug>.yaml files.

PokeAPI has no concept of "Pokemon Champions" or Mega Evolutions added in a
specific regulation set, so this script only ever fills in the base-form
fields (national_dex_number, types, base_stats, abilities). It leaves an
existing file's `mega`, `notes`, `added_in_regulation`, and
`legal_in_regulations` fields untouched unless --overwrite is passed, since
those need a human or a web-search pass to get right, not an API call.

Usage:
    # From a text file, one species name per line (e.g. names copied out of
    # a roster guide):
    python3 fetch_pokemon_data.py --species-file roster.txt --regulation M-B

    # Or a handful of names directly:
    python3 fetch_pokemon_data.py --species Sceptile Blaziken Swampert --regulation M-B

Species names should be PokeAPI's lowercase-hyphenated form where it
differs from the display name (e.g. "mr-mime", "nidoran-f"). Plain names
are lowercased and spaces turned into hyphens automatically, which covers
the vast majority of cases.
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
DEFAULT_OUTPUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "..", "references", "pokemon")
)


def api_slug(name):
    return name.strip().lower().replace(" ", "-").replace("'", "").replace(".", "")


def fetch_json(url, retries=3, backoff=2.0):
    last_err = None
    # PokeAPI's CDN returns 403 for requests without a browser-like User-Agent
    # (the default "Python-urllib/x.y" gets blocked), so set one explicitly.
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (fetch_pokemon_data.py)"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            last_err = e
        except urllib.error.URLError as e:
            last_err = e
        time.sleep(backoff * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def fetch_species_data(slug):
    data = fetch_json(f"{POKEAPI_BASE}/pokemon/{slug}")
    if data is None:
        return None
    stats_by_key = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
    base_stats = {
        "hp": stats_by_key.get("hp"),
        "atk": stats_by_key.get("attack"),
        "def": stats_by_key.get("defense"),
        "spa": stats_by_key.get("special-attack"),
        "spd": stats_by_key.get("special-defense"),
        "spe": stats_by_key.get("speed"),
    }
    types = [t["type"]["name"].capitalize() for t in sorted(data["types"], key=lambda t: t["slot"])]
    abilities = [
        {"name": a["ability"]["name"].replace("-", " ").title(), "hidden": a["is_hidden"]}
        for a in data["abilities"]
    ]
    return {
        "name": data["name"].replace("-", " ").title(),
        "national_dex_number": data["id"],
        "types": types,
        "base_stats": base_stats,
        "abilities": abilities,
    }


def fmt_stats(s):
    return "{{hp: {hp}, atk: {atk}, def: {def_}, spa: {spa}, spd: {spd}, spe: {spe}}}".format(
        hp=s["hp"], atk=s["atk"], def_=s["def"], spa=s["spa"], spd=s["spd"], spe=s["spe"]
    )


def read_existing_yaml(path):
    """Reads the fields we need to preserve out of an existing file.

    Returns None only when there's genuinely nothing to preserve (the file
    doesn't exist yet). If the file *does* exist but PyYAML isn't installed,
    raise instead of returning None -- silently treating a hand-curated file
    as "doesn't exist" would make write_yaml overwrite its mega/notes fields
    with placeholder text even when --overwrite wasn't requested, which is
    exactly the data loss this function exists to prevent.
    """
    if not os.path.exists(path):
        return None
    try:
        import yaml
    except ImportError:
        raise RuntimeError(
            f"{path} already exists but PyYAML isn't installed, so its "
            "hand-curated fields (mega, notes, etc.) can't be safely read "
            "and preserved. Install it first (`pip install pyyaml`), or "
            "pass --overwrite if you actually intend to replace this "
            "file's mega/notes data."
        )
    with open(path) as f:
        return yaml.safe_load(f)


def emit_field(key, value, indent):
    """Return the YAML lines for `key: value` at the given indent string.

    Preserved fields (mega sub-fields, notes) round-trip through here after
    being parsed back out of an existing hand-written file, so a string that
    was written as a folded `>` block scalar comes back from yaml.safe_load
    as a single string that may still contain embedded newlines (from blank
    lines separating paragraphs in the original block). Re-emitting that as
    a bare `key: value` line breaks YAML the moment there's a newline in the
    middle of it, or even just when the text contains a colon or a leading
    special character -- so any multi-line or otherwise unsafe string goes
    back out as a proper indented block scalar instead of a plain scalar.
    """
    if value is None:
        return [f"{indent}{key}: null"]
    if isinstance(value, dict):
        if key == "base_stats":
            return [f"{indent}{key}: {fmt_stats(value)}"]
        lines = [f"{indent}{key}:"]
        for k2, v2 in value.items():
            lines.extend(emit_field(k2, v2, indent + "  "))
        return lines
    if isinstance(value, list):
        return [f"{indent}{key}: [{', '.join(str(x) for x in value)}]"]
    if isinstance(value, bool):
        return [f"{indent}{key}: {str(value).lower()}"]
    if isinstance(value, str):
        needs_block = "\n" in value or len(value) > 80 or value[:1] in ":#-\"'" or ": " in value
        if needs_block:
            lines = [f"{indent}{key}: >"]
            # Each "\n" in a string that came from yaml.safe_load-ing a
            # folded (`>`) block scalar marks one paragraph break, so
            # re-insert a blank line between paragraphs to preserve that
            # instead of letting them re-fold into a single paragraph.
            for i, paragraph in enumerate(value.split("\n")):
                if i > 0:
                    lines.append("")
                if paragraph:
                    wrapped = textwrap.wrap(paragraph, width=76) or [""]
                    lines.extend(f"{indent}  {line}" for line in wrapped)
            return lines
        return [f"{indent}{key}: {value}"]
    return [f"{indent}{key}: {value}"]


def write_yaml(path, fresh, existing, regulation, overwrite):
    preserved = {}
    if existing and not overwrite:
        for key in ("mega", "notes", "added_in_regulation", "legal_in_regulations"):
            if key in existing:
                preserved[key] = existing[key]

    lines = []
    lines.append(f"name: {fresh['name']}")
    lines.append(f"national_dex_number: {fresh['national_dex_number']}")
    lines.append(f"types: [{', '.join(fresh['types'])}]")
    lines.append(f"base_stats: {fmt_stats(fresh['base_stats'])}")
    lines.append("abilities:")
    for a in fresh["abilities"]:
        lines.append(f"  - name: {a['name']}")
        lines.append(f"    hidden: {str(a['hidden']).lower()}")

    if "mega" in preserved:
        mega = preserved["mega"]
        if isinstance(mega, dict):
            lines.append("mega:")
            for k, v in mega.items():
                lines.extend(emit_field(k, v, "  "))
        else:
            lines.append("mega: null")
    else:
        lines.append("mega: null  # TODO: fill in if this species has a Mega Evolution")

    added_in = preserved.get("added_in_regulation", regulation)
    lines.extend(emit_field("added_in_regulation", added_in, ""))

    legal_in = preserved.get("legal_in_regulations", [regulation])
    if isinstance(legal_in, list) and regulation not in legal_in:
        legal_in = legal_in + [regulation]
    lines.append(f"legal_in_regulations: [{', '.join(legal_in)}]")

    notes = preserved.get("notes", "TODO: add competitive notes (role, speed-control relevance, etc).")
    lines.extend(emit_field("notes", notes, ""))

    lines.append("data_confidence: >")
    lines.append(
        "  Base stats/types/abilities fetched live from PokeAPI "
        f"({POKEAPI_BASE}) by fetch_pokemon_data.py. Mega Evolution data (if "
        "any) and competitive notes are NOT from PokeAPI and should be "
        "verified/updated by hand each season."
    )

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def slug_for_filename(name):
    return name.strip().lower().replace(" ", "-").replace("'", "")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--species", nargs="*", default=[], help="Species names to fetch, space-separated")
    parser.add_argument("--species-file", help="Path to a text file with one species name per line")
    parser.add_argument("--regulation", required=True, help="Regulation set ID to tag these as legal in, e.g. M-B")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Where to write <slug>.yaml files")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite mega/notes fields too, not just base stats")
    parser.add_argument("--sleep", type=float, default=0.3, help="Seconds to sleep between API calls (be nice to PokeAPI)")
    args = parser.parse_args()

    names = list(args.species)
    if args.species_file:
        with open(args.species_file) as f:
            names += [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    if not names:
        parser.error("Provide --species and/or --species-file with at least one name")

    os.makedirs(args.output_dir, exist_ok=True)

    ok, failed = [], []
    for raw_name in names:
        slug = api_slug(raw_name)
        try:
            fresh = fetch_species_data(slug)
        except RuntimeError as e:
            print(f"ERROR fetching {raw_name}: {e}", file=sys.stderr)
            failed.append(raw_name)
            continue
        if fresh is None:
            print(f"NOT FOUND on PokeAPI: {raw_name} (slug '{slug}')", file=sys.stderr)
            failed.append(raw_name)
            continue

        out_path = os.path.join(args.output_dir, f"{slug_for_filename(fresh['name'])}.yaml")
        try:
            existing = None if args.overwrite else read_existing_yaml(out_path)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            failed.append(raw_name)
            continue
        write_yaml(out_path, fresh, existing, args.regulation, args.overwrite)
        print(f"wrote {out_path}")
        ok.append(raw_name)
        time.sleep(args.sleep)

    print(f"\n{len(ok)} written, {len(failed)} failed.")
    if failed:
        print("Failed lookups (check spelling / PokeAPI slug form): " + ", ".join(failed), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
