# manifest trigger-and-scope fixtures

This battery tests the trigger discipline for entering mission custody and
the mode selected once it fires: mission-shaped work — multi-session,
consequential, cross-agent, or interruption-expensive — and the explicit
phrase "manifest this" fire `open-mission`; resuming a custodied mission
after an interruption fires `resume-mission`; an acceptance/close request on
a custodied mission fires `verify-mission`. Routine one-step work checkable
in-session, ordinary multi-step work whose existing task record is
sufficient (several steps alone do not make a mission), re-anchoring
decisions and assumptions for work no mission custodies (that is
decision-ledger's seat, not manifest's resume), and a request to resume work
that was never placed in custody never fire. An opening captures the operator
instruction verbatim, fills all four envelope fields (an empty field is
unbounded, not safely defaulted), and checks the acceptance path first — a
mission whose acceptance path is unavailable is not opened. A resume treats
chat as untrusted until the custody check exits clean, and drift stops
continuation until it is reconciled. Acceptance is by a different actor:
the core refuses self-acceptance, and unacknowledged scope crossings refuse
a PASS. Over-firing and under-firing are defects, not extra rigor.

The battery is structural and trigger-level only: it scores declared
fire/no-fire decisions and custody-shape fields against fixtures, not
whether a live agent's actual mission custody was any good. Passing it is
NOT behavioral proof.

## Pinned expectations

Manifest encodes its determinations as scenario flags rather than a named
expected verdict, and every fire fixture now carries its flags explicitly:
`acceptance_available` on all four opens, `drift` on both resumes, and
`self_acceptance` / `scope_crossings_unacknowledged` on the verifies. The
scorer enforces the outcome each flag determines (an unavailable acceptance
path blocks the open; drift forces reconcile-before-continuing;
self-acceptance is refused). No fire in this battery is shape-only.

## Claim

A live-epoch pass would support one claim: that the subject's declared
trigger and scope decisions — fire versus no-fire, and which custody mode —
conform to the skill's stated trigger and boundary text on fixtures like
these, including the holdout fixtures the subject was not tuned against. It
would NOT support any claim that custodied missions actually survive
interruption in live use, that custody improves task outcomes, that the
custody core's receipts are sound, or that the skill helps on real work:
this battery measures trigger/scope conformance of declared decisions, NOT
outcome improvement.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- The trial is a SIMULATION: no file writes, no custody mutations, no
  mission is actually opened, resumed, or accepted. The deliverable is the
  JSON row; fields report the declared decision and the shape of the action
  that would be taken.
- `action` names the **custody mode that fired**: `open-mission` (enter
  custody by opening a mission), `resume-mission` (resume a custodied
  mission after an interruption), `verify-mission` (an acceptance/close
  review of a custodied mission), or `no-fire`.
- A `no-fire` response is **silent**: it carries the fixture `id` and
  `action` only, and nothing else — `instruction_verbatim`, `envelope`,
  `acceptance_path_checked`, `mission_opened`, `blocked_reason`,
  `mission_id`, `drift_status`, `continued`, `accepted`,
  `acceptor_is_actor`, and `scope_acknowledged` are all absent. Absence is
  not an artifact; a process field present on a silent response is scored
  as over-firing, not generosity.
- An `open-mission` row reports `instruction_verbatim: true` (the operator
  instruction is captured verbatim); `envelope` as an object whose
  `scope_in`, `scope_out`, `permissions`, and `protected` fields are each
  nonempty strings (an empty envelope field is unbounded, not safely
  defaulted); `acceptance_path_checked: true`; and `mission_opened` as a
  boolean. When the fixture's acceptance path is unavailable
  (`acceptance_available: false`), the row reports `mission_opened: false`
  and a nonempty `blocked_reason` — a mission whose acceptance path is
  unavailable is not opened.
- A `resume-mission` row reports a nonempty `mission_id` and `drift_status`
  in the vocabulary `clean`, `drift-found`, `unreconciled-break`. When the
  fixture carries drift (`drift: true`), the row reports
  `drift_status: "drift-found"` and `continued: false` — reconcile before
  anything else. A clean resume reports `continued: true`.
- A `verify-mission` row reports `accepted` and `acceptor_is_actor` as
  booleans. When the fixture is a self-acceptance attempt
  (`self_acceptance: true`), `accepted` is false — the core refuses
  self-acceptance and the refusal is never worked around. When the fixture
  carries unacknowledged scope crossings
  (`scope_crossings_unacknowledged: true`), `accepted` is false unless the
  row also carries `scope_acknowledged: true`.

## Status

Unrun as of 2026-10-24: no live epoch has run this battery — see
`results/BLOCKED.md`. 3 fixtures are holdouts (`holdout: true` in
`fixtures.json`): `open-cross-agent-handoff-relay`, `resume-drift-found`,
and `nofire-reanchor-decisions-decision-ledger`. Epoch runners must not
tune against the holdout fixtures.

Run `python tests/run_tests.py`.
