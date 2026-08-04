#!/usr/bin/env python3
"""Single-source synchronization for every skill-inventory surface.

The hand-edited sources of truth are exactly two:

1. the filesystem — ``plugins/epistemic-skills/skills/<name>/`` defines which
   skills exist; and
2. ``contracts/epistemic-events/skill-event-map.json`` — per-skill collection
   metadata (event kinds, eligibility, outcome sources, mode, sentinel).

Everything else is a derived surface. ``--check`` (the CI mode) verifies every
derived surface agrees with the sources and exits nonzero with a named error
per drift. ``--write`` regenerates the derivable surfaces in place:

- ``skill-event-map.schema.json`` — bounds, per-skill oneOf const branches,
  and per-skill allOf contains clauses are generated from the map, ending the
  map/schema double-maintenance;
- count words (eleven..thirty) on every live surface — README, GEMINI.md, the
  router SKILL.md, and all harness manifests.

Python enumeration homes (verifier constants, test expectations) and the
router's frontmatter skill list stay hand-edited by design — they are cheap,
rare edits — but ``--check`` verifies them by import and reports exactly what
is missing. Stdlib only.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "plugins" / "epistemic-skills"
SKILLS_DIR = PACKAGE / "skills"
EVENTS_DIR = PACKAGE / "contracts" / "epistemic-events"
MAP_PATH = EVENTS_DIR / "skill-event-map.json"
MAP_SCHEMA_PATH = EVENTS_DIR / "skill-event-map.schema.json"
VERIFIER_PATH = EVENTS_DIR / "verify_epistemic_event.py"
EVENTS_TEST_PATH = EVENTS_DIR / "test_epistemic_events.py"
COMPOSITION_PATH = PACKAGE / "skills" / "helix" / "reference" / "composition-contract.json"
ROUTER_PATH = SKILLS_DIR / "using-epistemic-skills" / "SKILL.md"

NON_DISCIPLINES = {"using-epistemic-skills", "helix"}

WORDS = {
    9: "nine", 10: "ten",
    11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
    16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
    20: "twenty", 21: "twenty-one", 22: "twenty-two", 23: "twenty-three",
    24: "twenty-four", 25: "twenty-five", 26: "twenty-six",
    27: "twenty-seven", 28: "twenty-eight", 29: "twenty-nine", 30: "thirty",
}
ANY_WORD = "(?:" + "|".join(sorted(WORDS.values(), key=len, reverse=True)) + ")"
ANY_WORD_CAP = "(?:" + "|".join(w.capitalize() for w in sorted(WORDS.values(), key=len, reverse=True)) + ")"

# Count-bearing surfaces. Each entry: (path, [(pattern, template)]).
# {n}/{N} = total skill count word (lower/Title), {d}/{D} = discipline count
# word, {slug} = lowercase total word for anchors. Patterns are anchored with
# enough fixed context to never touch the historical per-version counts.


def count_surfaces() -> list[tuple[Path, list[tuple[str, str]]]]:
    return [
        (REPO / "README.md", [
            (rf"- \[{ANY_WORD_CAP}-skill catalog\]\(#{ANY_WORD}-skill-catalog\)",
             "- [{N}-skill catalog](#{slug}-skill-catalog)"),
            (rf"## {ANY_WORD_CAP}-skill catalog", "## {N}-skill catalog"),
            (rf"provides \*\*{ANY_WORD}\*\* skills: one router, \*\*{ANY_WORD}\*\* disciplines",
             "provides **{n}** skills: one router, **{d}** disciplines"),
            (rf"one router, Helix, and {ANY_WORD} disciplines",
             "one router, Helix, and {d} disciplines"),
            (rf"canonical skill cores \({ANY_WORD}\)", "canonical skill cores ({n})"),
            (rf"router and {ANY_WORD} disciplines", "router and {d} disciplines"),
            (rf"a v4\.0\.0 package or tagged checkout ships {ANY_WORD} ",
             "a v4.1.0 package or tagged checkout ships {n} "),
        ]),
        (REPO / "GEMINI.md", [
            (rf"{ANY_WORD} skills: router \+ {ANY_WORD} disciplines",
             "{n} skills: router + {d} disciplines"),
        ]),
        (ROUTER_PATH, [
            (rf"These {ANY_WORD} disciplines are one system",
             "These {d} disciplines are one system"),
            (rf"why these {ANY_WORD}, and not others", "why these {d}, and not others"),
        ]),
        (REPO / ".claude-plugin" / "marketplace.json", [
            (rf"One package, {ANY_WORD} self-triggering skills",
             "One package, {n} self-triggering skills"),
        ]),
        (REPO / ".cursor-plugin" / "marketplace.json", [
            (rf"One package, {ANY_WORD} self-triggering skills",
             "One package, {n} self-triggering skills"),
        ]),
        (REPO / ".cursor-plugin" / "plugin.json", [
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
        ]),
        (REPO / ".kimi-plugin" / "plugin.json", [
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
            (rf"{ANY_WORD_CAP} composable disciplines", "{D} composable disciplines"),
        ]),
        (REPO / "gemini-extension.json", [
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
        ]),
        (PACKAGE / ".claude-plugin" / "plugin.json", [
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
        ]),
        (PACKAGE / ".codex-plugin" / "plugin.json", [
            (rf"A router plus {ANY_WORD} composable disciplines",
             "A router plus {d} composable disciplines"),
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
        ]),
        (PACKAGE / ".cursor-plugin" / "plugin.json", [
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
        ]),
        (PACKAGE / ".kimi-plugin" / "plugin.json", [
            (rf"a router plus {ANY_WORD} disciplines", "a router plus {d} disciplines"),
            (rf"{ANY_WORD_CAP} composable disciplines", "{D} composable disciplines"),
        ]),
    ]


def discovered_skills() -> set[str]:
    return {p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}


def load_map() -> list[dict]:
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))["skills"]


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def branch_for(entry: dict) -> str:
    """One compact oneOf const branch, matching the schema's native style."""
    return json.dumps({
        "type": "object",
        "additionalProperties": False,
        "required": ["skill", "event_kinds", "eligible_when", "outcome_sources",
                     "collection_mode", "sentinel_fixture"],
        "properties": {
            "skill": {"const": entry["skill"]},
            "event_kinds": {"const": entry["event_kinds"]},
            "eligible_when": {"const": entry["eligible_when"]},
            "outcome_sources": {"const": entry["outcome_sources"]},
            "collection_mode": {"const": entry["collection_mode"]},
            "sentinel_fixture": {"const": entry["sentinel_fixture"]},
        },
    }, separators=(",", ":"))


def contains_for(skill: str) -> str:
    return json.dumps({
        "contains": {"type": "object", "required": ["skill"],
                     "properties": {"skill": {"const": skill}}},
        "minContains": 1, "maxContains": 1,
    }, separators=(",", ":"))


def render_map_schema(entries: list[dict]) -> str:
    branches = ",\n          ".join(branch_for(e) for e in entries)
    contains = ",\n        ".join(contains_for(e["skill"]) for e in entries)
    n = len(entries)
    return f"""{{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://zms-labs.github.io/epistemic-skills/contracts/skill-event-map.schema.json",
  "title": "Epistemic Skill Event Eligibility Map",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "skills"
  ],
  "properties": {{
    "skills": {{
      "type": "array",
      "minItems": {n},
      "maxItems": {n},
      "items": {{
        "oneOf": [
          {branches}
        ]
      }},
      "allOf": [
        {contains}
      ]
    }}
  }}
}}
"""


def apply_counts(write: bool, n_total: int, n_disc: int, failures: list[str]) -> None:
    values = {
        "n": WORDS[n_total], "N": WORDS[n_total].capitalize(),
        "d": WORDS[n_disc], "D": WORDS[n_disc].capitalize(),
        "slug": WORDS[n_total],
    }
    for path, rules in count_surfaces():
        if not path.is_file():
            failures.append(f"COUNT_SURFACE_MISSING: {path.relative_to(REPO)}")
            continue
        text = path.read_text(encoding="utf-8")
        changed = text
        for pattern, template in rules:
            expected = template.format(**values)
            if expected in changed:
                continue
            new, hits = re.subn(pattern, expected.replace("\\", r"\\"), changed)
            if hits == 0:
                failures.append(
                    f"COUNT_PATTERN_MISSING: {path.relative_to(REPO)} has no match for /{pattern}/")
                continue
            changed = new
            if not write:
                failures.append(
                    f"COUNT_DRIFT: {path.relative_to(REPO)} does not carry '{expected}'")
        if write and changed != text:
            path.write_text(changed, encoding="utf-8")
            print(f"wrote counts: {path.relative_to(REPO)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    failures: list[str] = []

    skills = discovered_skills()
    disciplines = skills - NON_DISCIPLINES
    entries = load_map()
    map_skills = {e["skill"] for e in entries}

    # Source agreement: filesystem vs the map.
    if map_skills != skills:
        failures.append(
            "MAP_GLOB_DRIFT: skill-event-map.json != skills/ glob "
            f"(map-only={sorted(map_skills - skills)}, fs-only={sorted(skills - map_skills)})")

    # Derived: map schema.
    rendered = render_map_schema(entries)
    if MAP_SCHEMA_PATH.read_text(encoding="utf-8") != rendered:
        if args.write:
            MAP_SCHEMA_PATH.write_text(rendered, encoding="utf-8")
            print(f"wrote: {MAP_SCHEMA_PATH.relative_to(REPO)}")
        else:
            failures.append(
                "MAP_SCHEMA_DRIFT: skill-event-map.schema.json is not the rendering of "
                "skill-event-map.json (run sync_skill_surfaces.py --write)")

    # Checked (hand-edited) Python homes.
    verifier = import_module(VERIFIER_PATH, "sync_verifier")
    if set(verifier.SKILL_NAMES) != skills:
        failures.append(
            f"VERIFIER_SKILL_NAMES_DRIFT: add/remove {sorted(set(verifier.SKILL_NAMES) ^ skills)}")
    expected_map = {
        e["skill"]: {
            "event_kinds": tuple(e["event_kinds"]),
            "eligible_when": tuple(e["eligible_when"]),
            "outcome_sources": tuple(e["outcome_sources"]),
            "collection_mode": e["collection_mode"],
            "sentinel_fixture": e["sentinel_fixture"],
        }
        for e in entries
    }
    if verifier.SKILL_EVENT_MAP != expected_map:
        diff = {k for k in expected_map.keys() | verifier.SKILL_EVENT_MAP.keys()
                if expected_map.get(k) != verifier.SKILL_EVENT_MAP.get(k)}
        failures.append(f"VERIFIER_EVENT_MAP_DRIFT: entries differ for {sorted(diff)}")
    map_kinds = {k for e in entries for k in e["event_kinds"]}
    if not map_kinds <= set(verifier.EVENT_KINDS):
        failures.append(
            f"VERIFIER_EVENT_KINDS_DRIFT: missing {sorted(map_kinds - set(verifier.EVENT_KINDS))}")

    events_test = import_module(EVENTS_TEST_PATH, "sync_events_test")
    if set(events_test.EXPECTED_SKILLS) != skills:
        failures.append(
            f"TEST_EXPECTED_SKILLS_DRIFT: add/remove {sorted(set(events_test.EXPECTED_SKILLS) ^ skills)}")

    composition = json.loads(COMPOSITION_PATH.read_text(encoding="utf-8"))
    members = set(composition.get("members", {}))
    if members != disciplines:
        failures.append(
            f"COMPOSITION_MEMBER_DRIFT: add/remove {sorted(members ^ disciplines)}")

    router_text = ROUTER_PATH.read_text(encoding="utf-8")
    front = router_text.split("---", 2)[1]
    listed = {name for name in disciplines if re.search(rf"\b{re.escape(name)}\b", front)}
    if listed != disciplines:
        failures.append(
            f"ROUTER_DESCRIPTION_DRIFT: frontmatter omits {sorted(disciplines - listed)}")

    # Counts everywhere.
    apply_counts(args.write, len(skills), len(disciplines), failures)

    if failures and not args.write:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1
    if failures:  # --write fixed what it could; report what it could not
        remaining = [f for f in failures if not f.startswith("COUNT_DRIFT")]
        for failure in remaining:
            print(failure, file=sys.stderr)
        if remaining:
            return 1
    print(f"skill surfaces in sync: {len(skills)} skills, {len(disciplines)} disciplines")
    return 0


if __name__ == "__main__":
    sys.exit(main())
