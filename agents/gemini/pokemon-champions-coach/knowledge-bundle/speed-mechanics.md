<!--
Compiled by agents/gemini/pokemon-champions-coach/scripts/build_knowledge_bundle.py.
Do not hand-edit this file -- most bundle files come from references/, but
this one may instead be a copy of a skill's own reference/*.md file (see
SPEED_MECHANICS_SOURCE, ARCHETYPES_DOUBLES_SOURCE, and ARCHETYPES_SINGLES_SOURCE
in build_knowledge_bundle.py for exactly which). Edit the actual source and
re-run the build script instead, or your changes will be overwritten and
CI's knowledge-bundle-guard will flag the file as stale anyway.
-->

# Turn-order mechanics reference

Core mainline-Pokemon battle mechanics that determine what happens in what
order during a turn. These rules are foundational to the whole franchise and
very unlikely to be reinvented by Pokemon Champions, but exact priority
integers have shifted slightly between generations in the past — treat the
**relative ordering** below as solid and the **exact numbers** as "best
available, verify Bulbapedia's Priority page if a specific integer matters
for a close call."

## 1. Priority bracket beats Speed, always

Every move has a priority value. All moves in a higher-priority bracket
resolve completely before any move in a lower bracket, regardless of Speed
stat — a level 50 Musharna (29 base Speed) using a +1 priority move goes
before a maxed-out Speed sweeper using a normal move. Only within the same
priority bracket does Speed (or Trick Room) decide order.

Functional groups, roughly highest to lowest priority (see caveat above on
exact numbers):

1. **Helping Hand** (~+5) — resolves before the ally's boosted move.
2. **Full-team/self protection moves** (~+4): Protect, Detect, Endure, Spiky
   Shield, Baneful Bunker, King's Shield, Obstruct, Silk Trap, Burning
   Bulwark, Mat Block, Quick Guard, Wide Guard, Crafty Shield.
3. **Redirection and Fake Out tier** (~+3): Follow Me, Rage Powder, Ally
   Switch, Fake Out (first-turn-out flinch move).
4. **Enhanced-priority attacks** (~+2): Extreme Speed, Feint (also punches
   through Protect), First Impression/Ambush.
5. **Standard priority attacks and Prankster-boosted status** (+1): Quick
   Attack, Aqua Jet, Bullet Punch, Ice Shard, Mach Punch, Shadow Sneak,
   Sucker Punch (fails if the target isn't using a damaging move that
   turn), Vacuum Wave, Water Shuriken, Accelerock, Grassy Glide (only while
   Grassy Terrain is active). Also: **any status move used by a Pokemon
   with the Prankster ability** gets +1 priority this way — this is a very
   relevant speed-control tool (Grimmsnarl, Whimsicott, Klefki, etc.), and
   note that since Gen 7, Prankster-boosted status moves fail against
   Dark-type targets.
6. **Normal priority (0)** — the vast majority of moves. Order within this
   bracket is entirely Speed-based (see below).
7. **Mildly negative priority**: a handful of moves like Vital Throw.
8. **"Charge and resolve last" moves** (very negative): Focus Punch, Beak
   Blast, Shell Trap — these can be interrupted (Focus Punch fails if hit
   before it resolves) and always act near the end of the turn.
9. **Counter-attack moves** (very negative): Counter, Mirror Coat, Mirror
   Move — must resolve after the opponent has already acted this turn.
10. **Forced-switch moves** (near the bottom): Roar, Whirlwind, Dragon Tail,
    Circle Throw.
11. **Trick Room** (the move itself, not the lingering field effect) is
    among the lowest priority in the game — it goes very last the turn it's
    used, then its field effect applies starting next turn.

## 2. Within a priority bracket: Speed stat decides, fastest first

...unless the **Trick Room** field effect is active, in which case order is
**reversed within each priority bracket** (slowest effective Speed acts
first). Trick Room does NOT touch the priority-bracket ordering above —
a +1 priority move still goes before a 0-priority move even under Trick
Room; Trick Room only flips the tiebreak *within* a bracket.

Effective Speed for ordering purposes is the Pokemon's Speed stat **after**
all of the following are applied, not its raw base stat:

- **Stat stages**: Speed-boosting moves/abilities (Dragon Dance, Agility,
  Rock Polish, Autotomize, Speed Boost) and team-wide Tailwind (2x Speed for
  the team, 4 turns) versus Speed-lowering effects (Sticky Web -1, Icy Wind,
  Electroweb, Scary Face, Cotton Spore, String Shot, an opponent's
  Intimidate does NOT affect Speed — that's Attack only, don't mix them up).
- **Mega Evolution locks the item slot**: a Pokemon must be holding its
  species-specific Mega Stone to Mega Evolve at all, and can't hold anything
  else instead — so "what if this Mega held a Choice Scarf/Band/Specs"
  hypotheticals actually mean "what if this Pokemon never Mega Evolved."
  Answer those as base-form-with-that-item, not Mega-form-with-that-item,
  and say so explicitly since it's an easy premise to miss.
- **Held items**: Choice Scarf (1.5x), Iron Ball (0.5x, and grounds the
  holder), Quick Powder (2x, Ditto only).
- **Abilities that key off weather/terrain**: Chlorophyll (2x in Sun), Swift
  Swim (2x in Rain), Sand Rush (2x in Sandstorm), Slush Rush (2x in
  Snow/Hail), Surge Surfer (2x in Electric Terrain), Unburden (2x the turn
  after losing its held item, until it holds an item again), Quick Feet
  (1.5x while statused — and this also bypasses the paralysis Speed drop
  below), Slow Start (0.5x for its first 5 turns out).
- **Status**: Paralysis halves Speed (0.5x) in modern generations (older
  generations used 0.25x — verify which generation's numbers Champions
  actually uses if this matters for a close call). Paralysis also carries a
  25% chance to not move at all regardless of speed order — worth flagging
  as a real outcome, not just an ordering nuance.
- **Speed ties**: if two Pokemon end up with identical effective Speed in
  the same priority bracket, the game picks randomly between them (all
  speed-tied actors are shuffled together in doubles, not just a coin flip
  between two). Say so explicitly rather than picking one arbitrarily.

## 3. What "current meta" adds on top of raw mechanics

The mechanical rules above are deterministic given full information, but in
a real game you often don't know the opponent's exact item, EV spread, or
ability going in. This is where "based on current meta" comes in — see
SKILL.md's Step 2 for how to fold that uncertainty into a coaching answer
instead of pretending to know things you don't.
