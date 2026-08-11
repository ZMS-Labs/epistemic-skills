#!/usr/bin/env python3
"""Validate mission-custody@1 records without third-party dependencies.

Record kinds: mission-manifest@1, checkpoint@1, receipt@1, acceptance-verdict@1.
validate_record() dispatches on the required "record" field and returns a list
of "FIELD: reason" strings; empty list means valid.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

STATES = {"draft", "active", "reopened", "verifying", "completed", "cancelled"}
TIERS = {"operator-accepted", "declared-role-separation"}
VERDICTS = {"PASS", "FAIL", "INCONCLUSIVE"}
RECORD_KINDS = {
    "mission-manifest@1",
    "checkpoint@1",
    "receipt@1",
    "acceptance-verdict@1",
}

_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

MANIFEST_FIELDS = {
    "record", "mission_id", "created_utc", "authority", "scope",
    "acceptance", "stop_rules", "steward_ref",
}
AUTHORITY_FIELDS = {
    "operator_ref", "instruction", "amendments", "permissions",
    "protected_state", "acceptable_costs",
}
CHECKPOINT_FIELDS = {
    "record", "mission_id", "revision", "status", "prev_checkpoint_sha256",
    "manifest", "state", "receipt_ids", "written_utc", "written_by",
}
RECEIPT_FIELDS = {
    "record", "mission_id", "request_id", "actor", "utc",
    "artifact_path", "before_sha256", "after_sha256",
}
VERDICT_FIELDS = {
    "record", "mission_id", "revision", "verdict", "acceptor_id", "worker_id",
    "operator_ref", "assurance_tier", "receipt_refs", "reason", "utc",
}


def is_iso_utc(value: Any) -> bool:
    return isinstance(value, str) and bool(_ISO_RE.match(value))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA_RE.match(value))


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and item for item in value)


def _require(errors: list[str], cond: bool, field: str, reason: str) -> None:
    if not cond:
        errors.append(f"{field}: {reason}")


def _check_exact_fields(errors: list[str], rec: dict, allowed: set[str],
                        where: str) -> None:
    for key in rec:
        if key not in allowed:
            errors.append(f"{where}.{key}: unknown field")
    for key in allowed:
        if key not in rec:
            errors.append(f"{where}.{key}: missing")


def validate_manifest(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, MANIFEST_FIELDS, "manifest")
    if errors:
        return errors
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    _require(errors, is_iso_utc(rec["created_utc"]),
             "created_utc", "ISO-8601 Z timestamp required")
    _require(errors, isinstance(rec["steward_ref"], str) and rec["steward_ref"],
             "steward_ref", "non-empty string required")

    auth = rec["authority"]
    if not isinstance(auth, dict):
        errors.append("authority: object required")
        return errors
    _check_exact_fields(errors, auth, AUTHORITY_FIELDS, "authority")
    if not errors:
        _require(errors, isinstance(auth["operator_ref"], str)
                 and auth["operator_ref"],
                 "authority.operator_ref", "non-empty string required")
        _require(errors, isinstance(auth["instruction"], str)
                 and auth["instruction"],
                 "authority.instruction", "non-empty verbatim string required")
        amendments = auth["amendments"]
        ok = isinstance(amendments, list) and all(
            isinstance(a, dict) and set(a) == {"utc", "text"}
            and is_iso_utc(a["utc"]) and isinstance(a["text"], str) and a["text"]
            for a in amendments)
        _require(errors, ok, "authority.amendments",
                 "append-only list of {utc, text} objects required")
        for name in ("permissions", "protected_state", "acceptable_costs"):
            _require(errors, _str_list(auth[name]),
                     f"authority.{name}", "list of strings required")

    scope = rec["scope"]
    ok = isinstance(scope, dict) and set(scope) == {"in", "out"} \
        and _str_list(scope.get("in")) and _str_list(scope.get("out"))
    _require(errors, ok, "scope", '{"in": [...], "out": [...]} required')

    acc = rec["acceptance"]
    ok = isinstance(acc, dict) and set(acc) == {"required_tier", "acceptor_ref"} \
        and acc.get("required_tier") in TIERS \
        and (acc.get("acceptor_ref") is None
             or (isinstance(acc.get("acceptor_ref"), str) and acc["acceptor_ref"]))
    _require(errors, ok, "acceptance",
             "required_tier in TIERS and acceptor_ref string-or-null required")

    stop = rec["stop_rules"]
    ok = isinstance(stop, dict) \
        and set(stop) == {"hold_if", "stop_if", "escalate_if"} \
        and all(_str_list(stop[k]) for k in ("hold_if", "stop_if", "escalate_if"))
    _require(errors, ok, "stop_rules",
             "hold_if/stop_if/escalate_if string lists required")
    return errors


def validate_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record: JSON object required"]
    kind = record.get("record")
    if kind not in RECORD_KINDS:
        return [f"record: unknown kind {kind!r}"]
    if kind == "mission-manifest@1":
        return validate_manifest(record)
    if kind == "checkpoint@1":
        return validate_checkpoint(record)      # Task 2
    if kind == "receipt@1":
        return validate_receipt(record)         # Task 3
    return validate_acceptance_verdict(record)  # Task 3


def validate_checkpoint(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, CHECKPOINT_FIELDS, "checkpoint")
    if errors:
        return errors
    _require(errors, isinstance(rec["revision"], int) and rec["revision"] >= 1,
             "revision", "integer >= 1 required")
    _require(errors, rec["status"] in STATES, "status",
             f"one of {sorted(STATES)} required")
    prev = rec["prev_checkpoint_sha256"]
    if rec.get("revision") == 1:
        _require(errors, prev is None, "prev_checkpoint_sha256",
                 "null required at revision 1")
    else:
        _require(errors, is_sha256(prev), "prev_checkpoint_sha256",
                 "64-hex sha256 of prior checkpoint file required")
    if isinstance(rec["manifest"], dict) \
            and rec["manifest"].get("record") == "mission-manifest@1":
        for err in validate_manifest(rec["manifest"]):
            errors.append(f"manifest.{err}")
        if rec["manifest"].get("mission_id") != rec["mission_id"]:
            errors.append("manifest.mission_id: must equal checkpoint mission_id")
    else:
        errors.append("manifest: embedded mission-manifest@1 required")
    state = rec["state"]
    ok = isinstance(state, dict) \
        and set(state) == {"frontier", "notes", "unresolved_verdicts"} \
        and isinstance(state.get("frontier"), str) and state["frontier"] \
        and _str_list(state.get("notes")) \
        and _str_list(state.get("unresolved_verdicts"))
    _require(errors, ok, "state",
             "frontier (non-empty str), notes[], unresolved_verdicts[] required")
    _require(errors, _str_list(rec["receipt_ids"]), "receipt_ids",
             "list of receipt id strings required")
    _require(errors, is_iso_utc(rec["written_utc"]), "written_utc",
             "ISO-8601 Z timestamp required")
    _require(errors, isinstance(rec["written_by"], str) and rec["written_by"],
             "written_by", "non-empty actor id required")
    return errors


def validate_receipt(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, RECEIPT_FIELDS, "receipt")
    if errors:
        return errors
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    for name in ("request_id", "actor", "artifact_path"):
        _require(errors, isinstance(rec[name], str) and rec[name],
                 name, "non-empty string required")
    _require(errors, is_iso_utc(rec["utc"]), "utc", "ISO-8601 Z required")
    _require(errors, rec["before_sha256"] is None or is_sha256(rec["before_sha256"]),
             "before_sha256", "null (new artifact) or 64-hex sha256 required")
    _require(errors, is_sha256(rec["after_sha256"]),
             "after_sha256", "64-hex sha256 required")
    return errors


def validate_acceptance_verdict(rec: dict) -> list[str]:
    errors: list[str] = []
    _check_exact_fields(errors, rec, VERDICT_FIELDS, "verdict")
    if errors:
        return errors
    _require(errors, isinstance(rec["revision"], int) and rec["revision"] >= 1,
             "revision", "integer >= 1 required")
    _require(errors, rec["verdict"] in VERDICTS, "verdict",
             f"one of {sorted(VERDICTS)} required")
    _require(errors, rec["assurance_tier"] in TIERS, "assurance_tier",
             f"one of {sorted(TIERS)} required")
    _require(errors, isinstance(rec["mission_id"], str)
             and bool(_ID_RE.match(rec["mission_id"])),
             "mission_id", "kebab-case identifier required")
    for name in ("acceptor_id", "worker_id", "operator_ref", "reason"):
        _require(errors, isinstance(rec[name], str) and rec[name],
                 name, "non-empty string required")
    _require(errors, _str_list(rec["receipt_refs"]), "receipt_refs",
             "list of receipt id strings required")
    _require(errors, is_iso_utc(rec["utc"]), "utc", "ISO-8601 Z required")
    if not errors:
        _require(errors, rec["acceptor_id"] != rec["worker_id"],
                 "acceptor_id", "self-certification refused (== worker_id)")
        if rec["assurance_tier"] == "operator-accepted":
            _require(errors, rec["acceptor_id"] == rec["operator_ref"],
                     "acceptor_id",
                     "operator-accepted tier requires acceptor_id == operator_ref")
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: verify_mission_custody.py <file.json>...", file=sys.stderr)
        return 2
    failed = False
    for arg in argv:
        rec = json.loads(Path(arg).read_text(encoding="utf-8"))
        errors = validate_record(rec)
        if errors:
            failed = True
            for err in errors:
                print(f"{arg}: {err}")
        else:
            print(f"{arg}: valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
