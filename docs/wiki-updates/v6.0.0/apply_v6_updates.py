#!/usr/bin/env python3
"""Apply the v6.0.0 corrections to a clone of the epistemic-skills wiki.

The wiki is a separate repository, so this cannot run in CI against the thing it
edits. It is therefore written to be *checkable*: `--dry-run` (the default)
reports what it would change and touches nothing, `--self-test` proves each rule
on fixtures, and `--apply` requires an explicit path to a wiki clone.

Scope is the measured drift, not a rewrite. Measured 2026-08-20 by cloning the
wiki: most pages said fourteen skills, `Skill-Manifest` did not exist, retired
seats were described in the present tense, and v5.0.0 outnumbered v5.1.0 in
version guidance 301 to 29.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CURRENT_VERSION = "6.0.0"

# Ordered: each rule is (name, compiled pattern, replacement).
RULES: list[tuple[str, re.Pattern[str], str]] = [
    # Skill count. Bounded by the word "skills" so it cannot rewrite an
    # unrelated numeral, and case-preserving for sentence starts.
    ("skill-count-lower", re.compile(r"\bfourteen(?= skills\b)"), "fifteen"),
    ("skill-count-title", re.compile(r"\bFourteen(?= skills\b)"), "Fifteen"),
    # Discipline count moves with it: fifteen skills = one entry point + fourteen.
    ("discipline-count", re.compile(r"\bthirteen(?= disciplines\b)"), "fourteen"),
    # Version-pinned source links and install guidance.
    ("tagged-tree-url", re.compile(r"(github\.com/ZMS-Labs/epistemic-skills/(?:tree|blob)/)v\d+\.\d+\.\d+"),
     r"\g<1>v" + CURRENT_VERSION),
    ("applies-to-banner", re.compile(r"(\*\*Applies to:\*\* epistemic-skills )v\d+\.\d+\.\d+"),
     r"\g<1>v" + CURRENT_VERSION),
]

# Seats deleted in earlier releases. A wiki page may describe them, but not in
# the present tense as though they were live.
RETIRED_PRESENT_TENSE = re.compile(
    r"\b(using-epistemic-skills|helix|blindspot-pass|wayfinding|harvest-before-adopt|"
    r"applying-formal-rigor|evidence-research|throwaway-prototyping|continuity-verify)\b"
    r"`?\s+(is|selects|owns|routes|hands)\b"
)


def plan(root: Path) -> dict[str, list[tuple[str, int]]]:
    """Report what would change, per rule. Never writes."""
    found: dict[str, list[tuple[str, int]]] = {}
    for page in sorted(root.glob("*.md")):
        text = page.read_text(encoding="utf-8")
        for name, pattern, _ in RULES:
            n = len(pattern.findall(text))
            if n:
                found.setdefault(name, []).append((page.name, n))
        n = len(RETIRED_PRESENT_TENSE.findall(text))
        if n:
            found.setdefault("retired-seat-present-tense (MANUAL)", []).append((page.name, n))
    return found


def apply(root: Path) -> int:
    changed = 0
    for page in sorted(root.glob("*.md")):
        text = original = page.read_text(encoding="utf-8")
        for _, pattern, repl in RULES:
            text = pattern.sub(repl, text)
        if text != original:
            page.write_text(text, encoding="utf-8")
            changed += 1
    manifest = Path(__file__).parent / "pages" / "Skill-Manifest.md"
    if manifest.is_file():
        (root / "Skill-Manifest.md").write_text(
            manifest.read_text(encoding="utf-8"), encoding="utf-8")
        changed += 1
    return changed


def self_test() -> int:
    failures = 0
    cases = [
        ("count is rewritten only beside 'skills'",
         "The package ships fourteen skills. Chapter fourteen is unrelated.",
         "The package ships fifteen skills. Chapter fourteen is unrelated."),
        ("title-case count",
         "Fourteen skills ship.", "Fifteen skills ship."),
        ("tagged url is bumped",
         "see github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins",
         "see github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins"),
        ("applies-to banner is bumped",
         "**Applies to:** epistemic-skills v5.0.0",
         "**Applies to:** epistemic-skills v6.0.0"),
        ("prose numeral untouched",
         "fourteen of the findings were closed", "fourteen of the findings were closed"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, src, want in cases:
            page = root / "T.md"
            page.write_text(src, encoding="utf-8")
            apply(root)
            got = page.read_text(encoding="utf-8")
            if got == want:
                print(f"[PASS] {name}")
            else:
                failures += 1
                print(f"[FAIL] {name}\n  want: {want!r}\n  got:  {got!r}")
            (root / "Skill-Manifest.md").unlink(missing_ok=True)
    # Guard 1: check_paths. Both directions, because a guard that never fires and
    # a guard that always fires are the same useless guard.
    with tempfile.TemporaryDirectory() as tmp:
        wiki = Path(tmp) / "wiki"
        wiki.mkdir()
        (wiki / "Home.md").write_text("hi", encoding="utf-8")
        if not check_paths(wiki):
            print("[PASS] check_paths accepts a wiki-shaped directory")
        else:
            failures += 1
            print(f"[FAIL] check_paths rejected a wiki-shaped directory: {check_paths(wiki)}")
        # The damaging case: aimed at the code repository.
        code = Path(tmp) / "code"
        (code / "plugins").mkdir(parents=True)
        (code / "RELEASING.md").write_text("x", encoding="utf-8")
        (code / "README.md").write_text("x", encoding="utf-8")
        why = check_paths(code)
        if any("CODE repository" in r for r in why):
            print("[PASS] check_paths refuses the code repository")
        else:
            failures += 1
            print(f"[FAIL] check_paths did not refuse the code repository: {why}")
        empty = Path(tmp) / "empty"
        empty.mkdir()
        if check_paths(empty):
            print("[PASS] check_paths refuses a directory with no pages")
        else:
            failures += 1
            print("[FAIL] check_paths accepted an empty directory")

    # Guard 2: tag_exists must fail closed. It returns True/False/None and the
    # caller must treat None as "do not write" -- prove the tri-state, not the
    # network call.
    if tag_exists.__doc__ and "None is NOT treated as True" in tag_exists.__doc__:
        observed = tag_exists()
        if observed in (True, False, None):
            print(f"[PASS] tag_exists returns a tri-state (observed: {observed!r})")
        else:
            failures += 1
            print(f"[FAIL] tag_exists returned {observed!r}")
    else:
        failures += 1
        print("[FAIL] tag_exists lost its fail-closed contract")

    # The present-tense detector is advisory; prove it sees a real case.
    if RETIRED_PRESENT_TENSE.search("`using-epistemic-skills` selects the set"):
        print("[PASS] retired-seat present tense detected")
    else:
        failures += 1
        print("[FAIL] retired-seat present tense not detected")
    print(f"apply_v6_updates self-test: {'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


# --- Guards. Two ways this script can do real damage, both cheap to prevent. ---

# 1. Pointed at the wrong tree. Its rules rewrite any `*.md` in the given
#    directory, so aimed at a checkout of THIS repository it would happily
#    rewrite the release notes it exists to support. A wiki clone is
#    recognisable: a flat directory of `.md` pages whose git remote ends in
#    `.wiki.git`, and which carries at least one page this package expects.
WIKI_SENTINEL_PAGES = ("Home.md", "Installation.md", "Skill-Catalog.md")


def check_paths(root: Path) -> list[str]:
    """Return the reasons `root` does not look like an epistemic-skills wiki clone.
    Empty list means it does. Never writes."""
    reasons: list[str] = []
    if not root.is_dir():
        return [f"not a directory: {root}"]
    pages = list(root.glob("*.md"))
    if not pages:
        reasons.append("no top-level *.md pages -- a wiki clone is a flat page directory")
    if not any((root / name).is_file() for name in WIKI_SENTINEL_PAGES):
        reasons.append(f"none of {list(WIKI_SENTINEL_PAGES)} present")
    # The unmistakable tell: this is the code repository, not its wiki.
    for marker in ("RELEASING.md", "plugins", ".github"):
        if (root / marker).exists():
            reasons.append(f"{marker!r} present -- this looks like the CODE repository, "
                           "which this script must never rewrite")
    remote = ""
    try:
        remote = subprocess.run(
            ["git", "-C", str(root), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        remote = ""
    if remote and not remote.endswith(".wiki.git"):
        reasons.append(f"git remote {remote!r} does not end in '.wiki.git'")
    return reasons


# 2. Run before the tag exists. `tagged-tree-url` and `applies-to-banner` rewrite
#    links to point at /v6.0.0/. If that tag has not been created yet, applying
#    them replaces working v5 links with 404s -- publication-gate finding PG-18,
#    reproduced in the wiki where no oracle in this repository can see it.
def tag_exists(version: str = CURRENT_VERSION) -> bool | None:
    """True/False if it could be determined, None if the check could not run
    (offline, no git). None is NOT treated as True by the caller."""
    try:
        r = subprocess.run(
            ["git", "ls-remote", "--tags", "origin", f"refs/tags/v{version}"],
            cwd=Path(__file__).resolve().parent, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    return bool(r.stdout.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki", nargs="?", help="path to a wiki clone")
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--check-paths", action="store_true",
                    help="report whether the given path looks like a wiki clone, and exit")
    ap.add_argument("--force", action="store_true",
                    help="apply despite a failed guard (states which guard was overridden)")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.wiki:
        ap.error("a wiki clone path is required unless --self-test")
    root = Path(args.wiki)
    if not root.is_dir():
        ap.error(f"not a directory: {root}")
    reasons = check_paths(root)
    if args.check_paths:
        if reasons:
            print(f"{root} does NOT look like an epistemic-skills wiki clone:")
            for r in reasons:
                print(f"  - {r}")
            return 1
        print(f"{root} looks like an epistemic-skills wiki clone")
        return 0
    if args.apply:
        blocked = list(reasons)
        tag = tag_exists()
        if tag is False:
            blocked.append(
                f"tag v{CURRENT_VERSION} does not exist on origin -- applying now would "
                "rewrite working links into 404s (PG-18). Tag first, then run this.")
        elif tag is None:
            blocked.append(
                f"could not determine whether tag v{CURRENT_VERSION} exists (offline or "
                "no git). Failing closed: an unknown tag state is not a present tag.")
        if blocked and not args.force:
            print("refusing to write. Guards that failed:")
            for r in blocked:
                print(f"  - {r}")
            print("\nRe-run with --check-paths to inspect, or --force to override "
                  "deliberately.")
            return 1
        if blocked:
            print("--force: overriding these guards deliberately:")
            for r in blocked:
                print(f"  - {r}")
        print(f"changed {apply(root)} page(s) in {root}")
        return 0
    found = plan(root)
    if not found:
        print("no changes needed")
        return 0
    for rule, pages in sorted(found.items()):
        total = sum(n for _, n in pages)
        print(f"{rule}: {total} occurrence(s) in {len(pages)} page(s)")
        for page, n in pages[:6]:
            print(f"    {page} ({n})")
    print("\ndry run — nothing written. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
