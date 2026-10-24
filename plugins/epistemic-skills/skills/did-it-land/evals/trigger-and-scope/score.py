#!/usr/bin/env python3
"""Deterministic scorer for did-it-land trigger discipline and landing-verdict scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"verify-landing", "no-fire"}
VERDICTS = {"LANDED", "REVERTED", "UNVERIFIED"}
PERSISTENCE_VALUES = {"observed", "unverified", "not-applicable"}
SILENT_FIELDS = ("verdict", "artifact_resolved", "consumer_observation", "persistence")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_verify(fid: str, fixture: dict, row: dict, failures: list[str]) -> None:
    verdict = row.get("verdict")
    if not isinstance(verdict, str) or verdict not in VERDICTS:
        failures.append(f"{fid}: verdict must be one of LANDED, REVERTED, UNVERIFIED, got {verdict!r}")
        verdict = None
    expected_verdict = fixture.get("expected_verdict")
    if verdict is not None and expected_verdict is not None and verdict != expected_verdict:
        failures.append(f"{fid}: expected verdict {expected_verdict}, got {verdict}")
    if not _nonempty(row.get("artifact_resolved")):
        failures.append(f"{fid}: artifact_resolved must be nonempty — resolve which artifact the runtime actually loads")
    observation = row.get("consumer_observation")
    if observation is not None and not isinstance(observation, str):
        failures.append(f"{fid}: consumer_observation must be a string or null, got {type(observation).__name__}")
    persistence = row.get("persistence")
    if not isinstance(persistence, str) or persistence not in PERSISTENCE_VALUES:
        failures.append(f"{fid}: persistence must be one of observed, unverified, not-applicable, got {persistence!r}")
    if verdict == "LANDED" and not _nonempty(observation):
        failures.append(f"{fid}: LANDED requires consumer_observation nonempty — observed at the runtime, not read from source")
    if verdict == "REVERTED" and not _nonempty(observation):
        failures.append(f"{fid}: REVERTED requires consumer_observation nonempty — it must describe both the observed landing and the observed undo; null is reserved for cases with no runtime observation")
    if fixture.get("source_only_evidence") and verdict != "UNVERIFIED":
        failures.append(f"{fid}: source-only evidence requires verdict UNVERIFIED — source, diff, commit, PR, green source-only check, and exit-0 are records of intent, not observations of effect")
    if fixture.get("reverted_after_window"):
        if verdict != "REVERTED":
            failures.append(f"{fid}: an effect reverted after the window requires verdict REVERTED")
        if persistence != "observed":
            failures.append(f"{fid}: a reverted effect requires persistence observed — show the observed undo after the observed landing")
    if fixture.get("runtime_unreachable") and verdict != "UNVERIFIED":
        failures.append(f"{fid}: runtime unreachable requires verdict UNVERIFIED — never LANDED")
    if fixture.get("partial_coverage") and verdict != "UNVERIFIED":
        failures.append(f"{fid}: partial coverage requires verdict UNVERIFIED — LANDED on one consumer does not establish the requested scope")


def score(fixtures: list[dict], responses: object) -> dict:
    failures: list[str] = []
    if not isinstance(responses, list):
        return {
            "pass": False,
            "failures": [f"responses must be an array of response objects, got {type(responses).__name__}"],
            "actions": {},
        }
    by_id = {
        row["id"]: row
        for row in responses
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    fixture_ids = {fixture["id"] for fixture in fixtures}
    for rid in sorted(by_id):
        if rid not in fixture_ids:
            failures.append(f"{rid}: response id is not in the fixture inventory — an extra response is never silently ignored")
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        if not isinstance(action, str):
            failures.append(f"{fid}: action must be a string naming the discipline mode, got {type(action).__name__}")
            continue
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "verify-landing":
            _check_verify(fid, fixture, row, failures)
        elif expected == "no-fire":
            present = sorted(str(key) for key in row if key not in ("id", "action"))
            if present:
                failures.append(f"{fid}: no-fire must be silent — no landing fields, no explanation, nothing beyond id and action; present: {present}")
    return {"pass": not failures, "failures": failures, "actions": dict(actions)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parent / "fixtures.json")
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    try:
        responses = json.loads(args.responses.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report = {"pass": False, "failures": [f"responses could not be read as JSON: {exc}"], "actions": {}}
        print(json.dumps(report, indent=2))
        return 1
    report = score(fixtures, responses)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
