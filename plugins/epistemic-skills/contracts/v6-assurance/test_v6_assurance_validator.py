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
        inv_notes = MOD.validate_source_inventory(copy.deepcopy(inventory), root)
        if all("not a git worktree" in n for n in inv_notes):
            print("[PASS] honest @2 inventory digest verifies (synthetic-tree notice only)")
        else:
            failures.append(f"honest inventory raised notices: {inv_notes}")
        target.write_text("print('mutated after freeze')\n", encoding="utf-8")
        expect_fail(
            "post-freeze-mutation", lambda: MOD.validate_source_inventory(copy.deepcopy(inventory), root),
            "digest mismatch", failures,
        )

        # S1: an inventory sealing an UNTRACKED path (volatile host state)
        # must fail closed in a real git worktree — the rc2 defect class.
        import subprocess as sp
        gitroot = root / "gitrepo"
        (gitroot / "scripts").mkdir(parents=True)
        tracked_file = gitroot / "scripts" / "tool.py"
        tracked_file.write_text("print('frozen')\n", encoding="utf-8")
        volatile = gitroot / "scripts" / "__pycache__"
        volatile.mkdir()
        pyc = volatile / "tool.cpython-311.pyc"
        pyc.write_bytes(b"\x00volatile")
        sp.run(["git", "init", "-q"], cwd=gitroot, check=True)
        sp.run(["git", "add", "scripts/tool.py"], cwd=gitroot, check=True)
        good_inv = {
            "schema": "v6-source-inventory@2",
            "exact_start_sha": SHA,
            "candidate_tree_hash": "t" * 40,
            "generated_at": "t",
            "workflows": [],
            "contracts": [],
            "ci_scripts": ["scripts/tool.py"],
            "file_digests": {
                "scripts/tool.py": hashlib.sha256(tracked_file.read_bytes()).hexdigest()
            },
        }
        if MOD.validate_source_inventory(copy.deepcopy(good_inv), gitroot) == []:
            print("[PASS] tracked-only inventory verifies in a git worktree")
        else:
            failures.append("tracked-only inventory raised notices in git worktree")
        sealed_pyc = copy.deepcopy(good_inv)
        sealed_pyc["ci_scripts"].append("scripts/__pycache__/tool.cpython-311.pyc")
        sealed_pyc["file_digests"]["scripts/__pycache__/tool.cpython-311.pyc"] = (
            hashlib.sha256(pyc.read_bytes()).hexdigest()
        )
        expect_fail(
            "inventory-seals-untracked-pyc",
            lambda: MOD.validate_source_inventory(copy.deepcopy(sealed_pyc), gitroot),
            "inventory_untracked", failures,
        )

        # S2: an operator-owned open claim outside both machine channels
        # must fail closed; naming it via a known_limits claim field passes.
        op_matrix = base_matrix()
        op_matrix["claims"][2]["owner"] = "operator"
        op_matrix["claims"][2]["consequence_severity"] = "P2"  # LIMITED already
        dropped = copy.deepcopy(packet)
        dropped["readiness"] = "NOT_READY"
        dropped["blocking_claims"] = []
        expect_fail(
            "operator-limited-claim-dropped",
            lambda: MOD.validate_operator_channel(op_matrix, dropped),
            "channel drop", failures,
        )
        channeled = copy.deepcopy(dropped)
        channeled["known_limits"].append({
            "id": "KL-OPERATOR-GAMMA", "kind": "operator-hold",
            "claim": "CLM-GAMMA", "statement": "s", "release_consequence": "c",
            "owner": "operator",
        })
        try:
            MOD.validate_operator_channel(op_matrix, channeled)
            print("[PASS] derived known_limits entry satisfies the channel law")
        except AssertionError as exc:
            failures.append(f"channeled operator claim rejected: {exc}")

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

        # R4-NF4: the owner VOCABULARY is closed, and the check found a real
        # unclassified spelling ("program") on its first run against the
        # shipped matrix. An owner outside the vocabulary must fail closed.
        stray = base_matrix()
        stray["claims"][0]["owner"] = "operator-team"
        expect_fail(
            "owner-outside-closed-vocabulary",
            lambda: MOD.validate_matrix(stray),
            "closed owner vocabulary", failures,
        )
        if MOD.is_operator_class("program") or "program" not in MOD.OWNER_VOCABULARY:
            failures.append("'program' must be in the vocabulary and NOT operator-class")
            print("[FAIL] 'program' must be in the vocabulary and NOT operator-class")
        else:
            print("[PASS] 'program' is vocabulary-known and deliberately not operator-class")
        if not MOD.OPERATOR_CLASS_OWNERS <= MOD.OWNER_VOCABULARY:
            failures.append("operator-class owners must be a subset of the vocabulary")
            print("[FAIL] operator-class owners must be a subset of the vocabulary")
        else:
            print("[PASS] every operator-class owner is vocabulary-known")

        # R3-NF6: the owner predicate is CLASS membership — a JOINT-owned
        # LIMITED P1/P2 claim outside both channels must fail closed too
        # (the substring-era seam let it drop from every channel silently).
        joint_matrix = base_matrix()
        joint_matrix["claims"][2]["owner"] = "joint"
        joint_matrix["claims"][2]["consequence_severity"] = "P1"
        expect_fail(
            "joint-limited-claim-dropped",
            lambda: MOD.validate_operator_channel(joint_matrix, copy.deepcopy(dropped)),
            "channel drop", failures,
        )
        if not MOD.is_operator_class("operator-adjacent-tool"):
            print("[PASS] owner matching is set membership, not substring")
        else:
            failures.append("is_operator_class matched a non-class owner by substring")
            print("[FAIL] is_operator_class matched a non-class owner by substring")

        # R3-NF7: _tracked_set requires the work tree's TOPLEVEL to be the
        # inventory root — a byte-exact non-git copy nested inside an
        # unrelated repository must degrade to the synthetic-tree notice,
        # never a false S1 alarm blaming 'volatile host state'.
        nested = gitroot / "nested-copy"
        (nested / "scripts").mkdir(parents=True)
        (nested / "scripts" / "tool.py").write_text("print('frozen')\n", encoding="utf-8")
        nested_notes = MOD.validate_source_inventory(copy.deepcopy(good_inv), nested)
        if any("not a git worktree" in n for n in nested_notes):
            print("[PASS] nested non-git copy degrades to a notice, not an S1 false alarm")
        else:
            failures.append(f"nested copy: expected worktree notice, got {nested_notes}")
            print(f"[FAIL] nested copy: expected worktree notice, got {nested_notes}")

    # ---- main()-path controls (R3-NF7: PRE-FREEZE, TORN, S3 and the NF6
    # severity gate were verified only by hand-probes at the rc3 review;
    # they are planted controls now) ----
    def run_main_in(root: Path):
        """Fresh validator instance retargeted at a scratch tree; returns
        (exit_code_or_None, stdout, raised_or_None)."""
        import contextlib
        import io

        spec = importlib.util.spec_from_file_location(
            "validate_v6_assurance_scratch", HERE / "validate_v6_assurance.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        mod.REPO_ROOT = root
        mod.V6_DOCS = root / "docs/v6/ES6-ZI-001"
        mod.CANDIDATE_DOCS = root / "docs/v6/ES6-V6-CANDIDATE"
        mod.REGISTER_PATH = root / "requirement-register.json"
        buf = io.StringIO()
        code = raised = None
        with contextlib.redirect_stdout(buf):
            try:
                code = mod.main()
            except (AssertionError, SystemExit) as exc:
                raised = exc
        return code, buf.getvalue(), raised

    import json as _json

    def write_json(path: Path, obj) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_json.dumps(obj), encoding="utf-8")

    def scratch_zi001(root: Path) -> None:
        zi = root / "docs/v6/ES6-ZI-001"
        legacy_matrix = base_matrix()
        for c in legacy_matrix["claims"]:
            c.pop("consequence_severity", None)
        write_json(zi / "claim-to-proof-matrix.json", legacy_matrix)
        write_json(zi / "issue-pr-reconciliation.json", {
            "schema": "issue-pr-reconciliation@1", "program": "T",
            "exact_start_sha": SHA, "generated_at": "t", "items": []})
        write_json(zi / "source-inventory.json", {
            "schema": "v6-source-inventory@1", "exact_start_sha": SHA,
            "generated_at": "t", "workflows": [], "contracts": [], "ci_scripts": []})
        write_json(root / "requirement-register.json", {
            "schema": "v6-requirement-register@1", "source_clauses": {},
            "crosswalk": {}})

    def scratch_candidate(root: Path, readme_text: str, matrix: dict | None = None) -> None:
        scratch_zi001(root)
        cdir = root / "docs/v6/ES6-V6-CANDIDATE"
        m = matrix if matrix is not None else base_matrix()
        write_json(cdir / "claim-to-proof-matrix.json", m)
        write_json(cdir / "issue-pr-reconciliation.json", {
            "schema": "issue-pr-reconciliation@1", "program": "T",
            "exact_start_sha": SHA, "generated_at": "t", "items": []})
        write_json(cdir / "source-inventory.json", {
            "schema": "v6-source-inventory@1", "exact_start_sha": SHA,
            "generated_at": "t", "workflows": [], "contracts": [], "ci_scripts": []})
        write_json(cdir / "promotion-packet.json", {
            "schema": "v6-promotion-packet@2", "program": "T", "issue": 191,
            "candidate_sha": SHA, "generated_at": "t",
            "readiness": "NOT_READY", "self_certification": "refused",
            "independent_gauntlet": "NOT_RUN", "independent_gauntlet_ref": None,
            "rollback": "r", "requested_irreversible_acts": [],
            "blocking_claims": MOD.derive_blocking(m["claims"]),
            "known_limits": [], "evidence_paths": ["x"]})
        write_json(cdir / "exact-candidate-receipt.json", {"candidate_sha": SHA})
        (cdir / "README.md").write_text(readme_text, encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp2:
        pf = Path(tmp2) / "prefreeze"
        scratch_zi001(pf)
        code, out, raised = run_main_in(pf)
        if code == 0 and raised is None and "PRE-FREEZE" in out:
            print("[PASS] main(): packet-less tree is loud PRE-FREEZE exit 0")
        else:
            failures.append(f"main() PRE-FREEZE: code={code} raised={raised}")
            print(f"[FAIL] main() PRE-FREEZE: code={code} raised={raised}")

        torn1 = Path(tmp2) / "torn-leftovers"
        scratch_zi001(torn1)
        leftdir = torn1 / "docs/v6/ES6-V6-CANDIDATE"
        leftdir.mkdir(parents=True)
        (leftdir / "README.md").write_text("stale seal remnant\n", encoding="utf-8")
        code, out, raised = run_main_in(torn1)
        if isinstance(raised, SystemExit) and "TORN" in str(raised):
            print("[PASS] main(): core deletion with leftovers is TORN, not PRE-FREEZE")
        else:
            failures.append(f"main() torn-leftovers: code={code} raised={raised}")
            print(f"[FAIL] main() torn-leftovers: code={code} raised={raised}")

        torn2 = Path(tmp2) / "torn-partial"
        scratch_zi001(torn2)
        write_json(torn2 / "docs/v6/ES6-V6-CANDIDATE/claim-to-proof-matrix.json",
                   base_matrix())
        code, out, raised = run_main_in(torn2)
        if isinstance(raised, SystemExit) and "TORN" in str(raised):
            print("[PASS] main(): partial candidate artifacts are TORN")
        else:
            failures.append(f"main() torn-partial: code={code} raised={raised}")
            print(f"[FAIL] main() torn-partial: code={code} raised={raised}")

        okroot = Path(tmp2) / "candidate-ok"
        scratch_candidate(okroot, f"subject C = {SHA}\n")
        code, out, raised = run_main_in(okroot)
        if code == 0 and raised is None:
            print("[PASS] main(): honest scratch candidate validates end-to-end")
        else:
            failures.append(f"main() candidate-ok: code={code} raised={raised}")
            print(f"[FAIL] main() candidate-ok: code={code} raised={raised}")

        s3root = Path(tmp2) / "candidate-s3"
        scratch_candidate(s3root, "this README forgot the subject\n")
        code, out, raised = run_main_in(s3root)
        if isinstance(raised, AssertionError) and "S3 README_SHA" in str(raised):
            print("[PASS] main(): README without the literal candidate SHA fails S3")
        else:
            failures.append(f"main() candidate-s3: code={code} raised={raised}")
            print(f"[FAIL] main() candidate-s3: code={code} raised={raised}")

        nosev_matrix = base_matrix()
        for c in nosev_matrix["claims"]:
            c.pop("consequence_severity", None)
        nosevroot = Path(tmp2) / "candidate-nosev"
        scratch_candidate(nosevroot, f"subject C = {SHA}\n", matrix=nosev_matrix)
        code, out, raised = run_main_in(nosevroot)
        if isinstance(raised, AssertionError) and "R3-NF6" in str(raised):
            print("[PASS] main(): severity-less matrix under a @2 packet fails closed")
        else:
            failures.append(f"main() candidate-nosev: code={code} raised={raised}")
            print(f"[FAIL] main() candidate-nosev: code={code} raised={raised}")

    print(
        f"v6 assurance validator self-test: {'PASS' if not failures else 'FAIL'}"
    )
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
