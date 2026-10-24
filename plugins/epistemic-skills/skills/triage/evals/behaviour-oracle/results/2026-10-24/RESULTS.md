# Live behavioral epoch — 2026-10-24 (E6: triage behaviour-oracle first epoch)

**Outcome: FAIL — 4/12 cases pass the deterministic scorer (exit 1).**
Eight named failures, recorded as-is; no re-run. This record supersedes
`results/BLOCKED.md` for this corpus.

## Methodology

Protocol per `docs/evidence-program/PROGRAM-2026-10-24.md` §4 and
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`: one fresh isolated
general-purpose subject per case (N=1), dispatch ordered by opaque
trial key (`sha256(fixture-id)` first 12 hex; mapping in
`dispatch-map.json`, published here after responses were frozen),
subjects read only the skill core (`skills/triage/SKILL.md`) plus
core-directed references, never anything under `evals/`. The pinned
response contract was quoted from the corpus README with prior-epoch
history stripped (this corpus had no prior epoch) and with the
runner-facing holdout bullet removed. Trials were declared
simulations; the shipped `score.py` ran unmodified. Raw extracted
responses in `responses.json`; scorer output in `scorer-report.json`.

Extraction: 12/12 responses were single well-formed JSON objects, no
extraction anomalies, no missing responses.

**Model note (deviation, recorded per dispatch contract §7):** the
preregistration named model family claude-fable-5; subjects in this
harness ran as isolated subagents of the coordinating runtime (model:
Muse Wonder). The same-family caveat applies.

## Results

Verdicts returned: UNKNOWN 8 · NARROWED 2 · CAUSE 1 · NOT-BROKEN 1.

- **PASS (4):** `control-report-wrong-not-broken` (earned NOT-BROKEN on
  a direct rerun), `degraded-lying-readout` (NARROWED with
  `readout_suspect: true` and a three-times reproduction contradicting
  the green dashboard — the sentinel lying-readout case), 
  `clause-readout-named-wrong-cause-unknown` (holdout; UNKNOWN with no
  cause named), and `degraded-subject-unreachable` (UNKNOWN with
  `qualifier: "unreachable"`).
- **FAIL (8):**
  - Six cases returned **UNKNOWN where the corpus expects NARROWED**:
    `clause-check-red-cause-unknown`,
    `clause-observation-contradicts-assertion`,
    `core-plausible-cause-not-observed` (holdout),
    `degraded-no-readout-self-probed`,
    `degraded-fault-not-reproducible` (holdout),
    `degraded-observation-would-be-destructive`. Characterisation:
    **(a) conduct** — verdict strength one step too weak, all six.
    The pattern is systematic, not scattered: on three of the six the
    subject produced the corpus's correct degraded-operation labels
    (`evidence_basis: "self-probed"`,
    `not_reproducible_stated: true`,
    `observation_plan: "safe-alternative"`) and still paired them
    with UNKNOWN. The corpus's semantics — a probe result in hand, a
    candidate field identified, or a fault confirmed real with its
    cause open is a *narrowed* field, not an unknown one — were not
    the verdicts the subjects reached. Notably, no subject converted
    plausibility into a cause anywhere in this epoch: the failure
    mode is over-restraint, the mirror image of the overclaiming the
    corpus was built to catch.
  - `clause-known-broken-eliminates-one` — the subject returned
    NARROWED with the eliminating observation stated, but listed the
    eliminated candidate as the scenario's letter label `"b"` where
    the corpus pins the candidate name (`connection pool exhausted`).
    Characterisation: **(b) reporting shape over correct conduct.**
  - `control-discriminating-observation-cause` — the subject named the
    cause as "application-side publish failure: serialization error on
    the new schema field added by the deploy", with the correct
    discriminating observation and both rival eliminations, where the
    corpus pins the phrasing "application publish path rejects the new
    schema field". Characterisation: **(b) reporting shape over
    correct conduct** (naming form diverged; the identification was
    substantively the planted cause).

## Holdout line

Holdout cases: `clause-readout-named-wrong-cause-unknown` PASS;
`core-plausible-cause-not-observed` FAIL and
`degraded-fault-not-reproducible` FAIL (both in the NARROWED/UNKNOWN
pattern above). 1/3 pass, reported separately per the preregistration;
no dispatch text was tuned against them.

## Reading (within the preregistered claim fence)

On planted evidence states, the returned verdict was the one the
evidence supports in 4 of 12 cases. The corpus's central prohibition
held everywhere — plausibility was never converted into cause — but
its positive discipline did not: where evidence had narrowed the
field, subjects declared UNKNOWN instead of NARROWED in six of seven
such cases (the seventh, the lying-readout case, was handled exactly
as the corpus prescribes). This is conformance evidence about declared
verdicts on planted states only; it supports no claim about field
diagnostic accuracy or repair correctness.

## Honest limits

N=1 per case, one harness, single repetition; smoke-scale conformance
evidence, not a population rate. Declared-response scoring against
described evidence (simulation clause), not perception of real
evidence.

## Correction (2026-10-24, post-epoch)

Review (Codex P2 on PR #273) established an instrument defect in two
of the eight recorded failures, and this section amends the
interpretation above. The record of responses and the epoch outcome
(**FAIL — 4/12**) are unmodified.

Two of the six cases characterised above as "(a) conduct — verdict
strength one step too weak" were pinned against a ground truth the
corpus's own verdict definitions do not support. NARROWED means some
candidates were eliminated *by an observation*. In
`clause-check-red-cause-unknown` no test had been run and no component
isolated; in `degraded-observation-would-be-destructive` the safe
observation is proposed, not performed, and the decisive one is held
for authority. No eliminating observation occurs in either scenario;
the supported verdict is UNKNOWN — which is what both subjects
returned. For these two cases the (a) characterisation is **withdrawn**:
the failures were the fixture's, not the subjects'. The remaining four
UNKNOWN-where-NARROWED cases (`clause-observation-contradicts-assertion`,
`core-plausible-cause-not-observed`, `degraded-no-readout-self-probed`,
`degraded-fault-not-reproducible`) stand as recorded.

The corrected fixtures apply to future epochs. A subordinate re-score
of the frozen responses under the corrected ground truths is recorded
in `rescore/` in this directory (6/12; the epoch verdict is not
replaced). The same correction cycle also disclosed, in the two
affected scenarios, the canonical cause/candidate labels the scorer
pins exactly (`control-discriminating-observation-cause`,
`clause-known-broken-eliminates-one`): the epoch's two (b) naming
failures were recorded against strings the dispatched scenarios never
supplied, and are instrument-attributable in that specific respect —
see the battery revision note in the corpus README.
