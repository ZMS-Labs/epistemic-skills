#!/usr/bin/env python3
"""Validate watch-commission@1 records without third-party dependencies."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

STATES = {"DECLARED", "BLOCKED", "INERT", "PROVEN", "SUSPECT"}
BLOCK_REASONS = {
    "NO_EXECUTION_SUBSTRATE",
    "NO_REACHABLE_DESTINATION",
    "NO_AUTHORITY_TO_ENABLE",
    "NO_KILL_SWITCH",
    "KILL_SWITCH_UNPROVEN",
    "NO_SAFE_PROOF_CROSSING",
    "PROBE_UNAVAILABLE",
}

TOP_LEVEL_FIELDS = {
    "schema",
    "commission_id",
    "subject",
    "bound",
    "probe",
    "destination",
    "external_observer",
    "kill_switch",
    "proof",
    "state",
    "block_reason",
    "reprove_after",
    "handoff",
    "coverage_limits",
}

OBJECT_FIELDS = {
    "subject": {"ref", "revision"},
    "bound": {"expression", "units", "direction", "threshold"},
    "probe": {"mechanism", "cadence_or_event", "failure_modes"},
    "destination": {"ref", "reachable"},
    "external_observer": {
        "substrate",
        "mechanism_ref",
        "persistent_outside_session",
        "enabled",
    },
    "kill_switch": {"procedure_ref", "exercised"},
    "proof": {
        "authorized_by",
        "safe_crossing",
        "production_path",
        "bound_crossed",
        "alert_received",
        "received_at",
    },
    "handoff": {"on_crossing"},
}


def _error(errors: list[str], code: str, detail: str) -> None:
    errors.append(f"{code}: {detail}")


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_object(
    record: dict[str, Any],
    key: str,
    errors: list[str],
) -> dict[str, Any] | None:
    value = record.get(key)
    if not isinstance(value, dict):
        _error(errors, "MISSING_FIELD", f"{key} must be an object")
        return None
    expected = OBJECT_FIELDS[key]
    missing = sorted(expected - value.keys())
    for field in missing:
        _error(errors, "MISSING_FIELD", f"{key}.{field} is required")
    unexpected = sorted(value.keys() - expected)
    for field in unexpected:
        _error(errors, "UNEXPECTED_FIELD", f"{key}.{field} is not allowed")
    return value


def _require_bool(
    container: dict[str, Any] | None,
    key: str,
    path: str,
    errors: list[str],
) -> bool | None:
    if container is None or key not in container:
        return None
    value = container[key]
    if not isinstance(value, bool):
        _error(errors, "INVALID_TYPE", f"{path}.{key} must be boolean")
        return None
    return value


def _require_string_or_null(
    container: dict[str, Any] | None,
    key: str,
    path: str,
    errors: list[str],
) -> str | None:
    if container is None or key not in container:
        return None
    value = container[key]
    if value is not None and not isinstance(value, str):
        _error(errors, "INVALID_TYPE", f"{path}.{key} must be a string or null")
        return None
    return value


def _require_string_list(
    container: dict[str, Any] | None,
    key: str,
    path: str,
    errors: list[str],
) -> list[str] | None:
    if container is None or key not in container:
        return None
    value = container[key]
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        _error(errors, "INVALID_TYPE", f"{path}.{key} must be an array of strings")
        return None
    return value


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return named semantic violations; an empty list means valid."""
    errors: list[str] = []

    if not isinstance(record, dict):
        return ["RECORD_MUST_BE_OBJECT: root must be an object"]

    missing_top = sorted(TOP_LEVEL_FIELDS - record.keys())
    for field in missing_top:
        _error(errors, "MISSING_FIELD", f"{field} is required")
    unexpected_top = sorted(record.keys() - TOP_LEVEL_FIELDS)
    for field in unexpected_top:
        _error(errors, "UNEXPECTED_FIELD", f"{field} is not allowed")

    if record.get("schema") != "watch-commission@1":
        _error(errors, "SCHEMA_MISMATCH", "schema must equal watch-commission@1")
    if not _is_non_empty_string(record.get("commission_id")):
        _error(errors, "MISSING_FIELD", "commission_id must be a non-empty string")

    subject = _require_object(record, "subject", errors)
    bound = _require_object(record, "bound", errors)
    probe = _require_object(record, "probe", errors)
    destination = _require_object(record, "destination", errors)
    observer = _require_object(record, "external_observer", errors)
    kill_switch = _require_object(record, "kill_switch", errors)
    proof = _require_object(record, "proof", errors)
    handoff = _require_object(record, "handoff", errors)

    if subject is not None:
        if not _is_non_empty_string(subject.get("ref")):
            _error(errors, "MISSING_FIELD", "subject.ref must be a non-empty string")
        revision = subject.get("revision")
        if revision is not None and not isinstance(revision, (str, int)):
            _error(errors, "INVALID_TYPE", "subject.revision must be string, integer, or null")

    if bound is not None:
        for field in ("expression", "units", "direction"):
            if not _is_non_empty_string(bound.get(field)):
                _error(errors, "MISSING_FIELD", f"bound.{field} must be a non-empty string")
        if "threshold" in bound and bound["threshold"] is None:
            _error(errors, "MISSING_FIELD", "bound.threshold cannot be null")

    failure_modes = _require_string_list(probe, "failure_modes", "probe", errors)
    if probe is not None:
        for field in ("mechanism", "cadence_or_event"):
            if not _is_non_empty_string(probe.get(field)):
                _error(errors, "MISSING_FIELD", f"probe.{field} must be a non-empty string")

    if destination is not None:
        ref = destination.get("ref")
        if ref is not None and not isinstance(ref, str):
            _error(errors, "INVALID_TYPE", "destination.ref must be a string or null")
    destination_reachable = _require_bool(destination, "reachable", "destination", errors)

    substrate = _require_string_or_null(observer, "substrate", "external_observer", errors)
    mechanism_ref = _require_string_or_null(
        observer, "mechanism_ref", "external_observer", errors
    )
    persistent = _require_bool(
        observer, "persistent_outside_session", "external_observer", errors
    )
    enabled = _require_bool(observer, "enabled", "external_observer", errors)

    procedure_ref = _require_string_or_null(
        kill_switch, "procedure_ref", "kill_switch", errors
    )
    exercised = _require_bool(kill_switch, "exercised", "kill_switch", errors)

    authorized_by = _require_string_or_null(proof, "authorized_by", "proof", errors)
    safe_crossing = _require_string_or_null(proof, "safe_crossing", "proof", errors)
    production_path = _require_bool(proof, "production_path", "proof", errors)
    bound_crossed = _require_bool(proof, "bound_crossed", "proof", errors)
    alert_received = _require_bool(proof, "alert_received", "proof", errors)
    received_at = _require_string_or_null(proof, "received_at", "proof", errors)

    on_crossing = _require_string_list(handoff, "on_crossing", "handoff", errors)
    if on_crossing is not None and len(on_crossing) != len(set(on_crossing)):
        _error(errors, "DUPLICATE_HANDOFF", "handoff.on_crossing contains duplicates")

    coverage_limits = record.get("coverage_limits")
    if not isinstance(coverage_limits, list) or any(
        not isinstance(item, str) for item in coverage_limits
    ):
        _error(errors, "INVALID_TYPE", "coverage_limits must be an array of strings")
        coverage_limits = []

    reprove_after = record.get("reprove_after")
    if reprove_after is not None and not isinstance(reprove_after, str):
        _error(errors, "INVALID_TYPE", "reprove_after must be a string or null")

    state = record.get("state")
    if state not in STATES:
        _error(errors, "INVALID_STATE", f"state must be one of {sorted(STATES)}")
        return errors

    block_reason = record.get("block_reason")
    if state == "BLOCKED":
        if block_reason is None:
            _error(errors, "BLOCK_REASON_REQUIRED", "BLOCKED requires block_reason")
        elif block_reason not in BLOCK_REASONS:
            _error(
                errors,
                "INVALID_BLOCK_REASON",
                f"block_reason must be one of {sorted(BLOCK_REASONS)}",
            )
    elif block_reason is not None:
        _error(errors, "BLOCK_REASON_FORBIDDEN", "block_reason is only valid for BLOCKED")

    if persistent is True and not _is_non_empty_string(mechanism_ref):
        _error(
            errors,
            "EXTERNAL_MECHANISM_REQUIRED",
            "persistent observer requires external_observer.mechanism_ref",
        )

    if state == "DECLARED":
        if enabled is True:
            _error(errors, "DECLARED_MUST_BE_DISABLED", "DECLARED observer cannot be enabled")
        if alert_received is True or received_at is not None:
            _error(errors, "ALERT_RECEIPT_FORBIDDEN", "DECLARED cannot claim an alert receipt")

    elif state == "BLOCKED":
        if enabled is True:
            _error(errors, "BLOCKED_MUST_BE_DISABLED", "BLOCKED observer cannot be enabled")
        if alert_received is True or received_at is not None:
            _error(errors, "ALERT_RECEIPT_FORBIDDEN", "BLOCKED cannot claim an alert receipt")

    elif state == "INERT":
        if not _is_non_empty_string(substrate) or not _is_non_empty_string(mechanism_ref):
            _error(
                errors,
                "EXTERNAL_MECHANISM_REQUIRED",
                "INERT requires substrate and mechanism_ref",
            )
        if persistent is not True:
            _error(
                errors,
                "EXTERNAL_PERSISTENCE_REQUIRED",
                "INERT requires a mechanism persistent outside the session",
            )
        if enabled is not False:
            _error(errors, "INERT_MUST_BE_DISABLED", "INERT observer must be disabled")
        if alert_received is True or received_at is not None:
            _error(errors, "ALERT_RECEIPT_FORBIDDEN", "INERT cannot claim an alert receipt")

    elif state == "PROVEN":
        if destination_reachable is not True:
            _error(
                errors,
                "DESTINATION_REACHABILITY_REQUIRED",
                "PROVEN requires a reachable destination",
            )
        if not _is_non_empty_string(substrate) or not _is_non_empty_string(mechanism_ref):
            _error(
                errors,
                "EXTERNAL_MECHANISM_REQUIRED",
                "PROVEN requires substrate and mechanism_ref",
            )
        if persistent is not True:
            _error(
                errors,
                "EXTERNAL_PERSISTENCE_REQUIRED",
                "PROVEN requires a mechanism persistent outside the session",
            )
        if enabled is not True:
            _error(errors, "PROVEN_MUST_BE_ENABLED", "PROVEN observer must be enabled")
        if not _is_non_empty_string(procedure_ref) or exercised is not True:
            _error(
                errors,
                "KILL_SWITCH_EXERCISE_REQUIRED",
                "PROVEN requires a real exercised kill switch",
            )
        if not _is_non_empty_string(authorized_by):
            _error(errors, "PROOF_AUTHORITY_REQUIRED", "PROVEN requires proof authority")
        if not _is_non_empty_string(safe_crossing):
            _error(errors, "SAFE_CROSSING_REQUIRED", "PROVEN requires a safe crossing")
        if production_path is not True:
            _error(
                errors,
                "PRODUCTION_PATH_REQUIRED",
                "PROVEN requires the production observation and delivery path",
            )
        if bound_crossed is not True:
            _error(errors, "BOUND_CROSSING_REQUIRED", "PROVEN requires an observed crossing")
        if alert_received is not True:
            _error(errors, "ALERT_RECEIPT_REQUIRED", "PROVEN requires received alert")
        if not _is_non_empty_string(received_at):
            _error(
                errors,
                "RECEIPT_TIMESTAMP_REQUIRED",
                "PROVEN requires the alert receipt timestamp",
            )

    elif state == "SUSPECT":
        if not _is_non_empty_string(substrate) and not _is_non_empty_string(mechanism_ref):
            _error(
                errors,
                "EXTERNAL_MECHANISM_REQUIRED",
                "SUSPECT must identify the mechanism under suspicion",
            )
        named_failures = [
            item
            for item in (failure_modes or []) + (coverage_limits or [])
            if item.strip()
        ]
        if not named_failures:
            _error(
                errors,
                "SUSPECT_FAILURE_REQUIRED",
                "SUSPECT must name the observation, delivery, proof, or freshness failure",
            )

    return errors


def verify_path(path: Path) -> list[str]:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"UNREADABLE_OR_INVALID_JSON: {error}"]
    if not isinstance(record, dict):
        return ["RECORD_MUST_BE_OBJECT: root must be an object"]
    record.pop("_expected", None)
    return validate_record(record)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate watch-commission@1 records")
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args(argv)

    failed = False
    for path in args.paths:
        errors = verify_path(path)
        if errors:
            failed = True
            for error in errors:
                print(f"INVALID {path} {error}", file=sys.stderr)
        else:
            print(f"VALID {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
