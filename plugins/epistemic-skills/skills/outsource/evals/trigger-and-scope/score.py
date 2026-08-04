#!/usr/bin/env python3
"""Deterministic scorer for outsource trigger discipline and the packet/relay contracts."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ACTIONS = {"publish-packet", "verify-relay", "report-blocked", "no-fire"}
BLOCKERS = {"unpushed-packet", "target-capability", "hidden-context"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# docs/outsource/<work-id>/HANDOFF.md where <work-id> is a short lowercase
# hyphenated slug — a path with no work-id segment is off-contract.
HANDOFF_RE = re.compile(r"^docs/outsource/[a-z0-9]+(?:-[a-z0-9]+)*/HANDOFF\.md$")

# A no-fire is silent. These are the process artifacts a silent episode may not
# produce: flag fields that may not be truthy, string fields that may not be
# non-empty.
NO_FIRE_FLAG_ARTIFACTS = (
    "packet_committed",
    "pushed",
    "prompt_emitted",
    "capability_preflight",
    "relay_template_recorded",
    "visible_process",
)
NO_FIRE_STRING_ARTIFACTS = ("immutable_ref", "handoff_path")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _id_set(row: dict, field: str, fid: str, failures: list) -> set:
    """Fail closed on non-list list-fields: name the shape violation instead
    of crashing on (or silently coercing) honest off-contract input."""
    value = row.get(field, [])
    if not isinstance(value, list):
        failures.append(f"{fid}: {field} must be an array of bare ids, got {type(value).__name__}")
        return set()
    bad = [entry for entry in value if not isinstance(entry, str)]
    if bad:
        failures.append(
            f"{fid}: {field} must be an array of bare ids, got {type(bad[0]).__name__} entry"
        )
        return set()
    return set(value)


def score(fixtures: list[dict], responses: object) -> dict:
    failures: list[str] = []
    if not isinstance(responses, list):
        return {
            "pass": False,
            "failures": [f"responses must be an array of response objects, got {type(responses).__name__}"],
            "actions": {},
        }
    by_id = {
        row.get("id"): row
        for row in responses
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    if len(by_id) != len(responses):
        failures.append("response ids missing or duplicated")
    actions: Counter = Counter()
    for fixture in fixtures:
        fid = fixture["id"]
        row = by_id.get(fid)
        if row is None:
            failures.append(f"{fid}: response missing")
            continue
        action = row.get("action")
        if isinstance(action, str):
            actions[action] += 1
        expected = fixture["expected_action"]
        if not isinstance(action, str) or action not in ACTIONS:
            failures.append(f"{fid}: unknown action {action!r}")
            continue
        if action != expected:
            failures.append(f"{fid}: expected {expected}, got {action}")
            continue
        if expected == "no-fire":
            artifacts = sorted(
                [f for f in NO_FIRE_FLAG_ARTIFACTS if row.get(f)]
                + [f for f in NO_FIRE_STRING_ARTIFACTS if _nonempty(row.get(f))]
            )
            if artifacts:
                failures.append(
                    f"{fid}: no-fire must be silent — no packet, no prompt, no preflight, "
                    f"no process artifact ({', '.join(artifacts)} set)"
                )
        elif expected == "publish-packet":
            if not row.get("packet_committed"):
                failures.append(f"{fid}: the packet must be committed — the repo is the memory, not the chat")
            if not row.get("pushed"):
                failures.append(f"{fid}: only a pushed commit is target-readable GitHub state")
            if not row.get("packet_published_first"):
                failures.append(f"{fid}: the packet is committed and pushed BEFORE any prompt is sent")
            ref = row.get("immutable_ref")
            if not (isinstance(ref, str) and SHA_RE.fullmatch(ref)):
                failures.append(
                    f"{fid}: the pointer names an immutable 40-character commit SHA, "
                    f"never a mutable branch or a locally guessed ref"
                )
            path = row.get("handoff_path")
            if not (isinstance(path, str) and HANDOFF_RE.fullmatch(path)):
                failures.append(f"{fid}: the packet lives at docs/outsource/<work-id>/HANDOFF.md — one predictable location")
            if not row.get("prompt_emitted"):
                failures.append(f"{fid}: publishing ends with the short copy/paste prompt and the readiness receipt")
            if not row.get("prompt_is_pointer") or row.get("full_context_pasted"):
                failures.append(f"{fid}: the prompt is the pointer — the handoff body is never pasted into it")
            if not row.get("relay_template_recorded"):
                failures.append(f"{fid}: the canonical outbound prompt template is stored in relay/NNNN-origin.md before dispatch")
            required = fixture.get("required_capabilities", [])
            if required:
                if not row.get("capability_preflight"):
                    failures.append(f"{fid}: dispatch is gated on target capability preflight before any READY pointer")
                verified = _id_set(row, "capabilities_verified", fid, failures)
                missing = sorted(set(required) - verified)
                if missing:
                    failures.append(f"{fid}: capability preflight must verify every required check — missing {missing}")
        elif expected == "verify-relay":
            if not row.get("stored_verbatim"):
                failures.append(f"{fid}: a returned relay is saved verbatim as relay/NNNN-target.md before it bears load")
            if not row.get("relay_verified"):
                failures.append(f"{fid}: a relay is a claim, not evidence — the origin re-verifies it against live state")
            if row.get("trusted_unverified"):
                failures.append(f"{fid}: 'the target said the tests pass' is never accepted before re-verification")
            claims = set(fixture.get("relay_claims", []))
            checked = _id_set(row, "claims_checked", fid, failures)
            if not claims <= checked:
                failures.append(f"{fid}: every relayed claim is checked — missing {sorted(claims - checked)}")
            if not row.get("packet_updated"):
                failures.append(f"{fid}: HANDOFF.md is updated with the verified current state before the next prompt")
        elif expected == "report-blocked":
            if not row.get("blocked"):
                failures.append(f"{fid}: a stop condition returns BLOCKED, never a ready-looking prompt")
            if row.get("prompt_emitted"):
                failures.append(f"{fid}: BLOCKED emits no prompt — a local preview is not a usable outsource prompt")
            want = fixture.get("expected_blocker")
            if want not in BLOCKERS:
                failures.append(f"{fid}: fixture has unknown expected_blocker {want!r}")
                continue
            got = row.get("blocker")
            if got != want:
                failures.append(f"{fid}: name the single blocking condition — expected {want}, got {got!r}")
            failed = fixture.get("failed_capabilities", [])
            if failed:
                if not row.get("capability_preflight"):
                    failures.append(f"{fid}: the capability gap is found by preflight, not by a wasted relay turn")
                caps = _id_set(row, "capabilities_failed", fid, failures)
                if not set(failed) <= caps:
                    failures.append(f"{fid}: every failed capability check is named — missing {sorted(set(failed) - caps)}")
    return {"pass": not failures, "failures": failures, "actions": dict(actions)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("responses", type=Path)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parent / "fixtures.json")
    args = parser.parse_args()
    fixtures = json.loads(args.fixtures.read_text(encoding="utf-8"))
    responses = json.loads(args.responses.read_text(encoding="utf-8"))
    report = score(fixtures, responses)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
