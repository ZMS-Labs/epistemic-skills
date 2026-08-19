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
  check_ledger_append_only.py --base-git-ref REF --current CURRENT_FILE
  check_ledger_append_only.py --self-test

BASE_FILE is a materialized copy of .ledger/entries.jsonl at the merge base
(empty file when the ledger did not exist there). --base-git-ref materializes
it from a git revision instead (R3-NF1's oracle gap: no surface ran this
check before ready-mark, so a byte-rewrite of published lines shipped inside
a sealed freeze and turned the freeze PR red on arrival; the pre-freeze
invocation is `git fetch origin main && check_ledger_append_only.py
--base-git-ref FETCH_HEAD --current .ledger/entries.jsonl`). An unresolvable
ref fails closed; a resolvable ref without the ledger file is an empty base
(the born case). Exit 0 when current begins with base byte-for-byte; exit 1
with a named reason otherwise. Fail closed: the caller must fail the run when
the base cannot be established, not skip.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

LEDGER_REL = ".ledger/entries.jsonl"


def base_from_ref(ref: str, cwd: Path | None = None) -> bytes:
    """Materialize the ledger bytes at REF. Raises SystemExit(1) when the ref
    cannot be resolved (fail closed); returns b"" when the ref resolves but
    the ledger does not exist there."""
    resolve = subprocess.run(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
        capture_output=True, text=True, cwd=cwd,
    )
    if resolve.returncode != 0:
        print(
            f"error LEDGER-BASE-UNRESOLVABLE: git ref {ref!r} does not "
            "resolve to a commit — failing closed, not skipping",
            file=sys.stderr,
        )
        raise SystemExit(1)
    show = subprocess.run(
        ["git", "show", f"{ref}:{LEDGER_REL}"],
        capture_output=True, cwd=cwd,
    )
    if show.returncode != 0:
        return b""
    return show.stdout


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
        # R3-NF1's literal defect class: parse-identical, byte-different —
        # the same entries re-dumped with spaced separators must FAIL.
        ("reserialize", base, b'{"id": "a-1"}\n{"id": "b-2"}\n', "LEDGER-REWRITTEN"),
    ]
    for name, b, c, expected in cases:
        reason = check(b, c)
        code = None if reason is None else reason.split(":", 1)[0]
        assert code == expected, f"{name}: expected {expected}, got {reason}"
    # --base-git-ref plumbing against a real scratch repository: resolvable
    # ref -> exact bytes; ref without the file -> empty base; bad ref ->
    # fail closed.
    import os

    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        # Identity values carry no '@' — the public-content gate bans the
        # email-address pattern class repo-wide, and git accepts any
        # explicitly-provided string here.
        env = {**os.environ,
               "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t",
               "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t"}

        def git(*args: str) -> None:
            subprocess.run(["git", *args], cwd=repo, env=env, check=True,
                           capture_output=True)

        git("init", "-q")
        git("commit", "-q", "--allow-empty", "-m", "empty")
        assert base_from_ref("HEAD", cwd=repo) == b"", "ref without ledger must be empty base"
        (repo / ".ledger").mkdir()
        (repo / LEDGER_REL).write_bytes(base)
        git("add", LEDGER_REL)
        git("commit", "-q", "-m", "ledger")
        assert base_from_ref("HEAD", cwd=repo) == base, "ref base must be byte-exact"
        try:
            base_from_ref("no-such-ref-xyz", cwd=repo)
        except SystemExit as exc:
            assert exc.code == 1, exc.code
        else:
            raise AssertionError("unresolvable ref did NOT fail closed")
    print(f"ledger append-only self-test: PASS ({len(cases)}/{len(cases)} byte cases + 3 ref cases)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path)
    parser.add_argument("--base-git-ref")
    parser.add_argument("--current", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if args.base and args.base_git_ref:
        parser.error("--base and --base-git-ref are mutually exclusive")
    if not (args.base or args.base_git_ref) or not args.current:
        parser.error("provide --base or --base-git-ref, plus --current; or --self-test")
    try:
        base = (
            base_from_ref(args.base_git_ref)
            if args.base_git_ref
            else args.base.read_bytes()
        )
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
