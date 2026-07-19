#!/usr/bin/env python3
"""Fail a PR if any Claude skill has no recorded Gemini-porting decision.

Every skill under agents/claude/pokemon-champions-coach/skills/ needs an
explicit row in the Gemini folder's capability matrix (agents/gemini/
pokemon-champions-coach/README.md) -- "Full", "Draft-only", "Not ported"
(with why), or any other explicit call. The point is that a skill can never
silently exist on one agent with nobody having decided what happens to it
on the other; this doesn't second-guess *what* the decision was, only that
one was made and written down where a human will actually see it.
"""
import glob
import os
import re
import sys

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILLS_GLOB = os.path.join(REPO_ROOT, "agents", "claude", "pokemon-champions-coach", "skills", "*", "SKILL.md")
GEMINI_README = os.path.join(REPO_ROOT, "agents", "gemini", "pokemon-champions-coach", "README.md")

NAME_FIELD_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)


def skill_name(path: str) -> str:
    with open(path) as f:
        text = f.read()
    frontmatter = text.split("---", 2)[1] if text.startswith("---") else text
    match = NAME_FIELD_RE.search(frontmatter)
    if not match:
        raise SystemExit(f"::error::{path} has no 'name:' field in its frontmatter.")
    return match.group(1)


def main() -> int:
    skill_paths = sorted(glob.glob(SKILLS_GLOB))
    if not skill_paths:
        print(f"::error::No skills found matching {SKILLS_GLOB} -- check the glob, this shouldn't be empty.")
        return 1

    with open(GEMINI_README) as f:
        gemini_readme = f.read()

    missing = [name for name in (skill_name(p) for p in skill_paths) if f"`{name}`" not in gemini_readme]

    if missing:
        rel_readme = os.path.relpath(GEMINI_README, REPO_ROOT)
        print(f"::error::These Claude skills have no recorded decision in the Gemini capability matrix ({rel_readme}):")
        for name in missing:
            print(f"::error::- {name}")
        print(
            "::error::Add a row for each -- \"Full\", \"Draft-only\", \"Not ported\" (with why), or any "
            "other explicit call. The point is a recorded decision, not necessarily a port."
        )
        return 1

    print(f"All {len(skill_paths)} Claude skills have a recorded Gemini decision.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
