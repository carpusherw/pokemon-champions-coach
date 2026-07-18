# Pokemon reference data

One YAML file per legal Pokemon species (`<species-slug>.yaml`), so coaching
skills can read stats/types/abilities/Mega data without a live lookup.

## Current coverage: partial (21 of ~224-228 legal species)

This directory currently covers every species confirmed to be new to
Regulation M-B, plus every species that gained a Mega Evolution in M-B. It
does **not** yet cover the full legal roster (the M-A carryover base, minus
the M-B additions above).

Why: populating this file set requires either (a) bulk stat lookups from a
data API like [PokeAPI](https://pokeapi.co), or (b) fetching wiki/roster
pages to get the exhaustive species list. Both require outbound network
access that this session's sandbox blocked (see `../current-season.yaml` for
details). The 21 files here were written from the assistant's own knowledge
of mainline-game Pokemon data, cross-checked against what web search could
confirm about Regulation M-B specifically.

## Completing the roster

Run `scripts/fetch_pokemon_data.py` (in the `refresh-references` skill,
`agents/claude/pokemon-champions-coach/skills/refresh-references/scripts/`)
from an environment with normal internet access:

1. It needs the full legal species list for the current regulation. Get this
   from a roster page (e.g. StrataDex's Pokedex guide, Serebii's ranked
   battle regulation page, or in-game) and pass it as an input file.
2. It queries PokeAPI per species for types, base stats, and abilities, and
   writes/overwrites the corresponding `references/pokemon/<slug>.yaml`.
3. Mega Evolution data (especially for Champions-exclusive Megas that don't
   exist in mainline games) isn't in PokeAPI. Cross-check those against a
   current wiki/guide site and fill in the `mega:` block by hand, or extend
   the script if a good structured source turns up.

## Data quality flags to know about

Every file has a `data_confidence` field explaining how its data was
sourced. A few specific things to double check before trusting a file for a
close competitive call:

- Any `mega:` block with `status: unknown` or `status: partially known` —
  Champions-exclusive Megas (Staraptor, Scolipede, Scrafty, Malamar,
  Barbaracle, Dragalge, Falinks, Raichu X/Y, and partially Eelektross/Pyroar)
  have unconfirmed stats/typing/ability in this batch.
- `pyroar.yaml` — Pyroar has a male/female base-stat split in mainline games;
  this file uses one commonly-cited baseline, not a verified per-gender
  split.
- `raichu.yaml` — assumes standard (Kantonian) Raichu, not Alolan Raichu.
  Confirm which form actually receives the M-B Mega Stones.
