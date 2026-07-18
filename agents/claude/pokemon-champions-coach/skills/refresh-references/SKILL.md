---
name: refresh-references
description: >
  Refreshes the local reference data for Pokemon Champions: the current
  regulation set's rules (team building, format, timers, legal roster) and
  the per-Pokemon dex data (types, base stats, abilities, Mega Evolutions)
  that every other coaching skill in this plugin reads instead of looking
  things up live. Only invoke this when the user explicitly asks for it --
  for example "M-C just dropped", "check if the rules changed", "is my
  reference data still current", "update the pokemon data/references", or
  "refresh the regulation data". This skill does real outbound
  research (web search/fetches) and rewrites shared reference files, so it
  should never fire on its own just because a file looks old or a
  conversation happens to be about Pokemon Champions -- if you notice the
  data might be stale while doing something else, mention that to the user
  and let them decide whether they want a refresh, rather than running it
  for them.
---

# Refresh Pokemon Champions references

Pokemon Champions rotates **regulation sets** every couple of months. Each
regulation set changes the legal Pokemon roster (this is a live-service game
that's still adding species, not the full National Dex) and can add new
Mega Evolutions, and occasionally other rule tweaks. Everything else in this
plugin -- the move-order-coach skill, and any future coaching skill -- reads
from `references/` instead of researching from scratch each time, so keeping
those files current is the whole point of this skill.

`references/` lives at the repo root, not inside this plugin, because it's
agent-agnostic: any other agent's skills should be able to read the same
files. Don't move it.

## When to actually do the work

Check `references/current-season.yaml` first:

- If `current_regulation` already matches what you (or the user) believe is
  current, and `last_refreshed` is recent (a few weeks old, not a few
  months), the references are probably fine -- confirm with the user rather
  than re-running the whole flow for no reason.
- If the regulation looks stale, wasn't found, or the user explicitly asks
  for a refresh, do the full flow below.

## Step 1: Confirm the current regulation set and its rules

Search for the current regulation (e.g. "Pokemon Champions current
regulation set rules 2026", "Pokemon Champions Regulation M-C" once you know
or suspect a letter/number). A few things worth knowing about doing this
research in practice:

- **Prefer WebSearch over WebFetch for these sources.** Major Pokemon wiki
  and news sites (Serebii, Bulbapedia, Game8, official pokemon.com posts,
  and most fan sites) tend to return 403s to direct page fetches from
  sandboxed tool environments, even though WebSearch's own result synthesis
  gets through fine. Do several targeted WebSearch queries and cross-check
  them against each other rather than fighting with WebFetch. If WebFetch
  *does* work in your environment, by all means use it for more detail --
  just don't burn turns retrying a host that's clearly blocking you.
- Cross-check at least two independent sources for anything you plan to
  write down as fact (dates, timer numbers, and roster counts are the fields
  most likely to be reported inconsistently across sites).
- If you can't pin something down precisely (this happens -- e.g. exact
  turn-timer seconds were inconsistent across sources as of M-B), write down
  what you found plus a note flagging the uncertainty, rather than picking
  one number and presenting it as certain. A wrong "confident" number is
  worse for the user than an honest "verify this" note.

Write the result to `references/rules/regulation-<id>.yaml` (lowercase,
e.g. `regulation-m-c.yaml`). **Use `references/rules/regulation-m-b.yaml` as
your schema template** -- match its structure (format, team_building_rules,
legality, new_in_this_regulation, ranked_ladder) so downstream skills don't
have to handle multiple shapes. Keep the sourcing comment block at the top
of the file, updated with what you actually used this time.

Then update `references/current-season.yaml` to point at the new file and
bump `last_refreshed`.

## Step 2: Update the legal Pokemon roster

You need to know, at minimum, what's *new* this regulation (newly legal
species, newly added Mega Evolutions) -- that's usually well covered in
patch-notes-style articles and is enough to make the roster useful even if
you can't get an exhaustive list. Getting the full legal roster (currently
~224-228 species as of M-B) is the ideal, but don't let a perfect-vs-good
tradeoff block you from shipping useful references.

For each newly-legal or newly-changed species:

1. Prefer bundling the base-stat/type/ability lookups through
   `scripts/fetch_pokemon_data.py`, which hits [PokeAPI](https://pokeapi.co)
   -- that's a real structured data source and is much faster and more
   reliable than reading it off a wiki page one Pokemon at a time. Give it
   either `--species Name1 Name2 ...` or `--species-file path/to/list.txt`
   plus `--regulation <id>`. It's safe to re-run on existing files: by
   default it only refreshes the base-stat/type/ability fields from the API
   and leaves any hand-written `mega`/`notes` fields alone (pass
   `--overwrite` if you really want to replace those too).
2. PokeAPI has no idea what Pokemon Champions or its Mega Evolutions are --
   it's mainline-game data only. For each species that has a Mega
   Evolution in this format, especially **Champions-exclusive Megas that
   don't exist in any mainline game**, you have to fill in the `mega:` block
   by hand from web research. If you can't confirm a Mega's stats/typing/
   ability, don't guess -- set the unconfirmed field(s) (`types`,
   `base_stats`, `ability`) to `null` and explain what's missing and why in
   `mega.note`, the same way the M-B batch handled the Champions-exclusive
   Megas it couldn't confirm. A coaching skill that trusts a fabricated stat
   line is worse than one that says "verify this."
3. Add a one or two sentence `notes:` field per species: not a full moveset
   dump, but the specific things that matter for coaching calls -- unusual
   Speed tier, priority-move access, Prankster/other speed-control
   abilities, Trick Room relevance, anything a human player would want
   flagged fast mid-draft or mid-battle.

If PokeAPI (or any outbound network call) is blocked in your current
environment -- check by trying one fetch early, don't discover it 20 calls
in -- fall back to your own knowledge for well-established mainline Pokemon
(types/stats/abilities for existing species are stable facts you likely
already know accurately) plus WebSearch for anything Champions-specific,
and say clearly in each file's `data_confidence` field that the data wasn't
fetched live this pass. See `references/pokemon/README.md` for how this was
handled the first time and what's still missing.

## Step 3: Report what changed

Tell the user, briefly: what regulation is now current, what's newly legal
(species and Megas), anything you couldn't confirm and flagged, and whether
the roster reference is complete or still partial. Point them at
`references/pokemon/README.md` if there's a coverage gap worth knowing
about before they rely on this for a real match.
