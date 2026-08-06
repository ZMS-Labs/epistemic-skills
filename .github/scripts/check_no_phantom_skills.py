#!/usr/bin/env python3
"""Fail when a routing surface names a skill that does not exist.

v4.0.0 consolidated eighteen skills into eleven. Every absorbed method survives
verbatim as a mode or instrument, and **every old name deliberately survives as
vocabulary in body prose** — "run a blindspot pass" is still a legitimate way to
ask for ``recon`` (brief mode). So a blanket ban on the old names would delete
working documentation.

The defect this catches is narrower and entirely decidable: a retired name
appearing in a surface that *routes*, where a reader or a router is told to go
somewhere that no longer exists. Two rules, no judgment calls:

1. **Firing surfaces.** No ``description:`` frontmatter field, and no manifest
   ``description``, may contain a retired skill name. Descriptions are the only
   text that governs whether a skill fires; a description that hands a boundary
   to a skill that was deleted routes into a hole.
2. **Path references.** No ``skills/<name>/`` path referenced anywhere in the
   repo's markdown or manifests may point at a directory that does not exist.
   This rule needs no registry and catches retirements nobody remembered to
   list here.

Rule 2 is self-maintaining. Rule 1 needs ``RETIRED`` kept current — one line per
retirement, which is the same cadence as a release. Stdlib only.

Exit 0 clean, 1 with a named defect per line.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILLS_DIR = REPO / "plugins" / "epistemic-skills" / "skills"

# Retired in v4.0.0 (the consolidation release), with the survivor that absorbed
# each one. Kept so a firing surface can never hand a boundary to a dead name.
RETIRED = {
    "blindspot-pass": "recon (brief mode)",
    "wayfinding": "recon (initiative mode)",
    "harvest-before-adopt": "recon (candidate mode)",
    "applying-formal-rigor": "resolve (derivation instrument)",
    "evidence-research": "resolve (literature instrument)",
    "throwaway-prototyping": "resolve (probe instrument)",
    "continuity-verify": "decision-ledger (resume mode)",
    "agent-interface-design": "reference/craft/ doctrine (no longer routed)",
    "intent-traced-merge": "reference/craft/ doctrine (no longer routed)",
}

# Anchored to the full package-relative path on purpose. A bare ``skills/(\w+)/``
# also matches every GitHub URL for this repo — ``.../epistemic-skills/tree/main``
# yields a phantom "tree" — because the repo name itself ends in "skills". That
# false-positive class was caught by running this check RED against the broken
# tree before trusting its green; do not loosen this anchor.
SKILL_PATH_RE = re.compile(r"plugins/epistemic-skills/skills/([a-z0-9][a-z0-9-]*)/")

# Historical evidence, not routing: dated eval results and archived docs record
# paths as they were at the time and must not be rewritten.
ARCHIVE_PARTS = {".git", ".worktrees", "docs", "results", "traces", "outputs", "runs"}


def live_skills() -> set[str]:
    return {p.parent.name for p in SKILLS_DIR.glob("*/SKILL.md")}


def frontmatter_description(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    block = text[3:end]
    match = re.search(r"^description:(.*?)(?=^\w+:|\Z)", block, re.S | re.M)
    return match.group(1) if match else ""


def check_firing_surfaces(defects: list[str]) -> None:
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        description = frontmatter_description(skill_md.read_text(encoding="utf-8"))
        for dead, survivor in RETIRED.items():
            if dead in description:
                defects.append(
                    f"{skill_md.relative_to(REPO)}: description names retired "
                    f"skill '{dead}' — route to {survivor}"
                )

    for manifest in sorted(REPO.glob("**/*plugin*.json")) + sorted(REPO.glob("*extension*.json")):
        if ".git" in manifest.parts or "node_modules" in manifest.parts:
            continue
        try:
            blob = json.dumps(json.loads(manifest.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
        for dead, survivor in RETIRED.items():
            if dead in blob:
                defects.append(
                    f"{manifest.relative_to(REPO)}: manifest advertises retired "
                    f"skill '{dead}' to installers — route to {survivor}"
                )


def check_path_references(defects: list[str]) -> None:
    live = live_skills()
    for source in sorted(REPO.glob("**/*.md")) + sorted(REPO.glob("**/*.json")):
        if ARCHIVE_PARTS.intersection(source.parts):
            continue  # dated archives record paths as they were; not routing
        try:
            text = source.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name in sorted(set(SKILL_PATH_RE.findall(text))):
            if name not in live and (SKILLS_DIR / name).exists() is False:
                defects.append(
                    f"{source.relative_to(REPO)}: references skills/{name}/ "
                    f"which does not exist"
                )


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 2

    defects: list[str] = []
    check_firing_surfaces(defects)
    check_path_references(defects)

    if defects:
        for defect in defects:
            print(f"phantom-skill reference: {defect}", file=sys.stderr)
        print(f"\n{len(defects)} routing surface(s) name a skill that does not exist", file=sys.stderr)
        return 1

    print(f"no phantom skill references: {len(live_skills())} live skills; "
          f"{len(RETIRED)} retired names allowed in prose, banned in routing surfaces")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
