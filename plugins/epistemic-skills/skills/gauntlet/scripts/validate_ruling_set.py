#!/usr/bin/env python3
"""Validate ruling-set@1 arbitration structure that affects epistemic integrity.

This narrow stdlib gate gives the Gauntlet's ``validation_kernel`` rule
mechanical teeth: every OVERRULED criticism must preserve, in a non-empty field,
what the criticism validly established before the arbitrator rejected its final
conclusion.  The check is structural only; it does not judge whether the kernel
is true or adequate.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "example-run" / "arbitration.md"
FENCED_JSON_RE = re.compile(r"```json\s*(.*?)```", re.S)


class RulingSetError(ValueError):
    pass


def extract_ruling_set(text: str) -> dict[str, Any]:
    for block in FENCED_JSON_RE.findall(text):
        try:
            value = json.loads(block)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("ruling_set") == "ruling-set@1":
            return value
    raise RulingSetError("RULING-SET-MISSING: no fenced ruling-set@1 JSON block")


def validate_ruling_set(value: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["RULING-SET-TYPE: root must be an object"]
    if value.get("ruling_set") != "ruling-set@1":
        errors.append("RULING-SET-KIND: ruling_set must equal ruling-set@1")
    rulings = value.get("rulings")
    if not isinstance(rulings, list):
        return [*errors, "RULINGS-TYPE: rulings must be an array"]

    seen_ids: set[str] = set()
    for index, ruling in enumerate(rulings):
        prefix = f"rulings[{index}]"
        if not isinstance(ruling, dict):
            errors.append(f"{prefix}: ruling must be an object")
            continue
        ruling_id = ruling.get("id")
        if not isinstance(ruling_id, str) or not ruling_id.strip():
            errors.append(f"{prefix}: id must be a non-empty string")
            ruling_id = f"index-{index}"
        elif ruling_id in seen_ids:
            errors.append(f"{prefix}: duplicate ruling id {ruling_id}")
        seen_ids.add(ruling_id)

        if ruling.get("ruling") == "OVERRULED":
            kernel = ruling.get("validation_kernel")
            if not isinstance(kernel, str) or not kernel.strip():
                errors.append(f"VALIDATION-KERNEL-MISSING:{ruling_id}")
    return errors


def validate_path(path: Path) -> list[str]:
    try:
        ruling_set = extract_ruling_set(path.read_text(encoding="utf-8"))
    except (OSError, RulingSetError) as error:
        return [str(error)]
    return validate_ruling_set(ruling_set)


def self_test() -> int:
    failures = 0
    positive = validate_path(EXAMPLE)
    if positive:
        failures += 1
        print(f"[FAIL] shipped example: {positive}")
    else:
        print("[PASS] shipped example preserves validation kernels")

    value = extract_ruling_set(EXAMPLE.read_text(encoding="utf-8"))
    planted = json.loads(json.dumps(value))
    for ruling in planted["rulings"]:
        if ruling.get("ruling") == "OVERRULED":
            ruling.pop("validation_kernel", None)
    negative = validate_ruling_set(planted)
    if not any(error.startswith("VALIDATION-KERNEL-MISSING:") for error in negative):
        failures += 1
        print(f"[FAIL] planted missing kernel was not rejected: {negative}")
    else:
        print("[PASS] planted missing kernel fails closed")

    print(f"validate_ruling_set self-test: {'PASS' if failures == 0 else 'FAIL'}")
    return 0 if failures == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--arbitration", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if args.arbitration is None:
        print("ERROR: --arbitration or --self-test is required", file=sys.stderr)
        return 2

    errors = validate_path(args.arbitration)
    for error in errors:
        print(f"[FAIL] {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"[PASS] {args.arbitration}: all overruled criticisms preserve validation_kernel")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
