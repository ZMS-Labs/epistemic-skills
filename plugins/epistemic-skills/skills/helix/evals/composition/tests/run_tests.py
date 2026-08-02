#!/usr/bin/env python3
"""Mutation-sensitive tests for the Helix composition contract."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELIX_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = Path(__file__).resolve().parents[4]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def expect_failure(
    verifier,
    name: str,
    contract: dict,
    discovered: set[str],
    skill_text: str,
    needle: str,
) -> None:
    report = verifier.validate(contract, discovered, skill_text)
    require(not report["pass"], f"{name} mutation unexpectedly passed")
    require(any(needle in failure for failure in report["failures"]), report["failures"])


def main() -> int:
    verify_path = ROOT / "verify.py"
    require(verify_path.is_file(), f"missing Helix composition verifier: {verify_path}")
    spec = importlib.util.spec_from_file_location("helix_composition", verify_path)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)

    contract = json.loads(
        (HELIX_ROOT / "reference" / "composition-contract.json").read_text(encoding="utf-8")
    )
    skill_text = (HELIX_ROOT / "SKILL.md").read_text(encoding="utf-8")
    discovered = verifier.discover_members(SKILLS_ROOT)

    clean = verifier.validate(contract, discovered, skill_text)
    require(clean["pass"], clean["failures"])
    require(clean["member_count"] == len(discovered), clean)
    require(clean["order_rules"] >= len(verifier.REQUIRED_ORDER_RULES), clean)

    missing_continuity = copy.deepcopy(contract)
    del missing_continuity["members"]["continuity-verify"]
    expect_failure(
        verifier,
        "missing-continuity",
        missing_continuity,
        discovered,
        skill_text,
        "member classification mismatch",
    )

    helix_owns_triggers = copy.deepcopy(contract)
    helix_owns_triggers["trigger_authority"] = "helix"
    expect_failure(
        verifier,
        "trigger-authority-drift",
        helix_owns_triggers,
        discovered,
        skill_text,
        "trigger-authoritative",
    )

    routine_before_resume = copy.deepcopy(contract)
    routine_before_resume["routine_policy"]["resumption_precedes_routine_classification"] = False
    expect_failure(
        verifier,
        "resumption-order-drift",
        routine_before_resume,
        discovered,
        skill_text,
        "precede routine-path classification",
    )

    narrowed_ledger = copy.deepcopy(contract)
    narrowed_ledger["members"]["decision-ledger"]["moments"].remove("load-bearing-assumption")
    expect_failure(
        verifier,
        "decision-ledger-narrowing",
        narrowed_ledger,
        discovered,
        skill_text,
        "decisions, assumptions",
    )

    explicit_only_questions = copy.deepcopy(contract)
    explicit_only_questions["members"]["open-questions"]["modes"] = ["explicit-full-exhaustion"]
    expect_failure(
        verifier,
        "open-questions-explicit-only",
        explicit_only_questions,
        discovered,
        skill_text,
        "automatic fork-scoped",
    )

    reversed_gate_prove = copy.deepcopy(contract)
    for rule in reversed_gate_prove["required_order_rules"]:
        if rule.get("id") == "gate-before-ui-proof":
            rule["before"], rule["after"] = rule["after"], rule["before"]
            break
    else:
        raise AssertionError("gate-before-ui-proof rule missing from clean contract")
    expect_failure(
        verifier,
        "gate-prove-reversal",
        reversed_gate_prove,
        discovered,
        skill_text,
        "order rule gate-before-ui-proof drifted",
    )

    globalized_order = copy.deepcopy(contract)
    for rule in globalized_order["required_order_rules"]:
        if rule.get("id") == "task-start-recon-before-design-derivation":
            rule["when"] = "always"
            break
    else:
        raise AssertionError("task-start-recon-before-design-derivation rule missing from clean contract")
    expect_failure(
        verifier,
        "context-erased-from-order",
        globalized_order,
        discovered,
        skill_text,
        "order rule task-start-recon-before-design-derivation drifted",
    )

    expect_failure(
        verifier,
        "future-member-unclassified",
        contract,
        discovered | {"future-discipline"},
        skill_text,
        "member classification mismatch",
    )

    expect_failure(
        verifier,
        "human-map-lost-registry-pointer",
        contract,
        discovered,
        skill_text.replace("reference/composition-contract.json", "reference/removed.json"),
        "registry pointer",
    )

    expect_failure(
        verifier,
        "ordered-set-collapsed-to-single-pair",
        contract,
        discovered,
        skill_text.replace("zero, one, or ordered set", "one selected pair"),
        "ordered-set handshake",
    )

    print("Helix composition contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
