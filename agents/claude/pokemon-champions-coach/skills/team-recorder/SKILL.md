---
name: team-recorder
description: >
  Saves a Pokemon Champions team to a reusable file so it doesn't have to be
  rebuilt or re-described from scratch in a later session or for a
  different matchup. Use this whenever the user asks to save, record,
  remember, log, or export a team; when `team-builder-doubles` or
  `team-builder-singles` just finished presenting a finished team and the
  user wants to keep it; or when the user pastes one or more screenshots of
  their in-game team screen (the roster list showing each Pokemon's
  ability/item/moves, or the stats screen showing base stats with nature
  arrows and EV investment) and wants it turned into something reusable.
  Works standalone -- the user does not need to have used either
  team-builder skill first; a screenshot, a pasted team export/team sheet,
  or even a rough text description of six Pokemon is enough to start from.
  Also use it to update an already-saved team after the user changes a
  set, and to list or load a previously saved team back into the
  conversation (e.g. "load my Trick Room team", "what did I save as
  rain-core"). Do NOT use this for building a team from an idea or a
  starting Pokemon -- that's `team-builder-doubles`/`team-builder-singles`;
  this skill only records/loads a team that's already decided.
---

# Save and reload a team

This skill exists because a finished team otherwise has to be rebuilt or
re-typed every time it comes up in a new session or against a new matchup.
It turns "here's my team" (however it's given) into a small file under
`saved-teams/` that any later session -- this skill, `move-order-coach`, or
the user themselves -- can read back instead of starting over.

## Step 1: Get the team from whatever source is given

- **Chained from `team-builder-doubles`/`team-builder-singles`**: use the
  team it just presented (Step 7's table) directly, plus the intent/win
  condition and speed-control or hazard/momentum plan it stated -- that
  context is worth keeping, not just the six species.
- **One or more screenshots of the in-game team screen**: Pokemon
  Champions' team view splits across two tabs per Pokemon --
  ability/item/moves on one, base stats with nature arrows (an
  up-highlighted stat is boosted, a down/dim one is lowered) and EV
  investment on the other. If the user only pastes one tab, work with it
  and say plainly what's missing (e.g. "I have moves and items, but not
  nature/EVs -- paste the stats tab too if you want those saved") rather
  than guessing the rest or stalling on it. The header bar's team name/ID
  field (if visible) is worth capturing as a label even though its value
  can't be decoded into contents -- it's just useful for the user to
  cross-reference against the game later.
- **Pasted text, a table, or a rough description**: use it as given; ask
  only for pieces that are genuinely missing and needed (see Step 2).

## Step 2: Pin down each Pokemon precisely

For each of the (up to six) Pokemon, resolve: species, ability, held item,
gender (if shown/relevant), its moves, and nature/EVs if available. Match
localized names (the game may be in any language, including screenshots
in non-English UI) to the canonical English species/move/ability/item
names used in `references/pokemon/` the same way `team-builder-doubles`
and `move-order-coach` already do -- don't let a localized name cause a
mismatch or a skipped lookup. Where you're genuinely unsure of a match
(an ambiguous move/item name, an EV number whose scale isn't obvious from
the screenshot) say so explicitly and record it as uncertain rather than
silently picking a guess -- a wrong saved set is worse than an incomplete
one, since it'll get trusted at face value next time it's loaded.

Cross-check each species/item against `references/current-season.yaml`
and the active regulation's `references/rules/regulation-<id>.yaml` the
same way the team-builder skills do, and flag (don't block on) anything
that looks illegal or stale.

## Step 3: Write the team file

Create `saved-teams/` at the repo root if it doesn't exist yet. Save to
`saved-teams/<slug>.yaml`, where `<slug>` is a short kebab-case name --
use one the user gives, or propose one from the team's theme (e.g.
`trick-room-torkoal`) and let them adjust it. If a file with that slug
already exists and this is meant to be the same team updated (not a new
one), overwrite it and say so; if it's ambiguous whether this is an update
or a new team, ask.

Fields to include, leaving any genuinely unknown one out rather than
inventing a value:

```yaml
name: <slug>
format: doubles | singles      # if known
in_game_team_id: <string>      # if the user's screenshot/paste showed one
intent: <one line>             # win condition / speed-control or hazard plan, if known
pokemon:
  - species: <canonical name>
    gender: <if known>
    ability: <canonical name>
    item: <canonical name>
    moves: [<move 1>, <move 2>, <move 3>, <move 4>]
    nature: <if known>
    evs: {hp: .., atk: .., def: .., spa: .., spd: .., spe: ..}   # if known
    notes: <anything uncertain or worth flagging>
  # ... up to 6
saved_from: team-builder | screenshot | pasted-text
saved_on: <date>
```

## Step 4: Confirm and explain reuse

Tell the user the file path it was saved to, and how to use it again:
reference the team by its slug/name in a later session (this skill can
load it back by reading the file) or hand it directly to
`move-order-coach` for a specific matchup instead of re-describing the
team from scratch. If any field was left uncertain or missing in Step 2,
repeat that here so it doesn't get silently trusted later.

## Loading a saved team

When the user references a team by name/slug ("my rain team", "the one I
saved as trick-room-torkoal") instead of pasting a new one, look for
`saved-teams/<slug>.yaml` (fuzzy-match the name if the exact slug isn't
given) and read it back instead of asking the user to redescribe the team.
If no matching file exists, say so rather than guessing which team they
mean.

## Language handling

Respond in whatever language the user is using. As in the other skills,
Pokemon/move/ability/item names should be matched to their canonical
English form before writing the file (the reference YAML and other saved
teams are keyed that way), even if the user's screenshots or prose use a
different language's official localized names.
