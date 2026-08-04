#!/usr/bin/env python3
"""Fail-closed suite-wide skill inventory contract.

Drift disease this prevents: the suite's skill inventory is enumerated in
several independently frozen homes — the epistemic-event schema's
``producer.skill`` enum, ``skill-event-map.json``, the verifier's
``SKILL_NAMES``, and the enforcement-language audit's ``SKILL_PATHS`` — and
frozen copies rot silently as skills are added. Before this contract existed,
three of those frozen inventories had drifted to 10/11 of the 17 packaged
skills. This check pins every enumerating home to the one ground truth that
cannot drift: the filesystem glob of packaged skill directories that contain
a ``SKILL.md``. Any mismatch is a named violation and a non-zero exit; any
unreadable surface fails closed the same way.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / "plugins" / "epistemic-skills" / "skills"
EVENTS_ROOT = REPO_ROOT / "plugins" / "epistemic-skills" / "contracts" / "epistemic-events"
EVENT_SCHEMA_PATH = EVENTS_ROOT / "epistemic-event.schema.json"
SKILL_EVENT_MAP_PATH = EVENTS_ROOT / "skill-event-map.json"
VERIFIER_PATH = EVENTS_ROOT / "verify_epistemic_event.py"
AUDIT_PATH = (
    SKILLS_ROOT
    / "using-epistemic-skills"
    / "evals"
    / "epistemic-flexibility"
    / "audit_enforcement_language.py"
)
AUDIT_PATH_PREFIX = "plugins/epistemic-skills/skills/"


class InventoryError(ValueError):
    """A named, fail-closed rejection of an inventory surface."""

    def __init__(self, name: str, detail: str):
        self.name = name
        self.detail = detail
        super().__init__(f"{name}: {detail}")


def _sorted_names(names: Iterable[str]) -> str:
    return ", ".join(sorted(names))


def load_module(path: Path, module_name: str):
    """Import a Python surface from its path, failing closed on any error."""
    if not path.is_file():
        raise InventoryError("MISSING_SURFACE", f"{path} does not exist")
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise InventoryError("UNIMPORTABLE_SURFACE", f"cannot build a spec for {path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as error:  # noqa: BLE001 — every import failure fails closed
        raise InventoryError("UNIMPORTABLE_SURFACE", f"{path} failed to import: {error}")
    return module


def load_json(path: Path) -> object:
    if not path.is_file():
        raise InventoryError("MISSING_SURFACE", f"{path} does not exist")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise InventoryError("MALFORMED_SURFACE", f"{path} is not readable JSON: {error}")


def packaged_skills(skills_root: Path) -> set[str]:
    """The one ground truth: skill directories that carry a SKILL.md."""
    if not skills_root.is_dir():
        raise InventoryError("MISSING_SURFACE", f"{skills_root} is not a directory")
    packaged = {
        entry.name
        for entry in sorted(skills_root.iterdir())
        if entry.is_dir() and (entry / "SKILL.md").is_file()
    }
    if not packaged:
        raise InventoryError("EMPTY_SKILL_GLOB", f"no SKILL.md-bearing directories under {skills_root}")
    return packaged


def schema_skill_enum(schema: object) -> list[str]:
    try:
        enum = schema["properties"]["producer"]["properties"]["skill"]["enum"]  # type: ignore[index]
    except (KeyError, TypeError):
        raise InventoryError(
            "MALFORMED_SURFACE",
            "epistemic-event schema has no properties.producer.properties.skill.enum",
        )
    if not isinstance(enum, list) or not all(isinstance(item, str) for item in enum):
        raise InventoryError("MALFORMED_SURFACE", "producer.skill enum is not a list of strings")
    return enum


def map_skill_entries(mapping: object) -> list[dict]:
    if not isinstance(mapping, dict) or not isinstance(mapping.get("skills"), list):
        raise InventoryError("MALFORMED_SURFACE", "skill-event-map.json has no skills list")
    entries = mapping["skills"]
    if not all(isinstance(entry, dict) and isinstance(entry.get("skill"), str) for entry in entries):
        raise InventoryError("MALFORMED_SURFACE", "skill-event-map.json entry lacks a string skill name")
    return entries


def check_inventory(
    packaged: set[str],
    schema_enum: list[str],
    map_entries: list[dict],
    verifier_names: set[str],
    audit_paths: list[str],
    path_exists: Callable[[str], bool],
) -> list[str]:
    """Compare every enumerating home against the packaged glob; return named violations."""
    violations: list[str] = []

    enum_set = set(schema_enum)
    if len(schema_enum) != len(enum_set):
        violations.append("SCHEMA_ENUM_DRIFT: producer.skill enum contains duplicates")
    if enum_set != packaged:
        missing = packaged - enum_set
        unknown = enum_set - packaged
        if missing:
            violations.append(
                f"SCHEMA_ENUM_DRIFT: producer.skill enum is missing packaged skills: {_sorted_names(missing)}"
            )
        if unknown:
            violations.append(
                f"SCHEMA_ENUM_DRIFT: producer.skill enum names unpackaged skills: {_sorted_names(unknown)}"
            )

    map_names = [entry["skill"] for entry in map_entries]
    map_set = set(map_names)
    if len(map_names) != len(map_set):
        duplicated = {name for name in map_names if map_names.count(name) > 1}
        violations.append(
            f"MAP_SKILL_DRIFT: skill-event-map.json repeats skills: {_sorted_names(duplicated)}"
        )
    if map_set != packaged:
        missing = packaged - map_set
        unknown = map_set - packaged
        if missing:
            violations.append(
                f"MAP_SKILL_DRIFT: skill-event-map.json is missing packaged skills: {_sorted_names(missing)}"
            )
        if unknown:
            violations.append(
                f"MAP_SKILL_DRIFT: skill-event-map.json names unpackaged skills: {_sorted_names(unknown)}"
            )

    if verifier_names != packaged:
        missing = packaged - verifier_names
        unknown = verifier_names - packaged
        if missing:
            violations.append(
                f"VERIFIER_SKILL_DRIFT: verifier SKILL_NAMES is missing packaged skills: {_sorted_names(missing)}"
            )
        if unknown:
            violations.append(
                f"VERIFIER_SKILL_DRIFT: verifier SKILL_NAMES names unpackaged skills: {_sorted_names(unknown)}"
            )

    for audit_path in audit_paths:
        parts = audit_path.split("/")
        # A valid audited surface is the skill core (skills/<name>/SKILL.md) or a
        # consolidated mode/instrument method (skills/<name>/<subtree>/METHOD.md,
        # v4.0.0) — always inside a packaged skill directory.
        valid_core = len(parts) == 5 and parts[4] == "SKILL.md"
        valid_method = len(parts) == 6 and (
            parts[5] == "METHOD.md"
            or (parts[4] == "reference" and parts[5].startswith("mode-") and parts[5].endswith(".md"))
        )
        if (
            not audit_path.startswith(AUDIT_PATH_PREFIX)
            or not (valid_core or valid_method)
            or parts[3] not in packaged
        ):
            violations.append(
                f"AUDIT_PATH_ESCAPE: audited path is outside the packaged skill inventory: {audit_path}"
            )
            continue
        if not path_exists(audit_path):
            violations.append(f"AUDIT_PATH_MISSING: audited path does not exist: {audit_path}")

    for entry in map_entries:
        sentinel = entry.get("sentinel_fixture")
        if not isinstance(sentinel, str) or not sentinel.strip():
            violations.append(
                f"EMPTY_SENTINEL_FIXTURE: skill-event-map.json entry for {entry['skill']!r} "
                "lacks a non-empty sentinel_fixture"
            )

    return violations


def run_check() -> int:
    try:
        packaged = packaged_skills(SKILLS_ROOT)
        schema_enum = schema_skill_enum(load_json(EVENT_SCHEMA_PATH))
        map_entries = map_skill_entries(load_json(SKILL_EVENT_MAP_PATH))
        verifier = load_module(VERIFIER_PATH, "inventory_verify_epistemic_event")
        verifier_names = set(getattr(verifier, "SKILL_NAMES", None) or ())
        if not verifier_names:
            raise InventoryError("MALFORMED_SURFACE", f"{VERIFIER_PATH} exports no SKILL_NAMES")
        audit = load_module(AUDIT_PATH, "inventory_audit_enforcement_language")
        audit_paths = list(getattr(audit, "SKILL_PATHS", None) or ())
        if not audit_paths:
            raise InventoryError("MALFORMED_SURFACE", f"{AUDIT_PATH} exports no SKILL_PATHS")
    except InventoryError as error:
        print(f"VIOLATION {error}", file=sys.stderr)
        return 1
    violations = check_inventory(
        packaged,
        schema_enum,
        map_entries,
        verifier_names,
        audit_paths,
        lambda relative: (REPO_ROOT / relative).is_file(),
    )
    if violations:
        for violation in violations:
            print(f"VIOLATION {violation}", file=sys.stderr)
        return 1
    print(
        "skill inventory contract ok: "
        f"{len(packaged)} packaged skills; schema enum, event map, and verifier SKILL_NAMES "
        f"match the glob exactly; {len(audit_paths)} audited paths inside the inventory; "
        "every map entry carries a sentinel fixture"
    )
    return 0


def run_self_test() -> int:
    """Plant synthetic mismatches in-memory and prove every check fails closed."""
    packaged = {"alpha-skill", "beta-skill"}
    aligned_entries = [
        {"skill": "alpha-skill", "sentinel_fixture": "alpha.json"},
        {"skill": "beta-skill", "sentinel_fixture": "beta.json"},
    ]
    aligned_paths = [
        "plugins/epistemic-skills/skills/alpha-skill/SKILL.md",
        "plugins/epistemic-skills/skills/beta-skill/SKILL.md",
    ]

    def run(schema_enum, map_entries, verifier_names, audit_paths, path_exists):
        return check_inventory(
            packaged, schema_enum, map_entries, verifier_names, audit_paths, path_exists
        )

    failures: list[str] = []
    baseline = run(
        ["alpha-skill", "beta-skill"], aligned_entries, set(packaged), aligned_paths, lambda _: True
    )
    if baseline:
        failures.append(f"aligned baseline must pass, got: {baseline}")

    probes = {
        "SCHEMA_ENUM_DRIFT": run(
            ["alpha-skill"], aligned_entries, set(packaged), aligned_paths, lambda _: True
        ),
        "MAP_SKILL_DRIFT": run(
            ["alpha-skill", "beta-skill"],
            aligned_entries + [{"skill": "ghost-skill", "sentinel_fixture": "ghost.json"}],
            set(packaged),
            aligned_paths,
            lambda _: True,
        ),
        "VERIFIER_SKILL_DRIFT": run(
            ["alpha-skill", "beta-skill"],
            aligned_entries,
            {"alpha-skill"},
            aligned_paths,
            lambda _: True,
        ),
        "AUDIT_PATH_ESCAPE": run(
            ["alpha-skill", "beta-skill"],
            aligned_entries,
            set(packaged),
            aligned_paths + ["plugins/epistemic-skills/skills/ghost-skill/SKILL.md"],
            lambda _: True,
        ),
        "AUDIT_PATH_MISSING": run(
            ["alpha-skill", "beta-skill"],
            aligned_entries,
            set(packaged),
            aligned_paths,
            lambda _: False,
        ),
        "EMPTY_SENTINEL_FIXTURE": run(
            ["alpha-skill", "beta-skill"],
            [{"skill": "alpha-skill", "sentinel_fixture": "alpha.json"},
             {"skill": "beta-skill", "sentinel_fixture": "   "}],
            set(packaged),
            aligned_paths,
            lambda _: True,
        ),
    }
    for expected_name, violations in probes.items():
        if not any(violation.startswith(expected_name) for violation in violations):
            failures.append(f"planted {expected_name} mismatch was not detected: {violations}")

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAILURE: {failure}", file=sys.stderr)
        return 1
    print(f"skill inventory self-test ok: {len(probes)} planted mismatches all failed closed")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Suite-wide skill inventory contract")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="plant synthetic in-memory mismatches and prove the check fails closed",
    )
    arguments = parser.parse_args(argv)
    if arguments.self_test:
        return run_self_test()
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
