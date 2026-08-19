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
        "CLM-V5-ROUTING",
        "CLM-V5-LEDGERS",
        "CLM-V5-SENTINELS",
        "CLM-V5-MEMBERSHIP",
        "CLM-DISPOSITION-CENSUS",
        "CLM-MC-137",
        "CLM-PUBLIC-CONTENT",
        "CLM-SECRET-SCAN",
        "CLM-COMPATIBILITY",
        "CLM-MC-GUARD-LEXICAL",
        "CLM-DESCRIPTION-BUDGET",
        "CLM-MERGE-190",
        "CLM-MERGE-156",
        "CLM-MERGE-192",
    }
    missing = required - set(ids)
    if missing:
        raise AssertionError(f"missing class claims: {missing}")
    if "CLM-TRACKER-RECONCILED" in ids:
        raise AssertionError(
            "CLM-TRACKER-RECONCILED must stay demoted (R6): the census row is "
            "CLM-DISPOSITION-CENSUS"
        )
    for claim in claims:
        if claim.get("consequence_severity") not in {"P1", "P2", "P3"}:
            raise AssertionError(f"claim {claim['id']} lacks consequence_severity")
    go = next(c for c in claims if c["id"] == "CLM-INDEPENDENT-GAUNTLET")
    if go["status"] != "UNPROVED":
        raise AssertionError("independent Gauntlet must start UNPROVED")
    if go["owner"] != "independent-panel":
        raise AssertionError("Gauntlet owner must not be the implementer")

    hold = tracker_claim(
        "issue",
        999,
        "Some future operator hold",
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
    if hold["id"] != "CLM-ISSUE-999":
        raise AssertionError(hold["id"])
    decided = tracker_claim(
        "issue",
        104,
        "Complete or retire v5 commitments",
        {
            "phase": "decided-2026-08-18",
            "disposition": "decided-implement-all",
            "owner": "agent",
            "evidence_note": "D3",
        },
        [],
    )
    if decided["status"] != "PARTIAL":
        raise AssertionError("a decided disposition must read PARTIAL, not BLOCKED")

    # R12: an open tracker item with no explicit disposition fails generation.
    from v6_generate_candidate_packet import apply_requalification, require_dispositions

    try:
        require_dispositions([{"number": 424242}], [])
    except SystemExit as exc:
        if "UNDISPOSITIONED_TRACKER_ITEMS" not in str(exc):
            raise AssertionError(f"wrong refusal message: {exc}")
    else:
        raise AssertionError("unknown open issue did NOT fail generation (R12)")

    # Requalification flips are evidence-driven and fail closed.
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        capture = Path(tmp) / "requalification.json"
        capture.write_text(json.dumps({
            "candidate_sha": sha,
            "claims": {"CLM-SECRET-SCAN": {
                "conclusion": "success",
                "runs": ["https://github.com/example/example/actions/runs/1"],
            }},
        }), encoding="utf-8")
        requal_claims = class_claims(sha)
        notes = apply_requalification(requal_claims, sha, capture)
        flipped = next(c for c in requal_claims if c["id"] == "CLM-SECRET-SCAN")
        if flipped["status"] != "PROVED" or not notes:
            raise AssertionError("green capture must flip PARTIAL to PROVED")
        capture.write_text(json.dumps({
            "candidate_sha": "b" * 40,
            "claims": {},
        }), encoding="utf-8")
        try:
            apply_requalification(class_claims(sha), sha, capture)
        except SystemExit as exc:
            if "REQUAL_SHA_MISMATCH" not in str(exc):
                raise AssertionError(f"wrong requal refusal: {exc}")
        else:
            raise AssertionError("capture for another SHA was NOT refused")
        capture.write_text(json.dumps({
            "candidate_sha": sha,
            "claims": {"CLM-COMPATIBILITY": {
                "conclusion": "success", "runs": ["u"],
            }},
        }), encoding="utf-8")
        try:
            apply_requalification(class_claims(sha), sha, capture)
        except SystemExit as exc:
            if "REQUAL_BAD_FLIP" not in str(exc):
                raise AssertionError(f"wrong bad-flip refusal: {exc}")
        else:
            raise AssertionError("flip of a non-PARTIAL claim was NOT refused")

    # S1: the inventory enumerates git-tracked files only — never volatile
    # host state like __pycache__ (the rc2 P1: 17 sealed .pyc digests).
    from v6_generate_candidate_packet import build_source_inventory

    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()
    inventory = build_source_inventory(head, "2026-08-18T00:00:00Z")
    volatile = [k for k in inventory["file_digests"] if "__pycache__" in k or k.endswith(".pyc")]
    if volatile:
        raise AssertionError(f"inventory seals volatile host state (S1): {volatile[:3]}")
    tracked = set(
        subprocess.check_output(["git", "ls-files", "-z"], cwd=REPO_ROOT)
        .decode("utf-8").split("\0")
    )
    untracked = [k for k in inventory["file_digests"] if k not in tracked]
    if untracked:
        raise AssertionError(f"inventory names untracked paths (S1): {untracked[:3]}")

    matrix = {"claims": claims}
    packet = build_promotion_packet(sha, "2026-08-18T00:00:00Z", matrix)
    if packet["schema"] != "v6-promotion-packet@2":
        raise AssertionError("packet must be @2")
    # S2: operator-CLASS LIMITED P1/P2 claims get DERIVED known_limits
    # entries naming them (machine channel, operator ruling 2026-08-18).
    # The owner predicate is the validator's is_operator_class — the SAME
    # test derive_blocking uses (R3-NF6 unification; substring-vs-set let a
    # joint-owned claim drop from every channel).
    from v6_generate_candidate_packet import _validator_module, operator_limited_limits
    is_operator_class = _validator_module().is_operator_class
    derived = {kl.get("claim") for kl in packet["known_limits"] if kl.get("claim")}
    for claim in claims:
        if (is_operator_class(claim["owner"]) and claim["status"] == "LIMITED"
                and claim["consequence_severity"] in ("P1", "P2")):
            if claim["id"] not in derived:
                raise AssertionError(
                    f"operator-class LIMITED claim {claim['id']} has no derived "
                    "known_limits entry (S2)")
    # R3-NF4: the description-budget fork is RESOLVED (ledger 17, hybrid
    # Path 2) — the row must say so and its oracle's record facts must exist
    # in this tree (the rc3 packet asserted the fork open against its own
    # ledger).
    budget = next(c for c in claims if c["id"] == "CLM-DESCRIPTION-BUDGET")
    if budget["status"] != "PROVED":
        raise AssertionError("CLM-DESCRIPTION-BUDGET must be PROVED per ledger entry 17 (R3-NF4)")
    if "v6-description-budget-hybrid-path2-20260818-17" not in budget["authority"]:
        raise AssertionError("budget row must cite the recorded ruling id (R3-NF4)")
    spec_text = (REPO_ROOT / "docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md").read_text(encoding="utf-8")
    if "AMENDMENT 2026-08-18 — the D8 estate fork is resolved" not in spec_text:
        raise AssertionError("the Path-2 owner amendment is missing from the v5 spec (R3-NF4 oracle)")
    if "description-byte delta" not in (REPO_ROOT / "RELEASING.md").read_text(encoding="utf-8"):
        raise AssertionError("RELEASING.md lacks the description-byte delta row (R3-NF4 oracle)")
    if "v6-description-budget-hybrid-path2-20260818-17" not in (REPO_ROOT / ".ledger/entries.jsonl").read_text(encoding="utf-8"):
        raise AssertionError("ledger entry 17 missing from the durable store (R3-NF4 oracle)")
    # S2 derivation exemplar on a SYNTHETIC matrix (the live matrix carries
    # no LIMITED operator-class P1/P2 row after R3-NF4): operator and
    # joint-owned LIMITED P1/P2 derive; PROVED and P3 do not (R3-NF6).
    synth = {"claims": [
        {"id": "CLM-A", "statement": "s", "release_consequence": "rc",
         "owner": "operator", "status": "LIMITED", "consequence_severity": "P2"},
        {"id": "CLM-B", "statement": "s", "release_consequence": "rc",
         "owner": "joint", "status": "LIMITED", "consequence_severity": "P1"},
        {"id": "CLM-C", "statement": "s", "release_consequence": "rc",
         "owner": "operator", "status": "PROVED", "consequence_severity": "P1"},
        {"id": "CLM-D", "statement": "s", "release_consequence": "rc",
         "owner": "operator", "status": "LIMITED", "consequence_severity": "P3"},
    ]}
    synth_derived = {kl["claim"] for kl in operator_limited_limits(synth)}
    if synth_derived != {"CLM-A", "CLM-B"}:
        raise AssertionError(
            f"S2 derivation exemplar wrong: {sorted(synth_derived)} — joint-owned "
            "LIMITED P1/P2 must derive (R3-NF6); PROVED/P3 must not")
    if packet["self_certification"] != "refused":
        raise AssertionError("must refuse self-certification")
    if packet["readiness"] != "NOT_READY":
        raise AssertionError("packet must not self-declare operator-ready")
    if packet["requested_irreversible_acts"]:
        raise AssertionError("BUILD packet must request no irreversible acts")
    if packet["independent_gauntlet_ref"] is not None:
        raise AssertionError("NOT_RUN packet must carry a null verdict ref (R1)")
    for limit in packet["known_limits"]:
        if not limit.get("owner"):
            raise AssertionError(f"known limit {limit['id']} lacks an owner (R12)")
    kl_ids = {limit["id"] for limit in packet["known_limits"]}
    for needed in ("KL-RESTAMP", "KL-GUARD-LEXICAL", "KL-DRAFT-CI", "KL-MAIN-137"):
        if needed not in kl_ids:
            raise AssertionError(f"missing known limit {needed}")
    if "KL-MAIN-RED" in kl_ids:
        raise AssertionError(
            "KL-MAIN-RED is retired (R3-NF3: #195 merged green 2026-08-18 as "
            "03b7724) — it must not reappear as a live limit")
    derived = blocking_from_matrix(matrix)
    if packet["blocking_claims"] != derived:
        raise AssertionError("packet blocking_claims must be the matrix derivation (R12)")
    if "CLM-INDEPENDENT-GAUNTLET" not in derived:
        raise AssertionError("independent Gauntlet must block readiness")
    if "CLM-MC-MACOS-CASE" in derived:
        raise AssertionError("a P3 LIMITED disclosure must not auto-block")

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
