#!/usr/bin/env python3
"""Fail a pull request when any commit lacks an author-matching DCO sign-off."""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.request


SIGNOFF = re.compile(r"^Signed-off-by:\s*(.+?)\s*<([^<>\s]+@[^<>\s]+)>\s*$", re.I | re.M)

# Commits the repository owner certifies under the DCO by exact SHA.
#
# These five predate this workflow's coverage of the branch they live on: they
# were produced by the owner's own Cursor Agent tool run against the owner's own
# repository, and were never amended with a sign-off line. The owner's ruling of
# 2026-08-19 (full wording in docs/v6/operator-decision-record-2026-08-19.md)
# certifies them under the Developer Certificate of Origin. The exemption is
# keyed on the full 40-hex SHA, which is content-bound: it exempts exactly these
# five trees-and-messages and nothing else, and any amend or rebase produces a
# different SHA that fails closed. This list is CLOSED — a new unsigned commit
# is a defect to fix with `git commit --amend --signoff`, never a new entry here.
ATTESTED_UNSIGNED = {
    "dc33de288077b367ce804d5de7220367bf77721f": "es#137 P1 false-allow closure (Cursor Agent, 2026-08-18)",
    "e8a476c730750a9b3e51ac1001b96825996187cc": "es#137 P2 contract/refusal gaps (Cursor Agent, 2026-08-18)",
    "00e5146e43ff9011153452b83fedda706723c52b": "ES6-V6-CANDIDATE original BUILD freeze packet (Cursor Agent, 2026-08-18)",
    "36df665e80a3d4abe3b5e849cd07397561f16f05": "ES6-V6-CANDIDATE restamp (Cursor Agent, 2026-08-18)",
    "7de88fab412e56268b73371e1cd44138987911ae": "ES6-V6-CANDIDATE tracker freeze (Cursor Agent, 2026-08-18)",
}


def is_merge(item: dict) -> bool:
    """Shape test only: does this commit join two histories?

    Being a merge is NOT by itself an exemption -- see `merge_authored_content`.
    """
    return len(item.get("parents") or []) > 1


def _git(*args: str) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return 1, ""
    return r.returncode, r.stdout.strip()


def merge_authored_content(item: dict) -> bool | None:
    """Did this merge commit AUTHOR content, rather than mechanically join two
    histories?

    A merge whose tree is exactly what a clean three-way merge of its parents
    produces authored nothing: its content is the join, and its "author" is
    whoever ran `git merge`. Exempting that is correct and matches GitHub's own
    DCO app.

    A merge whose tree DIFFERS from the clean result authored the difference --
    a conflict resolution is hand-written content that no one certified. The
    unconditional exemption this function replaces treated both cases alike, so
    a contributor could ship uncertified content by routing it through a
    conflict. That was a recorded limit of this checker (R5-NF4, and the release
    note's own "largest open finding"); this is the enforcement it was missing.

    Returns True (authored -> must be signed), False (clean -> exempt), or None
    (undecidable here, because the objects are not in this clone). None is NOT
    treated as False by the caller: an exemption that cannot be verified is not
    an exemption.
    """
    parents = [str(p.get("sha") or "") for p in (item.get("parents") or [])]
    sha = str(item.get("sha") or "")
    if len(parents) != 2 or not sha:
        # Octopus merges and malformed entries are not auto-exempted.
        return None
    for ref in (*parents, sha):
        if _git("cat-file", "-e", f"{ref}^{{commit}}")[0] != 0:
            return None
    rc, clean_tree = _git("merge-tree", "--write-tree", parents[0], parents[1])
    if rc != 0:
        # A clean merge is impossible (conflict). Any commit that exists here
        # therefore resolved it by hand, which is authoring.
        return True
    rc, actual_tree = _git("rev-parse", f"{sha}^{{tree}}")
    if rc != 0 or not clean_tree or not actual_tree:
        return None
    return clean_tree.split("\n")[0].strip() != actual_tree


def unsigned_commits(commits: list[dict]) -> list[str]:
    unsigned: list[str] = []
    unverifiable: list[str] = []
    for item in commits:
        if is_merge(item):
            authored = merge_authored_content(item)
            if authored is False:
                continue
            if authored is None:
                unverifiable.append(str(item.get("sha") or "unknown")[:12])
                continue
            # authored is True: fall through and require a sign-off like any
            # other authored contribution.
        if str(item.get("sha") or "") in ATTESTED_UNSIGNED:
            continue
        commit = item.get("commit") or {}
        author = commit.get("author") or {}
        expected_name = str(author.get("name") or "").strip().casefold()
        expected_email = str(author.get("email") or "").strip().casefold()
        matches = SIGNOFF.findall(str(commit.get("message") or ""))
        valid = any(
            name.strip().casefold() == expected_name
            and email.strip().casefold() == expected_email
            for name, email in matches
        )
        if not valid:
            unsigned.append(str(item.get("sha") or "unknown")[:12])
    if unverifiable:
        # Fail closed and say exactly what to do about it. A merge we cannot
        # classify is not silently waved through.
        raise SystemExit(
            "DCO: cannot verify whether these merge commits authored content, "
            f"because their objects are not in this clone: {', '.join(unverifiable)}. "
            "Fetch them before running this check (the DCO workflow does this "
            "with `git fetch --no-tags origin <sha>` for the pull request head). "
            "An exemption that cannot be verified is not an exemption."
        )
    return unsigned


# GitHub returns at most this many commits for a pull request, no matter how
# many pages are requested. Past it, completeness is unknowable from the API.
GITHUB_PR_COMMIT_CAP = 250


def github_commits() -> list[dict]:
    event_path = os.environ["GITHUB_EVENT_PATH"]
    repository = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    with open(event_path, encoding="utf-8") as handle:
        pull_number = json.load(handle)["pull_request"]["number"]

    commits: list[dict] = []
    page = 1
    while True:
        url = (
            f"https://api.github.com/repos/{repository}/pulls/{pull_number}/commits"
            f"?per_page=100&page={page}"
        )
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "zms-labs-dco-check",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)
        commits.extend(batch)
        if len(batch) < 100:
            if len(commits) >= GITHUB_PR_COMMIT_CAP:
                raise SystemExit(
                    f"DCO: this pull request has at least {len(commits)} commits and the "
                    f"GitHub pull-request commits endpoint returns at most "
                    f"{GITHUB_PR_COMMIT_CAP}. The remaining commits cannot be read here, "
                    "so this check cannot certify the range. Verify locally with "
                    "`git log --format='%H %(trailers:key=Signed-off-by)' BASE..HEAD` "
                    "and split the pull request."
                )
            return commits
        page += 1


def self_test() -> int:
    """Planted RED controls: every exemption must be provable and fail closed."""
    def c(sha, msg, name="A Dev", email="dev@example.test", parents=1):
        return {
            "sha": sha,
            "parents": [{"sha": "p"}] * parents,
            "commit": {"message": msg, "author": {"name": name, "email": email}},
        }

    signed = "feat: thing\n\nSigned-off-by: A Dev <dev@example.test>"
    attested = sorted(ATTESTED_UNSIGNED)[0]
    cases = [
        ("signed commit passes", [c("a" * 40, signed)], []),
        ("unsigned commit is caught", [c("b" * 40, "feat: thing")], ["b" * 12]),
        (
            "sign-off by someone other than the author is caught",
            [c("c" * 40, "x\n\nSigned-off-by: Other <other@example.test>")],
            ["c" * 12],
        ),
        # Merge behaviour is exercised against REAL git objects below -- a
        # synthetic dict cannot be tree-compared, and pretending otherwise is
        # how the unconditional exemption survived review for so long.
        ("attested commit is exempt", [c(attested, "no sign-off here")], []),
        (
            "an unsigned commit sharing an attested prefix is NOT exempt",
            [c(attested[:12] + "0" * 28, "no sign-off here")], [attested[:12]],
        ),
        (
            "one bad commit among good ones is still caught",
            [c("e" * 40, signed), c("f" * 40, "unsigned"), c(attested, "x")],
            ["f" * 12],
        ),
    ]
    failures = []
    for name, commits, expected in cases:
        got = unsigned_commits(commits)
        if got != expected:
            failures.append(f"{name}: expected {expected}, got {got}")
            print(f"[FAIL] {name}: expected {expected}, got {got}")
        else:
            print(f"[PASS] {name}")
    # The attestation list is closed and structurally exact: full 40-hex only,
    # so no prefix, branch name, or pattern can ever widen it.
    for sha in ATTESTED_UNSIGNED:
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            failures.append(f"attested entry is not a full 40-hex SHA: {sha!r}")
            print(f"[FAIL] attested entry is not a full 40-hex SHA: {sha!r}")
    # CLOSURE CONTROL. "This list is CLOSED" was asserted in a comment and
    # enforced by nothing: an independent review mutation-tested it and found
    # that appending an arbitrary sixth SHA, and deleting an exercised entry,
    # BOTH survived the self-test (R5-NF4). A property that survives its own
    # negation is not enforced. Pinning the digest of the exact set makes any
    # addition or removal fail here, which is the only place it can fail.
    ATTESTED_DIGEST = "422800ed2970640f6d82fb1ececd4a9e3fe29b0040c871f315ad721f58f091c2"
    actual = hashlib.sha256("\n".join(sorted(ATTESTED_UNSIGNED)).encode()).hexdigest()
    if actual != ATTESTED_DIGEST:
        failures.append("ATTESTED_UNSIGNED changed")
        print("[FAIL] ATTESTED_UNSIGNED is a CLOSED list and its contents changed.\n"
              f"       expected sha256 {ATTESTED_DIGEST}\n"
              f"       got             {actual}\n"
              "       Adding an entry requires a new owner ruling, not a code edit;\n"
              "       removing one silently drops a certification that was relied on.")
    else:
        print(f"[PASS] attested list is closed ({len(ATTESTED_UNSIGNED)} entries, digest pinned)")
    # --- merge classification, against real repositories -------------------
    import tempfile

    def run(*args, cwd):
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)

    def build(conflict: bool) -> tuple[str, str]:
        """Return (repo_dir, merge_sha) for a clean or conflicting merge."""
        d = tempfile.mkdtemp()
        env = ["-c", "user.email=t@example.test", "-c", "user.name=T"]
        run("init", "-q", "-b", "main", cwd=d)
        (pathlib.Path(d) / "shared.txt").write_text("base\n", encoding="utf-8")
        run("add", "-A", cwd=d); run(*env, "commit", "-qm", "base", cwd=d)
        run("checkout", "-q", "-b", "side", cwd=d)
        (pathlib.Path(d) / "shared.txt").write_text("side\n", encoding="utf-8")
        run("add", "-A", cwd=d); run(*env, "commit", "-qm", "side", cwd=d)
        run("checkout", "-q", "main", cwd=d)
        # Clean: touch a DIFFERENT file. Conflict: touch the SAME line.
        target = "other.txt" if not conflict else "shared.txt"
        (pathlib.Path(d) / target).write_text("main\n", encoding="utf-8")
        run("add", "-A", cwd=d); run(*env, "commit", "-qm", "main", cwd=d)
        r = run(*env, "merge", "--no-edit", "side", cwd=d)
        if r.returncode != 0:  # conflicted -- resolve by hand, which is authoring
            (pathlib.Path(d) / "shared.txt").write_text("hand-written\n", encoding="utf-8")
            run("add", "-A", cwd=d); run(*env, "commit", "-qm", "resolve", cwd=d)
        sha = run("rev-parse", "HEAD", cwd=d).stdout.strip()
        return d, sha

    cwd0 = os.getcwd()
    merge_controls = 0
    for conflict, expect, label in [
        (False, False, "a clean merge authored nothing -> exempt"),
        (True, True, "a conflict-resolving merge AUTHORED content -> not exempt"),
    ]:
        d, sha = build(conflict)
        os.chdir(d)
        try:
            parents = run("rev-list", "--parents", "-n", "1", sha, cwd=d).stdout.split()[1:]
            item = {"sha": sha, "parents": [{"sha": x} for x in parents],
                    "commit": {"message": "Merge", "author": {"name": "T", "email": "t@example.test"}}}
            got = merge_authored_content(item)
            merge_controls += 1
            if got is expect:
                print(f"[PASS] {label}")
            else:
                failures.append(label)
                print(f"[FAIL] {label}: expected {expect}, got {got}")
        finally:
            os.chdir(cwd0)

    # END-TO-END control, through unsigned_commits() rather than around it.
    # An earlier revision of this self-test exercised merge_authored_content()
    # directly, which left `is_merge` itself untested: mutating it to `False`
    # SURVIVED. A control that skips the dispatch path does not cover the
    # dispatch path. This routes a real clean merge through the real entry point.
    d, sha = build(conflict=False)
    os.chdir(d)
    try:
        parents = run("rev-list", "--parents", "-n", "1", sha, cwd=d).stdout.split()[1:]
        merge_item = {"sha": sha, "parents": [{"sha": x} for x in parents],
                      "commit": {"message": "Merge branch 'side'",
                                 "author": {"name": "T", "email": "t@example.test"}}}
        merge_controls += 1
        got = unsigned_commits([merge_item])
        if got == []:
            print("[PASS] clean merge is exempt end-to-end (exercises is_merge)")
        else:
            failures.append("clean merge not exempt end-to-end")
            print(f"[FAIL] clean merge not exempt end-to-end: {got}")
    finally:
        os.chdir(cwd0)

    # Fail-closed control: objects absent must NOT read as exempt.
    absent = {"sha": "d" * 40, "parents": [{"sha": "e" * 40}, {"sha": "f" * 40}],
              "commit": {"message": "Merge", "author": {"name": "T", "email": "t@example.test"}}}
    merge_controls += 1
    if merge_authored_content(absent) is None:
        print("[PASS] unverifiable merge is undecidable, never silently exempt")
    else:
        failures.append("unverifiable merge did not return None")
        print("[FAIL] unverifiable merge did not return None")

    total = len(cases) + merge_controls
    print(f"DCO self-test: {'PASS' if not failures else 'FAIL'} ({total} controls)")
    return 0 if not failures else 1


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        return self_test()
    commits = github_commits()
    unsigned = unsigned_commits(commits)
    if unsigned:
        print("DCO sign-off missing or does not match the commit author:")
        for sha in unsigned:
            print(f"  - {sha}")
        print("Amend each commit with: git commit --amend --signoff")
        return 1
    print(f"DCO: {len(commits)} commit(s) signed off by their authors")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (KeyError, OSError, ValueError) as exc:
        print(f"DCO check error: {exc}", file=sys.stderr)
        raise SystemExit(2)
