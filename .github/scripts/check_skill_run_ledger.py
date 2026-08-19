#!/usr/bin/env python3
"""Intrinsic skill-run ledger contract check (v5 design D7; es#104 section 2).

Every packaged skill must carry the intrinsic evidence-emission step in its
own SKILL.md and ship a valid `runs/ledger.example.jsonl` exemplar. The one
exception is `gauntlet`, whose richer Step-9 mechanism (finalize_run.py run
record + derived ledger-v2 line) predates and supersedes the generic block;
its SKILL.md must still name its own `runs/ledger.jsonl`.

Validation rules are DERIVED from
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json` at run time
(required set, property allowlist, `schema` const, `decision` enum, field
types) — this script carries no second copy of the contract.

Real ledgers are runtime-local state (git-ignored, `**/runs/*.jsonl`); the
tracked surfaces are the SKILL.md step, the schema, and the example lines.

Usage:
  python check_skill_run_ledger.py             # validate the tree
  python check_skill_run_ledger.py --self-test # planted RED controls

Exit codes: 0 ok - 1 violations (named) - 2 invalid invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = REPO_ROOT / "plugins/epistemic-skills/skills"
SCHEMA_PATH = (
    REPO_ROOT / "plugins/epistemic-skills/contracts/skill-run-ledger.schema.json"
)
BLOCK_HEADING = "## Evidence emission"
BLOCK_SCHEMA_TOKEN = '"schema":"skill-run@1"'
GAUNTLET_TOKEN = "runs/ledger.jsonl"

TYPE_CHECKS = {
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def load_schema(path: Path) -> dict:
    schema = json.loads(path.read_text(encoding="utf-8"))
    for key in ("required", "properties"):
        if key not in schema:
            raise SystemExit(f"schema missing '{key}': {path}")
    return schema


def _type_ok(spec: dict, value: object) -> bool:
    if "const" in spec:
        return value == spec["const"]
    if "enum" in spec:
        return value in spec["enum"]
    declared = spec.get("type")
    if declared is None:
        return True
    types = declared if isinstance(declared, list) else [declared]
    for t in types:
        checker = TYPE_CHECKS.get(t)
        if checker is not None and checker(value):
            if t == "string" and spec.get("minLength") and len(value) < spec["minLength"]:
                continue
            return True
    return False


def validate_line(schema: dict, raw: str, skill: str, where: str) -> list[str]:
    problems: list[str] = []
    try:
        record = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"LEDGER_LINE_UNPARSEABLE: {where}: {exc}"]
    if not isinstance(record, dict):
        return [f"LEDGER_LINE_NOT_OBJECT: {where}"]
    allowed = set(schema["properties"])
    for key in record:
        if key not in allowed:
            problems.append(f"LEDGER_UNKNOWN_FIELD: {where}: '{key}'")
    for key in schema["required"]:
        if key not in record:
            problems.append(f"LEDGER_MISSING_FIELD: {where}: '{key}'")
    for key, spec in schema["properties"].items():
        if key in record and not _type_ok(spec, record[key]):
            problems.append(f"LEDGER_FIELD_INVALID: {where}: '{key}'={record[key]!r}")
    if record.get("skill") not in (None, skill):
        problems.append(
            f"LEDGER_SKILL_MISMATCH: {where}: '{record.get('skill')}' != '{skill}'"
        )
    return problems


def check_tree(skills_root: Path, schema: dict) -> list[str]:
    problems: list[str] = []
    skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())
    if not skill_dirs:
        return [f"NO_SKILLS_FOUND: {skills_root}"]
    for skill_dir in skill_dirs:
        skill = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"SKILL_MD_MISSING: {skill}")
            continue
        text = skill_md.read_text(encoding="utf-8")
        if skill == "gauntlet":
            if GAUNTLET_TOKEN not in text:
                problems.append(
                    f"LEDGER_STEP_MISSING: {skill}: Step-9 mechanism must name "
                    f"'{GAUNTLET_TOKEN}'"
                )
        elif BLOCK_HEADING not in text or BLOCK_SCHEMA_TOKEN not in text:
            problems.append(
                f"LEDGER_STEP_MISSING: {skill}: SKILL.md lacks the "
                f"'{BLOCK_HEADING}' append step"
            )
        example = skill_dir / "runs" / "ledger.example.jsonl"
        if not example.is_file():
            problems.append(f"LEDGER_EXAMPLE_MISSING: {skill}")
            continue
        lines = [
            line
            for line in example.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if not lines:
            problems.append(f"LEDGER_EXAMPLE_EMPTY: {skill}")
        if skill == "gauntlet":
            # gauntlet's exemplar is its own richer ledger@2 projection
            # (schema prose in skills/gauntlet/runs/README.md, derived by
            # finalize_run.py). Assert it parses and declares that kind;
            # do not force skill-run@1 onto it.
            for i, line in enumerate(lines, 1):
                where = f"{skill}/runs/ledger.example.jsonl:{i}"
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    problems.append(f"LEDGER_LINE_UNPARSEABLE: {where}: {exc}")
                    continue
                if record.get("schema") != "ledger@2":
                    problems.append(
                        f"LEDGER_FIELD_INVALID: {where}: gauntlet exemplar must "
                        f"declare schema 'ledger@2', got {record.get('schema')!r}"
                    )
            continue
        for i, line in enumerate(lines, 1):
            problems.extend(
                validate_line(schema, line, skill, f"{skill}/runs/ledger.example.jsonl:{i}")
            )
    return problems


def self_test() -> int:
    schema = load_schema(SCHEMA_PATH)
    good = (
        '{"schema":"skill-run@1","ts":"2026-08-18T00:00:00Z","skill":"demo",'
        '"decision":"fired","discipline_engaged":"probe","action_changed":true,'
        '"example":true}'
    )
    planted: list[tuple[str, str, str]] = [
        ("missing-required-field",
         '{"schema":"skill-run@1","ts":"t","skill":"demo","decision":"fired",'
         '"discipline_engaged":null}',
         "LEDGER_MISSING_FIELD"),
        ("bad-decision-enum",
         good.replace('"fired"', '"maybe"'), "LEDGER_FIELD_INVALID"),
        ("unknown-extra-field",
         good[:-1] + ',"smuggled":1}', "LEDGER_UNKNOWN_FIELD"),
        ("skill-directory-mismatch",
         good.replace('"demo"', '"other"'), "LEDGER_SKILL_MISMATCH"),
        ("wrong-schema-const",
         good.replace("skill-run@1", "skill-run@9"), "LEDGER_FIELD_INVALID"),
    ]
    failures = 0
    if validate_line(schema, good, "demo", "self-test"):
        failures += 1
        print("[FAIL] honest line rejected")
    for name, raw, expected in planted:
        problems = validate_line(schema, raw, "demo", "self-test")
        if any(p.startswith(expected) for p in problems):
            print(f"[PASS] planted {name} fails closed")
        else:
            failures += 1
            print(f"[FAIL] planted {name} not rejected: {problems}")
    with tempfile.TemporaryDirectory() as tmp:
        skill = Path(tmp) / "skills" / "demo"
        (skill / "runs").mkdir(parents=True)
        (skill / "SKILL.md").write_text("# demo\nno emission step here\n")
        (skill / "runs" / "ledger.example.jsonl").write_text(
            good.replace('"demo"', '"demo"') + "\n"
        )
        problems = check_tree(Path(tmp) / "skills", schema)
        if any(p.startswith("LEDGER_STEP_MISSING") for p in problems):
            print("[PASS] planted SKILL.md-without-step fails closed")
        else:
            failures += 1
            print(f"[FAIL] planted missing step not rejected: {problems}")
    print(f"skill-run ledger self-test: {'PASS' if not failures else 'FAIL'}")
    return 0 if not failures else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    schema = load_schema(SCHEMA_PATH)
    problems = check_tree(SKILLS_ROOT, schema)
    if problems:
        for p in problems:
            print(f"skill-run ledger violation: {p}", file=sys.stderr)
        return 1
    count = len([p for p in SKILLS_ROOT.iterdir() if p.is_dir()])
    print(
        f"skill-run ledger contract ok: {count} skills carry the intrinsic "
        f"emission step (gauntlet via its Step-9 mechanism) and valid example lines"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
