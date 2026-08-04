#!/usr/bin/env python3
"""Stdlib structural validator for formal-rigor-record@2.

This validates the envelope and cross-field invariants. It never attests that
the derivations are true.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FAMILIES = {f"P{i}" for i in range(1, 10)}
TIERS = {"standard", "high-assurance"}
COVERAGE_STATES = {"fired", "not-applicable", "unmapped"}
RESULT_STATES = {"established", "refuted", "conditional", "incomplete"}
OUTCOMES = {"dominance", "pareto-set", "conditional", "underdetermined", "reversal", "reversible-probe"}
REQUIRED_NEVER_ATTESTS = {
    "derivation-correctness-by-envelope",
    "empirical-fact-without-observation",
    "gauntlet-independence",
}


def _mapping(value: Any, path: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected object")
        return {}
    return value


def _list(value: Any, path: str, errors: list[str]) -> list:
    if not isinstance(value, list):
        errors.append(f"{path}: expected array")
        return []
    return value


def _required(obj: dict, fields: set[str], path: str, errors: list[str]) -> None:
    for field in sorted(fields - set(obj)):
        errors.append(f"{path}.{field}: missing")


def validate_record(value: Any) -> list[str]:
    errors: list[str] = []
    record = _mapping(value, "$", errors)
    if not record:
        return errors
    if record.get("record") != "formal-rigor-record@2":
        errors.append("$.record: expected formal-rigor-record@2")
    _required(record, {
        "record", "subject", "valid_while", "coverage_limits", "rigor",
        "decision_frame", "coverage", "derivations", "empirical_closure",
        "synthesis", "never_attests",
    }, "$", errors)

    subject = _mapping(record.get("subject"), "$.subject", errors)
    _required(subject, {"ref", "revision"}, "$.subject", errors)
    if not isinstance(subject.get("ref"), str) or not subject.get("ref"):
        errors.append("$.subject.ref: expected non-empty string")
    revision = subject.get("revision")
    if revision is not None and (not isinstance(revision, str) or not revision):
        errors.append("$.subject.revision: expected non-empty string or null")
    valid_while = _list(record.get("valid_while"), "$.valid_while", errors)
    if revision is None and "subject-revision-unchanged" in valid_while:
        errors.append("$.valid_while: null revision cannot claim subject-revision-unchanged")
    if revision is not None and "subject-revision-unchanged" not in valid_while:
        errors.append("$.valid_while: pinned revision requires subject-revision-unchanged")
    coverage_limits = _list(record.get("coverage_limits"), "$.coverage_limits", errors)
    if revision is None and not coverage_limits:
        errors.append("$.coverage_limits: null revision requires an explicit freshness limit")

    rigor = _mapping(record.get("rigor"), "$.rigor", errors)
    _required(rigor, {"tier", "trigger", "tier_reason"}, "$.rigor", errors)
    if rigor.get("tier") not in TIERS:
        errors.append("$.rigor.tier: expected standard or high-assurance")
    for field in ("trigger", "tier_reason"):
        if not isinstance(rigor.get(field), str) or not rigor.get(field):
            errors.append(f"$.rigor.{field}: expected non-empty string")

    frame = _mapping(record.get("decision_frame"), "$.decision_frame", errors)
    _required(frame, {
        "question", "system_boundary", "actors", "alternatives",
        "hard_constraints", "authorized_objectives", "priority_rule",
        "assumptions", "empirical_premises", "uncertainty_posture",
    }, "$.decision_frame", errors)
    alternatives = _list(frame.get("alternatives"), "$.decision_frame.alternatives", errors)
    valid_alternatives = [item for item in alternatives if isinstance(item, dict)]
    if len(valid_alternatives) != len(alternatives):
        errors.append("$.decision_frame.alternatives: every item must be an object")
    if not valid_alternatives:
        errors.append("$.decision_frame.alternatives: at least one option is required")
    null_count = len([item for item in valid_alternatives if item.get("kind") == "null-option"])
    if len(valid_alternatives) > 1 and null_count != 1:
        errors.append("$.decision_frame.alternatives: a decision fork requires exactly one null-option")
    if len(valid_alternatives) == 1 and null_count:
        errors.append("$.decision_frame.alternatives: single-option justification must name the proposed option")
    priority = _mapping(frame.get("priority_rule"), "$.decision_frame.priority_rule", errors)
    if not priority.get("kind") or not priority.get("authority_ref"):
        errors.append("$.decision_frame.priority_rule: kind and authority_ref are required")

    coverage = _list(record.get("coverage"), "$.coverage", errors)
    rows = [row for row in coverage if isinstance(row, dict)]
    families = [row.get("family") for row in rows]
    if len(rows) != 9 or set(families) != FAMILIES or len(families) != len(set(families)):
        errors.append("$.coverage: expected exactly one row for each P1-P9")
    unmapped_families: list[str] = []
    for index, row in enumerate(rows):
        path = f"$.coverage[{index}]"
        _required(row, {"family", "status", "modules", "reason"}, path, errors)
        status = row.get("status")
        modules = _list(row.get("modules"), f"{path}.modules", errors)
        if status not in COVERAGE_STATES:
            errors.append(f"{path}.status: invalid coverage state")
        if status == "fired" and not modules:
            errors.append(f"{path}.modules: fired family requires a module")
        if status != "fired" and modules:
            errors.append(f"{path}.modules: non-fired family cannot name modules")
        if not isinstance(row.get("reason"), str) or not row.get("reason"):
            errors.append(f"{path}.reason: expected non-empty string")
        if status == "unmapped" and isinstance(row.get("family"), str):
            unmapped_families.append(row["family"])
    for family in unmapped_families:
        if not any(family in str(limit) for limit in coverage_limits):
            errors.append(f"$.coverage_limits: unmapped {family} requires a named limit")

    derivations = _list(record.get("derivations"), "$.derivations", errors)
    for index, item in enumerate(derivations):
        path = f"$.derivations[{index}]"
        derivation = _mapping(item, path, errors)
        _required(derivation, {
            "id", "module", "construct", "sources", "model", "preconditions",
            "fact_mapping", "steps", "result", "counterexample",
            "residual_mismatch",
        }, path, errors)
        if not _list(derivation.get("preconditions"), f"{path}.preconditions", errors):
            errors.append(f"{path}.preconditions: at least one is required")
        if not _list(derivation.get("fact_mapping"), f"{path}.fact_mapping", errors):
            errors.append(f"{path}.fact_mapping: at least one is required")
        result = _mapping(derivation.get("result"), f"{path}.result", errors)
        if result.get("state") not in RESULT_STATES or not result.get("statement"):
            errors.append(f"{path}.result: valid state and statement are required")
        sources = _mapping(derivation.get("sources"), f"{path}.sources", errors)
        _required(sources, {"primary_theory", "official_product_docs"}, f"{path}.sources", errors)

    empirical = _mapping(record.get("empirical_closure"), "$.empirical_closure", errors)
    if empirical.get("state") not in {"not-required", "pending", "observed", "post-hoc-weaker", "blocked"}:
        errors.append("$.empirical_closure.state: invalid state")
    _list(empirical.get("tests"), "$.empirical_closure.tests", errors)

    synthesis = _mapping(record.get("synthesis"), "$.synthesis", errors)
    _required(synthesis, {"outcome", "selected_option", "basis", "conditions", "concessions", "recovery_moves"}, "$.synthesis", errors)
    outcome = synthesis.get("outcome")
    if outcome not in OUTCOMES:
        errors.append("$.synthesis.outcome: invalid outcome")
    if outcome in {"pareto-set", "underdetermined"} and synthesis.get("selected_option") is not None:
        errors.append("$.synthesis.selected_option: pareto-set and underdetermined select no option")
    if unmapped_families and outcome == "dominance":
        errors.append("$.synthesis.outcome: dominance forbidden with unmapped terrain")

    never_attests = set(_list(record.get("never_attests"), "$.never_attests", errors))
    if not REQUIRED_NEVER_ATTESTS <= never_attests:
        errors.append("$.never_attests: required non-attestation boundaries missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errors = validate_record(value)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("formal-rigor-record@2: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
