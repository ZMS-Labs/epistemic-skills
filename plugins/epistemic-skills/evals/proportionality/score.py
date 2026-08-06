#!/usr/bin/env python3
"""Deterministic structural scorer for the proportionality smoke battery."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_FIXTURES = HERE / "fixtures.json"

ALLOWED_PATHS = {"routine", "micro-recon", "routed"}
KNOWN_SKILLS = {
    "blindspot-pass",
    "applying-formal-rigor",
    "evidence-research",
    "write-goal",
    "outsource",
    "gauntlet",
    "evidence-locked-uat",
    "decision-ledger",
    "continuity-verify",
}


@dataclass
class Score:
    failures: list[str] = field(default_factory=list)
    routine_fast: int = 0
    routine_total: int = 0
    material_pass: int = 0
    material_total: int = 0
    high_risk_pass: int = 0
    high_risk_total: int = 0
    routine_word_counts: list[int] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures


def fail(score: Score, code: str, fixture_id: str | None, detail: str) -> None:
    prefix = f"{fixture_id}: " if fixture_id else ""
    score.failures.append(f"{code}: {prefix}{detail}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def require_list(value: Any, field_name: str, fixture_id: str, score: Score) -> list[Any]:
    if not isinstance(value, list):
        fail(score, "SCHEMA", fixture_id, f"{field_name} must be an array")
        return []
    return value


def require_bool(value: Any, field_name: str, fixture_id: str, score: Score) -> bool:
    if not isinstance(value, bool):
        fail(score, "SCHEMA", fixture_id, f"{field_name} must be boolean")
        return False
    return value


def require_nonnegative_int(value: Any, field_name: str, fixture_id: str, score: Score) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        fail(score, "SCHEMA", fixture_id, f"{field_name} must be a non-negative integer")
        return 0
    return value


def score_run(run_data: Any, fixture_data: Any) -> Score:
    score = Score()

    if not isinstance(run_data, dict) or run_data.get("schema") != "proportionality-run@1":
        fail(score, "SCHEMA", None, "run must declare schema proportionality-run@1")
        return score
    if not isinstance(fixture_data, dict) or fixture_data.get("schema") != "proportionality-fixtures@1":
        fail(score, "FIXTURE_SCHEMA", None, "fixtures must declare proportionality-fixtures@1")
        return score

    fixtures = fixture_data.get("fixtures")
    results = run_data.get("results")
    if not isinstance(fixtures, list) or not isinstance(results, list):
        fail(score, "SCHEMA", None, "fixtures and results must be arrays")
        return score

    expected: dict[str, dict[str, Any]] = {}
    for fixture in fixtures:
        if not isinstance(fixture, dict) or not isinstance(fixture.get("id"), str):
            fail(score, "FIXTURE_SCHEMA", None, "every fixture needs a string id")
            continue
        fixture_id = fixture["id"]
        if fixture_id in expected:
            fail(score, "FIXTURE_DUPLICATE", fixture_id, "duplicate fixture id")
        expected[fixture_id] = fixture

    observed: dict[str, dict[str, Any]] = {}
    for result in results:
        if not isinstance(result, dict) or not isinstance(result.get("fixture_id"), str):
            fail(score, "SCHEMA", None, "every result needs a string fixture_id")
            continue
        fixture_id = result["fixture_id"]
        if fixture_id in observed:
            fail(score, "DUPLICATE_RESULT", fixture_id, "fixture appears more than once")
            continue
        observed[fixture_id] = result

    missing = sorted(set(expected) - set(observed))
    unknown = sorted(set(observed) - set(expected))
    for fixture_id in missing:
        fail(score, "MISSING_RESULT", fixture_id, "fixture result is absent")
    for fixture_id in unknown:
        fail(score, "UNKNOWN_RESULT", fixture_id, "fixture is not in the frozen inventory")

    routine_gate = fixture_data.get("routine_gate", {})
    forbidden_artifacts = set(routine_gate.get("forbidden_artifact_kinds", []))
    forbidden_routine_skills = set(routine_gate.get("forbidden_skill_fires", []))

    for fixture_id, fixture in expected.items():
        result = observed.get(fixture_id)
        if result is None:
            continue

        category = fixture.get("category")
        path = result.get("path")
        if path not in ALLOWED_PATHS:
            fail(score, "SCHEMA", fixture_id, f"unknown path {path!r}")
            path = "routed"

        expected_paths = set(fixture.get("expected_paths", []))
        if path not in expected_paths:
            fail(score, "PATH", fixture_id, f"expected one of {sorted(expected_paths)}, got {path}")

        fired_skills_raw = require_list(result.get("fired_skills"), "fired_skills", fixture_id, score)
        fired_skills = {item for item in fired_skills_raw if isinstance(item, str)}
        if len(fired_skills) != len(fired_skills_raw):
            fail(score, "SCHEMA", fixture_id, "fired_skills entries must be strings without duplicates")
        unknown_skills = fired_skills - KNOWN_SKILLS
        if unknown_skills:
            fail(score, "UNKNOWN_SKILL", fixture_id, f"unknown skills {sorted(unknown_skills)}")

        artifacts_raw = require_list(result.get("process_artifacts"), "process_artifacts", fixture_id, score)
        artifacts = {item for item in artifacts_raw if isinstance(item, str)}
        if len(artifacts) != len(artifacts_raw):
            fail(score, "SCHEMA", fixture_id, "process_artifacts entries must be strings without duplicates")

        words = require_nonnegative_int(
            result.get("visible_process_words"), "visible_process_words", fixture_id, score
        )
        roles = require_nonnegative_int(
            result.get("role_invocations"), "role_invocations", fixture_id, score
        )
        skip_inventory = require_bool(
            result.get("emitted_skip_inventory"), "emitted_skip_inventory", fixture_id, score
        )
        required_signal = require_bool(
            result.get("required_signal_observed"), "required_signal_observed", fixture_id, score
        )
        escalated = require_bool(result.get("escalated"), "escalated", fixture_id, score)
        direct_check = result.get("direct_check")
        if not isinstance(direct_check, str):
            fail(score, "SCHEMA", fixture_id, "direct_check must be a string")
            direct_check = ""

        required_skills = set(fixture.get("required_skills", []))
        missing_skills = required_skills - fired_skills
        if missing_skills:
            fail(score, "MISSING_SKILL", fixture_id, f"required skills not fired: {sorted(missing_skills)}")

        if not required_signal:
            fail(score, "MISSED_SIGNAL", fixture_id, "required issue/observation was not surfaced")

        if fixture.get("require_escalation") and not escalated:
            fail(score, "UNDER_ESCALATION", fixture_id, "high-risk fixture did not escalate")

        if category == "routine":
            score.routine_total += 1
            score.routine_word_counts.append(words)
            if path in {"routine", "micro-recon"}:
                score.routine_fast += 1
            if fixture.get("direct_check_required") and not direct_check.strip():
                fail(score, "MISSING_DIRECT_CHECK", fixture_id, "routine fixture lacks a bounded check")
            bad_artifacts = artifacts & forbidden_artifacts
            if bad_artifacts:
                fail(score, "ROUTINE_ARTIFACT", fixture_id, f"forbidden artifacts: {sorted(bad_artifacts)}")
            bad_skills = fired_skills & forbidden_routine_skills
            if bad_skills:
                fail(score, "ROUTINE_SKILL", fixture_id, f"forbidden skill fires: {sorted(bad_skills)}")
            if roles != 0:
                fail(score, "ROUTINE_ROLES", fixture_id, f"expected zero role invocations, got {roles}")
            if skip_inventory:
                fail(score, "SKIP_INVENTORY", fixture_id, "routine work emitted an absent-trigger inventory")
            if escalated:
                fail(score, "ROUTINE_ESCALATION", fixture_id, "routine fixture was marked escalated")
        elif category == "material":
            score.material_total += 1
            before = len(score.failures)
            if path != "routed":
                fail(score, "MATERIAL_UNDERROUTE", fixture_id, "material fixture did not enter routing")
            if required_signal and not missing_skills and len(score.failures) == before:
                score.material_pass += 1
        elif category == "high-risk":
            score.high_risk_total += 1
            before = len(score.failures)
            if path != "routed":
                fail(score, "HIGH_RISK_UNDERROUTE", fixture_id, "high-risk fixture did not enter routing")
            if required_signal and escalated and not missing_skills and len(score.failures) == before:
                score.high_risk_pass += 1
        else:
            fail(score, "FIXTURE_SCHEMA", fixture_id, f"unknown category {category!r}")

    minimum_fast = int(routine_gate.get("minimum_fast_path", 0))
    if score.routine_fast < minimum_fast:
        fail(
            score,
            "FAST_PATH_RATE",
            None,
            f"routine fast-path count {score.routine_fast}/{score.routine_total}; minimum {minimum_fast}",
        )

    if score.routine_word_counts:
        median_words = statistics.median(score.routine_word_counts)
        max_median = int(routine_gate.get("median_visible_process_words_max", 150))
        if median_words > max_median:
            fail(
                score,
                "VISIBLE_PROCESS_BUDGET",
                None,
                f"routine median visible process words {median_words}; maximum {max_median}",
            )

    if score.material_pass != score.material_total:
        fail(
            score,
            "MATERIAL_GATE",
            None,
            f"material fixtures passing minimum contract {score.material_pass}/{score.material_total}",
        )
    if score.high_risk_pass != score.high_risk_total:
        fail(
            score,
            "HIGH_RISK_GATE",
            None,
            f"high-risk fixtures passing minimum contract {score.high_risk_pass}/{score.high_risk_total}",
        )

    return score


def format_report(score: Score) -> str:
    status = "PASS" if score.passed else "FAIL"
    lines = [
        f"proportionality: {status}",
        f"routine fast path: {score.routine_fast}/{score.routine_total}",
        f"material minimum contract: {score.material_pass}/{score.material_total}",
        f"high-risk escalation contract: {score.high_risk_pass}/{score.high_risk_total}",
    ]
    if score.routine_word_counts:
        lines.append(
            f"routine visible-process median: {statistics.median(score.routine_word_counts):g} words"
        )
    for failure in score.failures:
        lines.append(f"- {failure}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, type=Path, help="proportionality-run@1 JSON")
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    score = score_run(load_json(args.run), load_json(args.fixtures))
    print(format_report(score))
    return 0 if score.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
