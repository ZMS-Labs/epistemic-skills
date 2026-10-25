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

**Further correction (2026-10-24, post-epoch).** One of the four
cases named above as standing — `degraded-no-readout-self-probed` —
carries the identical defect, established by a follow-up adjudication
applying the same principle (the case was also named in Codex's
finding on PR #281's thread). The fixture pinned NARROWED with
`expected_eliminated: []`, and its scenario states that nothing
distinguishes a full disk, a permissions change, or a storage-backend
outage: the single minimal probe — a test export failing with a
storage-write error — eliminates no candidate. The supported verdict
is UNKNOWN, which is what the subject returned, with the
`evidence_basis: "self-probed"` label the fixture requires. For this
case too the (a) characterisation is **withdrawn**: the failure was
the fixture's, not the subject's. Three UNKNOWN-where-NARROWED cases
now stand as recorded: `clause-observation-contradicts-assertion`,
`core-plausible-cause-not-observed`, and
`degraded-fault-not-reproducible`. The fixture is re-pinned for
future epochs, and the subordinate re-score in `rescore/` has been
extended to all three corrected fixtures (**7/12**; the epoch
verdict is not replaced).

**Further correction (2026-10-24, second adjudication round).** Dot's
review of the held branches re-raised the NARROWED/UNKNOWN
inconsistency, and a full audit of the corpus's remaining NARROWED
pins against the principle applied above — NARROWED requires at least
one candidate eliminated by the scenario's stated evidence — found
two more mis-pins among the three cases the earlier corrections left
standing. In `clause-observation-contradicts-assertion` the direct
query is consistent with every candidate explanation of the
disagreement, including the replica candidate under which the primary
queue drains normally; no candidate is eliminated. In
`core-plausible-cause-not-observed` the scenario states the
investigator made no observation that would come out differently
under one candidate than the others; no candidate is eliminated. For
both cases the (a) characterisation is **withdrawn**: the failures
were the fixtures', not the subjects' — both subjects returned the
supported verdict, UNKNOWN. The fixtures are re-pinned for future
epochs. Of the six UNKNOWN-where-NARROWED cases in the original
record, exactly one now stands as (a) conduct:
`degraded-fault-not-reproducible` (holdout), whose eleven clean
reloads eliminate the persistent-fault candidate and whose class the
skill's degraded-operation table caps at NARROWED. The holdout line
above is amended accordingly: `core-plausible-cause-not-observed`
moves from FAIL-as-conduct to instrument-attributable. The audit also
adjudicated `degraded-lying-readout` (a PASS in this epoch): its
direct reproduction eliminates the no-fault candidate, so its
NARROWED pin stands. The subordinate re-score in `rescore/` has been
regenerated against all five corrected fixtures (**9/12**; the epoch
verdict is not replaced).
