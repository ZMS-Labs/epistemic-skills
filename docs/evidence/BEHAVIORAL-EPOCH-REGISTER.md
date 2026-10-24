# Behavioral epoch register (issue #77)

Successor to closed #70. Every skill must have either (a) a dated live epoch under
its eval battery, or (b) a current `results/BLOCKED.md` reviewed at a release gate.

## A. CI-wired trigger-and-scope batteries (BLOCKED.md today)

| Skill | Battery path | Live epoch | Notes |
|---|---|---|---|
| open-questions | `evals/open-questions/` | 2026-10-24 (E11, §D) | also #61; house battery now at `skills/open-questions/evals/trigger-and-scope/` |
| context-audit | `evals/context-audit/` | 2026-10-24 (E10, §D) | house battery at `skills/context-audit/evals/trigger-and-scope/` |
| agent-interface-design | `evals/agent-interface-design/` | — | retired skill; battery may archive |
| wayfinding | `evals/wayfinding/` | — | |
| throwaway-prototyping | `evals/throwaway-prototyping/` | — | |
| intent-traced-merge | `evals/intent-traced-merge/` | — | |

## B. Core skills without house-shape batteries

| Skill | Status |
|---|---|
| blindspot-pass | no eval surface |
| evidence-research / resolve literature | method + connectors; no scored epoch |
| write-goal | no eval surface |
| outsource | trigger-and-scope battery shipped 2026-10-24 (`skills/outsource/evals/trigger-and-scope/`); second live epoch E12, §D |

## C. Linked campaigns

- **#39** — valid four-arm superiority run (epistemic-flexibility Phase 4)
- Amended arbitrator-certification battery — `NOT_RUN` per skill honest limits

## D. 2026-10-24 evidence program epochs (E1–E16)

Preregistered program: `docs/evidence-program/PROGRAM-2026-10-24.md`
(preregistration commit `44edf28`); full accounting in
`docs/evidence-program/WAVE2-REPORT-2026-10-24.md`. **Global model note:**
the preregistration named model family claude-fable-5; all subjects,
control arbitrators, and scorers ran as isolated subagents of the
coordinating runtime (Muse Wonder). Comparisons against 2026-08-04
baselines are descriptive, not cross-model replications. Metacognate and
perspective verdicts are recorded **only** as conformance to a
battery-defined contract, per the methodological review's binding
qualifier.

| ID | Epoch | Score line | Verdict | Artifacts |
|---|---|---|---|---|
| E1 | epistemic trigger | 13/13 (holdouts 3/3) | PASS | `skills/epistemic/evals/trigger-and-scope/results/2026-10-24/` |
| E2 | metacognate trigger | 11/13 (holdouts 3/3) | FAIL | `skills/metacognate/evals/trigger-and-scope/results/2026-10-24/` |
| E3 | perspective trigger | 12/13 (holdouts 3/3) | FAIL | `skills/perspective/evals/trigger-and-scope/results/2026-10-24/` |
| E4 | health trigger | 10/13 (holdouts 2/3) | FAIL | `skills/health/evals/trigger-and-scope/results/2026-10-24/` |
| E5 | triage trigger | 13/13 (holdouts 3/3) | PASS | `skills/triage/evals/trigger-and-scope/results/2026-10-24/` |
| E6 | triage behaviour-oracle | 4/12 (holdouts 1/3) | FAIL | `skills/triage/evals/behaviour-oracle/results/2026-10-24/` |
| E7 | watch trigger | 13/13 (holdouts 3/3) | PASS | `skills/watch/evals/trigger-and-scope/results/2026-10-24/` |
| E8 | manifest trigger | 13/13 (holdouts 3/3) | PASS | `skills/manifest/evals/trigger-and-scope/results/2026-10-24/` |
| E9 | did-it-land trigger | 13/13 (holdouts 3/3) | PASS | `skills/did-it-land/evals/trigger-and-scope/results/2026-10-24/` |
| E10 | context-audit, 2nd epoch | 11/14 comparable (baseline 8/14, not overwritten) | FAIL | `skills/context-audit/evals/trigger-and-scope/results/2026-10-24/` |
| E11 | open-questions, 2nd epoch | scorer exit 1 (crash) — no verdicts; baseline (FAIL 8/10) remains latest scored epoch | FAIL | `skills/open-questions/evals/trigger-and-scope/results/2026-10-24/` |
| E12 | outsource, 2nd epoch | 13/18 full; 11/14 comparable (baseline 12/14, not overwritten) | FAIL | `skills/outsource/evals/trigger-and-scope/results/2026-10-24/` |
| E13 | evidence-locked-uat, live | 4/4 (first live epoch; prior results were canned responses) | PASS | `skills/evidence-locked-uat/evals/triage/results/2026-10-24/` |
| E14 | gauntlet control arm | catch 25/30 per-trial, 8/10 majority vs certified 10/10 — certification claim narrows to verdict-match only (control 7/10 vs seat 8/10) | zone 7–8 | `skills/gauntlet/evals/arbitrator-certification/results-2026-10-24.md` |
| E15 | paired hard trials | did-it-land led 6/6 (SUPPORTED); triage led 1/6 (recorded NULL — rubric ceiling on four scenarios) | supported / null | `docs/evidence-program/e15-2026-10-24/` |
| E16 | cross-model replication | not run — no second model family genuinely available in this harness; recorded PENDING by the closing coordinator, not simulated | PENDING | `docs/evidence-program/WAVE2-REPORT-2026-10-24.md` §E16 |

## How to close #77

Commit `results/<YYYY-MM-DD>/` (or updated BLOCKED.md) per row, then update this
table with the evidence path. Release notes cite this register, not #70.
