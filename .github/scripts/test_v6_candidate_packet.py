#!/usr/bin/env python3
"""Self-test for v6 candidate packet generator (no GitHub live calls)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / ".github/scripts"))

from v6_generate_candidate_packet import (  # noqa: E402
    blocking_from_matrix,
    build_promotion_packet,
    build_receipt,
    class_claims,
    tracker_claim,
)


def main() -> int:
    sha = "a" * 40
    claims = class_claims(sha)
    ids = [c["id"] for c in claims]
    if len(ids) != len(set(ids)):
        raise AssertionError("duplicate class claim ids")
    required = {
        "CLM-INDEPENDENT-GAUNTLET",
        "CLM-V5-DESIGN-COMMITMENTS",
        "CLM-TRACKER-RECONCILED",
        "CLM-MC-137",
        "CLM-PUBLIC-CONTENT",
    }
    missing = required - set(ids)
    if missing:
        raise AssertionError(f"missing class claims: {missing}")
    go = next(c for c in claims if c["id"] == "CLM-INDEPENDENT-GAUNTLET")
    if go["status"] != "UNPROVED":
        raise AssertionError("independent Gauntlet must start UNPROVED")
    if go["owner"] != "independent-panel":
        raise AssertionError("Gauntlet owner must not be the implementer")

    hold = tracker_claim(
        "issue",
        104,
        "Complete or retire v5 commitments",
        {
            "phase": "frontier-decision",
            "disposition": "hold-operator",
            "owner": "operator",
            "evidence_note": "hold",
        },
        ["gate:operator"],
    )
    if hold["status"] != "BLOCKED":
        raise AssertionError("operator hold must be BLOCKED")
    if hold["id"] != "CLM-ISSUE-104":
        raise AssertionError(hold["id"])

    matrix = {"claims": claims}
    packet = build_promotion_packet(sha, "2026-08-18T00:00:00Z", matrix)
    if packet["self_certification"] != "refused":
        raise AssertionError("must refuse self-certification")
    if packet["readiness"] != "NOT_READY":
        raise AssertionError("packet must not self-declare operator-ready")
    if packet["requested_irreversible_acts"]:
        raise AssertionError("BUILD packet must request no irreversible acts")
    if "CLM-INDEPENDENT-GAUNTLET" not in blocking_from_matrix(matrix):
        raise AssertionError("independent Gauntlet must block readiness")

    receipt = build_receipt(sha, "2026-08-18T00:00:00Z")
    blob = json.dumps(receipt)
    forbidden = "zms-" + "homelab"
    if forbidden in blob.lower():
        raise AssertionError("candidate receipt must not name the private fleet overlay")
    if receipt["parent_program"] != "ZMS-Labs/epistemic-skills#191":
        raise AssertionError(receipt["parent_program"])

    collector = REPO_ROOT / ".github/scripts/v6_collect_candidate_evidence.py"
    proc = subprocess.run(
        [sys.executable, str(collector), "--self-test"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise AssertionError("evidence collector self-test failed")
    print("v6 candidate packet self-test: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
