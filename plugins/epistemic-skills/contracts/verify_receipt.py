#!/usr/bin/env python3
"""
verify_receipt.py — handoff-receipt@1 envelope verifier.

Validates a handoff receipt against the closed handoff-receipt@1 contract
(see handoff-receipt.schema.json and README.md in this directory). The
verifier certifies the ENVELOPE ONLY — identity, well-formedness, provenance
binding (sha256), and the validity-window vocabulary. It never evaluates
whether the judgment inside any artifact is right, and no check here raises
a consumer's confidence in a judgment it did not make or re-verify.

Stdlib-only; no third-party dependencies (the schema checks are implemented
directly so a plain python3 suffices, matching the select_lenses.py /
verify_evidence.py pattern).

Fails closed: any miss exits nonzero with a named reason:
    SCHEMA_VIOLATION        structural/type/closed-enum failure
    BAD_PRODUCER_SHA256     producer.sha256 is not 64 lowercase hex chars
    MISSING_NEVER_ATTESTS   never_attests absent or empty
    UNKNOWN_PREDICATE       valid_while entry outside the closed vocabulary
    NULL_REVISION_PREDICATE subject.revision null + subject-revision-unchanged
    ARTIFACT_MISSING        artifacts[].path does not resolve under the root
    ARTIFACT_HASH_MISMATCH  artifacts[].sha256 does not match the file content

Fixture annotation convention: top-level keys starting with "_" (e.g.
"_expected_failure" in examples/invalid/) are ignored by validation.

Usage:
    python verify_receipt.py RECEIPT.json [--artifact-root DIR]
    python verify_receipt.py --self-test

Exit codes:
    0  receipt valid (or self-test passed)
    1  fail-closed rejection (named reason on stderr)
    2  invalid invocation or unreadable input
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

RECEIPT_KIND = "handoff-receipt@1"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RUN_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*-[0-9]{8}-[0-9]+$")
DAY_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
SUBJECT_REF_RE = re.compile(r"^([0-9a-f]{64}|[a-z][a-z0-9-]{1,63})$")

# Closed vocabularies — extended ONLY by schema-version bump + verifier update
# in the same PR (see README.md, "Extending the vocabularies").
TRIGGER_CLASSES = frozenset({
    "explicit-request",
    "unfamiliar-territory",
    "design-decision",
    "literature-claim",
    "goal-authoring",
    "high-stakes-irreversible",
    "ui-facing-completion",
    "workflow-stage-pairing",
    "multi-skill-routing",
})
SKIP_GATE_VALUES = frozenset({"passed", "fired", "n/a"})
ARTIFACT_KINDS = frozenset({
    "rewritten-request",
    "derived-verdict",
    "claim-evidence-matrix",
    "goal-contract",
    "dossier",
    "gauntlet-run-record",
    "uat-packet",
    "routing-record",
})
VALID_WHILE_PREDICATES = frozenset({
    "subject-revision-unchanged",
    "session-continuous",
    "freeze-window-open",
    "environment-reachable",
})

TOP_LEVEL_KEYS = frozenset({
    "receipt", "synthetic", "producer", "run", "trigger", "subject",
    "artifacts", "valid_while", "coverage_limits", "never_attests",
})


class ReceiptError(Exception):
    """Fail-closed rejection. `name` is the stable named reason."""

    def __init__(self, name: str, detail: str):
        super().__init__(f"{name}: {detail}")
        self.name = name
        self.detail = detail


def _schema_fail(detail: str) -> ReceiptError:
    return ReceiptError("SCHEMA_VIOLATION", detail)


def _require_object(value, where: str) -> dict:
    if not isinstance(value, dict):
        raise _schema_fail(f"{where} must be an object")
    return value


def _require_keys(obj: dict, keys, where: str) -> None:
    for key in keys:
        if key not in obj:
            raise _schema_fail(f"{where}.{key} is required")


def _check_extra_keys(obj: dict, allowed, where: str) -> None:
    extra = sorted(k for k in obj if k not in allowed)
    if extra:
        raise _schema_fail(f"{where} has undeclared field(s): {', '.join(extra)}")


def _require_string(value, where: str) -> str:
    if not isinstance(value, str) or not value:
        raise _schema_fail(f"{where} must be a non-empty string")
    return value


def _check_schema_envelope(r: dict) -> None:
    """Structural conformance: required fields, types, closed enums.

    Three checks are deliberately reported under their own named reasons
    elsewhere: producer.sha256 format (BAD_PRODUCER_SHA256), never_attests
    presence/emptiness (MISSING_NEVER_ATTESTS), and the valid_while
    vocabulary (UNKNOWN_PREDICATE).
    """
    if r.get("receipt") != RECEIPT_KIND:
        raise _schema_fail(f'receipt must be "{RECEIPT_KIND}"')
    _check_extra_keys(
        {k: v for k, v in r.items() if not k.startswith("_")},
        TOP_LEVEL_KEYS, "receipt",
    )
    _require_keys(r, ("producer", "run", "trigger", "subject", "artifacts",
                      "valid_while", "coverage_limits"), "receipt")
    if "synthetic" in r and not isinstance(r["synthetic"], bool):
        raise _schema_fail("receipt.synthetic must be a boolean")

    producer = _require_object(r["producer"], "producer")
    _check_extra_keys(producer, {"skill", "version", "sha256"}, "producer")
    _require_keys(producer, ("skill", "version", "sha256"), "producer")
    _require_string(producer["skill"], "producer.skill")
    _require_string(producer["version"], "producer.version")
    if not isinstance(producer["sha256"], str):
        raise _schema_fail("producer.sha256 must be a string")

    run = _require_object(r["run"], "run")
    _check_extra_keys(run, {"id", "at", "session"}, "run")
    _require_keys(run, ("id", "at", "session"), "run")
    if not isinstance(run["id"], str) or not RUN_ID_RE.match(run["id"]):
        raise _schema_fail(
            "run.id must match <subject-class-or-hash>-<YYYYMMDD>-<seq>")
    if not isinstance(run["at"], str) or not DAY_RE.match(run["at"]):
        raise _schema_fail("run.at must be day-granularity YYYY-MM-DD")
    if run["session"] is not None and not (
        isinstance(run["session"], str) and SHA256_RE.match(run["session"])
    ):
        raise _schema_fail("run.session must be a keyed hash (64 hex) or null")

    trigger = _require_object(r["trigger"], "trigger")
    _check_extra_keys(trigger, {"matched", "skip_gate"}, "trigger")
    _require_keys(trigger, ("matched", "skip_gate"), "trigger")
    if trigger["matched"] not in TRIGGER_CLASSES:
        raise _schema_fail(
            f'trigger.matched "{trigger["matched"]}" is not a closed '
            "trigger-class")
    if trigger["skip_gate"] not in SKIP_GATE_VALUES:
        raise _schema_fail(
            f'trigger.skip_gate "{trigger["skip_gate"]}" is not in '
            "passed|fired|n/a")

    subject = _require_object(r["subject"], "subject")
    _check_extra_keys(subject, {"ref", "revision", "sha256"}, "subject")
    _require_keys(subject, ("ref", "revision", "sha256"), "subject")
    if not isinstance(subject["ref"], str) or not SUBJECT_REF_RE.match(subject["ref"]):
        raise _schema_fail("subject.ref must be a hash or closed subject-class")
    if subject["revision"] is not None and not isinstance(subject["revision"], str):
        raise _schema_fail("subject.revision must be a string or null")
    if subject["sha256"] is not None and not (
        isinstance(subject["sha256"], str) and SHA256_RE.match(subject["sha256"])
    ):
        raise _schema_fail("subject.sha256 must be 64 hex chars or null")

    artifacts = r["artifacts"]
    if not isinstance(artifacts, list):
        raise _schema_fail("artifacts must be an array")
    for i, art in enumerate(artifacts):
        where = f"artifacts[{i}]"
        art = _require_object(art, where)
        _check_extra_keys(art, {"kind", "path", "sha256"}, where)
        _require_keys(art, ("kind", "path", "sha256"), where)
        if art["kind"] not in ARTIFACT_KINDS:
            raise _schema_fail(f'{where}.kind "{art["kind"]}" is not a closed kind')
        _require_string(art["path"], f"{where}.path")
        if not isinstance(art["sha256"], str) or not SHA256_RE.match(art["sha256"]):
            raise _schema_fail(f"{where}.sha256 must be 64 lowercase hex chars")

    valid_while = r["valid_while"]
    if not isinstance(valid_while, list) or not all(
        isinstance(p, str) for p in valid_while
    ):
        raise _schema_fail("valid_while must be an array of strings")

    coverage = r["coverage_limits"]
    if not isinstance(coverage, list) or not all(
        isinstance(c, str) for c in coverage
    ):
        raise _schema_fail("coverage_limits must be an array of strings")

    if "never_attests" in r:
        na = r["never_attests"]
        if isinstance(na, list) and not all(isinstance(x, str) for x in na):
            raise _schema_fail("never_attests must be an array of strings")


def _check_producer_pin(r: dict) -> None:
    sha = r["producer"]["sha256"]
    if not SHA256_RE.match(sha):
        raise ReceiptError(
            "BAD_PRODUCER_SHA256",
            "producer.sha256 must be 64 lowercase hex chars "
            "(content pin of the producer SKILL.md)")


def _check_never_attests(r: dict) -> None:
    na = r.get("never_attests")
    if not isinstance(na, list) or len(na) == 0:
        raise ReceiptError(
            "MISSING_NEVER_ATTESTS",
            "never_attests is required and must be non-empty")


def _check_predicates(r: dict) -> None:
    for pred in r["valid_while"]:
        if pred not in VALID_WHILE_PREDICATES:
            raise ReceiptError(
                "UNKNOWN_PREDICATE",
                f'"{pred}" is not in the closed valid_while vocabulary; '
                "predicates are added only by schema-version bump + verifier "
                "update in the same PR")


def _check_null_subject_rule(r: dict) -> None:
    if (r["subject"]["revision"] is None
            and "subject-revision-unchanged" in r["valid_while"]):
        raise ReceiptError(
            "NULL_REVISION_PREDICATE",
            "subject.revision is null; null subjects fail closed and MUST NOT "
            "carry subject-revision-unchanged")


def _check_artifacts(r: dict, artifact_root: Path) -> None:
    for art in r["artifacts"]:
        path = artifact_root / art["path"]
        if not path.is_file():
            raise ReceiptError(
                "ARTIFACT_MISSING",
                f'{art["path"]} does not resolve under artifact root '
                f"{artifact_root}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != art["sha256"]:
            raise ReceiptError(
                "ARTIFACT_HASH_MISMATCH",
                f'{art["path"]}: recorded {art["sha256"]} != actual {digest}')


def verify_receipt(receipt: dict, artifact_root: Path) -> None:
    """Run every fail-closed check. Raises ReceiptError on any miss."""
    _check_schema_envelope(receipt)
    _check_producer_pin(receipt)
    _check_never_attests(receipt)
    _check_predicates(receipt)
    _check_null_subject_rule(receipt)
    _check_artifacts(receipt, artifact_root)


def _load_receipt(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"error: cannot read {path}: {exc}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict):
        print(f"error: {path} must contain a JSON object", file=sys.stderr)
        sys.exit(2)
    return data


# Self-test fixtures: (receipt path relative to examples/, expected named
# reason or None for pass). Every fail-closed path is exercised.
EXAMPLES_DIR = Path(__file__).resolve().parent / "examples"
SELF_TEST_CASES = [
    ("valid/gauntlet-run-record.receipt.json", None),
    ("valid/uat-packet.receipt.json", None),
    ("valid/evidence-matrix.receipt.json", None),
    ("invalid/schema-violation.receipt.json", "SCHEMA_VIOLATION"),
    ("invalid/unresolvable-hash.receipt.json", "ARTIFACT_MISSING"),
    ("invalid/unknown-predicate.receipt.json", "UNKNOWN_PREDICATE"),
    ("invalid/null-revision-predicate.receipt.json", "NULL_REVISION_PREDICATE"),
    ("invalid/missing-never-attests.receipt.json", "MISSING_NEVER_ATTESTS"),
]


def run_self_test() -> int:
    artifact_root = EXAMPLES_DIR
    failures = 0
    for rel, expected in SELF_TEST_CASES:
        path = EXAMPLES_DIR / rel
        receipt = _load_receipt(path)
        try:
            verify_receipt(receipt, artifact_root)
            got = None
        except ReceiptError as exc:
            got = exc.name
        if got == expected:
            outcome = "pass" if expected is None else f"rejected as expected ({got})"
            print(f"ok   {rel}: {outcome}")
        else:
            failures += 1
            print(f"FAIL {rel}: expected {expected or 'pass'}, got {got or 'pass'}",
                  file=sys.stderr)
    if failures:
        print(f"self-test: {failures} case(s) failed", file=sys.stderr)
        return 1
    print(f"self-test: all {len(SELF_TEST_CASES)} cases behaved as expected")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="handoff-receipt@1 envelope verifier (fails closed).")
    parser.add_argument("receipt", nargs="?", help="receipt JSON file")
    parser.add_argument("--artifact-root", default=None,
                        help="root that artifacts[].path resolves against "
                             "(default: the receipt file's directory)")
    parser.add_argument("--self-test", action="store_true",
                        help="run the bundled example fixtures and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.receipt:
        parser.error("a receipt file is required unless --self-test is given")

    receipt_path = Path(args.receipt)
    artifact_root = Path(args.artifact_root) if args.artifact_root else receipt_path.parent
    receipt = _load_receipt(receipt_path)
    try:
        verify_receipt(receipt, artifact_root)
    except ReceiptError as exc:
        print(f"FAIL {exc.name}: {exc.detail}", file=sys.stderr)
        return 1
    r = receipt
    print(f"OK handoff-receipt@1 producer={r['producer']['skill']}@{r['producer']['version']} "
          f"run={r['run']['id']} artifacts={len(r['artifacts'])} "
          f"valid_while={len(r['valid_while'])} predicate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
