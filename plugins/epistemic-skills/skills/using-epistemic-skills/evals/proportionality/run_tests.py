#!/usr/bin/env python3
"""Self-test the proportionality scorer against one good and two parody arms."""

from __future__ import annotations

from pathlib import Path

from score import DEFAULT_FIXTURES, load_json, score_run

HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def failure_codes(path: Path) -> set[str]:
    score = score_run(load_json(path), load_json(DEFAULT_FIXTURES))
    return {failure.split(":", 1)[0] for failure in score.failures}


def main() -> int:
    balanced = score_run(
        load_json(HERE / "examples" / "balanced.json"), load_json(DEFAULT_FIXTURES)
    )
    require(balanced.passed, "balanced example must pass:\n" + "\n".join(balanced.failures))

    ceremony_codes = failure_codes(HERE / "examples" / "full-ceremony.json")
    require("ROUTINE_ARTIFACT" in ceremony_codes, "full-ceremony must fail on routine artifacts")
    require("ROUTINE_ROLES" in ceremony_codes, "full-ceremony must fail on routine role calls")
    require("SKIP_INVENTORY" in ceremony_codes, "full-ceremony must fail on skip inventory")
    require(
        "VISIBLE_PROCESS_BUDGET" in ceremony_codes,
        "full-ceremony must fail the visible-process budget",
    )

    routine_codes = failure_codes(HERE / "examples" / "always-routine.json")
    require("MISSING_SKILL" in routine_codes, "always-routine must miss required skills")
    require("UNDER_ESCALATION" in routine_codes, "always-routine must fail high-risk escalation")
    require("MATERIAL_GATE" in routine_codes, "always-routine must fail material gate")
    require("HIGH_RISK_GATE" in routine_codes, "always-routine must fail high-risk gate")

    print("proportionality scorer self-test: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
