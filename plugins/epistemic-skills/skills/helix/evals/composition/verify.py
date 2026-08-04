#!/usr/bin/env python3
"""Validate Helix's machine-checkable cross-collection composition contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

SCHEMA = "helix-composition-contract@1"
ROUTER = "using-epistemic-skills"
HELIX = "helix"
REQUIRED_MEMBER_FIELDS = {"composition_class", "moments", "position"}
REQUIRED_ORDER_RULES = {
    "resumption-before-recon": {
        "when": "same-resumption-lineage",
        "before": "continuity-verify",
        "after": "recon",
    },
    "task-start-recon-before-design-derivation": {
        "when": "same-design-lineage-after-micro-recon-mismatch",
        "before": "recon",
        "after": "resolve",
    },
    "conflict-resolution-before-pre-merge-gate": {
        "when": "same-branch-pre-merge-lineage",
        "before": "intent-traced-merge",
        "after": "gauntlet",
    },
    "gate-before-ui-proof": {
        "when": "same-change-needs-gate-and-material-ui-proof",
        "before": "gauntlet",
        "after": "evidence-locked-uat",
    },
}
REQUIRED_INTERLOCK = (
    frozenset({"resolve"}),
    "instrument-sequencing-internal",
)
REQUIRED_TEXT_MARKERS = {
    "registry pointer": "reference/composition-contract.json",
    "ordered-set handshake": "zero, one, or ordered set",
    "member trigger authority": "the member skill owns its trigger",
    "resumption order": "continuity-verify → recon",
    "decision persistence breadth": "consequential decision, load-bearing assumption, or recurrent/operator correction",
    "open-questions modes": "explicit full-exhaustion mode and automatic fork-scoped mode",
    "gate/prove order": "gauntlet → evidence-locked-uat",
    "context-bound ordering": "context-bound order rules",
}


def discover_members(skills_root: Path) -> set[str]:
    """Discover every packaged skill that Helix must classify."""
    return {
        skill_file.parent.name
        for skill_file in skills_root.glob("*/SKILL.md")
        if skill_file.parent.name not in {ROUTER, HELIX}
    }


def _nonempty_strings(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item.strip() for item in value)
    )


def validate(contract: object, discovered_members: set[str], skill_text: str) -> dict:
    failures: list[str] = []
    if not isinstance(contract, dict):
        return {"pass": False, "failures": ["contract root must be an object"], "member_count": 0}

    if contract.get("schema") != SCHEMA:
        failures.append(f"schema must be {SCHEMA}")
    if contract.get("trigger_authority") != "member":
        failures.append("member skills, not Helix, must remain trigger-authoritative")
    if contract.get("selection_owner") != ROUTER:
        failures.append("the epistemic router must select the complete zero/one/ordered set")
    if contract.get("position_owner") != HELIX:
        failures.append("Helix must own cross-collection position and order custody")

    routine = contract.get("routine_policy")
    if not isinstance(routine, dict):
        failures.append("routine_policy must be an object")
    else:
        if routine.get("fresh_routine_path") != "silent":
            failures.append("fresh routine work must remain record-free and silent")
        if routine.get("resumption_precedes_routine_classification") is not True:
            failures.append("resumption verification must precede routine-path classification")

    members = contract.get("members")
    if not isinstance(members, dict):
        failures.append("members must be an object")
        members = {}
    contract_members = set(members)
    missing = sorted(discovered_members - contract_members)
    extra = sorted(contract_members - discovered_members)
    if missing or extra:
        failures.append(f"member classification mismatch: missing={missing} extra={extra}")

    for name, row in members.items():
        if not isinstance(row, dict):
            failures.append(f"{name}: composition entry must be an object")
            continue
        absent_fields = sorted(REQUIRED_MEMBER_FIELDS - set(row))
        if absent_fields:
            failures.append(f"{name}: missing fields {absent_fields}")
        if not (isinstance(row.get("composition_class"), str) and row["composition_class"].strip()):
            failures.append(f"{name}: composition_class must be a non-empty string")
        if not _nonempty_strings(row.get("moments")):
            failures.append(f"{name}: moments must be a non-empty list of strings")
        if not (isinstance(row.get("position"), str) and row["position"].strip()):
            failures.append(f"{name}: position must be a non-empty string")

    continuity = members.get("continuity-verify", {})
    if continuity.get("composition_class") != "pre-arc" or continuity.get("position") != "before":
        failures.append("continuity-verify must be classified pre-arc and before")
    if set(continuity.get("precedes_boundaries", [])) != {"routine-classification", "workflow-stage"}:
        failures.append("continuity-verify must precede routine classification and every resumed workflow stage")
    if "resumption" not in continuity.get("moments", []):
        failures.append("continuity-verify must classify the resumption moment")

    ledger = members.get("decision-ledger", {})
    if ledger.get("composition_class") != "retrospective-cross-cutting" or ledger.get("position") != "after":
        failures.append("decision-ledger must be retrospective-cross-cutting and after the moment")
    required_ledger_moments = {
        "consequential-decision",
        "load-bearing-assumption",
        "recurrent-or-operator-correction",
    }
    if not required_ledger_moments <= set(ledger.get("moments", [])):
        failures.append("decision-ledger must cover decisions, assumptions, and recurrent/operator corrections")
    if set(ledger.get("persistence_modes", [])) != {
        "reuse-existing-durable-artifact",
        "append-gap-only",
    }:
        failures.append("decision-ledger must reuse adequate artifacts and append only uncovered gaps")

    questions = members.get("open-questions", {})
    if set(questions.get("modes", [])) != {
        "explicit-full-exhaustion",
        "automatic-fork-scoped",
    }:
        failures.append("open-questions must preserve explicit full-exhaustion and automatic fork-scoped modes")

    raw_rules = contract.get("required_order_rules")
    rules: dict[str, dict[str, str]] = {}
    if not isinstance(raw_rules, list):
        failures.append("required_order_rules must be a list")
    else:
        for index, rule in enumerate(raw_rules):
            if not isinstance(rule, dict):
                failures.append(f"required_order_rules[{index}] must be an object")
                continue
            rule_id = rule.get("id")
            when = rule.get("when")
            before = rule.get("before")
            after = rule.get("after")
            fields = {"id": rule_id, "when": when, "before": before, "after": after}
            if not all(isinstance(value, str) and value.strip() for value in fields.values()):
                failures.append(f"required_order_rules[{index}] needs non-empty id/when/before/after strings")
                continue
            if rule_id in rules:
                failures.append(f"duplicate order rule id: {rule_id}")
                continue
            if before == after:
                failures.append(f"order rule {rule_id} cannot order a member before itself")
            if before not in discovered_members or after not in discovered_members:
                failures.append(
                    f"order rule {rule_id} names an unclassified member: before={before} after={after}"
                )
            rules[rule_id] = {"when": when, "before": before, "after": after}

    for rule_id, expected in REQUIRED_ORDER_RULES.items():
        actual = rules.get(rule_id)
        if actual is None:
            failures.append(f"required order rule missing: {rule_id}")
        elif actual != expected:
            failures.append(f"order rule {rule_id} drifted: expected={expected} got={actual}")

    interlocks = contract.get("interlocks")
    found_interlock = False
    if isinstance(interlocks, list):
        for row in interlocks:
            if not isinstance(row, dict):
                continue
            members_pair = row.get("members")
            if (
                isinstance(members_pair, list)
                and len(members_pair) in (1, 2)
                and all(isinstance(item, str) for item in members_pair)
            ):
                candidate = (frozenset(members_pair), row.get("rule") or row.get("id"))
                if candidate == REQUIRED_INTERLOCK:
                    found_interlock = True
                    break
    if not found_interlock:
        failures.append("resolve instrument-sequencing interlock is missing")

    lowered = " ".join(skill_text.lower().split())
    for label, marker in REQUIRED_TEXT_MARKERS.items():
        normalized_marker = " ".join(marker.lower().split())
        if normalized_marker not in lowered:
            failures.append(f"SKILL.md missing {label}: {marker}")

    return {
        "pass": not failures,
        "failures": failures,
        "member_count": len(contract_members),
        "order_rules": len(rules),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_root = Path(__file__).resolve().parents[2]
    parser.add_argument(
        "--contract",
        type=Path,
        default=default_root / "reference" / "composition-contract.json",
    )
    parser.add_argument("--skill", type=Path, default=default_root / "SKILL.md")
    parser.add_argument("--skills-root", type=Path, default=default_root.parent)
    args = parser.parse_args()

    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    skill_text = args.skill.read_text(encoding="utf-8")
    report = validate(contract, discover_members(args.skills_root), skill_text)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
