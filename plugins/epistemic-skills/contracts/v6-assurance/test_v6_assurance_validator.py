#!/usr/bin/env python3
"""Planted RED controls for validate_v6_assurance.py (gauntlet fix set).

Each rule that exists because a forgery or drift class was demonstrated at
the NO-GO subject must FAIL CLOSED on a synthetic replay of that class and
pass on the honest control — R1 (enum-flip forgery, unbound verdicts),
R12 (hand-edited blocking), R5 (post-freeze digest mutation), R13
(acceptance recording), R14 (register requirement with no covering claim).
"""

from __future__ import annotations

import copy
import importlib.util
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location(
    "validate_v6_assurance", HERE / "validate_v6_assurance.py"
)
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)

SHA = "a" * 40
RUN_ID = "es-v6-test-run"
VERDICT_REL = "docs/gauntlet-runs/es-v6-test-run/arbitration.md"


def base_matrix() -> dict:
    def claim(cid: str, status: str, owner: str, severity: str) -> dict:
        return {
            "id": cid,
            "statement": "s",
            "authority": "a",
            "subject": "x",
            "oracle": "o",
            "falsifier": "f",
            "environment": "e",
            "independence": "i",
            "evidence_tier": "R1",
            "status": status,
            "release_consequence": "c",
            "consequence_severity": severity,
            "owner": owner,
            "closure_path": "p",
        }

    return {
        "schema": "claim-to-proof-matrix@1",
        "program": "T",
        "exact_start_sha": SHA,
        "generated_at": "t",
        "claims": [
            claim("CLM-ALPHA", "PROVED", "agent", "P1"),
            claim("CLM-BETA", "PROVED", "agent", "P2"),
            claim("CLM-GAMMA", "LIMITED", "agent", "P3"),
        ],
    }


def base_packet(root: Path) -> dict:
    verdict = root / VERDICT_REL
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text(
        f"# arbitration\ncomputed verdict: GO\nsubject SHA {SHA}\n",
        encoding="utf-8",
    )
    return {
        "schema": "v6-promotion-packet@2",
        "program": "T",
        "issue": 191,
        "candidate_sha": SHA,
        "generated_at": "t",
        "readiness": "V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE",
        "self_certification": "refused",
        "independent_gauntlet": "GO",
        "independent_gauntlet_ref": {
            "gauntlet_run_id": RUN_ID,
            "verdict_path": VERDICT_REL,
            "subject_sha": SHA,
        },
        "rollback": "r",
        "requested_irreversible_acts": [],
        "blocking_claims": [],
        "known_limits": [
            {
                "id": "KL-X",
                "kind": "integrity",
                "statement": "s",
                "release_consequence": "c",
                "owner": "agent",
            }
        ],
        "operator_acceptance": {
            "accepted_by": "operator-login",
            "accepted_at": "2026-08-18T00:00:00Z",
            "verdict_ref": {
                "gauntlet_run_id": RUN_ID,
                "verdict_path": VERDICT_REL,
                "subject_sha": SHA,
            },
        },
        "evidence_paths": ["x"],
    }


def expect_fail(name: str, fn, needle: str, failures: list[str]) -> None:
    try:
        fn()
    except AssertionError as exc:
        if needle.lower() in str(exc).lower():
            print(f"[PASS] planted {name} fails closed")
        else:
            failures.append(f"{name}: wrong error: {exc}")
            print(f"[FAIL] planted {name}: wrong error: {exc}")
    else:
        failures.append(f"{name}: not rejected")
        print(f"[FAIL] planted {name} was NOT rejected")


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)

        # Honest control: terminal packet with bound GO verdict + acceptance.
        packet = base_packet(root)
        notes = MOD.validate_promotion_packet(packet, root)
        if notes:
            failures.append(f"honest terminal packet raised notices: {notes}")
            print(f"[FAIL] honest terminal packet: {notes}")
        else:
            print("[PASS] honest terminal @2 packet validates")

        # R1: the forgery drill — enum GO with open blocking claims.
        forged = copy.deepcopy(packet)
        forged["blocking_claims"] = ["CLM-ALPHA"]
        expect_fail(
            "terminal-with-open-blockers", lambda: MOD.validate_promotion_packet(forged, root),
            "forgery-drill", failures,
        )

        # R1: GO with no ref at all.
        bare = copy.deepcopy(packet)
        bare["independent_gauntlet_ref"] = None
        del bare["operator_acceptance"]
        expect_fail(
            "bare-enum-GO", lambda: MOD.validate_promotion_packet(bare, root),
            "bare enum", failures,
        )

        # R1: verdict artifact missing from disk.
        ghost = copy.deepcopy(packet)
        ghost["independent_gauntlet_ref"]["verdict_path"] = "docs/gauntlet-runs/nope/arbitration.md"
        ghost["operator_acceptance"]["verdict_ref"]["verdict_path"] = "docs/gauntlet-runs/nope/arbitration.md"
        expect_fail(
            "verdict-not-on-disk", lambda: MOD.validate_promotion_packet(ghost, root),
            "not on disk", failures,
        )

        # R1: verdict bound to a DIFFERENT SHA does not transfer.
        wrong = copy.deepcopy(packet)
        wrong["independent_gauntlet_ref"]["subject_sha"] = "b" * 40
        expect_fail(
            "verdict-for-other-sha", lambda: MOD.validate_promotion_packet(wrong, root),
            "does not transfer", failures,
        )

        # R1: verdict artifact that never names the candidate SHA.
        unbound = copy.deepcopy(packet)
        (root / VERDICT_REL).write_text("# arbitration with no sha\n", encoding="utf-8")
        expect_fail(
            "verdict-without-sha", lambda: MOD.validate_promotion_packet(unbound, root),
            "recycled", failures,
        )
        (root / VERDICT_REL).write_text(
            f"# arbitration\ncomputed verdict: GO\nsubject SHA {SHA}\n", encoding="utf-8"
        )

        # R13: terminal without recorded operator acceptance.
        unaccepted = copy.deepcopy(packet)
        del unaccepted["operator_acceptance"]
        expect_fail(
            "terminal-without-acceptance", lambda: MOD.validate_promotion_packet(unaccepted, root),
            "operator_acceptance", failures,
        )

        # R13: acceptance recorded on a non-GO packet.
        premature = copy.deepcopy(packet)
        premature["readiness"] = "NOT_READY"
        premature["independent_gauntlet"] = "NO-GO"
        expect_fail(
            "acceptance-on-no-go", lambda: MOD.validate_promotion_packet(premature, root),
            "without a GO verdict", failures,
        )

        # Terminal on a v1 packet is refused outright.
        v1 = copy.deepcopy(packet)
        v1["schema"] = "v6-promotion-packet@1"
        expect_fail(
            "terminal-on-v1", lambda: MOD.validate_promotion_packet(v1, root),
            "regenerate", failures,
        )

        # R12: hand-edited blocking list diverging from the derivation.
        matrix = base_matrix()
        matrix["claims"][0]["status"] = "PARTIAL"  # P1 not PROVED -> must block
        honest_block = MOD.derive_blocking(matrix["claims"])
        if honest_block != ["CLM-ALPHA"]:
            failures.append(f"derive_blocking wrong: {honest_block}")
            print(f"[FAIL] derive_blocking: {honest_block}")
        else:
            print("[PASS] derive_blocking blocks the P1 non-PROVED claim")
        drifted = copy.deepcopy(packet)
        drifted["readiness"] = "NOT_READY"
        drifted["blocking_claims"] = []  # hand-scrubbed
        expect_fail(
            "hand-edited-blocking", lambda: MOD.validate_blocking_derivation(matrix, drifted),
            "blocking drift", failures,
        )

        # R5: digest mutation after generation.
        target = root / "scripts" / "tool.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("print('frozen')\n", encoding="utf-8")
        import hashlib
        inventory = {
            "schema": "v6-source-inventory@2",
            "exact_start_sha": SHA,
            "candidate_tree_hash": "t" * 40,
            "generated_at": "t",
            "workflows": [],
            "contracts": [],
            "ci_scripts": ["scripts/tool.py"],
            "file_digests": {
                "scripts/tool.py": hashlib.sha256(target.read_bytes()).hexdigest()
            },
        }
        if MOD.validate_source_inventory(copy.deepcopy(inventory), root) == []:
            print("[PASS] honest @2 inventory digest verifies")
        else:
            failures.append("honest inventory raised notices")
        target.write_text("print('mutated after freeze')\n", encoding="utf-8")
        expect_fail(
            "post-freeze-mutation", lambda: MOD.validate_source_inventory(copy.deepcopy(inventory), root),
            "digest mismatch", failures,
        )

        # R14: register requirement with no covering claim.
        register = {
            "schema": "v6-requirement-register@1",
            "source_clauses": {
                "claim_classes": {"authority": "t", "items": ["security"]},
            },
            "crosswalk": {"claim_classes": {"security": {"claims": ["CLM-ALPHA"]}}},
        }
        try:
            MOD.validate_register(register, matrix)
            print("[PASS] honest register validates")
        except AssertionError as exc:
            failures.append(f"honest register rejected: {exc}")
            print(f"[FAIL] honest register rejected: {exc}")
        orphan = copy.deepcopy(register)
        orphan["crosswalk"]["claim_classes"]["security"] = {"claims": ["CLM-NOPE"]}
        expect_fail(
            "register-cites-missing-claim", lambda: MOD.validate_register(orphan, matrix),
            "absent from", failures,
        )
        bare_req = copy.deepcopy(register)
        bare_req["crosswalk"]["claim_classes"]["security"] = {}
        expect_fail(
            "register-requirement-unmapped", lambda: MOD.validate_register(bare_req, matrix),
            "neither claims nor", failures,
        )

        # Severity must be all-or-none on a matrix.
        partial_sev = base_matrix()
        del partial_sev["claims"][1]["consequence_severity"]
        expect_fail(
            "partial-severity-matrix", lambda: MOD.validate_matrix(partial_sev),
            "all or none", failures,
        )

    print(
        f"v6 assurance validator self-test: {'PASS' if not failures else 'FAIL'}"
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
