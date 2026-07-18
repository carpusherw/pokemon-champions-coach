#!/usr/bin/env python3
"""Fail a PR that touches plugin content without bumping plugin/marketplace versions.

Runs in CI (see .github/workflows/plugin-version-guard.yml). Complements
`claude plugin validate --strict`, which checks that marketplace.json and
plugin.json are internally consistent but does not know whether either
version actually moved compared to the PR base branch.
"""
import json
import subprocess
import sys

MARKETPLACE_FILE = ".claude-plugin/marketplace.json"
PLUGIN_DIR = "agents/claude/pokemon-champions-coach"
PLUGIN_MANIFEST = f"{PLUGIN_DIR}/.claude-plugin/plugin.json"
CONTENT_DIRS = (PLUGIN_DIR + "/", "references/")


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def file_at_ref(ref: str, path: str) -> str | None:
    try:
        return run("git", "show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None


def parse_version(raw: str) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in raw.strip().split("."))
    except ValueError as exc:
        raise SystemExit(f"Version '{raw}' isn't a plain dotted-integer semver string.") from exc


def json_at_ref(ref: str, path: str) -> dict | None:
    text = file_at_ref(ref, path)
    return json.loads(text) if text is not None else None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_version_bump.py <base-ref>", file=sys.stderr)
        return 2
    base_ref = sys.argv[1]

    changed = run("git", "diff", "--name-only", f"{base_ref}...HEAD").splitlines()
    plugin_touched = any(f.startswith(CONTENT_DIRS) for f in changed)
    if not plugin_touched:
        print("No changes under agents/claude/pokemon-champions-coach/ or references/ — skipping version-bump check.")
        return 0

    base_plugin = json_at_ref(base_ref, PLUGIN_MANIFEST)
    head_plugin = json_at_ref("HEAD", PLUGIN_MANIFEST)
    base_marketplace = json_at_ref(base_ref, MARKETPLACE_FILE)
    head_marketplace = json_at_ref("HEAD", MARKETPLACE_FILE)

    if head_plugin is None:
        print(f"::error::{PLUGIN_MANIFEST} is missing at HEAD.")
        return 1
    if head_marketplace is None:
        print(f"::error::{MARKETPLACE_FILE} is missing at HEAD.")
        return 1

    errors = []

    base_plugin_version = base_plugin["version"] if base_plugin else "0.0.0"
    head_plugin_version = head_plugin["version"]
    if parse_version(head_plugin_version) <= parse_version(base_plugin_version):
        errors.append(
            f"This PR changes plugin content but {PLUGIN_MANIFEST}'s \"version\" "
            f"wasn't bumped ({base_plugin_version} -> {head_plugin_version}). "
            "Bump it (patch for data/doc refreshes, minor for new skills/features, "
            "major for breaking changes)."
        )

    head_entry = next(
        (p for p in head_marketplace["plugins"] if p["source"] == f"./{PLUGIN_DIR}"),
        None,
    )
    if head_entry is None:
        errors.append(f"{MARKETPLACE_FILE} has no plugin entry with source \"./{PLUGIN_DIR}\".")
    elif head_entry.get("version") != head_plugin_version:
        errors.append(
            f"{MARKETPLACE_FILE}'s plugins[].version ({head_entry.get('version')!r}) "
            f"doesn't match {PLUGIN_MANIFEST}'s version ({head_plugin_version!r}). "
            "Keep the marketplace entry's version in sync with plugin.json."
        )

    base_marketplace_version = base_marketplace["version"] if base_marketplace else "0.0.0"
    head_marketplace_version = head_marketplace.get("version")
    if head_marketplace_version is None:
        errors.append(f"{MARKETPLACE_FILE} is missing a top-level \"version\" field.")
    elif parse_version(head_marketplace_version) <= parse_version(base_marketplace_version):
        errors.append(
            f"This PR changes plugin content but {MARKETPLACE_FILE}'s top-level "
            f"\"version\" wasn't bumped ({base_marketplace_version} -> {head_marketplace_version})."
        )

    if errors:
        print("::error::Plugin content changed without the required version bump(s):")
        for e in errors:
            print(f"::error::- {e}")
        return 1

    print("Version bump check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
