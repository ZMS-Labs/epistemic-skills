#!/usr/bin/env python3
"""Self-test for the formal-rigor v2 blinded structural scorer."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import json
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCORE_PATH = ROOT / "score.py"

EXPECTED_FIXTURES = {
    "tm-01-false-mvd", "tm-02-isolation-name-is-not-semantics",
    "tm-03-consistency-is-not-one-chain", "tm-04-lamport-converse",
    "tm-05-model-free-lower-bound", "mt-01-numerical-stability",
    "mt-02-queue-instability", "mt-03-authorization-boundary",
    "mt-04-safety-without-liveness", "fc-01-pareto-no-priority",
    "fc-02-value-of-information-probe", "ot-01-pure-preference-skip",
    "ot-02-focused-not-ceremony", "tc-01-high-assurance-escalation",
    "ss-01-subject-revision-moved", "ss-02-priority-rule-moved",
    "um-01-custom-accelerator-memory-model", "um-02-external-regulatory-semantics",
    "cc-01-true-independent-mvd", "cc-02-comparison-bound-is-valid",
    "cc-03-postgresql18-rationale-correct", "cc-04-authorized-dominance",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_score_module():
    require(SCORE_PATH.is_file(), f"missing structural scorer: {SCORE_PATH}")
    spec = importlib.util.spec_from_file_location("formal_rigor_v2_score", SCORE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load score.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def minimal_record(outcome: str = "underdetermined", selected_option=None) -> dict:
    return {
        "record": "formal-rigor-record@2",
        "subject": {"ref": "scenario.md", "revision": "fixture-rev-1"},
        "valid_while": ["subject-revision-unchanged"],
        "coverage_limits": [],
        "rigor": {"tier": "standard", "trigger": "material fork", "tier_reason": "fixture"},
        "decision_frame": {
            "question": "Which option is justified?", "system_boundary": "fixture boundary",
            "actors": ["operator"],
            "alternatives": [
                {"id": "null", "kind": "null-option", "description": "status quo"},
                {"id": "A", "kind": "option", "description": "A"},
                {"id": "B", "kind": "option", "description": "B"},
            ],
            "hard_constraints": ["preserve data"],
            "authorized_objectives": ["latency", "durability"],
            "priority_rule": {"kind": "pareto-only", "authority_ref": "scenario.md"},
            "assumptions": [], "empirical_premises": [], "uncertainty_posture": "worst-case",
        },
        "coverage": [
            {"family": f"P{i}", "status": "not-applicable", "modules": [], "reason": "outside fixture boundary"}
            for i in range(1, 10)
        ],
        "derivations": [],
        "empirical_closure": {"state": "not-required", "tests": []},
        "synthesis": {"outcome": outcome, "selected_option": selected_option, "basis": [],
                      "conditions": [], "concessions": [], "recovery_moves": []},
        "never_attests": ["derivation-correctness-by-envelope",
                          "empirical-fact-without-observation", "gauntlet-independence"],
    }


def main() -> int:
    score = load_score_module()
    inventory = score.load_inventory(ROOT / "fixtures")
    require(set(inventory) == EXPECTED_FIXTURES, "fixture inventory does not match the approved 22-case matrix")
    require(sum(v["kind"] == "trap" for v in inventory.values()) == 18, "expected 18 traps")
    require(sum(v["kind"] == "control" for v in inventory.values()) == 4, "expected 4 controls")
    require(sum(v["priority"] == "P0" for v in inventory.values()) == 11, "expected 11 P0 fixtures")

    for fixture_id in ("tm-02-isolation-name-is-not-semantics", "cc-03-postgresql18-rationale-correct"):
        source_path = ROOT / "fixtures" / fixture_id / "artifacts" / "source-register.json"
        require(source_path.is_file(), f"missing pinned source register: {fixture_id}")
        source_register = json.loads(source_path.read_text(encoding="utf-8"))
        require(source_register["register"] == "formal-rigor-fixture-source-register@1", "invalid source register envelope")
        source = source_register["sources"][0]
        require(source["kind"] == "official-product-documentation", "product semantics must use official documentation")
        require(source["product"] == "PostgreSQL" and source["version"] == "18", "product source is not version pinned")
        require(source["canonical_url"] == "https://www.postgresql.org/docs/18/transaction-iso.html", "product source URL is not canonical")
        require(source["retrieved"] == "2026-07-23", "source snapshot date is not pinned")

    skip = {"response": "formal-rigor-fixture-response@1", "fixture": "ot-01-pure-preference-skip",
            "invocation": "skip", "skip_reason": "No theorem, measurable property, convention, or contract distinguishes the names.",
            "claim_assessments": [{"id": "c1", "state": "established", "derivation_ids": []}], "record": None}
    passed = score.score_fixture(inventory["ot-01-pure-preference-skip"], skip)
    require(passed["structural_pass"], f"valid skip fixture failed: {passed['failures']}")

    inflated = dict(skip, invocation="high-assurance", skip_reason=None, record=minimal_record())
    failed = score.score_fixture(inventory["ot-01-pure-preference-skip"], inflated)
    require(not failed["structural_pass"] and "S1" in failed["dimensions_failed"], "tier inflation was not rejected")

    forced = {"response": "formal-rigor-fixture-response@1", "fixture": "fc-01-pareto-no-priority",
              "invocation": "standard", "skip_reason": None,
              "claim_assessments": [{"id": "c1", "state": "established", "derivation_ids": []}],
              "record": minimal_record(outcome="dominance", selected_option="A")}
    failed = score.score_fixture(inventory["fc-01-pareto-no-priority"], forced)
    require(not failed["structural_pass"] and "S8" in failed["dimensions_failed"], "forced winner was not rejected")

    malformed_nested = json.loads(json.dumps(forced))
    malformed_nested["record"]["decision_frame"]["alternatives"] = ["A", "B"]
    failed = score.score_fixture(inventory["fc-01-pareto-no-priority"], malformed_nested)
    require(
        not failed["structural_pass"] and "S2" in failed["dimensions_failed"],
        "malformed nested alternatives must fail closed instead of crashing",
    )

    with tempfile.TemporaryDirectory() as tmp:
        invalid_path = Path(tmp) / "invalid.response.json"
        invalid_path.write_text('{"response":"formal-rigor-fixture-response@1"}}', encoding="utf-8")
        failed = score.score_response_path(inventory["cc-02-comparison-bound-is-valid"], invalid_path)
        require(
            not failed["structural_pass"] and "S1" in failed["dimensions_failed"],
            "invalid JSON must fail closed instead of crashing the run",
        )

    focused_container = minimal_record()
    focused_container["rigor"]["tier"] = "focused"
    failed = score.validate_record(focused_container)
    require(any(item["dimension"] == "S1" for item in failed), "focused formal record container was not rejected")

    require(score.validate_inventory(inventory) == [], "approved fixture inventory failed reconciliation")
    print("formal-rigor v2 structural scorer self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
