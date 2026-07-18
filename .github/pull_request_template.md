## Summary

<!-- What does this PR change and why? -->

## Version bump

CI (`plugin-version-guard`) blocks merge if this is skipped, but check it yourself before pushing:

- [ ] This PR only touches docs/CI/README — no plugin code, skills, or `references/` data changed. **(skip the rest of this section)**
- [ ] Bumped `version` in `agents/claude/pokemon-champions-coach/.claude-plugin/plugin.json`
- [ ] Bumped the matching `plugins[].version` entry in `.claude-plugin/marketplace.json` to the same value
- [ ] Bumped the top-level `version` in `.claude-plugin/marketplace.json`
- [ ] Bump size matches [semver](https://semver.org/): patch for data/reference refreshes, minor for new skills or features, major for breaking changes to skill behavior or plugin structure

## Testing

<!-- How did you verify this change? -->
