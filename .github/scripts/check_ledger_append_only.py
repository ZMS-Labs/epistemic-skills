#!/usr/bin/env python3
"""Reject any rewrite of the durable decision ledger — committed lines are append-only.

The decision-ledger contract defines .ledger/entries.jsonl as an append-only
store: an amendment is a new entry with a supersedes link, never an edit of an
existing line. The structural validator (validate_examples.py) checks the
store's graph invariants but is snapshot-only: a PR that rewrites or deletes an
existing entry while keeping the graph valid passes it. This check closes that
gap by requiring the base revision's bytes to survive as an exact prefix of the
proposed file.

Usage:
  check_ledger_append_only.py --base BASE_FILE --current CURRENT_FILE
  check_ledger_append_only.py --self-test

BASE_FILE is a materialized copy of .ledger/entries.jsonl at the merge base
(empty file when the ledger did not exist there). Exit 0 when current begins
with base byte-for-byte; exit 1 with a named reason otherwise. Fail closed: the
caller must fail the run when the base cannot be established, not skip.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path


def check(base: bytes, current: bytes) -> str | None:
    """Return a failure reason, or None when current is an append-only extension."""
    if len(current) < len(base):
        return "LEDGER-TRUNCATED: proposed store is shorter than the merge base"
    if current[: len(base)] != base:
        for i, (a, b) in enumerate(zip(base, current)):
            if a != b:
                line = base[:i].count(b"\n") + 1
                return (
                    f"LEDGER-REWRITTEN: byte {i} (line {line}) differs from the merge "
                    "base — existing entries are append-only; amend via a new entry "
                    "with a supersedes link"
                )
        return "LEDGER-REWRITTEN: base bytes are not a prefix of the proposed store"
    appended = current[len(base):]
    if base and appended and not base.endswith(b"\n"):
        return (
            "LEDGER-REWRITTEN: appended content extends the base's final line "
            "(base does not end with a newline)"
        )
    return None


def self_test() -> None:
    base = b'{"id":"a-1"}\n{"id":"b-2"}\n'
    cases = [
        ("append", base, base + b'{"id":"c-3"}\n', None),
        ("no-op", base, base, None),
        ("born", b"", b'{"id":"a-1"}\n', None),
        ("rewrite", base, b'{"id":"a-9"}\n{"id":"b-2"}\n', "LEDGER-REWRITTEN"),
        ("delete", base, b'{"id":"a-1"}\n', "LEDGER-TRUNCATED"),
        ("insert", base, b'{"id":"x-0"}\n' + base, "LEDGER-REWRITTEN"),
    ]
    for name, b, c, expected in cases:
        reason = check(b, c)
        code = None if reason is None else reason.split(":", 1)[0]
        assert code == expected, f"{name}: expected {expected}, got {reason}"
    print(f"ledger append-only self-test: PASS ({len(cases)}/{len(cases)})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path)
    parser.add_argument("--current", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.base or not args.current:
        parser.error("provide --base and --current, or --self-test")
    try:
        base = args.base.read_bytes()
        current = args.current.read_bytes()
    except OSError as exc:
        print(f"error LEDGER-CHECK-UNREADABLE: {exc}", file=sys.stderr)
        return 1
    reason = check(base, current)
    if reason:
        print(f"error {reason}", file=sys.stderr)
        return 1
    added = current[len(base):].count(b"\n")
    print(f"ok ledger append-only: {added} line(s) appended over the merge base")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
