#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verify_watch_commission import validate_record  # noqa: E402


def empty_proof() -> dict[str, object]:
    return {
        "authorized_by": None,
        "authorization_ref": None,
        "safe_crossing": None,
        "production_path": False,
        "bound_crossed": False,
        "alert_received": False,
        "received_at": None,
        "alert_receipt_ref": None,
    }


def empty_failure() -> dict[str, object]:
    return {
        "kind": None,
        "detail": None,
        "observed_at": None,
        "receipt_ref": None,
    }


def empty_block_evidence() -> dict[str, object]:
    return {
        "detail": None,
        "observed_at": None,
        "receipt_ref": None,
    }


def proven_record() -> dict[str, object]:
    return {
        "schema": "watch-commission@1",
        "commission_id": "wc-test-001",
        "subject": {"ref": "service:example", "revision": "rev-1"},
        "bound": {
            "expression": "free_space_percent < 15",
            "units": "percent",
            "direction": "below",
            "threshold": 15,
        },
        "probe": {
            "mechanism": "external metric query",
            "cadence_or_event": "every 5 minutes",
            "failure_modes": ["timeout", "authentication failure"],
        },
        "destination": {
            "ref": "recipient:test",
            "reachable": True,
            "reachability_receipt_ref": "fixture://receipt/destination-001",
        },
        "external_observer": {
            "substrate_kind": "fixture",
            "substrate": "fixture-adapter",
            "mechanism_ref": "fixture://watch/001",
            "persistence_receipt_ref": "fixture://receipt/persistence-001",
            "persistent_outside_session": True,
            "enabled": True,
        },
        "kill_switch": {
            "procedure_ref": "fixture://kill/001",
            "exercised": True,
            "exercise_receipt_ref": "fixture://receipt/kill-001",
        },
        "proof": {
            "authorized_by": "operator:test",
            "authorization_ref": "fixture://authority/proof-001",
            "safe_crossing": "fixture threshold override",
            "production_path": True,
            "bound_crossed": True,
            "alert_received": True,
            "received_at": "2026-08-07T12:00:00Z",
            "alert_receipt_ref": "fixture://receipt/alert-001",
        },
        "failure": empty_failure(),
        "block_evidence": empty_block_evidence(),
        "state": "PROVEN",
        "block_reason": None,
        "reprove_after": "2026-09-07T12:00:00Z",
        "handoff": {"on_crossing": ["triage", "decision-ledger"]},
        "coverage_limits": [
            "isolated fixture adapter; no production provider claimed"
        ],
    }


def blocked_no_substrate_record() -> dict[str, object]:
    record = proven_record()
    record["state"] = "BLOCKED"
    record["block_reason"] = "NO_EXECUTION_SUBSTRATE"
    record["external_observer"] = {
        "substrate_kind": None,
        "substrate": None,
        "mechanism_ref": None,
        "persistence_receipt_ref": None,
        "persistent_outside_session": False,
        "enabled": False,
    }
    record["kill_switch"] = {
        "procedure_ref": None,
        "exercised": False,
        "exercise_receipt_ref": None,
    }
    record["proof"] = empty_proof()
    record["failure"] = empty_failure()
    record["block_evidence"] = {
        "detail": "capability discovery found no external observation substrate",
        "observed_at": "2026-08-07T11:55:00Z",
        "receipt_ref": "fixture://receipt/block-no-substrate-001",
    }
    record["reprove_after"] = None
    return record


def assert_rejected(record: dict[str, object], code: str) -> None:
    errors = validate_record(record)
    assert any(error.startswith(code + ":") for error in errors), errors


def test_complete_external_path_is_proven() -> None:
    assert validate_record(proven_record()) == []


def test_skill_text_cannot_be_the_external_observer_even_if_it_claims_persistence() -> None:
    record = proven_record()
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["substrate_kind"] = "markdown-skill"
    observer["substrate"] = "Markdown skill"
    observer["mechanism_ref"] = "plugins/epistemic-skills/skills/watch/SKILL.md"
    record["external_observer"] = observer
    assert_rejected(record, "INVALID_SUBSTRATE_KIND")


def test_allowed_kind_cannot_hide_a_prompt_time_mechanism_ref() -> None:
    record = proven_record()
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["substrate_kind"] = "fixture"
    observer["mechanism_ref"] = "plugins/epistemic-skills/skills/watch/SKILL.md"
    record["external_observer"] = observer
    assert_rejected(record, "PROMPT_TIME_MECHANISM_FORBIDDEN")


def test_self_asserted_receipt_is_not_external_evidence() -> None:
    record = proven_record()
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["persistence_receipt_ref"] = "self-asserted://persistent-because-I-said-so"
    record["external_observer"] = observer
    assert_rejected(record, "INVALID_EVIDENCE_REF")


def test_fixture_proof_must_disclose_its_scope() -> None:
    record = proven_record()
    record["coverage_limits"] = ["all checks passed"]
    assert_rejected(record, "FIXTURE_SCOPE_REQUIRED")


def test_silence_cannot_be_proven() -> None:
    record = proven_record()
    proof = copy.deepcopy(record["proof"])
    assert isinstance(proof, dict)
    proof["alert_received"] = False
    proof["received_at"] = None
    proof["alert_receipt_ref"] = None
    record["proof"] = proof
    assert_rejected(record, "ALERT_RECEIPT_REQUIRED")


def test_documented_kill_switch_is_not_exercised() -> None:
    record = proven_record()
    record["kill_switch"] = {
        "procedure_ref": "docs/kill.md",
        "exercised": False,
        "exercise_receipt_ref": None,
    }
    assert_rejected(record, "KILL_SWITCH_EXERCISE_REQUIRED")


def test_bypass_message_is_not_production_path_proof() -> None:
    record = proven_record()
    proof = copy.deepcopy(record["proof"])
    assert isinstance(proof, dict)
    proof["production_path"] = False
    record["proof"] = proof
    assert_rejected(record, "PRODUCTION_PATH_REQUIRED")


def test_missing_substrate_is_explicitly_blocked() -> None:
    assert validate_record(blocked_no_substrate_record()) == []


def test_blocked_requires_a_closed_reason() -> None:
    record = blocked_no_substrate_record()
    record["block_reason"] = None
    assert_rejected(record, "BLOCK_REASON_REQUIRED")


def test_blocked_requires_dated_evidence() -> None:
    record = blocked_no_substrate_record()
    record["block_evidence"] = empty_block_evidence()
    assert_rejected(record, "BLOCK_EVIDENCE_REQUIRED")


def test_non_blocked_state_cannot_carry_live_block_evidence() -> None:
    record = proven_record()
    record["block_evidence"] = {
        "detail": "stale block claim",
        "observed_at": "2026-08-07T11:55:00Z",
        "receipt_ref": "fixture://receipt/stale-block-001",
    }
    assert_rejected(record, "BLOCK_EVIDENCE_FORBIDDEN")


def test_block_reason_must_match_the_recorded_dependency() -> None:
    record = blocked_no_substrate_record()
    observer = copy.deepcopy(proven_record()["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = False
    record["external_observer"] = observer
    assert_rejected(record, "BLOCK_REASON_MISMATCH")


def test_prepared_mechanism_remains_blocked_until_kill_switch_is_proven() -> None:
    record = proven_record()
    record["state"] = "BLOCKED"
    record["block_reason"] = "KILL_SWITCH_UNPROVEN"
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = False
    record["external_observer"] = observer
    record["kill_switch"] = {
        "procedure_ref": "fixture://kill/001",
        "exercised": False,
        "exercise_receipt_ref": None,
    }
    record["proof"] = empty_proof()
    record["failure"] = empty_failure()
    record["block_evidence"] = {
        "detail": "the real mechanism exists but its disable path has not been exercised",
        "observed_at": "2026-08-07T11:57:00Z",
        "receipt_ref": "fixture://receipt/block-kill-unproven-001",
    }
    record["reprove_after"] = None
    assert validate_record(record) == []


def test_declared_state_cannot_hide_a_prepared_mechanism() -> None:
    record = proven_record()
    record["state"] = "DECLARED"
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = False
    record["external_observer"] = observer
    record["proof"] = empty_proof()
    record["failure"] = empty_failure()
    record["block_evidence"] = empty_block_evidence()
    record["reprove_after"] = None
    assert_rejected(record, "DECLARED_MECHANISM_FORBIDDEN")


def test_non_proven_record_cannot_claim_active_watching() -> None:
    record = proven_record()
    record["state"] = "INERT"
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = True
    record["external_observer"] = observer
    assert_rejected(record, "INERT_MUST_BE_DISABLED")


def test_successful_proof_can_end_inert_without_claiming_current_watching() -> None:
    record = proven_record()
    record["state"] = "INERT"
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = False
    record["external_observer"] = observer
    assert validate_record(record) == []


def test_partial_historical_proof_is_rejected_for_inert_state() -> None:
    record = proven_record()
    record["state"] = "INERT"
    observer = copy.deepcopy(record["external_observer"])
    proof = copy.deepcopy(record["proof"])
    assert isinstance(observer, dict)
    assert isinstance(proof, dict)
    observer["enabled"] = False
    proof["bound_crossed"] = False
    record["external_observer"] = observer
    record["proof"] = proof
    assert_rejected(record, "INCOMPLETE_PROOF_BUNDLE")


def test_proven_requires_a_reproof_boundary() -> None:
    record = proven_record()
    record["reprove_after"] = None
    assert_rejected(record, "REPROOF_BOUNDARY_REQUIRED")


def test_positive_claims_require_evidence_receipts() -> None:
    cases = [
        ("destination", "reachability_receipt_ref", "DESTINATION_RECEIPT_REQUIRED"),
        ("external_observer", "persistence_receipt_ref", "PERSISTENCE_RECEIPT_REQUIRED"),
        ("kill_switch", "exercise_receipt_ref", "KILL_SWITCH_RECEIPT_REQUIRED"),
        ("proof", "authorization_ref", "PROOF_AUTHORIZATION_RECEIPT_REQUIRED"),
        ("proof", "alert_receipt_ref", "ALERT_RECEIPT_REF_REQUIRED"),
    ]
    for object_name, field, code in cases:
        record = proven_record()
        child = copy.deepcopy(record[object_name])
        assert isinstance(child, dict)
        child[field] = None
        record[object_name] = child
        assert_rejected(record, code)


def test_suspect_requires_an_observed_failure_not_a_possible_failure_list() -> None:
    record = proven_record()
    record["state"] = "SUSPECT"
    record["failure"] = empty_failure()
    assert_rejected(record, "SUSPECT_FAILURE_REQUIRED")


def test_suspect_with_a_receipted_observed_failure_is_valid() -> None:
    record = proven_record()
    record["state"] = "SUSPECT"
    record["failure"] = {
        "kind": "delivery",
        "detail": "destination returned an authentication failure",
        "observed_at": "2026-08-07T12:05:00Z",
        "receipt_ref": "fixture://receipt/failure-001",
    }
    assert validate_record(record) == []


def test_bound_direction_is_closed() -> None:
    record = proven_record()
    bound = copy.deepcopy(record["bound"])
    assert isinstance(bound, dict)
    bound["direction"] = "sideways"
    record["bound"] = bound
    assert_rejected(record, "INVALID_DIRECTION")


def test_skill_surface_names_commission_boundary() -> None:
    text = (ROOT.parents[1] / "skills" / "watch" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    required = [
        "commission-watch",
        "The skill is not the external observer",
        "watch-commission@1",
        "BLOCKED",
        "NO_EXECUTION_SUBSTRATE",
    ]
    missing = [needle for needle in required if needle not in text]
    assert missing == [], missing


def test_committed_examples_match_expected_oracles() -> None:
    example_dir = ROOT / "examples"
    for path in sorted(example_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        expected = payload.pop("_expected")
        errors = validate_record(payload)
        if expected == "ACCEPT":
            assert errors == [], (path.name, errors)
        else:
            assert errors, path.name


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as error:  # noqa: BLE001 - standalone zero-dependency runner
            failures.append(f"{test.__name__}: {error}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"watch-commission tests ok: {len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
