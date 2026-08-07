#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verify_watch_commission import validate_record  # noqa: E402


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
        "destination": {"ref": "recipient:test", "reachable": True},
        "external_observer": {
            "substrate": "fixture-adapter",
            "mechanism_ref": "fixture://watch/001",
            "persistent_outside_session": True,
            "enabled": True,
        },
        "kill_switch": {"procedure_ref": "fixture://kill/001", "exercised": True},
        "proof": {
            "authorized_by": "operator:test",
            "safe_crossing": "fixture threshold override",
            "production_path": True,
            "bound_crossed": True,
            "alert_received": True,
            "received_at": "2026-08-07T12:00:00Z",
        },
        "state": "PROVEN",
        "block_reason": None,
        "reprove_after": "2026-09-07T12:00:00Z",
        "handoff": {"on_crossing": ["triage", "decision-ledger"]},
        "coverage_limits": ["fixture only"],
    }


def assert_rejected(record: dict[str, object], code: str) -> None:
    errors = validate_record(record)
    assert any(error.startswith(code + ":") for error in errors), errors


def test_complete_external_path_is_proven() -> None:
    assert validate_record(proven_record()) == []


def test_skill_text_cannot_be_the_external_observer() -> None:
    record = proven_record()
    record["external_observer"] = {
        "substrate": "markdown-skill",
        "mechanism_ref": "plugins/epistemic-skills/skills/watch/SKILL.md",
        "persistent_outside_session": False,
        "enabled": True,
    }
    assert_rejected(record, "EXTERNAL_PERSISTENCE_REQUIRED")


def test_silence_cannot_be_proven() -> None:
    record = proven_record()
    proof = copy.deepcopy(record["proof"])
    assert isinstance(proof, dict)
    proof["alert_received"] = False
    proof["received_at"] = None
    record["proof"] = proof
    assert_rejected(record, "ALERT_RECEIPT_REQUIRED")


def test_documented_kill_switch_is_not_exercised() -> None:
    record = proven_record()
    record["kill_switch"] = {"procedure_ref": "docs/kill.md", "exercised": False}
    assert_rejected(record, "KILL_SWITCH_EXERCISE_REQUIRED")


def test_bypass_message_is_not_production_path_proof() -> None:
    record = proven_record()
    proof = copy.deepcopy(record["proof"])
    assert isinstance(proof, dict)
    proof["production_path"] = False
    record["proof"] = proof
    assert_rejected(record, "PRODUCTION_PATH_REQUIRED")


def test_missing_substrate_is_explicitly_blocked() -> None:
    record = proven_record()
    record["state"] = "BLOCKED"
    record["block_reason"] = "NO_EXECUTION_SUBSTRATE"
    record["external_observer"] = {
        "substrate": None,
        "mechanism_ref": None,
        "persistent_outside_session": False,
        "enabled": False,
    }
    record["kill_switch"] = {"procedure_ref": None, "exercised": False}
    record["proof"] = {
        "authorized_by": None,
        "safe_crossing": None,
        "production_path": False,
        "bound_crossed": False,
        "alert_received": False,
        "received_at": None,
    }
    assert validate_record(record) == []


def test_blocked_requires_a_closed_reason() -> None:
    record = proven_record()
    record["state"] = "BLOCKED"
    record["block_reason"] = None
    assert_rejected(record, "BLOCK_REASON_REQUIRED")


def test_non_proven_record_cannot_claim_active_watching() -> None:
    record = proven_record()
    record["state"] = "INERT"
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = True
    record["external_observer"] = observer
    assert_rejected(record, "INERT_MUST_BE_DISABLED")


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
