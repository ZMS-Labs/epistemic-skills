# triage trigger-and-scope fixtures

This battery tests the trigger discipline and the verdict scope contract:
triage fires when a specific subject is known broken, degraded, or behaving
unexpectedly; when a check went red, a deploy failed, or a service is
unreachable; when a state readout named something wrong and the cause is not
yet known; and when an observation contradicts what a tool or document
asserts. It never fires when you do not yet know whether anything is wrong
(that is a health readout, and triage consumes its output), when the cause is
already established and the remedy is being applied, when the question is
about a change being made rather than a failure faced (including checking
that a change landed — `did-it-land`'s question), or when the fault is
deterministic and reproducible and one read of the error settles it. A
request to commission future noticing between sessions is `watch`'s
question, not a failure investigation. A fired investigation returns exactly
one of the four verdicts — `CAUSE`, `NARROWED`, `UNKNOWN`, `NOT-BROKEN` —
under the verdict-shape rules in the contract below: a `CAUSE` is earned
only by a discriminating observation, an `UNKNOWN` is never dressed up as a
most-likely cause, a `NARROWED` names what was eliminated and establishes no
cause, and a `NOT-BROKEN` rests on adequate direct observation of the
reported behaviour. The fixture's evidence state determines the expected
verdict, so a plausible story that fits the symptom scores as a failure.
Over-firing and under-firing are defects, not extra rigor.

## Pinned expectations

Every `investigate` fixture pins `expected_verdict` (CAUSE ×2, NARROWED
×2, UNKNOWN ×2, NOT-BROKEN ×1), and the scorer enforces it. No fire in
this battery is shape-only.

## Claim

A live-epoch pass would support a claim about trigger/scope conformance and
verdict-shape discipline on declared responses: subjects fire exactly on the
skill's trigger clauses, stay silent on its do-not-fire clauses and at the
neighbouring skills' boundaries, and shape their verdicts by the observation
rules above. It would NOT support any claim that diagnoses become more
accurate in the field, that the named causes are the real causes in live
incidents, that providers were actually used as claimed outside the trial,
or that repairs succeed — the battery scores declared fire/no-fire decisions
and verdict fields against fixtures, not live diagnostic outcomes. Passing
it is NOT behavioral proof of better diagnosis.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- One response object per fixture, carrying `id` (the fixture's id) and
  `action` naming the **discipline mode that fired**: `investigate` (triage
  ran an investigation and returns a verdict) or `no-fire`.
- A `no-fire` response is **silent**: it carries `id` and `action` only —
  none of the verdict-shape fields may be present at all (`verdict`,
  `discriminating_observation`, `named_cause`, `provider`, `eliminated` are
  the process artifacts, and silence means their keys are absent, not null
  or false). Do not explain why you did not fire; non-events are silent in
  deployment, so they are silent in trials.
- An `investigate` response reports `verdict` (one of `CAUSE`, `NARROWED`,
  `UNKNOWN`, `NOT-BROKEN`), `discriminating_observation` (a string or
  null), `named_cause` (a string or null), and `provider` (a nonempty string
  naming the investigation method actually used, e.g.
  `superpowers-systematic-debugging` or `standalone-debugging` — claiming a
  provider matters, and a provider that was not used must not be claimed).
  `eliminated` appears as an array of strings naming what was eliminated,
  and is required on `NARROWED` rows.
- `CAUSE` requires `discriminating_observation` nonempty AND `named_cause`
  nonempty: the observation is one that would have come out differently if
  the cause were something else, and it rules the alternatives out.
- `UNKNOWN` requires `named_cause` null or absent: a cause that could not
  be observed is never dressed up as a most-likely cause, and an unreachable
  subject is `UNKNOWN`, never inferred as the fault. It must not name
  eliminated candidates either: an elimination claims an observation that
  rules a candidate out, and `UNKNOWN` is the verdict for insufficient
  evidence to eliminate. An observation that eliminates nothing remains
  compatible with `UNKNOWN`, so `discriminating_observation` is not barred.
- `NARROWED` requires the `eliminated` array present, a nonempty
  `discriminating_observation`, and `named_cause` null: the observation is
  the one that eliminated a candidate — a narrowing with no eliminating
  observation is `UNKNOWN` — and a narrowed candidate is not an established
  cause, however plausible.
- `NOT-BROKEN` requires `discriminating_observation` nonempty and
  `named_cause` null or absent: an adequate direct observation of the
  reported behaviour itself, not a generic healthy readout; naming a cause
  asserts a fault, and the verdict is that there is none.
- The trial is a SIMULATION: no probes, no file writes, no mutations. The
  deliverable is the response object, which reports the investigation and
  verdict the scenario's stated evidence state supports — every fixture's
  expected action is performable under this clause.

## Status

Unrun as of 2026-10-24: no live epoch has run against this battery (see
`results/BLOCKED.md`). Exactly 3 fixtures are holdouts, marked `"holdout":
true` in `fixtures.json` and spread across fire and no-fire fixtures; epoch
runners must not tune against the holdout fixtures.

Run `python tests/run_tests.py`.
