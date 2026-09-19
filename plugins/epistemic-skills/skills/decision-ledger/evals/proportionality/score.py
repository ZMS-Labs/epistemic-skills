#!/usr/bin/env python3
"""Deterministic scorer for Decision Ledger persistence proportionality."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ENTRY_FIELDS = {"entry_type", "subject_revision", "future_consumer", "because", "valid_while", "revisit_when"}
CHAIN_FIELDS = {"prompting_event", "vulnerabilities", "links", "target_failure", "consequences", "earliest_interruptible_link", "replacement_behavior", "rehearsal_fixture"}
REF_FIELDS = {"coordinate", "subject_revision", "future_consumer", "revisit_condition"}


def score(fixtures: list[dict], responses: list[dict]) -> dict:
    failures: list[str] = []
    by_id = {row.get("id"): row for row in responses if isinstance(row, dict)}
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    actions = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        actions[action] += 1
        expected = fixture["expected_action"]
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
        entries = row.get("new_entries", [])
        ref = row.get("existing_ref")
        if expected == "resume":
            for field in ("revision", "authority", "answer", "next_action"):
                if row.get(field) != fixture[field]:
                    failures.append(f"{fid}: continuation must preserve current {field}")
            checked = row.get("rechecked", [])
            if not isinstance(checked, list) or not all(isinstance(x, str) for x in checked) or not set(fixture["rechecked"]) <= set(checked):
                failures.append(f"{fid}: next action lacks relevant re-anchoring")
            for field in ("restarted_investigation", "asked_authority_again", "task_complete"):
                if row.get(field) is not False:
                    failures.append(f"{fid}: settled authorized repair must continue without {field}")
            if entries:
                failures.append(f"{fid}: resumption alone does not require new entries")
            continue
        if expected == "outcome-review":
            for field in ("prediction", "observation", "source"):
                if row.get(field) != fixture[field]:
                    failures.append(f"{fid}: preserve separate original {field}")
            if row.get("standing_guidance") is not False:
                failures.append(f"{fid}: outcome data does not authorize standing guidance")
            continue
        if expected == "no-op":
            if entries or ref is not None or row.get("visible_process"):
                failures.append(f"{fid}: routine no-op must be silent and artifact-free")
        elif expected == "reuse":
            if not isinstance(ref, dict) or not REF_FIELDS <= set(ref) or not all(ref.get(k) for k in REF_FIELDS):
                failures.append(f"{fid}: adequate existing artifact is not resolvably anchored")
            if entries:
                failures.append(f"{fid}: duplicate store created despite adequate existing artifact")
            if fixture.get("requires_reanchor"):
                if row.get("reanchored") is not True:
                    failures.append(f"{fid}: ADR reuse does not waive resume re-anchoring")
                if row.get("claims_jsonl_validation") is not False:
                    failures.append(f"{fid}: ordinary ADR reuse does not prove JSONL mechanical checks")
        else:
            if ref is not None or len(entries) != 1:
                failures.append(f"{fid}: uncovered consequential item requires exactly one new entry")
                continue
            entry = entries[0]
            if not ENTRY_FIELDS <= set(entry) or not all(entry.get(k) for k in ENTRY_FIELDS):
                failures.append(f"{fid}: new entry lacks persistence contract fields")
            if fixture["recurrent_correction"]:
                chain = entry.get("failure_chain")
                if not isinstance(chain, dict) or not CHAIN_FIELDS <= set(chain) or not all(chain.get(k) for k in CHAIN_FIELDS):
                    failures.append(f"{fid}: recurrent correction requires complete failure_chain")
            elif entry.get("failure_chain") is not None:
                failures.append(f"{fid}: failure_chain is correction-only")
    return {"pass": not failures, "failures": failures, "actions": dict(sorted(actions.items()))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).parent / "fixtures.json")
    parser.add_argument("--responses", type=Path, required=True)
    args = parser.parse_args()
    report = score(json.loads(args.fixtures.read_text(encoding="utf-8")),
                   json.loads(args.responses.read_text(encoding="utf-8")))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
