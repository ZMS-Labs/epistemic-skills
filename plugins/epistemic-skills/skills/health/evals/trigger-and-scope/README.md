# health trigger-and-scope fixtures

This battery tests the trigger discipline and the readout scope contract
of Health: a request for the current state of a running system — "is
everything OK", a before-picture for a change with real blast radius, a
readout after a restart or power event, a health claim about to bear
load, or something feeling wrong with the subject unnamed — fires a
readout; a subject already known broken whose cause is wanted (that is
triage, which consumes this output), a single metric readable with one
command, a question about a change being made rather than the state the
system is in, and a routine reversible task touching nothing shared never
fire. On firing fixtures the battery plants each degradation the skill
names — subject unreachable, credential failure, probe tool absent,
bound undeclared, registry unreachable — and asserts the readout reports
`UNKNOWN` for it and does not report `OK`. Over-firing and under-firing
are defects, not extra rigor.

## Pinned expectations

Every `readout` fixture pins `expected_subjects` — the per-subject states
the scenario's stated probe outcomes determine — and the roll-up follows
from them by the aggregation rule. No fire in this battery is shape-only.

## Revision — canonical subject names stated in the scenarios (2026-10-24, issue #278)

The first live epoch (E4, `results/2026-10-24/`) failed 10/13 on one
mechanism, diagnosed in its record as a battery-design defect: subjects
reported the probe-determined states and the UNKNOWN rollup exactly
right but named the degraded subjects as the scenario prose names them
("backup system", "metrics pipeline", "storage pool"), where
`expected_subjects` pins short canonical names ("backup", "metrics",
"storage") the scenarios never stated — the scorer penalised the
scenario's own naming. The FAIL stands as scored, against the battery
revision that produced it.

This revision applies the epoch record's own prescription: every
readout scenario now states the battery's naming convention and the
canonical names for its subjects, in the same form the
`registry-unreachable-coverage-unknown` fixture already used for
`registry-coverage`. Nothing else changed — the scorer, the pinned
states, the roll-up expectations, the clause texts, and the holdout set
are untouched, and the health SKILL is unchanged. The revised battery
has **no live epoch yet**: any claim from it awaits a fresh
preregistered epoch, and no E4 result transfers to this revision.

## Claim

A live-epoch pass on this battery would support one claim only: that the
subject's *declared* fire/no-fire decisions and readout shape — per-subject
states, the aggregation rule, and the subject ordering — conform to the
skill's trigger and scope text on these fixtures, whose scenarios state
their probe outcomes so the correct states are determined. It would NOT
support any claim that a live readout probed the right systems, that
acting on a readout improved an outcome, or that the skill helps in live
work; outcome improvement is a different claim needing different
evidence. The synthetic example traces under `examples/` are
scorer-discrimination evidence only.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch (per
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: the pinned contract travels
verbatim with vocabularies inline, and silence semantics are explicit):

- `action` names the **discipline mode that fired**: `readout` (a health
  readout was produced) or `no-fire`.
- A `no-fire` response is **silent**: it carries `id` and `action` only —
  no `subjects`, no `rollup`, no `ordered_subjects`, no other field at
  all. Absence is not an artifact; a process field present on a silent
  response is scored as over-firing, not generosity.
- A `readout` response reports:
  - `subjects` — a nonempty array of `{"name", "state"}` objects, one per
    probed subject, where `state` is exactly one of `OK`, `WARN`,
    `CRITICAL`, `UNKNOWN`. `OK` requires a completed probe AND a declared
    bound; a subject that could not be probed — unreachable, credential
    failure, probe tool absent, timeout — or whose bound is undeclared
    is `UNKNOWN`, never `OK` and never omitted.
  - `rollup` — exactly one of `OK`, `WARN`, `CRITICAL`, `UNKNOWN`,
    aggregated by the skill's rule: if any subject is `CRITICAL`, the
    rollup is `CRITICAL`; otherwise, if any subject is `UNKNOWN`, the
    rollup is `UNKNOWN` (a roll-up containing `UNKNOWN` is at best
    `UNKNOWN` for that branch — absence of evidence is not health);
    otherwise, if any subject is `WARN`, the rollup is `WARN`; the
    rollup is `OK` only when every subject is `OK`.
  - `ordered_subjects` — an array naming every subject exactly once (a
    permutation of the `subjects` names), ordered `CRITICAL` first, then
    `UNKNOWN`, then `WARN`, then `OK`; subjects in the same state keep
    fixture order.
- Where a fixture carries `expected_subjects` — the exact name-to-state
  map its stated probe outcomes determine — the row's `subjects` must
  match it exactly. A planted degradation reported as any other state,
  in particular as `OK`, fails.
- Registry convention: when the subject registry is unreachable and
  coverage cannot be established, the unestablished coverage is
  represented as a subject named `registry-coverage` with state
  `UNKNOWN`, alongside any named subjects that were actually probed.

## Status

Unrun as of 2026-10-24: no live epoch has been run against these
fixtures. Three fixtures are marked `"holdout": true` in `fixtures.json`
(`credential-failure-unknown`, `registry-unreachable-coverage-unknown`,
`one-metric-one-command-no-fire`); epoch runners must not tune against
the holdout fixtures.
