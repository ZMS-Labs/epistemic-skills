#!/usr/bin/env python3
"""Single-source synchronization for every skill-inventory surface.

The hand-edited source of truth is exactly one:

1. the filesystem — ``plugins/epistemic-skills/skills/<name>/`` defines which
   skills exist, and each skill's OWN ``SKILL.md`` frontmatter ``metadata:``
   block declares its event metadata (``event-kinds``, ``eligible-when``,
   ``outcome-sources``, ``collection-mode``, ``sentinel-fixture``) alongside
   ``hands-to``.

``contracts/epistemic-events/skill-event-map.json`` is now a DERIVED surface,
generated from those frontmatter declarations (v5 design "structural
membership", es#104 s4 Option A: one generated source, so a second
hand-maintained membership home cannot drift). Everything else derives too. ``--check`` (the CI mode) verifies every
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

``--self-test`` is the planted-drift RED battery: on a scratch copy of the
tree, each named detector (MAP_DRIFT, MAP_SCHEMA_DRIFT, ROUTING_DRIFT,
COUNT_DRIFT, EVENT_METADATA_MISSING, HANDS_TO_UNKNOWN,
VERIFIER_SKILL_NAMES_DRIFT) must fire on its deliberately tampered surface
and stay silent on the honest copy — proof the checks watch rather than
pass vacuously.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "plugins" / "epistemic-skills"
SKILLS_DIR = PACKAGE / "skills"
EVENTS_DIR = PACKAGE / "contracts" / "epistemic-events"
MAP_PATH = EVENTS_DIR / "skill-event-map.json"
MAP_SCHEMA_PATH = EVENTS_DIR / "skill-event-map.schema.json"
VERIFIER_PATH = EVENTS_DIR / "verify_epistemic_event.py"
EVENTS_TEST_PATH = EVENTS_DIR / "test_epistemic_events.py"
EVENT_SCHEMA_PATH = EVENTS_DIR / "epistemic-event.schema.json"
ROUTING_PATH = PACKAGE / "ROUTING.md"
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---", re.S)
GENERATED_BEGIN = "# BEGIN GENERATED SKILL INVENTORY"
GENERATED_END = "# END GENERATED SKILL INVENTORY"

# The entry point is not a discipline. Was {router, helix}; both seats were
# deleted 2026-08-06 and replaced by metacognate, so the arithmetic is n-1.
NON_DISCIPLINES = {"metacognate"}

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
            (rf"provides \*\*{ANY_WORD}\*\* skills: (?:one router|one entry point), \*\*{ANY_WORD}\*\* disciplines",
             "provides **{n}** skills: one entry point, **{d}** disciplines"),
            (rf"(?:one router, Helix, and|one entry point and) {ANY_WORD} disciplines",
             "one entry point and {d} disciplines"),
            (rf"canonical skill cores \({ANY_WORD}\)", "canonical skill cores ({n})"),
            (rf"(?:router and|entry point and) {ANY_WORD} disciplines", "entry point and {d} disciplines"),
            # REMOVED 2026-08-06: a one-shot v4.0.0 -> v4.1.0 migration rule that
            # rewrote the per-RELEASE install-verification count from the CURRENT
            # glob. Two defects. (1) It contradicted this file's own stated intent
            # four lines above — "never touch the historical per-version counts" —
            # because what a released tag ships is a historical fact and cannot be
            # derived from today's tree. (2) Its anchor was consumed the first time
            # it ran, so it could never match again and raised COUNT_PATTERN_MISSING
            # on every subsequent skill addition, silently blocking them.
            # Release counts stay hand-written. Only counts describing the CURRENT
            # tree are generated.
        ]),
        (REPO / "GEMINI.md", [
            (rf"{ANY_WORD} skills: (?:router|entry point) \+ {ANY_WORD} disciplines",
             "{n} skills: entry point + {d} disciplines"),
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
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
        ]),
        (REPO / ".kimi-plugin" / "plugin.json", [
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
            (rf"{ANY_WORD_CAP} composable disciplines", "{D} composable disciplines"),
        ]),
        (REPO / "gemini-extension.json", [
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
        ]),
        # ADDED 2026-08-06: the ROOT plugin.json carries the same phrase as
        # gemini-extension.json and the package manifests below, but was never
        # listed here — so it was the one live surface the generator did not
        # maintain. It went stale on every skill addition and was caught only by
        # the outsource suite's count lint, one release late. A generator that
        # covers all-but-one instance of a phrase is worse than none: it makes the
        # remaining hand-edit invisible.
        (REPO / "plugin.json", [
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
        ]),
        (PACKAGE / ".claude-plugin" / "plugin.json", [
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
        ]),
        (PACKAGE / ".codex-plugin" / "plugin.json", [
            (rf"(?:A router plus|An entry point plus) {ANY_WORD} composable disciplines",
             "An entry point plus {d} composable disciplines"),
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
        ]),
        (PACKAGE / ".cursor-plugin" / "plugin.json", [
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
        ]),
        (PACKAGE / ".kimi-plugin" / "plugin.json", [
            (rf"(?:a router plus|an entry point plus) {ANY_WORD} disciplines", "an entry point plus {d} disciplines"),
            (rf"{ANY_WORD_CAP} composable disciplines", "{D} composable disciplines"),
        ]),
    ]


def discovered_skills() -> set[str]:
    return {p.name for p in SKILLS_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").is_file()}


def load_map() -> list[dict]:
    return json.loads(MAP_PATH.read_text(encoding="utf-8"))["skills"]


def parse_hands_to(skill_md: Path) -> list[str]:
    text = skill_md.read_text(encoding="utf-8")
    front = FRONTMATTER.match(text)
    if not front:
        return []
    match = re.search(r"hands-to:\s*\[(.*?)\]", front.group(1))
    if not match:
        return []
    return [part.strip().strip("'\"") for part in match.group(1).split(",") if part.strip()]


EVENT_META_KEYS = {
    "event-kinds": ("event_kinds", True),
    "eligible-when": ("eligible_when", True),
    "outcome-sources": ("outcome_sources", True),
    "collection-mode": ("collection_mode", False),
    "sentinel-fixture": ("sentinel_fixture", False),
}


def parse_event_metadata(skill_md: Path) -> dict | None:
    """Read the frontmatter event-metadata declaration; None when incomplete."""
    text = skill_md.read_text(encoding="utf-8")
    front = FRONTMATTER.match(text)
    if not front:
        return None
    block = front.group(1)
    out: dict = {}
    for key, (field, is_list) in EVENT_META_KEYS.items():
        if is_list:
            match = re.search(rf"{key}:\s*\[(.*?)\]", block)
            if not match:
                return None
            out[field] = [p.strip().strip("'\"") for p in match.group(1).split(",") if p.strip()]
        else:
            match = re.search(rf"{key}:\s*(\S+)", block)
            if not match:
                return None
            out[field] = match.group(1).strip().strip("'\"")
    return out


def hands_to_violations(skill: str, targets: list[str], known: set[str]) -> list[str]:
    """Every hands-to target must be a real packaged skill (fail closed)."""
    return [
        f"HANDS_TO_UNKNOWN: {skill} hands-to names {t!r}, not in the skills/ glob"
        for t in targets
        if t not in known
    ]


def render_event_map(skills: set[str], failures: list[str], skills_dir: Path | None = None) -> list[dict]:
    """Derive the skill-event-map entries from per-skill frontmatter."""
    root = skills_dir or SKILLS_DIR
    entries: list[dict] = []
    for name in sorted(skills):
        meta = parse_event_metadata(root / name / "SKILL.md")
        if meta is None:
            failures.append(
                f"EVENT_METADATA_MISSING: {name}: SKILL.md frontmatter lacks a complete "
                "event-kinds/eligible-when/outcome-sources/collection-mode/sentinel-fixture block")
            continue
        entries.append({"skill": name, **meta})
    return entries


def render_event_map_text(entries: list[dict]) -> str:
    return json.dumps({"skills": entries}, indent=2) + "\n"


def render_routing(skills: set[str]) -> str:
    """Generate ROUTING.md solely from metadata.hands-to declarations."""
    lines = [
        "# ROUTING — generated from metadata.hands-to",
        "",
        "<!-- GENERATED FILE. Do not hand-edit. Regenerate with:",
        "     python .github/scripts/sync_skill_surfaces.py --write",
        "     Hash-verified in CI via sync_skill_surfaces.py --check. -->",
        "",
        "Each skill declares its consumers in portable frontmatter:",
        "",
        "```yaml",
        "metadata:",
        "  hands-to: [consumer-a, consumer-b]",
        "```",
        "",
        "This file is the only aggregate routing surface. Hand-authored routing",
        "tables are forbidden. Adding a skill costs this file nothing beyond the",
        "regeneration that CI already requires.",
        "",
        "| Skill | hands-to |",
        "|---|---|",
    ]
    for name in sorted(skills):
        targets = parse_hands_to(SKILLS_DIR / name / "SKILL.md")
        rendered = ", ".join(f"`{t}`" for t in targets) if targets else "_(none)_"
        lines.append(f"| `{name}` | {rendered} |")
    lines.append("")
    return "\n".join(lines)


def render_skill_enum(skills: set[str]) -> str:
    return json.dumps(sorted(skills))


def render_skill_names(skills: set[str]) -> str:
    names = ", ".join(repr(name) for name in sorted(skills))
    return (
        f"{GENERATED_BEGIN} SKILL_NAMES\n"
        "# Generated by sync_skill_surfaces.py from the skills/ glob.\n"
        "SKILL_NAMES = {\n"
        f"    {names},\n"
        "}\n"
        f"{GENERATED_END} SKILL_NAMES\n"
    )


def render_skill_event_map(entries: list[dict]) -> str:
    lines = [
        f"{GENERATED_BEGIN} SKILL_EVENT_MAP",
        "# Generated by sync_skill_surfaces.py from skill-event-map.json.",
        "SKILL_EVENT_MAP = {",
    ]
    for entry in sorted(entries, key=lambda row: row["skill"]):
        lines.append(f'    {entry["skill"]!r}: {{')
        lines.append(f'        "event_kinds": {tuple(entry["event_kinds"])!r},')
        lines.append(f'        "eligible_when": {tuple(entry["eligible_when"])!r},')
        lines.append(f'        "outcome_sources": {tuple(entry["outcome_sources"])!r},')
        lines.append(f'        "collection_mode": {entry["collection_mode"]!r},')
        lines.append(f'        "sentinel_fixture": {entry["sentinel_fixture"]!r},')
        lines.append("    },")
    lines.append("}")
    lines.append(f"{GENERATED_END} SKILL_EVENT_MAP")
    return "\n".join(lines) + "\n"


def render_expected_skills(skills: set[str]) -> str:
    names = ", ".join(repr(name) for name in sorted(skills))
    return (
        f"{GENERATED_BEGIN} EXPECTED_SKILLS\n"
        "# Generated by sync_skill_surfaces.py from the skills/ glob.\n"
        "EXPECTED_SKILLS = {\n"
        f"    {names},\n"
        "}\n"
        f"{GENERATED_END} EXPECTED_SKILLS\n"
    )


def replace_labeled_block(text: str, label: str, block: str, failures: list[str]) -> str:
    begin = f"{GENERATED_BEGIN} {label}"
    end = f"{GENERATED_END} {label}"
    pattern = re.compile(
        rf"{re.escape(begin)}.*?{re.escape(end)}\n?",
        re.S,
    )
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    failures.append(f"GENERATED_BLOCK_MISSING: {label}")
    return text


def replace_assignment(text: str, name: str, block: str, failures: list[str]) -> str:
    pattern = re.compile(rf"{name} = \{{.*?\n\}}\n", re.S)
    if not pattern.search(text):
        failures.append(f"ASSIGNMENT_PATTERN_MISSING: {name}")
        return text
    return pattern.sub(block, text, count=1)


def sync_schema_skill_enum(write: bool, skills: set[str], failures: list[str]) -> None:
    if not EVENT_SCHEMA_PATH.is_file():
        failures.append(f"SCHEMA_MISSING: {EVENT_SCHEMA_PATH.relative_to(REPO)}")
        return
    text = EVENT_SCHEMA_PATH.read_text(encoding="utf-8")
    rendered = render_skill_enum(skills)
    pattern = re.compile(
        r'("skill"\s*:\s*\{\s*"enum"\s*:\s*)\[.*?\]',
        re.S,
    )
    match = pattern.search(text)
    if not match:
        failures.append("SCHEMA_ENUM_PATTERN_MISSING: producer.skill enum not found")
        return
    expected = match.group(1) + rendered
    new_text, count = pattern.subn(expected.replace("\\", r"\\"), text, count=1)
    if count != 1:
        failures.append("SCHEMA_ENUM_REPLACE_FAILED")
        return
    if new_text == text:
        return
    if write:
        EVENT_SCHEMA_PATH.write_text(new_text, encoding="utf-8")
        print(f"wrote: {EVENT_SCHEMA_PATH.relative_to(REPO)} skill enum")
    else:
        failures.append(
            "SCHEMA_ENUM_DRIFT: epistemic-event.schema.json producer.skill enum is not "
            "the sorted skills/ glob (run sync_skill_surfaces.py --write)"
        )


def sync_python_inventory(write: bool, entries: list[dict], skills: set[str], failures: list[str]) -> None:
    names_block = render_skill_names(skills)
    map_block = render_skill_event_map(entries)
    verifier_text = VERIFIER_PATH.read_text(encoding="utf-8")
    new_verifier = verifier_text
    if f"{GENERATED_BEGIN} SKILL_NAMES" in verifier_text:
        local_failures: list[str] = []
        new_verifier = replace_labeled_block(new_verifier, "SKILL_NAMES", names_block, local_failures)
        new_verifier = replace_labeled_block(new_verifier, "SKILL_EVENT_MAP", map_block, local_failures)
        failures.extend(local_failures)
    else:
        local_failures = []
        new_verifier = replace_assignment(new_verifier, "SKILL_NAMES", names_block, local_failures)
        new_verifier = replace_assignment(new_verifier, "SKILL_EVENT_MAP", map_block, local_failures)
        failures.extend(local_failures)
    if new_verifier != verifier_text:
        if write and not any("MISSING" in item for item in failures[-4:]):
            VERIFIER_PATH.write_text(new_verifier, encoding="utf-8")
            print(f"wrote: {VERIFIER_PATH.relative_to(REPO)} generated inventory")
        elif not write:
            failures.append(
                "VERIFIER_INVENTORY_DRIFT: SKILL_NAMES/SKILL_EVENT_MAP are not generated "
                "(run sync_skill_surfaces.py --write)"
            )

    expected_block = render_expected_skills(skills)
    test_text = EVENTS_TEST_PATH.read_text(encoding="utf-8")
    if f"{GENERATED_BEGIN} EXPECTED_SKILLS" in test_text:
        local_failures = []
        new_test = replace_labeled_block(test_text, "EXPECTED_SKILLS", expected_block, local_failures)
        failures.extend(local_failures)
    else:
        local_failures = []
        new_test = replace_assignment(test_text, "EXPECTED_SKILLS", expected_block, local_failures)
        failures.extend(local_failures)
    if new_test != test_text:
        if write and not any("MISSING" in item for item in local_failures):
            EVENTS_TEST_PATH.write_text(new_test, encoding="utf-8")
            print(f"wrote: {EVENTS_TEST_PATH.relative_to(REPO)} EXPECTED_SKILLS")
        elif not write:
            failures.append(
                "TEST_EXPECTED_SKILLS_DRIFT: EXPECTED_SKILLS is not generated "
                "(run sync_skill_surfaces.py --write)"
            )


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


def _selftest_copy(dst: Path) -> None:
    """Materialize the minimal tree main() reads into a scratch repo root."""
    rels = [Path(".github/scripts/sync_skill_surfaces.py")]
    rels += [path.relative_to(REPO) for path, _ in count_surfaces()]
    rels.append(ROUTING_PATH.relative_to(REPO))
    for name in ("skill-event-map.json", "skill-event-map.schema.json",
                 "verify_epistemic_event.py", "test_epistemic_events.py",
                 "epistemic-event.schema.json"):
        rels.append((EVENTS_DIR / name).relative_to(REPO))
    for skill in sorted(discovered_skills()):
        rels.append((SKILLS_DIR / skill / "SKILL.md").relative_to(REPO))
    for rel in rels:
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())
    # test_epistemic_events.py resolves the repo-root skills alias at import
    # time; recreate it (symlink where possible, alias text file otherwise —
    # the same two forms root_skills_reference() accepts).
    # target_is_directory is load-bearing on NT: without it a privileged
    # Windows host creates a FILE symlink to a directory and the self-test
    # crashes deterministically (kimi ruling S8).
    try:
        (dst / "skills").symlink_to(
            "plugins/epistemic-skills/skills", target_is_directory=True)
    except OSError:
        (dst / "skills").write_text(
            "plugins/epistemic-skills/skills\n", encoding="utf-8")


def _selftest_check(root: Path) -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, str(root / ".github/scripts/sync_skill_surfaces.py"),
         "--check"],
        capture_output=True, text=True)
    return proc.returncode, proc.stderr + proc.stdout


def self_test() -> int:
    skills = sorted(discovered_skills())
    n = len(skills)
    events_rel = EVENTS_DIR.relative_to(REPO)
    skills_rel = SKILLS_DIR.relative_to(REPO)
    routing_rel = ROUTING_PATH.relative_to(REPO)

    def tamper_map(root: Path) -> None:
        path = root / events_rel / "skill-event-map.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["skills"][0]["collection_mode"] = "zz-planted"
        path.write_text(render_event_map_text(data["skills"]), encoding="utf-8")

    def tamper_schema(root: Path) -> None:
        path = root / events_rel / "skill-event-map.schema.json"
        text = path.read_text(encoding="utf-8")
        tampered = text.replace(f'"minItems": {n},', f'"minItems": {n - 1},', 1)
        assert tampered != text, "schema tamper anchor not found"
        path.write_text(tampered, encoding="utf-8")

    def tamper_routing(root: Path) -> None:
        path = root / routing_rel
        path.write_text(
            path.read_text(encoding="utf-8") + "| `zz-hand-added` | `nobody` |\n",
            encoding="utf-8")

    def tamper_count(root: Path) -> None:
        path = root / "GEMINI.md"
        text = path.read_text(encoding="utf-8")
        tampered = text.replace(f"{WORDS[n]} skills:", f"{WORDS[n - 1]} skills:", 1)
        assert tampered != text, "count tamper anchor not found"
        path.write_text(tampered, encoding="utf-8")

    def tamper_metadata(root: Path) -> None:
        path = root / skills_rel / skills[0] / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        tampered = re.sub(r"\n[ \t]*event-kinds:[^\n]*", "", text, count=1)
        assert tampered != text, "event-kinds tamper anchor not found"
        path.write_text(tampered, encoding="utf-8")

    def tamper_hands_to(root: Path) -> None:
        for skill in skills:
            path = root / skills_rel / skill / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            tampered = re.sub(
                r"hands-to:\s*\[[^\]]*\]", "hands-to: [zz-planted-phantom]",
                text, count=1)
            if tampered != text:
                path.write_text(tampered, encoding="utf-8")
                return
        raise AssertionError("no skill carries a hands-to declaration to tamper")

    def plant_new_skill(root: Path) -> None:
        new = root / skills_rel / "zz-planted-skill"
        new.mkdir(parents=True)
        (new / "SKILL.md").write_text(
            "---\n"
            "name: zz-planted-skill\n"
            "description: planted membership-drift control (self-test only)\n"
            "metadata:\n"
            "  hands-to: []\n"
            "  event-kinds: [frontier-decision]\n"
            "  eligible-when: [always]\n"
            "  outcome-sources: [self-report]\n"
            "  collection-mode: observational\n"
            "  sentinel-fixture: zz-planted.json\n"
            "---\n\n# planted\n", encoding="utf-8")

    planted: list[tuple[str, object, list[str]]] = [
        ("map-value-tamper", tamper_map, ["MAP_DRIFT"]),
        ("map-schema-tamper", tamper_schema, ["MAP_SCHEMA_DRIFT"]),
        ("routing-hand-edit", tamper_routing, ["ROUTING_DRIFT"]),
        ("count-word-tamper", tamper_count, ["COUNT_DRIFT"]),
        ("event-metadata-removal", tamper_metadata, ["EVENT_METADATA_MISSING"]),
        ("hands-to-phantom", tamper_hands_to, ["HANDS_TO_UNKNOWN"]),
        ("unregistered-new-skill", plant_new_skill,
         ["MAP_DRIFT", "VERIFIER_SKILL_NAMES_DRIFT"]),
    ]
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _selftest_copy(root)
        code, out = _selftest_check(root)
        if code == 0:
            print("[PASS] honest scratch copy checks clean")
        else:
            failures += 1
            print(f"[FAIL] honest scratch copy rejected (exit {code}):\n{out}")
    for name, mutate, expected in planted:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _selftest_copy(root)
            mutate(root)
            code, out = _selftest_check(root)
            missing = [token for token in expected if token not in out]
            if code != 0 and not missing:
                print(f"[PASS] planted {name} fails closed ({', '.join(expected)})")
            else:
                failures += 1
                print(f"[FAIL] planted {name}: exit={code} missing={missing}\n{out}")
    print(f"skill-surface generator self-test: {'PASS' if not failures else 'FAIL'}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    failures: list[str] = []

    skills = discovered_skills()
    disciplines = skills - NON_DISCIPLINES

    # Single source: entries derive from per-skill frontmatter (fail closed on
    # any incomplete declaration). The committed map is a generated projection.
    entries = render_event_map(skills, failures)
    for name in sorted(skills):
        failures.extend(
            hands_to_violations(name, parse_hands_to(SKILLS_DIR / name / "SKILL.md"), skills))
    rendered_map = render_event_map_text(entries)
    if not MAP_PATH.is_file() or MAP_PATH.read_text(encoding="utf-8") != rendered_map:
        if args.write:
            MAP_PATH.write_text(rendered_map, encoding="utf-8")
            print(f"wrote: {MAP_PATH.relative_to(REPO)}")
        else:
            failures.append(
                "MAP_DRIFT: skill-event-map.json is not the rendering of the per-skill "
                "frontmatter event metadata (run sync_skill_surfaces.py --write)")

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

    # Derived: ROUTING.md from metadata.hands-to (byte-equality == hash verify).
    routing = render_routing(skills)
    if not ROUTING_PATH.is_file() or ROUTING_PATH.read_text(encoding="utf-8") != routing:
        if args.write:
            ROUTING_PATH.write_text(routing, encoding="utf-8")
            print(f"wrote: {ROUTING_PATH.relative_to(REPO)}")
        else:
            failures.append(
                "ROUTING_DRIFT: plugins/epistemic-skills/ROUTING.md is missing or not the "
                "rendering of metadata.hands-to (run sync_skill_surfaces.py --write)")

    # Derived: schema enum + verifier/test inventories from glob + map.
    sync_schema_skill_enum(args.write, skills, failures)
    sync_python_inventory(args.write, entries, skills, failures)

    # Post-generation agreement check (import after optional write).
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


    # REMOVED 2026-08-06 with the router seat itself: ROUTER_DESCRIPTION_DRIFT
    # required the router's frontmatter to enumerate every discipline. It was the
    # single largest source of the enumeration tax — adding any skill forced an
    # edit to another skill's firing surface — and it is exactly the defect that
    # shipped in v4.0.0, where the router's description named two skills that no
    # longer existed. metacognate replaces the seat and enumerates nothing, so
    # there is no list to keep in sync and this check has nothing left to check.

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
