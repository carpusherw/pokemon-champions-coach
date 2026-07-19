# pokemon-champions-coach

Agent skills for playing [Pokemon Champions](https://www.pokemon.com/us/pokemon-video-games/pokemon-champions) competitively: keeping season rules and Pokemon data current, and coaching in-battle decisions like speed/move order.

Claude is supported first, via a Claude Code plugin, with a Gemini Gem as a
second, more limited target. The repo is laid out so other agent ecosystems
can be added later without restructuring what's already here.

## Layout

```
references/                     Agent-agnostic data, shared by every agent's skills
├── current-season.yaml         Pointer to the active regulation set
├── rules/
│   └── regulation-<id>.yaml    Rules for one regulation set (team building, format, bans, legal roster)
└── pokemon/
    └── <species-slug>.yaml     One file per legal Pokemon: types, stats, abilities, movepool, Mega data

agents/
├── claude/
│   └── pokemon-champions-coach/    Claude Code plugin (see below)
└── gemini/
    └── pokemon-champions-coach/    Gemini Gem (see below)
    # agents/<other-agent>/ placeholders go here as support is added

.claude-plugin/
└── marketplace.json           Claude Code marketplace manifest, points at agents/claude/pokemon-champions-coach
```

`references/` is intentionally outside any single agent's folder: rules and Pokemon data aren't Claude-specific, so any agent's skills can read the same YAML files instead of re-fetching or duplicating them.

## Claude plugin

Install this marketplace in Claude Code, then install the `pokemon-champions-coach` plugin:

```
/plugin marketplace add carpusherw/pokemon-champions-coach
/plugin install pokemon-champions-coach@pokemon-champions-coach
```

Skills included:

- **refresh-references** — Looks up the current regulation set's rules and legal Pokemon, and refreshes `references/`. Run this at the start of each new season (Pokemon Champions rotates regulation sets periodically), or whenever the references look stale.
- **move-order-coach** — Given a board state (both sides' Pokemon, moves, items, field conditions), works out the speed order and move-resolution order for the turn, using the current regulation's legal roster and reference data instead of re-deriving stats from scratch.
- **team-builder** — Builds a battle team of 6 from a starting Pokemon, a loose idea/tactic, or a named strategy (Trick Room, Tailwind, weather, balance), following the idea → core → mode process top VGC/Champions players use, then threat-checks the result against the current regulation's meta.
- **skill-retro** — Turns concrete failures in this plugin's own coaching skills into GitHub issues, after showing the user the draft and getting a go-ahead.

## Gemini Gem

Gemini Web/mobile has no plugin system — the only extensibility point is a
Gem (one instructions blob + up to 10 uploaded knowledge files, set up by
hand in Gem Manager, then usable on both Gemini Web and the mobile apps).
See `agents/gemini/pokemon-champions-coach/README.md` for setup steps.

Only `move-order-coach` and a degraded, draft-only `skill-retro` are
ported — Gems can't read this repo live or call the GitHub API, so
`refresh-references` stays Claude-only, and `skill-retro` on Gemini can
draft an issue but can't file one. See that folder's README for the full
capability matrix and how the two agents stay in sync.

## Adding another agent

To support a new agent, add `agents/<agent-name>/` with whatever manifest/plugin format that ecosystem expects, and have its skills read from the shared `references/` directory rather than duplicating rules or Pokemon data. Keep the skill *logic* (how to look up rules, how to reason about speed order) consistent across agents — only the packaging format should differ.
