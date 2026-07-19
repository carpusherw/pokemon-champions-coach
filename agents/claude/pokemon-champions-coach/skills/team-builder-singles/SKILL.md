---
name: team-builder-singles
description: >
  Builds a Pokemon Champions battle team of 6 for the singles ranked ladder
  (sometimes called Champions OU or BSS/Battle Stadium Singles by the
  competitive community) from whatever starting point the user actually has:
  a specific Pokemon or small combo ("I want to build around Garchomp"), a
  loose idea or tactic ("I want a VoltTurn team", "I like the idea of a
  hazard-stacking team"), or a named archetype ("build me a stall team",
  "put together hyper offense", "I want a balance team"). Also use it when
  the user already has a partial team (1-5 Pokemon locked in) and wants help
  finishing it, fixing a hole, or picking the last slot(s), and for general
  singles teambuilding-process questions like "what's missing from this
  team" or "do I have hazard control". Do NOT use this for the doubles/
  VGC-style ranked ladder -- use `team-builder-doubles` instead, since doubles needs
  a genuinely different team structure (speed control, redirection, Fake
  Out) rather than just more Pokemon on the field. Do NOT use this for a
  single Pokemon's moveset/item/EV question in isolation ("what item should
  my Corviknight hold") -- that's a set-optimization question, not team
  construction, unless it's explicitly in service of finishing or fixing a
  6-Pokemon team. Draws on references/rules and references/pokemon for the
  current regulation's legal roster and stats, plus this skill's own
  reference/archetypes.md for known archetype skeletons, instead of guessing
  either from scratch.
---

# Build a singles team

Scope: the singles ranked ladder. For the doubles/VGC-style ladder, use
`team-builder-doubles` instead — singles teambuilding is its own tradition (hazard
control, pivoting, checks and counters) rather than a smaller version of
doubles, and reusing doubles archetypes (Trick Room, Tailwind, redirection)
here would be wrong more often than right.

This follows the same top-player teambuilding discipline as `team-builder-doubles`,
adapted for what actually matters in singles. Every team centers on a stated
**win condition** — the Pokemon or plan the whole team exists to enable —
and gets built out through **cores**: pairs or trios of Pokemon that patch
each other's holes through type synergy and check/counter coverage. Every
singles team also needs an explicit answer to the "boring but mandatory"
checklist items (entry hazards, hazard control, momentum) regardless of
archetype, because skipping them isn't a stylistic choice, it's a structural
hole.

Don't skip straight to listing 6 Pokemon. Making the reasoning at each step
explicit is what lets the user reconstruct or adjust the team later, and
lets them tell *why* a game was lost instead of just that it was.

## Step 0: Pin down the win condition / intent

Every team starts from one of three things:

- **A Pokemon or small combo** the user wants to use.
- **A tactic or move** they want to build around (e.g. "I want a VoltTurn
  team" -- U-turn/Volt Switch/Flip Turn users trading momentum -- or "I
  want to stack hazards").
- **A named archetype** (Hyper Offense, Balance, Stall, Bulky Offense/
  VoltTurn -- see `reference/archetypes.md` for what each actually needs to
  function).

If the user already told you which, say it back in one line and move on.
If it's genuinely vague, ask one focused question rather than guessing — a
wrong guess here derails everything downstream. If the user already has a
partial team (1-5 Pokemon locked), infer the shared theme/win condition from
what's already picked, state what you inferred so they can correct it, then
still run Step 1 against the locked Pokemon before continuing.

## Step 1: Confirm legality before picking anything

Check `references/current-season.yaml` and that regulation's
`references/rules/regulation-<id>.yaml`. The team-building rules (species
clause, item clause, 1-Mega-per-battle cap) apply the same way to singles as
to doubles — the regulation file itself notes its rules apply to both
ranked ladders unless stated otherwise, only matchmaking/rank progress are
separate.

One singles-specific wrinkle worth flagging to the user if it comes up:
this repo's `references/rules/` covers the *official in-game* ranked
ladder's legality, which (like doubles) has no separate ban list beyond the
regulation's own roster. If the user is instead building for a community-run
tier like "Champions OU" on a Pokemon Showdown-style simulator, that's a
*different*, stricter legality overlay (an Ubers cutoff and possibly other
tier-specific bans) layered on top of the base roster — ask which one they
mean rather than assuming, since it changes what's actually "legal."

Item legality has the same gap as the species roster: the regulation's
`held_items.reference_file` (e.g. `references/rules/items-m-b.yaml`) tracks
which held items actually exist in Pokemon Champions yet, separately from
the item clause's "no duplicates" rule. Don't recommend a mainline
VGC/Showdown staple (Choice Specs and Choice Band are the current known
gaps) without checking it's actually in that list first.

## Step 2: Work the win condition into a first Pokemon or two

- **From a Pokemon**: read `references/pokemon/<species>.yaml` for stats,
  abilities, and `notes`. Work out its role (wallbreaker, setup sweeper,
  bulky pivot, dedicated wall, hazard setter) from its stat spread, then
  what removing its checks and counters would take, and what it invites the
  opponent to bring in response. If a species isn't in
  `references/pokemon/` yet or its `notes` field is still a TODO, say so and
  fall back to your own knowledge, flagged as "not from the local reference
  -- verify."
- **From a tactic/move**: identify which currently-legal Pokemon can
  actually execute it well (a VoltTurn team needs real U-turn/Volt
  Switch/Flip Turn users with a good matchup into what they're switching
  into, not just any Pokemon that knows the move).
- **From an archetype**: read `reference/archetypes.md` for that
  archetype's role skeleton, then map each role onto currently-legal
  species — not everything in a general skeleton is necessarily legal this
  regulation.

## Step 3: Build the core (aim for 3-5 Pokemon)

Add the next most pivotal piece, then ask what *that* piece needs, and let
the answer drive the next pick. Judge every addition on:

- **Offensive core** — do two pieces' attacking types together threaten
  what would otherwise wall either one alone, opening a path through the
  opponent's defensive backbone.
- **Defensive core** — do two pieces cover each other's weaknesses well
  enough to freely pivot between them (a resists/is immune to what hurts
  the other), so the pair can absorb a much wider slice of the metagame
  than either could alone.
- **Checks and counters** — for the win condition specifically, what
  currently answers it, and does the rest of the core remove or wear those
  answers down? A win condition with no plan for its own checks is a
  Pokemon, not a team.
- **Role compression** — with only 6 slots total, a piece that does two or
  three jobs (e.g. a bulky pivot that's also the Stealth Rock setter) is
  worth more than a piece that does one job as well as two specialists
  would.

## Step 4: Handle the mandatory checklist -- hazards and momentum

Every singles team needs an explicit answer here, regardless of archetype:

- **Entry hazards.** Decide if the team has a Stealth Rock setter (close to
  mandatory in most singles metagames) and whether it's stacking further
  (Spikes, Toxic Spikes, Sticky Web) as part of the actual game plan or
  keeping it lean.
- **Hazard control stance.** Either the team removes the opponent's hazards
  (a Rapid Spin/Defog user, or reliance on Regenerator/Magic Bounce-style
  mitigation), or it's deliberately leaning into hazard stacking as a win
  condition — in which case it wants a spinblocker (commonly a Ghost-type)
  to protect its own hazards from being cleared. Pick one on purpose; "we
  never discussed hazards" is not a valid answer once the team is built.
- **Momentum.** Note whether the team has pivoting tools (U-turn, Volt
  Switch, Flip Turn, Teleport) to keep initiative, especially on a Balance
  or Bulky Offense build — a team that's constantly forced to play reactively
  gives up the tempo advantage those archetypes depend on.

See `reference/archetypes.md` for how this checklist's priority shifts by
archetype (Stall leans hardest on hazard control and a Phazer; Hyper
Offense leans hardest on hazard stacking and a cleaner).

## Step 5: Round out to 6 and close the archetype checklist

Use the remaining slot(s) to close out whatever `reference/archetypes.md`
flags as still missing for the chosen archetype (a Stall team without a
Cleric or Wish-passer, a Balance team without a stallbreaker), patch
whatever hole Step 3's synergy check turned up, and close out
species/item-clause bookkeeping from Step 1.

## Step 6: Threat-check the finished team against the current meta (relevance)

This repo doesn't track singles usage stats, so once the team is at or near
6, do a WebSearch (prefer it over WebFetch for these sources, same as
`team-builder-doubles`) for the current regulation's singles usage/viability
data — Pokékipe's Champions OU pages, Smogon's Pokemon Champions BSS
Viability Rankings thread, and PokeChamps' singles tier list are current
sources as of this writing. Check the team against the 3-5 most common
threats:

- Does something on the team check or counter it, or is there a structural
  gap (nothing that resists/switches into it safely, no reliable answer at
  all)?
- If there's a gap, look first for a set/item tweak on an existing member
  (role compression again) before assuming the team needs a slot it doesn't
  have.

Don't chase every threat in the tier — flag the 1-2 biggest structural risks
honestly rather than claiming the team is airtight.

## Step 7: Present the team

Give a short table: slot, Pokemon, role, and the one-line reason it's on
the team, tied back to the win condition from Step 0. Call out explicitly:

- The hazard/momentum plan from Step 4.
- Any data gaps flagged along the way (missing reference file, TODO notes
  field).
- The 1-2 threats from Step 6 the team is weakest against, and the most
  natural fix if the user wants to iterate further.

Offer to hand off to `move-order-coach` once they want to work out a
specific matchup's turn order, rather than trying to answer that here.

## Language handling

Respond in whatever language the user is using. The one thing to watch is
**Pokemon, move, and ability names**: the reference YAML files are keyed by
English/canonical names, so when a user writes in another language and uses
that language's official localized name (which is often not a close
transliteration), match it to the canonical entry before looking anything
up, and it's fine to use their localized name back in your response.
