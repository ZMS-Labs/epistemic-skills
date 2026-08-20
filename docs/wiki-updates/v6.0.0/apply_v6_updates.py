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
    # The present-tense detector is advisory; prove it sees a real case.
    if RETIRED_PRESENT_TENSE.search("`using-epistemic-skills` selects the set"):
        print("[PASS] retired-seat present tense detected")
    else:
        failures += 1
        print("[FAIL] retired-seat present tense not detected")
    print(f"apply_v6_updates self-test: {'PASS' if not failures else 'FAIL'}")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki", nargs="?", help="path to a wiki clone")
    ap.add_argument("--apply", action="store_true", help="write changes (default is dry-run)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.wiki:
        ap.error("a wiki clone path is required unless --self-test")
    root = Path(args.wiki)
    if not root.is_dir():
        ap.error(f"not a directory: {root}")
    if args.apply:
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
