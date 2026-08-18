#!/usr/bin/env python3
"""Generate ES6-BASELINE-CLAIMS artifacts (matrix, reconciliation, inventory)."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "docs/v6/ES6-ZI-001"
PROGRAM = "ES6-ZI-001"


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
    ).strip()


def gh_json(args: list[str]) -> list[dict]:
    out = subprocess.check_output(["gh", *args], cwd=REPO_ROOT, text=True)
    data = json.loads(out)
    return data if isinstance(data, list) else [data]


# Dispositions from the 2026-08-18 metacognate/recon review (#191 reconciliation).
ISSUE_DISPOSITIONS: dict[int, dict] = {
    191: {
        "phase": "ES6-ZI-001",
        "disposition": "reconcile-in-matrix",
        "owner": "program",
        "evidence_note": "Parent v6 program; this run implements packet 1–3.",
    },
    186: {
        "phase": "ES6-ZI-001",
        "disposition": "reconcile-in-matrix",
        "owner": "operator+agent",
        "evidence_note": "Post-tag docket; path-filter guard lands in oracle audit.",
    },
    173: {
        "phase": "blocked-parent",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "blocked_by": [],
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
        "evidence_note": "Capture real harness hook payloads.",
    },
    137: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "P1 false-allow bypasses from PR #128 review.",
    },
    136: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Cursor CLI hook must use plugin-root path.",
    },
    129: {
        "phase": "custody-build-packet",
        "disposition": "implement-when-unblocked",
        "owner": "agent",
        "evidence_note": "Antigravity adapter not wired.",
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
        "phase": "ES6-ZI-001",
        "disposition": "reconcile-in-matrix",
        "owner": "agent",
        "evidence_note": "Exact-candidate public-content gate.",
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
        "disposition": "reconcile-in-matrix",
        "owner": "joint",
        "evidence_note": "Items 1–2 done; field-pair supply remains.",
    },
    77: {
        "phase": "evidence-process",
        "disposition": "close-when-evidence",
        "owner": "agent",
        "evidence_note": "Behavioral epoch program.",
    },
    40: {
        "phase": "frontier-decision",
        "disposition": "reconcile-in-matrix",
        "owner": "operator",
        "evidence_note": "Re-scope v3 Step-7b into v6 Gauntlet.",
    },
    39: {
        "phase": "evidence-process",
        "disposition": "close-when-evidence",
        "owner": "agent",
        "evidence_note": "Four-arm superiority run.",
    },
}

PR_DISPOSITIONS: dict[int, dict] = {
    190: {
        "phase": "ES6-ZI-001",
        "disposition": "reconcile-in-matrix",
        "owner": "operator",
        "evidence_note": "Merged 2026-08-18 (dcf26f2): RELEASING.md required-job semantics for dispatch-only diagnostics.",
    },
    176: {
        "phase": "park",
        "disposition": "do-not-merge",
        "owner": "agent",
        "evidence_note": "94k-line planning boundary; DCO red; verdict narrow.",
    },
    156: {
        "phase": "frontier-decision",
        "disposition": "keep-sequence",
        "owner": "operator",
        "evidence_note": "Publication authorization step; sequence with #190.",
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
    192: {
        "phase": "ES6-ZI-001",
        "disposition": "reconcile-in-matrix",
        "owner": "agent",
        "evidence_note": "ES6-ZI-001 baseline claims, oracle audit, clean baseline (draft).",
    },
}

DEFAULT_ISSUE = {
    "phase": "custody-build-packet",
    "disposition": "implement-when-unblocked",
    "owner": "agent",
    "evidence_note": "Mission-custody residue; deferred past ES6-ZI-001 per #191.",
}


def build_reconciliation(sha: str, ts: str) -> dict:
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
    pr_numbers = {p["number"] for p in gh_json(["pr", "list", "--state", "open", "--limit", "100", "--json", "number"])}
    issues = [i for i in issues if i["number"] not in pr_numbers]
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
                "phase": "ES6-ZI-001",
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


def build_claim_matrix(sha: str, ts: str) -> dict:
    return {
        "schema": "claim-to-proof-matrix@1",
        "program": PROGRAM,
        "exact_start_sha": sha,
        "generated_at": ts,
        "claims": [
            {
                "id": "CLM-STDlib-GATE",
                "statement": "The epistemic-flexibility stdlib-checks job exercises every packaged skill contract and integration surface on push/PR to main.",
                "authority": "RELEASING.md gate 5; .github/workflows/epistemic-flexibility.yml",
                "subject": f"commit {sha}",
                "oracle": "GitHub Actions stdlib-checks job green on candidate; local v6_run_clean_baseline.py reproduces extracted python steps.",
                "falsifier": "A committed change to a gated surface passes push without triggering stdlib-checks or without failing a required step.",
                "environment": "ubuntu-24.04 CI; clean-room Linux checkout",
                "independence": "Workflow-declared steps; scorer/runner separation in eval harnesses",
                "evidence_tier": "R1",
                "status": "PARTIAL",
                "release_consequence": "P1 — cannot tag without green stdlib-checks on exact candidate",
                "owner": "agent",
                "closure_path": "ES6-ORACLE-AUDIT path-filter coverage + ES6-CLEAN-BASELINE evidence",
                "linked_issues": [186, 191],
                "evidence_paths": [
                    ".github/workflows/epistemic-flexibility.yml",
                    ".github/scripts/cleanroom_ci.sh",
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
                "closure_path": "plugins/epistemic-skills/evals/** added to epistemic-flexibility path filters; oracle audit 0 findings",
                "linked_issues": [186, 191],
            },
            {
                "id": "CLM-MC-HOOK-POSIX",
                "statement": "mission-custody test_custody_hook.py POSIX branch runs in CI on ubuntu-24.04.",
                "authority": ".github/workflows/mission-custody-contract.yml",
                "subject": "plugins/epistemic-skills/contracts/mission-custody/test_custody_hook.py",
                "oracle": "mission-custody-contract job step 'Custody enforcement hook tests' executes on push/PR.",
                "falsifier": "Hook test file changes without mission-custody-contract workflow dispatch.",
                "environment": "ubuntu-24.04",
                "independence": "CI runner distinct from developer host",
                "evidence_tier": "R1",
                "status": "PROVED",
                "release_consequence": "P1 for custody claims",
                "owner": "agent",
                "closure_path": "Already wired; retained in matrix for regression",
                "linked_issues": [136, 142],
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
                "closure_path": "Probe at open + es#162 fix in later custody packet",
                "linked_issues": [162, 186, 190],
            },
            {
                "id": "CLM-PUBLIC-CONTENT",
                "statement": "Exact candidate public tree contains no disallowed private identifiers or user-specific paths.",
                "authority": "RELEASING.md; es#105; check_public_content.py",
                "subject": f"commit {sha} public tree",
                "oracle": "check_public_content.py green with seeded RED controls",
                "falsifier": "Seeded private-repo id or user path pattern passes gate.",
                "environment": "CI + exact-candidate review record",
                "independence": "checker distinct from content author",
                "evidence_tier": "R1",
                "status": "PARTIAL",
                "release_consequence": "P1 — item 6b not met for v5.0.0; required for v6",
                "owner": "agent",
                "closure_path": "Finish #105 remediation + exact-candidate review step in RELEASING.md",
                "linked_issues": [105, 145],
            },
            {
                "id": "CLM-V5-DESIGN-COMMITMENTS",
                "statement": "Each approved v5 design commitment is implemented, retired with amended public claims, or explicitly limited.",
                "authority": "es#104; v5 design spec",
                "subject": "ROUTING.md, intrinsic ledgers, sentinel corpora, structural membership",
                "oracle": "Claim matrix row per commitment with PROVED/RETIRED/LIMITED status",
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
                "authority": "PR #156; RELEASING.md step 7 (not yet on main)",
                "subject": "refs/tags/v* creation",
                "oracle": "Committed release notes name verdict, exact SHA, owner; ruleset creation rule armed except during authorized window.",
                "falsifier": "Tag created without authorization line or with ruleset left disarmed.",
                "environment": "GitHub ruleset + release notes",
                "independence": "operator authorization",
                "evidence_tier": "R0",
                "status": "UNPROVED",
                "release_consequence": "PROMOTION gate — merge #156/#190 only with operator word",
                "owner": "operator",
                "closure_path": "Operator approves #190 and #156; #186 tag-ruleset decision",
                "linked_prs": [156, 190],
                "linked_issues": [186],
            },
        ],
    }


def build_exact_start_receipt(sha: str, ts: str) -> dict:
    return {
        "schema": "exact-start-receipt@1",
        "program": PROGRAM,
        "issue": 191,
        "exact_start_sha": sha,
        "recorded_at": ts,
        "parent_program": "ZMS-Labs/zms-homelab#1601",
        "authorized_packets": [
            "ES6-BASELINE-CLAIMS",
            "ES6-ORACLE-AUDIT",
            "ES6-CLEAN-BASELINE",
        ],
        "forbidden_this_run": [
            "merge",
            "tag",
            "close issues",
            "close PRs",
            "settings/ruleset changes",
            "mission-custody implementation packets",
            "behavioral epoch runs",
            "promotion",
        ],
    }


def main() -> int:
    sha = git_head()
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "exact-start-receipt.json").write_text(
        json.dumps(build_exact_start_receipt(sha, ts), indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "issue-pr-reconciliation.json").write_text(
        json.dumps(build_reconciliation(sha, ts), indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "source-inventory.json").write_text(
        json.dumps(build_source_inventory(sha, ts), indent=2) + "\n",
        encoding="utf-8",
    )
    (OUT_DIR / "claim-to-proof-matrix.json").write_text(
        json.dumps(build_claim_matrix(sha, ts), indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated ES6-BASELINE-CLAIMS artifacts at {OUT_DIR} for {sha[:12]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
