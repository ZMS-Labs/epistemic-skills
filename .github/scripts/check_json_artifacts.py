#!/usr/bin/env python3
"""Parse committed integration JSON, preserving declared malformed raw evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FORMAL_ROOT = REPO_ROOT / "plugins/epistemic-skills/skills/applying-formal-rigor"
RED_ROOT = FORMAL_ROOT / "evals/formal-rigor-v2-fixtures/results/2026-07-24-red-baseline"


def main() -> int:
    evidence = json.loads((RED_ROOT / "evidence.json").read_text(encoding="utf-8"))
    allowed_invalid = {
        RED_ROOT / row["path"]: row["sha256"]
        for row in evidence["responses"]
        if not row["json_parseable"]
    }
    roots = [
        REPO_ROOT / "plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility",
        REPO_ROOT / "plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality",
        FORMAL_ROOT,
        REPO_ROOT / "plugins/epistemic-skills/skills/evidence-locked-uat/evals/triage",
        REPO_ROOT / "plugins/epistemic-skills/skills/decision-ledger/evals/proportionality",
        REPO_ROOT / "plugins/epistemic-skills/skills/decision-ledger/reference",
    ]
    files = [path for root in roots for path in root.rglob("*.json")]
    observed_invalid: set[Path] = set()
    for path in files:
        raw = path.read_bytes()
        try:
            json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            if path not in allowed_invalid:
                raise
            actual = hashlib.sha256(raw).hexdigest()
            if actual != allowed_invalid[path]:
                raise AssertionError(f"declared invalid evidence hash mismatch: {path}")
            observed_invalid.add(path)
    if observed_invalid != set(allowed_invalid):
        raise AssertionError("declared invalid evidence set was not fully observed")
    print(
        f"checked {len(files)} JSON artifacts; "
        f"{len(observed_invalid)} hash-pinned malformed response preserved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
