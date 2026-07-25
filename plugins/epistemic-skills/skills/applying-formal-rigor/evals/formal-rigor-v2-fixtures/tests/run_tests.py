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
        "Focused is permitted only when all of these are true",
        "Do not emit P1-P9 reconciliation",
        "model → preconditions → fact mapping → derivation → result → residual mismatch",
        "fired", "not-applicable", "unmapped",
        "formal-rigor-record@2",
        "dominance", "pareto-set", "conditional", "underdetermined", "reversal", "reversible-probe",
        "derivation-correctness-by-envelope",
        "empirical-fact-without-observation",
        "gauntlet-independence",
        "A `reversal` rejects a premise or proposal; it does not by itself select a replacement",
        "Product/version semantics require an exact official source pin at every tier that emits a record",
        "Cross-check these observable cues before marking a family",
        "Coverage `modules` entries use the registry's exact unversioned `module_id`",
        "Do not let an unmapped external-semantic slice erase an adequately modeled engineering slice",
        "An invalid justification does not establish the opposite external meaning",
        "A pending empirical premise does not make an applicable formal module `unmapped`",
        "If more than one property family bears load, use `standard`",
        "Before emitting, rerun the tier gate and cue cross-check",
        "A rejected current premise can use `reversal` even when replacement selection remains unresolved",
        "asymptotic resource behavior with numerical stability crosses `P7` and `P8`",
        "`reversible-probe` keeps `selected_option` null",
    ):
        require(marker in skill_text, f"production SKILL.md missing v2 contract marker: {marker}")
    require("enumerate all 7 lenses" not in skill_text, "v1 closed seven-lens sweep remains normative")
    require("4NF decomposition eliminating the MVD `user_id ↠ method`" not in skill_text,
            "invalid ranked-contact 4NF derivation remains in production skill")
    require("formal-rigor-record@2" in router_text and "focused" in router_text,
            "router handoff does not distinguish focused inline output from v2 records")
    require("persistent schema, architecture, protocol, or operational decision" in skill_text
            and "use `standard`" in skill_text,
            "bounded theorem rule does not escalate a downstream decision mandate")
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

    dominance_facts = json.loads(
        (ROOT / "fixtures" / "cc-04-authorized-dominance" / "artifacts" / "facts.json")
        .read_text(encoding="utf-8")
    )
    require(
        dominance_facts["A"].get("reliability") == "equal"
        and dominance_facts["B"].get("reliability") == "equal",
        "authorized-dominance control prioritizes reliability without supplying a reliability tie",
    )

    for fixture_id in ("cc-03-postgresql18-rationale-correct", "tm-02-isolation-name-is-not-semantics"):
        facts = json.loads(
            (ROOT / "fixtures" / fixture_id / "artifacts" / "facts.json").read_text(encoding="utf-8")
        )
        history = facts.get("history")
        require(
            isinstance(history, dict) and len(history.get("transactions", [])) >= 2,
            f"{fixture_id}: concrete history obligation has no staged operations",
        )
    require(
        inventory["cc-03-postgresql18-rationale-correct"]["expected_invocation"] == ["standard"],
        "version-pinned PostgreSQL semantics incorrectly permit focused mode",
    )
    stale_priority = inventory["ss-02-priority-rule-moved"]
    require(stale_priority["freshness"].get("must_re_fire") is True,
            "changed authorized priority does not require re-fire")
    require(stale_priority["freshness"].get("current_authority_ref") == "operator-change-2",
            "changed authorized priority is incorrectly modeled as a code-revision change")
    require(stale_priority["synthesis"].get("allowed_outcomes") == ["reversal"],
            "changed-priority trap permits unsupported synthesis")
    regulatory_rows = {
        row["family"]: row for row in inventory["um-02-external-regulatory-semantics"]["coverage"]["required"]
    }
    require(regulatory_rows.get("P9", {}).get("status") == "unmapped",
            "unmapped regulatory terrain is not represented as unmapped coverage")
    cache_rows = {
        row["family"]: row for row in inventory["fc-02-value-of-information-probe"]["coverage"]["required"]
    }
    require(cache_rows.get("P7", {}).get("status") == "not-applicable"
            and cache_rows.get("P8", {}).get("status") == "unmapped"
            and cache_rows.get("P9", {}).get("status") == "fired",
            "cache replay fixture does not separate capacity, uncertainty, and decision coverage")
    token_rows = {
        row["family"]: row for row in inventory["tc-01-high-assurance-escalation"]["coverage"]["required"]
    }
    require(token_rows.get("P1", {}).get("status") == "fired",
            "token migration fixture omits protocol-semantics coverage")
    require(set(token_rows.get("P5", {}).get("any_modules", [])) == {
        "dependability-fault-models", "interface-protocol-evolution",
    }, "token migration fixture does not allow either adequate rollback module")
    require(inventory["um-01-custom-accelerator-memory-model"]["expected_invocation"] == ["high-assurance"],
            "model-sensitive accelerator proof incorrectly permits standard tier")
    chain_truth = inventory["tm-03-consistency-is-not-one-chain"]
    chain_rows = {row["family"]: row for row in chain_truth["coverage"]["required"]}
    require(chain_rows.get("P3", {}).get("status") == "fired"
            and chain_rows.get("P4", {}).get("status") == "fired",
            "universal consistency-chain fixture omits ordering or distribution coverage")
    require(set(chain_truth["synthesis"].get("allowed_outcomes", [])) == {"underdetermined", "reversal"},
            "universal consistency-chain fixture cannot distinguish premise reversal from unresolved replacement")

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

    refreshed_priority = {
        "response": "formal-rigor-fixture-response@1",
        "fixture": "ss-02-priority-rule-moved",
        "invocation": "standard",
        "skip_reason": None,
        "claim_assessments": [{"id": "c1", "state": "refuted", "derivation_ids": []}],
        "record": minimal_record(outcome="reversal"),
    }
    refreshed_priority["record"]["subject"]["revision"] = "same-code"
    refreshed_priority["record"]["decision_frame"]["priority_rule"]["authority_ref"] = "operator-change-2"
    refreshed_priority["record"]["coverage"][8] = {
        "family": "P9", "status": "fired", "modules": ["decision-theory-multiobjective"],
        "reason": "the current authority changes normative synthesis",
    }
    passed = score.score_fixture(stale_priority, refreshed_priority)
    require(passed["structural_pass"], f"current-authority re-fire failed: {passed['failures']}")
    stale_authority = copy.deepcopy(refreshed_priority)
    stale_authority["record"]["decision_frame"]["priority_rule"]["authority_ref"] = "old-authority"
    failed = score.score_fixture(stale_priority, stale_authority)
    require(not failed["structural_pass"] and "S9" in failed["dimensions_failed"],
            "stale decision authority was not rejected")

    alternative_module_truth = {
        "fixture_id": "alternative-module-synthetic", "expected_invocation": ["standard"],
        "claims": [{"id": "c1", "allowed_states": ["established"]}],
        "coverage": {"required": [{"family": "P5", "status": "fired", "any_modules": [
            "dependability-fault-models", "interface-protocol-evolution",
        ]}]},
        "decision_frame": {}, "synthesis": {}, "freshness": {},
    }
    alternative_module_response = {
        "response": "formal-rigor-fixture-response@1", "fixture": "alternative-module-synthetic",
        "invocation": "standard", "skip_reason": None,
        "claim_assessments": [{"id": "c1", "state": "established", "derivation_ids": []}],
        "record": minimal_record(),
    }
    alternative_module_response["record"]["coverage"][4] = {
        "family": "P5", "status": "fired", "modules": ["interface-protocol-evolution"],
        "reason": "version-skew-sensitive rollback",
    }
    passed = score.score_fixture(alternative_module_truth, alternative_module_response)
    require(passed["structural_pass"], f"adequate alternative module failed: {passed['failures']}")
    no_adequate_module = copy.deepcopy(alternative_module_response)
    no_adequate_module["record"]["coverage"][4]["modules"] = ["temporal-specification-model-checking"]
    failed = score.score_fixture(alternative_module_truth, no_adequate_module)
    require(not failed["structural_pass"] and "S3" in failed["dimensions_failed"],
            "scorer accepted a module outside the allowed alternatives")

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

    high_outer = {
        "response": "formal-rigor-fixture-response@1", "fixture": "high-tier-synthetic",
        "invocation": "high-assurance", "skip_reason": None,
        "claim_assessments": [{"id": "c1", "state": "established", "derivation_ids": []}],
        "focused_output": None, "record": minimal_record(),
    }
    high_truth = {
        "fixture_id": "high-tier-synthetic", "expected_invocation": ["high-assurance"],
        "claims": [{"id": "c1", "allowed_states": ["established"]}],
        "coverage": {}, "decision_frame": {}, "synthesis": {}, "freshness": {},
    }
    failed = score.score_fixture(high_truth, high_outer)
    require(not failed["structural_pass"] and "S1" in failed["dimensions_failed"],
            "high-assurance invocation accepted a standard-tier record")

    invalid_inventory = copy.deepcopy(inventory)
    invalid_inventory["ot-02-focused-not-ceremony"]["coverage"] = {
        "required": [{"family": "P7", "status": "fired", "modules": ["algorithms-data-structures"]}],
    }
    require(any("exclusive focused fixture carries record-only expectations" in error
                for error in score.validate_inventory(invalid_inventory)),
            "inventory validator accepted record-only obligations on an exclusive focused fixture")
    invalid_inventory = copy.deepcopy(inventory)
    invalid_inventory["um-02-external-regulatory-semantics"]["coverage"]["required"] = [
        {"family": "P9", "status": "fired", "modules": ["interface-protocol-evolution"]},
    ]
    require(any("unmapped class has no unmapped coverage" in error
                for error in score.validate_inventory(invalid_inventory)),
            "inventory validator accepted an unmapped trap with no unmapped coverage")

    require(score.validate_inventory(inventory) == [], "approved fixture inventory failed reconciliation")
    print("formal-rigor v2 structural scorer self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
