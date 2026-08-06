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

# Retired skills, with the survivor that absorbed each one. Kept so a firing
# surface can never hand a boundary to a dead name.
#
# THIS MAP IS THE GUARD'S OWN HAND-MAINTAINED INVENTORY, AND IT DRIFTED. It listed
# only the v4.0.0 retirements. v5.0.0 deleted ``using-epistemic-skills`` and
# ``helix`` and nobody added them here, so the check that exists precisely to catch
# "manifest advertises retired skill to installers" was never told about the
# release's own deletions — and v5.0.0 shipped with eight manifests advertising
# both, plus a GEMINI.md instructing users to start with a skill that is not in
# the package.
#
# Adding a skill costs nothing here. DELETING one obliges an entry in this map, in
# the same commit. That obligation is now enforced: see check_retired_map_covers_
# deletions below, which fails when a name the RETIRED map has never heard of
# appears in an installer-facing surface.
RETIRED = {
    # v4.0.0 — the consolidation release
    "blindspot-pass": "recon (brief mode)",
    "wayfinding": "recon (initiative mode)",
    "harvest-before-adopt": "recon (candidate mode)",
    "applying-formal-rigor": "resolve (derivation instrument)",
    "evidence-research": "resolve (literature instrument)",
    "throwaway-prototyping": "resolve (probe instrument)",
    "continuity-verify": "decision-ledger (resume mode)",
    "agent-interface-design": "reference/craft/ doctrine (no longer routed)",
    "intent-traced-merge": "reference/craft/ doctrine (no longer routed)",
    # v5.0.0 — the loop release. Both seats deleted; metacognate replaces them.
    "using-epistemic-skills": "metacognate (the sole entry point)",
    "helix": "metacognate (Tier 2 pairing judgment, not a pair table)",
}

# Installer-facing surfaces: what a user reads or a package manager consumes when
# deciding what this package contains. A retired name here is worse than a stale
# doc — it sends someone to look for something that is not installed.
#
# ``**/*plugin*.json`` matches on FILENAME, so it never matched ``marketplace.json``
# despite it sitting inside ``.claude-plugin/``. Both marketplace files went
# unscanned through every release. The glob's scope was its blind spot.
INSTALLER_JSON_GLOBS = (
    "**/*plugin*.json",
    "**/marketplace.json",
    "*extension*.json",
)

# Root instruction files are read by an agent at session start. A retired skill
# named here is an instruction to use something that does not exist. Prose, not
# paths — SKILL_PATH_RE deliberately only matches ``skills/<name>/`` references,
# which is why GEMINI.md's "Start with the `using-epistemic-skills` skill" was
# invisible to this check while the file was being scanned.
ROOT_INSTRUCTION_FILES = ("GEMINI.md", "AGENTS.md", "CLAUDE.md", "README.md")

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

    seen: set[Path] = set()
    for pattern in INSTALLER_JSON_GLOBS:
        for manifest in sorted(REPO.glob(pattern)):
            if ARCHIVE_PARTS.intersection(manifest.parts) or "node_modules" in manifest.parts:
                continue
            if manifest in seen:
                continue
            seen.add(manifest)
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

    # Root instruction files, checked as PROSE. An agent reading "Start with the
    # `using-epistemic-skills` skill" at session start will go looking for a skill
    # that is not installed. Historical framing is allowed and required — these
    # files legitimately describe what was removed and why.
    # Historical framing is ALLOWED and necessary — these files legitimately record
    # what was removed, when, and why. The vocabulary below was widened after the
    # first version flagged two correct README sentences: a "Craft doctrine (not
    # disciplines) ... v4.0.0 demotion" note, and a version-history line describing
    # what 3.4.0 added. Both name retired skills accurately. A guard that punishes
    # accurate history teaches people to delete history.
    historical = re.compile(
        r"retired|replaced|former|absorbed|deleted|no longer|superseded|historical|"
        r"used to|previously|removed in|renamed|demot|doctrine|preserved|archived|"
        r"consolidat|deprecat|\bv?\d+\.\d+\.\d+\b|version \d|\badds?\b|\badded\b",
        re.I,
    )
    for name in ROOT_INSTRUCTION_FILES:
        source = REPO / name
        if not source.is_file():
            continue
        try:
            lines = source.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            if historical.search(line):
                continue
            for dead, survivor in RETIRED.items():
                if re.search(rf"(?<![a-z0-9-]){re.escape(dead)}(?![a-z0-9-])", line, re.I):
                    defects.append(
                        f"{name}:{number}: instructs an agent to use retired skill "
                        f"'{dead}' — route to {survivor}"
                    )
                    break


def check_path_references(defects: list[str]) -> None:
    live = live_skills()
    for source in sorted(REPO.glob("**/*.md")) + sorted(REPO.glob("**/*.json")):
        if ARCHIVE_PARTS.intersection(source.parts):
            continue  # dated archives record paths as they were; not routing
        try:
            text = source.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        # Tag-pinned and commit-pinned URLs are historical by construction: the
        # path existed at that ref. Rewriting them would falsify a citation.
        text = re.sub(r"blob/v?\d[^)\s]*", "", text)
        for name in sorted(set(SKILL_PATH_RE.findall(text))):
            # NO `.exists()` fallback. It made this check environment-dependent:
            # `git rm` leaves empty directories behind on Windows, so `.exists()`
            # returned True for a DELETED skill and silently suppressed the
            # finding. The same check passed on a dirty Windows tree and failed on
            # a clean Linux clone, against identical content. The filesystem glob
            # (`live`) is the only authority on what exists.
            if name not in live:
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
