<!--
Compiled by agents/gemini/pokemon-champions-coach/scripts/build_knowledge_bundle.py.
Do not hand-edit this file -- most bundle files come from references/, but
this one may instead be a copy of a skill's own reference/*.md file (see
SPEED_MECHANICS_SOURCE, ARCHETYPES_DOUBLES_SOURCE, and ARCHETYPES_SINGLES_SOURCE
in build_knowledge_bundle.py for exactly which). Edit the actual source and
re-run the build script instead, or your changes will be overwritten and
CI's knowledge-bundle-guard will flag the file as stale anyway.
-->

# Archetype skeletons

<!-- Sourced from general VGC/Pokemon Champions teambuilding methodology (the
"idea -> core -> mode" framework popularized by VGC Guide/Wolfe
Glick/Aaron Traylor/Aaron Zheng, plus widely-repeated Trick Room and
weather-team guides from PokeStats, Smogon, and VGC-focused sites) via web
search on 2026-07-19. These are stable structural patterns that predate
and outlive any single regulation set -- treat the roles/order below as
solid, and always re-check which specific species fill each role against
the *current* regulation's legal roster in references/pokemon/ rather than
assuming a classic example (e.g. a specific mainline Trick Room setter)
is actually legal in Pokemon Champions right now. -->

Each entry below is a skeleton of roles, roughly in priority order for what
to lock in first when building that archetype from scratch. These aren't
exhaustive species lists -- cross-reference the roles against
`references/pokemon/` for what's actually legal and any competitive `notes`
already on file.

## Trick Room

Trick Room teams invert normal Speed order for 5 turns so the team's own
slow, hard-hitting Pokemon act first.

1. **At least two Trick Room setters.** Never rely on a single setter --
   if it's KO'd or the room gets Taunted/disrupted before it's up, the whole
   plan collapses. Look for bulky support Pokemon that can survive to set
   Trick Room even under pressure.
2. **Slow, hard-hitting abusers.** These want the *lowest* practical Speed
   (0 Speed IVs, a Speed-hindering nature) so they reliably act first once
   the room is up, paired with real power (high base Attack/Special Attack,
   Choice items or setup moves) since they'll usually only get a few turns
   inside Trick Room to close out the game.
3. **A secondary speed-control answer for non-Trick-Room turns.** Trick
   Room only lasts 5 turns and can be removed early -- include something
   that still functions once it's down (a fast attacker, or a Tailwind
   setter as a second gear) rather than building a team that's helpless the
   moment the room ends.
4. **Setter protection.** A Fake-Out user of your own (to stop the
   opponent's Fake Out from interrupting your setter) and/or a Mental Herb
   on at least one setter (to guarantee the room goes up even through
   Taunt) are standard insurance, not optional flavor.

## Tailwind / hyper offense

Tailwind doubles the team's Speed for 4 turns, aiming to bury the opponent
before it drops.

1. **A fast, reliable Tailwind setter** -- ideally one that can act early
   even without Tailwind up yet (a Prankster user setting it as a
   status move is a common pattern since Prankster's priority boost doesn't
   need Tailwind to go first).
2. **Support that protects the setter and the tempo**: a Fake Out user
   and/or redirection (Follow Me/Rage Powder) to keep the setter alive
   through the first couple of turns.
3. **Fast wallbreakers built to abuse the Tailwind window** -- the whole
   point of the archetype is doing as much damage as possible in the 4
   turns Tailwind is up, so this is where raw power belongs.
4. **A plan for after Tailwind drops.** Same principle as Trick Room's
   "mode" slot: at least one piece that isn't dead weight once the Speed
   boost expires, since a team that only works during Tailwind gives the
   opponent an obvious win condition (survive the burst, then win the slow
   game after).

## Weather (Sun / Rain / Sand / Snow)

Weather teams commit a field condition for the whole team to abuse.

1. **A reliable weather setter**, ideally via an auto-weather ability
   (Drought for Sun, Drizzle for Rain, Sand Stream for Sand, Snow Warning
   for Snow) rather than a move that only lasts a few turns, so the weather
   is up from turn one without spending an action.
2. **Weather-boosted Speed abusers** -- the signature payoff of a weather
   team is a normally-mid-Speed attacker suddenly outrunning most of the
   format: Chlorophyll (Sun), Swift Swim (Rain), Sand Rush (Sand), Slush
   Rush (Snow), all doubling Speed while their weather is active.
3. **Weather-boosted attacks/typing.** Fire-type STAB and Solar Beam-style
   moves in Sun; Water-type STAB and Thunder's perfect accuracy in Rain;
   Rock-types getting a Special Defense boost in Sand (and immunity to Sand
   damage); Ice-types getting a Defense boost in Snow. Build the attacking
   core around whichever of these the chosen weather actually grants.
4. **A hybrid "mode" answer for when the weather isn't up** -- a second
   speed-control tool (Trick Room and Sun/Chlorophyll is a well-known
   pairing, since both want a slow-looking attacker that's actually fast
   under the right condition) or at least one piece that isn't purely
   weather-dependent, for the same reason every archetype above needs a
   plan for its gimmick being unavailable.

## Balance / "goodstuffs"

Not built around a single shared gimmick -- instead prioritizes individually
strong, flexible Pokemon that each answer a wide slice of the metagame on
their own.

1. **Prioritize role compression over raw power** when choosing pieces --
   a Pokemon that's simultaneously a bulky pivot, a check to two or three
   common threats, and a secondary speed-control tool is worth more here
   than a specialist that does one thing extremely well but nothing else.
2. **Build check/counter coverage deliberately**, not by accident -- for
   each of the format's most common threats (see Step 6 of SKILL.md), have
   at least one team member that can reasonably answer it, even if no
   single member answers everything.
3. **Still needs an explicit speed-control plan** (Step 4 of SKILL.md) --
   "balance" doesn't mean "no plan," it means the plan is spread across
   multiple flexible pieces rather than concentrated in one archetype's
   dedicated setter.
4. **Consistency over ceiling.** Balance teams are usually chosen because
   they're reliable across many different opposing team styles rather than
   because they have the single highest win rate against the *most* common
   team -- weigh "does this lose badly to anything" more heavily than "does
   this beat the top team even harder."
