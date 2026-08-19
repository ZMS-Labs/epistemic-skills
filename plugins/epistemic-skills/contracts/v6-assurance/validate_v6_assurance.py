#!/usr/bin/env python3
"""Validate v6 assurance JSON artifacts against committed schemas and rules.

Beyond shape checks, this enforces the gauntlet fix-set semantics
(run es-v6-candidate-freeze-2026-08-18):

- R1  verdict binding: an `independent_gauntlet` enum other than NOT_RUN
  requires `independent_gauntlet_ref` naming a run id, an ON-DISK verdict
  artifact, and the exact candidate SHA; the artifact must itself name that
  SHA. A bare enum flip is not a verdict. Terminal readiness additionally
  requires GO, EMPTY blocking_claims, and a recorded operator acceptance
  whose verdict_ref matches (R13).
- R12 derived blocking: `blocking_claims` must equal `derive_blocking(...)`
  recomputed from the matrix — a hand-edited blocking list fails.
- R5  content binding: the source inventory's per-file sha256 digests are
  recomputed from the tree; any divergence fails (the restamp class).
- R14 requirement register: every registered requirement (es#191 claim and
  evidence classes; RELEASING.md gates) maps to existing matrix claims or an
  explicit disposition with a reason.

Version gating: legacy @1 artifacts (the ES6-ZI-001 baseline and any
pre-fix-set candidate packet) get the original shape checks plus an explicit
LEGACY notice; the strong rules bind on @2 artifacts, which the generator
now emits — and a packet may NEVER reach the terminal readiness state on @1.
This file is the single home of `derive_blocking`; the generator imports it.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
CONTRACT_ROOT = REPO_ROOT / "plugins/epistemic-skills/contracts/v6-assurance"
V6_DOCS = REPO_ROOT / "docs/v6/ES6-ZI-001"
CANDIDATE_DOCS = REPO_ROOT / "docs/v6/ES6-V6-CANDIDATE"
REGISTER_PATH = CONTRACT_ROOT / "requirement-register.json"

TERMINAL = "V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE"

# Owners whose non-PROVED claims gate readiness (mirrored by the generator,
# which imports derive_blocking from here — one home, no drift).
OPERATOR_CLASS_OWNERS = {"operator", "operator+agent", "joint", "independent-panel"}

# The closed owner vocabulary (R4-NF4). Every matrix claim's owner must be one
# of these; the operator-class subset above decides channel membership. Keeping
# the vocabulary closed is what makes is_operator_class total rather than a
# best-effort string test.
# "program" owns exactly one row: the parent tracker issue (es#191) whose
# census entry stays open until the program itself closes. It is deliberately
# NOT operator-class — it is a P3 census row channeled by the reconciliation
# artifact and walked at acceptance item 3, not a hold anyone can discharge.
# The vocabulary check found it on its first run (R4-NF4), which is the point:
# an owner spelling nobody classified was sitting in the shipped matrix.
OWNER_VOCABULARY = OPERATOR_CLASS_OWNERS | {"agent", "program"}


def is_operator_class(owner: str) -> bool:
    """The ONE owner predicate for the R12 derivation and the S2 channel
    law. R3-NF6: derive_blocking tested membership in the set above while
    the channel enforcer and the generator's derivation tested the
    substring 'operator' — under that seam a joint-owned LIMITED P1/P2
    claim silently dropped from every machine channel. Every owner test
    routes through here now; matching is set membership, never substrings."""
    return owner in OPERATOR_CLASS_OWNERS


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_keys(obj: dict, keys: tuple[str, ...], label: str) -> None:
    missing = [k for k in keys if k not in obj]
    if missing:
        raise AssertionError(f"{label} missing keys: {missing}")


def derive_blocking(claims: list[dict]) -> list[str]:
    """R12: the one derivation of blocking_claims from matrix rows."""
    block = []
    for claim in claims:
        severity = claim.get("consequence_severity", "P3")
        status = claim["status"]
        owner = claim["owner"]
        if status == "BLOCKED":
            block.append(claim["id"])
        elif severity == "P1" and status != "PROVED":
            block.append(claim["id"])
        elif (
            is_operator_class(owner)
            and status not in {"PROVED", "LIMITED"}
            and severity != "P3"
        ):
            block.append(claim["id"])
    return sorted(set(block))


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
    with_severity = 0
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
        # R4-NF4: owner presence was checked, but never its VOCABULARY. An
        # out-of-vocabulary operator-ish spelling ("operator-team", "Operator")
        # would sit outside is_operator_class and fall silently out of both
        # machine channels. The vocabulary is closed and checked here, so a new
        # owner class is a deliberate edit to OWNER_VOCABULARY plus a decision
        # about whether it is operator-class.
        if claim["owner"] not in OWNER_VOCABULARY:
            raise AssertionError(
                f"claim {claim['id']}: owner {claim['owner']!r} is outside the "
                f"closed owner vocabulary {sorted(OWNER_VOCABULARY)} — add it "
                "deliberately and decide whether it is operator-class "
                "(is_operator_class), never by accident"
            )
        if "consequence_severity" in claim:
            if claim["consequence_severity"] not in {"P1", "P2", "P3"}:
                raise AssertionError(
                    f"claim {claim['id']}: bad consequence_severity "
                    f"{claim['consequence_severity']!r}"
                )
            with_severity += 1
    # Severity is all-or-none: a matrix where only SOME rows are classified
    # would make the blocking derivation silently partial.
    if 0 < with_severity < len(doc["claims"]):
        raise AssertionError(
            f"consequence_severity on {with_severity} of {len(doc['claims'])} "
            "claims — must be all or none"
        )


def matrix_has_severity(doc: dict) -> bool:
    return bool(doc["claims"]) and all(
        "consequence_severity" in c for c in doc["claims"]
    )


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


def _tracked_set(root: Path) -> set[str] | None:
    """Git-tracked paths under root, or None when root is not a git worktree
    (synthetic test trees). Used by the S1 guard below. R3-NF7: being inside
    SOME work tree is not enough — a byte-exact non-git copy nested under an
    unrelated repository would answer the enclosing repo's file list and
    false-alarm every inventoried path as untracked; require the work tree's
    toplevel to be root itself, else treat the tree as non-git."""
    import subprocess

    probe = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True,
    )
    if probe.returncode != 0 or probe.stdout.strip() != "true":
        return None
    top = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
        capture_output=True, text=True,
    )
    if top.returncode != 0 or Path(top.stdout.strip()).resolve() != root.resolve():
        return None
    out = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    return {p for p in out.decode("utf-8").split("\0") if p}


def validate_source_inventory(doc: dict, root: Path = REPO_ROOT) -> list[str]:
    """Returns notices; raises on failure. @2 recomputes every digest (R5)."""
    _require_keys(
        doc,
        ("schema", "exact_start_sha", "generated_at", "workflows", "contracts", "ci_scripts"),
        "source-inventory",
    )
    if doc["schema"] == "v6-source-inventory@1":
        return ["LEGACY source-inventory@1: no content digests (R5 binding starts at @2)"]
    if doc["schema"] != "v6-source-inventory@2":
        raise AssertionError("unexpected source inventory schema")
    _require_keys(doc, ("candidate_tree_hash", "file_digests"), "source-inventory@2")
    listed = [*doc["workflows"], *doc["contracts"], *doc["ci_scripts"]]
    digests = doc["file_digests"]
    missing = [rel for rel in listed if rel not in digests]
    if missing:
        raise AssertionError(f"source-inventory@2: files without digests: {missing[:5]}")
    notices: list[str] = []
    # S1 (kimi run es-v6-rc2-gauntlet-kimi-2026-08-18): an inventory must
    # never seal untracked host state — the rc2 freeze sealed 17 volatile
    # __pycache__/*.pyc digests and failed on every clean checkout. Both
    # sides now hold the line: the generator enumerates via git ls-files,
    # and this guard rejects any inventoried path git does not track.
    tracked = _tracked_set(root)
    if tracked is None:
        notices.append("root is not a git worktree: INVENTORY_UNTRACKED guard skipped (synthetic tree)")
    else:
        untracked = sorted(rel for rel in digests if rel not in tracked)
        if untracked:
            raise AssertionError(
                "S1 INVENTORY_UNTRACKED: sealed digests name paths git does "
                f"not track (volatile host state): {untracked[:10]}"
            )
    mismatched: list[str] = []
    for rel, recorded in digests.items():
        path = root / rel
        if not path.is_file():
            mismatched.append(f"{rel} (absent)")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != recorded:
            mismatched.append(rel)
    if mismatched:
        raise AssertionError(
            "R5 DIGEST MISMATCH: inventoried files changed after the packet "
            f"was generated (restamp class): {mismatched[:10]}"
        )
    return notices


def validate_promotion_packet(doc: dict, root: Path = REPO_ROOT) -> list[str]:
    """Returns notices; raises on failure. R1/R13 bind on @2."""
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
    notices: list[str] = []
    version = doc["schema"]
    if version not in {"v6-promotion-packet@1", "v6-promotion-packet@2"}:
        raise AssertionError("unexpected promotion packet schema")
    if doc["self_certification"] != "refused":
        raise AssertionError("promotion packet must refuse self-certification")

    if version == "v6-promotion-packet@1":
        if doc["readiness"] == TERMINAL:
            raise AssertionError(
                "terminal readiness is REFUSED on a v1 packet: regenerate at "
                "@2 so verdict binding and operator acceptance can be checked"
            )
        if doc["readiness"] != TERMINAL and doc["independent_gauntlet"] == "GO":
            raise AssertionError("GO on a v1 packet cannot be verdict-bound; regenerate at @2")
        notices.append("LEGACY promotion-packet@1: R1/R13 binding starts at @2")
        return notices

    _require_keys(doc, ("independent_gauntlet_ref",), "promotion-packet@2")
    ref = doc["independent_gauntlet_ref"]
    enum = doc["independent_gauntlet"]
    if enum == "NOT_RUN":
        if ref is not None:
            raise AssertionError("independent_gauntlet_ref must be null while NOT_RUN")
    else:
        # R1: any recorded verdict must be bound to a real, on-disk run.
        if not isinstance(ref, dict):
            raise AssertionError(
                f"independent_gauntlet={enum!r} requires independent_gauntlet_ref "
                "(a bare enum is not a verdict)"
            )
        _require_keys(ref, ("gauntlet_run_id", "verdict_path", "subject_sha"), "independent_gauntlet_ref")
        if ref["subject_sha"] != doc["candidate_sha"]:
            raise AssertionError(
                "verdict subject_sha != candidate_sha: a verdict against a "
                "different SHA does not transfer"
            )
        verdict_file = root / ref["verdict_path"]
        if not verdict_file.is_file():
            raise AssertionError(
                f"verdict artifact not on disk: {ref['verdict_path']} — the "
                "enum does not constitute the verdict"
            )
        verdict_text = verdict_file.read_text(encoding="utf-8", errors="replace")
        if doc["candidate_sha"] not in verdict_text:
            raise AssertionError(
                "verdict artifact does not name the candidate SHA — refusing "
                "an unbound or recycled verdict"
            )

    for limit in doc["known_limits"]:
        _require_keys(limit, ("id", "kind", "statement", "release_consequence", "owner"), f"known_limit {limit.get('id', '?')}")

    acceptance = doc.get("operator_acceptance")
    if acceptance is not None:
        _require_keys(acceptance, ("accepted_by", "accepted_at", "verdict_ref"), "operator_acceptance")
        if enum != "GO":
            raise AssertionError("operator_acceptance recorded without a GO verdict")
        if acceptance["verdict_ref"] != ref:
            raise AssertionError("operator_acceptance.verdict_ref != independent_gauntlet_ref")

    if doc["readiness"] == TERMINAL:
        if enum != "GO":
            raise AssertionError("cannot be operator-ready without independent Gauntlet GO")
        if doc["blocking_claims"]:
            raise AssertionError(
                f"terminal readiness with {len(doc['blocking_claims'])} open "
                "blocking claims — the forgery-drill class (R1)"
            )
        if acceptance is None:
            raise AssertionError(
                "terminal readiness requires a recorded operator_acceptance "
                "(R13; see docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md)"
            )
    return notices


def validate_blocking_derivation(matrix: dict, packet: dict) -> list[str]:
    """R12: the packet's blocking list must be the matrix derivation."""
    if not matrix_has_severity(matrix):
        return ["LEGACY matrix without consequence_severity: blocking derivation not checked"]
    expected = derive_blocking(matrix["claims"])
    actual = sorted(packet["blocking_claims"])
    if actual != expected:
        raise AssertionError(
            "R12 BLOCKING DRIFT: packet blocking_claims is not the matrix "
            f"derivation. expected={expected} actual={actual}"
        )
    return []


def validate_operator_channel(matrix: dict, packet: dict) -> list[str]:
    """S2 channel law (operator ruling 2026-08-18; kimi run
    es-v6-rc2-gauntlet-kimi-2026-08-18, CL-2 synthesis):

    Every P1/P2 claim whose owner is in the operator CLASS (is_operator_class
    — the same predicate derive_blocking uses; R3-NF6 closed the
    substring-vs-set seam that silently uncovered joint-owned claims) must
    occupy a machine channel while it is open — blocking_claims for
    non-PROVED non-LIMITED statuses (the R12 derivation already puts it
    there), or a known_limits entry naming it via its `claim` field for
    LIMITED (derived by the generator, so it cannot be dropped by hand).
    PROVED operator claims are completed acts (row-only); P3 tracker census
    rows are channeled by the reconciliation artifact per
    acceptance-procedure item 3. The identical law is codified in
    requirement-register.json (operator_channel_law) so the register and
    this derivation agree. Known residual, recorded not hidden (R3-NF6 /
    ledger entry 18 revisit_when): an operator-class P3 claim that is NOT a
    census row occupies no machine channel; no such claim exists, and one
    emerging triggers the ruling's revisit clause.
    """
    if not matrix_has_severity(matrix):
        return ["LEGACY matrix without consequence_severity: operator channel law not checked"]
    blocking = set(packet["blocking_claims"])
    named = {kl.get("claim") for kl in packet["known_limits"] if kl.get("claim")}
    for claim in matrix["claims"]:
        if not is_operator_class(claim["owner"]):
            continue
        if claim.get("consequence_severity", "P3") == "P3":
            continue
        if claim["status"] == "PROVED":
            continue
        cid = claim["id"]
        if cid in blocking or cid in named:
            continue
        raise AssertionError(
            f"S2 CHANNEL DROP: operator-class {claim['status']} claim {cid} "
            "appears in neither blocking_claims nor a known_limits entry "
            "naming it (claim field)"
        )
    return []


def validate_register(register: dict, matrix: dict) -> None:
    """R14: every registered requirement maps to claims or a disposition."""
    _require_keys(register, ("schema", "source_clauses", "crosswalk"), "requirement-register")
    if register["schema"] != "v6-requirement-register@1":
        raise AssertionError("unexpected requirement register schema")
    matrix_ids = {c["id"] for c in matrix["claims"]}
    for section, clause in register["source_clauses"].items():
        crosswalk = register["crosswalk"].get(section)
        if crosswalk is None:
            raise AssertionError(f"register section {section!r} has no crosswalk")
        for item in clause["items"]:
            entry = crosswalk.get(item)
            if entry is None:
                raise AssertionError(
                    f"R14: registered requirement {section}/{item} has no "
                    "crosswalk entry (neither claims nor disposition)"
                )
            claims = entry.get("claims", [])
            disposition = entry.get("disposition")
            if not claims and not disposition:
                raise AssertionError(
                    f"R14: {section}/{item} maps to neither claims nor an "
                    "explicit disposition"
                )
            if disposition and not entry.get("reason"):
                raise AssertionError(f"R14: {section}/{item} disposition lacks a reason")
            missing = [c for c in claims if c not in matrix_ids]
            if missing:
                raise AssertionError(
                    f"R14: {section}/{item} cites claims absent from the "
                    f"matrix: {missing}"
                )
        extra = set(crosswalk) - set(clause["items"])
        if extra:
            raise AssertionError(
                f"register section {section!r} has crosswalk entries for "
                f"unregistered items: {sorted(extra)}"
            )


def main() -> int:
    notices: list[str] = []
    matrix_path = V6_DOCS / "claim-to-proof-matrix.json"
    recon_path = V6_DOCS / "issue-pr-reconciliation.json"
    inventory_path = V6_DOCS / "source-inventory.json"
    for path in (matrix_path, recon_path, inventory_path):
        if not path.is_file():
            raise SystemExit(f"missing required artifact: {path}")

    validate_matrix(_load_json(matrix_path))
    validate_reconciliation(_load_json(recon_path))
    notices += validate_source_inventory(_load_json(inventory_path), REPO_ROOT)

    cand_matrix = CANDIDATE_DOCS / "claim-to-proof-matrix.json"
    cand_recon = CANDIDATE_DOCS / "issue-pr-reconciliation.json"
    cand_inventory = CANDIDATE_DOCS / "source-inventory.json"
    cand_packet = CANDIDATE_DOCS / "promotion-packet.json"
    cand_receipt = CANDIDATE_DOCS / "exact-candidate-receipt.json"
    required = (cand_matrix, cand_recon, cand_inventory, cand_packet, cand_receipt)
    present = [p for p in required if p.is_file()]
    if not present:
        # PRE-FREEZE state: the C/C+1 discipline means the code-final
        # candidate commit C legitimately carries NO packet (the packet is
        # generated AT C and committed as C+1; a superseded packet is
        # deleted WHOLE with its repair, immutable in history at its own
        # freeze commit). A tree with no packet CLAIMS nothing — there is
        # nothing to certify and nothing to counterfeit; the terminal state
        # lives inside a packet, so it is unreachable from here. R3-NF7:
        # PRE-FREEZE requires the packet DIRECTORY empty or absent — core
        # artifacts gone but README/evidence remaining is a hand-pruned
        # seal, and that is TORN, not pre-freeze.
        leftovers = (
            sorted(str(p.relative_to(CANDIDATE_DOCS)) for p in CANDIDATE_DOCS.rglob("*") if p.is_file())
            if CANDIDATE_DOCS.is_dir() else []
        )
        if leftovers:
            raise SystemExit(
                "TORN candidate packet — no core artifacts but "
                f"{len(leftovers)} file(s) remain under {CANDIDATE_DOCS.name}/ "
                f"(R3-NF7: full-deletion with leftovers is not PRE-FREEZE): {leftovers[:5]}"
            )
        print("note: PRE-FREEZE tree — no candidate packet present; ZI-001 checks only")
        for notice in notices:
            print(f"note: {notice}")
        print("v6 assurance artifacts: schema + rule checks passed (ZI-001; no candidate packet)")
        return 0
    if len(present) != len(required):
        # A TORN packet is never legitimate — partial artifacts are exactly
        # how a half-regenerated or hand-pruned freeze would present.
        missing = [str(p) for p in required if not p.is_file()]
        raise SystemExit(f"TORN candidate packet — missing: {missing}")
    matrix = _load_json(cand_matrix)
    recon = _load_json(cand_recon)
    packet = _load_json(cand_packet)
    validate_matrix(matrix)
    # R3-NF6: a wholly severity-less matrix would degrade BOTH the blocking
    # derivation and the channel law to notices. Legitimate only for the
    # legacy @1 lineage — a committed @2 candidate must be fully classified.
    if packet.get("schema") == "v6-promotion-packet@2" and not matrix_has_severity(matrix):
        raise AssertionError(
            "R3-NF6: a @2 candidate packet requires consequence_severity on "
            "every matrix claim — the channel and blocking laws must not "
            "degrade to notices on a committed candidate"
        )
    validate_reconciliation(recon)
    notices += validate_source_inventory(_load_json(cand_inventory), REPO_ROOT)
    notices += validate_promotion_packet(packet, REPO_ROOT)
    notices += validate_blocking_derivation(matrix, packet)
    notices += validate_operator_channel(matrix, packet)
    validate_candidate_coverage(matrix, recon)
    # S3: the packet README must name the subject SHA literally (R4's letter).
    if packet["schema"] == "v6-promotion-packet@2":
        readme = CANDIDATE_DOCS / "README.md"
        if not readme.is_file() or packet["candidate_sha"] not in readme.read_text(encoding="utf-8"):
            raise AssertionError(
                "S3 README_SHA: the packet README must literally name the "
                f"candidate SHA {packet['candidate_sha'][:12]}… (R4's letter)"
            )

    if not REGISTER_PATH.is_file():
        raise SystemExit(f"missing requirement register: {REGISTER_PATH}")
    register = _load_json(REGISTER_PATH)
    if packet["schema"] == "v6-promotion-packet@2":
        validate_register(register, matrix)
    else:
        notices.append(
            "LEGACY packet@1: register crosswalk enforcement starts when the "
            "freeze regenerates artifacts at @2"
        )

    for notice in notices:
        print(f"note: {notice}")
    print("v6 assurance artifacts: schema + rule checks passed (ZI-001 + candidate)")
    return 0


def validate_candidate_coverage(matrix: dict, recon: dict) -> None:
    ids = {c["id"] for c in matrix["claims"]}
    for item in recon["items"]:
        expected = f"CLM-ISSUE-{item['number']}" if item["kind"] == "issue" else f"CLM-PR-{item['number']}"
        if expected not in ids:
            raise AssertionError(f"matrix missing tracker claim {expected}")


if __name__ == "__main__":
    raise SystemExit(main())
