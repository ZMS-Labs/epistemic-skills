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


def test_unknown_record_kind_rejected() -> None:
    check("unknown-record-kind", validate_record({"record": "mystery@1"}) != [])


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
    test_examples_corpus()
    print(f"\n{len(FAILURES)} failures")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    raise SystemExit(main())
