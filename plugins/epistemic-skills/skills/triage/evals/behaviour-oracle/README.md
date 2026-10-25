# triage behaviour-oracle corpus

Triage's `SKILL.md` Oracle section specifies this corpus: one planted case
per trigger clause and per degraded-operation row, asserting the verdict
the planted evidence state supports — including the assertion a naive
suite omits, that the run does **not** name the most plausible candidate
as the cause when no discriminating observation was made. This directory
ships that corpus. The trigger-and-scope battery in
`../trigger-and-scope/` tests whether triage fires at all; this corpus
tests what verdict it returns when it does.

Two classes were already covered in abstract form by the shipped
sentinels, which this corpus builds around rather than duplicates:
`contracts/epistemic-events/sentinels/triage-plausible-not-observed.json`
(plausible cause, no discriminating observation) and
`triage-lying-readout.json` (readout healthy, failure reproduced), plus
the operational response controls in `operational-scenarios.json`. The
cases here are concrete scenario instances with determined verdicts,
including fresh instances of both sentinel classes
(`core-plausible-cause-not-observed`, `degraded-lying-readout`).

Coverage: the four trigger clauses (known-broken, check-red,
readout-named-wrong, observation-contradicts-assertion); the five
degraded-operation rows (no readout → self-probed label; unreachable →
`UNKNOWN (unreachable)`; not reproducible → stated explicitly, `NARROWED`
at best; destructive observation → safe alternative or held for authority;
suspect readout → becomes the subject); the plausible-cause core case;
and two positive controls — a discriminating observation that earns
`CAUSE`, and a report that direct observation shows was wrong
(`NOT-BROKEN`). A corpus that only punished overclaiming would teach
blanket `UNKNOWN`; the controls exist so the scorer rewards earned
verdicts too.

## Pinned expectations

Every case pins `expected_verdict`, and the positive control pins
`expected_cause`; the scorer also enforces the forbidden-cause and
eliminated-candidate fields. No case in this corpus is shape-only.

## Claim

A live-epoch pass on this corpus would support: on planted scenarios with
determined evidence states, an agent applying triage returns the verdict
the evidence supports and does not convert plausibility into cause. It
would NOT support: that field diagnoses become more accurate, that the
verdict vocabulary transfers to unplanted failures, or that any repair
that follows is correct. This is behaviour conformance against planted
states — a step above trigger conformance, below outcome evidence.

## Live-epoch response contract

Pinned before the first live epoch, per
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`:

- Each response is one object per fixture: `id`, `verdict` (exactly one of
  `CAUSE`, `NARROWED`, `UNKNOWN`, `NOT-BROKEN`), `named_cause` (the cause
  named as established — required for `CAUSE`, and **null for `NARROWED`
  and `UNKNOWN`**: a candidate that merely fits the symptom is a
  hypothesis, and naming it as the cause is the failure this corpus
  plants), `discriminating_observation` (the observation that would have
  come out differently under an alternative — required nonempty for
  `CAUSE` and `NOT-BROKEN`), `eliminated` (array of bare candidate ids
  eliminated, with the eliminating observation being the one named above).
- Degraded cases carry their labels: `evidence_basis: "self-probed"` when
  no readout existed; `qualifier: "unreachable"` on an unreachable
  `UNKNOWN`; `not_reproducible_stated: true` when the fault could not be
  reproduced; `readout_suspect: true` when the readout is the subject;
  `observation_plan` (one of `safe-alternative`, `held-for-authority`)
  when the decisive observation would be destructive.
- Three fixtures are marked `"holdout": true`. Epoch runners must not
  tune prompts, skills, or dispatch text against them; they are scored
  with the rest and reported separately in the epoch record.

## Battery revision (2026-10-24, post-E6)

Two defects found by review after the first live epoch (E6), corrected
here for future epochs; expected values otherwise unchanged:

1. **Undisclosed exact strings.** The positive control pinned
   `expected_cause` and `clause-known-broken-eliminates-one` pinned
   `expected_eliminated` as exact strings the dispatched scenarios
   never supplied, so the scorer measured guessing a hidden label as
   much as causal identification. Both scenarios now disclose the
   canonical labels a response must use (the cause label for the
   control; the candidate labels (a)/(b)/(c) for the known-broken
   case), in the same way the health battery's scenarios state their
   canonical subject names.
2. **Five ground truths corrected.** `clause-check-red-cause-unknown`
   and `degraded-observation-would-be-destructive` were re-pinned from
   NARROWED to UNKNOWN: neither scenario contains an observation that
   eliminates any candidate, and under the verdict definitions
   NARROWED requires one. `degraded-no-readout-self-probed` was
   re-pinned in the same cycle on the identical ground: it pinned
   NARROWED with `expected_eliminated: []`, and its scenario states
   nothing distinguishes the candidates. A second adjudication round
   in the same cycle applied the principle to the two remaining
   NARROWED pins with no eliminating observation and re-pinned both:
   `clause-observation-contradicts-assertion` (the direct query is
   consistent with every candidate explanation of the disagreement,
   including the replica candidate under which the primary queue
   drains normally) and `core-plausible-cause-not-observed` (its
   scenario states no observation was made that would come out
   differently under one candidate than the others). The two surviving
   NARROWED pins with `expected_eliminated: []` were adjudicated, not
   overlooked: `degraded-lying-readout`'s direct reproduction
   eliminates the no-fault candidate, and
   `degraded-fault-not-reproducible`'s eleven clean reloads eliminate
   the persistent-fault candidate (the skill's degraded-operation
   table caps that class at NARROWED). See the corrections appended
   to the E6 epoch record and the subordinate re-score under
   `results/2026-10-24/rescore/`.

The committed E6 epoch ran under the **prior** revision. Its five
mis-pinned verdict failures and its exact-string naming failures are
instrument-attributable as detailed in those corrections; no E6 verdict
was re-issued — the re-score is a separate, subordinate record.

## Status

Unrun as of 2026-10-24: no live epoch has run against this corpus. The
synthetic examples (`examples/balanced.json`, `overclaiming.json`,
`underclaiming.json`) prove scorer discrimination only — the scorer
passes a correct response set and fails both parody directions. See
`results/BLOCKED.md`.

Run `python tests/run_tests.py`.
