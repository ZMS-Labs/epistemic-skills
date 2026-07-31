#!/usr/bin/env python3
"""Polarity tests for agent-interface-design trigger discipline and scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing agent-interface-design trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("agent_interface_design_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "tool-schema-new-engage", "mcp-surface-new-engage", "structured-output-contract-engage",
        "subagent-dispatch-contract-engage", "agent-caller-cli-engage", "review-adds-tool-engage",
        "human-ui-no-fire", "human-docs-no-fire", "throwaway-script-no-fire",
        "prose-dispatch-brief-no-fire", "inbound-context-audit-no-fire", "human-caller-cli-no-fire",
        "cold-consumer-gate-fail", "example-lint-three-examples",
    ], "agent-interface-design fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"engage": 6, "no-fire": 6, "consumer-gate": 1, "example-lint": 1}, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")

    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire, got engage" in failure for failure in over["failures"]) == 6, over["failures"])

    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(sum("expected engage, got no-fire" in failure for failure in under["failures"]) == 6, under["failures"])
    require(any("recorded as a compatibility concession" in failure for failure in under["failures"]), under["failures"])
    require(any("transcript" in failure for failure in under["failures"]), under["failures"])
    require(any("no lint disposition" in failure for failure in under["failures"]), under["failures"])
    require(any("weaker-consumer audience" in failure for failure in under["failures"]), under["failures"])
    require(any("structural fix that replaces it" in failure for failure in under["failures"]), under["failures"])

    print("agent-interface-design trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
