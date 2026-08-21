#!/usr/bin/env python3
"""Generate the ES6-V6-CANDIDATE BUILD freeze (issue #191 terminal contract).

This packet is BUILD, not PROMOTION. It may not claim independent Gauntlet GO.
The same actor that produced the work refuses self-certification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs/v6/ES6-V6-CANDIDATE"
PROGRAM = "ES6-V6-CANDIDATE"

# Dispositions from the 2026-08-18 recon map, refreshed for this candidate and
# for the ratified operator interview decisions D1-D15
# (docs/v6/operator-decision-record-2026-08-18.md, echo-certified).
#
# EVERY open tracker item must have an EXPLICIT entry here (R12: a newly
# opened issue must never inherit a disposition silently — generation fails
# closed on any open item this map has never heard of).
ISSUE_DISPOSITIONS: dict[int, dict] = {
    191: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "reconcile-in-matrix",
        "owner": "program",
        "evidence_note": "Parent v6 program; this packet is the BUILD freeze.",
    },
    186: {
        "phase": "decided-2026-08-18",
        "disposition": "decided-disarm-as-authorization",
        "owner": "operator+agent",
        "evidence_note": "Operator decision D6: disarm-as-authorization confirmed as the v6.0.0 regime (zero bypass actors; RELEASING.md step 7 procedure IS the authorization act). Remaining docket items (wiki packet) are PROMOTION-owned.",
    },
    173: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Concurrent missions; naive relaxation fail-opens Stage-C.",
    },
    166: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Non-file envelope; scope empty on live mission.",
    },
    165: {
        "phase": "evidence-process",
        "disposition": "close-when-evidence",
        "owner": "agent",
        "evidence_note": "Codex scan null at cap; not clean coverage.",
    },
    150: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Structured --grants-path for amend discharge.",
    },
    149: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Effects permitted in draft before operator approve.",
    },
    148: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Tier-1 self-accept; derive worker from chain.",
    },
    145: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Synthetic fixture operator names spreading.",
    },
    142: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Capture real harness hook payloads; live wire required.",
    },
    137: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "in-candidate-draft",
        "owner": "agent",
        "evidence_note": "P1+P2 implemented on this candidate (not on main). Draft CI skips required jobs.",
    },
    136: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Cursor CLI hook must use plugin-root path; live CLI required.",
    },
    129: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Antigravity adapter not wired; live harness required.",
    },
    124: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Receipt continuity check design open.",
    },
    118: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "contract@2 receipt hash + tail anchor.",
    },
    105: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "reconcile-in-matrix",
        "owner": "agent",
        "evidence_note": "Exact-candidate public-content gate; ES6-ZI-001 parent-tracker hits allowlisted this packet.",
    },
    104: {
        "phase": "decided-2026-08-18",
        "disposition": "decided-implement-all",
        "owner": "agent",
        "evidence_note": "Operator decision D3: implement ALL v5 design commitments. Implemented on this candidate — see CLM-V5-ROUTING/LEDGERS/SENTINELS/MEMBERSHIP rows.",
    },
    95: {
        "phase": "evidence-process",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Local-cluster CI fallback.",
    },
    89: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Discovery-engine auth canary missing.",
    },
    84: {
        "phase": "decided-2026-08-18",
        "disposition": "decided-ownership-split",
        "owner": "joint",
        "evidence_note": "Operator decision D10: field-pair ownership split confirmed (epistemic-calibration owns the outcome store and resolution loop; epistemic-skills owns emission) and the outcome store is granted operator-visible status. Implementation of the store remains cross-repo work.",
    },
    77: {
        "phase": "evidence-process",
        "disposition": "close-when-evidence",
        "owner": "agent",
        "evidence_note": "Behavioral epoch program; live environment required.",
    },
    40: {
        "phase": "decided-2026-08-18",
        "disposition": "decided-rescope",
        "owner": "operator",
        "evidence_note": "Operator decision D9: cross-family requirement re-scoped into v6-and-future publication gauntlets' Step 7b (first exercised at the next GO-posture verdict per D8). Closing #40 itself remains the operator's act.",
    },
    39: {
        "phase": "evidence-process",
        "disposition": "close-when-evidence",
        "owner": "agent",
        "evidence_note": "Four-arm superiority run; live environment required.",
    },
    162: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "macOS default APFS case-insensitivity; dispatch-only probe.",
    },
    # Mission-custody residue class, verified item-by-item in the 2026-08-18
    # reconciliation sweep: named seams/defects behind the blocked custody
    # parents (#118/#124/#173 lineage), none implemented on this candidate.
    # Each number is listed EXPLICITLY so a newly opened issue can never ride
    # this class silently (R12 hard-fail applies to anything not named here).
    **{
        number: {
            "phase": "custody-build-packet",
            "disposition": "implement-when-unblocked",
            "owner": "agent",
            "evidence_note": "Mission-custody residue; disclosed seam/defect, not implemented on this candidate (2026-08-18 reconciliation sweep).",
        }
        for number in (
            139, 140, 141, 147, 151, 154, 157, 158, 159, 160,
            161, 163, 164, 167, 168, 169, 170,
        )
    },
}

PR_DISPOSITIONS: dict[int, dict] = {
    197: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "in-candidate-draft",
        "owner": "agent",
        "evidence_note": "The successor freeze PR itself (D12); draft until GO + recorded operator acceptance; merging it is PROMOTION.",
    },
    195: {
        "phase": "main-repair",
        "disposition": "operator-merge",
        "owner": "operator",
        "evidence_note": "D11 minimal non-draft fix to main (three exact-file allowlist entries + oracle-audit PyYAML). MERGED 2026-08-18 as squash 03b7724 under the operator's RATIFY-V6-2026-08-18 instruction; main's push runs green at that head — KL-MAIN-RED retired (R3-NF3). Entry kept for the census only if the PR reopens.",
    },
    193: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "in-candidate-draft",
        "owner": "agent",
        "evidence_note": "es#137 P1+P2; included in this candidate tree; stays open as the isolated custody PR per D12; not merged to main.",
    },
    194: {
        "phase": "superseded",
        "disposition": "supersede-and-close",
        "owner": "agent",
        "evidence_note": "Superseded by the rc2 successor freeze PR (operator decision D12); close authorized after the supersession comment carrying the NO-GO verdict pointer (D13). The dead candidate branch keeps its historical NOT_RUN stamp.",
    },
    176: {
        "phase": "park",
        "disposition": "do-not-merge",
        "owner": "agent",
        "evidence_note": "94k-line planning boundary; DCO red; verdict narrow.",
    },
    103: {
        "phase": "supersede",
        "disposition": "harvest-supersede",
        "owner": "agent",
        "evidence_note": "Draft conflicting; harvest unique errata then supersede.",
    },
    100: {
        "phase": "park",
        "disposition": "park",
        "owner": "agent",
        "evidence_note": "Exploratory Fudge/visual craft; not operator-approved.",
    },
}

# R12: there is deliberately NO default disposition. An open tracker item
# absent from the maps above fails generation closed (see load_tracker's
# unknown-item check) — a fresh issue must be dispositioned by a human-read
# edit here, never by inheriting a silent class.

LIVE_LABELS = {"work:live-verification", "gate:live-environment"}
OPERATOR_LABELS = {"gate:operator", "work:decision"}


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def gh_json(args: list[str]) -> list[dict]:
    out = subprocess.check_output(["gh", *args], cwd=REPO_ROOT, text=True)
    data = json.loads(out)
    return data if isinstance(data, list) else [data]


def _now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _tier_from_labels(labels: list[str]) -> str:
    for name in labels:
        if name.startswith("assurance:") and len(name) >= 12:
            token = name.split(":", 1)[1]
            if token in {"R0", "R1", "R2", "R3"}:
                return token
    return "R1"


# R12: release consequence is a STRUCTURED severity, not prose to be parsed.
# P1 = release-deciding; P2 = must be disclosed/limited; P3 = tracked.
CLAIM_SEVERITY: dict[str, str] = {
    "CLM-STDLIB-GATE": "P1",
    "CLM-WF-PATH-COVERAGE": "P2",
    "CLM-ORACLE-REJECT": "P1",
    "CLM-MC-HOOK-POSIX": "P1",
    "CLM-MC-MACOS-CASE": "P3",
    "CLM-PUBLIC-CONTENT": "P1",
    "CLM-V5-DESIGN-COMMITMENTS": "P1",
    "CLM-V5-ROUTING": "P2",
    "CLM-V5-LEDGERS": "P2",
    "CLM-V5-SENTINELS": "P2",
    "CLM-V5-MEMBERSHIP": "P2",
    "CLM-RELEASE-AUTH": "P1",
    "CLM-BEHAVIORAL-EPOCHS": "P2",
    "CLM-HARNESS-LIVE": "P2",
    "CLM-INDEPENDENT-GAUNTLET": "P1",
    "CLM-DISPOSITION-CENSUS": "P2",
    "CLM-REQUIRED-JOB": "P2",
    "CLM-WINDOWS-FS": "P3",
    "CLM-MC-137": "P1",
    "CLM-SECRET-SCAN": "P1",
    "CLM-COMPATIBILITY": "P2",
    "CLM-MC-GUARD-LEXICAL": "P3",
    "CLM-DESCRIPTION-BUDGET": "P2",
    "CLM-MERGE-190": "P1",
    "CLM-MERGE-156": "P1",
    "CLM-MERGE-192": "P1",
}


def class_claims(sha: str) -> list[dict]:
    """Material claim classes required by #191, independent of tracker rows."""
    claims = [
        {
            "id": "CLM-STDLIB-GATE",
            "statement": "The epistemic-flexibility stdlib-checks job exercises every packaged skill contract and integration surface on push/PR to main.",
            "authority": "RELEASING.md gate 5; .github/workflows/epistemic-flexibility.yml",
            "subject": f"commit {sha}",
            "oracle": "cleanroom_ci.sh extracts BOTH single-line and block python steps with a completeness assertion (extraction divergence is FATAL; every skip is named) and all executable steps pass; GitHub stdlib-checks on a non-draft candidate.",
            "falsifier": "A committed change to a gated surface passes push without triggering stdlib-checks or without failing a required step; or the clean-room replicates fewer steps than the workflow declares without naming the difference.",
            "environment": "ubuntu-24.04 CI; clean-room Linux checkout",
            "independence": "Workflow-declared steps; scorer/runner separation in eval harnesses",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 — cannot tag without green stdlib-checks on exact candidate",
            "owner": "agent",
            "closure_path": "Local clean-room evidence this packet; required CI on non-draft PR",
            "linked_issues": [186, 191],
            "evidence_paths": [
                ".github/workflows/epistemic-flexibility.yml",
                ".github/scripts/cleanroom_ci.sh",
                "docs/v6/ES6-V6-CANDIDATE/evidence/clean-baseline.json",
            ],
        },
        {
            "id": "CLM-WF-PATH-COVERAGE",
            "statement": "Workflows running whole-tree readers carry NO pull_request/push paths filter (R7 path A); scoped workflows' filters are supersets of their steps' inputs.",
            "authority": "es#186 docket path-filter guard; ES6-ORACLE-AUDIT; gauntlet ruling R7",
            "subject": "all .github/workflows/*.yml",
            "oracle": "v6_audit_workflow_oracles.py exits 0 — both the uncovered-path rules and the path_filtered_whole_tree_reader rule — with planted RED controls in its self-test.",
            "falsifier": "A change confined to a scanned-but-unlisted file does not dispatch the gate that reads it, or a whole-tree reader reappears behind a paths: filter without a finding.",
            "environment": "repository static analysis",
            "independence": "script distinct from workflow authors; planted controls prove the rules fire",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P2 — silent skip risk on release gate suites",
            "owner": "agent",
            "closure_path": "Oracle audit 0 findings retained this packet",
            "linked_issues": [186, 191],
            "evidence_paths": [
                "docs/v6/ES6-V6-CANDIDATE/evidence/workflow-oracle-audit.json"
            ],
        },
        {
            "id": "CLM-ORACLE-REJECT",
            "statement": "The evidence system can reject a plausible wrong world, bounded to the checkers' planted-control batteries (live-behavioral mutation stays under CLM-BEHAVIORAL-EPOCHS).",
            "authority": "#191 terminal contract",
            "subject": f"commit {sha} checker suites + custody suites",
            "oracle": "Planted RED batteries across the gate: public-content (seeds + digest tamper), sync_skill_surfaces (7-case drift battery), check_no_phantom_skills (routing tables), check_skill_run_ledger, score_sentinels (both directions), workflow-oracle audit, ledger append-only, description budget, loaded-descriptions, v6 assurance validator — each fails closed on its planted case and clean on the honest control.",
            "falsifier": "Any planted defect grades clean, or a checker's self-test passes with its rule inverted (e.g. the R15 scratch-patch RED-proof).",
            "environment": "local Linux + CI ubuntu-24.04 + clean-room replication",
            "independence": "scorer/runner separation; batteries run through the same code path as the live checks",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P1 if oracles cannot fail",
            "owner": "agent",
            "closure_path": "Self-test steps wired in CI ahead of each live check",
            "linked_issues": [191],
        },
        {
            "id": "CLM-MC-HOOK-POSIX",
            "statement": "mission-custody test_custody_hook.py POSIX branch runs in CI on ubuntu-24.04.",
            "authority": ".github/workflows/mission-custody-contract.yml",
            "subject": "plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py",
            "oracle": "mission-custody-contract required job on non-draft PR/push to main.",
            "falsifier": "Hook test file changes without mission-custody-contract workflow dispatch.",
            "environment": "ubuntu-24.04",
            "independence": "CI runner distinct from developer host",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 for custody claims while candidate remains draft (job skipped)",
            "owner": "agent",
            "closure_path": "Local POSIX suite this packet; required CI after PR is marked ready",
            "linked_issues": [136, 137, 142],
        },
        {
            "id": "CLM-MC-MACOS-CASE",
            "statement": "Custody artifact distinctness on case-insensitive APFS is DISCLOSED-DIVERGENT: the contract's deliberately ASCII-only fold keeps 'straße.txt'/'strasse.txt' distinct while APFS merges them under Unicode case folding — two contract-distinct artifacts, one physical file (measured).",
            "authority": "es#162; mission-custody-contract contract-macos job",
            "subject": "custody scope case fold + artifact distinctness on macos-14 APFS",
            "oracle": "workflow_dispatch contract-macos: the es#162 ASCII probe passed, and the first full macOS lifecycle-suite execution measured the Unicode-fold instance — tests distinct-real-file-untouched and distinct-both-files-tracked-separately FAILED because writing the strasse.txt decoy clobbered straße.txt (run 32189655677, 2026-08-18).",
            "falsifier": "The two named tests pass on a case-insensitive APFS runner without a disclosed contract change, or a PASS is recorded after writing secrets/ when scope.out lists Secrets/.",
            "environment": "macos-14 workflow_dispatch only",
            "independence": "dispatch-only diagnostic; not merge-gating per #190 lineage",
            "evidence_tier": "R3",
            "status": "LIMITED",
            "release_consequence": "Disclosed limitation; the ASCII-only fold is the chosen fail direction (folding ß→ss would cause silent custody loss on case-SENSITIVE systems); the platform-side merge is es#162's open work",
            "owner": "agent",
            "closure_path": "es#162 remains open, now carrying the measured Unicode-fold instance",
            "linked_issues": [162, 186],
        },
        {
            "id": "CLM-PUBLIC-CONTENT",
            "statement": "Exact candidate public tree contains no disallowed private identifiers or user-specific paths outside exact-file allowlist.",
            "authority": "RELEASING.md; es#105; check_public_content.py",
            "subject": f"commit {sha} public tree",
            "oracle": "check_public_content.py --self-test and live run both exit 0; every allowlist exemption is digest-bound (R11: tampered bytes at an allowlisted path fail closed, planted control in the self-test).",
            "falsifier": "Seeded private-repo id or user path pattern passes gate; a live scan hits a non-allowlisted file; or changed bytes at an allowlisted path pass without a digest review.",
            "environment": "CI + exact-candidate review record",
            "independence": "checker distinct from content author",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 — item 6b required for v6",
            "owner": "agent",
            # R11b: the honest blast radius — the allowlist exempts WHOLE
            # FILES for every pattern class, now bounded by per-file digests;
            # the #105/#145 fixture-name residue remains open work.
            "closure_path": "Exact-file allowlist is digest-bound (allowlist-stale fails closed); entries for the ES6-ZI-001 coordinates and the D7 gauntlet record are reviewable acts; #105/#145 residue still open",
            "linked_issues": [105, 145],
        },
        {
            "id": "CLM-V5-DESIGN-COMMITMENTS",
            "statement": "Every approved v5 design commitment is implemented on this candidate per operator decision D3 (implement all); the four per-commitment rows below carry the evidence.",
            "authority": "es#104; v5 design spec; operator decision D3 (echo-certified)",
            "subject": "ROUTING.md, intrinsic ledgers, sentinel corpora, structural membership",
            "oracle": "CLM-V5-ROUTING, CLM-V5-LEDGERS, CLM-V5-SENTINELS, CLM-V5-MEMBERSHIP all PROVED; spec AMENDMENT 2026-08-18 reconciles residual wording.",
            "falsifier": "Any per-commitment row is not PROVED, or a public doc promises an artifact that does not exist and is not marked retired.",
            "environment": "repository + operator decision record",
            "independence": "operator decided the path; CI checks verify the implementations",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "Was the successor-GO blocker until D3; discharged by implementation",
            "owner": "agent",
            "closure_path": "docs/v6/operator-decision-record-2026-08-18.md (D3) + the four child rows",
            "linked_issues": [104],
        },
        {
            "id": "CLM-V5-ROUTING",
            "statement": "ROUTING.md is generated solely from metadata.hands-to, byte-verified in CI, and the hand-authored-routing-table ban is mechanically enforced.",
            "authority": "v5 design spec (Routing is generated, never authored) + AMENDMENTS 2026-08-07/2026-08-18",
            "subject": "plugins/epistemic-skills/ROUTING.md + all markdown surfaces",
            "oracle": "sync_skill_surfaces.py --check byte-compares the rendering; check_no_phantom_skills.py rule 3 rejects routing-column tables outside ROUTING.md; both self-tests carry planted RED controls.",
            "falsifier": "A hands-to edit does not surface as ROUTING_DRIFT, or a planted hand-authored routing table passes rule 3.",
            "environment": "CI ubuntu-24.04 + clean-room replication",
            "independence": "byte-equality re-rendering, not the generator's own green",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "Routing enumeration tax stays deleted",
            "owner": "agent",
            "closure_path": "Checks green this candidate; first live catch (write-goal two-home drift) fixed same day",
            "linked_issues": [104],
        },
        {
            "id": "CLM-V5-LEDGERS",
            "statement": "Every packaged skill carries the intrinsic evidence-emission step (skill-run@1) with a schema-validated tracked exemplar; live ledgers are runtime-local by amended design.",
            "authority": "v5 design spec (Evidence emission, intrinsic) + AMENDMENT 2026-08-18 (storage class)",
            "subject": "all 15 SKILL.md files + contracts/skill-run-ledger.schema.json + runs/ledger.example.jsonl",
            "oracle": "check_skill_run_ledger.py green (rules derived from the schema at run time; gauntlet's ledger@2 exception explicit) with planted RED self-tests.",
            "falsifier": "A skill lacks the emission step or a valid exemplar and the check stays green.",
            "environment": "CI ubuntu-24.04 + clean-room replication",
            "independence": "checker derives rules from the schema; no second copy of the contract",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "Run evidence exists by construction of each skill's own procedure",
            "owner": "agent",
            "closure_path": "Checks green this candidate",
            "linked_issues": [104],
        },
        {
            "id": "CLM-V5-SENTINELS",
            "statement": "Sentinel corpora exist for every skill with event_kind bound into each fixture and a scorer that fails closed in both directions.",
            "authority": "v5 design spec (Verification: RED before green)",
            "subject": "contracts/epistemic-events/sentinels/*.json + score_sentinels.py",
            "oracle": "score_sentinels.py green; --self-test exercises the shared event_kind_violation rule in REJECT and ACCEPT directions.",
            "falsifier": "A sentinel with a wrong event kind grades clean, or the self-test passes with the rule inverted.",
            "environment": "CI ubuntu-24.04 + clean-room replication",
            "independence": "scorer distinct from fixture authors; shared rule exercised from both sides",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "Sentinel oracles cannot pass vacuously",
            "owner": "agent",
            "closure_path": "Checks green this candidate",
            "linked_issues": [104],
        },
        {
            "id": "CLM-V5-MEMBERSHIP",
            "statement": "Skill membership has one source of truth: per-skill frontmatter event metadata derives skill-event-map.json, its schema, the verifier inventory, and every count surface; membership drift fails closed.",
            "authority": "v5 design spec (structural membership) — es#104 s4 Option A",
            "subject": "15 SKILL.md frontmatters + contracts/epistemic-events/skill-event-map.json + derived surfaces",
            "oracle": "sync_skill_surfaces.py --check green; --self-test plants MAP/SCHEMA/ROUTING/COUNT drift, EVENT_METADATA_MISSING, HANDS_TO_UNKNOWN, and an unregistered-new-skill case — all must fail closed.",
            "falsifier": "A skill added without regeneration passes --check, or any planted battery case grades clean.",
            "environment": "CI ubuntu-24.04 + clean-room replication",
            "independence": "byte-equality re-rendering against the frontmatter source",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "A second hand-maintained membership home cannot drift",
            "owner": "agent",
            "closure_path": "Checks green this candidate",
            "linked_issues": [104],
        },
        {
            "id": "CLM-RELEASE-AUTH",
            "statement": "Publication requires explicit owner authorization recorded before tag creation; the authorization regime is decided (disarm-as-authorization, operator decision D6).",
            "authority": "PR #156 (merged, D1-ratified); RELEASING.md step 7; operator decision D6 (echo-certified)",
            "subject": "refs/tags/v* creation",
            "oracle": "Committed release notes name verdict, exact SHA, owner; protect-version-tags keeps zero bypass actors; the documented disarm -> tag -> re-arm-with-seeded-probe procedure IS the authorization act (D6).",
            "falsifier": "Tag created without the authorization procedure, or the ruleset carries a bypass actor, or is left disarmed outside an authorized window.",
            "environment": "GitHub ruleset + release notes",
            "independence": "operator authorization; ruleset state live-verified",
            "evidence_tier": "R0",
            "status": "PROVED",
            "release_consequence": "PROMOTION remains a separate operator act; the mechanism question is closed",
            "owner": "operator",
            "closure_path": "D6 recorded; execution occurs only inside a PROMOTION_RUN",
            "linked_prs": [156, 190],
            "linked_issues": [186],
        },
        {
            "id": "CLM-BEHAVIORAL-EPOCHS",
            "statement": "Every BLOCKED/absent behavioral battery has dated live-epoch evidence, including a valid four-arm superiority run.",
            "authority": "es#77; es#39; EVIDENCE-POLICY.md",
            "subject": "evals/**/results live epochs",
            "oracle": "Dated epoch directories with independent scores, not fixture-only green.",
            "falsifier": "A BLOCKED battery is cited as PASS, or a four-arm run is absent while claimed complete.",
            "environment": "gate:live-environment",
            "independence": "live harness distinct from fixture scorer self-tests",
            "evidence_tier": "R3",
            "status": "LIMITED",
            "release_consequence": "Cannot claim behavioral completeness",
            "owner": "agent",
            "closure_path": "Later evidence-process packet in a live environment",
            "linked_issues": [77, 39],
        },
        {
            "id": "CLM-HARNESS-LIVE",
            "statement": "Native harness bindings are verified from captured payloads or explicit verification tiers, not docs prose alone.",
            "authority": "RELEASING.md harness-evidence gate; es#136/#129/#142",
            "subject": "Claude/Cursor/Codex/Gemini/Antigravity hook adapters",
            "oracle": "Captured payloads or recorded verification tier per harness in release notes.",
            "falsifier": "A harness claimed verified while only docs-shaped fixtures exist.",
            "environment": "native harness hosts",
            "independence": "payloads from the running harness, not reconstructed",
            "evidence_tier": "R3",
            "status": "LIMITED",
            "release_consequence": "Harness claims must degrade to named tiers",
            "owner": "agent",
            "closure_path": "Live-fire packet; until then disclose LIMIT",
            "linked_issues": [136, 129, 142],
        },
        {
            "id": "CLM-INDEPENDENT-GAUNTLET",
            "statement": "An isolated independent Gauntlet computes GO on the exact candidate with no unresolved P1/P2 release blockers.",
            "authority": "#191 terminal contract; RELEASING.md independent judgment gate",
            "subject": f"commit {sha}",
            "oracle": "Recorded GO by a fresh seat that did not produce the candidate, BOUND to a run id, an on-disk verdict artifact, and this exact SHA (independent_gauntlet_ref). A bare enum flip in this packet is not a verdict (R1).",
            "falsifier": "The implementer records GO; GO is recorded against a different SHA; or the enum says GO with no matching verdict artifact on disk.",
            "environment": "isolated independent panel",
            "independence": "No actor certifies its own acceptance",
            "evidence_tier": "R0",
            "status": "UNPROVED",
            "release_consequence": "Blocks V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE",
            "owner": "independent-panel",
            "closure_path": "Operator-dispatched independent Gauntlet on this packet's SHA",
            "linked_issues": [191, 40],
        },
        {
            # R6: the predecessor row (CLM-TRACKER-RECONCILED) claimed
            # evidence-backed reconciliation and was PROVED-but-false on
            # #191's own strong reading. This row claims only what the
            # artifact establishes: a complete DISPOSITION CENSUS. Whether
            # each disposition satisfies #191's reconcile-not-merely-cite
            # bar is carried per-item by the matrix rows and the decision
            # record, never certified wholesale by this row.
            "id": "CLM-DISPOSITION-CENSUS",
            "statement": "Every currently open issue and PR carries an explicit, human-read disposition in the reconciliation artifact (a census claim; per-item substance lives in the individual rows).",
            "authority": "#191 required reconciliation (census limb); gauntlet ruling R6",
            "subject": "open GitHub issues and PRs at generation time",
            "oracle": "issue-pr-reconciliation.json item count equals the live open tracker count; each item has phase+disposition+owner; generation fails closed on any item without an explicit map entry.",
            "falsifier": "An open issue/PR is absent from the reconciliation, present with no disposition, or generation succeeded despite an item missing from the disposition maps.",
            "environment": "GitHub Issues/PR API + committed JSON",
            "independence": "generator reads the live tracker, not a remembered list",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P2 if the freeze drifts from the live tracker",
            "owner": "agent",
            "closure_path": "Regenerate this packet if the open set changes",
            "linked_issues": [191],
            "evidence_paths": [
                "docs/v6/ES6-V6-CANDIDATE/issue-pr-reconciliation.json"
            ],
        },
        {
            "id": "CLM-REQUIRED-JOB",
            "statement": "Across all six workflows, merge-gating jobs are named, skip on draft PRs, and DISPATCH when a draft is marked ready; dispatch-only diagnostics are documented as non-gating.",
            "authority": "RELEASING.md required-job semantics; PR #190 (D1-ratified); gauntlet ruling R8",
            "subject": "all six .github/workflows/*.yml: epistemic-flexibility stdlib-checks; mission-custody contract (+dispatch-only contract-macos); commission-watch contract; openai-bundles build; release-security full-history-secret-scan; dco",
            "oracle": "Every gating workflow declares pull_request types [opened, synchronize, reopened, ready_for_review]; the R8 ready-mark drill dispatched all five gating workflows at an unchanged head; contract-macos remains workflow_dispatch only.",
            "falsifier": "A ready-marked draft fails to dispatch any gating workflow at the same head, a dispatch-only job is treated as required, or a required job runs on a draft PR.",
            "environment": "repository workflows + RELEASING.md + live drill",
            "independence": "drill evidence from GitHub's own run records, not workflow prose",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P2 if required-job semantics drift",
            "owner": "agent",
            "closure_path": "docs/v6/evidence/r8-ready-mark-drill-2026-08-18.md; re-audit if workflow if:/types change",
            "linked_issues": [186, 191],
            "linked_prs": [190],
        },
        {
            "id": "CLM-WINDOWS-FS",
            "statement": "Custody path-scope and hook behavior are verified on native Windows.",
            "authority": "#191 terminal contract (Windows evidence)",
            "subject": "mission-custody hook/gate path comparison on NT",
            "oracle": "Native Windows run of test_custody_hook.py and related suites with recorded SHA.",
            "falsifier": "A POSIX-only green is cited as Windows coverage.",
            "environment": "native Windows (not this Linux BUILD host)",
            "independence": "OS distinct from the Linux CI runner",
            "evidence_tier": "R3",
            "status": "LIMITED",
            "release_consequence": "Windows claims remain disclosed-limited until a native run is retained",
            "owner": "agent",
            "closure_path": "Later evidence-process packet on a Windows host",
            "linked_issues": [162, 191],
        },
        {
            "id": "CLM-MC-137",
            "statement": "The three P1 false-allow bypasses and four P2 refusal gaps from es#137 are closed in THIS CANDIDATE TREE (main's exposure is disclosed separately as KL-MAIN-137).",
            "authority": "es#137",
            "subject": "mission-custody hook/gate/validator/CLI/API on this candidate",
            "oracle": "Named acceptance tests green in the full mission-custody-contract suite on this tree.",
            "falsifier": "Any of the seven named tests fail on this candidate tree.",
            "environment": "local Linux custody suite; CI ubuntu-24.04 when not draft",
            "independence": "suite is not the production hook process",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P1 false-allows remain on main until an operator merge — carried as KL-MAIN-137, not hidden inside this row's status",
            "owner": "agent",
            "closure_path": "Suite green this candidate; operator merge of this candidate or of #193 retires the main exposure",
            "linked_issues": [137],
            "linked_prs": [193],
        },
        {
            "id": "CLM-SECRET-SCAN",
            "statement": "The full git history of the candidate contains no credential-shaped secrets (release-security full-history-secret-scan).",
            "authority": "RELEASING.md gate 6; .github/workflows/release-security.yml",
            "subject": f"commit {sha} full history",
            "oracle": "release-security full-history-secret-scan job green on the candidate head (dispatches on ready PRs and pushes; verified dispatching by the R8 ready-mark drill), WITH the job's planted controls green: a seeded private key must be detected, the digest allowlist must reject a neighbouring credential field, and the record-path narrowness control must show the entropy exemption firing outside ^docs/gauntlet-runs/ and on a look-alike path while a branded credential inside it still fires.",
            "falsifier": "A seeded credential in a historical commit passes the scan; or the job never executes on the candidate; or the ^docs/gauntlet-runs/ entropy exemption (added because verifier prose there quotes run ids beside the word API) suppresses a finding outside that anchored path, or suppresses any rule other than generic-api-key inside it. The exemption is scoped to one rule and one anchored path, and CI proves that scoping on every run rather than asserting it.",
            "environment": "ubuntu-24.04 CI",
            "independence": "scanner distinct from content authors",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 — required security-class surface; unclaimed/unrun was gauntlet ruling R2",
            "owner": "agent",
            "closure_path": "Requalification run URLs on the exact candidate recorded in evidence at freeze",
            "linked_issues": [191],
        },
        {
            "id": "CLM-COMPATIBILITY",
            "statement": "Every packaging surface (Claude/Cursor/Kimi/Codex/Gemini manifests, OpenAI bundles, count words, skill inventories) is generated-or-verified in sync with the packaged tree.",
            "authority": "es#191 terminal contract (compatibility claims); gauntlet ruling R14 (compatibility class was unclaimed)",
            "subject": f"commit {sha} manifests + bundles + inventory surfaces",
            "oracle": "check_json_artifacts.py, sync_skill_surfaces.py --check, check_skill_inventory.py, and build_openai_bundles.py --check all exit 0.",
            "falsifier": "A manifest names a skill count or member that the packaged tree does not carry, or a bundle build diverges from the packaged skills.",
            "environment": "repository static analysis + CI",
            "independence": "generators verified by byte-equality re-rendering, not by their own output",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P2 — installers receive stale surfaces on drift",
            "owner": "agent",
            "closure_path": "Checks green this candidate; regenerate on any membership change",
            "linked_issues": [191],
        },
        {
            "id": "CLM-MC-GUARD-LEXICAL",
            "statement": "Custody guard path matching is lexical and can diverge from filesystem resolution through symlinked parents; the divergence is disclosed, pinned by a characterization test, and unchanged this epoch.",
            "authority": "Gauntlet ruling R15 (run es-v6-candidate-freeze-2026-08-18); PR #128 safe-direction analysis",
            "subject": "custody_gate _guard_norm_path matching semantics",
            "oracle": "test_guard_match_is_lexical_symlinked_parent_diverges green (RED-proven against a scratch resolution-aware patch); SECURITY.md section present.",
            "falsifier": "The probe's divergence case stops reproducing without a disclosed semantics change, or the pin test is deleted/weakened.",
            "environment": "POSIX symlink-capable checkout; NT skips loudly",
            "independence": "characterization pin distinct from the production gate code",
            "evidence_tier": "R1",
            "status": "LIMITED",
            "release_consequence": "Guard globs bound spellings, not filesystem effects — disclosed in SECURITY.md",
            "owner": "agent",
            "closure_path": "docs/v6/evidence/r15-guard-lexical-probe-2026-08-18.md; resolution-aware matching is a future contract-epoch decision",
            "linked_issues": [137, 147],
        },
        {
            # R3-NF4: this row previously asserted the estate fork OPEN while
            # the same tree's ledger entry 17 + the spec amendment recorded it
            # resolved — the exact prose-vs-record class S2 exists to kill.
            # Re-derived against the recorded ruling.
            "id": "CLM-DESCRIPTION-BUDGET",
            "statement": "The packaged description byte ceiling is enforced (check_description_budget.py); the ESTATE net-negative release gate is RETIRED by recorded operator ruling (hybrid Path 2): the package-local ceiling stays a hard CI gate, every release's notes report the description-byte delta vs the prior release (RELEASING.md), and check_loaded_descriptions.py --require-capture remains available for on-demand estate measurement.",
            "authority": "v5 design AMENDMENT 2026-08-07 (D8 dual scope) as resolved by the owner AMENDMENT 2026-08-18 (hybrid form) under the operator's recorded ruling, ledger id v6-description-budget-hybrid-path2-20260818-17",
            "subject": "packaged SKILL.md description frontmatter bytes; estate release-gate status",
            "oracle": "check_description_budget.py green (package ceiling); the 'AMENDMENT 2026-08-18 — the D8 estate fork is resolved' section present in docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md; the RELEASING.md description-byte-delta row present; .ledger/entries.jsonl carries entry v6-description-budget-hybrid-path2-20260818-17.",
            "falsifier": "Package bytes exceed the ceiling; or any of the amendment section, the RELEASING.md delta row, or the ledger ruling entry is absent from this tree; or a release ships without the delta report the amendment promises.",
            "environment": "CI (package ceiling); repository record (amendment + RELEASING.md + ledger)",
            "independence": "budget checker distinct from description authors; the ruling is the operator's own recorded act",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "The estate acceptance line no longer gates v6.0; the package ceiling still fails CI closed on any overrun; each release must carry the delta report per RELEASING.md",
            "owner": "operator",
            "closure_path": "Completed act: operator ruling recorded (ledger 17) and the Path-2 amendment landed in-tree; per-release delta reporting is a standing RELEASING.md procedure",
            "linked_issues": [104, 191],
        },
        {
            "id": "CLM-MERGE-190",
            "statement": "The BUILD-window merge of PR #190 (required-job semantics) to main is an operator-ratified act.",
            "authority": "Operator decision D1, echo-certified (docs/v6/operator-decision-record-2026-08-18.md; ratified object at commit d7c4178)",
            "subject": "PR #190 merge to main, 2026-08-18",
            "oracle": "The decision record is present in the tree with its certification section; D1 names #190 explicitly.",
            "falsifier": "The record is absent, its certification fails re-verification, or the operator reverses the ratification.",
            "environment": "repository record + live tracker",
            "independence": "ratification is the operator's own echo-certified act, not agent-authored consent",
            "evidence_tier": "R0",
            "status": "PROVED",
            "release_consequence": "P1 — unresolved merge consent was gauntlet ruling R3's cap on every acceptance path",
            "owner": "operator",
            "closure_path": "Discharged by D1 upon echo certification; packet-disclosure limb is this row",
            "linked_prs": [190],
        },
        {
            "id": "CLM-MERGE-156",
            "statement": "The BUILD-window merge of PR #156 (publication-authorization step) to main is an operator-ratified act.",
            "authority": "Operator decision D1, echo-certified (docs/v6/operator-decision-record-2026-08-18.md; ratified object at commit d7c4178)",
            "subject": "PR #156 merge to main, 2026-08-18",
            "oracle": "The decision record is present in the tree with its certification section; D1 names #156 explicitly.",
            "falsifier": "The record is absent, its certification fails re-verification, or the operator reverses the ratification.",
            "environment": "repository record + live tracker",
            "independence": "ratification is the operator's own echo-certified act, not agent-authored consent",
            "evidence_tier": "R0",
            "status": "PROVED",
            "release_consequence": "P1 — unresolved merge consent was gauntlet ruling R3's cap on every acceptance path",
            "owner": "operator",
            "closure_path": "Discharged by D1 upon echo certification; packet-disclosure limb is this row",
            "linked_prs": [156],
        },
        {
            "id": "CLM-MERGE-192",
            "statement": "The BUILD-window merge of PR #192 (ES6-ZI-001 baseline; this candidate lineage's base) to main is an operator-ratified act.",
            "authority": "Operator decision D1, echo-certified (docs/v6/operator-decision-record-2026-08-18.md; ratified object at commit d7c4178)",
            "subject": "PR #192 merge to main, 2026-08-18",
            "oracle": "The decision record is present in the tree with its certification section; D1 names #192 explicitly.",
            "falsifier": "The record is absent, its certification fails re-verification, or the operator reverses the ratification.",
            "environment": "repository record + live tracker",
            "independence": "ratification is the operator's own echo-certified act, not agent-authored consent",
            "evidence_tier": "R0",
            "status": "PROVED",
            "release_consequence": "P1 — unresolved merge consent was gauntlet ruling R3's cap on every acceptance path; #192 appeared in no packet artifact at the NO-GO subject",
            "owner": "operator",
            "closure_path": "Discharged by D1 upon echo certification; packet-disclosure limb is this row",
            "linked_prs": [192],
        },
    ]
    for claim in claims:
        claim["consequence_severity"] = CLAIM_SEVERITY[claim["id"]]
    return claims


def tracker_claim(kind: str, number: int, title: str, meta: dict, labels: list[str]) -> dict:
    label_set = set(labels)
    status = "UNPROVED"
    if meta["disposition"] == "hold-operator" or meta["phase"] == "frontier-decision":
        status = "BLOCKED"
    elif meta["disposition"].startswith("decided-"):
        # The operator decision is recorded (D-series, echo-certified);
        # remaining execution is carried by the note and the class rows.
        status = "PARTIAL"
    elif meta["disposition"] in {"park", "do-not-merge", "harvest-supersede",
                                 "supersede-and-close"}:
        status = "LIMITED"
    elif LIVE_LABELS & label_set or meta["disposition"] == "close-when-evidence":
        status = "LIMITED"
    elif meta["disposition"] in {"in-candidate-draft", "operator-merge"}:
        status = "PARTIAL"
    elif OPERATOR_LABELS & label_set:
        status = "BLOCKED"
    prefix = "ISSUE" if kind == "issue" else "PR"
    return {
        "id": f"CLM-{prefix}-{number}",
        "statement": title,
        "authority": f"es#{number}" if kind == "issue" else f"PR #{number}",
        "subject": f"{kind} {number}",
        "oracle": meta["evidence_note"],
        "falsifier": "Disposition is stale relative to the live tracker or the cited evidence does not exist.",
        "environment": "GitHub tracker + candidate tree",
        "independence": "disposition recorded separately from implementation",
        "evidence_tier": _tier_from_labels(labels),
        "status": status,
        "release_consequence": meta["evidence_note"],
        "consequence_severity": "P3",
        "owner": meta["owner"],
        "closure_path": meta["disposition"],
        "linked_issues": [number] if kind == "issue" else [],
        "linked_prs": [number] if kind == "pr" else [],
    }


def require_dispositions(issues: list[dict], prs: list[dict]) -> None:
    """R12: an open tracker item with no explicit disposition fails generation."""
    unknown_issues = sorted(
        i["number"] for i in issues if i["number"] not in ISSUE_DISPOSITIONS
    )
    unknown_prs = sorted(p["number"] for p in prs if p["number"] not in PR_DISPOSITIONS)
    if unknown_issues or unknown_prs:
        raise SystemExit(
            "UNDISPOSITIONED_TRACKER_ITEMS: every open item needs an explicit "
            f"entry (no silent default). issues={unknown_issues} prs={unknown_prs} "
            "— add human-read dispositions to ISSUE_DISPOSITIONS/PR_DISPOSITIONS."
        )


def build_reconciliation(sha: str, ts: str, issues: list[dict], prs: list[dict]) -> dict:
    items: list[dict] = []
    for issue in sorted(issues, key=lambda x: x["number"]):
        meta = ISSUE_DISPOSITIONS[issue["number"]]
        items.append(
            {
                "kind": "issue",
                "number": issue["number"],
                "title": issue["title"],
                "phase": meta["phase"],
                "disposition": meta["disposition"],
                "owner": meta["owner"],
                "blocked_by": meta.get("blocked_by", []),
                "labels": [l["name"] for l in issue.get("labels", [])],
                "evidence_note": meta["evidence_note"],
                "url": issue["url"],
            }
        )
    for pr in sorted(prs, key=lambda x: x["number"]):
        meta = PR_DISPOSITIONS[pr["number"]]
        note = meta["evidence_note"]
        if pr.get("isDraft"):
            note = f"{note} (draft PR)."
        items.append(
            {
                "kind": "pr",
                "number": pr["number"],
                "title": pr["title"],
                "phase": meta["phase"],
                "disposition": meta["disposition"],
                "owner": meta["owner"],
                "blocked_by": meta.get("blocked_by", []),
                "labels": [l["name"] for l in pr.get("labels", [])],
                "evidence_note": note,
                "url": pr["url"],
            }
        )
    return {
        "schema": "issue-pr-reconciliation@1",
        "program": PROGRAM,
        "exact_start_sha": sha,
        "generated_at": ts,
        "items": items,
    }


def _tracked_files(pathspec: str) -> list[str]:
    """Git-tracked files matching pathspec — the ONE tree model (S1).

    The rc2 freeze walked the FILESYSTEM (rglob) while its clean-tree guard
    used .gitignore-aware `git status --porcelain`: two tree models that
    disagreed exactly on ignored host state, sealing 17 volatile
    `__pycache__/*.pyc` digests and making the validator fail on every clean
    checkout (kimi ruling S1, run es-v6-rc2-gauntlet-kimi-2026-08-18). Git's
    index is now the single authority for what the inventory contains, the
    same authority the dirt check consults.
    """
    out = subprocess.check_output(
        ["git", "ls-files", "-z", "--", pathspec], cwd=REPO_ROOT
    )
    return sorted(p for p in out.decode("utf-8").split("\0") if p)


def build_source_inventory(sha: str, ts: str) -> dict:
    workflows = _tracked_files(".github/workflows/*.yml")
    contracts = _tracked_files("plugins/epistemic-skills/contracts")
    ci_scripts = _tracked_files(".github/scripts/*.py")
    # R5b/d: bind the inventory to CONTENT, not just a name. Per-file sha256
    # digests plus the candidate's git tree hash make any post-freeze edit to
    # an inventoried file detectable (the predecessor packet's artifacts were
    # mutated after generation and nothing could tell).
    digests = {
        rel: hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()
        for rel in [*workflows, *contracts, *ci_scripts]
    }
    tree_hash = subprocess.check_output(
        ["git", "rev-parse", f"{sha}^{{tree}}"], cwd=REPO_ROOT, text=True
    ).strip()
    return {
        "schema": "v6-source-inventory@2",
        "exact_start_sha": sha,
        "candidate_tree_hash": tree_hash,
        "generated_at": ts,
        "workflows": workflows,
        "contracts": contracts,
        "ci_scripts": ci_scripts,
        "file_digests": digests,
    }


REQUAL_PATH = OUT_DIR / "evidence" / "requalification.json"


def apply_requalification(claims: list[dict], sha: str, path: Path = REQUAL_PATH) -> list[str]:
    """Evidence-driven PARTIAL->PROVED flips from recorded requalification runs.

    A claim status is never hand-flipped: the only path from PARTIAL to
    PROVED at freeze is a committed requalification capture naming THIS
    candidate SHA with successful run records (GitHub run URLs). Anything
    else refuses — unknown claim ids, non-PARTIAL flips, non-green runs,
    or a capture for a different SHA (the restamp class again).
    """
    if not path.is_file():
        return []
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("candidate_sha") != sha:
        raise SystemExit(
            "REQUAL_SHA_MISMATCH: requalification evidence names "
            f"{str(doc.get('candidate_sha', '?'))[:12]}, packet names {sha[:12]} "
            "— regenerate the capture at the candidate."
        )
    notes: list[str] = []
    by_id = {c["id"]: c for c in claims}
    for cid, entry in doc.get("claims", {}).items():
        claim = by_id.get(cid)
        if claim is None:
            raise SystemExit(f"REQUAL_UNKNOWN_CLAIM: {cid}")
        if claim["status"] != "PARTIAL":
            raise SystemExit(
                f"REQUAL_BAD_FLIP: {cid} is {claim['status']}; only PARTIAL "
                "claims may be requalified by run evidence"
            )
        if entry.get("conclusion") != "success" or not entry.get("runs"):
            raise SystemExit(f"REQUAL_NOT_GREEN: {cid} capture is not a successful run set")
        claim["status"] = "PROVED"
        claim.setdefault("evidence_paths", []).append(
            "docs/v6/ES6-V6-CANDIDATE/evidence/requalification.json"
        )
        notes.append(f"requalified {cid} via {len(entry['runs'])} recorded run(s)")
    return notes


def build_claim_matrix(sha: str, ts: str, issues: list[dict], prs: list[dict]) -> dict:
    claims = class_claims(sha)
    for note in apply_requalification(claims, sha):
        print(note)
    seen = {c["id"] for c in claims}
    for issue in issues:
        meta = ISSUE_DISPOSITIONS[issue["number"]]
        labels = [l["name"] for l in issue.get("labels", [])]
        claim = tracker_claim("issue", issue["number"], issue["title"], meta, labels)
        if claim["id"] not in seen:
            claims.append(claim)
            seen.add(claim["id"])
    for pr in prs:
        meta = PR_DISPOSITIONS[pr["number"]]
        labels = [l["name"] for l in pr.get("labels", [])]
        claim = tracker_claim("pr", pr["number"], pr["title"], meta, labels)
        if claim["id"] not in seen:
            claims.append(claim)
            seen.add(claim["id"])
    return {
        "schema": "claim-to-proof-matrix@1",
        "program": PROGRAM,
        "exact_start_sha": sha,
        "generated_at": ts,
        "claims": claims,
    }


def build_receipt(sha: str, ts: str) -> dict:
    return {
        "schema": "exact-start-receipt@1",
        "program": PROGRAM,
        "issue": 191,
        "exact_start_sha": sha,
        "recorded_at": ts,
        "parent_program": "ZMS-Labs/epistemic-skills#191",
        "authorized_packets": [
            "ES6-V6-CANDIDATE-MATRIX",
            "ES6-V6-CANDIDATE-REQUAL",
            "ES6-V6-CANDIDATE-PACKET",
        ],
        "forbidden_this_run": [
            "merge to main",
            "tag",
            "close issues",
            "close PRs",
            "settings/ruleset changes",
            "self-certified Gauntlet GO",
            "promotion",
        ],
    }


def _validator_module():
    """The v6-assurance contract owns the blocking derivation (one home)."""
    import importlib.util

    path = REPO_ROOT / "plugins/epistemic-skills/contracts/v6-assurance/validate_v6_assurance.py"
    spec = importlib.util.spec_from_file_location("validate_v6_assurance", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def blocking_from_matrix(matrix: dict) -> list[str]:
    """R12: blocking_claims is DERIVED from the matrix, never a hand list.

    The rule lives in validate_v6_assurance.derive_blocking — the validator
    recomputes it on every run, so a hand-edited blocking list fails CI. The
    predecessor's hand-maintained 9-id whitelist is exactly what let
    arbitrary inclusion/omission drift in (gauntlet ruling R12).
    """
    return _validator_module().derive_blocking(matrix["claims"])


def operator_limited_limits(matrix: dict) -> list[dict]:
    """S2 (operator ruling 2026-08-18, machine channel DERIVED): every
    operator-CLASS LIMITED P1/P2 claim gets a known_limits entry naming it
    via the `claim` field — derived here so it cannot be dropped by hand.
    Non-PROVED non-LIMITED operator-class P1/P2 claims already block via
    derive_blocking; PROVED operator claims are completed acts (row-only);
    P3 census rows are channeled by the reconciliation artifact. The full
    law lives in requirement-register.json (operator_channel_law) and
    validate_operator_channel enforces it. The owner test is the validator's
    is_operator_class — the SAME predicate derive_blocking and the enforcer
    use (R3-NF6: a substring test here vs the set test there let a
    joint-owned LIMITED P1/P2 claim silently drop from every channel)."""
    is_operator_class = _validator_module().is_operator_class
    derived = []
    for claim in matrix["claims"]:
        if (
            is_operator_class(claim["owner"])
            and claim["status"] == "LIMITED"
            and claim.get("consequence_severity") in ("P1", "P2")
        ):
            derived.append({
                "id": f"KL-OPERATOR-{claim['id'][4:]}",
                "kind": "operator-hold",
                "claim": claim["id"],
                "statement": (
                    f"Operator-class LIMITED claim {claim['id']} "
                    f"(owner: {claim['owner']}): {claim['statement']}"
                ),
                "release_consequence": claim["release_consequence"],
                "owner": claim["owner"],
            })
    return derived


def build_promotion_packet(sha: str, ts: str, matrix: dict) -> dict:
    return {
        "schema": "v6-promotion-packet@2",
        "program": PROGRAM,
        "issue": 191,
        "candidate_sha": sha,
        # A new freeze is born ACTIVE: its digests bind the tree under review.
        # It becomes LANDED once its freeze PR merges and work continues past
        # it, after which the attestation is verified against candidate_sha's
        # own commit instead of constraining the default branch.
        "freeze_state": "ACTIVE",
        "generated_at": ts,
        "readiness": "NOT_READY",
        "self_certification": "refused",
        "independent_gauntlet": "NOT_RUN",
        # R1: the verdict is a bound artifact, never a bare enum. Populated
        # only by the acceptance flow after a real run exists on disk.
        "independent_gauntlet_ref": None,
        # R10: the rollback premise names dated, immutable facts plus a live
        # re-check obligation — never a decaying "main is currently X" claim
        # (the rc3 packet shipped this field asserting main RED hours after
        # #195 had landed green; R3-NF3).
        "rollback": (
            "Do not merge this branch to main outside a PROMOTION_RUN. "
            "Abandoning this branch reverts to origin/main, which merged "
            "this lineage's Public-content repair (PR #195, squash 03b7724, "
            "2026-08-18, operator-ratified D11/RATIFY) and ran its required "
            "stdlib-checks green at that head. Main's live state is "
            "re-checked at operator acceptance per the acceptance "
            "procedure, never assumed from this dated record. One qualified "
            "exposure remains: the es#137 custody fixes exist only in this "
            "candidate tree (KL-MAIN-137). An independent GO and a separate "
            "PROMOTION_RUN remain required either way."
        ),
        "requested_irreversible_acts": [],
        "blocking_claims": blocking_from_matrix(matrix),
        "known_limits": [
            {
                "id": "KL-SELF-GO",
                "kind": "independence",
                "statement": "The implementer of this packet cannot record Gauntlet GO on it.",
                "release_consequence": "V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE is unreachable until an independent panel runs (fresh seat: the prior adjudicating seat took the repair role under D2).",
                "owner": "independent-panel",
            },
            {
                "id": "KL-LIVE-ENV",
                "kind": "live-environment",
                "statement": "Behavioral epochs (#77/#39) and native harness live-fire (#136/#129/#142) were not run.",
                "release_consequence": "Those claims are LIMITED, not PROVED.",
                "owner": "agent",
            },
            {
                "id": "KL-MACOS-162",
                "kind": "platform",
                "statement": (
                    "es#162 case-insensitivity is disclosed and now MEASURED "
                    "beyond the ASCII probe: on macos-14 APFS the first full "
                    "lifecycle-suite dispatch showed straße.txt/strasse.txt "
                    "— contract-distinct artifacts — are one physical file "
                    "under the filesystem's Unicode case folding; a decoy "
                    "write clobbered the real artifact (tests "
                    "distinct-real-file-untouched, "
                    "distinct-both-files-tracked-separately; run "
                    "32189655677). contract-macos stays dispatch-only and "
                    "non-gating."
                ),
                "release_consequence": "Not a merge-gating required job; custody distinctness claims exclude case-insensitive APFS until es#162 lands.",
                "owner": "agent",
            },
            {
                # KL-DRAFT-CI rewrite (gauntlet rulings R8/R9): the full
                # shape of what draft state hides, with current numbers.
                "id": "KL-DRAFT-CI",
                "kind": "integrity",
                "statement": (
                    "While the freeze PR is a draft, ALL FIVE gating "
                    "workflows skip their jobs (stdlib-checks, mission-"
                    "custody contract, commission-watch contract, "
                    "openai-bundles build, full-history-secret-scan) plus "
                    "DCO. Marking the PR ready dispatches every one of them "
                    "at the unchanged head (ready_for_review trigger types; "
                    "proven by the 2026-08-18 ready-mark drill). Until "
                    "then the BUILD oracle is the local clean-room, which "
                    "replicates the python steps of ONE workflow "
                    "(epistemic-flexibility) with a completeness assertion "
                    "and every non-replicated step NAMED with its reason — "
                    "exact per-step counts live in "
                    "evidence/clean-baseline.json, never in this prose "
                    "(counts drift per commit; the rc2 packet's hand-"
                    "written fraction did, kimi ruling S6). The other five "
                    "workflows are NOT covered by the clean-room. A "
                    "fail-fast CI failure also masks later steps: the "
                    "oracle-audit step's missing-PyYAML defect was "
                    "invisible on main behind the public-content failure "
                    "until 2026-08-18."
                ),
                "release_consequence": (
                    "Local clean-room green is not GitHub required-job "
                    "green. Requalification requires the ready-mark (or "
                    "workflow_dispatch, D4b) runs on the exact candidate."
                ),
                "owner": "agent",
            },
            {
                "id": "KL-MAIN-137",
                "kind": "integrity",
                "statement": "es#137 P1 false-allows are present on origin/main; closed only in this candidate tree.",
                "release_consequence": "Merging this candidate is a PROMOTION act, not performed here.",
                "owner": "operator",
            },
            # KL-MAIN-RED retired (R3-NF3): its own self-retiring clause fired
            # when PR #195 merged 2026-08-18 as 03b7724 and main's push runs
            # went green at that head. The rc3 packet shipped the limit as if
            # still live — prose asserting decayed state. Main's live state
            # is re-checked at operator acceptance; the residual main
            # exposure that remains true is KL-MAIN-137 above.
            {
                "id": "KL-SEAL-MAIN-COUPLING",
                "kind": "integrity",
                "statement": (
                    "The digest seal binds inventoried sources as they stood "
                    "at C. CI runs the freeze PR against its MERGE ref, so a "
                    "change on main to ANY inventoried file makes that merge "
                    "tree differ from C and the validator fails R5 DIGEST "
                    "MISMATCH on the freeze PR — even though the candidate "
                    "branch itself is untouched. Measured, not theorised: the "
                    "rc4 candidate's own R4-NF1 repair landed on main "
                    "(check_dco.py, dco.yml, release-security.yml) and forced "
                    "the rc5 re-cut that absorbed it."
                ),
                "release_consequence": (
                    "While a freeze is open, main must not change inventoried "
                    "files, or the freeze must be re-cut to absorb them. The "
                    "practical rule: land main-side policy repairs BEFORE "
                    "cutting a candidate, and keep the window between freeze "
                    "and ready-mark short."
                ),
                "owner": "operator",
            },
            {
                "id": "KL-SCAN-EXEMPTION",
                "kind": "integrity",
                "statement": (
                    "The full-history secret scan carries exactly one path "
                    "exemption, `^docs/gauntlet-runs/.*`, because verifier "
                    "prose in those immutable records quotes credential-shaped "
                    "strings it is reporting on. Two properties are PROVEN on "
                    "every run by a CI narrowness control: the pattern is "
                    "anchored (an earlier unanchored form also suppressed "
                    "`notdocs/gauntlet-runs/` and `sub/docs/gauntlet-runs/`), "
                    "and it applies to no look-alike path. "
                    "What the control does NOT prove, and what this limit "
                    "exists to say: the exemption is OPEN-ENDED OVER FUTURE "
                    "FILES and is NOT digest-bound. It suppresses scanning for "
                    "any file that later appears under that prefix, which is "
                    "the exact contrast this repository draws against its own "
                    "digest-binding doctrine elsewhere. The refreshed "
                    "CLM-SECRET-SCAN falsifier states what the scoping proves "
                    "and never what it still permits."
                ),
                "release_consequence": (
                    "A real credential committed under docs/gauntlet-runs/ "
                    "would not be caught by this scan. Residual risk is "
                    "bounded by review, not by the oracle: reaching that path "
                    "requires a reviewed commit into an immutable record "
                    "directory. Treat it as a review obligation on gauntlet-run "
                    "records, not as scanner coverage. Disclosed as R5-NF2; "
                    "the narrowness control is necessary and not sufficient."
                ),
                "owner": "agent",
            },
            {
                "id": "KL-WINDOWS",
                "kind": "platform",
                "statement": "No native Windows requalification was run for this candidate.",
                "release_consequence": "CLM-WINDOWS-FS stays LIMITED.",
                "owner": "agent",
            },
            {
                "id": "KL-RESTAMP",
                "kind": "integrity",
                "statement": (
                    "The predecessor freeze's packet artifacts were "
                    "generated at one commit and mutated at the freeze "
                    "commit while still carrying the earlier stamp — "
                    "self-falsifying evidence nothing detected (gauntlet "
                    "ruling R5). The two specific instances R5(c) named "
                    "(kimi ruling S4 completed this disclosure): (1) "
                    "clean-baseline.json was ADDED to the predecessor "
                    "packet after its freeze while the packet claimed "
                    "immutability; (2) the packet's original disclaimer — "
                    "that a recorded candidate SHA is an OBSERVATION of "
                    "the tree it was generated from, never a target to "
                    "restamp — was deleted rather than preserved, and its "
                    "substance is hereby re-erected as the governing "
                    "invariant of this packet. This packet is generated "
                    "under the C/C+1 discipline: generation refuses a "
                    "dirty tree and refuses --sha != HEAD, the source "
                    "inventory binds per-file sha256 digests of git-"
                    "tracked sources plus the candidate tree hash, and "
                    "the validator recomputes those digests and rejects "
                    "untracked inventory paths (S1)."
                ),
                "release_consequence": "Any post-freeze edit to an inventoried file turns the validator red instead of shipping silently; the SHA-is-an-observation invariant governs every artifact in this directory.",
                "owner": "agent",
            },
            {
                "id": "KL-GUARD-LEXICAL",
                "kind": "integrity",
                "statement": (
                    "Custody guard path matching is lexical; a write "
                    "spelled through a symlinked parent resolves inside a "
                    "guarded tree while the guard does not match "
                    "(measured probe; characterization-pinned; disclosed "
                    "in mission-custody SECURITY.md). No matching-behavior "
                    "change this epoch per gauntlet ruling R15."
                ),
                "release_consequence": "Guard globs bound spellings, not filesystem effects; CLM-MC-GUARD-LEXICAL stays LIMITED.",
                "owner": "agent",
            },
        ] + operator_limited_limits(matrix),
        "evidence_paths": [
            "docs/v6/ES6-V6-CANDIDATE/claim-to-proof-matrix.json",
            "docs/v6/ES6-V6-CANDIDATE/issue-pr-reconciliation.json",
            "docs/v6/ES6-V6-CANDIDATE/source-inventory.json",
            "docs/v6/ES6-V6-CANDIDATE/exact-candidate-receipt.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/clean-baseline.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/workflow-oracle-audit.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/public-content.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/custody-suite.json",
            # R3-NF8: the requalification and tracker captures ARE packet
            # evidence — listing them only per-claim hid them from the
            # packet-level index.
            "docs/v6/ES6-V6-CANDIDATE/evidence/requalification.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/tracker-capture.json",
        ],
    }


def load_tracker() -> tuple[list[dict], list[dict]]:
    issues = gh_json(
        [
            "issue",
            "list",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,labels,url",
        ]
    )
    prs = gh_json(
        [
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,labels,url,isDraft",
        ]
    )
    pr_numbers = {p["number"] for p in prs}
    issues = [i for i in issues if i["number"] not in pr_numbers]
    return issues, prs


def dirty_tree() -> list[str]:
    out = subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=REPO_ROOT, text=True
    )
    return [line for line in out.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sha",
        help="Stamp this commit as the candidate (must equal HEAD; default: HEAD)",
    )
    parser.add_argument(
        "--tracker-json",
        type=Path,
        help="Read {issues:[...], prs:[...]} from this file instead of the gh "
        "CLI (for hosts without gh; the file must be a verbatim live capture).",
    )
    args = parser.parse_args()
    sha = args.sha or git_head()
    if len(sha) != 40:
        sha = subprocess.check_output(
            ["git", "rev-parse", sha], cwd=REPO_ROOT, text=True
        ).strip()
    # R5d (C/C+1 discipline): the packet must be generated AT the commit it
    # names, from a clean tree. Anything else reproduces the predecessor's
    # self-falsifying restamp (artifacts stamped with a SHA whose tree they
    # do not describe). No override flag exists on purpose.
    head = git_head()
    if sha != head:
        raise SystemExit(
            f"RESTAMP_REFUSED: --sha {sha[:12]} != HEAD {head[:12]}. Check out "
            "the candidate commit and regenerate; a packet may only describe "
            "the tree it was generated from (C/C+1 layering)."
        )
    dirty = dirty_tree()
    # The packet output directory itself is the one permitted difference: a
    # regeneration overwrites docs/v6/ES6-V6-CANDIDATE/* in place before the
    # C+1 commit records it.
    blocking_dirt = [
        line for line in dirty
        if "docs/v6/ES6-V6-CANDIDATE/" not in line
    ]
    if blocking_dirt:
        raise SystemExit(
            "DIRTY_TREE_REFUSED: the working tree differs from HEAD outside "
            f"the packet directory ({len(blocking_dirt)} entries, e.g. "
            f"{blocking_dirt[0]!r}). Commit or stash first; evidence stamped "
            "from a dirty tree is the R5 defect class."
        )
    ts = _now()
    if args.tracker_json:
        blob = json.loads(args.tracker_json.read_text(encoding="utf-8"))
        issues, prs = blob["issues"], blob["prs"]
        pr_numbers = {p["number"] for p in prs}
        issues = [i for i in issues if i["number"] not in pr_numbers]
    else:
        issues, prs = load_tracker()
    require_dispositions(issues, prs)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "evidence").mkdir(parents=True, exist_ok=True)
    recon = build_reconciliation(sha, ts, issues, prs)
    matrix = build_claim_matrix(sha, ts, issues, prs)
    (OUT_DIR / "exact-candidate-receipt.json").write_text(
        json.dumps(build_receipt(sha, ts), indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "issue-pr-reconciliation.json").write_text(
        json.dumps(recon, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "source-inventory.json").write_text(
        json.dumps(build_source_inventory(sha, ts), indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "claim-to-proof-matrix.json").write_text(
        json.dumps(matrix, indent=2) + "\n", encoding="utf-8"
    )
    (OUT_DIR / "promotion-packet.json").write_text(
        json.dumps(build_promotion_packet(sha, ts, matrix), indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"generated {PROGRAM} at {OUT_DIR} for {sha[:12]} "
        f"({len(matrix['claims'])} claims, {len(recon['items'])} tracker items)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
