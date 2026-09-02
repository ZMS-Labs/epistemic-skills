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
        "mission-manifest@1", "checkpoint@1", "receipt@1", "acceptance-verdict@1"})


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


def test_manifest_envelope_lists_require_nonblank_entries() -> None:
    """es#160: truthy whitespace is not a usable declaration.

    These are manifest declarations, not filesystem names. A whitespace-only
    artifact path remains legal and is pinned separately below.
    """
    fields = (
        ("permissions", ("authority", "permissions")),
        ("protected-state", ("authority", "protected_state")),
        ("acceptable-costs", ("authority", "acceptable_costs")),
        ("scope-in", ("scope", "in")),
        ("scope-out", ("scope", "out")),
        ("hold-if", ("stop_rules", "hold_if")),
        ("stop-if", ("stop_rules", "stop_if")),
        ("escalate-if", ("stop_rules", "escalate_if")),
    )
    for label, (section, field) in fields:
        blank = copy.deepcopy(valid_manifest())
        blank[section][field] = [" \t\u00a0 "]
        check(f"manifest-{label}-blank-refused", validate_record(blank) != [])

        substantive = copy.deepcopy(valid_manifest())
        substantive[section][field] = ["  declared boundary  "]
        check(f"manifest-{label}-substantive-whitespace-allowed",
              validate_record(substantive) == [])

        empty = copy.deepcopy(valid_manifest())
        empty[section][field] = []
        check(f"manifest-{label}-empty-allowed", validate_record(empty) == [])


def test_manifest_envelope_compound_and_embedded_blanks() -> None:
    """Blank declarations fail predictably when faults are combined or nested."""
    fields = (
        ("authority", "permissions"),
        ("authority", "protected_state"),
        ("authority", "acceptable_costs"),
        ("scope", "in"),
        ("scope", "out"),
        ("stop_rules", "hold_if"),
        ("stop_rules", "stop_if"),
        ("stop_rules", "escalate_if"),
    )

    compound = copy.deepcopy(valid_manifest())
    for section, field in fields:
        compound[section][field] = [" \t\u00a0 "]
    check("manifest-envelope-all-blanks-refused",
          validate_record(compound) != [])

    mixed = copy.deepcopy(valid_manifest())
    mixed["authority"]["permissions"] = []
    mixed["scope"]["in"] = ["  substantive  "]
    mixed["stop_rules"]["escalate_if"] = ["\u0085"]
    check("manifest-envelope-mixed-blank-refused",
          validate_record(mixed) != [])

    checkpoint = valid_checkpoint_r1()
    for section, field in fields:
        checkpoint["manifest"][section][field] = ["\u001c"]
    check("checkpoint-embedded-envelope-blanks-refused",
          validate_record(checkpoint) != [])


def test_whitespace_only_artifact_path_remains_legal() -> None:
    """Declaration validation must not leak into the filename surface."""
    rec = load("valid-receipt.json")
    rec["artifact_path"] = "   "
    check("receipt-whitespace-only-artifact-path-valid",
          validate_record(rec) == [])


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

    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["Write"],
        "command_regexes": [], "path_globs": [""]}]
    check("guard-empty-path-glob-rejected", validate_record(rec) != [])


def test_unhashable_guard_mode_returns_validation_error() -> None:
    """es#137 P2: a list/dict guard_mode must be a validation error, never
    TypeError from set membership."""
    rec = copy.deepcopy(valid_manifest())
    rec["authority"]["guard_mode"] = ["enforce"]
    rec["authority"]["actuator_guards"] = [{
        "name": "g", "tool_names": ["Bash"],
        "command_regexes": ["rm"], "path_globs": []}]
    try:
        errors = validate_record(rec)
    except TypeError:
        check("unhashable-guard-mode-no-typeerror", False)
        return
    check("unhashable-guard-mode-no-typeerror", True)
    check("unhashable-guard-mode-returns-validation-error", errors != [])

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


def test_closed_vocabularies_never_raise_typeerror() -> None:
    """Every CLOSED vocabulary must answer a non-string with a validation
    ERROR, not a TypeError.

    es#137 P2 fixed exactly one of these -- `guard_mode` -- and the class was
    scoped to that instance. The same `value in SET` shape sits on
    `checkpoint.status`, `verdict.verdict`, `verdict.assurance_tier`,
    `manifest.acceptance.required_tier`, and the top-level `record` kind, and
    every one of them raises `TypeError: unhashable type` on a list or dict.
    Measured before the fix: `validate_record({... "status": []})` raised
    TypeError, and a sibling checkpoint carrying `"status": []` took EVERY
    pathless custody command in the workspace down with it (see
    test_custody_mission.test_typeinvalid_sibling_is_skipped_not_fatal).

    `validate_record` promises a list of errors. A promise that becomes a
    traceback on hostile input is a denial of service through the recovery
    path -- exactly what drift detection exists to survive."""
    cases = []

    rec = copy.deepcopy(valid_checkpoint_r1())
    rec["status"] = []
    cases.append(("checkpoint-status", rec))

    rec = copy.deepcopy(valid_checkpoint_r1())
    rec["manifest"]["acceptance"]["required_tier"] = {}
    cases.append(("manifest-required-tier", rec))

    rec = copy.deepcopy(valid_manifest())
    rec["acceptance"]["required_tier"] = []
    cases.append(("manifest-required-tier-standalone", rec))

    rec = load("valid-verdict-pass-separated.json")
    rec["verdict"] = []
    cases.append(("verdict-verdict", rec))

    rec = load("valid-verdict-pass-separated.json")
    rec["assurance_tier"] = {"a": 1}
    cases.append(("verdict-assurance-tier", rec))

    cases.append(("record-kind", {"record": ["checkpoint@1"]}))

    for name, record in cases:
        try:
            errors = validate_record(record)
        except TypeError:
            check(f"closed-vocab-no-typeerror-{name}", False)
            continue
        check(f"closed-vocab-no-typeerror-{name}", True)
        check(f"closed-vocab-returns-errors-{name}", errors != [])


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
    test_manifest_envelope_lists_require_nonblank_entries()
    test_manifest_envelope_compound_and_embedded_blanks()
    test_whitespace_only_artifact_path_remains_legal()
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
    test_unhashable_guard_mode_returns_validation_error()
    test_closed_vocabularies_never_raise_typeerror()
    test_examples_corpus()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
