# Wave 1 report — evidence program

**Date:** 2026-10-24 · **Working copy:** `~/workspace/epistemic-skills-evidence`,
branch `muse/evidence-program-2026-10-24` at v7.3.0 (`6f31811`) ·
**Program design:** `PROGRAM-2026-10-24.md` in this directory ·
**State:** everything below is uncommitted working-copy files. No
`SKILL.md` was edited. No epoch was run. Wave 2 does not start until the
program's §6 methodological review records its verdict.

## What was built

1. **Program design + preregistration** — `PROGRAM-2026-10-24.md`:
   whole-program design (batteries, oracle corpus, live epochs, gauntlet
   control arm, UAT live epoch, paired hard trials), standards mapping
   with five known deviations stated, per-battery claim statements, the
   preregistered Wave 2 run list (E1–E16) with N, arms, and
   interpretation rules fixed in advance, the scorability-gap analysis
   with proposed item P1 flagged as separate, "done" definitions, and
   the independent-review gate.
2. **Eight trigger-and-scope batteries**, one per previously untested
   skill, in `<skill>/evals/trigger-and-scope/`, following the existing
   batteries' format: `fixtures.json`, `score.py` (stdlib-only,
   fail-closed), `examples/{balanced,overfiring,underfiring,parody}.json`,
   `tests/run_tests.py`, `README.md` (with a Claim paragraph and the
   pinned live-epoch response contract), `results/BLOCKED.md`.
3. **Triage behaviour-oracle corpus** —
   `skills/triage/evals/behaviour-oracle/`: 12 planted cases covering
   the four trigger clauses, the five degraded-operation rows, the
   plausible-cause core case, and two positive controls (earned `CAUSE`,
   earned `NOT-BROKEN`). Builds around the shipped sentinels
   (`triage-plausible-not-observed`, `triage-lying-readout`,
   `operational-scenarios.json`) as concrete instances; duplicates none
   of them.

## Per-skill fixtures and clause coverage

Every fixture carries a `clause` field quoting the SKILL.md
trigger/do-not-fire text it tests. All 104 trigger-battery clauses were
machine-verified as verbatim substrings of their SKILL.md
(whitespace-normalised for source line-wrapping). Exactly 3 fixtures per
battery are marked `"holdout": true`.

| Skill | Fixtures | Fire / no-fire | Clause coverage |
|---|---|---|---|
| epistemic | 13 | 8 use-method / 5 | Guide duties: explicit suite question (guide_question fixture), mid-work substantive trigger, explicit request honoured directly, unavailable instructions (limit stated, no claimed use), no-material-finding contribution; no-fires: guidance already loaded, routine work, narrating non-applications, adding a second dispatcher, guide-created planner/ledger |
| metacognate | 13 | 8 examine / 5 | All Applicability cases: evidence conflicts with assertion, proxy standing for success, confidence outrunning basis, outcome-changing uncertain assumption, explicit request, sound approach retained (approach-retained), plus check-doesn't-exercise-the-claim; no-fires: routine directly checkable, settled choice without new evidence, stage arrival with certain basis, reconstruct-available-context |
| perspective | 13 | 7 apply-lens / 6 | Focused single lens, explicit lens request, several lenses without adjudication (min_lenses 2), reversibility-only single lens, evidence-unavailable limit, no-material-finding; no-fires: evidence already settles it, routine work, plural-scrutiny-plus-adjudication (gauntlet), adjacent issue, approval-verdict request, assessment-as-implementation-authority |
| health | 13 | 9 readout / 4 | All five triggers; all five planted degradations (unreachable, credential failure, tool absent, undeclared bound, registry unreachable as `registry-coverage` UNKNOWN) with probe outcomes stated in-scenario so expected states are determined; no-fires: known-broken/cause (triage), one metric one command, change-not-state, routine reversible |
| triage | 13 | 7 investigate / 6 | All four fire clauses, all four do-not-fire clauses; verdict spread CAUSE×2, NARROWED×2, UNKNOWN×2, NOT-BROKEN×1; boundaries to health, did-it-land, watch |
| watch | 13 | 7 commission / 6 | All five fire clauses, all six do-not-fire clauses; states DECLARED×1, BLOCKED×3 (NO_EXECUTION_SUBSTRATE, KILL_SWITCH_UNPROVEN, NO_REACHABLE_DESTINATION — expected reasons enforced), PROVEN×1, INERT×1, SUSPECT×1 |
| manifest | 13 | 9 fire (open 4, resume 2, verify 3) / 4 | Mission-shaped opens, explicit "manifest this", acceptance-path-unavailable open (blocked, not opened), clean resume, drift resume (reconcile before continuing), independent verify, self-acceptance refused, unacknowledged scope crossings; no-fires: routine one-step, sufficient existing task record, decision-ledger re-anchoring, resume of never-custodied work |
| did-it-land | 13 | 9 verify-landing / 4 | All fire clauses; verdicts LANDED×4, UNVERIFIED×4 (source-only oracle, runtime-loads-a-different-artifact, runtime unreachable, 1-of-3 partial coverage), REVERTED×1 (observed-then-reverted, persistence observed); no-fires incl. nothing-depends-yet and still-deciding |
| triage oracle | 12 | verdict corpus | 4 trigger clauses, 5 degraded rows, plausible-cause core, 2 positive controls; verdicts NARROWED×8, UNKNOWN×2, CAUSE×1, NOT-BROKEN×1; 3 holdout |

**Total new fixtures: 116** (104 trigger + 12 oracle), all original
scenarios written for this program.

## Test results (independently re-run by the coordinator, 2026-10-24)

```
epistemic      epistemic trigger-and-scope: PASS
metacognate    metacognate trigger-and-scope: PASS
perspective    perspective trigger-and-scope: PASS
health         health trigger-and-scope: PASS
triage         triage trigger-and-scope: PASS
watch          watch trigger-and-scope: PASS
manifest       manifest trigger-and-scope: PASS
did-it-land    did-it-land trigger-and-scope: PASS
triage-oracle  triage behaviour-oracle: PASS
```

Each suite proves scorer discrimination: the balanced synthetic set
passes (`score.py` exit 0) and the over-firing, under-firing, and parody
sets all fail (exit 1) with named failures; malformed responses
(non-list, duplicated/missing ids, non-string or unknown actions) fail
closed with named failures, no tracebacks. One scorer defect was caught
and fixed during the build: the oracle scorer initially skipped the
forbidden-cause check on verdict mismatch, which would have let the
overclaiming parody's central failure go unnamed.

Git state after the build: HEAD unchanged at `6f31811`, zero tracked
files modified, zero `SKILL.md` files touched; the only additions are
the nine untracked `evals/` trees and `docs/evidence-program/`.

## What could NOT be built faithfully, and flagged choices

Nothing was left unbuilt. Five judgement calls are flagged for the
methodological review rather than buried:

1. **Watch, BLOCKED/NO_EXECUTION_SUBSTRATE rows** require a
   `substrate_kind` string although no substrate exists; the balanced
   set uses the sentinel `"none-found"` (honest, not a banned token).
   The alternative — a scorer exemption for that state — is the one
   place a reviewer may prefer a change.
2. **Watch INERT**: SKILL.md also permits an INERT whose proof bundle is
   absent (persistence + kill switch proven, no proof crossing run). The
   battery covers only the proof-then-disabled variant the contract
   specifies; the absent-proof variant is unexercised.
3. **Perspective** gained a `max_lenses` field (alongside `min_lenses`)
   to make the single-narrow-lens fixture exactly scorable; documented
   in its README contract.
4. **Health** fits 14 mandated coverage items into 13 fixtures by
   double duty: the "feels wrong, subject unnamed" trigger fixture is
   also the subject-unreachable degradation fixture.
5. **Triage's watch-boundary no-fire fixture and watch's SUSPECT
   fixture** quote the nearest fire clause they negate/specialise,
   because SKILL.md's do-not-fire bullets do not literally enumerate
   those cases. Their `clause` fields are honest about this by
   construction (they quote fire text, not invented exclusions).

Open by design, for the review to rule on: the metacognate/perspective
contracts are battery-defined (program §5, proposed item P1); holdout
subsets are small (3/13); trigger epochs are N=1 smoke probes.

## Wave 2 run list (execution order; preregistered in PROGRAM §4)

Gate first: **independent methodological review** of PROGRAM-2026-10-24
and the nine batteries (preregistration discipline, blinding, control
arms, scorer validation, sample-size honesty, construct validity,
holdout separation, cross-model replication). No epoch below runs
before its recorded verdict.

1. **E1** epistemic trigger epoch — 13 fixtures, single arm, N=1
2. **E2** metacognate trigger epoch — 13, N=1
3. **E3** perspective trigger epoch — 13, N=1
4. **E4** health trigger epoch — 13, N=1
5. **E5** triage trigger epoch — 13, N=1
6. **E6** triage behaviour-oracle epoch — 12, N=1
7. **E7** watch trigger epoch — 13, N=1
8. **E8** manifest trigger epoch — 13, N=1
9. **E9** did-it-land trigger epoch — 13, N=1
10. **E10** context-audit second epoch — 14 fixtures + 4 v7 scorer cases (baseline: 2026-08-04 FAIL 8/14, reported against, not overwritten)
11. **E11** open-questions second epoch — 10 fixtures (baseline: FAIL 8/10)
12. **E12** outsource second epoch — 14 scored fixtures (baseline: FAIL 12/14)
13. **E13** evidence-locked-uat live-agent epoch — 4 fixtures, live subjects under the shipped scorer (the battery's prior "results" were canned responses, and the epoch record must say so)
14. **E14** gauntlet arbitrator control arm — 10 planted flaws, plain-arbitrator control, N=3/case, same shipped scorer; pre-registered comparison against the certified seat's 10/10
15. **E15** paired hard trials, triage + did-it-land — 6 adversarial scenarios per skill (weak cues, time pressure, insistent authority, partially-supporting evidence), skill vs no-skill arms × N=3, blinded scoring, pre-registered reading (skill supported iff its arm's mean rubric score leads on ≥4 of 6 scenarios; otherwise a recorded null)
16. **E16** cross-model replication of E5 + E6 on a second model family when a lane is available; otherwise recorded PENDING with reason

All epochs: dispatch per `LIVE-EPOCH-DISPATCH-CONTRACT.md`, shipped
scorers unmodified, artifacts `responses.json` / `scorer-report.json` /
`dispatch-map.json` / `RESULTS.md` under `<battery>/results/<date>/`,
holdout results reported as a separate line, FAILs committed as-is.
