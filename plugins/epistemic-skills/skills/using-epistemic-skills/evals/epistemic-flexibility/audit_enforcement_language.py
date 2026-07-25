#!/usr/bin/env python3
"""Audit enforcement language in every SKILL.md amended by PR #35.

The audit is intentionally exhaustive over a frozen path inventory: every use of
``enforce*`` or ``fail[- ]closed`` is emitted with a semantic category. A use
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
    # Shared-invariant language is a normative fallback contract unless the
    # same local context names a validator/schema/workflow. Mechanical markers
    # are evaluated first, so these phrases never upgrade a named mechanism to
    # policy or downgrade a mechanical claim.
    "missing evidence",
    "no durable home",
    "malformed chains",
    "family resemblance",
    "belongs in this collection",
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


def classification_self_test() -> list[str]:
    """Pin category precedence and the four previously ambiguous policy forms."""

    probes = {
        "mechanical": (
            "The schema validator rejects malformed entries and fails closed.",
            "mechanical",
        ),
        "policy-missing-evidence": (
            "Fail closed; degrade explicitly. Missing evidence means the claim is unverified.",
            "policy",
        ),
        "policy-durable-home": (
            "Fail closed. No durable home means session-only; malformed chains fail closed.",
            "policy",
        ),
        "policy-family-membership": (
            "A skill belongs in this collection only if it enforces all of these family resemblance invariants.",
            "policy",
        ),
        "external": (
            "An org-enforced branch protection external gate remains separate.",
            "external",
        ),
        "limitation": (
            "This is human-enforced policy and not enforcement by the harness.",
            "limitation",
        ),
        "ambiguous": (
            "The component enforces quality.",
            None,
        ),
    }
    errors: list[str] = []
    for name, (context, expected) in probes.items():
        actual = classify(context)
        if actual != expected:
            errors.append(
                f"classification probe {name}: expected {expected!r}, got {actual!r}"
            )
    return errors


def audit() -> tuple[list[dict[str, object]], list[str]]:
    records: list[dict[str, object]] = []
    errors: list[str] = classification_self_test()

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
