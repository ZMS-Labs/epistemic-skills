#!/usr/bin/env python3
"""Fail-closed aggregate ceiling on packaged skill description bytes.

Drift disease this prevents: **per-item discipline with no aggregate check.**

A skill's ``description`` is the only text that governs whether it fires. The
harness caps the *total* UTF-8 description bytes it will carry across everything
installed, and when that cap is exceeded it silently drops descriptions. A skill
whose description is dropped cannot fire on description match at all -- **it is
functionally uninstalled, and no error is emitted anywhere.** Nothing in the
package fails, nothing in CI goes red, and the seat is simply gone.

Adding a skill is therefore a *transfer*, not an addition: it displaces roughly
its own byte-weight of some other skill's ability to fire, possibly in a different
package entirely.

This is not hypothetical. Measured on a live estate 2026-08-06 by reversible
manipulation -- adding probes, then removing them, then removing unrelated
commands -- with the count of blank descriptions as the observable::

    108 skills          ->  1 description dropped
    111 (+3 probes)     ->  5 dropped
    108 (-3 probes)     ->  back to 1
    100 (-8 commands)   ->  0
     68 (-35 commands)  ->  0, full headroom

v5.0.0 shipped **+1,389 net description bytes** and knocked two of its own new
skills (``triage``, ``watch``) out of the firing set until unrelated commands
were deleted elsewhere on the machine. Every individual description had been
held inside sibling range; the *sum* was never checked. That is the exact defect
class this package exists to catch, committed by the package itself.

What this check can and cannot do
---------------------------------

It cannot see the harness cap -- that is a property of the whole installed
estate, which no single package can observe or control. What it *can* do, and
does, is bound this package's own contribution to a number that was deliberately
chosen and is visible in a diff whenever it changes.

``CEILING_BYTES`` is set to the measured total at the time of writing, so any
increase fails closed and must be paid for explicitly: either shorten another
description, or raise the constant in the same commit and say in the message what
the added bytes bought. Raising it is allowed. Raising it *silently* is what this
prevents.

If the total drops well below the ceiling, lower the constant to match. A ceiling
with slack quietly re-permits the growth it was installed to stop.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / "plugins" / "epistemic-skills" / "skills"

# The recorded budget: the sum of the 15 packaged skill description
# values, measured as the harness sees them -- YAML-resolved and then UTF-8
# encoded, so a quoted scalar is charged for its content and not its
# delimiters, while non-ASCII characters are charged for their real byte width.
# Verified per-skill against pyyaml with zero mismatches; pyyaml is the oracle for
# that check but not a runtime dependency of this one.
#
# Originally recorded as 8200 under a character-count bug, then corrected to
# 8230 on 2026-08-07 when the guard switched to UTF-8 bytes. The commission-watch
# clarification reduced the exact package total by 71 bytes without adding a
# skill or weakening another trigger. The ceiling therefore moves down to 8159
# so that released headroom cannot silently refill.
#
# Changing this number is a reviewed act: it must appear in a diff with a
# justification, which is the entire point of the check.
#
# 2026-08-11: +477 bytes for the `manifest` custodian skill (mission custody:
# authority, checkpoints, drift re-anchoring, independent acceptance). The
# spend was operator-authorized by an explicit byte-budget sign-off ("Approve
# — spend the bytes", recorded in the mission-custody build ledger and PR
# #113) before the skill landed — the deliberate-spend gate this ceiling
# exists to force.
CEILING_BYTES = 8636

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)
# `description:` runs until the next top-level YAML key or end of frontmatter,
# so a folded multi-line description is counted in full rather than truncated
# at its first line.
DESCRIPTION = re.compile(r"^description:\s*(.*?)(?=^[A-Za-z_][A-Za-z0-9_-]*:|\Z)", re.S | re.M)


def unquote_scalar(value: str) -> str:
    """Resolve a YAML-quoted scalar to the string the harness actually carries.

    This matters, and is not pedantry. Five of the packaged descriptions are
    quoted. Counting the raw frontmatter text charges them for their delimiters
    and escapes, so the budget would not mean what it claims, and merely
    *unquoting* a description would look like freed headroom when nothing was
    actually freed.

    Done in stdlib on purpose: every other check in this directory runs on a bare
    interpreter, and a gate that needs a dependency installed is a gate that can
    silently fail to run.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        inner = value[1:-1]
        if value[0] == '"':
            return inner.replace('\\"', '"').replace("\\\\", "\\")
        return inner.replace("''", "'")
    return value


class BudgetError(ValueError):
    """A named, fail-closed rejection of a description surface."""

    def __init__(self, name: str, detail: str):
        self.name = name
        self.detail = detail
        super().__init__(f"{name}: {detail}")


def description_bytes(text: str, skill: str) -> int:
    """UTF-8 byte width of a SKILL.md description, failing closed on defects."""
    front = FRONTMATTER.match(text)
    if front is None:
        raise BudgetError("MALFORMED_FRONTMATTER", f"{skill}/SKILL.md has no leading --- block")
    found = DESCRIPTION.search(front.group(1))
    if found is None:
        raise BudgetError("MISSING_DESCRIPTION", f"{skill}/SKILL.md frontmatter has no description key")
    value = unquote_scalar(found.group(1).strip())
    if not value:
        # A blank description is the failure this check exists to detect, so it
        # is never silently counted as zero cost.
        raise BudgetError("EMPTY_DESCRIPTION", f"{skill}/SKILL.md description is empty; it cannot fire")
    return len(value.encode("utf-8"))


def measure(skills_root: Path) -> dict[str, int]:
    """Ground truth: every skill directory carrying a SKILL.md, mapped to bytes."""
    if not skills_root.is_dir():
        raise BudgetError("MISSING_SURFACE", f"{skills_root} is not a directory")
    sizes: dict[str, int] = {}
    for entry in sorted(skills_root.iterdir()):
        skill_md = entry / "SKILL.md"
        if not entry.is_dir() or not skill_md.is_file():
            continue
        try:
            text = skill_md.read_text(encoding="utf-8")
        except OSError as error:
            raise BudgetError("UNREADABLE_SURFACE", f"{entry.name}/SKILL.md is not readable: {error}")
        sizes[entry.name] = description_bytes(text, entry.name)
    if not sizes:
        raise BudgetError("EMPTY_SKILL_GLOB", f"no SKILL.md-bearing directories under {skills_root}")
    return sizes


def check_budget(sizes: dict[str, int], ceiling: int) -> list[str]:
    """Compare the measured total against the recorded ceiling; return violations."""
    violations: list[str] = []
    total = sum(sizes.values())
    if total > ceiling:
        widest = ", ".join(
            f"{name} ({size}B)"
            for name, size in sorted(sizes.items(), key=lambda item: -item[1])[:3]
        )
        violations.append(
            f"BUDGET_EXCEEDED: {total} description bytes across {len(sizes)} skills exceeds the "
            f"recorded ceiling of {ceiling} by {total - ceiling}. Description bytes are a shared, "
            f"rivalrous budget: over the harness cap, descriptions are dropped silently and those "
            f"skills stop firing entirely. Either buy the width back with concision, or raise "
            f"CEILING_BYTES in this file and say what the added bytes bought. Widest seats: {widest}."
        )
    return violations


def run_check(ceiling: int = CEILING_BYTES) -> int:
    try:
        sizes = measure(SKILLS_ROOT)
    except BudgetError as error:
        print(f"VIOLATION {error}", file=sys.stderr)
        return 1
    violations = check_budget(sizes, ceiling)
    if violations:
        for violation in violations:
            print(f"VIOLATION {violation}", file=sys.stderr)
        return 1
    total = sum(sizes.values())
    headroom = ceiling - total
    note = (
        f"; {headroom} bytes of slack -- lower CEILING_BYTES to {total} so the slack cannot "
        "quietly refill" if headroom else "; exactly at the recorded ceiling"
    )
    print(f"description budget ok: {total} bytes across {len(sizes)} skills, ceiling {ceiling}{note}")
    return 0


def run_report() -> int:
    """Print the per-skill breakdown. Measurement, not a gate; always exits 0."""
    try:
        sizes = measure(SKILLS_ROOT)
    except BudgetError as error:
        print(f"VIOLATION {error}", file=sys.stderr)
        return 1
    for name, size in sorted(sizes.items(), key=lambda item: -item[1]):
        print(f"{size:6d}  {name}")
    print(f"{sum(sizes.values()):6d}  TOTAL across {len(sizes)} skills (ceiling {CEILING_BYTES})")
    return 0


def run_self_test() -> int:
    """Plant synthetic defects in-memory and prove every check fails closed."""
    failures: list[str] = []

    aligned = {"alpha-skill": 100, "beta-skill": 200}
    if check_budget(aligned, 300):
        failures.append("a total exactly at the ceiling must pass")
    if check_budget(aligned, 500):
        failures.append("a total under the ceiling must pass")
    over = check_budget(aligned, 299)
    if not any(violation.startswith("BUDGET_EXCEEDED") for violation in over):
        failures.append(f"a total over the ceiling must fail, got: {over}")

    # A one-byte overrun must fail: the defect that shipped in v5.0.0 was an
    # accumulation of individually-reasonable additions, so the gate cannot
    # carry a tolerance.
    if not check_budget({"alpha-skill": 301}, 300):
        failures.append("a one-byte overrun must fail")

    parse_probes = {
        "MALFORMED_FRONTMATTER": "no frontmatter here\n",
        "MISSING_DESCRIPTION": "---\nname: alpha\n---\nbody\n",
        "EMPTY_DESCRIPTION": "---\nname: alpha\ndescription:\nmodel: sonnet\n---\nbody\n",
    }
    for expected, text in parse_probes.items():
        try:
            description_bytes(text, "alpha-skill")
        except BudgetError as error:
            if error.name != expected:
                failures.append(f"planted {expected} raised {error.name} instead")
        else:
            failures.append(f"planted {expected} was not detected")

    # Positive control: the parser must actually measure a well-formed skill, so
    # the failures above are real detections and not a parser that rejects
    # everything it is handed.
    plain_value = "Use when the thing happens."
    good = f"---\nname: alpha\ndescription: {plain_value}\nmodel: sonnet\n---\nbody\n"
    measured = description_bytes(good, "alpha-skill")
    if measured != len(plain_value.encode("utf-8")):
        failures.append(f"positive control mis-measured a valid description: {measured}")

    # A folded multi-line description must be counted in full, not truncated at
    # its first line -- undercounting would let the real total drift above the
    # ceiling while the gate reported green.
    folded = "---\nname: alpha\ndescription: first line\n  second line\nmodel: sonnet\n---\n"
    if description_bytes(folded, "alpha-skill") <= len("first line".encode("utf-8")):
        failures.append("a multi-line description was truncated at its first line")

    # UTF-8 byte width is load-bearing. `é` is one Python character but two UTF-8
    # bytes; a character count would silently undercharge the actual harness
    # budget.
    unicode_value = "Use when café state matters."
    unicode_skill = f"---\nname: alpha\ndescription: {unicode_value}\n---\n"
    unicode_measured = description_bytes(unicode_skill, "alpha-skill")
    if unicode_measured != len(unicode_value.encode("utf-8")):
        failures.append(
            f"UTF-8 control measured {unicode_measured}, expected "
            f"{len(unicode_value.encode('utf-8'))} bytes"
        )
    if unicode_measured == len(unicode_value):
        failures.append("UTF-8 control collapsed to character count")

    # Quoted scalars must be charged for their content, not their delimiters, or
    # unquoting a description would read as freed budget.
    quoted_probes = {
        '"Use when the thing happens."': "Use when the thing happens.",
        "'Use when the thing happens.'": "Use when the thing happens.",
        '"He said \\"go\\" once."': 'He said "go" once.',
        "'it''s here'": "it's here",
        "Use when unquoted.": "Use when unquoted.",
        # Not a wrapping quote pair: an apostrophe mid-value must survive intact.
        "don't strip me": "don't strip me",
    }
    for raw, expected in quoted_probes.items():
        got = unquote_scalar(raw)
        if got != expected:
            failures.append(f"unquote_scalar({raw!r}) gave {got!r}, expected {expected!r}")

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAILURE: {failure}", file=sys.stderr)
        return 1
    print("description budget self-test ok: planted overruns, UTF-8 width, and parse defects all passed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Aggregate skill description byte ceiling")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="plant synthetic overruns and parse defects, and prove the check fails closed",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="print the per-skill byte breakdown without gating",
    )
    arguments = parser.parse_args(argv)
    if arguments.self_test:
        return run_self_test()
    if arguments.report:
        return run_report()
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
