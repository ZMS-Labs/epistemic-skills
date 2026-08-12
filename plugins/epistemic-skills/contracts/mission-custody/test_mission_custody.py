#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verify_mission_custody import (  # noqa: E402
    RECORD_KINDS,
    STATES,
    TIERS,
    VERDICTS,
    validate_record,
)

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    if not cond:
        FAILURES.append(name)
        print(f"FAIL {name}")
    else:
        print(f"ok   {name}")


def load(name: str) -> dict:
    return json.loads((ROOT / "examples" / name).read_text(encoding="utf-8"))


def valid_manifest() -> dict:
    return load("valid-manifest-minimal.json")


def test_constants() -> None:
    check("states-closed-list", STATES == {
        "draft", "active", "reopened", "verifying", "completed", "cancelled"})
    check("tiers", TIERS == {"operator-accepted", "declared-role-separation"})
    check("verdicts", VERDICTS == {"PASS", "FAIL", "INCONCLUSIVE"})
    check("record-kinds", RECORD_KINDS == {
        "mission-manifest@1", "checkpoint@1", "checkpoint@2", "receipt@1",
        "acceptance-verdict@1"})


def test_manifest_valid_example() -> None:
    check("manifest-valid-example", validate_record(valid_manifest()) == [])


def test_manifest_missing_instruction() -> None:
    rec = copy.deepcopy(valid_manifest())
    del rec["authority"]["instruction"]
    check("manifest-missing-instruction", validate_record(rec) != [])


def test_manifest_unknown_top_level_field() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["surprise"] = 1
    check("manifest-unknown-field", validate_record(rec) != [])


def test_manifest_bad_tier() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["acceptance"]["required_tier"] = "externally-proven"
    check("manifest-no-externally-proven-tier", validate_record(rec) != [])


def test_manifest_amendments_must_be_list_of_dated_text() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["amendments"] = ["bare string"]
    check("manifest-amendment-shape", validate_record(rec) != [])


def test_unknown_record_kind_rejected() -> None:
    check("unknown-record-kind", validate_record({"record": "mystery@1"}) != [])


def valid_checkpoint_r1() -> dict:
    return load("valid-checkpoint-r1.json")


def test_checkpoint_valid_examples() -> None:
    check("checkpoint-r1", validate_record(valid_checkpoint_r1()) == [])
    check("checkpoint-r2", validate_record(load("valid-checkpoint-r2-chained.json")) == [])


def test_checkpoint_r1_must_have_null_prev() -> None:
    rec = copy.deepcopy(valid_checkpoint_r1())
    rec["prev_checkpoint_sha256"] = "a" * 64
    check("checkpoint-r1-null-prev", validate_record(rec) != [])


def test_checkpoint_r2_requires_prev_sha() -> None:
    rec = load("valid-checkpoint-r2-chained.json")
    rec["prev_checkpoint_sha256"] = None
    check("checkpoint-r2-needs-prev", validate_record(rec) != [])


def test_checkpoint_embedded_manifest_is_validated() -> None:
    rec = copy.deepcopy(valid_checkpoint_r1())
    del rec["manifest"]["authority"]
    check("checkpoint-embedded-manifest", validate_record(rec) != [])


def test_checkpoint_status_closed_list() -> None:
    rec = copy.deepcopy(valid_checkpoint_r1())
    rec["status"] = "paused"
    check("checkpoint-closed-status", validate_record(rec) != [])


def test_receipt_valid() -> None:
    check("receipt-valid", validate_record(load("valid-receipt.json")) == [])


def test_receipt_after_hash_required() -> None:
    rec = load("valid-receipt.json")
    rec["after_sha256"] = "not-a-hash"
    check("receipt-after-hash", validate_record(rec) != [])


def test_verdict_valid_pass() -> None:
    check("verdict-pass", validate_record(load("valid-verdict-pass-separated.json")) == [])
    check("verdict-fail", validate_record(load("valid-verdict-fail.json")) == [])


def test_verdict_self_certification_refused() -> None:
    rec = load("valid-verdict-pass-separated.json")
    rec["acceptor_id"] = rec["worker_id"]
    check("verdict-no-self-cert", validate_record(rec) != [])

    # a capitalization variant of the worker is still the worker
    rec = load("valid-verdict-pass-separated.json")
    rec["acceptor_id"] = rec["worker_id"].title()
    check("verdict-no-self-cert-casefold", validate_record(rec) != [])


def test_verdict_operator_tier_binds_acceptor() -> None:
    rec = load("valid-verdict-pass-separated.json")
    rec["assurance_tier"] = "operator-accepted"
    check("verdict-operator-tier-acceptor", validate_record(rec) != [])


def test_receipt_and_verdict_mission_id_kebab_required() -> None:
    rec = load("valid-receipt.json")
    rec["mission_id"] = "Bad_ID"
    check("receipt-mission-id-kebab", validate_record(rec) != [])

    rec = load("valid-verdict-pass-separated.json")
    rec["mission_id"] = "Bad_ID"
    check("verdict-mission-id-kebab", validate_record(rec) != [])


def test_manifest_guards_valid_example() -> None:
    check("manifest-guards-valid-example",
          validate_record(load("valid-manifest-guards.json")) == [])


def test_manifest_guard_examples_invalid() -> None:
    for name in (
        "invalid-manifest-guard-bad-mode.json",
        "invalid-manifest-guard-empty-rule.json",
        "invalid-manifest-guard-bad-regex.json",
        "invalid-manifest-guard-mode-without-guards.json",
        "invalid-manifest-guard-unknown-field.json",
        "invalid-manifest-guard-shell-only-globs.json",
    ):
        check(f"manifest-{name}", validate_record(load(name)) != [])


def test_manifest_guards_optional_absent() -> None:
    # The pre-change minimal manifest must still validate: fields are additive.
    check("manifest-guards-optional-absent",
          validate_record(valid_manifest()) == [])


def test_manifest_guard_rules_shape() -> None:
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["guard_mode"] = "audit"
    rec["authority"]["actuator_guards"] = [{
        "name": "arr", "tool_names": ["Bash"],
        "command_regexes": ["7878"], "path_globs": []}]
    check("manifest-guard-rules-inline-valid", validate_record(rec) == [])
    bad = copy.deepcopy(rec)
    bad["authority"]["actuator_guards"][0]["tool_names"] = []
    check("manifest-guard-empty-tool-names", validate_record(bad) != [])


def test_manifest_guard_empty_guards_list_invalid() -> None:
    # [] is not "clear the guards" (that is amend(..., actuator_guards=None));
    # the schema's minItems: 1 forbids it and the hand validator must agree.
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = []
    check("manifest-guards-empty-list", validate_record(rec) != [])


def test_manifest_guard_inert_shapes_rejected() -> None:
    # A rule whose patterns can never fire for its tools arms nothing while
    # reading as armed -- refuse those shapes at validation.
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["Bash"],
        "command_regexes": [], "path_globs": ["M:/Media/**"]}]
    check("guard-shell-only-globs-inert", validate_record(rec) != [])

    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["Write"],
        "command_regexes": ["secret"], "path_globs": []}]
    check("guard-write-only-regexes-inert", validate_record(rec) != [])

    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["mcp__sonarr__post"],
        "command_regexes": [], "path_globs": ["M:/Media/**"]}]
    check("guard-mcp-only-globs-inert", validate_record(rec) != [])

    # mixed or unknown tool names pass: one arm can still fire (mixed), and
    # unknown tools are the operator's responsibility
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["Bash", "Write"],
        "command_regexes": [], "path_globs": ["M:/Media/**"]}]
    check("guard-mixed-tools-pass", validate_record(rec) == [])
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["FutureTool"],
        "command_regexes": [], "path_globs": ["M:/Media/**"]}]
    check("guard-unknown-tools-pass", validate_record(rec) == [])


def test_examples_corpus() -> None:
    ex = ROOT / "examples"
    for path in sorted(ex.glob("valid-*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        check(f"corpus-{path.name}", validate_record(rec) == [])
    for path in sorted(ex.glob("invalid-*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        check(f"corpus-{path.name}", validate_record(rec) != [])


def main() -> int:
    test_constants()
    test_manifest_valid_example()
    test_manifest_missing_instruction()
    test_manifest_unknown_top_level_field()
    test_manifest_bad_tier()
    test_manifest_amendments_must_be_list_of_dated_text()
    test_unknown_record_kind_rejected()
    test_checkpoint_valid_examples()
    test_checkpoint_r1_must_have_null_prev()
    test_checkpoint_r2_requires_prev_sha()
    test_checkpoint_embedded_manifest_is_validated()
    test_checkpoint_status_closed_list()
    test_receipt_valid()
    test_receipt_after_hash_required()
    test_verdict_valid_pass()
    test_verdict_self_certification_refused()
    test_verdict_operator_tier_binds_acceptor()
    test_receipt_and_verdict_mission_id_kebab_required()
    test_manifest_guards_valid_example()
    test_manifest_guard_examples_invalid()
    test_manifest_guards_optional_absent()
    test_manifest_guard_rules_shape()
    test_manifest_guard_empty_guards_list_invalid()
    test_manifest_guard_inert_shapes_rejected()
    test_examples_corpus()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
