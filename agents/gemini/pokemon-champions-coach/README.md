# Pokemon Champions Coach — Gemini Gem

Gemini Web/mobile has no plugin or skill-marketplace system like Claude
Code's. The only extensibility point is a **Gem**: one instructions blob,
plus up to 10 uploaded "Knowledge" files, created by hand in the Gem
Manager (gemini.google.com). Gems created there sync automatically to the
Gemini mobile apps (iOS/Android) on the same Google account -- there's no
separate mobile build step.

This folder packages the plugin's portable skills for that surface.
`references/` is still the single source of truth; nothing here duplicates
it by hand.

## What's here

- `gem-instructions.md` -- paste the contents (below the divider) into the
  Gem's Instructions field.
- `knowledge-bundle/` -- upload these 5 files under the Gem's Knowledge
  panel. Generated from `references/` (plus the skill-bundled reference
  files noted below) by `scripts/build_knowledge_bundle.py`; don't hand-edit
  them.
- `scripts/build_knowledge_bundle.py` -- regenerates `knowledge-bundle/`.

## Setting up the Gem (one-time)

1. Go to gemini.google.com -> Gem Manager -> New Gem.
2. Name it (e.g. "Pokemon Champions Coach") and paste `gem-instructions.md`'s
   content (everything after the `---` divider) into Instructions.
3. Under Knowledge, upload all 5 files from `knowledge-bundle/`.
4. Enable the Google Search grounding toggle if offered -- move-order
   coaching uses it for "what set does this Pokemon usually run" lookups
   when the reference notes don't cover it.
5. Save. It's now available in both Gemini Web and the Gemini mobile apps
   under Gems, no further setup.

## Keeping it current

Nothing here refreshes itself, and nothing here can write back to this
repo -- both are one-way, human-driven steps:

1. Regulation rotates or `references/` changes on the Claude side, same as
   today (`refresh-references` skill, Claude-only).
2. Run `python3 agents/gemini/pokemon-champions-coach/scripts/build_knowledge_bundle.py`
   and commit the result. CI (`knowledge-bundle-guard.yml`) fails any PR
   that changes `references/`, `speed-mechanics.md`, `archetypes.md`, or
   `singles-archetypes.md` without also regenerating this bundle, so this
   step can't silently get skipped.
3. In Gem Manager, remove the 5 old Knowledge files and upload the new
   ones (there's no Gems API to automate this upload).
4. If `agents/claude/.../move-order-coach/SKILL.md`, `.../team-builder/SKILL.md`,
   `.../singles-team-builder/SKILL.md`, or `.../skill-retro/SKILL.md` changed
   in a way that affects behavior (not just data), re-read it and hand-update
   `gem-instructions.md` too -- that file is a judgment-based condensation,
   not something CI can diff-check for correctness the way it checks the
   knowledge bundle.
5. If a **new** Claude skill gets added under `agents/claude/.../skills/`,
   add a row for it to the capability matrix below (even if the decision is
   "not ported, here's why") -- CI (`knowledge-bundle-guard.yml`) fails a PR
   that adds a skill with no matching row, so this can't silently get
   skipped either.

## Capability matrix vs. the Claude plugin

| Skill | Claude Code plugin | Gemini Gem |
|---|---|---|
| `move-order-coach` | Full — reads `references/` live | Full — reads the pre-built knowledge bundle instead of live files; otherwise same reasoning |
| `team-builder` | Full, doubles/VGC-style format only — reads `references/` live, threat-checks via WebSearch | Full, same doubles-only scope — reads the knowledge bundle (including `archetypes.md`) instead of live files; the meta threat-check step uses Google Search grounding if enabled for the Gem, otherwise it says plainly that step is skipped rather than guessing |
| `singles-team-builder` | Full, singles ladder only — reads `references/` live, threat-checks via WebSearch against singles usage/viability sources | Full, same singles-only scope — reads the knowledge bundle (including `singles-archetypes.md`) instead of live files; the meta threat-check step uses Google Search grounding if enabled for the Gem, otherwise it says plainly that step is skipped rather than guessing |
| `refresh-references` | Full — researches and writes back to `references/` | **Not ported.** Gems can't fetch-and-write repo files; stays a Claude-only maintenance task |
| `skill-retro` | Full — files/comments on GitHub issues after user go-ahead | **Draft-only.** Gems have no external API access, so it drafts the title/body/label and best-effort-checks for duplicates via Search, but the user must relay the draft to Claude or GitHub's UI to actually file it — it never claims to have filed anything |

## Known limitations

- **10-file Knowledge cap.** The bundle only ships species legal in the
  *current* regulation, not full historical rosters — that's a deliberate
  cut, not a bug, to leave headroom under the cap (5 of 10 files used as of
  `singles-team-builder`'s addition).
- **No live file reads.** Everything the Gem knows about rules/roster is
  whatever was in the bundle at last upload. It's instructed to flag
  stale-looking data rather than assume it's current.
- **No GitHub access at all.** Confirmed no Gems equivalent to ChatGPT
  Custom GPT "Actions" (arbitrary external API calls) exists as of this
  writing — `skill-retro`'s filing step is degraded by platform
  limitation, not an oversight.
