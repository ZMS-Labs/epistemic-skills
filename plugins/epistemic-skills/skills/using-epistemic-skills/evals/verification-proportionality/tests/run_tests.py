#!/usr/bin/env python3
"""Self-test verification proportionality, packet integrity, and policy bindings."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUITE = HERE.parent
REPO_ROOT = HERE.parents[6]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def failure_codes(score) -> set[str]:
    return {failure.split(":", 1)[0] for failure in score.failures}


def main() -> int:
    scorer = load_module("verification_proportionality_score", SUITE / "score.py")
    fixtures = load(SUITE / "fixtures.json")

    balanced = scorer.score_run(load(SUITE / "examples" / "balanced.json"), fixtures)
    require(balanced.passed, "balanced example must pass:\n" + "\n".join(balanced.failures))

    legacy = scorer.score_run(load(SUITE / "examples" / "legacy-final-pass.json"), fixtures)
    legacy_codes = failure_codes(legacy)
    require("DUPLICATE_CHECK" in legacy_codes, "legacy final pass must fail duplicate checks")
    require("UNMAPPED_ACTION" in legacy_codes, "legacy final pass must fail unmapped ceremony")
    require("UNNECESSARY_RERUN" in legacy_codes, "legacy final pass must fail unnecessary reruns")
    require(
        "UNNECESSARY_INDEPENDENCE" in legacy_codes,
        "legacy final pass must fail unnecessary independence",
    )

    verifier = scorer.score_run(load(SUITE / "examples" / "verifier-subagent.json"), fixtures)
    verifier_codes = failure_codes(verifier)
    require(
        "UNNECESSARY_INDEPENDENCE" in verifier_codes,
        "always-verifier arm must fail routine independence",
    )
    require("DUPLICATE_CHECK" in verifier_codes, "always-verifier arm must fail duplicate work")

    absent = scorer.score_run(load(SUITE / "examples" / "never-verify.json"), fixtures)
    absent_codes = failure_codes(absent)
    require(
        "STALE_OR_MISSING_EVIDENCE" in absent_codes,
        "never-verify must fail current-evidence requirements",
    )
    require("MISSING_EVIDENCE" in absent_codes, "never-verify must fail evidence minimums")
    require("UNDER_ESCALATION" in absent_codes, "never-verify must fail required escalation")
    require(
        "MISSING_INDEPENDENCE" in absent_codes,
        "never-verify must fail independent acceptance/audit requirements",
    )

    arms = load(SUITE / "blinded" / "arms.json")
    scenarios = load(SUITE / "blinded" / "scenarios.json")
    require(arms.get("schema") == "verification-proportionality-arms@1", "invalid arms schema")
    require(
        scenarios.get("schema") == "verification-proportionality-scenarios@1",
        "invalid scenarios schema",
    )
    arm_ids = {arm["id"] for arm in arms["arms"]}
    require(
        arm_ids
        == {
            "neutral-opus5",
            "candidate-opus5",
            "legacy-final-pass",
            "verifier-subagent",
            "never-verify",
        },
        f"unexpected arm inventory: {sorted(arm_ids)}",
    )
    require(
        arms["invocation"]["model_id"] is None,
        "committed arms must require an exact model id at prepare time",
    )
    fixture_ids = {fixture["id"] for fixture in fixtures["fixtures"]}
    scenario_ids = {scenario["id"] for scenario in scenarios["scenarios"]}
    require(fixture_ids == scenario_ids, "fixture/scenario inventories must match")
    for arm in arms["arms"]:
        require((SUITE / "blinded" / arm["prompt"]).is_file(), f"missing prompt {arm['prompt']}")

    router = (
        REPO_ROOT
        / "plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md"
    ).read_text(encoding="utf-8")
    routine = (
        REPO_ROOT
        / "plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md"
    ).read_text(encoding="utf-8")
    policy = (
        REPO_ROOT
        / "plugins/epistemic-skills/skills/using-epistemic-skills/reference/verification-proportionality.md"
    ).read_text(encoding="utf-8")
    helix = (
        REPO_ROOT / "plugins/epistemic-skills/skills/helix/SKILL.md"
    ).read_text(encoding="utf-8")
    outsource = (
        REPO_ROOT / "plugins/epistemic-skills/skills/outsource/SKILL.md"
    ).read_text(encoding="utf-8")

    require(
        "reference/verification-proportionality.md" in router,
        "router must bind the verification policy reference",
    )
    require(
        "Verification is a claim-evidence boundary" in router,
        "router must state the claim-evidence boundary",
    )
    require(
        "The actor never judges its own work" not in router,
        "router must not prohibit actor-run bounded evidence",
    )
    require(
        "postdates the last material change" in routine,
        "routine path must bind freshness to the last material change",
    )
    require(
        "Do not rerun an equivalent bounded check solely" in routine,
        "routine path must reject turn-bound final reruns",
    )
    require(
        "Do not add a second verification pass" in helix,
        "helix must prevent duplicate workflow verification",
    )
    require(
        "load-bearing completion claim" in outsource
        and "independently inspectable" in outsource,
        "outsource must verify claims without automatically duplicating commands",
    )
    require(
        "prompting-claude-opus-5" in policy and "migration-guide" in policy,
        "policy must cite the official Opus 5 prompting sources",
    )
    require(
        "<opus5_scope_and_verification>" in policy,
        "policy must include the model-specific overlay",
    )

    runner = load_module(
        "verification_proportionality_runner",
        SUITE / "blinded" / "runner.py",
    )
    with tempfile.TemporaryDirectory() as tmp:
        packet_dir = Path(tmp) / "packet"
        result = runner.prepare(
            "candidate-opus5",
            1,
            "claude-opus-5-test-pin",
            packet_dir,
            REPO_ROOT,
        )
        require(result == 0, "packet preparation must succeed")
        balanced_data = load(SUITE / "examples" / "balanced.json")
        for fixture_result in balanced_data["results"]:
            fixture_id = fixture_result["fixture_id"]
            response = {
                "schema": "verification-proportionality-fixture-response@1",
                **fixture_result,
            }
            runner.write_json(packet_dir / "responses" / f"{fixture_id}.json", response)
        require(runner.score_packets(packet_dir) == 0, "prepared balanced packet must score")
        evidence = load(packet_dir / "evidence.json")
        require(evidence["status"] == "PASS", "packet evidence must record PASS")

    print("verification proportionality tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
