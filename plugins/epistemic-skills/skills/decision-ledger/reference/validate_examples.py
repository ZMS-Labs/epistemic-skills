#!/usr/bin/env python3
"""Stdlib validator for ledger-entry@1 examples and durable JSONL stores.

The implementation mirrors the repository's closed ``ledger-entry.schema.json``
contract without introducing a runtime dependency on a general JSON Schema
library.  It also checks the store-level invariants the schema cannot express:
unique ids, durable-only committed entries, non-dangling supersedes links,
acyclic supersession, and one head per connected supersession component.

This is structural validation only.  It makes no truth, authorization, or
freshness claim about a well-formed entry.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[4]
DEFAULT_LEDGER = REPO_ROOT / ".ledger" / "entries.jsonl"

REQUIRED = {
    "entry",
    "id",
    "at",
    "type",
    "statement",
    "because",
    "supersedes",
    "revisit_when",
    "durability",
}
OPTIONAL = {"synthetic", "session", "recurrence_risk", "failure_chain"}
ALLOWED = REQUIRED | OPTIONAL
CHAIN_REQUIRED = {
    "prompting_event",
    "vulnerabilities",
    "links",
    "target_failure",
    "consequences",
    "earliest_interruptible_link",
    "replacement_behavior",
    "rehearsal_fixture",
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*-[0-9]{8}-[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(item) for item in value)


def validate(entry: Any) -> list[str]:
    """Validate one entry against the closed ledger-entry@1 shape."""

    errors: list[str] = []
    if not isinstance(entry, dict):
        return ["root must be an object"]

    missing = sorted(REQUIRED - entry.keys())
    unknown = sorted(entry.keys() - ALLOWED)
    if missing:
        errors.append(f"missing required fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"additional properties are forbidden: {', '.join(unknown)}")

    if entry.get("entry") != "ledger-entry@1":
        errors.append("entry must equal ledger-entry@1")

    identifier = entry.get("id")
    if not isinstance(identifier, str) or ID_RE.fullmatch(identifier) is None:
        errors.append("id must match <slug>-<YYYYMMDD>-<seq>")

    at = entry.get("at")
    if not isinstance(at, str) or DATE_RE.fullmatch(at) is None:
        errors.append("at must match YYYY-MM-DD")

    if "synthetic" in entry and not isinstance(entry.get("synthetic"), bool):
        errors.append("synthetic must be boolean")
    if "session" in entry and not nonempty(entry.get("session")):
        errors.append("session must be a non-empty string")

    if entry.get("type") not in {"decision", "assumption", "correction"}:
        errors.append("invalid type")
    for field in ("statement", "because", "revisit_when"):
        if not nonempty(entry.get(field)):
            errors.append(f"{field} must be a non-empty string")

    supersedes = entry.get("supersedes")
    if not isinstance(supersedes, list) or not all(
        isinstance(item, str) and ID_RE.fullmatch(item) is not None for item in supersedes
    ):
        errors.append("supersedes must be an array of ledger-entry ids")

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
            unknown_chain = sorted(chain.keys() - CHAIN_REQUIRED)
            if missing_chain:
                errors.append(f"failure_chain missing: {', '.join(missing_chain)}")
            if unknown_chain:
                errors.append(
                    "failure_chain additional properties are forbidden: "
                    + ", ".join(unknown_chain)
                )
            for field in sorted(CHAIN_REQUIRED):
                value = chain.get(field)
                if field in {"vulnerabilities", "links"}:
                    if not nonempty_list(value):
                        errors.append(
                            f"failure_chain.{field} must be a non-empty string array"
                        )
                elif not nonempty(value):
                    errors.append(f"failure_chain.{field} must be a non-empty string")
    return errors


def validate_store(entries: list[dict[str, Any]]) -> list[str]:
    """Validate invariants spanning a committed append-only JSONL store."""

    errors: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries, 1):
        identifier = entry.get("id")
        if not isinstance(identifier, str):
            continue
        if identifier in by_id:
            errors.append(f"line {index}: duplicate id {identifier}")
        else:
            by_id[identifier] = entry
        if entry.get("durability") == "session-only":
            errors.append(
                f"line {index}: session-only entry {identifier} may not be committed to the durable store"
            )

    graph: dict[str, list[str]] = {}
    undirected: dict[str, set[str]] = {identifier: set() for identifier in by_id}
    for identifier, entry in by_id.items():
        parents = [item for item in entry.get("supersedes", []) if isinstance(item, str)]
        graph[identifier] = parents
        for parent in parents:
            if parent not in by_id:
                errors.append(f"{identifier}: dangling supersedes id {parent}")
                continue
            undirected[identifier].add(parent)
            undirected[parent].add(identifier)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(identifier: str, trail: list[str]) -> None:
        if identifier in visiting:
            cycle = " -> ".join([*trail, identifier])
            errors.append(f"supersedes cycle: {cycle}")
            return
        if identifier in visited:
            return
        visiting.add(identifier)
        for parent in graph.get(identifier, []):
            if parent in by_id:
                visit(parent, [*trail, identifier])
        visiting.remove(identifier)
        visited.add(identifier)

    for identifier in sorted(by_id):
        visit(identifier, [])

    superseded = {
        parent
        for parents in graph.values()
        for parent in parents
        if parent in by_id
    }
    component_seen: set[str] = set()
    for start in sorted(by_id):
        if start in component_seen:
            continue
        stack = [start]
        component: set[str] = set()
        while stack:
            current = stack.pop()
            if current in component:
                continue
            component.add(current)
            stack.extend(undirected.get(current, set()) - component)
        component_seen |= component
        heads = sorted(component - superseded)
        if len(heads) != 1:
            errors.append(
                f"supersedes component {sorted(component)} must have exactly one head; got {heads}"
            )
    return errors


def read_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw_line.strip():
            continue
        try:
            value = json.loads(raw_line)
        except json.JSONDecodeError as error:
            errors.append(f"line {line_number}: malformed JSON: {error.msg}")
            continue
        entry_errors = validate(value)
        if entry_errors:
            errors.extend(f"line {line_number}: {error}" for error in entry_errors)
            continue
        entries.append(value)
    errors.extend(validate_store(entries))
    return entries, errors


def check_examples() -> int:
    failures = 0
    for path in sorted(ROOT.glob("example-*.json")):
        errors = validate(json.loads(path.read_text(encoding="utf-8")))
        print(
            f"[{'PASS' if not errors else 'FAIL'}] {path.name}: "
            f"{'; '.join(errors) if errors else 'valid'}"
        )
        failures += bool(errors)

    base = json.loads((ROOT / "example-correction-with-chain.json").read_text(encoding="utf-8"))
    planted = {
        "recurrent correction without chain": {
            key: value for key, value in base.items() if key != "failure_chain"
        },
        "chain on decision": {**base, "type": "decision"},
        "unknown property": {**base, "verdict": "GO"},
        "bad id": {**base, "id": "not-an-entry-id"},
    }
    for name, payload in planted.items():
        errors = validate(payload)
        passed = bool(errors)
        print(
            f"[{'PASS' if passed else 'FAIL'}] planted {name}: "
            f"{'; '.join(errors) if errors else 'unexpectedly valid'}"
        )
        failures += not passed
    return failures


def check_ledger(path: Path) -> int:
    if not path.is_file():
        # Portability note (gauntlet R12): a copied plugin tree outside the
        # repository has no durable store at the derived default path. Failing
        # is still correct (store validation is the default on purpose), but
        # the message must say how to proceed, not just that a file is absent.
        print(
            f"[FAIL] durable ledger: no store at {path} — this checkout has no "
            "durable ledger at the default location; pass --ledger <path> to "
            "validate a store elsewhere, or --examples-only to validate only "
            "the shipped examples"
        )
        return 1
    entries, errors = read_jsonl(path)
    print(
        f"[{'PASS' if not errors else 'FAIL'}] durable ledger {path}: "
        f"{len(entries)} valid entries"
    )
    for error in errors:
        print(f"  - {error}")
    return bool(errors)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ledger",
        type=Path,
        default=DEFAULT_LEDGER,
        help="durable JSONL store to validate (default: repository .ledger/entries.jsonl)",
    )
    parser.add_argument(
        "--examples-only",
        action="store_true",
        help="run fixture checks without validating a durable store",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    failures = check_examples()
    if not args.examples_only:
        failures += check_ledger(args.ledger)
    print(f"\nRESULT: {'PASS' if failures == 0 else 'FAIL'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
