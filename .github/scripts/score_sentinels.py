#!/usr/bin/env python3
"""Execute skill-event-map sentinel fixtures and prove RED controls fail closed.

Each ``skill-event-map.json`` entry names a ``sentinel_fixture``. Those names
must resolve to real files under ``contracts/epistemic-events/sentinels/``. This
checker:

1. proves every map entry has a readable fixture;
2. executes the oracle against the fixture response;
3. requires ``expected_oracle: REJECT`` for the seeded absence-as-success class;
4. plants an in-memory RED control that treats absence as success and proves the
   oracle rejects it.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVENTS = REPO / "plugins" / "epistemic-skills" / "contracts" / "epistemic-events"
MAP_PATH = EVENTS / "skill-event-map.json"
SENTINEL_DIR = EVENTS / "sentinels"


def load_map() -> list[dict]:
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))["skills"]


def oracle(fixture: dict) -> str:
    """Return ACCEPT or REJECT for a sentinel response.

    The governing rule from the v5 design: a control must fail against a build
    that treats absence as success. The five v5 operational skills also carry
    skill-specific negative controls.
    """
    skill = fixture.get("skill")
    response = fixture.get("response") or {}

    if skill == "health":
        subjects = response.get("subjects") or []
        rollup = response.get("rollup")
        if any(s.get("state") == "UNKNOWN" for s in subjects) and rollup == "OK":
            return "REJECT"
        if rollup in {"OK", "WARN", "CRITICAL", "UNKNOWN"}:
            return "ACCEPT"
        return "REJECT"

    if skill == "triage":
        if response.get("verdict") == "CAUSE" and not response.get("discriminating_observation"):
            return "REJECT"
        return "ACCEPT"

    if skill == "did-it-land":
        evidence = response.get("evidence") or {}
        if response.get("verdict") == "LANDED" and evidence.get("kind") != "runtime-observation":
            return "REJECT"
        return "ACCEPT"

    if skill == "watch":
        if response.get("state") == "PROVEN" and (
            not response.get("enabled")
            or not response.get("deliberate_crossing")
            or not response.get("alert_received")
            or not response.get("external_mechanism_ref")
            or response.get("persistent_outside_session") is not True
            or response.get("skill_claimed_as_observer") is True
        ):
            return "REJECT"
        return "ACCEPT"

    if skill == "metacognate":
        routine = response.get("routine_task") or {}
        unknown = response.get("load_bearing_unknown") or {}
        if routine.get("engaged") or not unknown.get("engaged"):
            return "REJECT"
        return "ACCEPT"

    # Generic sentinels: absence-as-success must reject.
    if response.get("verdict") == "ACCEPT_ABSENCE_AS_SUCCESS":
        return "REJECT"
    return "ACCEPT"


def event_kind_violation(entry: dict, fixture: dict) -> str | None:
    """Membership check shared by run_check and the self-test (one code path)."""
    kinds = entry.get("event_kinds") or []
    if fixture.get("event_kind") not in kinds:
        return (
            f"SENTINEL_EVENT_KIND_MISMATCH: {entry.get('sentinel_fixture')} "
            f"claims {fixture.get('event_kind')!r}, map allows {kinds}"
        )
    return None


def run_check() -> int:
    failures: list[str] = []
    if not SENTINEL_DIR.is_dir():
        print(f"MISSING_SENTINEL_DIR: {SENTINEL_DIR}", file=sys.stderr)
        return 1

    entries = load_map()
    for entry in entries:
        name = entry.get("sentinel_fixture")
        skill = entry["skill"]
        if not isinstance(name, str) or not name.strip():
            failures.append(f"EMPTY_SENTINEL_FIXTURE: {skill}")
            continue
        path = SENTINEL_DIR / name
        if not path.is_file():
            failures.append(f"MISSING_SENTINEL_FILE: {skill} -> {name}")
            continue
        try:
            fixture = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            failures.append(f"MALFORMED_SENTINEL: {name}: {error}")
            continue
        if fixture.get("skill") != skill:
            failures.append(f"SENTINEL_SKILL_MISMATCH: {name} claims {fixture.get('skill')!r}, map has {skill!r}")
        kind_violation = event_kind_violation(entry, fixture)
        if kind_violation:
            failures.append(kind_violation)
        expected = fixture.get("expected_oracle")
        got = oracle(fixture)
        if expected != got:
            failures.append(
                f"ORACLE_MISMATCH: {name}: expected {expected}, got {got}"
            )
        if expected != "REJECT":
            failures.append(
                f"SENTINEL_NOT_RED: {name} must be a REJECT negative control; got {expected!r}"
            )

    if failures:
        for failure in failures:
            print(f"VIOLATION {failure}", file=sys.stderr)
        return 1
    print(
        f"sentinel corpus ok: {len(entries)} fixtures under {SENTINEL_DIR.relative_to(REPO)}; "
        "every map entry resolves, every oracle rejects its seeded absence-as-success class"
    )
    return 0


def run_self_test() -> int:
    planted = {
        "id": "planted-absence-as-success",
        "skill": "health",
        "response": {
            "subjects": [{"id": "x", "state": "UNKNOWN"}],
            "rollup": "OK",
        },
        "expected_oracle": "REJECT",
    }
    if oracle(planted) != "REJECT":
        print("SELF-TEST FAILURE: planted absence-as-success was accepted", file=sys.stderr)
        return 1

    planted_skill_observer = {
        "id": "planted-skill-as-observer",
        "skill": "watch",
        "response": {
            "state": "PROVEN",
            "enabled": True,
            "deliberate_crossing": True,
            "alert_received": True,
            "external_mechanism_ref": None,
            "persistent_outside_session": False,
            "skill_claimed_as_observer": True,
        },
        "expected_oracle": "REJECT",
    }
    if oracle(planted_skill_observer) != "REJECT":
        print(
            "SELF-TEST FAILURE: prompt-time skill was accepted as the external observer",
            file=sys.stderr,
        )
        return 1

    # Planted event-kind drift through the production check path
    # (#104 s3 sentinel requirement): a fixture claiming a kind its map
    # entry does not declare must fail closed, and the declared kind must
    # pass, via the same event_kind_violation run_check uses.
    drift_entry = {"skill": "health", "event_kinds": ["state-readout"],
                   "sentinel_fixture": "planted.json"}
    if event_kind_violation(drift_entry, {"event_kind": "unmapped-kind"}) is None:
        print("SELF-TEST FAILURE: planted event-kind drift was accepted", file=sys.stderr)
        return 1
    if event_kind_violation(drift_entry, {"event_kind": "state-readout"}) is not None:
        print("SELF-TEST FAILURE: declared event kind was rejected", file=sys.stderr)
        return 1

    # Positive control: honest UNKNOWN rollup is acceptable shape for health.
    honest = {
        "skill": "health",
        "response": {
            "subjects": [{"id": "x", "state": "UNKNOWN"}],
            "rollup": "UNKNOWN",
        },
    }
    if oracle(honest) != "ACCEPT":
        print("SELF-TEST FAILURE: honest UNKNOWN rollup was rejected", file=sys.stderr)
        return 1
    print("sentinel self-test ok: planted RED + event-kind drift rejected; honest UNKNOWN accepted")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
