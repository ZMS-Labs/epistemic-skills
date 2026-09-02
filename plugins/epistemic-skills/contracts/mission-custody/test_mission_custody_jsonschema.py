#!/usr/bin/env python3
"""Execute the manifest boundary through both validation authorities.

`verify_mission_custody.py` is normative.  The checked-in JSON Schema is a
secondary consumer contract, so this suite uses a real Draft 2020-12 engine and
fails on any accept/reject divergence at the eight envelope-list positions.

Both authorities here state the WRITE contract -- `validate_record`'s default.
The READ path is deliberately more permissive (es#217): applying a newly-added
declaration rule to an already-persisted record makes the Stage-C gate skip an
armed mission and answer `allow`.  That asymmetry is pinned in
`test_custody_gate.py`, not here, and is documented in SECURITY.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # fail closed: missing oracle is not a clean result
    raise SystemExit(
        "ERROR: jsonschema is required for the Draft 2020-12 parity oracle"
    ) from exc

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verify_mission_custody import (  # noqa: E402
    DECLARATION_CONTENT_PATTERN,
    validate_record,
)


FIELDS = (
    ("authority", "permissions"),
    ("authority", "protected_state"),
    ("authority", "acceptable_costs"),
    ("scope", "in"),
    ("scope", "out"),
    ("stop_rules", "hold_if"),
    ("stop_rules", "stop_if"),
    ("stop_rules", "escalate_if"),
)


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def manifest() -> dict:
    return json.loads(
        (ROOT / "examples" / "valid-manifest-minimal.json").read_text(
            encoding="utf-8"))


def schema_pattern(schema: dict, section: str, field: str) -> str:
    return schema["properties"][section]["properties"][field]["items"]["pattern"]


def accepted_by_stdlib(record: dict) -> bool:
    return validate_record(record) == []


def main() -> int:
    schema = load("mission-manifest.schema.json")
    Draft202012Validator.check_schema(schema)
    draft202012 = Draft202012Validator(schema)

    for section, field in FIELDS:
        actual = schema_pattern(schema, section, field)
        if actual != DECLARATION_CONTENT_PATTERN:
            raise AssertionError(
                f"{section}.{field}: schema pattern drifted from stdlib")

    # Enumerate the complete Python whitespace set rather than a hand-picked
    # sample.  The explicit shared pattern makes the result independent of the
    # host regex engine's meaning of `\s`/`\S`.
    whitespace = [chr(cp) for cp in range(sys.maxunicode + 1)
                  if chr(cp).isspace()]
    cases: list[tuple[str, list[str], bool]] = [
        ("empty-list", [], True),
        ("substantive-edge-whitespace", ["  declared boundary  "], True),
        ("mixed-substantive-and-blank", ["declared", " \t\u00a0 "], False),
        ("all-whitespace-codepoints", ["".join(whitespace)], False),
    ]
    cases.extend(
        (f"blank-u+{ord(char):04x}", [char], False)
        for char in whitespace
    )

    for section, field in FIELDS:
        for label, value, expected in cases:
            record = manifest()
            record[section][field] = value
            stdlib = accepted_by_stdlib(record)
            schema_ok = not list(draft202012.iter_errors(record))
            if stdlib != schema_ok:
                raise AssertionError(
                    f"{section}.{field}/{label}: stdlib={stdlib} "
                    f"draft202012={schema_ok}")
            if stdlib != expected:
                raise AssertionError(
                    f"{section}.{field}/{label}: expected {expected}, "
                    f"both validators returned {stdlib}")

    compound = manifest()
    for section, field in FIELDS:
        compound[section][field] = [" \t\u00a0 "]
    if accepted_by_stdlib(compound) or not list(
            draft202012.iter_errors(compound)):
        raise AssertionError("compound blank envelope was accepted")

    print(
        f"all green: {len(FIELDS)} fields x {len(cases)} parity cases "
        "+ compound control")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
