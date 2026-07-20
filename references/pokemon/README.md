# Pokemon reference data

One YAML file per legal Pokemon species (`<species-slug>.yaml`), so coaching
skills can read stats/types/abilities/Mega data without a live lookup.

## Current coverage: complete for Regulation M-B (232 files)

This directory covers the full Regulation M-B legal roster: every carryover
species from M-A plus all 22 species newly added in M-B, including regional
forms (Alolan/Galarian/Hisuian/Paldean), Rotom's appliance forms, and other
battle-relevant variants (Lycanroc time forms, Meowstic/Basculegion gender
splits, the three Paldean Tauros breeds) that have genuinely different
types/stats/abilities. Purely cosmetic variants (Alcremie flavors, Florges
colors, Furfrou trims, Vivillon patterns, Maushold family size, Polteageist
form) are *not* broken out into separate files since they share identical
battle data with their default form — see each species' `notes` field for
which forms a file's data applies to when that's non-obvious (e.g.
`aegislash.yaml`, `morpeko.yaml`, `palafin.yaml`, `mimikyu.yaml`,
`gourgeist.yaml`, `maushold.yaml`).

The full species list was sourced from Game8's "Regulation M-B Complete
Roster" page, cross-checked against Serebii's ranked-battle and recruit
roster pages. Base stats, types, and abilities for every file were fetched
live from [PokeAPI](https://pokeapi.co) via `scripts/fetch_pokemon_data.py`
on 2026-07-18.

## Mega Evolution coverage

PokeAPI has already ingested Pokemon Champions' Mega Evolution data (as
`<slug>-mega` / `-mega-x` / `-mega-y` pokemon entries), which made it
possible to fetch confirmed typing/ability/base-stat data -- not just
recalled/search-synthesized guesses -- for every Champions-exclusive Mega
introduced in M-B:

- `staraptor.yaml`, `scolipede.yaml`, `scrafty.yaml`, `malamar.yaml`,
  `barbaracle.yaml`, `dragalge.yaml`, `falinks.yaml`, `eelektross.yaml`,
  `pyroar.yaml` -- full `mega:` block (types, ability, base_stats) confirmed
  via PokeAPI.
- `raichu.yaml` -- both Mega Raichu X and Mega Raichu Y confirmed via
  PokeAPI, under `mega.x` / `mega.y` (this species has two Mega Stones, so
  it doesn't fit the single-mega schema every other file uses).
- `blaziken.yaml`, `mawile.yaml`, `metagross.yaml`, `sceptile.yaml`,
  `swampert.yaml` -- mainline-returning Megas; PokeAPI data cross-checked
  against and matched this session's prior recall exactly.

This pass only filled in Mega data for the species explicitly flagged as
having previously-unconfirmed Megas. Plenty of *other* legal species also
have Megas (e.g. Meowstic, Hawlucha, Crabominable, Drampa, Scovillain,
Glimmora, and all the classic mainline Megas like Charizard/Gengar/etc.) --
their files still have `mega: null` even though PokeAPI likely has that data
too (`<slug>-mega` resolves for most of them). Filling those in was out of
scope for this pass but would be a straightforward follow-up with the same
method.

## Moves field

Each file has a `moves` field, but it is **not** a full learnset (mainline
Pokemon can legally learn dozens to 100+ moves via level-up/TM/egg/tutor --
that's PokeAPI's job, or Showdown's, not this repo's). It's a curated list
of the handful of moves (typically 4-6) the species actually runs in
competitive Reg M-B play, e.g. `moves: [Flare Blitz, Close Combat, Swords
Dance, Protect]` for Blaziken. The intent is to answer "what does this
Pokemon actually do in a real set" for coaching purposes, not "what could
this Pokemon theoretically learn."

This also means a reverse lookup ("what can run Flamethrower?") doesn't
need its own index -- since these are read by an agent rather than queried
by a program, `grep -l "Flamethrower" references/pokemon/*.yaml` across 232
small files answers that directly.

**Current coverage: 29 of 232 species** (the ones that already had
hand-written competitive `notes` from the M-B-new-species/Champions-Mega
research pass -- see each file's `data_confidence` for exactly what's
curated vs recalled). Every other file has `moves: null` with a TODO
comment. Filling those in is a straightforward follow-up with the same
method described in the refresh-references skill, one regulation-relevant
batch at a time -- there was no attempt to guess movepools for species that
haven't had a real competitive research pass yet, the same policy already
applied to `notes`.

## Learnset field

Each file also has a `learnset` field: the full list of moves this species
can learn (level-up/TM/egg/tutor combined), as opposed to `moves`'
curated "what does it actually run" subset. This is the "what *could* this
Pokemon learn" answer that `moves`' own doc comment above explicitly says
isn't its job.

`learnset` is sourced from PokeAPI's per-species `/pokemon/{slug}` moves
list (via `backfill_learnset.py` in the refresh-references skill), which is
a **mainline-game learnset**, not confirmed against the live Pokemon
Champions client. A spot-check against gamewith.jp's Champions-specific
per-species move page for Garchomp (a real, game-sourced move list, just
not exhaustively scraped for all 232 species due to the volume involved)
showed Champions' actual learnable-move list is a *subset* of PokeAPI's
mainline list -- consistent with Champions already being known to diverge
from mainline itemization (see `references/rules/items-m-b.yaml` re: Choice
items not being implemented). Treat `learnset` as a reliable candidate
pool, not a guarantee that every listed move is obtainable in Champions;
each file's `data_confidence` repeats this caveat. Move names use PokeAPI's
official English display spelling/punctuation (e.g. `U-turn`,
`Will-O-Wisp`), not naive title-casing.

Unlike `mega`/`moves`, a species not yet covered has **no `learnset` key at
all** rather than a `learnset: null` placeholder -- adding that placeholder
to all 232 files in one pass was tried first, but it meant even a
single-batch PR touched all 232 files and blew past the review tooling's
100-file limit. Each batch instead adds the key straight to real content
for just that batch's species.

**Current coverage: 96 of 232 species** (batch 1: alphabetical
`abomasnow`..`crabominable` plus `garchomp`/`palafin`/`pyroar` picked up
early as spot-checks; batch 2: `decidueye-hisui`..`hawlucha`). The
remaining backfill is being rolled out in ~44-46-species batches, one PR
per batch -- see `backfill_learnset.py`'s docstring for how to run a
batch.

## Data quality flags to know about

Every file has a `data_confidence` field explaining how its data was
sourced. A few specific things to double check before trusting a file for a
close competitive call:

- `pyroar.yaml` -- Pyroar has a documented male/female base-stat split in
  mainline games, but PokeAPI only exposes a male variety (no
  `pyroar-female` entry), so this file's base stats are male-only. Its Mega
  data, ability, and typing are all confirmed via PokeAPI.
- `eelektross.yaml` -- Mega Eelektross's ability, `Eelevate`, is confirmed
  by name via PokeAPI but this session couldn't confirm its exact in-battle
  effect from any source.
- `raichu.yaml` -- assumes standard (Kantonian) Raichu; the two Mega Stones
  were seen paired with this form in research, but which Raichu form (this
  one vs. `raichu-alola.yaml`) Pokemon Champions actually grants the Mega
  Stones to was not confirmed against a primary/official source.
- Any file whose competitive `notes` field still reads
  `TODO: add competitive notes (...)` hasn't had hand-written competitive
  commentary added yet -- its base stats/types/abilities are still live
  PokeAPI data and reliable, just without the coaching-relevant color
  commentary the M-B-new species and Megas above have.

## Refreshing this data

Run `scripts/fetch_pokemon_data.py` (in the `refresh-references` skill,
`agents/claude/pokemon-champions-coach/skills/refresh-references/scripts/`)
from an environment with normal internet access to refresh base
stats/types/abilities for any species, or add new ones:

```
python3 fetch_pokemon_data.py --species-file <list-of-pokeapi-slugs> --regulation <id>
```

It's safe to re-run over existing files -- it only refreshes base-form
fields and won't touch a file's hand-written `mega`/`notes` unless you pass
`--overwrite`. Mega Evolution data for species not covered above still needs
either a `<slug>-mega` PokeAPI lookup (works for most classic mainline
Megas and, as of this pass, Champions-exclusive ones too) or a wiki/guide
cross-check, filled in by hand.
