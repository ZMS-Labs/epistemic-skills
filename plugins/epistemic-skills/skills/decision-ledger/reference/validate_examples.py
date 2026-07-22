#!/usr/bin/env python3
"""Stdlib smoke check for ledger-entry@1 examples and recurrent corrections.

This checks the narrow structural contract added for recurrent corrections. It is
not a general JSON Schema implementation and makes no truth/authorization claim.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REQUIRED = {
    "entry", "id", "at", "type", "statement", "because",
    "supersedes", "revisit_when", "durability",
}
CHAIN_REQUIRED = {
    "prompting_event", "vulnerabilities", "links", "target_failure",
    "consequences", "earliest_interruptible_link", "replacement_behavior",
    "rehearsal_fixture",
}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(item) for item in value)


def validate(entry: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(entry, dict):
        return ["root must be an object"]
    missing = sorted(REQUIRED - entry.keys())
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if entry.get("entry") != "ledger-entry@1":
        errors.append("entry must equal ledger-entry@1")
    if entry.get("type") not in {"decision", "assumption", "correction"}:
        errors.append("invalid type")
    if entry.get("durability") not in {"durable", "session-only"}:
        errors.append("invalid durability")
    recurrence = entry.get("recurrence_risk")
    chain = entry.get("failure_chain")
    if recurrence is not None and not isinstance(recurrence, bool):
        errors.append("recurrence_risk must be boolean")
    if recurrence is not None and entry.get("type") != "correction":
        errors.append("recurrence_risk is correction-only")
    if chain is not None and entry.get("type") != "correction":
        errors.append("failure_chain is correction-only")
    if recurrence is True and chain is None:
        errors.append("recurrent correction requires failure_chain")
    if chain is not None:
        if not isinstance(chain, dict):
            errors.append("failure_chain must be an object")
        else:
            missing_chain = sorted(CHAIN_REQUIRED - chain.keys())
            if missing_chain:
                errors.append(f"failure_chain missing: {', '.join(missing_chain)}")
            for field in sorted(CHAIN_REQUIRED):
                value = chain.get(field)
                if field in {"vulnerabilities", "links"}:
                    if not nonempty_list(value):
                        errors.append(f"failure_chain.{field} must be a non-empty string array")
                elif not nonempty(value):
                    errors.append(f"failure_chain.{field} must be a non-empty string")
    return errors


def main() -> int:
    failures = 0
    for path in sorted(ROOT.glob("example-*.json")):
        errors = validate(json.loads(path.read_text(encoding="utf-8")))
        print(f"[{'PASS' if not errors else 'FAIL'}] {path.name}: {'; '.join(errors) if errors else 'valid'}")
        failures += bool(errors)

    base = json.loads((ROOT / "example-correction-with-chain.json").read_text(encoding="utf-8"))
    planted = {
        "recurrent correction without chain": {key: value for key, value in base.items() if key != "failure_chain"},
        "chain on decision": {**base, "type": "decision"},
    }
    for name, payload in planted.items():
        errors = validate(payload)
        passed = bool(errors)
        print(f"[{'PASS' if passed else 'FAIL'}] planted {name}: {'; '.join(errors) if errors else 'unexpectedly valid'}")
        failures += not passed

    print(f"\nRESULT: {'PASS' if failures == 0 else 'FAIL'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
