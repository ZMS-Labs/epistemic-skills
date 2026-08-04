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
    "plugins/epistemic-skills/skills/recon/SKILL.md",
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

# All markers are word-boundary regexes over the whitespace-normalized lowered
# context. Unbounded substrings proved too coarse: bare "check"/"test"/"ci"
# upgraded normative prose to mechanical, and "rule" matched inside
# "overruled". A mechanical classification now requires a CONCRETE executable
# mechanism (a named tool file, validator, schema, workflow, selector, parser,
# machine-readable artifact, or exit/status semantics) — generic
# verification vocabulary is not a mechanism.
def _markers(*patterns: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(p) for p in patterns)


LIMITATION_MARKERS = _markers(
    r"\bnot enforcement\b",
    r"\b(?:does not|doesn't|cannot|can't|never|not) enforce",
    r"\bnot mechanically\b",
    r"\bunachievable\b",
    r"\bstructural only\b",
    r"\bstructural[- ]only\b",
    r"\bhuman[- ](?:review|enforced)\b",
    r"\bpolicy backstop\b",
    r"\badvisory\b",
    r"\bno runtime\b",
    r"\bnot a security control\b",
    r"\bnever claimed\b",
    r"\bdoes not satisfy\b",
    r"\bnot guaranteed\b",
    r"\bcategory limit\b",
)
EXTERNAL_MARKERS = _markers(
    r"\borg-enforced\b",
    r"\bexternally enforced\b",
    r"\bexternal (?:gate|review)\b",
    r"\boutside this skill\b",
    r"\bbranch protection\b",
    r"\bruntime tool-call\b",
    r"\btool-call boundary\b",
    r"\bif your environment\b",
    r"\benvironment enforces\b",
)
MECHANICAL_MARKERS = _markers(
    r"\bmechanically\b",
    r"\bvalidators?\b",
    r"\bschemas?\b",
    r"\bworkflows?\b",
    r"\bscripts?\b",
    r"\bselector\b",
    r"\bparser\b",
    r"\bexecutable\b",
    r"\bmachine-readable\b",
    r"\brequired status\b",
    r"\b[a-z0-9_]+\.py\b",
    r"\bexit codes?\b",
    r"\bhard errors?\b",
    r"\bci\b",
)
POLICY_MARKERS = _markers(
    r"\bnon-negotiable\b",
    r"\bmust\b",
    r"\brequired?\b",
    r"\bdisciplines?\b",
    r"\bpolicy\b",
    r"\boperator\b",
    r"\brules?\b",
    r"\bguardrails?\b",
    # Shared-invariant language is a normative fallback contract unless the
    # same local context names a validator/schema/workflow. Mechanical markers
    # are evaluated first, so these phrases never upgrade a named mechanism to
    # policy or downgrade a mechanical claim.
    r"\bmissing evidence\b",
    r"\bno durable home\b",
    r"\bmalformed chains\b",
    r"\bfamily resemblance\b",
    r"\bbelongs in this collection\b",
    r"\bfloors?, not ceilings?\b",
    r"\bnever a silent pass\b",
)


def classify(context: str) -> str | None:
    lowered = " ".join(context.lower().split())
    if any(marker.search(lowered) for marker in LIMITATION_MARKERS):
        return "limitation"
    if any(marker.search(lowered) for marker in EXTERNAL_MARKERS):
        return "external"
    if any(marker.search(lowered) for marker in MECHANICAL_MARKERS):
        return "mechanical"
    if any(marker.search(lowered) for marker in POLICY_MARKERS):
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
        # decoys: generic verification vocabulary is not a mechanism — these
        # pin that bare "check"/"test" no longer upgrade prose to mechanical
        # and that "overruled" no longer smuggles in the "rule" policy marker
        "decoy-generic-check": (
            "Each change enforces a bounded check before completion.",
            None,
        ),
        "decoy-overruled": (
            "Every overruled criticism is enforced to preserve its kernel.",
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

    # Out-of-inventory tripwire: the frozen inventory is a deliberate v1 scope,
    # but silent decay is not — enforcement language appearing in any
    # non-inventoried SKILL.md fails the gate until SKILL_PATHS is extended
    # deliberately (curated lists create unscanned paths otherwise).
    skills_root = REPO_ROOT / "plugins" / "epistemic-skills" / "skills"
    inventoried = {(REPO_ROOT / relative).resolve() for relative in SKILL_PATHS}
    for path in sorted(skills_root.glob("*/SKILL.md")):
        if path.resolve() in inventoried:
            continue
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
            if TERM_RE.search(line):
                relative = path.resolve().relative_to(REPO_ROOT).as_posix()
                errors.append(
                    f"OUT-OF-INVENTORY-ENFORCEMENT-LANGUAGE:{relative}:{index + 1}: "
                    f"{line.strip()} — add the file to SKILL_PATHS deliberately"
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
