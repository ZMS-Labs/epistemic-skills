#!/usr/bin/env python3
"""Align design and implementation plans with the final watch carrier.

This branch-scoped helper performs only exact, uniquely anchored replacements.
It is removed after the generated documentation commit passes repository checks.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-08-07-practical-agency-and-commission-watch-design.md"
WATCH_PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-08-07-commission-watch-clarification.md"
PRACTICAL_PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-08-07-practical-agency-bootstrap.md"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one source match, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def replace_region(path: Path, start: str, end: str, replacement: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(start) != 1 or text.count(end) != 1:
        raise SystemExit(
            f"{path}: expected unique region markers; start={text.count(start)} end={text.count(end)}"
        )
    left, remainder = text.split(start, 1)
    _, right = remainder.split(end, 1)
    path.write_text(left + replacement + end + right, encoding="utf-8")


def main() -> int:
    replace_once(
        DESIGN,
        "The carrier separates four facts that must never be collapsed:",
        "The carrier separates five facts that must never be collapsed:",
    )
    replace_once(
        DESIGN,
        """3. **positive-claim evidence** — durable references supporting reachability,
   external persistence, kill-switch exercise, proof authority, and alert
   receipt; and
4. **observed failure** — a separately typed, timestamped, receipted incident
   used only when current state is `SUSPECT`.
""",
        """3. **positive-claim evidence** — durable references supporting reachability,
   external persistence, kill-switch exercise, proof authority, and alert
   receipt;
4. **block evidence** — the checked missing or unproven dependency, observation
   time, and external receipt used only when current state is `BLOCKED`; and
5. **observed failure** — a separately typed, timestamped, receipted incident
   used only when current state is `SUSPECT`.
""",
    )
    replace_once(
        DESIGN,
        """failure:
  kind: probe|delivery|proof|freshness|kill-switch|external-mechanism|unknown|null
  detail: <observed failure or null>
  observed_at: <timestamp or null>
  receipt_ref: <durable evidence ref or null>
state: DECLARED|BLOCKED|INERT|PROVEN|SUSPECT
""",
        """failure:
  kind: probe|delivery|proof|freshness|kill-switch|external-mechanism|unknown|null
  detail: <observed failure or null>
  observed_at: <timestamp or null>
  receipt_ref: <durable evidence ref or null>
block_evidence:
  detail: <checked missing or unproven dependency, or null>
  observed_at: <timestamp or null>
  receipt_ref: <durable external check ref or null>
state: DECLARED|BLOCKED|INERT|PROVEN|SUSPECT
""",
    )
    replace_once(
        DESIGN,
        "| `BLOCKED` | A required dependency is absent, the closed reason agrees with the recorded fields, and the observer remains disabled. |",
        "| `BLOCKED` | A required dependency was checked and found absent or unproven, the reason agrees with the recorded fields, dated block evidence exists, and the observer remains disabled. |",
    )
    replace_once(
        DESIGN,
        """`state` reports the observer now. A successful proof followed by deliberate
disablement yields `INERT` with complete proof history retained. It does not stay
`PROVEN`, and the proof is not erased. Partial proof history is invalid because it
manufactures an easy-to-overread intermediate state.
""",
        """`state` reports the observer now. A successful proof followed by deliberate
disablement yields `INERT` with complete proof history retained. It does not stay
`PROVEN`, and the proof is not erased. Partial proof history is invalid because it
manufactures an easy-to-overread intermediate state.

Preparing or deploying a new persistent mechanism does not immediately earn
`INERT`. Until the real disable procedure has stopped that mechanism under
observation, the honest state is `BLOCKED: KILL_SWITCH_UNPROVEN` with dated block
evidence. Successful kill-switch exercise clears the block and yields `INERT`.
A pre-existing mechanism may enter `INERT` directly only when persistence and
kill-switch receipts already exist.
""",
    )
    replace_once(
        DESIGN,
        """The semantic verifier rejects a reason contradicted by the record, such as
`NO_EXECUTION_SUBSTRATE` beside a populated external mechanism and persistence
receipt.
""",
        """The semantic verifier rejects a reason contradicted by the record, such as
`NO_EXECUTION_SUBSTRATE` beside a populated external mechanism and persistence
receipt. Every `BLOCKED` record also requires `block_evidence.detail`,
`block_evidence.observed_at`, and an external `block_evidence.receipt_ref`.
Those fields are empty in all non-blocked states; a reason string or an agent's
unsearched inability to imagine a capability is not evidence of absence.
""",
    )

    final_rules = r'''### Positive-claim, evidence, and promotion rules

A positive boolean never bears load alone:

- `destination.reachable: true` requires `reachability_receipt_ref`;
- `persistent_outside_session: true` requires `persistence_receipt_ref`;
- `kill_switch.exercised: true` requires `exercise_receipt_ref`;
- named proof authority requires `authorization_ref`; and
- `alert_received: true` requires both `received_at` and
  `alert_receipt_ref`.

A `BLOCKED` result likewise requires a dated evidence carrier naming the check
that established the missing or unproven dependency. The reason must agree with
the other fields. In particular, a prepared persistent mechanism whose disable
procedure is not yet exercised is `BLOCKED: KILL_SWITCH_UNPROVEN`, not `INERT`.

Evidence references using self-assertion, prompt/chat/session state, or remembered
model context are refused. An allowed substrate label cannot hide an obvious
`SKILL.md` or other prompt-time mechanism reference. A fixture is permitted only
for isolated contract/proof-path evaluation and must disclose fixture/test scope
and the unestablished production environment in `coverage_limits`.

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
currently disabled and its kill switch is already proven. `SUSPECT` may retain
historical receipts but requires its own later observed-failure carrier.
Configuration presence, source inspection, deployment, formatter tests,
self-asserted persistence, partial proof fields, generic failure possibilities,
bypass messages, and "no alert yet" cannot satisfy these rules.

'''
    replace_region(
        DESIGN,
        "### Positive-claim and promotion rules\n",
        "### Runtime division\n",
        final_rules,
    )

    final_watch_amendment = r'''## As-built contract refinement — normative over the original task sketches

Implementation uncovered state/evidence distinctions the original task-level
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
- `BLOCKED` requires a checked missing or unproven dependency, observation time,
  and external evidence receipt; its closed reason must agree with the record.
- A newly prepared persistent mechanism remains
  `BLOCKED: KILL_SWITCH_UNPROVEN` until the real disable path is exercised and
  receipted. Only then can the disabled mechanism become `INERT`.
- External substrates use a closed type set that excludes Markdown skills and
  prompt/session memory even when mislabeled or self-asserted as persistent.
- Fixture evidence is accepted only with explicit isolated/test scope and a
  statement of the unestablished production coverage.
- `PROVEN` requires a re-proof boundary.
- `SUSPECT` requires an observed failure kind, detail, time, and receipt; possible
  failure modes alone are not an incident.

Additional committed fixtures are required:

- `valid-inert-with-proof-history.json`;
- `valid-suspect-observed-failure.json`;
- `valid-blocked-kill-switch-unproven.json`;
- `invalid-inert-partial-proof-history.json`; and
- `invalid-suspect-without-observed-failure.json`.

The authoritative executable surface is the checked-in schema, verifier, tests,
and examples. Preserve the original RED/GREEN chronology below as implementation
history; do not use an earlier code excerpt to weaken the final carrier.

'''
    replace_region(
        WATCH_PLAN,
        "## As-built contract refinement — normative over the original task sketches\n",
        "## File structure\n",
        final_watch_amendment,
    )

    final_adapter = r'''#### Hardened commission carrier requirements

The adapter must preserve the distinction among current state, historical proof,
block evidence, and later observed failure. It never synthesizes, strips, or
reinterprets evidence fields:

- every adapter claim returns a durable external receipt reference;
- a missing or unproven dependency returns dated `block_evidence` as well as the
  closed `block_reason`;
- preparing a disabled external mechanism yields
  `BLOCKED: KILL_SWITCH_UNPROVEN` until `exercise_kill_switch` returns a verified
  receipt; only then may the adapter request `INERT`;
- `INERT` can retain a complete prior proof after deliberate disablement;
- `PROVEN` is accepted only from the upstream semantic verifier and only while
  the external mechanism remains enabled;
- `SUSPECT` carries a later observed failure kind, detail, time, and receipt;
- prompt/chat/session artifacts and self-asserted receipt references are refused;
- fixture adapters explicitly identify isolated scope and unestablished
  production coverage;
- a missing verifier leaves the external contract unverified; and
- revocation/disablement changes current state without rewriting prior proof or
  block evidence.

Tests must round-trip the dedicated upstream fixtures: valid proven, valid
inert-with-proof-history, valid suspect-observed-failure, valid
blocked-no-substrate, and valid blocked-kill-switch-unproven. Also prove rejection
of self-asserted skill persistence, missing block evidence, undeclared fixture
scope, and partial proof history.

'''
    replace_region(
        PRACTICAL_PLAN,
        "#### Hardened commission carrier requirements\n",
        "- [ ] **Step 1: Write failing integration tests**\n",
        final_adapter,
    )
    replace_once(
        PRACTICAL_PLAN,
        "- a `DECLARED` commission can be prepared `INERT` only through an adapter receipt;",
        "- a prepared external mechanism remains `BLOCKED: KILL_SWITCH_UNPROVEN` until the adapter returns a verified kill-switch receipt, then becomes `INERT`;",
    )
    replace_once(
        PRACTICAL_PLAN,
        "    def prepare_inert(self, commission: Mapping[str, Any]) -> Mapping[str, Any]: ...",
        "    def prepare_disabled(self, commission: Mapping[str, Any]) -> Mapping[str, Any]: ...",
    )
    replace_once(
        PRACTICAL_PLAN,
        "The example contains a mission whose desired state is a proven external disk-space alert. It begins with `watch_commissions` containing `BLOCKED/NO_EXECUTION_SUBSTRATE`, demonstrating honest degradation rather than fabricated persistence.",
        "The example contains a mission whose desired state is a proven external disk-space alert. It begins with `watch_commissions` containing `BLOCKED/NO_EXECUTION_SUBSTRATE` plus dated discovery evidence, demonstrating honest degradation rather than fabricated persistence. A second transition fixture prepares a mechanism as `BLOCKED/KILL_SWITCH_UNPROVEN` and reaches `INERT` only after a verified kill-switch receipt.",
    )

    print("final watch contract documentation aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
