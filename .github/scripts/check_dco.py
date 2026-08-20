#!/usr/bin/env python3
"""Fail a pull request when any commit lacks an author-matching DCO sign-off."""
from __future__ import annotations

import json
import os
import re
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
    """A merge commit joins two histories; its content is the mechanical result
    of that join, and its author is whoever ran `git merge`. The DCO certifies
    authored contributions, so merge commits are exempt — the same default
    GitHub's own DCO app applies. Recorded limit: content a merge commit DOES
    author, namely conflict resolutions, is uncertified by this exemption. Keep
    merges clean, and prefer `git merge --signoff` where the sign-off matters.
    """
    return len(item.get("parents") or []) > 1


def unsigned_commits(commits: list[dict]) -> list[str]:
    unsigned: list[str] = []
    for item in commits:
        if is_merge(item):
            continue
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
        ("merge commit is exempt", [c("d" * 40, "Merge branch", parents=2)], []),
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
    print(f"DCO self-test: {'PASS' if not failures else 'FAIL'} ({len(cases)} controls)")
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
