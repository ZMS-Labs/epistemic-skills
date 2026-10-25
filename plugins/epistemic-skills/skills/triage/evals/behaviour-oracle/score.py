#!/usr/bin/env python3
"""Deterministic scorer for the triage behaviour-oracle corpus.

Scores declared causal verdicts against planted evidence states: the
verdict the evidence supports, the rule that a cause requires an
observation that would have come out differently under an alternative,
and the degraded-operation behaviours triage's Oracle section specifies.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

VERDICTS = {"CAUSE", "NARROWED", "UNKNOWN", "NOT-BROKEN"}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _id_set(row: dict, field: str, fid: str, failures: list) -> set:
    value = row.get(field, [])
    if not isinstance(value, list):
        failures.append(f"{fid}: {field} must be an array of bare ids, got {type(value).__name__}")
        return set()
    bad = [item for item in value if not isinstance(item, str)]
    if bad:
        failures.append(f"{fid}: {field} must contain only bare string ids")
        return {item for item in value if isinstance(item, str)}
    if any(not item.strip() for item in value):
        failures.append(f"{fid}: {field} must not contain empty ids")
    return set(value)


def score(fixtures: list[dict], responses: object) -> dict:
    failures: list[str] = []
    if not isinstance(responses, list):
        return {
            "pass": False,
            "failures": [f"responses must be an array of response objects, got {type(responses).__name__}"],
            "verdicts": {},
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
            failures.append(f"{rid}: response id not in fixtures")
    verdicts: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        verdict = row.get("verdict")
        if not isinstance(verdict, str):
            failures.append(f"{fid}: verdict must be a string naming the causal verdict, got {type(verdict).__name__}")
            continue
        verdicts[verdict] += 1
        if verdict not in VERDICTS:
            failures.append(f"{fid}: unknown verdict {verdict!r}")
            continue
        named = row.get("named_cause")
        forbidden = fixture.get("forbidden_cause")
        if forbidden and isinstance(named, str) and named.strip().lower() == forbidden.strip().lower():
            failures.append(f"{fid}: the most plausible candidate was named as the cause without a discriminating observation")
        expected = fixture["expected_verdict"]
        if verdict != expected:
            failures.append(f"{fid}: expected {expected}, got {verdict}")
            continue
        if verdict == "CAUSE":
            if not _nonempty(row.get("discriminating_observation")):
                failures.append(f"{fid}: CAUSE requires a discriminating observation — an observation that would have come out differently if the cause were something else")
            if not _nonempty(named):
                failures.append(f"{fid}: CAUSE requires the cause to be named")
            if fixture.get("expected_cause") and named != fixture["expected_cause"]:
                failures.append(f"{fid}: expected cause {fixture['expected_cause']!r}, got {named!r}")
        if verdict in ("NARROWED", "UNKNOWN") and named is not None:
            failures.append(f"{fid}: {verdict} never names a cause — a candidate that merely fits the symptom is a hypothesis")
        if verdict == "NOT-BROKEN":
            if not _nonempty(row.get("discriminating_observation")):
                failures.append(f"{fid}: NOT-BROKEN requires an adequate direct observation of the reported behavior — a generic readout cannot contradict a specific failure")
            if named is not None:
                failures.append(f"{fid}: NOT-BROKEN never names a cause — naming a cause asserts a fault, and the verdict is that there is none")
        eliminated = _id_set(row, "eliminated", fid, failures)
        if verdict == "NARROWED":
            if not _nonempty(row.get("discriminating_observation")):
                failures.append(f"{fid}: NARROWED requires a discriminating observation — the observation that eliminated a candidate; a narrowing with no eliminating observation is UNKNOWN")
            if not any(_nonempty(item) for item in eliminated):
                failures.append(f"{fid}: NARROWED requires at least one eliminated candidate — name the candidate the observation eliminated")
        if verdict == "UNKNOWN" and any(_nonempty(item) for item in eliminated):
            failures.append(f"{fid}: UNKNOWN must not name eliminated candidates — an elimination claims an observation that rules a candidate out, and UNKNOWN is the verdict for insufficient evidence to eliminate")
        for required in fixture.get("expected_eliminated", []):
            if required not in eliminated:
                failures.append(f"{fid}: the observation eliminated {required!r}; the verdict must name what was eliminated and by what observation")
        if forbidden and any(isinstance(item, str) and item.strip().lower() == forbidden.strip().lower() for item in eliminated):
            failures.append(f"{fid}: the forbidden candidate {forbidden!r} was claimed as eliminated — an elimination claims an observation that rules a candidate out, and no observation in this scenario rules this one out")
        if verdict == "NARROWED":
            expected_eliminated = fixture.get("expected_eliminated", [])
            extra = sorted(item for item in eliminated if item not in expected_eliminated)
            if extra:
                failures.append(f"{fid}: eliminated names {extra!r}, which the discriminating observation does not eliminate — a candidate is eliminated only by an observation that rules it out, and this verdict's observation eliminates {sorted(expected_eliminated)!r}")
        if fixture.get("evidence_basis_required"):
            if row.get("evidence_basis") != fixture["evidence_basis_required"]:
                failures.append(f"{fid}: with no readout available the output is labelled self-probed — evidence_basis must be {fixture['evidence_basis_required']!r}")
        if fixture.get("qualifier_required"):
            if row.get("qualifier") != fixture["qualifier_required"]:
                failures.append(f"{fid}: verdict must carry the qualifier {fixture['qualifier_required']!r}")
        flag = fixture.get("flag_required")
        if flag and row.get(flag) is not True:
            failures.append(f"{fid}: {flag} must be true — the degraded condition is named in the output, never absorbed")
        plans = fixture.get("observation_plan_required")
        if plans and row.get("observation_plan") not in plans:
            failures.append(f"{fid}: a destructive observation is never run on diagnosis authority — observation_plan must be one of {plans}")
    return {"pass": not failures, "failures": failures, "verdicts": dict(verdicts)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parent / "fixtures.json")
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    responses = json.loads(args.responses.read_text(encoding="utf-8"))
    report = score(fixtures, responses)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
