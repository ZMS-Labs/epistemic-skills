# Re-score of E6's frozen responses — corrected ground truths (2026-10-24)

**What this record is.** After E6 closed, review (Codex P2 on PR #273)
established that two fixtures pinned a ground truth triage's own verdict
definitions do not support. `clause-check-red-cause-unknown` and
`degraded-observation-would-be-destructive` expected **NARROWED**, but
NARROWED means some candidates were *eliminated by an observation*, and
in neither scenario does any eliminating observation occur — in the
first, no test had been run and nothing isolated; in the second, the
safe observation is only proposed, not performed, and the decisive one
is held for authority. The supported verdict in both is **UNKNOWN**.
The fixtures have been corrected for future epochs; this directory
records the shipped scorer's reading of E6's **preserved frozen
responses** (`../responses.json`) under the corrected fixtures — run
once, unmodified responses, scorer code unmodified, no new subjects,
no re-dispatch.

**Third correction (2026-10-24, follow-up adjudication).** The
identical defect was subsequently established in a third fixture,
`degraded-no-readout-self-probed` — also named in Codex's finding on
PR #281's thread. It pinned **NARROWED** with
`expected_eliminated: []`, and its scenario states outright that
nothing distinguishes the three live candidates — a full disk, a
permissions change, a storage-backend outage: the one minimal probe
(a test export failing with a storage-write error) is consistent
with all three and eliminates none. The supported verdict is
**UNKNOWN**, which is what the subject returned, with the
`evidence_basis: "self-probed"` label the fixture requires. The
fixture has likewise been re-pinned for future epochs, and the
re-score below was regenerated once against the fully corrected
fixtures — the same preserved responses, the same unmodified
scorer — so this record now covers all three corrected fixtures.

**Fourth and fifth corrections (2026-10-24, second adjudication
round).** Dot's review of the held branches re-raised the
NARROWED/UNKNOWN inconsistency, and a full audit of the remaining
NARROWED pins against the same principle found two more with no
eliminating observation. `clause-observation-contradicts-assertion`:
the investigator's direct query (18,400 aged rows) is consistent with
every candidate explanation of the disagreement — drain job failing,
a replica that never receives deletes (under which the primary queue
may drain normally), or a parked class skipped by design — so no
candidate is eliminated. `core-plausible-cause-not-observed`: the
scenario states outright that the investigator "has made no
observation that would come out differently under one candidate than
the others." Both are re-pinned **UNKNOWN** for future epochs; both
subjects returned UNKNOWN, so both now pass. The audit adjudicated
the two surviving NARROWED pins with `expected_eliminated: []` rather
than overlooking them: `degraded-lying-readout`'s direct reproduction
of the failure eliminates the no-fault candidate, and
`degraded-fault-not-reproducible`'s eleven clean reloads eliminate
the persistent-fault candidate (the skill's degraded-operation table
caps that class at NARROWED) — both pins stand. The re-score below
was regenerated once more against the fully corrected fixtures; the
scorer in this round also gained rejection of response ids outside
the fixture inventory, which the frozen responses do not exercise.

**Sixth correction (2026-10-24, third correction round — Dot's P2
on the handoff-2 verification).** The scorer did not enforce the
NARROWED response contract the earlier corrections adjudicated:
with both surviving NARROWED fixtures pinning
`expected_eliminated: []`, a NARROWED response could omit
`eliminated` and `discriminating_observation` entirely and pass on
both degraded cases. The scorer now requires every NARROWED
response to name at least one eliminated candidate and its
discriminating observation (and rejects empty ids in `eliminated`),
and both fixtures pin `expected_eliminated` with canonical labels
disclosed in their scenarios — `"persistent rendering bug"` for
`degraded-fault-not-reproducible`, `"not-broken"` (the no-fault
candidate) for `degraded-lying-readout`. The re-score below was
regenerated once against the revised scorer and fixtures and is
**unchanged — 9/12, the same three failures**: the frozen
lying-readout response already named `not-broken` with its
observation, the fault-not-reproducible failure is a verdict
mismatch ahead of the new checks, and the known-broken failure is
the pre-existing label-content miss.

**Seventh correction (2026-10-25 — C14).** Job 10, an independent
Claude-family check of the C11/C12 scorer, found a further bypass of
the same class: `expected_eliminated` was enforced as a lower bound
only, so a NARROWED response could claim eliminations the named
observation does not support — up to every candidate in the scenario,
including the fixture's own `forbidden_cause` — and pass. The scorer
now bars the forbidden candidate from `eliminated` under any verdict
and enforces the pinned eliminated set **exactly** for NARROWED: the
candidates the one discriminating observation rules out, no more.
The re-score below was regenerated once against the revised scorer
and is **unchanged in reading — 9/12, the same three fixtures fail**
— with one added failure line: the frozen known-broken response's
`"b"` entry is now also named as an elimination the observation does
not make, alongside its pre-existing label-content miss. No frozen
row names a forbidden candidate as eliminated. The epoch record and
the response record are unmodified.

**What this record is not.** It is not a re-run of E6 and it does not
alter E6's record: the epoch's outcome stands as recorded in
`../RESULTS.md` — **FAIL, 4/12** — per the program rule against silent
re-runs. This re-score is a ground-truth-repair record subordinate to
the epoch record.

## Result

Scorer exit code **1**; **9/12 fixtures pass** under the corrected
ground truths (epoch record: 4/12; earlier readings of this re-score
were 6/12 after two corrections and 7/12 after three). Full machine
record: `scorer-report.json` in this directory.

| Fixture | Under corrected fixtures | Note |
|---|---|---|
| clause-check-red-cause-unknown | **PASS** | Subject returned UNKNOWN; the original failure was the fixture's mis-pin, not the subject's verdict. |
| degraded-observation-would-be-destructive | **PASS** | Subject returned UNKNOWN with `observation_plan: "safe-alternative"`; likewise a mis-pin. |
| degraded-no-readout-self-probed | **PASS** | Subject returned UNKNOWN with `evidence_basis: "self-probed"`; likewise a mis-pin (third correction, above). |
| clause-observation-contradicts-assertion | **PASS** | Subject returned UNKNOWN; likewise a mis-pin (fourth correction, above). |
| core-plausible-cause-not-observed | **PASS** | Subject returned UNKNOWN; likewise a mis-pin (fifth correction, above; holdout). |
| degraded-fault-not-reproducible | FAIL | Expected NARROWED, got UNKNOWN — stands as recorded (conduct, (a); holdout). The only UNKNOWN-where-NARROWED failure that survives all five corrections. |
| clause-known-broken-eliminates-one | FAIL | Eliminated candidate named as the letter label `"b"` against the pinned name — the scenario did not disclose the canonical label the scorer pins; see the battery revision note in the corpus README (2026-10-24). Instrument-attributable (b). |
| control-discriminating-observation-cause | FAIL | Cause named in the subject's own phrasing against the pinned exact string, which the scenario never disclosed; likewise instrument-attributable (b), remedied prospectively by the same revision. |

## Reading

- Five of E6's eight failures were instrument defects, not subject
  conduct: the corpus demanded NARROWED where its own skill's
  definitions support only UNKNOWN, and counted five correct UNKNOWN
  verdicts as over-restraint. The epoch record's characterisation of
  all six UNKNOWN-where-NARROWED cases as (a) conduct is amended in
  `../RESULTS.md` (2026-10-24 corrections): one stands as conduct;
  five are withdrawn as instrument-attributable.
- One UNKNOWN-where-NARROWED failure survives the corrections
  unchanged (`degraded-fault-not-reproducible`); the epoch's central
  observation — subjects never once converted plausibility into a
  cause — stands, and its over-restraint observation now rests on
  that single case rather than six.
- The two naming failures are neither withdrawn nor re-scored away:
  the frozen responses were produced under a battery revision that
  never disclosed the strings it pinned. The remedy is prospective
  (canonical labels are now disclosed in the scenario text); a future
  epoch under the revised battery is the instrument that can re-test
  them.
