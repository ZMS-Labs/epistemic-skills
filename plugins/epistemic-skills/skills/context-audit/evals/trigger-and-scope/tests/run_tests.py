#!/usr/bin/env python3
"""Polarity tests for context-audit trigger discipline and audit scope."""

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
    require(score_path.is_file(), f"missing context-audit trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("context_audit_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-claudemd-audit", "explicit-prune-instructions", "midtask-layer-conflict",
        "model-upgrade-stale-guardrails", "single-doc-prose", "new-agent-interface",
        "task-brief-recon", "single-task-prompt-tuning", "hard-neg-intradoc-contradictions",
        "hard-neg-system-prompt-tuning", "keep-gotcha-with-origin",
        "duplicate-most-local-survives", "no-version-control-report-only",
        "governance-projection-conflict",
    ], "context-audit fixture inventory drifted")

    balanced = scorer.score(fixtures, json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8")))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"full-audit": 7, "no-fire": 6, "report-only-audit": 1}, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 6, over["failures"])
    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(any("without reading its origin" in failure for failure in under["failures"]), under["failures"])
    require(any("most local" in failure for failure in under["failures"]), under["failures"])
    require(any("expected report-only-audit" in failure for failure in under["failures"]), under["failures"])

    print("context-audit trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
