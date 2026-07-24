#!/usr/bin/env python3
"""Regression test: focused formal rigor is smaller in kind, not degree."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("score", ROOT / "score.py")
assert spec and spec.loader
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

truth = {
    "fixture_id": "ot-02-focused-not-ceremony",
    "expected_invocation": ["focused"],
    "claims": [{"id": "c1", "allowed_states": ["established"]}],
    "coverage": {}, "decision_frame": {}, "synthesis": {}, "freshness": {},
}

compact = {
    "response": "formal-rigor-fixture-response@1",
    "fixture": "ot-02-focused-not-ceremony",
    "invocation": "focused",
    "skip_reason": None,
    "claim_assessments": [{"id": "c1", "state": "established", "derivation_ids": ["inline-1"]}],
    "focused_output": [
        "Subject/model: membership lookup under n-element in-memory collection.",
        "Construct: list scan versus hash-set lookup.",
        "Preconditions: hash quality and build cost are explicit.",
        "Derivation: list membership is theta(n); set build theta(n), expected lookup theta(1).",
        "Result: established for repeated lookups after construction.",
        "Residual: constants and worst-case hashing remain empirical.",
    ],
    "record": None,
}

result = score.score_fixture(truth, compact)
assert result["structural_pass"], result

container_tax = dict(compact, focused_output=None, record={"record": "formal-rigor-record@2"})
result = score.score_fixture(truth, container_tax)
assert not result["structural_pass"] and "S1" in result["dimensions_failed"], result

print("formal-rigor focused proportionality: PASS")
