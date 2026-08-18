#!/usr/bin/env python3
"""Validate v6 assurance JSON artifacts against committed schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRACT_ROOT = REPO_ROOT / "plugins/epistemic-skills/contracts/v6-assurance"
V6_DOCS = REPO_ROOT / "docs/v6/ES6-ZI-001"
CANDIDATE_DOCS = REPO_ROOT / "docs/v6/ES6-V6-CANDIDATE"


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_keys(obj: dict, keys: tuple[str, ...], label: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise AssertionError(f"{label} missing keys: {missing}")


def validate_matrix(doc: dict) -> None:
    _require_keys(
        doc,
        ("schema", "program", "exact_start_sha", "generated_at", "claims"),
        "claim-to-proof-matrix",
    )
    if doc["schema"] != "claim-to-proof-matrix@1":
        raise AssertionError("unexpected matrix schema")
    if not doc["claims"]:
        raise AssertionError("matrix must contain at least one claim")
    claim_ids: set[str] = set()
    for claim in doc["claims"]:
        _require_keys(
            claim,
            (
                "id",
                "statement",
                "authority",
                "subject",
                "oracle",
                "falsifier",
                "environment",
                "independence",
                "evidence_tier",
                "status",
                "release_consequence",
                "owner",
                "closure_path",
            ),
            f"claim {claim.get('id', '?')}",
        )
        if claim["id"] in claim_ids:
            raise AssertionError(f"duplicate claim id: {claim['id']}")
        claim_ids.add(claim["id"])


def validate_reconciliation(doc: dict) -> None:
    _require_keys(
        doc,
        ("schema", "program", "exact_start_sha", "generated_at", "items"),
        "issue-pr-reconciliation",
    )
    if doc["schema"] != "issue-pr-reconciliation@1":
        raise AssertionError("unexpected reconciliation schema")
    seen: set[tuple[str, int]] = set()
    for item in doc["items"]:
        _require_keys(
            item,
            ("kind", "number", "title", "phase", "disposition", "owner", "evidence_note"),
            f"item #{item.get('number', '?')}",
        )
        key = (item["kind"], item["number"])
        if key in seen:
            raise AssertionError(f"duplicate tracker item: {key}")
        seen.add(key)


def validate_source_inventory(doc: dict) -> None:
    _require_keys(
        doc,
        ("schema", "exact_start_sha", "generated_at", "workflows", "contracts", "ci_scripts"),
        "source-inventory",
    )
    if doc["schema"] != "v6-source-inventory@1":
        raise AssertionError("unexpected source inventory schema")


def validate_promotion_packet(doc: dict) -> None:
    _require_keys(
        doc,
        (
            "schema",
            "program",
            "issue",
            "candidate_sha",
            "generated_at",
            "readiness",
            "self_certification",
            "independent_gauntlet",
            "rollback",
            "requested_irreversible_acts",
            "blocking_claims",
            "known_limits",
            "evidence_paths",
        ),
        "promotion-packet",
    )
    if doc["schema"] != "v6-promotion-packet@1":
        raise AssertionError("unexpected promotion packet schema")
    if doc["self_certification"] != "refused":
        raise AssertionError("promotion packet must refuse self-certification")
    if doc["readiness"] == "V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE":
        if doc["independent_gauntlet"] != "GO":
            raise AssertionError("cannot be operator-ready without independent Gauntlet GO")


def validate_candidate_coverage(matrix: dict, recon: dict) -> None:
    ids = {c["id"] for c in matrix["claims"]}
    for item in recon["items"]:
        expected = f"CLM-ISSUE-{item['number']}" if item["kind"] == "issue" else f"CLM-PR-{item['number']}"
        if expected not in ids:
            raise AssertionError(f"matrix missing tracker claim {expected}")


def main() -> int:
    matrix_path = V6_DOCS / "claim-to-proof-matrix.json"
    recon_path = V6_DOCS / "issue-pr-reconciliation.json"
    inventory_path = V6_DOCS / "source-inventory.json"
    for path in (matrix_path, recon_path, inventory_path):
        if not path.is_file():
            raise SystemExit(f"missing required artifact: {path}")

    validate_matrix(_load_json(matrix_path))
    validate_reconciliation(_load_json(recon_path))
    validate_source_inventory(_load_json(inventory_path))

    cand_matrix = CANDIDATE_DOCS / "claim-to-proof-matrix.json"
    cand_recon = CANDIDATE_DOCS / "issue-pr-reconciliation.json"
    cand_inventory = CANDIDATE_DOCS / "source-inventory.json"
    cand_packet = CANDIDATE_DOCS / "promotion-packet.json"
    cand_receipt = CANDIDATE_DOCS / "exact-candidate-receipt.json"
    for path in (cand_matrix, cand_recon, cand_inventory, cand_packet, cand_receipt):
        if not path.is_file():
            raise SystemExit(f"missing required candidate artifact: {path}")
    matrix = _load_json(cand_matrix)
    recon = _load_json(cand_recon)
    validate_matrix(matrix)
    validate_reconciliation(recon)
    validate_source_inventory(_load_json(cand_inventory))
    validate_promotion_packet(_load_json(cand_packet))
    validate_candidate_coverage(matrix, recon)
    print("v6 assurance artifacts: schema checks passed (ZI-001 + candidate)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
