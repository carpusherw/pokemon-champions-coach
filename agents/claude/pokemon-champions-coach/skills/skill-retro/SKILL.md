---
name: skill-retro
description: >
  Reviews how this plugin's own coaching skills (refresh-references,
  move-order-coach, and any future skill added here) actually performed --
  wrong or stale data, a bad turn-order call, an unhelpful non-answer, a
  skill that fired when it shouldn't have or stayed silent when it should
  have helped -- and turns real, specific problems into GitHub issues on
  this repo so they get fixed instead of forgotten. Use this whenever the
  user explicitly asks for it: "log this as a skill issue," "file issues
  for what went wrong," "what should we improve about these skills," "check
  the feedback log," or similar. Also use it when the user pastes or
  describes a real Pokemon Champions battle result or ruling that
  contradicts something a skill said, even in an unrelated past
  conversation -- that mismatch is exactly the kind of concrete signal this
  skill exists to capture. Bring this up proactively near the end of a
  conversation, but only if a coaching skill actually stumbled during it
  (the user corrected it, seemed confused by its answer, or it visibly
  guessed at something it shouldn't have) -- don't offer this after every
  routine, successful use of a skill; that would make it as annoying as the
  over-eager auto-triggering this skill exists to help prevent.
---

# Skill retrospective

The other skills in this plugin (`refresh-references`, `move-order-coach`)
get better the same way anything does: someone notices a specific failure,
writes it down precisely enough to act on, and someone (usually a future
Claude session, maybe with `skill-creator`) fixes it. This skill is that
noticing-and-writing-down step, applied to *this plugin's own skills*
rather than to Pokemon Champions itself.

The two things that make this useful instead of noisy:

1. **Every finding is a concrete failure, not a vibe.** "Move-order-coach
   could be more thorough" isn't actionable. "Asked whether a Scarf
   Raichu outspeeds a Choice Specs Hydreigon; the skill answered using
   Raichu's Kantonian base Speed but the user's team sheet clearly listed
   Alolan Raichu, and it didn't check `raichu-alola.yaml`" is something a
   future session can actually go fix. If you can't state a finding as a
   specific input that produced a specific wrong (or missing, or annoying)
   output, it's not ready to file yet -- dig deeper or drop it.
2. **Filing is never silent.** Draft what you'd file, show it to the user,
   and only actually create anything after they've said yes. This skill's
   whole purpose is to open issues, but that's still a GitHub-visible
   action on someone else's repo activity feed, and the user should always
   see the exact title/body before it goes out.

## Step 1: Gather findings

Depending on what triggered this:

- **Something just went wrong in this conversation** -- look back over what
  actually happened: what did the user ask, what did the skill say or do,
  what turned out to be wrong or unhelpful, and how do you know (did the
  user correct it, did a later message contradict it, did the user have to
  ask again because the first answer didn't land)?
- **The user pasted a battle result, ruling, or other real-world fact that
  contradicts something a skill said** -- treat the pasted fact as ground
  truth and work backward: which skill or reference file produced the
  wrong claim, and why (stale data, a missed form/variant, a bad speed-tier
  assumption, a misread rule)?
- **The user wants a general review** -- read
  `feedback-log.md` in this skill's folder for notes logged since the last
  retro (see "Logging a quick note" below), and ask the user directly if
  anything else has been bugging them about how these skills behave that
  hasn't been written down yet.

Resist the urge to pad the list. Two or three specific, well-diagnosed
findings are worth far more than ten vague ones, and a retro that turns up
nothing real is a fine outcome -- say so and stop.

## Step 2: Write each finding as a draft issue

For each distinct problem, draft:

- **Title**, prefixed with the affected skill's name in brackets, e.g.
  `[move-order-coach] Uses Kantonian Raichu stats even when the team sheet says Alolan`.
  (This repo doesn't have per-skill GitHub labels set up, so the bracket
  prefix is what makes these filterable/searchable instead.)
- **Body**, covering:
  - What happened: the actual input/prompt and the actual (wrong) output.
  - Why it's wrong: what should have happened instead, and how you know.
  - Likely root cause, if you can tell (e.g., "the skill's description
    doesn't mention regional forms" vs. "the reference file itself has
    stale data" vs. "this looks like a one-off, not a pattern").
  - A suggested fix, if one's apparent -- but it's fine to leave this to
    whoever picks up the issue if you're not sure.
- **Label**: `bug` for "the skill did something factually wrong or
  unhelpful," `enhancement` for "the skill did nothing wrong but could
  clearly do better" (e.g., a coverage gap it already flagged honestly).

## Step 3: Check for duplicates before drafting anything new

Search this repo's open issues for similar titles/content (the bracket
prefix makes this easy -- search for `[skill-name]` plus a keyword from the
problem). If a close match exists, plan to add a comment to it with the
new occurrence instead of opening a duplicate -- a second data point on an
existing issue is more useful than a fragmented second issue anyway.

## Step 4: Show the user the drafts and get a go-ahead

Present each draft (title + body + label + whether it's new or a comment
on an existing issue) before filing anything. Let the user approve
everything, approve some and drop others, or ask you to edit the wording.
Only move to Step 5 once they've actually said to proceed -- "here's what
I'd file, want me to go ahead?" is enough; you don't need a separate
confirmation per issue if they green-light the batch.

## Step 5: File

Create the approved issues (or add the approved comments to existing
ones) in this repo. Then remove or check off the corresponding entries in
`feedback-log.md` so they don't get re-surfaced next retro.

## Step 6: Report back

Tell the user what was filed or commented on, with links, and anything you
deliberately decided *not* to file and why (e.g., "this looked like a
one-off, not worth an issue unless it happens again").

## Logging a quick note without doing a full retro

If the user just wants to flag something in passing mid-conversation
("yeah that speed calc was off, note that for later") without stopping to
do a whole retro right now, append a short entry to `feedback-log.md`
(what happened, which skill, one line) and keep going with whatever else
they're doing. The full Step 1-6 flow is for when someone actually wants to
turn accumulated notes (or a fresh, serious finding) into tracked issues --
don't force it every time something minor comes up.
