#!/usr/bin/env python3
"""Generate the ES6-V6-CANDIDATE BUILD freeze (issue #191 terminal contract).

This packet is BUILD, not PROMOTION. It may not claim independent Gauntlet GO.
The same actor that produced the work refuses self-certification.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs/v6/ES6-V6-CANDIDATE"
PROGRAM = "ES6-V6-CANDIDATE"

# Dispositions from the 2026-08-18 recon map, refreshed for this candidate.
ISSUE_DISPOSITIONS: dict[int, dict] = {
    191: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "reconcile-in-matrix",
        "owner": "program",
        "evidence_note": "Parent v6 program; this packet is the BUILD freeze.",
    },
    186: {
        "phase": "frontier-decision",
        "disposition": "hold-operator",
        "owner": "operator+agent",
        "evidence_note": "Path-filter guard landed; tag-ruleset decision remains.",
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
        "phase": "frontier-decision",
        "disposition": "hold-operator",
        "owner": "operator",
        "evidence_note": "Implement vs retire v5 design commitments.",
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
        "phase": "frontier-decision",
        "disposition": "hold-operator",
        "owner": "joint",
        "evidence_note": "Items 1–2 done; field-pair supply remains.",
    },
    77: {
        "phase": "evidence-process",
        "disposition": "close-when-evidence",
        "owner": "agent",
        "evidence_note": "Behavioral epoch program; live environment required.",
    },
    40: {
        "phase": "frontier-decision",
        "disposition": "hold-operator",
        "owner": "operator",
        "evidence_note": "Re-scope v3 Step-7b into v6 Gauntlet.",
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
}

PR_DISPOSITIONS: dict[int, dict] = {
    193: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "in-candidate-draft",
        "owner": "agent",
        "evidence_note": "es#137 P1+P2; included in this candidate tree; not merged to main.",
    },
    194: {
        "phase": "ES6-V6-CANDIDATE",
        "disposition": "in-candidate-draft",
        "owner": "agent",
        "evidence_note": "This BUILD freeze packet; draft; not a PROMOTION merge.",
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

DEFAULT_ISSUE = {
    "phase": "custody-build-packet",
    "disposition": "implement-when-unblocked",
    "owner": "agent",
    "evidence_note": "Mission-custody residue; not implemented on this candidate.",
}

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


def class_claims(sha: str) -> list[dict]:
    """Material claim classes required by #191, independent of tracker rows."""
    return [
        {
            "id": "CLM-STDLIB-GATE",
            "statement": "The epistemic-flexibility stdlib-checks job exercises every packaged skill contract and integration surface on push/PR to main.",
            "authority": "RELEASING.md gate 5; .github/workflows/epistemic-flexibility.yml",
            "subject": f"commit {sha}",
            "oracle": "cleanroom_ci.sh extracts workflow python steps and all pass; GitHub stdlib-checks on a non-draft candidate.",
            "falsifier": "A committed change to a gated surface passes push without triggering stdlib-checks or without failing a required step.",
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
            "statement": "Each CI workflow's path filter is a superset of the files its steps read or execute.",
            "authority": "es#186 docket path-filter guard; ES6-ORACLE-AUDIT",
            "subject": "all .github/workflows/*.yml",
            "oracle": "v6_audit_workflow_oracles.py exits 0 with no uncovered_paths findings.",
            "falsifier": "A change confined to a test input outside the workflow path filter does not dispatch the workflow.",
            "environment": "repository static analysis",
            "independence": "script distinct from workflow authors",
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
            "statement": "The evidence system can reject a plausible wrong world (negative, positive, and mutation controls).",
            "authority": "#191 terminal contract",
            "subject": f"commit {sha} eval harnesses + custody suites",
            "oracle": "Existing RED seeds (public-content --self-test, custody positive controls) fail when the control is removed.",
            "falsifier": "A seeded defect grades clean, or a mutation of a required assertion still passes.",
            "environment": "local Linux + CI ubuntu-24.04",
            "independence": "scorer/runner separation in eval harnesses; custody tests are not the production hook",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 if oracles cannot fail",
            "owner": "agent",
            "closure_path": "Public-content RED seeds + custody suite mutation notes; full mutation battery is later evidence-process",
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
            "statement": "Scope matching behaves correctly on case-insensitive APFS.",
            "authority": "es#162; mission-custody-contract contract-macos job",
            "subject": "custody scope case fold",
            "oracle": "workflow_dispatch contract-macos probe_case_insensitivity.py measured outcome recorded.",
            "falsifier": "PASS after writing secrets/ when scope.out lists Secrets/ on case-insensitive FS.",
            "environment": "macos-14 workflow_dispatch only",
            "independence": "dispatch-only diagnostic; not merge-gating per #190 lineage",
            "evidence_tier": "R3",
            "status": "LIMITED",
            "release_consequence": "Disclosed limitation until probe + fix land",
            "owner": "agent",
            "closure_path": "es#162 remains open",
            "linked_issues": [162, 186],
        },
        {
            "id": "CLM-PUBLIC-CONTENT",
            "statement": "Exact candidate public tree contains no disallowed private identifiers or user-specific paths outside exact-file allowlist.",
            "authority": "RELEASING.md; es#105; check_public_content.py",
            "subject": f"commit {sha} public tree",
            "oracle": "check_public_content.py --self-test and live run both exit 0",
            "falsifier": "Seeded private-repo id or user path pattern passes gate; or live scan hits a non-allowlisted file.",
            "environment": "CI + exact-candidate review record",
            "independence": "checker distinct from content author",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 — item 6b required for v6",
            "owner": "agent",
            "closure_path": "Allowlist only the ES6-ZI-001 parent-tracker files; remaining #105/#145 residue still open",
            "linked_issues": [105, 145],
        },
        {
            "id": "CLM-V5-DESIGN-COMMITMENTS",
            "statement": "Each approved v5 design commitment is implemented, retired with amended public claims, or explicitly limited.",
            "authority": "es#104; v5 design spec",
            "subject": "ROUTING.md, intrinsic ledgers, sentinel corpora, structural membership",
            "oracle": "Claim matrix row per commitment with PROVED/RETIRED/LIMITED status after operator decision",
            "falsifier": "Public doc promises artifact that does not exist and is not marked retired.",
            "environment": "repository + operator decision record",
            "independence": "operator decision for retire path",
            "evidence_tier": "R0",
            "status": "BLOCKED",
            "release_consequence": "Blocks successor GO",
            "owner": "operator",
            "closure_path": "Operator interview on #104 implement vs retire",
            "linked_issues": [104],
        },
        {
            "id": "CLM-RELEASE-AUTH",
            "statement": "Publication requires explicit owner authorization recorded before tag creation.",
            "authority": "PR #156 (merged); RELEASING.md step 7",
            "subject": "refs/tags/v* creation",
            "oracle": "Committed release notes name verdict, exact SHA, owner; ruleset creation rule armed except during authorized window.",
            "falsifier": "Tag created without authorization line or with ruleset left disarmed.",
            "environment": "GitHub ruleset + release notes",
            "independence": "operator authorization",
            "evidence_tier": "R0",
            "status": "PARTIAL",
            "release_consequence": "PROMOTION gate — docs landed; #186 tag-ruleset decision remains",
            "owner": "operator",
            "closure_path": "Operator #186 tag-ruleset; PROMOTION_RUN still required",
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
            "oracle": "Recorded GO by a seat that did not produce the candidate, against this SHA.",
            "falsifier": "The implementer records GO, or GO is recorded against a different SHA.",
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
            "id": "CLM-TRACKER-RECONCILED",
            "statement": "Every current open issue and PR has an explicit evidence-backed disposition, not a citation-only mention.",
            "authority": "#191 required reconciliation",
            "subject": "open GitHub issues and PRs at generation time",
            "oracle": "issue-pr-reconciliation.json item count equals live open tracker count; each item has phase+disposition+owner.",
            "falsifier": "An open issue/PR is absent from the reconciliation, or present with no disposition.",
            "environment": "GitHub Issues/PR API + committed JSON",
            "independence": "generator reads live tracker, not a remembered list",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P2 if the freeze drifts from live tracker",
            "owner": "agent",
            "closure_path": "Regenerate this packet if the open set changes",
            "linked_issues": [191],
            "evidence_paths": [
                "docs/v6/ES6-V6-CANDIDATE/issue-pr-reconciliation.json"
            ],
        },
        {
            "id": "CLM-REQUIRED-JOB",
            "statement": "Dispatch-only diagnostics are documented as non-gating; merge-gating jobs are named and skip on draft PRs.",
            "authority": "RELEASING.md required-job semantics; PR #190",
            "subject": "epistemic-flexibility.yml stdlib-checks; mission-custody-contract.yml contract vs contract-macos",
            "oracle": "RELEASING.md names required vs dispatch-only jobs; workflow if: skips drafts; contract-macos is workflow_dispatch only.",
            "falsifier": "A dispatch-only job is treated as a required check, or a required job runs on a draft PR.",
            "environment": "repository workflows + RELEASING.md",
            "independence": "docs distinct from Actions configuration",
            "evidence_tier": "R1",
            "status": "PROVED",
            "release_consequence": "P2 if required-job semantics drift",
            "owner": "agent",
            "closure_path": "Retained from merged #190; re-audit if workflow if: changes",
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
            "statement": "The three P1 false-allow bypasses and four P2 refusal gaps from es#137 are closed in the candidate tree.",
            "authority": "es#137",
            "subject": "mission-custody hook/gate/validator/CLI/API on this candidate",
            "oracle": "Named acceptance tests green in the full mission-custody-contract suite.",
            "falsifier": "Any of the seven named tests fail, or main (without this candidate) still exhibits the bypass.",
            "environment": "local Linux custody suite; CI ubuntu-24.04 when not draft",
            "independence": "suite is not the production hook process",
            "evidence_tier": "R1",
            "status": "PARTIAL",
            "release_consequence": "P1 false-allows remain on main until this candidate is merged",
            "owner": "agent",
            "closure_path": "Operator merge of this candidate or of #193 after required CI",
            "linked_issues": [137],
            "linked_prs": [193],
        },
    ]


def tracker_claim(kind: str, number: int, title: str, meta: dict, labels: list[str]) -> dict:
    label_set = set(labels)
    status = "UNPROVED"
    if meta["disposition"] == "hold-operator" or meta["phase"] == "frontier-decision":
        status = "BLOCKED"
    elif meta["disposition"] in {"park", "do-not-merge", "harvest-supersede"}:
        status = "LIMITED"
    elif LIVE_LABELS & label_set or meta["disposition"] == "close-when-evidence":
        status = "LIMITED"
    elif meta["disposition"] == "in-candidate-draft":
        status = "PARTIAL"
    elif number in {104, 40, 84, 186} or OPERATOR_LABELS & label_set:
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
        "owner": meta["owner"],
        "closure_path": meta["disposition"],
        "linked_issues": [number] if kind == "issue" else [],
        "linked_prs": [number] if kind == "pr" else [],
    }


def build_reconciliation(sha: str, ts: str, issues: list[dict], prs: list[dict]) -> dict:
    items: list[dict] = []
    for issue in sorted(issues, key=lambda x: x["number"]):
        meta = ISSUE_DISPOSITIONS.get(issue["number"], DEFAULT_ISSUE)
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
        meta = PR_DISPOSITIONS.get(
            pr["number"],
            {
                "phase": "ES6-V6-CANDIDATE",
                "disposition": "reconcile-in-matrix",
                "owner": "agent",
                "evidence_note": "Open PR; disposition recorded at generation time.",
            },
        )
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


def build_source_inventory(sha: str, ts: str) -> dict:
    workflows = sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in (REPO_ROOT / ".github/workflows").glob("*.yml")
    )
    contracts = sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in (REPO_ROOT / "plugins/epistemic-skills/contracts").rglob("*")
        if p.is_file()
    )
    ci_scripts = sorted(
        p.relative_to(REPO_ROOT).as_posix()
        for p in (REPO_ROOT / ".github/scripts").glob("*.py")
    )
    return {
        "schema": "v6-source-inventory@1",
        "exact_start_sha": sha,
        "generated_at": ts,
        "workflows": workflows,
        "contracts": contracts,
        "ci_scripts": ci_scripts,
    }


def build_claim_matrix(sha: str, ts: str, issues: list[dict], prs: list[dict]) -> dict:
    claims = class_claims(sha)
    seen = {c["id"] for c in claims}
    for issue in issues:
        meta = ISSUE_DISPOSITIONS.get(issue["number"], DEFAULT_ISSUE)
        labels = [l["name"] for l in issue.get("labels", [])]
        claim = tracker_claim("issue", issue["number"], issue["title"], meta, labels)
        if claim["id"] not in seen:
            claims.append(claim)
            seen.add(claim["id"])
    for pr in prs:
        meta = PR_DISPOSITIONS.get(
            pr["number"],
            {
                "phase": "ES6-V6-CANDIDATE",
                "disposition": "reconcile-in-matrix",
                "owner": "agent",
                "evidence_note": "Open PR.",
            },
        )
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


def blocking_from_matrix(matrix: dict) -> list[str]:
    by_id = {c["id"]: c for c in matrix["claims"]}
    required = [
        "CLM-INDEPENDENT-GAUNTLET",
        "CLM-V5-DESIGN-COMMITMENTS",
        "CLM-BEHAVIORAL-EPOCHS",
        "CLM-HARNESS-LIVE",
        "CLM-MC-MACOS-CASE",
        "CLM-RELEASE-AUTH",
        "CLM-MC-137",
        "CLM-STDLIB-GATE",
        "CLM-PUBLIC-CONTENT",
    ]
    block = []
    for cid in required:
        claim = by_id.get(cid)
        if claim is None or claim["status"] != "PROVED":
            block.append(cid)
    return block


def build_promotion_packet(sha: str, ts: str, matrix: dict) -> dict:
    return {
        "schema": "v6-promotion-packet@1",
        "program": PROGRAM,
        "issue": 191,
        "candidate_sha": sha,
        "generated_at": ts,
        "readiness": "NOT_READY",
        "self_certification": "refused",
        "independent_gauntlet": "NOT_RUN",
        "rollback": "Do not merge this branch to main. Abandon the branch. main remains the last PROMOTION-valid channel until an independent GO and a separate PROMOTION_RUN.",
        "requested_irreversible_acts": [],
        "blocking_claims": blocking_from_matrix(matrix),
        "known_limits": [
            {
                "id": "KL-SELF-GO",
                "kind": "independence",
                "statement": "The implementer of this packet cannot record Gauntlet GO on it.",
                "release_consequence": "V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE is unreachable until an independent panel runs.",
            },
            {
                "id": "KL-OPERATOR-104",
                "kind": "operator-hold",
                "statement": "es#104 implement-vs-retire is unresolved.",
                "release_consequence": "Blocks successor GO.",
            },
            {
                "id": "KL-OPERATOR-186",
                "kind": "operator-hold",
                "statement": "Tag-ruleset / ratification remainder of es#186 is unresolved.",
                "release_consequence": "Publication authorization docs landed; tag creation still operator-owned.",
            },
            {
                "id": "KL-LIVE-ENV",
                "kind": "live-environment",
                "statement": "Behavioral epochs (#77/#39) and native harness live-fire (#136/#129/#142) were not run.",
                "release_consequence": "Those claims are LIMITED, not PROVED.",
            },
            {
                "id": "KL-MACOS-162",
                "kind": "platform",
                "statement": "es#162 case-insensitivity is disclosed; contract-macos is dispatch-only.",
                "release_consequence": "Not a merge-gating required job; still a named v6 limit.",
            },
            {
                "id": "KL-DRAFT-CI",
                "kind": "integrity",
                "statement": "Draft PRs skip required stdlib-checks and mission-custody-contract jobs.",
                "release_consequence": "Local clean-room is the BUILD oracle until the PR is marked ready.",
            },
            {
                "id": "KL-MAIN-137",
                "kind": "integrity",
                "statement": "es#137 P1 false-allows are present on origin/main; closed only in this candidate tree.",
                "release_consequence": "Merging this candidate is a PROMOTION act, not performed here.",
            },
            {
                "id": "KL-WINDOWS",
                "kind": "platform",
                "statement": "No native Windows requalification was run for this candidate.",
                "release_consequence": "CLM-WINDOWS-FS stays LIMITED.",
            },
        ],
        "evidence_paths": [
            "docs/v6/ES6-V6-CANDIDATE/claim-to-proof-matrix.json",
            "docs/v6/ES6-V6-CANDIDATE/issue-pr-reconciliation.json",
            "docs/v6/ES6-V6-CANDIDATE/source-inventory.json",
            "docs/v6/ES6-V6-CANDIDATE/exact-candidate-receipt.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/clean-baseline.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/workflow-oracle-audit.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/public-content.json",
            "docs/v6/ES6-V6-CANDIDATE/evidence/custody-suite.json",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sha",
        help="Stamp this commit as the candidate (default: HEAD)",
    )
    args = parser.parse_args()
    sha = args.sha or git_head()
    if len(sha) != 40:
        sha = subprocess.check_output(
            ["git", "rev-parse", sha], cwd=REPO_ROOT, text=True
        ).strip()
    ts = _now()
    issues, prs = load_tracker()
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
