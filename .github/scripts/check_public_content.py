#!/usr/bin/env python3
"""Fail-closed public-content pattern gate for exact release candidates.

Drift disease this prevents: treating a green credential scan as proof that the
public tree contains no private-fleet topology. The July 21 public-release
addendum already classified private-repository identifiers and user-specific
local paths as scrub targets. Those strings need not look like secrets.

This check scans the tracked tree for a narrow, seeded pattern set and fails
closed on any hit outside an explicit allowlist of historical review receipts
that intentionally document the scrub vocabulary.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Patterns drawn from docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md.
# Keep the list small and reasoned. Each entry must have a RED seed below.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("private-fleet-repo-name", re.compile(r"\bzms-homelab\b", re.I)),
    # Windows user homes in either slash form.
    ("windows-user-path", re.compile(r"[A-Za-z]:[\\/]Users[\\/][A-Za-z0-9._-]+", re.I)),
    # POSIX user homes. Negative lookbehind avoids matching the `/Users/`
    # substring inside `C:/Users/...`.
    ("posix-user-path", re.compile(r"(?<![A-Za-z:])/Users/[A-Za-z0-9._-]+/")),
    ("y-drive-private-checkout", re.compile(r"[Yy]:[/\\]dev[/\\]zms-homelab", re.I)),
]

# Files that must remain able to name the scrub vocabulary so the review trail
# stays intelligible. Hits elsewhere fail closed.
ALLOWLIST_PREFIXES = (
    "docs/release/PUBLIC-RELEASE-REVIEW-",
    "docs/release/PUBLIC-CONTENT-POST-RELEASE-REVIEW-",
    "docs/release/RELEASE-5.0.0-ERRATA-",
    "docs/release/POST-RELEASE-INDEPENDENT-REVIEW-",
    "docs/release/V5.0.0-DESIGN-CONFORMANCE-",
    ".github/scripts/check_public_content.py",
)


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    return [REPO_ROOT / rel for rel in result.stdout.decode("utf-8").split("\0") if rel]


def is_allowlisted(path: Path) -> bool:
    rel = path.relative_to(REPO_ROOT).as_posix()
    return any(rel.startswith(prefix) or rel == prefix for prefix in ALLOWLIST_PREFIXES)


def scan_text(path: Path, text: str) -> list[str]:
    defects: list[str] = []
    if is_allowlisted(path):
        return defects
    rel = path.relative_to(REPO_ROOT).as_posix()
    # Synthetic RED-seed usernames used by package tests (not real operator homes).
    sanitized = re.sub(r"([A-Za-z]:[\\/]Users[\\/]|/Users/)example\b", r"\1<synthetic>", text, flags=re.I)
    for name, pattern in PATTERNS:
        if pattern.search(sanitized):
            defects.append(f"{name}: {rel}")
    return defects


def run_check() -> int:
    defects: list[str] = []
    for path in tracked_files():
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        defects.extend(scan_text(path, text))
    if defects:
        for defect in defects:
            print(f"public-content defect: {defect}", file=sys.stderr)
        return 1
    print(
        "public-content gate ok: "
        f"{len(PATTERNS)} patterns, {len(ALLOWLIST_PREFIXES)} allowlist prefixes"
    )
    return 0


def run_self_test() -> int:
    failures: list[str] = []
    seeds = {
        "private-fleet-repo-name": "see also ZMS-Labs/zms-homelab for fleet overlays",
        "windows-user-path": r"probe under C:\Users\example\.claude\skills",
        "posix-user-path": "probe under /Users/example/.claude/skills",
        "y-drive-private-checkout": r"checkout at Y:\dev\zms-homelab-main",
    }
    for expected, blob in seeds.items():
        hits = []
        for name, pattern in PATTERNS:
            if pattern.search(blob):
                hits.append(name)
        if expected not in hits:
            failures.append(f"seeded {expected} was not detected in {blob!r}: {hits}")

    # Allowlisted historical review text must not fail the check when scanned alone.
    allowlisted = scan_text(
        REPO_ROOT / "docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md",
        "Patterns swept: private-repo name (`zms-homelab`)",
    )
    if allowlisted:
        failures.append(f"allowlisted review text was rejected: {allowlisted}")

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAILURE: {failure}", file=sys.stderr)
        return 1
    print(f"public-content self-test ok: {len(seeds)} seeded RED controls passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
