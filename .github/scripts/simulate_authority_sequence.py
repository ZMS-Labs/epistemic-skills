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

import re
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
    # No address shape: git accepts an arbitrary identity string, and the
    # public-content gate rightly refuses email patterns in tracked files.
    git(repo, "config", "user.email", "sim-owner")
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


def amended(repo: Path, *, drop: tuple[str, ...] = ()) -> tuple[str, dict[str, str], list[str]]:
    """Pre-authorization BEFORE the candidate; tag object AFTER.

    `drop` omits annotation fields from the created tag, so the tampered
    variants below exercise THIS scenario's own binding logic: a falsifier
    that derives nothing from the tag reports PASS over a tag that says
    nothing."""
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
    lines = ["verdict: runs/gate GO", f"authorized-sha: {candidate}",
             "owner: Sim Owner", "exact-sha-runs: 111,222,333,444,555"]
    git(repo, "tag", "-a", "v1.0.0", "-m",
        "\n".join(l for l in lines if l.split(":", 1)[0] not in drop))
    # The authorization subject is what the TAG SAYS, not what this harness
    # remembers. Hard-coding `candidate` here meant a tag that omitted or
    # mistyped `authorized-sha` still produced one distinct subject and PASS:
    # the AMENDED-TAMPERED scenario above went red only when this binding
    # started reading the annotation. A missing or wrong field now yields a
    # subject that is not the candidate, and the scenario fails as it must.
    fields = tag_fields(repo, "v1.0.0")
    bound["authorization"] = fields.get("authorized-sha", "")
    # The evidence binding is read from the same annotation: the
    # `exact-sha-runs` field must exist and carry the run-id list it claims.
    # Hard-coded to `candidate`, this value survived the field being removed,
    # malformed, or attached to the wrong subject -- the
    # AMENDED-EVIDENCE-TAMPERED scenario stayed green until the binding was
    # derived from the tag message it asserts about.
    bound["evidence_record"] = (
        candidate if re.fullmatch(r"[0-9]+(,[0-9]+)*",
                                  fields.get("exact-sha-runs", "")) else "")
    bound["tag_target"] = git(repo, "rev-list", "-n", "1", "v1.0.0")

    writes_after = []
    if git(repo, "rev-parse", "HEAD") != candidate:
        writes_after.append("a commit was made after the candidate")
    return candidate, bound, writes_after


def tag_fields(repo: Path, tag: str) -> dict[str, str]:
    """`key: value` lines of the annotated tag OBJECT. The amended sequence
    keeps its authorization and evidence bindings in this message and nowhere
    else, so what the tag actually says is the only honest source for either
    subject."""
    msg = git(repo, "for-each-ref", f"refs/tags/{tag}", "--format=%(contents)")
    fields: dict[str, str] = {}
    for line in msg.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def amended_tampered(repo: Path) -> tuple[str, dict[str, str], list[str]]:
    """The amended sequence with `authorized-sha` DROPPED from the tag. A
    falsifier that hard-codes the authorization subject cannot see this: the
    tag authorizes nothing, yet every bound value still reads candidate."""
    return amended(repo, drop=("authorized-sha",))


def amended_evidence_tampered(repo: Path) -> tuple[str, dict[str, str], list[str]]:
    """The amended sequence with `exact-sha-runs` DROPPED from the tag. The
    authorization field survives, so only an evidence binding that actually
    reads the annotation can turn this scenario red."""
    return amended(repo, drop=("exact-sha-runs",))


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


def evidence_committed(repo: Path) -> tuple[str, dict[str, str], list[str]]:
    """Evidence table COMMITTED after the candidate -- the limb missed by the
    first version of this cure, and the reason this scenario exists."""
    git(repo, "merge", "--no-ff", "-q", "-m", "merge: mint the candidate", "feature")
    candidate = git(repo, "rev-parse", "HEAD")
    bound = {"exact_checks": candidate, "independent_verdict": candidate,
             "authorization": candidate}
    notes = repo / "RELEASE.md"
    notes.write_text(notes.read_text(encoding="utf-8")
                     + "\nruns at candidate: 111,222,333,444,555\n", encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "exact-SHA evidence table")
    bound["evidence_record"] = candidate
    git(repo, "tag", "-a", "v1.0.0", "-m", "tag")
    bound["tag_target"] = git(repo, "rev-list", "-n", "1", "v1.0.0")
    writes_after = []
    if git(repo, "rev-parse", "HEAD") != candidate:
        writes_after.append("evidence was committed after the candidate")
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
    ok &= run("AMENDED-TAMPERED sequence (tag omits authorized-sha)",
              amended_tampered, False)
    ok &= run("AMENDED-EVIDENCE-TAMPERED sequence (tag omits exact-sha-runs)",
              amended_evidence_tampered, False)
    ok &= run("SUPERSEDED sequence (authorization committed after candidate)",
              superseded, False)
    ok &= run("EVIDENCE-COMMITTED variant (the limb the first cure missed)",
              evidence_committed, False)
    print(f"\nauthority-sequence falsifier: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
