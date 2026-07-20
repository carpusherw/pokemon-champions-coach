---
name: move-order-coach
description: >
  Works out what order actions resolve in during a Pokemon Champions turn --
  which Pokemon moves first, whether a priority move beats a faster
  opponent, whether a KO lands before the target can act, what a Trick Room
  or Tailwind flips. Use this whenever the user describes a board state or
  a matchup and asks things like "who moves first", "does my Scarf Landorus
  outspeed their team", "will Fake Out stop that", "what's the speed order
  this turn", "should I Trick Room here", or is generally trying to plan a
  turn or a team around speed control -- including when the board state is
  given as screenshot(s) of the in-game team screen rather than typed out.
  Also use it proactively when the user is deciding between two sets/items/
  EV spreads and the deciding factor is actually turn order, even if they
  didn't phrase it as a speed question.
  Draws on references/rules and references/pokemon for the current
  regulation's legal roster and stats instead of guessing them.
---

# Coach speed and move order

This skill answers "what happens first" questions for a Pokemon Champions
turn: priority brackets, Speed stat comparisons under whatever modifiers are
in play, and — because real games are played with incomplete information —
reasonable meta-informed guesses when the user doesn't know the opponent's
exact set.

Read `reference/speed-mechanics.md` before working through a turn if you
haven't already loaded it this conversation — it has the full priority
bracket ordering and the list of Speed-modifying items/abilities/effects.
Don't try to reconstruct that from memory each time; it's easy to get a
priority tier or a multiplier wrong under pressure and confidently wrong is
worse than checking.

## Step 1: Get the board state

You need, for each relevant Pokemon: species, the move(s) being considered,
and ideally item/ability/relevant stat boosts/status. Field state matters
too: weather, terrain, Trick Room, Tailwind, any Speed-altering hazards
(Sticky Web) already in play.

If the user pastes screenshot(s) of the in-game team screen instead of
typing the board out, read them with the same extraction discipline
`team-recorder` documents in its own Step 1-2 (the ability/item/moves tab
and the stats tab with nature arrows and EV investment, localized names
matched to canonical ones) -- don't re-derive that procedure separately
here, it's the same screenshots either skill would be reading. Answer the
actual move-order question first; only after that, if you ended up with a
full team's worth of data this way, mention that `team-recorder` can save
it so it doesn't have to be re-read from screenshots next time -- don't
make saving a prerequisite to answering.

If the user gives you a full team sheet or battle log, work from that. If
they instead reference a team by name ("does my Trick Room team beat
this", "using the rain-core team I saved"), look in `saved-teams/`
(`team-recorder` writes these, best-effort, when a persistent local
filesystem is available) for a matching `<slug>.yaml` — fuzzy-match the
name against the slugs there, the same way `team-recorder`'s own loading
step does, rather than treating what the user said as a literal filename —
and read it back instead of asking them to redescribe six Pokemon that are
already on file. If no matching file exists, that doesn't mean the user
never saved the team — this environment may just not have that file (e.g.
a different device, or an ephemeral session) — so ask them to paste back
the team card `team-recorder` gave them instead of assuming from scratch.
If they only give you a partial
picture ("I have a Scarf Raichu, what beats it?"), that's fine — reason
about it explicitly as a range of cases rather than silently assuming the
gaps. Don't ask a battery of clarifying questions before giving any answer;
give the best answer you can from what you have, and flag the specific
missing piece if it would flip the outcome.

## Step 2: Look up stats, don't reconstruct them from memory

Pull each Pokemon's base Speed, ability, and (if relevant) Mega Evolution
data from `references/pokemon/<species>.yaml`. This is faster and more
reliable than recalling stats from general knowledge, and it's already
regulation-checked.

- If a species isn't in `references/pokemon/` yet, that's a coverage gap,
  not a dead end: say so, then fall back to your own knowledge of that
  Pokemon's stats if you're confident in them (most are stable, well-known
  facts), clearly flagged as "not from the local reference — verify." Don't
  block the whole answer on one missing file.
- Cross-check the species is actually legal in the current regulation via
  `references/current-season.yaml` and the matching `references/rules/
  regulation-<id>.yaml` — a set built around a Pokemon that got rotated out
  isn't useful advice. If references look stale, say so and suggest running
  the refresh-references skill, but still answer the actual question with
  what you have.
- Same check applies to items: before treating a held item as in play
  (either one the user stated, or a hypothetical like "what if it's Choice
  Specs"), check `held_items.reference_file` (e.g.
  `references/rules/items-m-b.yaml`) for the current regulation. Some
  mainline VGC/Showdown staples aren't actually implemented in Pokemon
  Champions yet (Choice Specs and Choice Band as of the last check) — flag
  that instead of computing a speed/damage line for an item that can't
  actually be held in-game.

## Step 3: Work out priority, then Speed, in that order

1. Identify each action's priority bracket (base move priority, plus
   Prankster/Gale Wings/Triage-style ability boosts if relevant). Group
   actions by bracket — the highest bracket resolves in full before the
   next one even starts.
2. Within a bracket, compute each actor's *effective* Speed: base Speed ×
   every applicable modifier (item, ability, stat stages, Tailwind,
   paralysis, hazards) — see the reference file's full list. Show this
   arithmetic when it's not obvious; a bare "X goes first" is much less
   useful than "X's effective Speed is 110 × 1.5 (Scarf) = 165, Y is 130
   unboosted, so X goes first" because the user can sanity-check and reuse
   the reasoning.
3. If Trick Room is up, reverse the within-bracket order (lowest effective
   Speed first) — but priority brackets still take precedence over Trick
   Room, don't let that slip.
4. Call out speed ties explicitly as a coinflip rather than picking a
   winner arbitrarily.

## Step 4: Fold in "current meta" when the set isn't fully known

This is the part that separates this skill from a plain calculator. When
the user doesn't know an opponent's exact item/EVs/ability:

- Use the target Pokemon's `notes` field in its reference YAML if it
  mentions a common set or role (e.g. "commonly Scarfed", "usually runs
  Trick Room support").
- If the reference notes don't cover it, a quick WebSearch for the
  Pokemon's current competitive usage (e.g. "<Pokemon> Pokemon Champions
  Regulation <id> common set") is reasonable when the outcome genuinely
  hinges on it and it's a Pokemon likely to show up in real games — don't
  do this for every single mon in a hypothetical, only when it actually
  changes the answer.
- When you're genuinely uncertain, present it as a branch: "if it's
  Scarfed, X happens; if it's running max-Speed uninvested, Y happens" is a
  more useful answer than silently guessing one and stating it as fact.

## Step 5: Give a clear, resolved answer

State the turn order plainly (a short numbered list is usually clearest for
more than two actions), then the specific thing the user actually asked
(does the KO land first, does Fake Out flinch before the target acts, etc).
Keep the arithmetic available but don't let it bury the actual answer at
the top.

## Language handling

Respond in whatever language the user is using — that's native to how you
work and doesn't need special handling for the prose. The one thing to
watch is **Pokemon, move, and ability names**: a user writing in Spanish,
Japanese, French, etc. may use that language's official localized name
(these are often not close transliterations — e.g. Japanese Pokemon names
frequently differ completely from English ones). The reference YAML files
are keyed by English/canonical names. When you recognize a localized name,
match it to the canonical entry before looking anything up, and it's fine
to use the user's localized name back in your response — just don't let a
name mismatch cause you to silently look up the wrong Pokemon or fail to
find one that's actually in the references. If you're not sure which
species a localized name refers to, ask or say what you're assuming.
