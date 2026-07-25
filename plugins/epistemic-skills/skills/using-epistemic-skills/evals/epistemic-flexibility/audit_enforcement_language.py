#!/usr/bin/env python3
"""Audit enforcement language in every SKILL.md amended by PR #35.

The audit is intentionally exhaustive over a frozen path inventory: every use of
``enforce*`` or ``fail[- ]closed`` is emitted with a semantic category.  A use
that cannot be classified from its local context fails the gate rather than
silently inheriting the strongest interpretation.

Categories:
- mechanical: an executable schema, validator, script, workflow, selector, or test;
- policy: a normative discipline without a claimed runtime interlock;
- external: a separately operated/environmental enforcement mechanism;
- limitation: an explicit non-claim or category boundary.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
REFERENCE = (
    REPO_ROOT
    / "plugins"
    / "epistemic-skills"
    / "skills"
    / "using-epistemic-skills"
    / "reference"
    / "epistemic-flexibility.md"
)
SKILL_PATHS = [
    "plugins/epistemic-skills/skills/applying-formal-rigor/SKILL.md",
    "plugins/epistemic-skills/skills/blindspot-pass/SKILL.md",
    "plugins/epistemic-skills/skills/continuity-verify/SKILL.md",
    "plugins/epistemic-skills/skills/decision-ledger/SKILL.md",
    "plugins/epistemic-skills/skills/evidence-locked-uat/SKILL.md",
    "plugins/epistemic-skills/skills/evidence-research/SKILL.md",
    "plugins/epistemic-skills/skills/gauntlet/SKILL.md",
    "plugins/epistemic-skills/skills/helix/SKILL.md",
    "plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md",
    "plugins/epistemic-skills/skills/write-goal/SKILL.md",
]
TERM_RE = re.compile(
    r"\b(?:enforc(?:e|ed|es|ing|ement)|fail(?:s|ed|ing)?(?:-|\s)closed)\b",
    re.IGNORECASE,
)

LIMITATION_MARKERS = (
    "not enforcement",
    "not enforce",
    "does not enforce",
    "doesn't enforce",
    "cannot enforce",
    "can't enforce",
    "not mechanically",
    "unachievable",
    "structural only",
    "human review",
    "policy backstop",
    "advisory",
    "no runtime",
    "not a security control",
    "never claimed",
    "does not satisfy",
    "not guaranteed",
    "category limit",
)
EXTERNAL_MARKERS = (
    "org-enforced",
    "externally enforced",
    "external gate",
    "outside this skill",
    "branch protection",
    "runtime tool-call",
    "tool-call boundary",
    "if your environment",
    "environment enforces",
)
MECHANICAL_MARKERS = (
    "mechanically",
    "validator",
    "schema",
    "workflow",
    "script",
    "selector",
    "parser",
    "test",
    "reject",
    "check",
    "executable",
    "machine-readable",
    "required status",
    "ci ",
    "ci-",
    " ci",
)
POLICY_MARKERS = (
    "non-negotiable",
    "must ",
    " must",
    "required",
    "discipline",
    "policy",
    "operator",
    "rule",
    "guardrail",
)


def classify(context: str) -> str | None:
    lowered = " ".join(context.lower().split())
    if any(marker in lowered for marker in LIMITATION_MARKERS):
        return "limitation"
    if any(marker in lowered for marker in EXTERNAL_MARKERS):
        return "external"
    if any(marker in lowered for marker in MECHANICAL_MARKERS):
        return "mechanical"
    if any(marker in lowered for marker in POLICY_MARKERS):
        return "policy"
    return None


def audit() -> tuple[list[dict[str, object]], list[str]]:
    records: list[dict[str, object]] = []
    errors: list[str] = []

    if not REFERENCE.is_file() or "## Enforcement status" not in REFERENCE.read_text(
        encoding="utf-8"
    ):
        errors.append("enforcement-status reference boundary is missing")

    for relative in SKILL_PATHS:
        path = REPO_ROOT / relative
        if not path.is_file():
            errors.append(f"missing audited skill: {relative}")
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            terms = [match.group(0) for match in TERM_RE.finditer(line)]
            if not terms:
                continue
            start = max(0, index - 2)
            end = min(len(lines), index + 3)
            context = "\n".join(lines[start:end])
            category = classify(context)
            record = {
                "path": relative,
                "line": index + 1,
                "terms": terms,
                "category": category,
                "text": line.strip(),
            }
            records.append(record)
            if category is None:
                errors.append(
                    f"AMBIGUOUS-ENFORCEMENT-LANGUAGE:{relative}:{index + 1}: {line.strip()}"
                )

    if not records:
        errors.append("audit found zero enforcement-language occurrences")
    return records, errors


def main() -> int:
    records, errors = audit()
    for record in records:
        print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    counts: dict[str, int] = {}
    for record in records:
        category = str(record["category"])
        counts[category] = counts.get(category, 0) + 1
    print(
        "enforcement-language audit: "
        f"{len(records)} occurrences across {len(SKILL_PATHS)} skill files; "
        + ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    )
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
