#!/usr/bin/env python3
"""Align durable design and plans with the hardened watch-commission contract.

Branch-scoped one-shot migration. Every marker must occur exactly once; otherwise
it fails without writing. The helper and invoking workflow are removed after the
generated commit passes repository checks.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-08-07-practical-agency-and-commission-watch-design.md"
WATCH_PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-08-07-commission-watch-clarification.md"
PRACTICAL_PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-08-07-practical-agency-bootstrap.md"


def replace_region(path: Path, start: str, end: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(
            f"{path}: expected unique region markers; start={text.count(start)} end={text.count(end)}"
        )
    left, remainder = text.split(start, 1)
    _, right = remainder.split(end, 1)
    path.write_text(left + replacement + end + right, encoding="utf-8")


def insert_before_once(path: Path, marker: str, insertion: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(marker) != 1:
        raise SystemExit(f"{path}: expected one insertion marker, found {text.count(marker)}")
    path.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")


def main() -> int:
    hardened_design = r'''## `watch-commission@1`

The carrier separates four facts that must never be collapsed:

1. **current operating state** — whether the observer is absent, blocked,
   disabled, currently trusted and enabled, or presently suspect;
2. **proof history** — either wholly absent or a complete end-to-end proof
   bundle, retained even after deliberate disablement;
3. **positive-claim evidence** — durable references supporting reachability,
   external persistence, kill-switch exercise, proof authority, and alert
   receipt; and
4. **observed failure** — a separately typed, timestamped, receipted incident
   used only when current state is `SUSPECT`.

The JSON Schema is the structural carrier. The stdlib semantic verifier is the
cross-field oracle; a schema-valid record is not automatically trusted.

### Required fields

```yaml
schema: watch-commission@1
commission_id: <stable id>
subject:
  ref: <watched subject>
  revision: <revision or bounded dynamic identity>
bound:
  expression: <comparison>
  units: <units>
  direction: above|below|equals|changes|absent
  threshold: <scalar value>
probe:
  mechanism: <how state is observed>
  cadence_or_event: <when observation occurs>
  failure_modes: []
destination:
  ref: <recipient or endpoint>
  reachable: <boolean>
  reachability_receipt_ref: <durable evidence ref or null>
external_observer:
  substrate_kind: scheduler|event-listener|monitoring-service|human-cadence|other-external|fixture|null
  substrate: <provider/runtime/human-cadence label or null>
  mechanism_ref: <external id or null>
  persistence_receipt_ref: <durable evidence ref or null>
  persistent_outside_session: <boolean>
  enabled: <boolean>
kill_switch:
  procedure_ref: <reference or null>
  exercised: <boolean>
  exercise_receipt_ref: <durable evidence ref or null>
proof:
  authorized_by: <authority identity or null>
  authorization_ref: <durable authority ref or null>
  safe_crossing: <description or null>
  production_path: <boolean>
  bound_crossed: <boolean>
  alert_received: <boolean>
  received_at: <timestamp or null>
  alert_receipt_ref: <durable evidence ref or null>
failure:
  kind: probe|delivery|proof|freshness|kill-switch|external-mechanism|unknown|null
  detail: <observed failure or null>
  observed_at: <timestamp or null>
  receipt_ref: <durable evidence ref or null>
state: DECLARED|BLOCKED|INERT|PROVEN|SUSPECT
block_reason: <closed enum or null>
reprove_after: <timestamp/condition or null>
handoff:
  on_crossing: [triage, decision-ledger]
coverage_limits: []
```

### State semantics

| State | Meaning |
|---|---|
| `DECLARED` | The commission specification exists; no external mechanism or proof attempt is implied. |
| `BLOCKED` | A required dependency is absent, the closed reason agrees with the recorded fields, and the observer remains disabled. |
| `INERT` | A permitted external mechanism is persistence-proven, disabled, and governed by an exercised kill switch. Proof history is either wholly absent or complete. |
| `PROVEN` | The external mechanism is currently enabled, every positive claim is evidence-bound, the production path was safely proof-fired, and a re-proof boundary exists. |
| `SUSPECT` | A permitted external mechanism exists and a specific later failure is recorded with kind, detail, observation time, and receipt. Possible failure modes alone cannot establish this state. |

`state` reports the observer now. A successful proof followed by deliberate
disablement yields `INERT` with complete proof history retained. It does not stay
`PROVEN`, and the proof is not erased. Partial proof history is invalid because it
manufactures an easy-to-overread intermediate state.

`BLOCKED` reasons are closed initially:

```text
NO_EXECUTION_SUBSTRATE
NO_REACHABLE_DESTINATION
NO_AUTHORITY_TO_ENABLE
NO_KILL_SWITCH
KILL_SWITCH_UNPROVEN
NO_SAFE_PROOF_CROSSING
PROBE_UNAVAILABLE
```

The semantic verifier rejects a reason contradicted by the record, such as
`NO_EXECUTION_SUBSTRATE` beside a populated external mechanism and persistence
receipt.

### Positive-claim and promotion rules

A positive boolean never bears load alone:

- `destination.reachable: true` requires `reachability_receipt_ref`;
- `persistent_outside_session: true` requires `persistence_receipt_ref`;
- `kill_switch.exercised: true` requires `exercise_receipt_ref`;
- named proof authority requires `authorization_ref`; and
- `alert_received: true` requires both `received_at` and
  `alert_receipt_ref`.

`PROVEN` additionally requires:

- a permitted external `substrate_kind`, not skill text or chat state;
- populated substrate and external `mechanism_ref`;
- current enablement;
- a named reachable destination;
- an exercised and receipted kill switch;
- a complete proof bundle;
- safe crossing through the production observation and delivery path;
- observed bound crossing and alert receipt; and
- a dated or condition-bound `reprove_after` value.

`INERT` may retain that same complete proof bundle only while the mechanism is
currently disabled. `SUSPECT` may retain historical receipts but requires its own
later observed-failure carrier. Configuration presence, source inspection,
deployment, formatter tests, self-asserted persistence, partial proof fields,
generic failure possibilities, bypass messages, and "no alert yet" cannot satisfy
these rules.

'''
    replace_region(
        DESIGN,
        "## `watch-commission@1`\n",
        "### Runtime division\n",
        hardened_design,
    )

    watch_amendment = r'''## As-built contract refinement — normative over the original task sketches

Implementation uncovered a state/evidence distinction the original task-level
examples did not express. The following rules govern every task below and
supersede any simpler fixture or field sketch later in this plan:

- `state` is current operating state; proof is retained historical evidence.
- A successful proof followed by disablement is valid `INERT` with a complete
  proof bundle, never current `PROVEN` and never discarded evidence.
- Proof history under `INERT` is either wholly absent or complete; partial proof
  is rejected.
- Positive claims require durable receipt references for destination
  reachability, external persistence, kill-switch exercise, proof authority, and
  alert delivery.
- External substrates use a closed type set that excludes Markdown skills and
  prompt/session memory even when they self-assert persistence.
- `PROVEN` requires a re-proof boundary.
- `SUSPECT` requires an observed failure kind, detail, time, and receipt; possible
  failure modes alone are not an incident.
- A `BLOCKED` reason must agree with the other fields in the record.

Additional committed fixtures are required:

- `valid-inert-with-proof-history.json`;
- `valid-suspect-observed-failure.json`;
- `invalid-inert-partial-proof-history.json`; and
- `invalid-suspect-without-observed-failure.json`.

The authoritative executable surface is the checked-in schema, verifier, tests,
and examples. Preserve the original RED/GREEN chronology below as implementation
history; do not use an earlier code excerpt to weaken the final carrier.

'''
    insert_before_once(WATCH_PLAN, "## File structure\n", watch_amendment)

    practical_amendment = r'''#### Hardened commission carrier requirements

The adapter must preserve the distinction between current state and historical
proof. It never synthesizes or strips evidence fields:

- every adapter claim returns a durable receipt reference;
- `INERT` can retain a complete prior proof after deliberate disablement;
- `PROVEN` is accepted only from the upstream semantic verifier and only while
  the external mechanism remains enabled;
- `SUSPECT` carries a later observed failure kind, detail, time, and receipt;
- a missing verifier leaves the external contract unverified; and
- revocation/disablement changes current state without rewriting prior proof
  evidence.

Tests must round-trip all four dedicated fixtures from `epistemic-skills`:
valid proven, valid inert-with-proof-history, valid suspect-observed-failure, and
valid blocked-no-substrate. Also prove rejection of self-asserted skill
persistence and partial proof history.

'''
    insert_before_once(PRACTICAL_PLAN, "- [ ] **Step 1: Write failing integration tests**\n", practical_amendment)

    print("watch contract design and plans aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
