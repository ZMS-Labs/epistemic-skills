#!/usr/bin/env python3
"""Deterministic structural scorer for verification proportionality."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_FIXTURES = HERE / "fixtures.json"

ACTION_FIELDS = {
    "claim",
    "oracle",
    "subject_revision",
    "independence",
    "reuses_existing_evidence",
    "rerun",
    "discriminating_purpose",
}
RESULT_FIELDS = {
    "fixture_id",
    "mode",
    "claim_status",
    "verification_actions",
    "duplicate_equivalent_checks",
    "unmapped_verification_actions",
    "subagent_invocations",
    "evidence_postdates_last_material_change",
    "independence_trigger_observed",
    "escalated",
}


@dataclass
class Score:
    failures: list[str] = field(default_factory=list)
    fixture_total: int = 0
    fixture_pass: int = 0

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


def index_by_id(items: Any, label: str, score: Score) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        fail(score, "SCHEMA", None, f"{label} must be an array")
        return {}
    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            fail(score, "SCHEMA", None, f"every {label} entry needs a string id")
            continue
        item_id = item["id"]
        if item_id in indexed:
            fail(score, "DUPLICATE", item_id, f"duplicate {label} id")
            continue
        indexed[item_id] = item
    return indexed


def validate_action(
    action: Any,
    fixture_id: str,
    index: int,
    score: Score,
    allowed_oracles: set[str],
    allowed_independence: set[str],
) -> dict[str, Any]:
    if not isinstance(action, dict):
        fail(score, "SCHEMA", fixture_id, f"verification_actions[{index}] must be an object")
        return {}
    missing = sorted(ACTION_FIELDS - set(action))
    unknown = sorted(set(action) - ACTION_FIELDS)
    if missing or unknown:
        fail(
            score,
            "SCHEMA",
            fixture_id,
            f"verification_actions[{index}] fields missing={missing}, unknown={unknown}",
        )

    for field_name in ("claim", "subject_revision", "discriminating_purpose"):
        if not isinstance(action.get(field_name), str):
            fail(
                score,
                "SCHEMA",
                fixture_id,
                f"verification_actions[{index}].{field_name} must be a string",
            )

    oracle = action.get("oracle")
    if oracle not in allowed_oracles:
        fail(
            score,
            "SCHEMA",
            fixture_id,
            f"verification_actions[{index}].oracle must be one of {sorted(allowed_oracles)}",
        )

    independence = action.get("independence")
    if independence not in allowed_independence:
        fail(
            score,
            "SCHEMA",
            fixture_id,
            "verification_actions"
            f"[{index}].independence must be one of {sorted(allowed_independence)}",
        )

    reuse = require_bool(
        action.get("reuses_existing_evidence"),
        f"verification_actions[{index}].reuses_existing_evidence",
        fixture_id,
        score,
    )
    rerun = require_bool(
        action.get("rerun"),
        f"verification_actions[{index}].rerun",
        fixture_id,
        score,
    )
    if reuse and rerun:
        fail(
            score,
            "CONTRADICTORY_ACTION",
            fixture_id,
            f"verification_actions[{index}] cannot both reuse and rerun",
        )
    if rerun and not str(action.get("discriminating_purpose", "")).strip():
        fail(
            score,
            "RERUN_WITHOUT_PURPOSE",
            fixture_id,
            f"verification_actions[{index}] reruns without a stated discriminating purpose",
        )
    if not str(action.get("claim", "")).strip():
        fail(
            score,
            "UNMAPPED_ACTION",
            fixture_id,
            f"verification_actions[{index}] lacks a mapped claim",
        )
    if not str(action.get("subject_revision", "")).strip():
        fail(
            score,
            "UNBOUND_EVIDENCE",
            fixture_id,
            f"verification_actions[{index}] lacks a subject revision",
        )
    return action


def score_run(run_data: Any, fixture_data: Any) -> Score:
    score = Score()

    if not isinstance(run_data, dict) or run_data.get("schema") != "verification-proportionality-run@1":
        fail(score, "SCHEMA", None, "run must declare verification-proportionality-run@1")
        return score
    if (
        not isinstance(fixture_data, dict)
        or fixture_data.get("schema") != "verification-proportionality-fixtures@1"
    ):
        fail(
            score,
            "FIXTURE_SCHEMA",
            None,
            "fixtures must declare verification-proportionality-fixtures@1",
        )
        return score

    allowed_modes = set(fixture_data.get("allowed_modes", []))
    allowed_claim_statuses = set(fixture_data.get("allowed_claim_statuses", []))
    allowed_oracles = set(fixture_data.get("allowed_oracles", []))
    allowed_independence = set(fixture_data.get("allowed_independence", []))

    fixtures = index_by_id(fixture_data.get("fixtures"), "fixture", score)

    raw_results = run_data.get("results")
    if not isinstance(raw_results, list):
        fail(score, "SCHEMA", None, "results must be an array")
        return score

    results: dict[str, dict[str, Any]] = {}
    for result in raw_results:
        if not isinstance(result, dict) or not isinstance(result.get("fixture_id"), str):
            fail(score, "SCHEMA", None, "every result needs a string fixture_id")
            continue
        fixture_id = result["fixture_id"]
        if fixture_id in results:
            fail(score, "DUPLICATE_RESULT", fixture_id, "fixture appears more than once")
            continue
        missing = sorted(RESULT_FIELDS - set(result))
        unknown = sorted(set(result) - RESULT_FIELDS)
        if missing or unknown:
            fail(
                score,
                "SCHEMA",
                fixture_id,
                f"result fields missing={missing}, unknown={unknown}",
            )
        results[fixture_id] = result

    for fixture_id in sorted(set(fixtures) - set(results)):
        fail(score, "MISSING_RESULT", fixture_id, "fixture result is absent")
    for fixture_id in sorted(set(results) - set(fixtures)):
        fail(score, "UNKNOWN_RESULT", fixture_id, "fixture is not in the frozen inventory")

    for fixture_id, fixture in fixtures.items():
        result = results.get(fixture_id)
        if result is None:
            continue
        score.fixture_total += 1
        before = len(score.failures)

        mode = result.get("mode")
        if mode not in allowed_modes:
            fail(score, "SCHEMA", fixture_id, f"unknown mode {mode!r}")
        if mode not in set(fixture.get("expected_modes", [])):
            fail(
                score,
                "MODE",
                fixture_id,
                f"expected one of {fixture.get('expected_modes', [])}, got {mode!r}",
            )

        claim_status = result.get("claim_status")
        if claim_status not in allowed_claim_statuses:
            fail(score, "SCHEMA", fixture_id, f"unknown claim_status {claim_status!r}")
        expected_status = fixture.get("expected_claim_status")
        if claim_status != expected_status:
            fail(
                score,
                "CLAIM_STATUS",
                fixture_id,
                f"expected {expected_status!r}, got {claim_status!r}",
            )

        actions_raw = result.get("verification_actions")
        if not isinstance(actions_raw, list):
            fail(score, "SCHEMA", fixture_id, "verification_actions must be an array")
            actions_raw = []
        actions = [
            validate_action(
                action,
                fixture_id,
                index,
                score,
                allowed_oracles,
                allowed_independence,
            )
            for index, action in enumerate(actions_raw)
        ]

        minimum = int(fixture.get("min_actions", 0))
        maximum = int(fixture.get("max_actions", minimum))
        if len(actions) < minimum:
            fail(
                score,
                "MISSING_EVIDENCE",
                fixture_id,
                f"expected at least {minimum} verification action(s), got {len(actions)}",
            )
        if len(actions) > maximum:
            fail(
                score,
                "ACTION_BUDGET",
                fixture_id,
                f"expected at most {maximum} verification action(s), got {len(actions)}",
            )

        observed_oracles = {
            str(action.get("oracle"))
            for action in actions
            if action.get("oracle") is not None
        }
        required_oracles = set(fixture.get("required_oracles", []))
        if required_oracles and not (required_oracles & observed_oracles):
            fail(
                score,
                "WRONG_ORACLE",
                fixture_id,
                f"expected one of {sorted(required_oracles)}, got {sorted(observed_oracles)}",
            )

        duplicates = require_nonnegative_int(
            result.get("duplicate_equivalent_checks"),
            "duplicate_equivalent_checks",
            fixture_id,
            score,
        )
        if duplicates:
            fail(
                score,
                "DUPLICATE_CHECK",
                fixture_id,
                f"{duplicates} equivalent check(s) repeated over unchanged state",
            )

        unmapped = require_nonnegative_int(
            result.get("unmapped_verification_actions"),
            "unmapped_verification_actions",
            fixture_id,
            score,
        )
        if unmapped:
            fail(
                score,
                "UNMAPPED_ACTION",
                fixture_id,
                f"{unmapped} verification action(s) have no material claim",
            )

        subagents = require_nonnegative_int(
            result.get("subagent_invocations"),
            "subagent_invocations",
            fixture_id,
            score,
        )
        current = require_bool(
            result.get("evidence_postdates_last_material_change"),
            "evidence_postdates_last_material_change",
            fixture_id,
            score,
        )
        trigger = require_bool(
            result.get("independence_trigger_observed"),
            "independence_trigger_observed",
            fixture_id,
            score,
        )
        escalated = require_bool(result.get("escalated"), "escalated", fixture_id, score)

        if fixture.get("require_current_evidence") and not current:
            fail(
                score,
                "STALE_OR_MISSING_EVIDENCE",
                fixture_id,
                "completion claim lacks evidence after the last relevant material change",
            )

        if fixture.get("require_reuse") and not any(
            action.get("reuses_existing_evidence") is True for action in actions
        ):
            fail(score, "MISSED_REUSE", fixture_id, "current reusable evidence was not reused")

        if fixture.get("require_rerun") and not any(
            action.get("rerun") is True for action in actions
        ):
            fail(score, "MISSING_REFRESH", fixture_id, "stale or prose-only evidence was not refreshed")

        if fixture.get("forbid_rerun") and any(action.get("rerun") is True for action in actions):
            fail(
                score,
                "UNNECESSARY_RERUN",
                fixture_id,
                "an equivalent current check was rerun without a freshness need",
            )

        independent_actions = [
            action
            for action in actions
            if action.get("independence") in {"distinct-context", "deterministic"}
            or action.get("oracle") in {"verifier", "gate"}
        ]

        if fixture.get("require_independence"):
            if not trigger:
                fail(
                    score,
                    "MISSED_INDEPENDENCE_TRIGGER",
                    fixture_id,
                    "required independence trigger was not observed",
                )
            if not independent_actions:
                fail(
                    score,
                    "MISSING_INDEPENDENCE",
                    fixture_id,
                    "required distinct-context or deterministic judgment is absent",
                )
        if fixture.get("forbid_independence"):
            if trigger:
                fail(
                    score,
                    "FALSE_INDEPENDENCE_TRIGGER",
                    fixture_id,
                    "routine/deterministic work was treated as needing independence",
                )
            if independent_actions or subagents:
                fail(
                    score,
                    "UNNECESSARY_INDEPENDENCE",
                    fixture_id,
                    "independent verifier or subagent was added without a positive trigger",
                )

        if fixture.get("require_escalation") and not escalated:
            fail(score, "UNDER_ESCALATION", fixture_id, "required escalation did not occur")
        if not fixture.get("require_escalation") and escalated:
            fail(score, "OVER_ESCALATION", fixture_id, "fixture escalated without a trigger")

        if len(score.failures) == before:
            score.fixture_pass += 1

    return score


def format_report(score: Score) -> str:
    lines = [
        f"verification proportionality: {'PASS' if score.passed else 'FAIL'}",
        f"fixtures passing: {score.fixture_pass}/{score.fixture_total}",
    ]
    if score.failures:
        lines.append("failures:")
        lines.extend(f"- {failure}" for failure in score.failures)
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", required=True, type=Path)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    score = score_run(load_json(args.run), load_json(args.fixtures))
    print(format_report(score))
    return 0 if score.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
