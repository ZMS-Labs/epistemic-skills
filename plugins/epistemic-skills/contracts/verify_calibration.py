#!/usr/bin/env python3
"""Validate the epistemic-product-calibration@1 envelope and invariants.

This verifier is intentionally stdlib-only. It validates identity, closed
vocabularies, revision/hash shapes, and population accounting. It does not
certify the referenced evidence or its behavioral/statistical conclusions.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys


PROTOCOL = "epistemic-product-calibration@1"
GIT_REVISION = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
RFC3339 = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)
STATUSES = {"observed", "candidate-gate", "accepted-gate", "superseded"}
REQUIRED_NEVER_ATTESTS = {
    "behavioral-merit-by-envelope",
    "statistical-validity-by-envelope",
    "release-readiness-by-envelope",
}
ALLOWED_NEVER_ATTESTS = REQUIRED_NEVER_ATTESTS | {"independence-by-declaration"}
TOP_LEVEL_FIELDS = {
    "protocol", "synthetic", "producer", "subject", "contract_revision",
    "corpus", "runner", "execution", "sampling_frame", "preregistration",
    "result", "status", "supersedes", "limitations", "never_attests",
}
REQUIRED_FIELDS = TOP_LEVEL_FIELDS - {"synthetic", "supersedes"}


class ValidationError(ValueError):
    """A named fail-closed contract violation."""


def fail(code: str, detail: str) -> None:
    raise ValidationError(f"{code}: {detail}")


def object_fields(value: object, path: str, required: set[str], allowed: set[str]) -> dict:
    if not isinstance(value, dict):
        fail("SCHEMA_VIOLATION", f"{path} must be an object")
    missing = required - value.keys()
    extra = value.keys() - allowed
    if missing:
        fail("SCHEMA_VIOLATION", f"{path} missing {sorted(missing)}")
    if extra:
        fail("SCHEMA_VIOLATION", f"{path} has unknown fields {sorted(extra)}")
    return value


def revision(value: object, path: str) -> None:
    if not isinstance(value, str) or not GIT_REVISION.fullmatch(value):
        fail("BAD_REVISION", f"{path} must be a full 40- or 64-hex revision")


def content_revision(value: object, path: str) -> None:
    row = object_fields(value, path, {"ref", "revision", "sha256"}, {"ref", "revision", "sha256"})
    if not isinstance(row["ref"], str) or not row["ref"]:
        fail("SCHEMA_VIOLATION", f"{path}.ref must be non-empty")
    revision(row["revision"], f"{path}.revision")
    if not isinstance(row["sha256"], str) or not SHA256.fullmatch(row["sha256"]):
        fail("BAD_HASH", f"{path}.sha256 must be 64 lowercase hex characters")


def date_time(value: object, path: str) -> datetime:
    # fromisoformat alone accepts ISO forms RFC 3339 forbids (space separator,
    # basic-format offsets, week dates), so the grammar gates before parsing.
    if not isinstance(value, str) or not RFC3339.fullmatch(value):
        fail("SCHEMA_VIOLATION", f"{path} must be an RFC 3339 date-time")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00").replace("z", "+00:00"))
    except ValueError:
        fail("SCHEMA_VIOLATION", f"{path} must be an RFC 3339 date-time")
    if parsed.tzinfo is None:
        fail("SCHEMA_VIOLATION", f"{path} must include a timezone")
    return parsed


def validate(value: object) -> None:
    record = object_fields(value, "$", REQUIRED_FIELDS, TOP_LEVEL_FIELDS)
    if record["protocol"] != PROTOCOL:
        fail("UNKNOWN_PROTOCOL", f"expected {PROTOCOL}")
    if "synthetic" in record and not isinstance(record["synthetic"], bool):
        fail("SCHEMA_VIOLATION", "$.synthetic must be boolean")

    producer = object_fields(record["producer"], "$.producer", {"repo", "revision"}, {"repo", "revision"})
    if producer["repo"] != "ZMS-Labs/epistemic-calibration":
        fail("WRONG_PRODUCER", "producer.repo must be ZMS-Labs/epistemic-calibration")
    revision(producer["revision"], "$.producer.revision")

    subject = object_fields(
        record["subject"], "$.subject",
        {"repo", "revision", "version", "skill_or_surface"},
        {"repo", "revision", "version", "skill_or_surface"},
    )
    if subject["repo"] != "ZMS-Labs/epistemic-skills":
        fail("WRONG_SUBJECT", "subject.repo must be ZMS-Labs/epistemic-skills")
    revision(subject["revision"], "$.subject.revision")
    if not isinstance(subject["version"], str) or not SEMVER.fullmatch(subject["version"]):
        fail("SCHEMA_VIOLATION", "$.subject.version must be semver")
    if not isinstance(subject["skill_or_surface"], str) or not SLUG.fullmatch(subject["skill_or_surface"]):
        fail("SCHEMA_VIOLATION", "$.subject.skill_or_surface must be a slug")
    if not isinstance(record["contract_revision"], str) or not record["contract_revision"]:
        fail("SCHEMA_VIOLATION", "$.contract_revision must be non-empty")

    for key in ("corpus", "runner", "preregistration", "result"):
        content_revision(record[key], f"$.{key}")

    execution = object_fields(
        record["execution"], "$.execution",
        {"models", "harnesses", "started_at", "completed_at"},
        {"models", "harnesses", "started_at", "completed_at"},
    )
    for key in ("models", "harnesses"):
        items = execution[key]
        # element types gate before set() so non-hashable elements fail closed
        # as SCHEMA_VIOLATION instead of an uncaught TypeError
        if not isinstance(items, list) or not items or not all(isinstance(item, str) and item for item in items) or len(items) != len(set(items)):
            fail("SCHEMA_VIOLATION", f"$.execution.{key} must contain unique non-empty strings")
    started = date_time(execution["started_at"], "$.execution.started_at")
    completed = date_time(execution["completed_at"], "$.execution.completed_at")
    if completed < started:
        fail("INVALID_TIME_WINDOW", "completed_at precedes started_at")

    frame = object_fields(
        record["sampling_frame"], "$.sampling_frame",
        {"population", "planned", "observed", "excluded", "missing"},
        {"population", "planned", "observed", "excluded", "missing"},
    )
    if not isinstance(frame["population"], str) or not frame["population"]:
        fail("SCHEMA_VIOLATION", "$.sampling_frame.population must be non-empty")
    for key in ("planned", "observed", "excluded", "missing"):
        minimum = 1 if key == "planned" else 0
        if isinstance(frame[key], bool) or not isinstance(frame[key], int) or frame[key] < minimum:
            fail("SCHEMA_VIOLATION", f"$.sampling_frame.{key} must be an integer >= {minimum}")
    if frame["observed"] + frame["excluded"] + frame["missing"] != frame["planned"]:
        fail("POPULATION_MISMATCH", "observed + excluded + missing must equal planned")

    # isinstance FIRST: `STATUSES` is a set of strings, so an unhashable
    # status ({} or []) is not a member -- but `in` RAISES on it instead of
    # answering, and this verifier's contract is a named failure, never a
    # traceback.
    if not isinstance(record["status"], str) or record["status"] not in STATUSES:
        fail("UNKNOWN_STATUS", f"status must be one of {sorted(STATUSES)}")
    supersedes = record.get("supersedes")
    if supersedes is not None and (not isinstance(supersedes, str) or not SHA256.fullmatch(supersedes)):
        fail("BAD_HASH", "$.supersedes must be null or a sha256")
    if record["status"] == "superseded" and supersedes is None:
        fail("MISSING_SUPERSESSION", "superseded status requires supersedes")

    limitations = record["limitations"]
    if not isinstance(limitations, list) or not limitations or not all(isinstance(item, str) and item for item in limitations):
        fail("MISSING_LIMITATIONS", "limitations must contain non-empty strings")
    never = record["never_attests"]
    if (
        not isinstance(never, list)
        or not all(isinstance(item, str) for item in never)
        or len(never) != len(set(never))
        or not REQUIRED_NEVER_ATTESTS <= set(never)
        or not set(never) <= ALLOWED_NEVER_ATTESTS
    ):
        fail("MISSING_NEVER_ATTESTS", f"never_attests must include {sorted(REQUIRED_NEVER_ATTESTS)}")


def load(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail("INVALID_JSON", str(exc))


def self_test() -> None:
    root = Path(__file__).parent / "examples" / "calibration"
    cases = {
        "valid-observed.json": None,
        "invalid-population.json": "POPULATION_MISMATCH",
        "invalid-missing-never-attests.json": "MISSING_NEVER_ATTESTS",
        "invalid-floating-revision.json": "BAD_REVISION",
        "invalid-nonrfc3339-timestamp.json": "SCHEMA_VIOLATION",
        # A CLOSED vocabulary tested with `in` raises TypeError on an
        # unhashable value, so an inbound envelope carrying `"status": []`
        # produced a traceback instead of the promised named failure --
        # the same shape es#137 P2 fixed once, in one place, for one field.
        "invalid-unhashable-status.json": "UNKNOWN_STATUS",
    }
    for name, expected in cases.items():
        try:
            validate(load(root / name))
        except ValidationError as exc:
            actual = str(exc).split(":", 1)[0]
            if expected != actual:
                raise AssertionError(f"{name}: expected {expected}, got {actual}: {exc}") from exc
        else:
            if expected is not None:
                raise AssertionError(f"{name}: expected {expected}, got pass")
    # SCHEMA/VERIFIER PARITY. A producer is told to validate against the
    # published JSON Schema; a consumer runs this verifier. Where the two
    # disagree the producer gets a false PASS and the consumer refuses the
    # same bytes. This asserts the schema DECLARES the status-dependent
    # supersession requirement this verifier enforces.
    #
    # HONEST SCOPE OF THIS ORACLE: it reads the schema document, so it
    # establishes that the constraint is DECLARED -- not that any JSON Schema
    # implementation enforces it. There is no stdlib JSON Schema validator, so
    # enforcement cannot be exercised here; a structural pin is what this
    # repository can actually check, and saying so is the point.
    schema = json.loads(
        (Path(__file__).parent / "epistemic-product-calibration.schema.json")
        .read_text(encoding="utf-8"))
    conditionals = [
        rule for rule in schema.get("allOf", [])
        if rule.get("if", {}).get("properties", {}).get("status", {}).get("const")
        == "superseded"
        and "supersedes" in rule.get("then", {}).get("required", [])
    ]
    if not conditionals:
        raise AssertionError(
            "schema/verifier parity: this verifier raises MISSING_SUPERSESSION "
            "for status=superseded without `supersedes`, but the published "
            "schema declares no such conditional -- a producer validating "
            "against the schema would get a false PASS")
    print(f"calibration contract self-test: PASS ({len(cases)}/{len(cases)} "
          "cases + schema/verifier supersession parity)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
        elif args.record:
            validate(load(args.record))
            print(f"ok {args.record}: envelope valid")
        else:
            parser.error("provide RECORD or --self-test")
    except ValidationError as exc:
        print(f"error {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
