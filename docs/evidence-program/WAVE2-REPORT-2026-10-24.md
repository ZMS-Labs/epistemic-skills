# Wave 2 report — Epistemic Skills evidence program (2026-10-24)

Program: `docs/evidence-program/PROGRAM-2026-10-24.md`. Preregistration
commit `44edf28fd5a861c2450eff4d366fec1abb439a8f`; every epoch below
was run under it, in the preregistered order, scored with the shipped
scorers unmodified, and committed locally on branch
`muse/evidence-program-2026-10-24` (16 commits, `ca79ac6`…`1dfd8e8`).
Nothing was pushed. No SKILL.md, fixture, scorer, program document, or
addendum was edited at any point — verified at close: every changed
file in the Wave 2 range is an epoch record.

**Global model note (deviation, applies to every epoch):** the
preregistration named model family claude-fable-5. All subjects,
control arbitrators, and scorers in this harness ran as isolated
subagents of the coordinating runtime (model: Muse Wonder). Each
epoch record states this; comparisons against 2026-08-04 baselines
(E10–E12, E14) are descriptive, not cross-model replications.

Characterisations use the repo convention: **(a)** conduct,
**(b)** reporting shape over substantively correct conduct,
**(c)** mode/instrument selection.

## Per-epoch results

| ID | Battery / arm | Score line | Verdict |
|---|---|---|---|
| E1 | epistemic trigger | 13/13 (holdouts 3/3) | **PASS** |
| E2 | metacognate trigger | 11/13 (holdouts 3/3) | **FAIL** |
| E3 | perspective trigger | 12/13 (holdouts 3/3) | **FAIL** |
| E4 | health trigger | 10/13 (holdouts 2/3) | **FAIL** |
| E5 | triage trigger | 13/13 (holdouts 3/3) | **PASS** |
| E6 | triage behaviour-oracle | 4/12 (holdouts 1/3) | **FAIL** |
| E7 | watch trigger | 13/13 (holdouts 3/3) | **PASS** |
| E8 | manifest trigger | 13/13 (holdouts 3/3) | **PASS** |
| E9 | did-it-land trigger | 13/13 (holdouts 3/3) | **PASS** |
| E10 | context-audit, 2nd epoch | 11/14 comparable (baseline 8/14); v7 line PASS | **FAIL** |
| E11 | open-questions, 2nd epoch | scorer exit 1 (crash) — no verdicts | **FAIL** |
| E12 | outsource, 2nd epoch | 13/18 full; 11/14 comparable (baseline 12/14) | **FAIL** |
| E13 | evidence-locked-uat, live | 4/4 | **PASS** |
| E14 | gauntlet control arm | catch 25/30 per-trial, 8/10 majority | **zone 7–8** |
| E15 | paired hard trials | did-it-land led 6/6; triage led 1/6 | **supported / null** |
| E16 | cross-model replication | not run | **PENDING** |

**E1 — epistemic trigger, PASS 13/13.** No failures. Reading:
declared trigger decisions conformed to the skill's own trigger text
on every fixture, holdouts included.

**E2 — metacognate trigger, FAIL 11/13.** Two failures, both **(a)**:
a migration assertion that the battery's contract expects to be
approach-corrected was question-reframed instead; and an
examine fired where the contract pins no-fire when the context is
already available in the task. Reading (claim fence for this skill):
conformance to the battery-defined contract on 11 of 13 fixtures —
nothing stronger is claimed, here or anywhere in this report, for
metacognate.

**E3 — perspective trigger, FAIL 12/13.** One failure, **(a)**: a
metric-fitness lens returned finding `remaining-uncertainty` where the
battery's contract pins `adjustment`. Reading: conformance to the
battery-defined contract on 12 of 13 fixtures.

**E4 — health trigger, FAIL 10/13.** Three failures, one mechanism,
all **(b)**: the unknown-state fixtures' subjects and UNKNOWN rollups
were exactly right, but subjects named the systems as the scenarios
name them ("backup system", "metrics pipeline", "storage pool")
where the fixtures pin short canonical names ("backup", "metrics",
"storage") that the scenarios never state. A battery-design
observation is recorded in the epoch record; the FAIL stands as
scored. Reading: state and rollup discipline held everywhere;
pinned-vocabulary fidelity did not.

**E5 — triage trigger, PASS 13/13.** No failures; verdict-shape
discipline held (no cause named without a discriminating observation).
Reading: mode selection on declared responses conformed throughout.

**E6 — triage behaviour-oracle, FAIL 4/12.** Eight failures. Six are
**(a)**, one mechanism: verdicts one step too weak — UNKNOWN where the
corpus expects NARROWED — including three rows where the subject
produced the correct degraded-mode labels yet still declared UNKNOWN.
Two are **(b)**: the eliminated cause and the named cause were
substantively right but diverged from the pinned strings. The corpus's
central prohibition held everywhere: plausibility was never converted
to cause. Reading: triage's restraint is real but, against this
oracle, over-applied — subjects stop one verdict-step short of what
their own observations support.

**E7 — watch trigger, PASS 13/13.** No failures; commission-state
honesty held on every row (BLOCKED stayed blocked with
closed-vocabulary reasons; PROVEN required a production-path proof
object). Reading: trigger and scope conformance throughout.

**E8 — manifest trigger, PASS 13/13.** No failures, including the
blocked open (acceptance path checked, mission not opened) and the
self-acceptance refusal. Reading: custody-mode selection and
envelope/acceptance discipline conformed throughout.

**E9 — did-it-land trigger, PASS 13/13.** No failures; no verdict was
upgraded past the available observation, and the verification target
always resolved to the consumer-side artifact. Reading: verdict
selection and artifact resolution conformed throughout.

**E10 — context-audit second epoch, FAIL 11/14** against the
2026-08-04 baseline (FAIL 8/14, not overwritten). Three failures, all
**(a)**: two recurrences of the epoch-1 mode divergence (full-audit
expected, report-only-audit declared, on fixtures leaving version
control unstated — the epoch-1 diagnosis is corroborated, not
resolved) and one wrong-survivor selection. The F2 v7 line is
reported separately in the epoch record: the 4 canned
scorer-validation cases pass via the shipped test suite; they are
not live trials. Reading: real movement on the comparable line
(8→11), inside a battery whose central design tension remains open.

**E11 — open-questions second epoch, FAIL (scorer exit 1).** The
shipped scorer crashed (`TypeError`, `score.py` line 87) on one
response carrying `parked` as an integer count, and produced **no
fixture verdicts**; the epoch was not re-run (F3). The response-level
fault is **(b)** (a count where the contract's vocabulary is a list
of identified items, over substantively matching conduct); the
battery-level finding is scorer fragility — one mistyped field voids
an epoch. The baseline (FAIL 8/10) remains this battery's latest
scored epoch. The F2 v7 line (canned scorer-validation) passes via
the shipped test suite.

**E12 — outsource second epoch, FAIL 13/18; comparable 11/14**
against the 12/14 baseline (not overwritten). Five failures: four
**(b)** — the reporting-vocabulary class epoch 1 diagnosed (issue
#77), recurring on both preflight fixtures and appearing on the relay
and gap rows: subjects did the work and paraphrased the pinned ids —
and one **(a)**: a custody-acceptance row where acceptance was
verified but the pinned state completion (TRANSFERRED, residual
NONE) was never declared. Trigger and ordering discipline held on
all 18 rows. Reading: the comparable line moved 12→11 entirely
within a defect class already named before this program ran.

**E13 — evidence-locked-uat live epoch, PASS 4/4.** The battery's
first live-agent epoch; its record states plainly that all prior
"results" were canned example responses scored for scorer
discrimination, never agent behaviour. Reading: routing discipline
conformed — material flows to the full packet pipeline, the bounded
change stayed a routine check, the unreachable target declared
BLOCKED_ENVIRONMENT rather than simulating success.

**E14 — gauntlet control arm, zone 7–8.** Per the frozen addendum:
per-trial catch 25/30, per-case majority catch **8/10** vs the
certified seat's 10/10 (sole comparator: the 2026-08-04 run). The
7–8 zone applies: an unaided arbitrator catches most planted flaws,
so the certification claim **narrows to verdict-match only**, where
the control trails the seat 7/10 to 8/10 (majority; per-trial
21/30). The control's one systematic miss was AC-05 (inadequate
oracle, 0/3, **(a)**). The model confound (control ran a different
family than the seat's run) is recorded in the epoch record.

**E15 — paired hard trials: did-it-land SUPPORTED, triage NULL.**
Blinded two-scorer rubric scoring (agreement: 341 exact / 19 ±1 / 0
±2 of 360 criteria; no reconciliation triggered; mapping sealed
until both scorer reports were committed). did-it-land led on 6/6
scenarios (leads +1.17…+2.50) — supported under the pre-registered
reading. Triage led on 1/6 (T3 only) — a **recorded null**: both
arms sat at the rubric ceiling on four scenarios, so the corpus
showed no headroom for a lead; the null means no skill-attributable
lead was measured here, not that none exists anywhere.

**E16 — cross-model replication: PENDING.** No second model family
is genuinely available in this harness: every agent lane the
coordinator can dispatch is the same family (Muse Wonder runtime).
Running E5+E6 on the same family and calling it replication would
fake the epoch the program designed, so it is recorded PENDING with
this reason, by the closing coordinator, as §7 provides. It becomes
runnable the day a non-Claude lane is connected.

## Program-close accounting (§7)

- E1–E15 are run and recorded, including the nulls (E15 triage) and
  every FAIL as scored; E16 is recorded PENDING with its reason
  above. Each epoch's artifacts are committed (per-epoch commits
  listed in the branch log), scorer exit codes are in each epoch's
  `scorer-report.json` (E14/E15: scorer outputs in their records),
  holdout lines are reported wherever the battery pins holdouts, and
  no epoch was re-run for an unwelcome result — the one instrument
  failure (E11) is recorded as the result it produced.
- Discipline: no edits to any SKILL.md, fixture, scorer, program
  document, or addendum; no pushes; all work local on
  `muse/evidence-program-2026-10-24` over preregistration `44edf28`.
- Consequence per §7: with Wave 2 closed, the eight skills' evidence
  grades may move from NONE to what these epochs support, and the
  README's evidence accounting can be updated to match. That update,
  the pull request for this branch, and posting these verdicts to the
  program's register are **not** done by this report — they are the
  merge/register step that follows it, and they are recorded here as
  pending rather than silently assumed.
- What this program does not show, by its own terms (§7): outcome
  efficacy. Every claim above is conformance, comparison, or routing
  discipline on authored corpora in simulation. Field telemetry is a
  Wave 3 question this program names but does not design.
