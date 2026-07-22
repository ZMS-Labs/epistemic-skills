#!/usr/bin/env python3
"""Validate an epistemic-process-trace@1 record.

This is a deterministic protocol checker, not a JSON Schema implementation and
not a behavioral effectiveness measurement. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

TRACE_CONST = "epistemic-process-trace@1"
STAKE_VOCAB = {"low", "standard", "high"}
MOMENT_VOCAB = {"recon", "decision", "goal", "verification", "correction", "resumption"}
KIND_VOCAB = {"observation", "interpretation", "prediction", "value", "authorization"}
STATUS_VOCAB = {"verified", "contradicted", "unverified", "not-applicable"}
CONTROL_VOCAB = {"act", "hold", "escalate", "reversible-probe"}
FAILURE_CHAIN_FIELDS = {
    "prompting_event",
    "vulnerabilities",
    "links",
    "target_failure",
    "consequences",
    "earliest_interruptible_link",
    "replacement_behavior",
    "rehearsal_fixture",
}
GOAL_FIELDS = {"authorized_priority", "success_proxy", "proxy_failure", "acceptable_cost"}
EXPERIMENT_FIELDS = {
    "belief",
    "prediction",
    "disconfirming_observation",
    "test",
    "prediction_recorded_before_result",
}


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty_string(v) for v in value)


def validate_trace(trace: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(trace, dict):
        return ["root must be an object"]

    if trace.get("trace") != TRACE_CONST:
        errors.append(f"trace must equal {TRACE_CONST!r}")
    if not nonempty_string(trace.get("subject")):
        errors.append("subject must be a non-empty string")
    stakes = trace.get("stakes")
    if stakes not in STAKE_VOCAB:
        errors.append(f"stakes must be one of {sorted(STAKE_VOCAB)}")
    moment = trace.get("moment")
    if moment not in MOMENT_VOCAB:
        errors.append(f"moment must be one of {sorted(MOMENT_VOCAB)}")
    control = trace.get("control")
    if control not in CONTROL_VOCAB:
        errors.append(f"control must be one of {sorted(CONTROL_VOCAB)}")
    if not nonempty_string(trace.get("control_reason")):
        errors.append("control_reason must be a non-empty string")

    claims = trace.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty array")
        claims = []

    seen_ids: set[str] = set()
    load_bearing_unverified = False
    for index, claim in enumerate(claims):
        prefix = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{prefix} must be an object")
            continue
        cid = claim.get("id")
        if not nonempty_string(cid):
            errors.append(f"{prefix}.id must be a non-empty string")
        elif cid in seen_ids:
            errors.append(f"{prefix}.id duplicates {cid!r}")
        else:
            seen_ids.add(cid)
        kind = claim.get("kind")
        if kind not in KIND_VOCAB:
            errors.append(f"{prefix}.kind must be one of {sorted(KIND_VOCAB)}")
        status = claim.get("status")
        if status not in STATUS_VOCAB:
            errors.append(f"{prefix}.status must be one of {sorted(STATUS_VOCAB)}")
        if not nonempty_string(claim.get("text")):
            errors.append(f"{prefix}.text must be a non-empty string")
        confidence = claim.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not (0 <= confidence <= 1):
            errors.append(f"{prefix}.confidence must be a number in [0, 1]")
        if kind in {"observation", "authorization", "value"} and not nonempty_string(claim.get("source")):
            errors.append(f"{prefix}.source is required for {kind}")
        if kind == "prediction" and not nonempty_string(claim.get("disconfirming_observation")):
            errors.append(f"{prefix}.disconfirming_observation is required for prediction")
        if claim.get("load_bearing") is not None and not isinstance(claim.get("load_bearing"), bool):
            errors.append(f"{prefix}.load_bearing must be boolean when present")
        if claim.get("load_bearing") is True and status == "unverified":
            load_bearing_unverified = True

    if stakes in {"standard", "high"} and load_bearing_unverified and control == "act":
        errors.append("standard/high-stakes trace cannot act on a load-bearing unverified claim")

    goal = trace.get("goal")
    if goal is not None:
        if not isinstance(goal, dict):
            errors.append("goal must be an object when present")
        else:
            missing = sorted(field for field in GOAL_FIELDS if not nonempty_string(goal.get(field)))
            if missing:
                errors.append(f"goal missing non-empty fields: {', '.join(missing)}")

    experiment = trace.get("experiment")
    if experiment is not None:
        if not isinstance(experiment, dict):
            errors.append("experiment must be an object when present")
        else:
            missing = sorted(
                field for field in EXPERIMENT_FIELDS
                if field != "prediction_recorded_before_result" and not nonempty_string(experiment.get(field))
            )
            if missing:
                errors.append(f"experiment missing non-empty fields: {', '.join(missing)}")
            prereg = experiment.get("prediction_recorded_before_result")
            if not isinstance(prereg, bool):
                errors.append("experiment.prediction_recorded_before_result must be boolean")
            has_result = "result" in experiment
            if has_result:
                if not nonempty_string(experiment.get("result")):
                    errors.append("experiment.result must be a non-empty string when present")
                if prereg is not True:
                    errors.append("experiment result requires prediction_recorded_before_result=true")
                if not nonempty_string(experiment.get("update")):
                    errors.append("experiment.update is required when result is present")

    recurrence_risk = trace.get("recurrence_risk", False)
    if not isinstance(recurrence_risk, bool):
        errors.append("recurrence_risk must be boolean when present")
        recurrence_risk = False
    failure_chain = trace.get("failure_chain")
    if moment == "correction" and recurrence_risk and failure_chain is None:
        errors.append("recurrent correction requires failure_chain")
    if failure_chain is not None:
        if moment != "correction":
            errors.append("failure_chain is only valid for moment='correction'")
        if not isinstance(failure_chain, dict):
            errors.append("failure_chain must be an object when present")
        else:
            for field in sorted(FAILURE_CHAIN_FIELDS):
                value = failure_chain.get(field)
                if field in {"vulnerabilities", "links"}:
                    if not nonempty_string_list(value):
                        errors.append(f"failure_chain.{field} must be a non-empty string array")
                elif not nonempty_string(value):
                    errors.append(f"failure_chain.{field} must be a non-empty string")

    residual = trace.get("residual_uncertainty", [])
    if not isinstance(residual, list) or not all(nonempty_string(v) for v in residual):
        errors.append("residual_uncertainty must be an array of non-empty strings")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        trace = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_trace(trace)
    payload = {"path": str(args.path), "valid": not errors, "errors": errors}
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif errors:
        print(f"FAIL: {args.path}")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"PASS: {args.path}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
