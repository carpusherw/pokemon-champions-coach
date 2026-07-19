<!--
Compiled by agents/gemini/pokemon-champions-coach/scripts/build_knowledge_bundle.py
from the canonical data in references/. Do not hand-edit this file -- edit the
source (references/, or agents/claude/.../speed-mechanics.md) and re-run the
build script instead, or your changes will be overwritten and CI's
knowledge-bundle-guard will flag the file as stale anyway.
-->

# Archetype skeletons

<!-- Sourced from Smogon's long-running singles teambuilding tradition
(Teambuilding Guide, Synergy and Cores, hazard-stacking and VoltTurn
resources on Smogon Forums, plus "Building Hyper Offense in OU" and "A
Guide to Stallbreakers" on Smogon University) and Pokemon Champions-specific
singles usage/tiering sources (Pokékipe's Champions OU pages, Smogon's
Pokemon Champions BSS Viability Rankings thread) via web search on
2026-07-19. These are stable structural patterns from decades of mainline
singles metagames and predate any single regulation set -- treat the
roles/order below as solid, and always re-check which specific species fill
each role against the *current* regulation's legal roster in
references/pokemon/ rather than assuming a classic example is actually
legal in Pokemon Champions right now. -->

Each entry below is a skeleton of roles, roughly in priority order for what
to lock in first when building that archetype from scratch. These aren't
exhaustive species lists -- cross-reference the roles against
`references/pokemon/` for what's actually legal and any competitive `notes`
already on file.

## Hyper Offense

The plan: set hazards, chip the opposing team down with wallbreakers and
setup sweepers, then send in a cleaner once the opposition is weak enough
to not survive a hit.

1. **A Stealth Rock setter**, ideally one that can also apply early
   offensive pressure rather than being pure dead weight once hazards are
   down.
2. **A secondary hazard setter** (Spikes, Toxic Spikes, or Sticky Web) if
   the team is actually committing to hazard stacking as part of its win
   condition, rather than just running Stealth Rock as a formality.
3. **1-2 wallbreakers** -- high raw power, usually a boosting item or a
   setup move, meant to weaken the opponent's bulkiest answers early-to-mid
   game so they can't just wall the team's actual win condition.
4. **A setup sweeper** as the win condition itself -- the Pokemon the whole
   team exists to get a clean setup opportunity for.
5. **A cleaner** for the endgame -- fast, hard-hitting, ideally with
   priority access, to finish a weakened team after hazards and
   wallbreakers have done their job.
6. **Hazard-stack support**, if applicable -- a spinblocker (commonly a
   Ghost-type) or a Defiant/Competitive user punishes the opponent's hazard
   removal attempts, which matters a lot more here than on other
   archetypes since the whole plan leans on hazards staying up.

## Bulky Offense / VoltTurn

The plan: keep tempo and chip damage through constant pivoting, forcing the
opponent into worse and worse positioning until a win condition can clean
up.

1. **A fast U-turn user** and **a fast Volt Switch user** -- these keep
   momentum by pivoting out of good matchups into the next piece before the
   opponent can capitalize.
2. **A hard-hitting U-turn user** and **a hard-hitting Volt Switch user** --
   same pivoting principle, but built to actually threaten damage on the
   way out rather than just scouting.
3. **A Stealth Rock setter** -- the constant switching this archetype
   generates (on both sides) makes hazard chip add up fast.
4. **A hazard remover** -- the team forces a lot of switches into hazards
   too, on its own side, so this archetype needs removal more than most.
5. **A win condition that benefits from the chip** this archetype
   generates -- a sweeper or wallbreaker that can capitalize once the
   constant pivoting has worn down the opponent's answers.

## Balance

Not built around a single shared gimmick -- mixes offensive and defensive
pieces for a team that can play multiple ways depending on the matchup.

1. **Start with a breaker** (a Pokemon strong enough to force progress
   against the current metagame), **then choose a pivot that answers the
   breaker's own checks** -- repeat this pattern (pick the next piece to
   cover what threatens the previous one) rather than picking 6 individually
   strong Pokemon and hoping they combine into a plan.
2. **Roughly**: 0-1 sweepers, 1-2 breakers, 1 stallbreaker (something that
   can punch through a wall/stall matchup specifically), 2-3 pivots or
   walls, 1 Stealth Rock setter, 1 hazard remover. Not a rigid quota --
   a guide for what's usually missing if the team feels thin.
3. **Defensive synergy and momentum are the actual foundation** here --
   prioritize pieces that can freely pivot into a wide slice of the
   metagame over pieces that are merely individually powerful.

## Stall

The plan: outlast the opponent, wearing them down with entry hazards and
residual damage while denying them any real progress.

1. **A Wish-passer / Cleric** -- sustain is the core resource stall is
   built around; without reliable recovery being passed around the team,
   residual damage kills the user as fast as the opponent.
2. **A Stealth Rock setter** plus **a secondary hazard setter** (Spikes/
   Toxic Spikes) -- hazards are stall's actual offense, not a courtesy
   addition.
3. **A Defogger or Rapid Spinner** -- stall needs to control the hazard
   war on both sides, since it can't afford to also take hazard chip while
   trying to win a war of attrition.
4. **A Phazer** (Whirlwind/Roar/Dragon Tail) -- prevents the opponent from
   ever getting a clean setup turn, and doubles as extra hazard damage by
   forcing switches.
5. **Useful extras**: a Taunt user (stops opposing setup and hazard-laying
   in its tracks), a grounded Poison-type (absorbs Toxic Spikes so it never
   goes active), and a spinblocker (protects the team's own hazards from
   being cleared) -- not all mandatory, but each patches a specific,
   well-known stall weakness.
