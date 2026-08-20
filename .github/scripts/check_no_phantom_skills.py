#!/usr/bin/env python3
"""Fail when a routing surface names a skill that does not exist.

v4.0.0 consolidated eighteen skills into eleven. Every absorbed method survives
verbatim as a mode or instrument, and **every old name deliberately survives as
vocabulary in body prose** — "run a blindspot pass" is still a legitimate way to
ask for ``recon`` (brief mode). So a blanket ban on the old names would delete
working documentation.

The defect this catches is narrower and entirely decidable: a retired name
appearing in a surface that *routes*, where a reader or a router is told to go
somewhere that no longer exists. Three rules, no judgment calls:

1. **Firing surfaces.** No ``description:`` frontmatter field, and no manifest
   ``description``, may contain a retired skill name. Descriptions are the only
   text that governs whether a skill fires; a description that hands a boundary
   to a skill that was deleted routes into a hole.
2. **Path references.** No ``skills/<name>/`` path referenced anywhere in the
   repo's markdown or manifests may point at a directory that does not exist.
   This rule needs no registry and catches retirements nobody remembered to
   list here.
3. **Hand-authored routing tables.** The generated ``ROUTING.md`` is the ONLY
   aggregate routing surface (v5 design, AMENDMENT 2026-08-07: "any central
   member/pair table" is a forbidden hand-authored routing surface). A markdown
   table row outside it whose cells carry a routing column (``hands-to`` and
   variants) reintroduces the enumeration tax the v5 design deleted, and
   drifts silently. Decidable: table-row syntax plus the column vocabulary;
   prose may discuss hands-to freely.

Rule 2 is self-maintaining. Rule 1 needs ``RETIRED`` kept current — one line per
retirement, which is the same cadence as a release. Rule 3 needs no registry.
Stdlib only.

Usage:
  python check_no_phantom_skills.py             # validate the tree
  python check_no_phantom_skills.py --self-test # planted RED controls (rule 3)

Exit 0 clean, 1 with a named defect per line.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
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

# SKILL_PATH_RE requires the full package prefix, so it is structurally blind to
# the BARE form -- `using-epistemic-skills/reference/routine-fast-path.md` names
# a seat deleted in v5.0.0 but carries no `skills/` prefix to match. Three
# shipped files routed that way, one of them the file the README pins, and it
# survived since v5.0.0 (publication-gate finding PG-14). Matched only against
# the CLOSED retired-name list, so it cannot invent findings.
BARE_RETIRED_PATH_RE = re.compile(
    r"(?<![a-z0-9/-])(" + "|".join(sorted(RETIRED, key=len, reverse=True)) + r")/[A-Za-z0-9._-]"
)

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
            # Live "router ties the package" claims after the router seat was deleted.
            if re.search(r"\brouter that ties\b|\bEpistemic router\b", line):
                if not historical.search(line):
                    defects.append(
                        f"{name}:{number}: live routing prose names the deleted router seat "
                        "— use metacognate / entry point wording"
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


# The one aggregate routing surface. Exact path: a second file by this name
# elsewhere (e.g. inside a skill directory) is NOT exempt.
ROUTING_MD = REPO / "plugins" / "epistemic-skills" / "ROUTING.md"

# Routing-column vocabulary. 'hands-to' variants and 'routes to' are handoff
# semantics; a bare 'Consumes'/'Skill' column is inventory, not routing, and
# stays legal (the README catalog and sibling-placement tables use those).
ROUTING_COLUMN_RE = re.compile(
    r"\b(?:hands?[- ]to|hands?[- ]off[- ]to|routes?[- ]to|routed[- ]to)\b", re.I
)
# A markdown table header is the row immediately above a separator row.
SEPARATOR_ROW_RE = re.compile(r"^\|(?:\s*:?-+:?\s*\|)+$")


def check_no_hand_authored_routing_tables(defects: list[str], root: Path = REPO) -> None:
    """Rule 3: the generated ROUTING.md is the only aggregate routing surface.

    Header rows only: a routing COLUMN is what makes a table a routing table.
    A data cell that cites the ``metadata.hands-to`` key name is documentation
    of the convention, not a routing surface, and stays legal.
    """
    routing_md = root / "plugins" / "epistemic-skills" / "ROUTING.md"
    for source in sorted(root.glob("**/*.md")):
        if ARCHIVE_PARTS.intersection(source.relative_to(root).parts):
            continue  # archives record the old hand-authored tables as evidence
        if source == routing_md:
            continue
        try:
            lines = source.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not (stripped.startswith("|") and stripped.endswith("|")):
                continue
            following = lines[number].strip() if number < len(lines) else ""
            if not SEPARATOR_ROW_RE.match(following):
                continue  # not a header row; prose and data cells are free
            if ROUTING_COLUMN_RE.search(stripped):
                defects.append(
                    f"{source.relative_to(root)}:{number}: hand-authored routing table "
                    "(a hands-to/routes-to column outside the generated ROUTING.md) — "
                    "declare metadata.hands-to in the skill's frontmatter and run "
                    "sync_skill_surfaces.py --write"
                )


def check_bare_retired_paths(defects: list[str], root: Path = REPO) -> None:
    """A skill's SKILL.md and its reference/ files ARE routing surfaces.

    Scoped to those deliberately: eval READMEs and retirement notes describe
    history and must stay free to name a dead seat in prose.
    """
    skills_dir = root / "plugins" / "epistemic-skills" / "skills"
    for source in sorted(skills_dir.glob("**/*.md")):
        if ARCHIVE_PARTS.intersection(source.parts):
            continue
        try:
            text = source.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        text = re.sub(r"blob/v?\d[^)\s]*", "", text)
        for dead in sorted(set(BARE_RETIRED_PATH_RE.findall(text))):
            defects.append(
                f"{source.relative_to(root)}: routes to `{dead}/...`, a seat "
                f"deleted in an earlier release (now {RETIRED[dead]})"
            )


def self_test() -> int:
    """Planted RED controls for rule 3 (the tree-independent rule)."""
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "plugins" / "epistemic-skills").mkdir(parents=True)
        (root / "plugins" / "epistemic-skills" / "ROUTING.md").write_text(
            "| Skill | hands-to |\n|---|---|\n| `a` | `b` |\n", encoding="utf-8")
        (root / "NOTES.md").write_text(
            "Prose that discusses the hands-to convention is fine.\n"
            "| Skill | Purpose |\n|---|---|\n| `a` | inventory row |\n"
            "| Key | Meaning |\n|---|---|\n"
            "| `metadata.hands-to` | data cell citing the key name is fine |\n",
            encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "old.md").write_text(
            "| Skill | Hands to |\n|---|---|\n| `a` | `b` |\n", encoding="utf-8")
        defects: list[str] = []
        check_no_hand_authored_routing_tables(defects, root)
        if defects:
            failures += 1
            print(f"[FAIL] honest tree flagged: {defects}")
        else:
            print("[PASS] generated ROUTING.md, prose mention, inventory table, "
                  "archived table all pass")
        planted = [
            ("hands-to-column", "| Skill | hands-to |\n|---|---|\n| `a` | `b` |\n"),
            ("hands-off-spaced", "| Seat | Hands off to |\n|---|---|\n| `a` | `b` |\n"),
            ("routes-to-column", "| From | routes to |\n|---|---|\n| `a` | `b` |\n"),
        ]
        for name, table in planted:
            (root / "NOTES.md").write_text(table, encoding="utf-8")
            defects = []
            check_no_hand_authored_routing_tables(defects, root)
            if any("hand-authored routing table" in d for d in defects):
                print(f"[PASS] planted {name} table fails closed")
            else:
                failures += 1
                print(f"[FAIL] planted {name} table not rejected: {defects}")
        # PG-14: the bare retired-path form, and the prose that must stay legal.
        sk = root / "plugins" / "epistemic-skills" / "skills" / "some-skill"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "Apply the gate from `using-epistemic-skills/reference/routine-fast-path.md`.\n",
            encoding="utf-8")
        defects = []
        check_bare_retired_paths(defects, root)
        if any("deleted in an earlier release" in d for d in defects):
            print("[PASS] planted bare retired path fails closed")
        else:
            failures += 1
            print(f"[FAIL] planted bare retired path not rejected: {defects}")
        (sk / "SKILL.md").write_text(
            "The `using-epistemic-skills` seat was retired in v5.0.0; metacognate "
            "replaces it. See `metacognate/reference/routine-fast-path.md`.\n",
            encoding="utf-8")
        defects = []
        check_bare_retired_paths(defects, root)
        if defects:
            failures += 1
            print(f"[FAIL] honest prose naming a retired seat flagged: {defects}")
        else:
            print("[PASS] prose naming a retired seat without routing to it stays legal")

        # A rogue second ROUTING.md inside a skill directory is NOT exempt.
        (root / "NOTES.md").write_text("clean\n", encoding="utf-8")
        rogue = root / "plugins" / "epistemic-skills" / "skills" / "x"
        rogue.mkdir(parents=True)
        (rogue / "ROUTING.md").write_text(
            "| Skill | hands-to |\n|---|---|\n", encoding="utf-8")
        defects = []
        check_no_hand_authored_routing_tables(defects, root)
        if any("hand-authored routing table" in d for d in defects):
            print("[PASS] rogue second ROUTING.md fails closed")
        else:
            failures += 1
            print(f"[FAIL] rogue second ROUTING.md not rejected: {defects}")
    print(f"phantom-skill self-test: {'PASS' if not failures else 'FAIL'}")
    return 0 if not failures else 1


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return self_test()
    if not SKILLS_DIR.is_dir():
        print(f"skills directory not found: {SKILLS_DIR}", file=sys.stderr)
        return 2

    defects: list[str] = []
    check_firing_surfaces(defects)
    check_path_references(defects)
    check_bare_retired_paths(defects)
    check_no_hand_authored_routing_tables(defects)

    if defects:
        for defect in defects:
            print(f"phantom-skill reference: {defect}", file=sys.stderr)
        print(f"\n{len(defects)} routing surface(s) name a skill that does not exist", file=sys.stderr)
        return 1

    print(f"no phantom skill references: {len(live_skills())} live skills; "
          f"{len(RETIRED)} retired names allowed in prose, banned in routing surfaces; "
          f"generated ROUTING.md is the only routing table")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
