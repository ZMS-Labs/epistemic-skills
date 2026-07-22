#!/usr/bin/env python3
"""Validate an epistemic-process-trace@1 record.

This is a deterministic protocol checker, not a JSON Schema implementation and
not a behavioral effectiveness measurement. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TRACE_CONST = "epistemic-process-trace@1"
STAKE_VOCAB = {"low", "standard", "high"}
MOMENT_VOCAB = {"recon", "decision", "goal", "verification", "correction", "resumption"}
KIND_VOCAB = {"observation", "interpretation", "prediction", "value", "authorization"}
STATUS_VOCAB = {"verified", "contradicted", "unverified", "not-applicable"}
CONTROL_VOCAB = {"act", "hold", "escalate", "reversible-probe"}

# --- Control/action consistency (fail-closed teeth for C2/C5) ---------------
# PRIMARY enforcement is STRUCTURAL, not text-parsing: the trace must DECLARE
# `action_executes` (bool). A non-acting control (`hold`/`escalate`) whose action
# is declared to execute is rejected. This is paraphrase-proof — it does not try to
# read the action's English (a keyword matcher cannot; a 2026-07-22 cross-family
# Step-7b review measured a 100% false-negative rate on paraphrases). The text
# matcher below is retained ONLY as a SECONDARY mis-declaration lint: if the action
# is declared non-executing yet its text carries a blatant execution imperative, the
# declaration is likely inaccurate and is flagged. The guarantee rests on the
# declared boolean; the lint is best-effort and explicitly NOT complete.
NON_ACTING_CONTROLS = {"hold", "escalate"}
# Blatant execution imperatives — the lint catches obvious mis-declarations, not every
# paraphrase (see adversarial_paraphrase_battery.py). A hold action that merely mentions
# an execution noun ("handoff claims 'release merged'", "halt the deployment") must NOT
# trip it — only a directive that tells the system to execute.
_EXEC_DIRECTIVES = (
    "proceed with", "go ahead with", "go ahead and",
    "deploy now", "deploy it", "start deployment", "start the deployment",
    "run the deployment", "continue deployment", "continue the deployment",
    "publish now", "publish the release", "publish it",
    "merge now", "merge the release", "merge it", "merge to",
    "ship it", "ship now", "release it to",
    "execute now", "execute the", "roll it out", "roll out now", "go live",
    "apply the change now", "overwrite the", "delete the", "drop the",
)
# Negation/deferral in a directive's local clause neutralizes it: "do not proceed
# with", "before you merge the release", etc.
_NEUTRALIZERS = (
    "not ", "n't", "never", "avoid", "refrain from", "without", "hold off", "instead of",
    "rather than", "do not", "don't", "cannot", "must not", "should not",
    "before", "until", "after ", "pending", "once ", "unless",
    "halt", "stop", "block", "abort", "cancel", "prevent", "postpone", "suspend", "defer",
    "reject", "decline", "deny", "refuse", "do NOT".lower(),
)


def action_asserts_execution(action: str) -> str | None:
    """Return the affirmative execution directive an `action` asserts, or None.

    Only unambiguous imperatives count; a directive is neutralized when a negation,
    deferral, or stop verb appears in its local clause. So "halt the deployment" and
    "do not proceed with the merge; verify first" do NOT assert execution, while
    "proceed with the deployment now" and "merge the release to production" do.
    """
    text = action.lower()
    for directive in _EXEC_DIRECTIVES:
        pos = text.find(directive)
        while pos != -1:
            clause = text[max(0, pos - 30): pos + len(directive) + 5]
            if not any(marker in clause for marker in _NEUTRALIZERS):
                return directive
            pos = text.find(directive, pos + len(directive))
    return None


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

    action = trace.get("action")
    if action is not None and not nonempty_string(action):
        errors.append("action must be a non-empty string when present")

    # Control/action consistency. PRIMARY = the declared `action_executes` boolean
    # (paraphrase-proof); SECONDARY = a best-effort mis-declaration lint on the text.
    action_executes = trace.get("action_executes")
    if action_executes is not None and not isinstance(action_executes, bool):
        errors.append("action_executes must be a boolean when present")
        action_executes = None
    if control in NON_ACTING_CONTROLS:
        # A non-acting control MUST declare that its action does not execute.
        if action_executes is None:
            errors.append(
                f"control {control!r} requires action_executes to be declared (boolean); "
                "a non-acting control must prove it does not execute (fail-closed)"
            )
        elif action_executes is True:
            errors.append(
                f"control {control!r} is contradicted by action_executes=true; a non-acting "
                "control must not execute (control/action consistency — fail-closed)"
            )
    # Secondary lint (best-effort, NOT complete): if declared non-executing but the text
    # carries a blatant execution imperative, the declaration is probably inaccurate.
    if action_executes is False and nonempty_string(action):
        blatant = action_asserts_execution(action)
        if blatant:
            errors.append(
                f"action_executes=false but the action text asserts execution ({blatant!r}); "
                "the declaration appears inaccurate (mis-declaration lint — not exhaustive)"
            )

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
