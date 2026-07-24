#!/usr/bin/env python3
"""Self-test for the formal-rigor v2 blinded structural scorer."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import copy
import json
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCORE_PATH = ROOT / "score.py"
SKILL_ROOT = ROOT.parents[1]
PACKAGE_ROOT = SKILL_ROOT.parents[1]

FIRST_RELEASE_MODULES = {
    "algorithms-data-structures",
    "decision-theory-multiobjective",
    "dependability-fault-models",
    "distributed-consistency",
    "interface-protocol-evolution",
    "numerical-analysis-floating-point",
    "queueing-capacity-parallelism",
    "relational-dependencies",
    "security-information-flow-privacy",
    "temporal-specification-model-checking",
    "transaction-histories",
}

MODULE_CONTRACT_FIELDS = {
    "module_id:", "version:", "property_families:", "trigger_properties:",
    "constructs:", "models:", "required_inputs:", "applicability_template:",
    "derivation_templates:", "counterexample_obligations:",
    "result_vocabulary:", "canonical_sources:", "known_exclusions:",
}

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


def assert_v2_production_contract() -> None:
    skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    theory_text = (SKILL_ROOT / "theory-battery.md").read_text(encoding="utf-8")
    router_text = (PACKAGE_ROOT / "skills" / "using-epistemic-skills" / "SKILL.md").read_text(encoding="utf-8")

    for marker in (
        "cost of error × uncertainty × downstream dependence × irreversibility",
        "at most six short bullets or 250 visible words",
        "Do not emit P1-P9 reconciliation",
        "model → preconditions → fact mapping → derivation → result → residual mismatch",
        "fired", "not-applicable", "unmapped",
        "formal-rigor-record@2",
        "dominance", "pareto-set", "conditional", "underdetermined", "reversal", "reversible-probe",
    ):
        require(marker in skill_text, f"production SKILL.md missing v2 contract marker: {marker}")
    require("enumerate all 7 lenses" not in skill_text, "v1 closed seven-lens sweep remains normative")
    require("4NF decomposition eliminating the MVD `user_id ↠ method`" not in skill_text,
            "invalid ranked-contact 4NF derivation remains in production skill")
    require("formal-rigor-record@2" in router_text and "focused" in router_text,
            "router handoff does not distinguish focused inline output from v2 records")
    require("compatibility" in theory_text.lower() and "reference/modules/index.md" in theory_text,
            "theory-battery.md is not an explicit compatibility index")

    modules_dir = SKILL_ROOT / "reference" / "modules"
    require((modules_dir / "index.md").is_file(), "missing specialist module registry")
    actual_modules = {path.stem for path in modules_dir.glob("*.md") if path.name != "index.md"}
    require(actual_modules == FIRST_RELEASE_MODULES,
            f"first-release module set mismatch: {sorted(actual_modules ^ FIRST_RELEASE_MODULES)}")
    for module_id in sorted(FIRST_RELEASE_MODULES):
        text = (modules_dir / f"{module_id}.md").read_text(encoding="utf-8")
        for field in MODULE_CONTRACT_FIELDS:
            require(field in text, f"{module_id}: missing module contract field {field}")
        require(f"module_id: {module_id}" in text, f"{module_id}: module_id/path mismatch")

    validator = SKILL_ROOT / "validate_record.py"
    valid_example = SKILL_ROOT / "examples" / "valid-formal-rigor-record.json"
    record_schema_path = ROOT / "formal-rigor-record.schema.json"
    require(validator.is_file(), "missing standalone formal-rigor-record@2 validator")
    require(valid_example.is_file(), "missing valid formal-rigor-record@2 example")
    record_schema = json.loads(record_schema_path.read_text(encoding="utf-8"))
    derivation_required = set(record_schema["properties"]["derivations"]["items"]["required"])
    require("counterexample" in derivation_required, "record schema omits the counterexample field")
    frame_schema = record_schema["properties"]["decision_frame"]
    require(frame_schema.get("additionalProperties") is False, "decision-frame schema is not closed")
    require("authority_ref" in frame_schema["properties"]["priority_rule"]["required"],
            "record schema does not require decision authority provenance")
    spec = importlib.util.spec_from_file_location("formal_rigor_record_validator", validator)
    require(spec is not None and spec.loader is not None, "cannot load standalone record validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    example = json.loads(valid_example.read_text(encoding="utf-8"))
    require(module.validate_record(example) == [], "valid formal-rigor-record@2 example failed validation")
    invalid = copy.deepcopy(example)
    invalid["coverage"][0]["status"] = "fired"
    invalid["coverage"][0]["modules"] = []
    require(module.validate_record(invalid), "validator accepted a fired family with no module")
    single_option = copy.deepcopy(example)
    single_option["decision_frame"]["alternatives"] = [
        {"id": "proposal", "kind": "option", "description": "The design under review."}
    ]
    require(
        not any("null-option" in error for error in module.validate_record(single_option)),
        "validator incorrectly requires a null option for single-option justification",
    )


def main() -> int:
    assert_v2_production_contract()
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
