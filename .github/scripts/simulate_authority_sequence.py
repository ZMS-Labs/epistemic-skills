#!/usr/bin/env python3
"""Falsifier for the publication authority sequence (ruling OAI-P1-03).

The ruling's own acceptance criterion:

    Simulate the amended steps from frozen candidate through tag; recompute the
    SHA after every required write and verify all exact-SHA predicates still
    refer to the tagged commit.
    threshold: one immutable 40-hex subject remains identical across required
    checks, independent verdict, authorization, and annotated tag target.

This executes that literally, in a throwaway repository, for BOTH sequences.
The amended sequence must pass and the superseded one must fail; a test that
only ever passes proves nothing about the defect it claims to cure.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    out = subprocess.run(("git", "-C", str(repo)) + args,
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout.strip()


def new_repo(root: Path) -> Path:
    repo = root / "sim"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Sim Owner")
    git(repo, "config", "user.email", "owner@sim.invalid")
    (repo / "RELEASE.md").write_text("# Release 1.0.0\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "base")
    # A feature branch whose merge will mint the candidate.
    git(repo, "checkout", "-q", "-b", "feature")
    (repo / "code.txt").write_text("shipped\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "feature work")
    git(repo, "checkout", "-q", "main")
    return repo


def amended(repo: Path) -> tuple[str, dict[str, str], list[str]]:
    """Pre-authorization BEFORE the candidate; tag object AFTER."""
    (repo / "PRE-AUTH.md").write_text(
        "I authorize publication of the commit produced by merging the feature "
        "branch, and only that commit, iff the gate returns GO.\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "pre-authorization (names no SHA)")

    git(repo, "merge", "--no-ff", "-q", "-m", "merge: mint the candidate", "feature")
    candidate = git(repo, "rev-parse", "HEAD")

    bound = {}
    bound["exact_checks"] = git(repo, "rev-parse", "HEAD")      # step 4
    bound["independent_verdict"] = git(repo, "rev-parse", "HEAD")  # step 5
    # Step 7: authorization lives in the tag OBJECT, not a commit.
    git(repo, "tag", "-a", "v1.0.0", "-m",
        f"verdict: runs/gate GO\nauthorized-sha: {candidate}\nowner: Sim Owner")
    bound["authorization"] = candidate
    bound["tag_target"] = git(repo, "rev-list", "-n", "1", "v1.0.0")

    writes_after = []
    if git(repo, "rev-parse", "HEAD") != candidate:
        writes_after.append("a commit was made after the candidate")
    return candidate, bound, writes_after


def superseded(repo: Path) -> tuple[str, dict[str, str], list[str]]:
    """The old sequence: authorization line COMMITTED after the candidate."""
    git(repo, "merge", "--no-ff", "-q", "-m", "merge: mint the candidate", "feature")
    candidate = git(repo, "rev-parse", "HEAD")

    bound = {}
    bound["exact_checks"] = candidate
    bound["independent_verdict"] = candidate
    # Step 7 as previously written: commit a line naming the candidate.
    notes = repo / "RELEASE.md"
    notes.write_text(notes.read_text(encoding="utf-8")
                     + f"\nAuthorized SHA: {candidate}\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "authorization line naming the candidate")
    bound["authorization"] = candidate          # what the line CLAIMS
    git(repo, "tag", "-a", "v1.0.0", "-m", "tag")
    bound["tag_target"] = git(repo, "rev-list", "-n", "1", "v1.0.0")

    writes_after = []
    if git(repo, "rev-parse", "HEAD") != candidate:
        writes_after.append("a commit was made after the candidate")
    return candidate, bound, writes_after


def run(label: str, fn, expect_pass: bool) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        repo = new_repo(Path(tmp))
        candidate, bound, writes_after = fn(repo)
        distinct = set(bound.values())
        passed = len(distinct) == 1 and not writes_after
        print(f"\n  {label}")
        for k, v in bound.items():
            mark = "ok " if v == bound["tag_target"] else "DIFF"
            print(f"    {mark} {k:22} {v[:12]}")
        if writes_after:
            for w in writes_after:
                print(f"    DIFF required write after the candidate: {w}")
        print(f"    -> {len(distinct)} distinct subject(s); "
              f"{'PASS' if passed else 'FAIL'} (expected {'PASS' if expect_pass else 'FAIL'})")
        return passed == expect_pass


def main() -> int:
    print("Falsifier: one immutable subject across checks, verdict, "
          "authorization, and tag target.")
    ok = run("AMENDED sequence (pre-authorization + tag object)", amended, True)
    ok &= run("SUPERSEDED sequence (authorization committed after candidate)",
              superseded, False)
    print(f"\nauthority-sequence falsifier: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
