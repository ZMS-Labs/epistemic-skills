#!/usr/bin/env python3
"""Deterministically score an epistemic-process trace against a behavioral fixture.

This scorer checks observable control decisions and required artifact use. It is a
fixture smoke test, not evidence that the controls improve real-world performance.
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
sys.path.insert(0, str(PARENT))
from validate_trace import validate_trace  # noqa: E402


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def get_path(root: Any, dotted: str) -> Any:
    current = root
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def claim_matches(claim: Any, rule: dict[str, Any]) -> bool:
    if not isinstance(claim, dict):
        return False
    for key in ("kind", "status", "load_bearing"):
        if key in rule and claim.get(key) != rule[key]:
            return False
    if "source_contains" in rule:
        source = claim.get("source")
        if not nonempty(source) or rule["source_contains"].lower() not in source.lower():
            return False
    if "text_contains" in rule:
        text = claim.get("text")
        if not nonempty(text) or rule["text_contains"].lower() not in text.lower():
            return False
    return True


def score(fixture: Any, trace: Any) -> list[str]:
    errors = validate_trace(trace)
    if not isinstance(fixture, dict):
        return ["fixture root must be an object"] + errors

    fixture_id = fixture.get("id")
    if not nonempty(fixture_id):
        errors.append("fixture.id must be non-empty")
    if trace.get("scenario") != fixture_id:
        errors.append(f"trace.scenario must equal {fixture_id!r}")

    expected = fixture.get("expected")
    if not isinstance(expected, dict):
        errors.append("fixture.expected must be an object")
        return errors

    allowed_controls = expected.get("allowed_controls", [])
    if trace.get("control") not in allowed_controls:
        errors.append(
            f"control {trace.get('control')!r} not in allowed controls {allowed_controls!r}"
        )

    action = trace.get("action", "")
    if not nonempty(action):
        errors.append("trace.action must be a non-empty string")
    else:
        lower_action = action.lower()
        for phrase in expected.get("forbidden_action_phrases", []):
            if phrase.lower() in lower_action:
                errors.append(f"action contains forbidden phrase {phrase!r}")
        required_action_any = expected.get("required_action_any", [])
        if required_action_any and not any(p.lower() in lower_action for p in required_action_any):
            errors.append(f"action must contain one of {required_action_any!r}")

    claims = trace.get("claims", [])
    for index, rule in enumerate(expected.get("required_claims", [])):
        if not any(claim_matches(claim, rule) for claim in claims):
            errors.append(f"required_claims[{index}] not satisfied: {rule!r}")

    for dotted in expected.get("required_paths", []):
        value = get_path(trace, dotted)
        if value is None or value == "" or value == []:
            errors.append(f"required path {dotted!r} is missing or empty")

    for dotted, phrases in expected.get("path_contains_any", {}).items():
        value = get_path(trace, dotted)
        if not nonempty(value) or not any(p.lower() in value.lower() for p in phrases):
            errors.append(f"path {dotted!r} must contain one of {phrases!r}")

    for dotted, phrases in expected.get("path_forbids", {}).items():
        value = get_path(trace, dotted)
        if nonempty(value):
            for phrase in phrases:
                if phrase.lower() in value.lower():
                    errors.append(f"path {dotted!r} contains forbidden phrase {phrase!r}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    try:
        fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
        trace = json.loads(args.trace.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = score(fixture, trace)
    payload = {
        "fixture": str(args.fixture),
        "trace": str(args.trace),
        "pass": not errors,
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif errors:
        print(f"FAIL: {args.trace}")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"PASS: {args.trace}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
