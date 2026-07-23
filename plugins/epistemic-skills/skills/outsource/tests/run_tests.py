#!/usr/bin/env python3
"""Deterministic package-integration checks for the outsource skill."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve()
SKILL_ROOT = HERE.parents[1]
PACKAGE_ROOT = HERE.parents[3]
REPO_ROOT = HERE.parents[5]
EXPECTED_VERSION = "2.9.0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    skill = read(SKILL_ROOT / "SKILL.md")
    require(skill.startswith("---\nname: outsource\n"), "invalid skill frontmatter/name")
    for phrase in (
        "docs/outsource/<work-id>/HANDOFF.md",
        "## Context-erasure test",
        "## Output contract",
        "## Workflow",
        "## Relay loop",
        "## Stop conditions",
        "https://github.com/<owner>/<repo>/blob/<commit>/docs/outsource/<work-id>/HANDOFF.md",
    ):
        require(phrase in skill, f"SKILL.md missing contract phrase: {phrase}")

    template = read(SKILL_ROOT / "reference" / "HANDOFF_TEMPLATE.md")
    for heading in (
        "# Outsource handoff:",
        "## Repository and source",
        "## Required outcome",
        "## Context map",
        "## Requirements",
        "## Completion contract",
        "## Authority and boundaries",
        "## Relay response contract",
    ):
        require(heading in template, f"handoff template missing heading: {heading}")

    router = read(PACKAGE_ROOT / "skills" / "using-epistemic-skills" / "SKILL.md")
    require("These nine disciplines" in router, "router discipline count is stale")
    require("**outsource**" in router, "router does not route outsource")
    require("why these nine" in router, "router family-resemblance count is stale")

    helix = read(PACKAGE_ROOT / "skills" / "helix" / "SKILL.md")
    require("external delegation / model handoff" in helix, "helix lacks outsource pairing")

    readme = read(REPO_ROOT / "README.md")
    require(f"**Version {EXPECTED_VERSION}.**" in readme, "README version is stale")
    require("**eleven** skills" in readme, "README skill count is stale")
    require("**nine** disciplines" in readme, "README discipline count is stale")
    require("all eleven skills" in readme, "README harness success check is stale")
    require("**outsource**" in readme, "README skill table lacks outsource")

    skill_dirs = [p for p in (PACKAGE_ROOT / "skills").iterdir() if p.is_dir()]
    require(len(skill_dirs) == 11, f"expected 11 skill directories, found {len(skill_dirs)}")
    for directory in skill_dirs:
        require((directory / "SKILL.md").is_file(), f"missing SKILL.md: {directory.name}")

    manifests = (
        REPO_ROOT / "gemini-extension.json",
        REPO_ROOT / ".claude-plugin" / "marketplace.json",
        REPO_ROOT / ".cursor-plugin" / "plugin.json",
        REPO_ROOT / ".cursor-plugin" / "marketplace.json",
        REPO_ROOT / ".kimi-plugin" / "plugin.json",
        PACKAGE_ROOT / ".claude-plugin" / "plugin.json",
        PACKAGE_ROOT / ".codex-plugin" / "plugin.json",
        PACKAGE_ROOT / ".cursor-plugin" / "plugin.json",
        PACKAGE_ROOT / ".kimi-plugin" / "plugin.json",
    )
    for path in manifests:
        data = json.loads(read(path))
        version = data.get("version") or data.get("metadata", {}).get("version")
        require(version == EXPECTED_VERSION, f"stale version in {path}")
        text = json.dumps(data).lower()
        require("outsource" in text, f"manifest does not advertise outsource: {path}")

    require(
        "outsource" in json.loads(read(REPO_ROOT / "plugin.json"))["description"].lower(),
        "Antigravity manifest does not advertise outsource",
    )

    print("outsource integration: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
