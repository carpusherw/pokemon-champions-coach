---
name: team-builder
description: >
  Builds a Pokemon Champions battle team of 6 for the doubles/VGC-style
  ranked ladder from whatever starting point the user actually has: a
  specific Pokemon or small combo they want to use ("I want to build around
  Kingambit"), a loose idea or tactic ("I like the idea of a min-Speed team",
  "I want to abuse Fake Out + redirection"), or a named strategy/archetype
  ("build me a Trick Room team", "put together a Tailwind hyper offense
  team", "I want a Sun team"). Also use it when the user already has a
  partial team (1-5 Pokemon locked in) and wants help finishing it, fixing a
  hole, or picking the last slot(s), and when they ask general
  teambuilding-process questions like "what's missing from this team" or "does
  this team have a plan for Trick Room". Do NOT use this for the singles
  ranked ladder (sometimes called Champions OU or BSS) -- use
  `team-builder-singles` instead, since singles needs a genuinely different
  team structure (hazards, pivoting, checks/counters) rather than just fewer
  Pokemon on the field. Do NOT use this for a single Pokemon's moveset/item/EV
  question in isolation ("what item should my Corviknight hold") -- that's a
  set-optimization question, not team construction, unless it's explicitly in
  service of finishing or fixing a 6-Pokemon team. Draws on references/rules
  and references/pokemon for the current regulation's legal roster and
  stats, plus this skill's own reference/archetypes.md for known archetype
  skeletons, instead of guessing either from scratch.
---

# Build a team

Scope: the doubles/VGC-style ranked ladder. For the singles ladder, use
`team-builder-singles` instead — the two formats need genuinely different
team structures, not just a smaller battle party, so don't reuse this
skill's archetypes or steps there.

This follows the same process top VGC/Pokemon Champions players actually
use: every team starts from a stated **intent**, gets built out into a
**core** that fully expresses that intent, then gets a **mode** added — one
or two final Pokemon that give the team a second gear for situations the
core alone can't handle. Throughout, a team gets judged on three things:
**synergy** (do the pieces cover each other's weaknesses and enable each
other's strengths), **consistency** (does the plan work reliably, or does it
need too many specific things to go right), and **relevance** (how does it
actually fare against what people are bringing to the current regulation).

Don't skip straight to listing 6 Pokemon. The value of this skill is in
making the reasoning at each step explicit enough that the user could
reconstruct or adjust it later — a team is much easier to pilot and fix when
you know *why* each slot is there.

## Step 0: Pin down the intent

Every team starts from an idea, and that idea is always one of three things:

- **A Pokemon or small combo** the user wants to use.
- **A tactic or move** they want to build around (e.g. "I want a team that
  abuses Follow Me + a hard-hitting partner", "I want to run double Fake
  Out").
- **A named strategy/archetype** (Trick Room, Tailwind/hyper offense, a
  weather team, sand, balance/"goodstuffs" — see `reference/archetypes.md`
  for what each of these actually needs to function).

If the user already told you which of these it is, say so back to them in
one line and move on — don't interrogate something that's already clear.
If the idea is genuinely vague ("I want something fun and different"), ask
one focused question to convert it into something concrete enough to build
from (a Pokemon, a tactic, or an archetype) rather than silently picking one
for them. A wrong guess here derails every later step, so this is the one
place worth pausing to confirm rather than plowing ahead.

If the user already has a partial team (1-5 Pokemon locked), the intent is
implicit in what they've already picked — infer the shared theme from those
Pokemon's roles/types/abilities, state what you inferred so they can correct
it if you're off, then still run Step 1 (checking the already-locked Pokemon
against it too, not just species picked later) before continuing to Step 2.

## Step 1: Confirm legality before picking anything

Check `references/current-season.yaml` for the active regulation, then that
regulation's `references/rules/regulation-<id>.yaml` for the rules that
constrain every legal team:

- `team_building_rules.species_clause` — no two Pokemon sharing a national
  dex number (alternate forms of the same species count as the same
  species).
- `team_building_rules.item_clause` — no two Pokemon holding the exact same
  item, including duplicate Mega Stones.
- `team_building_rules.mega_evolution.max_per_battle` — a team can carry more
  than one Mega Stone, but only one Pokemon can actually Mega Evolve in a
  given battle, so a team built around two simultaneous Mega Evolutions
  isn't legal no matter how good it looks on paper.
- `legality.currently_excluded_categories` and the regulation's roster —
  don't build around a species that isn't legal yet or got rotated out.

If references look stale (regulation looks old, a species you'd expect to
see is missing), say so and suggest `refresh-references`, but keep working
with what's there rather than blocking the whole build on it.

## Step 2: Work the intent into a first Pokemon or two

How this looks depends on the starting point from Step 0:

- **From a Pokemon**: read `references/pokemon/<species>.yaml` for its
  stats, abilities, and `notes` field instead of recalling them from
  memory. Work out its role from its stat spread (fast attacker, bulky
  pivot, dedicated speed-control support, etc.), then what it structurally
  needs from teammates — what it's weak to that it can't handle alone, what
  it invites the opponent to bring, what Speed tier it actually sits at. If
  a species isn't in `references/pokemon/` yet or its `notes` field is still
  a TODO placeholder, say so and fall back to your own knowledge, flagged as
  "not from the local reference — verify."
- **From a tactic/move**: identify the specific Pokemon that can actually
  execute the tactic well under the current regulation (e.g. "double Fake
  Out" needs two legal Fake Out users with the bulk/priority-order to both
  land it) — this is the "intent" step made concrete, so don't leave it as
  an abstract tactic once you're picking Pokemon.
- **From an archetype**: read `reference/archetypes.md` for that archetype's
  skeleton (what roles it needs filled and in what rough order of
  priority), then map each role onto currently-legal species — not
  everything in a general archetype skeleton will actually be a legal
  species this regulation, so check as you go rather than assuming.

## Step 3: Build out the core (aim for 3-5 Pokemon)

Repeat: pick the next most pivotal piece the intent needs, add it, then ask
"what does *this* need to function" and let that answer the next pick.
Stop once the core actually finishes expressing the stated idea — that's
usually 3-5 Pokemon, not all 6. At each addition, check:

- **Synergy** — offensive (does a new piece threaten what an existing piece
  struggles against) and defensive (can one switch into an attack that
  would hurt the other, without taking much itself). Two pieces that are
  merely both good in a vacuum aren't a core; a core is pieces that make
  each other better.
- **Consistency** — does this plan come together reliably, or does it need
  several specific things to go right in sequence (the right lead, the
  opponent not disrupting the one setter, etc.)? A flashier but fragile
  plan is often worse than a slightly duller, more reliable one.
- **Role compression** — with only 6 slots (and only 4 brought to an actual
  battle), a piece that does two or three jobs at once (e.g. a
  redirection/pivot Pokemon that's also a speed-control answer) is worth
  more than a piece that does only one job as well as two separate
  specialists would.

## Step 4: State the team's speed-control plan explicitly

Every team needs an answer to "who moves first and why" — decide this on
purpose instead of discovering it's missing mid-battle. The main options are
Trick Room, Tailwind, or "naturally fast enough that we don't need a
dedicated tool" (see `reference/archetypes.md` for what each implies for the
rest of the team). If the core from Step 3 doesn't already answer this,
Step 4 is where you pick it. Once battle-planning gets specific (an actual
board state, a specific matchup's Speed tiers), that's `move-order-coach`'s
job, not this skill's — hand off to it rather than re-deriving speed math
here.

## Step 5: Add the "mode" — final slot(s) that give a second gear

The last one or two Pokemon should take the team somewhere the core alone
can't go, not just be "another good Pokemon." Concretely: if the core is
fast-paced/Tailwind-based, a mode piece might still function once Tailwind
expires; if the core is Trick Room, a mode piece should be able to function
when Trick Room is down or gets removed — a team that only works inside its
own gimmick invites the opponent's entire gameplan to just be "stop, stall,
or reverse the gimmick." Use this slot to also patch whatever hole Step 3's
synergy check turned up, and to close out species/item-clause bookkeeping
from Step 1.

## Step 6: Threat-check the finished team against the current meta (relevance)

This repo's references don't track live usage stats, so once the team is at
or near 6 Pokemon, do a WebSearch (prefer it over WebFetch — the same major
VGC/Champions data sites that block direct fetches from sandboxed
environments usually come through fine via WebSearch's own synthesis) for
the current regulation's top Pokemon/cores — Pikalytics, PokeStats, and
Smogon's VGC strategy dex are good current sources for Pokemon Champions
usage data. Check the team against the 3-5 most common threats/cores you
find:

- Does something on the team already answer it, or is there a structural
  gap (nothing that can safely switch into it, no way to out-speed or
  out-priority it)?
- If there's a gap, look first for a set/item tweak on an existing member
  (role compression again) before assuming it needs a whole extra slot the
  team doesn't have.

Don't chase every possible threat — a team that tries to answer everything
answers nothing well. Flag the 1-2 biggest structural risks honestly rather
than pretending the team is airtight.

## Step 7: Present the team

Give a short table: slot, Pokemon, role, and the one-line reason it's on the
team, tied back to the intent from Step 0 so the reasoning is legible on its
own later (this is the same "intent" discipline top players use to evaluate
whether a team is actually performing as designed once they start playing
it, not just whether it looks good on paper). Call out explicitly:

- The stated speed-control plan from Step 4.
- Any data gaps flagged along the way (missing reference file, TODO notes
  field, a Mega whose competitive data wasn't confirmed).
- The 1-2 threats from Step 6 the team is weakest against, and what the
  most natural fix would be if the user wants to iterate further.

Offer to hand off to `move-order-coach` once they want to work out a
specific matchup's turn order, rather than trying to answer that here.

## Language handling

Respond in whatever language the user is using. The one thing to watch is
**Pokemon, move, and ability names**: the reference YAML files are keyed by
English/canonical names, so when a user writes in another language and uses
that language's official localized name (which is often not a close
transliteration), match it to the canonical entry before looking anything
up, and it's fine to use their localized name back in your response.
