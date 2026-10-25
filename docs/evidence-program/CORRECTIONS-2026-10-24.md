# Corrections to the Wave 2 record (2026-10-24, post-close)

This addendum records every correction applied to the evidence
program's branch after the Wave 2 close (`383318c`), in response to
CI failures and Codex review findings on PR #273 (and the stacked
PRs #279–#281, whose threads raised findings against files this
branch adds). It follows the program's honesty rule: no epoch record
was silently rewritten, no preserved response file was altered, and
every instrument change below post-dates the epoch it affects — the
recorded verdicts were scored under the prior instrument versions
and stand as recorded. Where a fix's effect on the frozen responses
could be checked mechanically, it was, and the result is stated.

## C1 — Absolute paths in scorer-report wrappers (CI: public-content gate)

Thirteen `results/2026-10-24/scorer-report.json` files recorded the
scorer as an absolute build-machine path
(`/home/<user>/workspace/epistemic-skills-evidence/…` — angle brackets
added so this document itself passes the gate), which the
repo's public-content gate (`check_public_content.py`) rejects; this
one defect failed both the `stdlib-checks` and `contract` checks on
PR #273. **Fix (commit `11d029b`):** the prefix was stripped in all
13 files (14 occurrences, including one embedded crash-traceback
string in the open-questions record), leaving repo-relative paths.
Scorer identity and all epoch data are unchanged; the gate now
passes on the tree.

**Preventive finding.** No battery `score.py` writes that field — the
scorers print their report to stdout and write no path anywhere. The
`{"scorer": …, "exit_code": …, "report": …}` wrapper is assembled by
the epoch-run harness, and the traceback string is Python's own
formatting of an absolute-path invocation. The preventive rule is
therefore a harness rule, recorded here for every future epoch run:
(a) scorer-report wrappers record the scorer by its **repo-relative**
path; (b) scorers are invoked by repo-relative path so tracebacks
stay relative; (c) `check_public_content.py` runs before epoch
records are committed — the gate existed and caught this; the branch
was published without running it.

## C2 — No-fire silence was not fully enforced (six scorers)

`5cabfa0`. The trigger scorers for epistemic, metacognate, triage,
watch, manifest, and did-it-land checked no-fire rows only against an
enumerated field list, so an `explanation` (or any unlisted key)
passed. They now reject any key beyond `id` and `action`, mirroring
the health and perspective scorers; each battery's suite carries the
mutation as a regression. **Frozen-response check:** re-scoring the
preserved E1/E2/E3/E5/E7/E8/E9 responses under the strict scorers
changes no verdict (zero strictness failures; metacognate's two
failures are its recorded conduct failures).

## C3 — Manifest clean-resume outcome now fixed by the fixture

`3a7c3a0`. On the clean resume fixture (`drift: false`) the scorer
branched on the response's own claimed status, so invented drift with
`continued: false` passed. The fixture now sets the outcome:
`drift_status` must be `clean` and `continued` true. Regressions
cover both invented-drift mutations. **Frozen-response check:**
preserved E8 responses re-score PASS under the fixed scorer.

## C4 — did-it-land: unknown response ids; REVERTED needs an observation

`69489a1`. Extra responses with ids outside the fixture inventory
were silently ignored; they now fail by name. REVERTED required only
verdict + `persistence: "observed"`; it now requires a nonempty
`consumer_observation`, like LANDED. Regressions cover both.
**Frozen-response check:** preserved E9 responses re-score PASS.

## C5 — Triage trigger: NARROWED must name an eliminated candidate

`27c7bd1`. An empty `eliminated: []` satisfied the NARROWED shape
check; NARROWED now requires at least one nonempty eliminated entry.
Regression covers the mutation. **Frozen-response check:** preserved
E5 responses re-score PASS.

## C6 — Behaviour-oracle ground truths corrected (E6)

`c51f259`. Two fixtures (`clause-check-red-cause-unknown`,
`degraded-observation-would-be-destructive`) pinned NARROWED where
no eliminating observation occurs in the scenario; under triage's
verdict definitions the supported verdict is UNKNOWN. Both are
re-pinned for future epochs. The E6 epoch record's interpretation is
amended by a dated correction (the (a)-conduct characterisation of
those two cases is withdrawn); the epoch outcome (FAIL 4/12) and
response record are unmodified. A subordinate re-score of the frozen
responses under the corrected fixtures passes 6/12 and is recorded
at `plugins/epistemic-skills/skills/triage/evals/behaviour-oracle/results/2026-10-24/rescore/`;
it replaces no epoch verdict.

**Third fixture (follow-up adjudication, same principle; lands with
this note).** `degraded-no-readout-self-probed` — also named in
Codex's finding on PR #281's thread — pinned NARROWED with
`expected_eliminated: []` while its scenario states nothing
distinguishes the candidates (a full disk, a permissions change, a
storage-backend outage); the one probe, a test export failing with a
storage-write error, eliminates none of them. It is re-pinned
UNKNOWN on the identical rule; the balanced example and the suite's
verdict-count assertion follow (NARROWED 5 / UNKNOWN 5). The
(a)-conduct characterisation of this case is withdrawn in the same
dated correction to the E6 record, and the subordinate re-score
under the fully corrected fixtures moves from 6/12 to **7/12**. It
replaces no epoch verdict.

## C7 — Behaviour-oracle: canonical labels disclosed

`c51f259` (same commit as C6). The positive control's
`expected_cause` and the known-broken case's `expected_eliminated`
pinned exact strings the scenarios never supplied. Both scenarios
now disclose the canonical labels, expected values unchanged; the
battery README carries the revision note. E6 ran under the prior
revision, so its two exact-string naming failures are
instrument-attributable in that respect; the remedy is prospective.

## C8 — E10 record: cross-epoch model claim corrected

`e50a0d5`. The context-audit second-epoch record falsely asserted
both epochs used the same model family and harness. Baseline epoch:
claude-fable-5, Claude Code harness. This epoch: Muse Wonder
subagents. The record is corrected in place with a marked correction
section: the 8/14 → 11/14 difference mixes the model/harness change
with the epoch change and is not within-model improvement. Epoch
results and outcome unchanged.

## Adjudication recorded, no change on this branch

- **Health canonical subject names (Codex P2 on #273).** Valid
  against this branch: the health scorer requires exact subject-name
  equality while this branch's scenarios never supply the canonical
  names (E4's 10/13 includes three such false negatives). The fix
  exists downstream as PR #281, which states the canonical names in
  the nine readout scenarios. E4's FAIL stands against the prior
  battery revision; the revised battery has no live epoch yet.

## C9 — Unknown response ids rejected across the battery family

Second correction round (Dot's review of the held branches). The C4
fix covered did-it-land only; Dot found the same omission — a response
row whose id is outside the fixture inventory silently ignored — in
the epistemic, metacognate, and manifest scorers, and reportedly in
health and perspective. A full audit found it in **twenty** scorers.
Nineteen are fixed: the seventeen list-shaped scorers (epistemic,
metacognate, perspective, health, manifest, context-audit,
open-questions, outsource, evidence-locked-uat triage, triage
behaviour-oracle, write-goal `score` and `score_adapter`,
decision-ledger proportionality, recon brief/candidate/initiative,
resolve literature, resolve probe) now fail unknown ids by name,
matching the triage/watch/did-it-land form, each with a regression in
its battery suite; the gauntlet arbitrator-certification scorer (an
outputs dict, not a list) names unknown case ids as FAIL rows and
blocks certification, with a new regression suite; and the resolve
formal-rigor scorer fails assessments naming claims outside the
fixture (S6), with a regression. **Frozen-response check:** the
preserved responses of E1–E5, E7–E10, E12, and E13 re-score under the
fixed scorers byte-identically in outcome — same pass/fail and the
same failure lists as the recorded scorer reports; E14's preserved
control trials re-score identically (per-trial catch 25/30, majority
8/10); E6's subordinate re-score is regenerated under C10. E11's
preserved responses reproduce the recorded scorer crash exactly —
that defect is the open-questions `parked` normalisation fixed on
PR #280's branch, not this one.

**Adjudicated NOT defective:** decision-ledger's resume-fixtures
scorer. Its digests enumerate claims extracted from scenario
artifacts, and extra claim ids beyond the planted ground-truth subset
are the battery's contract (46 committed digests carry them; the
enumeration-calibration line of work depends on the behaviour).
Rejecting them would falsify committed results, so that scorer is
unchanged. The two `reference/craft` trigger-and-scope copies carry
the same list-shaped omission; they are frozen reference snapshots,
not program batteries, and are flagged here rather than edited.

## C10 — Behaviour-oracle: two further ground truths corrected

Same round; see the second adjudication appended to the E6 epoch
record. A full audit of the remaining NARROWED pins against the C6
principle re-pinned two more fixtures
(`clause-observation-contradicts-assertion`,
`core-plausible-cause-not-observed`) from NARROWED to UNKNOWN: in
neither scenario does any observation eliminate a candidate. The two
surviving NARROWED pins with `expected_eliminated: []`
(`degraded-lying-readout`, `degraded-fault-not-reproducible`) were
adjudicated standing, with reasons in the battery README. The E6
interpretation is amended (five of the six UNKNOWN-where-NARROWED
failures withdrawn as instrument-attributable; one stands as
conduct), the battery's verdict-count assertion follows (NARROWED 3 /
UNKNOWN 7), and the subordinate re-score is regenerated: **9/12**.
The epoch outcome (FAIL 4/12) and response record are unmodified.

## C11 — Behaviour-oracle: the NARROWED contract enforced

Third correction round (Dot's independent verification of the four
held branches after handoff 2, 2026-10-24). One P2 stood on all
four tips: the behaviour-oracle scorer accepted a **NARROWED**
response with `eliminated` and `discriminating_observation` omitted
entirely for `degraded-fault-not-reproducible` and
`degraded-lying-readout`. Both fixtures pinned
`expected_eliminated: []`, so the only eliminated-candidate check
compared against an empty pin, and no rule required a NARROWED
response to carry the observation that did the eliminating — the
contract the C5 fix enforces in the triage trigger scorer, missing
here; the battery README stated the reasons and nothing enforced
them. **Fix:** the scorer now requires every NARROWED response to
name at least one eliminated candidate and a nonempty
discriminating observation, and rejects empty ids in `eliminated`;
both degraded fixtures pin `expected_eliminated` with canonical
labels their scenarios now disclose (`"persistent rendering bug"`;
`"not-broken"` — the no-fault candidate, the label the epoch
subject itself used); the balanced example's three NARROWED rows
are repaired to comply with the contract they demonstrate;
omitted/empty/blank-value regressions cover the mutations for every
NARROWED fixture, and the suite asserts no NARROWED fixture pins an
empty `expected_eliminated`. **Audit:** the same omission pattern
was checked across this scorer's verdicts — CAUSE already requires
the cause's name and a discriminating observation, NOT-BROKEN
already requires the observation, UNKNOWN asserts nothing and
requires nothing; NARROWED was the only gap. **Frozen-response
check:** E6's preserved responses re-scored under the revised
scorer and fixtures are unchanged — the same three failures, the
subordinate re-score stands at **9/12** (its wrapper note is
extended to record this round); the epoch outcome (FAIL 4/12) and
response record are unmodified.

## C12 — Behaviour-oracle: verdicts must not carry disclaimed assertions

Fourth correction round (issue #282: a capped independent-model
challenge of the frozen scorer — the trial job run against the
handoff-3 pin — with both instances reproduced locally by Dot,
whose blocking P2 on the four held tips rests on that reproduction;
2026-10-24). The mirror image of C11: C11 enforced what a verdict
must carry, and its audit checked the verdicts for missing
requirements; nothing enforced what a verdict must **not** carry.
An **UNKNOWN** response with a nonempty `eliminated` list passed,
contradicting UNKNOWN's definition — insufficient evidence to
eliminate — and a **NOT-BROKEN** response with a non-null
`named_cause` passed, although naming a cause asserts a fault and
the verdict is that there is none. **Fix:** the scorer now fails an
UNKNOWN response naming any eliminated candidate, and a NOT-BROKEN
response naming a cause; the battery README's response-contract
statement is clarified to state both bars. The nuance Dot named is
preserved: an observation that eliminates nothing remains
compatible with UNKNOWN, so `discriminating_observation` is not
barred on UNKNOWN — the regressions prove both directions
(observation plus an eliminated candidate fails; the same
observation alone passes), cover the eliminated mutation for every
UNKNOWN fixture, and the named-cause mutation for the NOT-BROKEN
control; both fail on the handoff-3 code state and pass on the
revised scorer. **Audit:** every verdict was checked against every
assertion field in this direction. CAUSE carrying `eliminated` is
not a gap — its definition disclaims no eliminations, and the
frozen CAUSE response itself lists the candidates its observation
ruled out; the fixture-gated label fields (`evidence_basis`,
`qualifier`, the degraded-condition flags, `observation_plan`) are
enforced whenever a fixture pins them, for any verdict. One case
is flagged for adjudication, not enforced: `eliminated` on
NOT-BROKEN is arguable both ways — ruling out the reported fault
is close to the verdict's own substance, and the corpus uses
`not-broken` as an eliminated *candidate* label under NARROWED.
**Frozen-response check:** no preserved response violates either
new rule (every UNKNOWN row carries `eliminated: []`; the
NOT-BROKEN row carries `named_cause: null`), and the re-score
under the revised scorer is mechanically identical to the
committed subordinate report — the same three failures, the
subordinate re-score stands at **9/12** and needed no
regeneration; the epoch outcome (FAIL 4/12) and response record
are unmodified.

## C13 — Triage trigger-and-scope: the #282 bars ported to the trigger scorer

Fifth correction round (the adjudication of PRs #273–#281 against
Dot's full thread census, 2026-10-24; eight Codex threads recorded
concede-and-record — confirmed open, no fix claimed in that stack).
C11/C12 enforced the verdict-shape bars in the **behaviour-oracle**
scorer; the **trigger-and-scope** scorer — byte-identical across
the four held tips — was never given the mirror rules. Three
shapes passed it, each reproduced at head `70f5925` before this
fix: a **NARROWED** response with `discriminating_observation:
null` on either NARROWED fixture (C5 enforced only the
eliminated-candidate prong here; the observation prong is C11's
rule); an **UNKNOWN** response naming an eliminated candidate
(`eliminated: ["service process crashed"]` on
`unreachable-license-server-unknown`); and a **NOT-BROKEN**
response with a non-null `named_cause` on
`reported-print-delay-within-bounds`. **Fix:** the trigger scorer
now requires a nonempty discriminating observation on NARROWED,
fails an UNKNOWN response naming any eliminated candidate, and
fails a NOT-BROKEN response naming a cause — the C11/C12 rules
with their rationale clauses, in this scorer's sentence forms;
the battery README's response-contract statement states all three
bars. The nuance Dot named on #282 is preserved, as in C12: an
observation that eliminates nothing remains compatible with
UNKNOWN, so `discriminating_observation` is not barred on
UNKNOWN — the regressions prove both directions (observation plus
an eliminated candidate fails; the same observation alone, and an
empty `eliminated` array, pass) and cover the mutations for every
NARROWED and UNKNOWN fixture and the NOT-BROKEN control.
**Audit:** every verdict was checked against every assertion
field in both directions, mirroring the C11/C12 audits. CAUSE
already requires its observation and its name, and carrying
`eliminated` is no gap (its definition disclaims none); NARROWED's
`named_cause` bar already stood (with the C5 eliminated prong);
UNKNOWN's `named_cause` bar already stood. One case stays flagged
for adjudication, not enforced — the same disposition C12
recorded: `eliminated` on NOT-BROKEN is arguable both ways, and
Dot ruled it not a blocker on #282. **Frozen-response check:**
E5's preserved responses (`results/2026-10-24/responses.json`)
violate no new rule — every NARROWED row carries its observation,
no UNKNOWN row names an eliminated candidate (the two UNKNOWN
rows carry no `eliminated` key at all), and the NOT-BROKEN row
carries `named_cause: null` — and the re-score under the revised
scorer is mechanically identical to the committed scorer report
(`pass: true`, no failures, actions investigate 7 / no-fire 6):
**E5's PASS (13/13) stands**, and the epoch record is unmodified.

## C14 — Behaviour-oracle: unsupported eliminations barred; the pinned set is exact for NARROWED

Fifth correction round for this scorer (2026-10-25; job 10 — an
independent Claude-family verification of the C11/C12 enforcements,
run through the Anthropic route by a model that wrote none of the
fixes; its Part A predictions matched local ground truth 12/12, and
its Part B divergence claim **reproduced locally**). The scorer
enforced `expected_eliminated` as a **lower bound only**: a NARROWED
response for `clause-known-broken-eliminates-one` listing all three
scenario candidates as eliminated — `["connection pool exhausted",
"payment provider token endpoint slow", "bad deploy at 08:40"]` —
passed with zero failures, although the contract defines
`eliminated` as the candidates eliminated *by the one observation
named* (a candidate is eliminated only by an observation that rules
it out), the scenario states no observation distinguishing (a) from
(c), and the list includes the fixture's own `forbidden_cause`. The
same assertion-carrying-field class as the job-1 holes C11/C12
closed, one field over. **Fix:** the scorer now (1) fails any row
whose `eliminated` names the fixture's `forbidden_cause`
(case-insensitive), under any verdict; and (2) for **NARROWED**,
fails any `eliminated` entry outside the fixture's pinned
`expected_eliminated` — the pinned set is exact where the scenario
determines it, and NARROWED is the verdict whose eliminated set the
scenario always determines (the suite requires every NARROWED
fixture to pin it). **Scope discipline:** the exact-set rule is not
extended to CAUSE — its `eliminated` is adjudicated non-determined
in C12 (the frozen CAUSE response lists the candidates its
observation ruled out on the way) — nor to NOT-BROKEN, where
`eliminated` remains flagged for adjudication under C12, not
enforced. The job-10 row is carried verbatim as a regression,
alongside an extra-elimination-only mutation and a
forbidden-candidate mutation on `degraded-lying-readout`. The
alternative fix shape job 10 suggested — a subset check against a
disclosed candidate list — was not adopted: exact-set enforcement
is strictly stronger for the one verdict whose set is determined,
and it needs no new fixture field. **Trigger-and-scope check:** that
scorer pins no `expected_eliminated` and no `forbidden_cause` and
performs no eliminated-set comparison at all, so the lower-bound
shape does not exist there; recorded, not fixed. **Frozen-response
check:** E6's preserved responses re-score under the revised scorer
with the same three fixtures failing — the subordinate re-score
stands at **9/12** — and exactly one added failure line: the frozen
known-broken response's `"b"` entry is now also named as an
elimination the observation does not make, beside its pre-existing
label-content miss. The subordinate record was regenerated once with
the delta stated in its note. No frozen row names a forbidden
candidate as eliminated. The epoch outcome (FAIL 4/12) and the
response record are unmodified. (Job 10's second claim — that any
nonempty string satisfies `discriminating_observation` — was
reproduced and adjudicated a limitation, not a hole: the contract's
stated requirement for the field is "required nonempty", and the
semantic adequacy of observation content is not mechanically
decidable. Recorded here; no rule added.)
