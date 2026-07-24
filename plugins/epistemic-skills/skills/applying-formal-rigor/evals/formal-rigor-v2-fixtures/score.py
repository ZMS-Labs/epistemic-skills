#!/usr/bin/env python3
"""Deterministic stdlib structural scorer for formal-rigor v2 fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FAMILIES = {f"P{i}" for i in range(1, 10)}
INVOCATIONS = {"skip", "focused", "standard", "high-assurance"}
SYNTHESIS = {"dominance", "pareto-set", "conditional", "underdetermined", "reversal", "reversible-probe"}
TRAP_CLASSES = {"theorem-misuse", "missed-terrain", "forced-closure", "overtrigger-tier", "staleness", "unmapped"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_inventory(fixtures_dir: Path) -> dict[str, dict]:
    inventory = {}
    for directory in sorted(p for p in Path(fixtures_dir).iterdir() if p.is_dir()):
        truth_path = directory / "ground-truth.json"
        if not (truth_path.is_file() and (directory / "scenario.md").is_file() and (directory / "artifacts").is_dir()):
            raise ValueError(f"incomplete fixture directory: {directory}")
        truth = load_json(truth_path)
        fixture_id = truth.get("fixture_id")
        if fixture_id != directory.name or fixture_id in inventory:
            raise ValueError(f"fixture id/path mismatch or duplicate: {directory}")
        inventory[fixture_id] = truth
    return inventory


def validate_inventory(inventory: dict[str, dict]) -> list[str]:
    errors = []
    traps = [v for v in inventory.values() if v.get("kind") == "trap"]
    controls = [v for v in inventory.values() if v.get("kind") == "control"]
    if len(inventory) != 22: errors.append(f"inventory count {len(inventory)} != 22")
    if len(traps) != 18: errors.append(f"trap count {len(traps)} != 18")
    if len(controls) != 4: errors.append(f"control count {len(controls)} != 4")
    if sum(v.get("priority") == "P0" for v in inventory.values()) != 11: errors.append("P0 count != 11")
    classes = {c for v in traps for c in v.get("classes", [])}
    if TRAP_CLASSES - classes: errors.append(f"missing trap classes: {sorted(TRAP_CLASSES - classes)}")
    for fixture_id, truth in inventory.items():
        if truth.get("kind") not in {"trap", "control"}: errors.append(f"{fixture_id}: invalid kind")
        if truth.get("priority") not in {"P0", "P1"}: errors.append(f"{fixture_id}: invalid priority")
        if not truth.get("claims"): errors.append(f"{fixture_id}: claims missing")
        if not truth.get("author", {}).get("relationship"): errors.append(f"{fixture_id}: provenance missing")
    return errors


def fail(failures: list[dict], dimension: str, reason: str) -> None:
    failures.append({"dimension": dimension, "reason": reason})


def validate_record(record: object) -> list[dict]:
    failures = []
    if not isinstance(record, dict) or record.get("record") != "formal-rigor-record@2":
        fail(failures, "S2", "missing formal-rigor-record@2 envelope")
        return failures
    required = {"subject", "valid_while", "coverage_limits", "rigor", "decision_frame", "coverage", "derivations", "empirical_closure", "synthesis", "never_attests"}
    if required - set(record): fail(failures, "S2", f"record fields missing: {sorted(required - set(record))}")
    subject, valid = record.get("subject", {}), record.get("valid_while", [])
    if not subject.get("ref"): fail(failures, "S9", "subject.ref missing")
    if subject.get("revision") is None and "subject-revision-unchanged" in valid:
        fail(failures, "S9", "null revision cannot claim subject-revision-unchanged")
    if subject.get("revision") is not None and "subject-revision-unchanged" not in valid:
        fail(failures, "S9", "revision-pinned record lacks subject-revision-unchanged")
    rigor = record.get("rigor", {})
    if rigor.get("tier") not in {"standard", "high-assurance"} or not rigor.get("trigger") or not rigor.get("tier_reason"):
        fail(failures, "S1", "rigor tier/trigger/reason incomplete")
    frame = record.get("decision_frame", {})
    if not isinstance(frame, dict):
        fail(failures, "S2", "decision_frame must be an object")
        frame = {}
    for field in ("question", "system_boundary", "actors", "alternatives", "hard_constraints", "authorized_objectives", "priority_rule", "assumptions", "empirical_premises", "uncertainty_posture"):
        if field not in frame: fail(failures, "S2", f"decision_frame.{field} missing")
    coverage = record.get("coverage", [])
    families = [c.get("family") for c in coverage if isinstance(c, dict)]
    if len(coverage) != 9 or set(families) != FAMILIES or len(families) != len(set(families)):
        fail(failures, "S5", "coverage must contain exactly one P1-P9 entry")
    for row in coverage:
        if not isinstance(row, dict):
            fail(failures, "S5", "coverage row is not an object"); continue
        status, modules = row.get("status"), row.get("modules", [])
        if status not in {"fired", "not-applicable", "unmapped"} or not row.get("reason"):
            fail(failures, "S5", f"invalid coverage row {row.get('family')}")
        if status == "fired" and not modules: fail(failures, "S5", f"fired {row.get('family')} names no module")
        if status != "fired" and modules: fail(failures, "S5", f"non-fired {row.get('family')} names modules")
    for derivation in record.get("derivations", []):
        if not isinstance(derivation, dict): fail(failures, "S4", "derivation is not an object"); continue
        for field in ("id", "module", "construct", "sources", "model", "preconditions", "fact_mapping", "steps", "result", "residual_mismatch"):
            if field not in derivation: fail(failures, "S4", f"derivation missing {field}")
        if not derivation.get("preconditions") or not derivation.get("fact_mapping"):
            fail(failures, "S4", "derivation lacks applicability mapping")
    synthesis = record.get("synthesis", {})
    if synthesis.get("outcome") not in SYNTHESIS: fail(failures, "S8", "invalid synthesis outcome")
    if synthesis.get("outcome") in {"pareto-set", "underdetermined"} and synthesis.get("selected_option") is not None:
        fail(failures, "S8", "pareto/underdetermined cannot select an option")
    unmapped = [c for c in coverage if isinstance(c, dict) and c.get("status") == "unmapped"]
    if unmapped and not record.get("coverage_limits"): fail(failures, "S5", "unmapped terrain absent from coverage_limits")
    if unmapped and synthesis.get("outcome") == "dominance": fail(failures, "S8", "dominance forbidden with unmapped terrain")
    never = set(record.get("never_attests", []))
    expected = {"derivation-correctness-by-envelope", "empirical-fact-without-observation", "gauntlet-independence"}
    if not expected <= never: fail(failures, "S10", "never_attests boundary incomplete")
    return failures


def score_fixture(truth: dict, response: dict) -> dict:
    failures = []
    fixture_id = truth["fixture_id"]
    if not isinstance(response, dict):
        return {
            "fixture": fixture_id,
            "structural_pass": False,
            "dimensions_failed": ["S1"],
            "failures": [{"dimension": "S1", "reason": "response root must be an object"}],
        }
    if response.get("response") != "formal-rigor-fixture-response@1" or response.get("fixture") != fixture_id:
        fail(failures, "S1", "response envelope or fixture id mismatch")
    invocation = response.get("invocation")
    if invocation not in INVOCATIONS or invocation not in truth.get("expected_invocation", []):
        fail(failures, "S1", f"invocation {invocation!r} not allowed")
    focused_output = response.get("focused_output")
    if invocation == "skip":
        if not response.get("skip_reason") or response.get("record") is not None:
            fail(failures, "S1", "skip requires reason and null record")
        if focused_output not in (None, []): fail(failures, "S1", "skip cannot carry focused output")
    elif invocation == "focused":
        if response.get("record") is not None: fail(failures, "S1", "focused mode cannot emit formal-rigor-record@2")
        if not isinstance(focused_output, list) or not 1 <= len(focused_output) <= 6:
            fail(failures, "S1", "focused mode requires one to six short bullets")
        elif sum(len(str(item).split()) for item in focused_output) > 250:
            fail(failures, "S1", "focused output exceeds 250 visible words")
        if response.get("skip_reason") is not None: fail(failures, "S1", "focused response carries skip_reason")
    else:
        failures.extend(validate_record(response.get("record")))
        if response.get("skip_reason") is not None: fail(failures, "S1", "non-skip carries skip_reason")
        if focused_output not in (None, []): fail(failures, "S1", "standard/high-assurance cannot carry focused output")
    assessments = response.get("claim_assessments", [])
    by_id = {a.get("id"): a for a in assessments if isinstance(a, dict)}
    if len(by_id) != len(assessments): fail(failures, "S6", "claim ids missing or duplicated")
    for claim in truth.get("claims", []):
        actual = by_id.get(claim["id"])
        if actual is None: fail(failures, "S6", f"claim {claim['id']} omitted")
        elif actual.get("state") not in claim.get("allowed_states", []): fail(failures, "S6", f"claim {claim['id']} state not allowed")
    record = response.get("record") if isinstance(response.get("record"), dict) else {}
    rows = {c.get("family"): c for c in record.get("coverage", []) if isinstance(c, dict)}
    for req in truth.get("coverage", {}).get("required", []):
        row = rows.get(req["family"], {})
        if row.get("status") != req["status"]: fail(failures, "S5", f"{req['family']} expected {req['status']}")
        if not set(req.get("modules", [])) <= set(row.get("modules", [])): fail(failures, "S3", f"{req['family']} missing module")
    for item in truth.get("coverage", {}).get("forbidden", []):
        if rows.get(item["family"], {}).get("status") == item.get("status"): fail(failures, "S5", f"forbidden coverage state {item['family']}")
    frame = record.get("decision_frame", {})
    if not isinstance(frame, dict):
        fail(failures, "S2", "decision_frame must be an object")
        frame = {}
    if truth.get("decision_frame", {}).get("null_option_required"):
        alternatives = frame.get("alternatives", [])
        if not isinstance(alternatives, list) or any(not isinstance(item, dict) for item in alternatives):
            fail(failures, "S2", "decision_frame.alternatives must be an array of objects")
            alternatives = [item for item in alternatives if isinstance(item, dict)] if isinstance(alternatives, list) else []
        if len([a for a in alternatives if a.get("kind") == "null-option"]) != 1: fail(failures, "S2", "exactly one null option required")
    if truth.get("decision_frame", {}).get("priority_rule_required") and not frame.get("priority_rule", {}).get("authority_ref"):
        fail(failures, "S2", "authorized priority rule required")
    synthesis = record.get("synthesis", {})
    allowed = truth.get("synthesis", {}).get("allowed_outcomes", [])
    if invocation in {"standard", "high-assurance"} and allowed and synthesis.get("outcome") not in allowed: fail(failures, "S8", f"outcome {synthesis.get('outcome')} not allowed")
    expected_selected = truth.get("synthesis", {}).get("selected_option", "__unspecified__")
    if invocation in {"standard", "high-assurance"} and expected_selected != "__unspecified__" and synthesis.get("selected_option") != expected_selected:
        fail(failures, "S8", "selected option does not match obligation")
    freshness = truth.get("freshness", {})
    if freshness.get("must_re_fire") and record.get("subject", {}).get("revision") == freshness.get("stale_revision"):
        fail(failures, "S9", "stale revision reused")
    if invocation in {"standard", "high-assurance"}:
        pinned_sources = {
            source_id
            for derivation in record.get("derivations", []) if isinstance(derivation, dict)
            for source_ids in derivation.get("sources", {}).values() if isinstance(source_ids, list)
            for source_id in source_ids
        }
        missing_sources = set(truth.get("source_requirements", [])) - pinned_sources
        if missing_sources:
            fail(failures, "S9", f"required source pins missing: {sorted(missing_sources)}")
    dimensions = sorted({item["dimension"] for item in failures})
    return {"fixture": fixture_id, "structural_pass": not failures, "dimensions_failed": dimensions, "failures": failures}


def score_response_path(truth: dict, path: Path) -> dict:
    fixture_id = truth["fixture_id"]
    if not path.is_file():
        return {"fixture": fixture_id, "structural_pass": False, "dimensions_failed": ["S1"],
                "failures": [{"dimension": "S1", "reason": "response missing"}]}
    try:
        response: Any = load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return {"fixture": fixture_id, "structural_pass": False, "dimensions_failed": ["S1"],
                "failures": [{"dimension": "S1", "reason": f"invalid response JSON: {exc}"}]}
    try:
        return score_fixture(truth, response)
    except (AttributeError, KeyError, TypeError, ValueError) as exc:
        return {"fixture": fixture_id, "structural_pass": False, "dimensions_failed": ["S1"],
                "failures": [{"dimension": "S1", "reason": f"malformed response structure: {exc}"}]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures-dir", type=Path, default=Path(__file__).parent / "fixtures")
    ap.add_argument("--responses-dir", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--inventory-only", action="store_true")
    args = ap.parse_args()
    inventory = load_inventory(args.fixtures_dir)
    errors = validate_inventory(inventory)
    if errors:
        print("\n".join(f"ERROR: {e}" for e in errors)); return 1
    if args.inventory_only:
        print("inventory: PASS (22 fixtures; 18 traps; 4 controls; 11 P0)"); return 0
    if not args.responses_dir: ap.error("--responses-dir required unless --inventory-only")
    results = []
    for fixture_id, truth in sorted(inventory.items()):
        path = args.responses_dir / f"{fixture_id}.response.json"
        results.append(score_response_path(truth, path))
    report = {"scorer": "formal-rigor-v2-structural@1", "results": results,
              "passed": sum(r["structural_pass"] for r in results), "total": len(results)}
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out: args.out.write_text(text, encoding="utf-8", newline="\n")
    else: print(text, end="")
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
