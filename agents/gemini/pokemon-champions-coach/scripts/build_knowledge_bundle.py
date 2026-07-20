#!/usr/bin/env python3
"""Compile references/ into the small, fixed set of files Gemini Gems can
actually ingest, and write them to ../knowledge-bundle/.

Gemini's "Knowledge" upload (Gem Manager -> Knowledge -> Add files) caps out
at 10 files per Gem and has no native YAML support, no filesystem access, and
no way to run this repo's scripts live -- so unlike the Claude plugin, which
reads references/*.yaml directly at chat time, the Gemini Gem instead reads a
handful of pre-compiled Markdown files that a human uploads by hand. This
script is what produces those files.

references/ stays the single source of truth. This script only ever reads
from it; it never writes back. Re-run it (and re-upload the changed files to
the Gem's Knowledge panel) any time references/ or the current regulation
changes -- CI's knowledge-bundle-guard.yml fails a PR if the checked-in
bundle is stale relative to what this script would produce.

Usage:
    python3 build_knowledge_bundle.py
    python3 build_knowledge_bundle.py --check   # exit 1 if output would change (used by CI)
"""
import argparse
import filecmp
import os
import sys
import tempfile

import yaml

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
REFERENCES_DIR = os.path.join(REPO_ROOT, "references")
POKEMON_DIR = os.path.join(REFERENCES_DIR, "pokemon")
SPEED_MECHANICS_SOURCE = os.path.join(
    REPO_ROOT,
    "agents", "claude", "pokemon-champions-coach", "skills", "move-order-coach",
    "reference", "speed-mechanics.md",
)
ARCHETYPES_DOUBLES_SOURCE = os.path.join(
    REPO_ROOT,
    "agents", "claude", "pokemon-champions-coach", "skills", "team-builder-doubles",
    "reference", "archetypes.md",
)
ARCHETYPES_SINGLES_SOURCE = os.path.join(
    REPO_ROOT,
    "agents", "claude", "pokemon-champions-coach", "skills", "team-builder-singles",
    "reference", "archetypes.md",
)
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge-bundle")

BUNDLE_HEADER = """\
<!--
Compiled by agents/gemini/pokemon-champions-coach/scripts/build_knowledge_bundle.py.
Do not hand-edit this file -- most bundle files come from references/, but
this one may instead be a copy of a skill's own reference/*.md file (see
SPEED_MECHANICS_SOURCE, ARCHETYPES_DOUBLES_SOURCE, and ARCHETYPES_SINGLES_SOURCE
in build_knowledge_bundle.py for exactly which). Edit the actual source and
re-run the build script instead, or your changes will be overwritten and
CI's knowledge-bundle-guard will flag the file as stale anyway.
-->

"""


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def fmt_stats(stats):
    order = [("hp", "HP"), ("atk", "Atk"), ("def", "Def"), ("spa", "SpA"), ("spd", "SpD"), ("spe", "Spe")]
    return ", ".join(f"{label} {stats.get(key)}" for key, label in order)


def fmt_abilities(abilities):
    return ", ".join(f"{a['name']}{' (hidden)' if a.get('hidden') else ''}" for a in abilities or [])


def fmt_mega(mega):
    if not mega:
        return None
    if "x" in mega or "y" in mega:
        # Two-Mega-Stone species (e.g. Raichu): render each form.
        parts = []
        for form_key in ("x", "y"):
            form = mega.get(form_key)
            if not form:
                continue
            parts.append(f"  - Mega ({form_key.upper()}): " + fmt_mega_form(form))
        return "\n".join(parts) if parts else None
    return "  - Mega: " + fmt_mega_form(mega)


def fmt_mega_form(form):
    bits = []
    if form.get("types"):
        bits.append("Types " + "/".join(form["types"]))
    if form.get("base_stats"):
        bits.append(fmt_stats(form["base_stats"]))
    if form.get("ability"):
        bits.append(f"Ability {form['ability']}")
    text = "; ".join(bits) if bits else "(unconfirmed)"
    if form.get("note"):
        text += f" -- {form['note']}"
    return text


def build_season_and_rules():
    season = load_yaml(os.path.join(REFERENCES_DIR, "current-season.yaml"))
    regulation = load_yaml(os.path.join(REFERENCES_DIR, season["regulation_file"]))

    lines = [BUNDLE_HEADER.rstrip(), ""]
    lines.append("# Current season & rules")
    lines.append("")
    lines.append(
        f"Current regulation: **{regulation['id']}** ({regulation.get('name', '')}), "
        f"active {regulation.get('active_from')} to {regulation.get('active_until')}. "
        f"references/ last refreshed {season.get('last_refreshed')}."
    )
    lines.append("")
    if regulation.get("summary"):
        lines.append(regulation["summary"].strip())
        lines.append("")

    fmt = regulation.get("format", {})
    lines.append("## Format")
    lines.append(f"- Level: {fmt.get('level')}, auto-leveled: {fmt.get('auto_leveling')}")
    lines.append(f"- Win condition: {fmt.get('win_condition')}")
    lines.append(f"- Team preview: {fmt.get('team_preview_seconds')}s")
    lines.append(f"- Turn timer: {fmt.get('per_turn_seconds')}, match limit: {fmt.get('match_time_limit_minutes')} min")
    modes = fmt.get("modes", {})
    for mode_name, mode in modes.items():
        desc = f" -- {mode['description'].strip()}" if mode.get("description") else ""
        lines.append(f"- {mode_name.capitalize()}: {mode.get('battlers_per_side')} battler(s) per side{desc}")
    lines.append("")

    tb = regulation.get("team_building_rules", {})
    lines.append("## Team building")
    lines.append(f"- Battle team size: {tb.get('battle_team_size')}, brought to battle: {tb.get('brought_to_battle')}")
    if tb.get("species_clause", {}).get("enabled"):
        lines.append(f"- Species clause: {tb['species_clause'].get('description', '').strip()}")
    if tb.get("item_clause", {}).get("enabled"):
        lines.append(f"- Item clause: {tb['item_clause'].get('description', '').strip()}")
    mega = tb.get("mega_evolution", {})
    if mega.get("allowed"):
        lines.append(
            f"- Mega Evolution: allowed, max {mega.get('max_per_battle')} per battle -- "
            f"{mega.get('description', '').strip()}"
        )
    lines.append("")

    legality = regulation.get("legality", {})
    lines.append("## Legality")
    if legality.get("no_separate_banlist"):
        lines.append("- No separate ban list -- legality is simply \"has this species been added to the game yet.\"")
    for cat in legality.get("currently_excluded_categories", []):
        lines.append(f"- Excluded: {cat}")
    if legality.get("approx_legal_species_count"):
        lines.append(f"- Roster size: {legality['approx_legal_species_count']}")
    lines.append("")

    new_reg = regulation.get("new_in_this_regulation", {})
    if new_reg:
        lines.append(f"## New in {regulation['id']}")
        species_list = new_reg.get("new_species_list", [])
        if species_list:
            lines.append(f"- {new_reg.get('new_species_count', len(species_list))} newly legal species: " + ", ".join(species_list))
        megas = new_reg.get("new_mega_evolutions", {})
        if megas:
            lines.append(f"- {megas.get('count')} new Mega Evolutions across {megas.get('species_count')} species.")
            if megas.get("champions_exclusive_new_megas"):
                lines.append("  Champions-exclusive (no mainline equivalent): " + ", ".join(str(m) for m in megas["champions_exclusive_new_megas"]))
        lines.append("")

    ladder = regulation.get("ranked_ladder", {})
    if ladder:
        lines.append("## Ranked ladder")
        lines.append(f"- Tiers: {', '.join(ladder.get('tiers', []))} ({ladder.get('sub_ranks_per_tier')} sub-ranks each)")
        lines.append(f"- Promotion: {ladder.get('promotion')}")
        if ladder.get("gating"):
            lines.append(f"- Gating: {ladder['gating']}")
        lines.append(f"- Singles and doubles ladders independent: {ladder.get('singles_and_doubles_are_independent')}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_pokemon_dex():
    season = load_yaml(os.path.join(REFERENCES_DIR, "current-season.yaml"))
    current_regulation = season["current_regulation"]

    entries = []
    for filename in sorted(os.listdir(POKEMON_DIR)):
        if not filename.endswith(".yaml"):
            continue
        data = load_yaml(os.path.join(POKEMON_DIR, filename))
        legal_in = data.get("legal_in_regulations") or []
        if current_regulation not in legal_in:
            continue
        entries.append(data)

    lines = [BUNDLE_HEADER.rstrip(), ""]
    lines.append("# Pokemon dex")
    lines.append("")
    lines.append(
        f"{len(entries)} species legal in the current regulation ({current_regulation}). "
        "One entry per species: dex number, types, base stats, abilities, Mega "
        "Evolution data (if any), a curated competitive movepool (if any -- a "
        "handful of moves this species actually runs, not its full learnset), "
        "and hand-written competitive notes. Species no longer legal in the "
        "current regulation are omitted -- see the main repo's "
        "references/pokemon/ for full history."
    )
    lines.append("")

    for data in entries:
        lines.append(f"## {data['name']} (#{data.get('national_dex_number')})")
        lines.append(f"- Types: {'/'.join(data.get('types', []))}")
        lines.append(f"- Base stats: {fmt_stats(data.get('base_stats', {}))}")
        lines.append(f"- Abilities: {fmt_abilities(data.get('abilities'))}")
        mega_text = fmt_mega(data.get("mega"))
        if mega_text:
            lines.append(mega_text)
        moves = data.get("moves")
        if moves:
            lines.append(f"- Common moves: {', '.join(moves)}")
        notes = (data.get("notes") or "").strip()
        if notes and not notes.startswith("TODO"):
            lines.append(f"- Notes: {notes}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_pokemon_learnsets():
    season = load_yaml(os.path.join(REFERENCES_DIR, "current-season.yaml"))
    current_regulation = season["current_regulation"]

    entries = []
    for filename in sorted(os.listdir(POKEMON_DIR)):
        if not filename.endswith(".yaml"):
            continue
        data = load_yaml(os.path.join(POKEMON_DIR, filename))
        legal_in = data.get("legal_in_regulations") or []
        if current_regulation not in legal_in:
            continue
        entries.append(data)

    lines = [BUNDLE_HEADER.rstrip(), ""]
    lines.append("# Pokemon learnsets")
    lines.append("")
    lines.append(
        f"{len(entries)} species legal in the current regulation ({current_regulation}). "
        "One entry per species: its full learnable movepool (level-up + TM/HM + "
        "egg + tutor moves combined), fetched from PokeAPI's mainline data -- "
        "NOT confirmed against the live Pokemon Champions client, and NOT the "
        "same thing as pokemon-dex.md's curated \"common moves\" list (a "
        "handful of moves the species actually runs). Use this file for \"could "
        "X learn move Y\" or \"what are X's options\" questions; use "
        "pokemon-dex.md for \"what does X actually run.\" A species with no "
        "learnset entry here hasn't been backfilled yet -- say so rather than "
        "guessing its movepool from general knowledge."
    )
    lines.append("")

    for data in entries:
        learnset = data.get("learnset")
        if not learnset:
            continue
        lines.append(f"## {data['name']} (#{data.get('national_dex_number')})")
        lines.append(", ".join(learnset))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_speed_mechanics():
    with open(SPEED_MECHANICS_SOURCE) as f:
        body = f.read()
    return BUNDLE_HEADER + body


def build_archetypes_doubles():
    with open(ARCHETYPES_DOUBLES_SOURCE) as f:
        body = f.read()
    return BUNDLE_HEADER + body


def build_archetypes_singles():
    with open(ARCHETYPES_SINGLES_SOURCE) as f:
        body = f.read()
    return BUNDLE_HEADER + body


def write_bundle(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = {
        "season-and-rules.md": build_season_and_rules(),
        "speed-mechanics.md": build_speed_mechanics(),
        "pokemon-dex.md": build_pokemon_dex(),
        "pokemon-learnsets.md": build_pokemon_learnsets(),
        "archetypes-doubles.md": build_archetypes_doubles(),
        "archetypes-singles.md": build_archetypes_singles(),
    }
    for name, content in files.items():
        with open(os.path.join(output_dir, name), "w") as f:
            f.write(content)
    return sorted(files.keys())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR, help="Where to write the bundle (default: knowledge-bundle/)")
    parser.add_argument("--check", action="store_true", help="Don't write; exit 1 if the checked-in bundle is stale")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            names = write_bundle(tmp)
            mismatches = []
            for name in names:
                committed = os.path.join(args.output_dir, name)
                fresh = os.path.join(tmp, name)
                if not os.path.exists(committed) or not filecmp.cmp(committed, fresh, shallow=False):
                    mismatches.append(name)
            if mismatches:
                print("Knowledge bundle is stale (would change): " + ", ".join(mismatches), file=sys.stderr)
                print("Run `python3 agents/gemini/pokemon-champions-coach/scripts/build_knowledge_bundle.py` and commit the result.", file=sys.stderr)
                return 1
            print("Knowledge bundle is up to date.")
            return 0

    names = write_bundle(args.output_dir)
    print(f"Wrote {', '.join(names)} to {args.output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
