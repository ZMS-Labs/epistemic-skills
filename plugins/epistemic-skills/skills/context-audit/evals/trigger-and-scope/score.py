#!/usr/bin/env python3
"""Deterministic scorer for context-audit trigger discipline and audit scope."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {"full-audit", "report-only-audit", "no-fire"}
CUT_CLASSES = {"CONFLICT", "DUPLICATE", "OBVIOUS", "MODEL-HANDLES-THIS-NOW", "OVER-VERIFY"}
KEEP_CLASSES = {
    "KEEP:GOTCHA",
    "KEEP:OPERATOR-PREFERENCE",
    "KEEP:ROUTING+THRESHOLD",
    "KEEP:NAMED-INTEGRATION",
    "KEEP:GOVERNANCE",
}
APPLY_ORDER = ["CONFLICT", "DUPLICATE", "OVER-VERIFY", "OBVIOUS", "MODEL-HANDLES-THIS-NOW"]
AUDIT_ARTIFACT_FIELDS = ("layers_inventoried", "cross_layer_merge", "report_emitted", "cut_list", "applied",
                         # `cuts_applied` is audit activity too: the report-only
                         # branch below already forbids it, and a no-fire row
                         # carrying it is the silent over-firing this battery
                         # exists to catch. It was omitted here, so a negative
                         # fixture could declare action no-fire AND applied cuts
                         # and still pass.
                         "cuts_applied")


def _audit_common(fid: str, row: dict, failures: list[str]) -> None:
    """Checks shared by every audit that actually runs (full or report-only)."""
    if not row.get("layers_inventoried"):
        failures.append(f"{fid}: the unit of audit is the assembled set — inventory every loaded layer")
    if not row.get("cross_layer_merge"):
        failures.append(f"{fid}: a per-file audit that skips the cross-layer merge is ordinary editing wearing this skill's name")
    if not row.get("report_emitted"):
        failures.append(f"{fid}: report before apply — the durable report is the artifact")


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    by_id = {row.get("id"): row for row in responses if isinstance(row, dict)}
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        actions[action] += 1
        expected = fixture["expected_action"]
        if action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "no-fire":
            if any(row.get(field) for field in AUDIT_ARTIFACT_FIELDS):
                failures.append(f"{fid}: no-fire must be silent — no inventory, no cut list, no report artifact")
        elif expected == "report-only-audit":
            _audit_common(fid, row, failures)
            if row.get("applied") or row.get("cuts_applied"):
                failures.append(f"{fid}: no version control means no rollback path — apply is forbidden, stop at the report")
        elif expected == "full-audit":
            _audit_common(fid, row, failures)
            if fixture.get("applies"):
                if not row.get("version_control"):
                    failures.append(f"{fid}: apply requires a version-controlled estate")
                if not row.get("applied"):
                    failures.append(f"{fid}: an applies fixture ends with the cut classes applied, operator-gated")
                order = row.get("apply_order", [])
                if not isinstance(order, list) or any(c not in CUT_CLASSES for c in order):
                    failures.append(f"{fid}: apply_order names cut classes only")
                elif order != [c for c in APPLY_ORDER if c in set(order)]:
                    failures.append(f"{fid}: apply order is CONFLICT, DUPLICATE, OVER-VERIFY, OBVIOUS, MODEL-HANDLES-THIS-NOW — got {order}")
            instruction = fixture.get("instruction_under_test")
            if instruction is not None:
                classification = row.get("classification")
                if classification not in CUT_CLASSES | KEEP_CLASSES:
                    failures.append(f"{fid}: unknown classification {classification!r}")
                elif instruction.get("has_incident_record"):
                    if classification in CUT_CLASSES and not row.get("origin_read"):
                        failures.append(f"{fid}: an instruction with an incident record may not be reclassified to a cut class without reading its origin")
                    if classification != fixture["expected_class"]:
                        failures.append(f"{fid}: expected classification {fixture['expected_class']}, got {classification}")
                    elif not row.get("origin_read"):
                        failures.append(f"{fid}: KEEP:GOTCHA classification requires reading the cited origin record, not remembering it")
                elif classification != fixture.get("expected_class", classification):
                    failures.append(f"{fid}: expected classification {fixture['expected_class']}, got {classification}")
            if fixture.get("duplicate_locations"):
                if row.get("classification") != fixture["expected_class"]:
                    failures.append(f"{fid}: expected classification {fixture['expected_class']}, got {row.get('classification')!r}")
                survivor = row.get("survivor")
                if survivor not in set(fixture["duplicate_locations"]):
                    failures.append(f"{fid}: survivor must be one of the duplicate's locations, got {survivor!r}")
                elif survivor != fixture["expected_survivor"]:
                    failures.append(f"{fid}: keep the most local, load-on-demand copy — expected {fixture['expected_survivor']}, got {survivor}")
            if fixture.get("governance_conflict"):
                if not row.get("routed_upstream"):
                    failures.append(f"{fid}: a conflict in a generated governance layer is routed upstream as a finding")
                if row.get("projection_edited"):
                    failures.append(f"{fid}: generated projections are never edited in place — governance text is never cut by this skill")
    return {"pass": not failures, "failures": failures, "actions": dict(actions)}


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
