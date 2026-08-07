#!/usr/bin/env python3
"""Migrate the exact watch-commission example corpus to the final carrier.

This branch-scoped helper refuses unknown or missing fixtures, updates every
existing record deterministically, and adds one positive transition example.
It is removed after the generated commit is verified.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = (
    ROOT
    / "plugins"
    / "epistemic-skills"
    / "contracts"
    / "watch-commission"
    / "examples"
)
EXPECTED = {
    "invalid-inert-partial-proof-history.json",
    "invalid-proven-without-alert.json",
    "invalid-proven-without-kill-switch.json",
    "invalid-proven-without-production-path.json",
    "invalid-skill-is-observer.json",
    "invalid-suspect-without-observed-failure.json",
    "valid-blocked.json",
    "valid-inert-with-proof-history.json",
    "valid-proven.json",
    "valid-suspect-observed-failure.json",
}
NEW_FILE = "valid-blocked-kill-switch-unproven.json"
EMPTY_BLOCK = {"detail": None, "observed_at": None, "receipt_ref": None}


def write(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def ensure_fixture_scope(payload: dict) -> None:
    observer = payload.get("external_observer") or {}
    if observer.get("substrate_kind") != "fixture":
        return
    limits = payload.setdefault("coverage_limits", [])
    joined = " ".join(item for item in limits if isinstance(item, str)).lower()
    if "fixture" not in joined or "production" not in joined:
        limits.append("isolated fixture evidence; no production provider or environment claimed")


def main() -> int:
    actual = {path.name for path in EXAMPLES.glob("*.json")}
    if actual != EXPECTED:
        missing = sorted(EXPECTED - actual)
        unexpected = sorted(actual - EXPECTED)
        raise SystemExit(
            f"example corpus drifted; missing={missing} unexpected={unexpected}"
        )

    records: dict[str, dict] = {}
    for name in sorted(EXPECTED):
        path = EXAMPLES / name
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise SystemExit(f"{name}: root must be an object")
        if payload.get("schema") != "watch-commission@1":
            raise SystemExit(f"{name}: schema mismatch")
        payload["block_evidence"] = copy.deepcopy(EMPTY_BLOCK)
        if payload.get("state") == "BLOCKED":
            if name != "valid-blocked.json":
                raise SystemExit(f"{name}: unexpected pre-existing BLOCKED fixture")
            payload["block_evidence"] = {
                "detail": "capability discovery found no external observation substrate",
                "observed_at": "2026-08-07T11:55:00Z",
                "receipt_ref": "fixture://receipt/block-no-substrate-001",
            }
        ensure_fixture_scope(payload)
        records[name] = payload
        write(path, payload)

    transition = copy.deepcopy(records["valid-proven.json"])
    transition["_expected"] = "ACCEPT"
    transition["commission_id"] = "wc-example-blocked-kill-unproven-001"
    transition["external_observer"]["enabled"] = False
    transition["kill_switch"] = {
        "procedure_ref": "fixture://kill/example-001",
        "exercised": False,
        "exercise_receipt_ref": None,
    }
    transition["proof"] = {
        "authorized_by": None,
        "authorization_ref": None,
        "safe_crossing": None,
        "production_path": False,
        "bound_crossed": False,
        "alert_received": False,
        "received_at": None,
        "alert_receipt_ref": None,
    }
    transition["failure"] = {
        "kind": None,
        "detail": None,
        "observed_at": None,
        "receipt_ref": None,
    }
    transition["block_evidence"] = {
        "detail": "the real mechanism exists but its disable path has not been exercised",
        "observed_at": "2026-08-07T11:57:00Z",
        "receipt_ref": "fixture://receipt/block-kill-unproven-001",
    }
    transition["state"] = "BLOCKED"
    transition["block_reason"] = "KILL_SWITCH_UNPROVEN"
    transition["reprove_after"] = None
    transition["coverage_limits"] = [
        "isolated fixture transition; no production provider or environment claimed"
    ]
    write(EXAMPLES / NEW_FILE, transition)

    print(f"migrated {len(records)} examples and added {NEW_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
