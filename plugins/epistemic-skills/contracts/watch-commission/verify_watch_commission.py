#!/usr/bin/env python3
"""Validate watch-commission@1 records without third-party dependencies."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

STATES = {"DECLARED", "BLOCKED", "INERT", "PROVEN", "SUSPECT"}
DIRECTIONS = {"above", "below", "equals", "changes", "absent"}
SUBSTRATE_KINDS = {
    "scheduler",
    "event-listener",
    "monitoring-service",
    "human-cadence",
    "other-external",
    "fixture",
}
FAILURE_KINDS = {
    "probe",
    "delivery",
    "proof",
    "freshness",
    "kill-switch",
    "external-mechanism",
    "unknown",
}
BLOCK_REASONS = {
    "NO_EXECUTION_SUBSTRATE",
    "NO_REACHABLE_DESTINATION",
    "NO_AUTHORITY_TO_ENABLE",
    "NO_KILL_SWITCH",
    "KILL_SWITCH_UNPROVEN",
    "NO_SAFE_PROOF_CROSSING",
    "PROBE_UNAVAILABLE",
}
POST_CROSSING_HANDOFF = frozenset({"triage", "decision-ledger"})
FORBIDDEN_EVIDENCE_PREFIXES = (
    "self-asserted:",
    "memory:",
    "chat:",
    "session:",
    "prompt:",
)
PROMPT_TIME_MECHANISM_MARKERS = (
    "/skills/",
    "\\skills\\",
    "skill.md",
    "chat:",
    "session:",
    "prompt:",
    "memory:",
)

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
    "failure",
    "block_evidence",
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
    "destination": {"ref", "reachable", "reachability_receipt_ref"},
    "external_observer": {
        "substrate_kind",
        "substrate",
        "mechanism_ref",
        "persistence_receipt_ref",
        "persistent_outside_session",
        "enabled",
    },
    "kill_switch": {"procedure_ref", "exercised", "exercise_receipt_ref"},
    "proof": {
        "authorized_by",
        "authorization_ref",
        "safe_crossing",
        "production_path",
        "bound_crossed",
        "alert_received",
        "received_at",
        "alert_receipt_ref",
    },
    "failure": {"kind", "detail", "observed_at", "receipt_ref"},
    "block_evidence": {"detail", "observed_at", "receipt_ref"},
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
    for field in sorted(expected - value.keys()):
        _error(errors, "MISSING_FIELD", f"{key}.{field} is required")
    for field in sorted(value.keys() - expected):
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
    if len(value) != len(set(value)):
        _error(errors, "DUPLICATE_VALUE", f"{path}.{key} contains duplicates")
    return value


def _validate_evidence_ref(value: str | None, path: str, errors: list[str]) -> None:
    if not _is_non_empty_string(value):
        return
    lowered = value.strip().lower()
    if lowered.startswith(FORBIDDEN_EVIDENCE_PREFIXES):
        _error(
            errors,
            "INVALID_EVIDENCE_REF",
            f"{path} cannot use prompt/session memory or self-assertion as evidence",
        )


def _proof_absent(proof: dict[str, Any] | None) -> bool:
    if proof is None:
        return False
    return (
        not _is_non_empty_string(proof.get("authorized_by"))
        and not _is_non_empty_string(proof.get("authorization_ref"))
        and not _is_non_empty_string(proof.get("safe_crossing"))
        and proof.get("production_path") is False
        and proof.get("bound_crossed") is False
        and proof.get("alert_received") is False
        and not _is_non_empty_string(proof.get("received_at"))
        and not _is_non_empty_string(proof.get("alert_receipt_ref"))
    )


def _proof_complete(proof: dict[str, Any] | None) -> bool:
    if proof is None:
        return False
    return (
        _is_non_empty_string(proof.get("authorized_by"))
        and _is_non_empty_string(proof.get("authorization_ref"))
        and _is_non_empty_string(proof.get("safe_crossing"))
        and proof.get("production_path") is True
        and proof.get("bound_crossed") is True
        and proof.get("alert_received") is True
        and _is_non_empty_string(proof.get("received_at"))
        and _is_non_empty_string(proof.get("alert_receipt_ref"))
    )


def _failure_empty(failure: dict[str, Any] | None) -> bool:
    if failure is None:
        return False
    return (
        failure.get("kind") is None
        and not _is_non_empty_string(failure.get("detail"))
        and not _is_non_empty_string(failure.get("observed_at"))
        and not _is_non_empty_string(failure.get("receipt_ref"))
    )


def _failure_complete(failure: dict[str, Any] | None) -> bool:
    if failure is None:
        return False
    return (
        failure.get("kind") in FAILURE_KINDS
        and _is_non_empty_string(failure.get("detail"))
        and _is_non_empty_string(failure.get("observed_at"))
        and _is_non_empty_string(failure.get("receipt_ref"))
    )


def _block_evidence_empty(block_evidence: dict[str, Any] | None) -> bool:
    if block_evidence is None:
        return False
    return (
        not _is_non_empty_string(block_evidence.get("detail"))
        and not _is_non_empty_string(block_evidence.get("observed_at"))
        and not _is_non_empty_string(block_evidence.get("receipt_ref"))
    )


def _block_evidence_complete(block_evidence: dict[str, Any] | None) -> bool:
    if block_evidence is None:
        return False
    return (
        _is_non_empty_string(block_evidence.get("detail"))
        and _is_non_empty_string(block_evidence.get("observed_at"))
        and _is_non_empty_string(block_evidence.get("receipt_ref"))
    )


def _external_identity_complete(observer: dict[str, Any] | None) -> bool:
    if observer is None:
        return False
    return (
        observer.get("substrate_kind") in SUBSTRATE_KINDS
        and _is_non_empty_string(observer.get("substrate"))
        and _is_non_empty_string(observer.get("mechanism_ref"))
    )


def _kill_switch_complete(kill_switch: dict[str, Any] | None) -> bool:
    if kill_switch is None:
        return False
    return (
        _is_non_empty_string(kill_switch.get("procedure_ref"))
        and kill_switch.get("exercised") is True
        and _is_non_empty_string(kill_switch.get("exercise_receipt_ref"))
    )


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return named semantic violations; an empty list means valid."""
    errors: list[str] = []

    if not isinstance(record, dict):
        return ["RECORD_MUST_BE_OBJECT: root must be an object"]

    for field in sorted(TOP_LEVEL_FIELDS - record.keys()):
        _error(errors, "MISSING_FIELD", f"{field} is required")
    for field in sorted(record.keys() - TOP_LEVEL_FIELDS):
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
    failure = _require_object(record, "failure", errors)
    block_evidence = _require_object(record, "block_evidence", errors)
    handoff = _require_object(record, "handoff", errors)

    if subject is not None:
        if not _is_non_empty_string(subject.get("ref")):
            _error(errors, "MISSING_FIELD", "subject.ref must be a non-empty string")
        revision = subject.get("revision")
        if isinstance(revision, bool) or (
            revision is not None and not isinstance(revision, (str, int))
        ):
            _error(errors, "INVALID_TYPE", "subject.revision must be string, integer, or null")

    if bound is not None:
        for field in ("expression", "units"):
            if not _is_non_empty_string(bound.get(field)):
                _error(errors, "MISSING_FIELD", f"bound.{field} must be a non-empty string")
        direction = bound.get("direction")
        if direction not in DIRECTIONS:
            _error(errors, "INVALID_DIRECTION", f"bound.direction must be one of {sorted(DIRECTIONS)}")
        threshold = bound.get("threshold")
        if threshold is None or isinstance(threshold, (list, dict)):
            _error(errors, "INVALID_TYPE", "bound.threshold must be a scalar value")

    failure_modes = _require_string_list(probe, "failure_modes", "probe", errors)
    if probe is not None:
        for field in ("mechanism", "cadence_or_event"):
            if not _is_non_empty_string(probe.get(field)):
                _error(errors, "MISSING_FIELD", f"probe.{field} must be a non-empty string")

    destination_ref = _require_string_or_null(destination, "ref", "destination", errors)
    destination_reachable = _require_bool(destination, "reachable", "destination", errors)
    destination_receipt = _require_string_or_null(
        destination, "reachability_receipt_ref", "destination", errors
    )

    substrate_kind = _require_string_or_null(
        observer, "substrate_kind", "external_observer", errors
    )
    substrate = _require_string_or_null(observer, "substrate", "external_observer", errors)
    mechanism_ref = _require_string_or_null(
        observer, "mechanism_ref", "external_observer", errors
    )
    persistence_receipt = _require_string_or_null(
        observer, "persistence_receipt_ref", "external_observer", errors
    )
    persistent = _require_bool(
        observer, "persistent_outside_session", "external_observer", errors
    )
    enabled = _require_bool(observer, "enabled", "external_observer", errors)
    if substrate_kind is not None and substrate_kind not in SUBSTRATE_KINDS:
        _error(
            errors,
            "INVALID_SUBSTRATE_KIND",
            f"external_observer.substrate_kind must be one of {sorted(SUBSTRATE_KINDS)}",
        )
    if _is_non_empty_string(mechanism_ref):
        lowered_mechanism = mechanism_ref.strip().lower()
        if any(marker in lowered_mechanism for marker in PROMPT_TIME_MECHANISM_MARKERS):
            _error(
                errors,
                "PROMPT_TIME_MECHANISM_FORBIDDEN",
                "external_observer.mechanism_ref resolves to prompt/session instructions, not an external mechanism",
            )

    procedure_ref = _require_string_or_null(
        kill_switch, "procedure_ref", "kill_switch", errors
    )
    exercised = _require_bool(kill_switch, "exercised", "kill_switch", errors)
    exercise_receipt = _require_string_or_null(
        kill_switch, "exercise_receipt_ref", "kill_switch", errors
    )

    authorized_by = _require_string_or_null(proof, "authorized_by", "proof", errors)
    authorization_ref = _require_string_or_null(
        proof, "authorization_ref", "proof", errors
    )
    safe_crossing = _require_string_or_null(proof, "safe_crossing", "proof", errors)
    production_path = _require_bool(proof, "production_path", "proof", errors)
    bound_crossed = _require_bool(proof, "bound_crossed", "proof", errors)
    alert_received = _require_bool(proof, "alert_received", "proof", errors)
    received_at = _require_string_or_null(proof, "received_at", "proof", errors)
    alert_receipt = _require_string_or_null(
        proof, "alert_receipt_ref", "proof", errors
    )

    failure_kind = _require_string_or_null(failure, "kind", "failure", errors)
    failure_detail = _require_string_or_null(failure, "detail", "failure", errors)
    failure_observed_at = _require_string_or_null(
        failure, "observed_at", "failure", errors
    )
    failure_receipt = _require_string_or_null(failure, "receipt_ref", "failure", errors)
    if failure_kind is not None and failure_kind not in FAILURE_KINDS:
        _error(
            errors,
            "INVALID_FAILURE_KIND",
            f"failure.kind must be one of {sorted(FAILURE_KINDS)} or null",
        )

    block_detail = _require_string_or_null(
        block_evidence, "detail", "block_evidence", errors
    )
    block_observed_at = _require_string_or_null(
        block_evidence, "observed_at", "block_evidence", errors
    )
    block_receipt = _require_string_or_null(
        block_evidence, "receipt_ref", "block_evidence", errors
    )

    on_crossing = _require_string_list(handoff, "on_crossing", "handoff", errors)
    if on_crossing is not None and any(not item.strip() for item in on_crossing):
        _error(errors, "INVALID_VALUE", "handoff.on_crossing entries must be non-empty")
    if on_crossing is not None and set(on_crossing) != POST_CROSSING_HANDOFF:
        _error(
            errors,
            "INVALID_POST_CROSSING_HANDOFF",
            "handoff.on_crossing must classify exactly triage and decision-ledger; mission custody is separate",
        )

    coverage_limits = record.get("coverage_limits")
    if not isinstance(coverage_limits, list) or any(
        not isinstance(item, str) for item in coverage_limits
    ):
        _error(errors, "INVALID_TYPE", "coverage_limits must be an array of strings")
        coverage_limits = []

    reprove_after = record.get("reprove_after")
    if reprove_after is not None and not isinstance(reprove_after, str):
        _error(errors, "INVALID_TYPE", "reprove_after must be a string or null")

    for path, value in (
        ("destination.reachability_receipt_ref", destination_receipt),
        ("external_observer.persistence_receipt_ref", persistence_receipt),
        ("kill_switch.exercise_receipt_ref", exercise_receipt),
        ("proof.authorization_ref", authorization_ref),
        ("proof.alert_receipt_ref", alert_receipt),
        ("failure.receipt_ref", failure_receipt),
        ("block_evidence.receipt_ref", block_receipt),
    ):
        _validate_evidence_ref(value, path, errors)

    if substrate_kind == "fixture":
        scope_text = " ".join(coverage_limits).lower()
        if "fixture" not in scope_text or not any(
            marker in scope_text for marker in ("production", "test", "isolated")
        ):
            _error(
                errors,
                "FIXTURE_SCOPE_REQUIRED",
                "fixture observers must disclose test/isolated scope and production limits",
            )

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

    # A positive claim must carry the receipt that supports it. Receipts may
    # remain after the current claim becomes false; they are historical evidence.
    if destination_reachable is True and not _is_non_empty_string(destination_receipt):
        _error(
            errors,
            "DESTINATION_RECEIPT_REQUIRED",
            "destination.reachable=true requires reachability_receipt_ref",
        )
    if persistent is True and not _is_non_empty_string(persistence_receipt):
        _error(
            errors,
            "PERSISTENCE_RECEIPT_REQUIRED",
            "persistent_outside_session=true requires persistence_receipt_ref",
        )
    if exercised is True and not _is_non_empty_string(exercise_receipt):
        _error(
            errors,
            "KILL_SWITCH_RECEIPT_REQUIRED",
            "kill_switch.exercised=true requires exercise_receipt_ref",
        )
    if _is_non_empty_string(authorized_by) and not _is_non_empty_string(authorization_ref):
        _error(
            errors,
            "PROOF_AUTHORIZATION_RECEIPT_REQUIRED",
            "proof.authorized_by requires authorization_ref",
        )
    if alert_received is True and not _is_non_empty_string(alert_receipt):
        _error(
            errors,
            "ALERT_RECEIPT_REF_REQUIRED",
            "proof.alert_received=true requires alert_receipt_ref",
        )
    if alert_received is True and not _is_non_empty_string(received_at):
        _error(
            errors,
            "RECEIPT_TIMESTAMP_REQUIRED",
            "proof.alert_received=true requires received_at",
        )

    if failure_kind is None:
        if any(
            _is_non_empty_string(value)
            for value in (failure_detail, failure_observed_at, failure_receipt)
        ):
            _error(
                errors,
                "FAILURE_FIELDS_WITHOUT_KIND",
                "failure details require a failure.kind",
            )
    elif not _failure_complete(failure):
        _error(
            errors,
            "OBSERVED_FAILURE_RECEIPT_REQUIRED",
            "a named failure requires detail, observed_at, and receipt_ref",
        )

    if state == "DECLARED":
        if enabled is not False:
            _error(errors, "DECLARED_MUST_BE_DISABLED", "DECLARED observer must be disabled")
        if _is_non_empty_string(mechanism_ref) or persistent is True or _is_non_empty_string(
            persistence_receipt
        ):
            _error(
                errors,
                "DECLARED_MECHANISM_FORBIDDEN",
                "DECLARED cannot hide an externally prepared mechanism; use BLOCKED or INERT",
            )
        if not _proof_absent(proof):
            _error(errors, "PROOF_FORBIDDEN", "DECLARED cannot carry a proof attempt")
        if not _failure_empty(failure):
            _error(errors, "FAILURE_ONLY_VALID_FOR_SUSPECT", "DECLARED cannot carry a live failure")
        if not _block_evidence_empty(block_evidence):
            _error(
                errors,
                "BLOCK_EVIDENCE_FORBIDDEN",
                "block_evidence is only valid for BLOCKED",
            )

    elif state == "BLOCKED":
        if enabled is not False:
            _error(errors, "BLOCKED_MUST_BE_DISABLED", "BLOCKED observer cannot be enabled")
        if not _proof_absent(proof):
            _error(errors, "PROOF_FORBIDDEN", "BLOCKED cannot carry a proof attempt")
        if not _failure_empty(failure):
            _error(errors, "FAILURE_ONLY_VALID_FOR_SUSPECT", "BLOCKED cannot carry a live failure")
        if not _block_evidence_complete(block_evidence):
            _error(
                errors,
                "BLOCK_EVIDENCE_REQUIRED",
                "BLOCKED requires detail, observed_at, and an external evidence receipt",
            )

        mismatch = False
        if block_reason == "NO_EXECUTION_SUBSTRATE":
            mismatch = any(
                (
                    _is_non_empty_string(substrate_kind),
                    _is_non_empty_string(substrate),
                    _is_non_empty_string(mechanism_ref),
                    _is_non_empty_string(persistence_receipt),
                    persistent is True,
                )
            )
        elif block_reason == "NO_REACHABLE_DESTINATION":
            mismatch = destination_reachable is not False or not _is_non_empty_string(
                destination_receipt
            )
        elif block_reason == "NO_AUTHORITY_TO_ENABLE":
            mismatch = _is_non_empty_string(authorized_by) or _is_non_empty_string(
                authorization_ref
            )
        elif block_reason == "NO_KILL_SWITCH":
            mismatch = _is_non_empty_string(procedure_ref) or exercised is True
        elif block_reason == "KILL_SWITCH_UNPROVEN":
            mismatch = (
                not _external_identity_complete(observer)
                or persistent is not True
                or not _is_non_empty_string(persistence_receipt)
                or not _is_non_empty_string(procedure_ref)
                or exercised is True
                or _is_non_empty_string(exercise_receipt)
            )
        elif block_reason == "NO_SAFE_PROOF_CROSSING":
            mismatch = _is_non_empty_string(safe_crossing)
        if mismatch:
            _error(
                errors,
                "BLOCK_REASON_MISMATCH",
                f"recorded fields do not support block_reason={block_reason}",
            )

    elif state == "INERT":
        if not _block_evidence_empty(block_evidence):
            _error(
                errors,
                "BLOCK_EVIDENCE_FORBIDDEN",
                "block_evidence is only valid for BLOCKED",
            )
        if not _external_identity_complete(observer):
            _error(
                errors,
                "EXTERNAL_MECHANISM_REQUIRED",
                "INERT requires a valid external substrate and mechanism_ref",
            )
        if persistent is not True or not _is_non_empty_string(persistence_receipt):
            _error(
                errors,
                "EXTERNAL_PERSISTENCE_REQUIRED",
                "INERT requires a mechanism proven persistent outside the session",
            )
        if enabled is not False:
            _error(errors, "INERT_MUST_BE_DISABLED", "INERT observer must be disabled")
        if not _kill_switch_complete(kill_switch):
            _error(
                errors,
                "KILL_SWITCH_EXERCISE_REQUIRED",
                "INERT requires an exercised, receipted kill switch",
            )
        if not _failure_empty(failure):
            _error(errors, "FAILURE_ONLY_VALID_FOR_SUSPECT", "INERT cannot carry a live failure")
        if not _proof_absent(proof) and not _proof_complete(proof):
            _error(
                errors,
                "INCOMPLETE_PROOF_BUNDLE",
                "INERT proof history must be wholly absent or a complete historical proof",
            )
        if _proof_complete(proof) and not _is_non_empty_string(reprove_after):
            _error(
                errors,
                "REPROOF_BOUNDARY_REQUIRED",
                "historical successful proof requires reprove_after",
            )

    elif state == "PROVEN":
        if not _block_evidence_empty(block_evidence):
            _error(
                errors,
                "BLOCK_EVIDENCE_FORBIDDEN",
                "block_evidence is only valid for BLOCKED",
            )
        if not _external_identity_complete(observer):
            _error(
                errors,
                "EXTERNAL_MECHANISM_REQUIRED",
                "PROVEN requires a valid external substrate and mechanism_ref",
            )
        if persistent is not True:
            _error(
                errors,
                "EXTERNAL_PERSISTENCE_REQUIRED",
                "PROVEN requires a mechanism persistent outside the session",
            )
        if enabled is not True:
            _error(errors, "PROVEN_MUST_BE_ENABLED", "PROVEN observer must be enabled")
        if not _is_non_empty_string(destination_ref) or destination_reachable is not True:
            _error(
                errors,
                "DESTINATION_REACHABILITY_REQUIRED",
                "PROVEN requires a named reachable destination",
            )
        if not _kill_switch_complete(kill_switch):
            _error(
                errors,
                "KILL_SWITCH_EXERCISE_REQUIRED",
                "PROVEN requires an exercised, receipted kill switch",
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
            _error(errors, "ALERT_RECEIPT_REQUIRED", "PROVEN requires a received alert")
        if not _proof_complete(proof):
            _error(
                errors,
                "INCOMPLETE_PROOF_BUNDLE",
                "PROVEN requires a complete proof bundle and evidence refs",
            )
        if not _is_non_empty_string(reprove_after):
            _error(
                errors,
                "REPROOF_BOUNDARY_REQUIRED",
                "PROVEN requires a dated or condition-bound reprove_after value",
            )
        if not _failure_empty(failure):
            _error(errors, "FAILURE_ONLY_VALID_FOR_SUSPECT", "PROVEN cannot carry a live failure")

    elif state == "SUSPECT":
        if not _block_evidence_empty(block_evidence):
            _error(
                errors,
                "BLOCK_EVIDENCE_FORBIDDEN",
                "block_evidence is only valid for BLOCKED",
            )
        if not _external_identity_complete(observer):
            _error(
                errors,
                "EXTERNAL_MECHANISM_REQUIRED",
                "SUSPECT must identify the external mechanism under suspicion",
            )
        if not _failure_complete(failure):
            _error(
                errors,
                "SUSPECT_FAILURE_REQUIRED",
                "SUSPECT requires a receipted observed failure",
            )

    # Keep variables bound to their typed validations even where the state rules
    # use the helper predicates; this prevents silently accepting malformed
    # block-evidence fields merely because a state does not consume them.
    _ = (block_detail, block_observed_at)

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
