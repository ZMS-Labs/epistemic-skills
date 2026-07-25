#!/usr/bin/env python3
"""Deterministic tests for blinded packet construction and scoring."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
BLINDED = HERE.parent
PARENT = BLINDED.parent
sys.path.insert(0, str(BLINDED))

from runner import (  # noqa: E402
    REPO_ROOT,
    RESPONSE_SCHEMA,
    SKILL_PATHS,
    codex_live_command,
    codex_live_prompt,
    load,
    prepare,
    score_packets,
    skill_catalog,
    source_skill_hashes,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def response_from_result(result: dict[str, object]) -> dict[str, object]:
    return {
        "schema": "proportionality-fixture-response@1",
        **result,
    }


def main() -> int:
    arms = load(BLINDED / "arms.json")
    arm_ids = [arm["id"] for arm in arms["arms"]]
    require(
        arm_ids
        == [
            "main-80eb0827",
            "pr46-candidate-a4f2210f",
            "candidate-final-b73b04a",
            "full-ceremony",
            "always-routine",
        ],
        "the five required arms must remain pinned",
    )
    require(arms["invocation"]["settings"]["fresh_context_per_fixture"] is True, "isolation lost")

    router = (REPO_ROOT / "plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md").read_text(
        encoding="utf-8"
    )
    require(
        "proposed design needs correctness confirmation or reversal" in router,
        "router must preserve the member-owned single-design formal-rigor trigger",
    )
    require(
        "historical convention" in router,
        "router must identify unresolved repository conventions as blindspot evidence",
    )
    require(
        "Micro-recon is not a third path for non-routine work" in router,
        "router must not use routine micro-recon to close a precedential fork",
    )

    scenarios = load(BLINDED / "scenarios.json")["scenarios"]
    fixtures = load(PARENT / "fixtures.json")["fixtures"]
    require(len(scenarios) == 18, "expected 18 self-contained scenarios")
    require({x["id"] for x in scenarios} == {x["id"] for x in fixtures}, "inventory drift")

    with tempfile.TemporaryDirectory() as historical_raw:
        historical = Path(historical_raw)
        present = historical / SKILL_PATHS[0]
        present.parent.mkdir(parents=True, exist_ok=True)
        present.write_text("historical skill\n", encoding="utf-8")
        hashes = source_skill_hashes(historical)
        require(isinstance(hashes[SKILL_PATHS[0]], str), "present historical skill must be hashed")
        require(
            hashes["plugins/epistemic-skills/skills/using-epistemic-skills/reference/routine-fast-path.md"]
            is None,
            "a file absent at a pinned historical commit must be recorded as absent",
        )

    balanced = load(PARENT / "examples" / "balanced.json")
    with tempfile.TemporaryDirectory() as first_raw, tempfile.TemporaryDirectory() as second_raw:
        first = Path(first_raw)
        second = Path(second_raw)
        # Unit-test the pure packet projection after the source-verification
        # boundary. The CLI never exposes this bypass and always verifies the
        # checkout against the arm commit.
        prepare("candidate-final-b73b04a", 1, first, REPO_ROOT, _source_already_verified=True)
        prepare("candidate-final-b73b04a", 1, second, REPO_ROOT, _source_already_verified=True)
        require(load(first / "manifest.json") == load(second / "manifest.json"), "manifest not deterministic")

        for packet in (first / "packets").glob("*/input.json"):
            data = load(packet)
            serialized = json.dumps(data)
            for hidden in ("expected_paths", "required_skills", "require_escalation", "category"):
                require(hidden not in serialized, f"packet leaks scorer-only field {hidden}")
        sample_packet = first / "packets" / "m-01-data-structure-choice" / "input.json"
        catalog = skill_catalog(REPO_ROOT)
        require("name: applying-formal-rigor" in catalog, "member trigger catalog missing")
        require(
            "when a proposed design needs correctness confirmation or reversal" in catalog,
            "member-owned formal-rigor trigger missing from catalog",
        )
        require("# Applying Formal Rigor" not in catalog, "catalog must not preload skill bodies")
        live_prompt = codex_live_prompt(sample_packet, REPO_ROOT)
        require(
            "plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md" in live_prompt,
            "live adapter must activate the pinned repository router",
        )
        require("name: blindspot-pass" in live_prompt, "live adapter must expose member triggers")
        require("Choose between a list" in live_prompt, "live adapter must embed the packet")
        require("required_skills" not in live_prompt, "live adapter leaked scorer ground truth")
        command = codex_live_command(
            Path("codex.cmd"), REPO_ROOT, Path("response.json"), "gpt-5.6-sol"
        )
        require(command[-1] == "-", "sealed live prompt must travel on stdin")
        require(str(REPO_ROOT) in command, "live adapter must expose the pinned source checkout")
        require(str(RESPONSE_SCHEMA) in command, "live adapter must enforce the response schema")
        for result in balanced["results"]:
            out = first / "responses" / f"{result['fixture_id']}.json"
            out.write_text(json.dumps(response_from_result(result)), encoding="utf-8")
        require(score_packets(first) == 0, "balanced raw responses must score PASS")
        evidence = load(first / "evidence.json")
        require(evidence["status"] == "PASS", "evidence status mismatch")
        require(len(evidence["response_hashes"]) == 18, "all raw responses must be hashed")

    blocked = (BLINDED / "results" / "BLOCKED.md").read_text(encoding="utf-8")
    require(blocked.count("`NOT_RUN`") == 5, "all live arms must be explicitly NOT_RUN")
    require("No live result is claimed" in blocked, "block record must reject fabricated evidence")

    print("blinded proportionality packets: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
