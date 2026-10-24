# watch trigger-and-scope fixtures

This battery tests the trigger discipline and the commission-state scope
contract: watch fires when a bound matters between agent runs and nothing
currently observes it; when the first natural symptom would otherwise be an
outage, loss, or material degradation; when someone is about to infer from a
green health readout that they would be told if the condition changed; when
an external observer exists but has never completed an end-to-end proof; and
when a prior proof is old enough that liveness has become an assumption. It
never fires when the user wants the current state now (that is `health`),
when the bound is already known crossed and the cause is wanted (that is
`triage`), when learning late would change no action, when a human reliably
observes the condition on a cadence shorter than the harm, when the request
is to auto-remediate, or when the only proposed "mechanism" is the skill or
the current agent session. A fired commission reports exactly one current
state — `DECLARED`, `BLOCKED`, `INERT`, `PROVEN`, or `SUSPECT` — under the
state-shape rules in the contract below: a missing or unproven dependency is
an evidence-bearing `BLOCKED` with a reason from the closed vocabulary, a
`PROVEN` carries a complete production-path proof with a re-proof boundary,
an `INERT` that follows a completed proof retains that proof as history, and
a `SUSPECT` rests on an observed, receipted failure — never on possible
failure modes, silence, or configuration presence. Over-firing and
under-firing are defects, not extra rigor.

## Pinned expectations and coverage limits

Every `commission` fixture pins `expected_state`, and every `BLOCKED`
fixture also pins `expected_block_reason`; the scorer enforces both. No
fire in this battery is shape-only.

One coverage limit, stated here and not only in the program's Wave 1
report: the `INERT` state is exercised only in its proof-then-disabled
variant — a mechanism that completed its proof and was then deliberately
disabled, retaining the proof as history. Watch's `SKILL.md` also permits
an absent-proof `INERT` (persistence and kill switch proven, no proof
crossing ever run); that variant is **unexercised** by this battery, and
no epoch result on this battery says anything about it.

## Claim

A live-epoch pass would support a claim about trigger/scope conformance and
state-shape discipline on declared responses: subjects fire exactly on the
skill's trigger clauses, stay silent on its do-not-fire clauses and at the
neighbouring skills' boundaries, and shape their commission states by the
evidence rules above. It would NOT support any claim that a real observer is
watching, that commissioned observers stay alive or actually alert in the
field, or that commissions become more reliable in operation — the battery
scores declared fire/no-fire decisions and commission fields against
fixtures, not live observer behaviour. Passing it is NOT behavioral proof of
a working watch.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- One response object per fixture, carrying `id` (the fixture's id) and
  `action` naming the **discipline mode that fired**: `commission` (watch
  ran and returns a commission state) or `no-fire`.
- A `no-fire` response is **silent**: it carries `id` and `action` only —
  none of the commission-shape fields may be present at all (`state`,
  `bound`, `substrate_kind`, `destination`, `block_reason`, `block_evidence`,
  `proof`, `failure` are the process artifacts, and silence means their keys
  are absent, not null or false). Do not explain why you did not fire;
  non-events are silent in deployment, so they are silent in trials.
- A `commission` response reports `state` (one of `DECLARED`, `BLOCKED`,
  `INERT`, `PROVEN`, `SUSPECT`); `bound` as an object with `direction` (one
  of `above`, `below`, `equals`, `changes`, `absent`) and `threshold`
  present (any scalar or string); `substrate_kind` (a nonempty string naming
  the external observer kind — a value naming the skill, the session, the
  chat, the prompt, Markdown, or memory is rejected, because the observer
  must be external and persistent); and `destination` (a nonempty string
  naming a reachable recipient or endpoint).
- `BLOCKED` requires `block_reason` from the closed vocabulary —
  `NO_EXECUTION_SUBSTRATE`, `NO_REACHABLE_DESTINATION`,
  `NO_AUTHORITY_TO_ENABLE`, `NO_KILL_SWITCH`, `KILL_SWITCH_UNPROVEN`,
  `NO_SAFE_PROOF_CROSSING`, `PROBE_UNAVAILABLE` — agreeing with the
  fixture's expected reason, AND `block_evidence` as an object with
  `detail`, `observed_at`, and `receipt_ref` all nonempty: the check
  performed, when, and its durable evidence reference. A reason string
  alone does not establish a block.
- `PROVEN` requires `proof` as an object with `production_path: true`,
  `alert_receipt_ref` nonempty, and `reproof_boundary` nonempty: the proof
  crossed through the real probe and delivery path, the alert arrived, and
  the freshness boundary says when or under what condition it must be
  re-proved — a proof with no boundary silently becomes permanent.
- `INERT` (a mechanism that completed its proof and was then deliberately
  disabled) carries the same complete `proof` object as history: the proof
  is retained, not erased, and the state still says the observer is not
  currently watching.
- `SUSPECT` requires `failure` as an object with `kind`, `detail`,
  `observed_at`, and `receipt_ref` all nonempty: a specific observed and
  receipted failure of the mechanism, probe, delivery, proof, kill switch,
  or freshness — possibility is not an incident.
- `DECLARED` claims only that a commission specification exists: bound,
  probe, destination, kill-switch requirement, and proof plan are
  specified, and no external mechanism is yet prepared.
- The trial is a SIMULATION: no mechanisms are prepared, enabled, or
  proof-fired, and no alerts are sent. The deliverable is the response
  object, which reports the commission and state the scenario's stated
  facts support — every fixture's expected action is performable under
  this clause.

## Status

Unrun as of 2026-10-24: no live epoch has run against this battery (see
`results/BLOCKED.md`). Exactly 3 fixtures are holdouts, marked `"holdout":
true` in `fixtures.json` and spread across fire and no-fire fixtures; epoch
runners must not tune against the holdout fixtures.

Run `python tests/run_tests.py`.
