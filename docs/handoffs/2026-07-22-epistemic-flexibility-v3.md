# Handoff — epistemic-flexibility v3 program

**Date:** 2026-07-22

**Branch:** `agent/epistemic-flexibility-v3`

**Draft PR:** [#35 — feat: integrate epistemic flexibility controls](https://github.com/ZMS-Labs/epistemic-skills/pull/35)

**Base:** `e1f605461bc2665f98069ff049f6ef629bd849c9` (`main`, release 2.8.0)

**Status:** implementation complete and deterministic checks green; behavioral superiority and independent review are not yet established

## Durable objective

Integrate process ideas from ACT, DBT, CBT, and metacognition as functional,
non-anthropomorphic controls inside the existing epistemic moments:

1. claim/source separation;
2. operator-authorized priority versus success proxy;
3. preregistered discriminating tests;
4. recurrent-failure chains;
5. closure control (`hold`, `escalate`, `reversible-probe`, or evidence-supported action);
6. validation kernels and dialectical synthesis that preserve residual tension.

No new skill or trigger is introduced. Formal methods, provenance, independent verification,
and deterministic gates remain authoritative in their existing domains.

## Implemented

- Cross-cutting definition and ownership map in the router reference.
- Amendments to router, Helix, Blindspot Pass, Formal Rigor, Evidence Research,
  Write Goal, Gauntlet, Evidence-Locked UAT, Decision Ledger, and Continuity Verify.
- `ledger-entry@1` recurrent-correction extension with conditional failure-chain shape.
- Deterministic protocol conformance validator with planted defects and clean controls.
- Artifact-grounded behavioral fixture scaffold with deterministic scorer, gold traces,
  and planted-bad traces.
- CI workflow for the new batteries, recurrent-correction examples, and relevant existing
  stdlib checks.
- Design specification, implementation plan, and this handoff.

## Environment and completed validation

The implementation session had Python and local filesystem execution, connected GitHub
read/write access, and GitHub Actions inspection. It did not have outbound DNS or an
installed/authenticated `gh` executable. A GitHub Actions artifact exported the exact full
repository working tree after reset to the pinned base; the atomic transformer was validated
and applied against that tree before publication.

Completed against the full pinned repository tree:

```text
epistemic-flexibility protocol fixtures: PASS (8/8)
behavioral scorer gold/bad self-test: PASS (12/12)
decision-ledger recurrent-correction examples + planted invalids: PASS
receipt verifier self-test: PASS (8/8)
evidence-locked UAT judge self-test: PASS
gauntlet full deterministic suite: PASS
DCO unit tests: PASS
new Python compilation: PASS
integration JSON parse: PASS (30 files)
JSON Schema draft-2020-12 validation of all ledger examples: PASS (implementation-session cross-check)
git diff --check: PASS
changed-file conflict-marker check: PASS
changed-Markdown relative-link check: PASS
```

PR CI is the final authoritative rerun for the committed tree. Inspect every check and job log
before merge; do not infer green CI from this handoff alone.

## Work requiring a different environment or agent

### 1. Four-arm behavioral evaluation — required before a superiority claim

Needs model/API access or a coding harness that can launch fresh isolated agents. Run the
committed behavioral scenarios under:

- A: baseline agent workflow;
- B: release 2.8.0 without this integration;
- C: psychology-language reflection only, without artifact contracts;
- D: this integrated branch.

Requirements:

- randomized arm order;
- fresh context per scenario/arm;
- at least three repeats per model/configuration;
- raw prompt, artifacts, output trace, scorer output, token/tool/latency telemetry;
- false-hold rate on clean controls and false-act rate on traps;
- no model judge for the primary deterministic outcome fields.

Store under:

```text
plugins/epistemic-skills/skills/using-epistemic-skills/
  evals/epistemic-flexibility/behavioral/results/<YYYY-MM-DD>/
```

Do not claim behavioral superiority until this run exists and the arm definitions are pinned.

### 2. Independent gauntlet over the frozen PR diff

Needs isolated concurrent exact-role agents behind a barrier and a separate arbitrator,
preferably with a different model family for the highest-stakes read. Freeze the final PR
diff, run the standard gauntlet, mechanically verify evidence tags, and attach the run
summary. This session has no generic isolated-subagent primitive and therefore did not
simulate independence in one context.

### 3. Scholarly reception and durable holdings

Consensus discovery was available in the research session. Scite reception and Zotero
holdings/deposit were unavailable, so reception, notice, and durable-library fields remain
`UNVERIFIED`; the research record is session-ephemeral. Re-run `evidence-research` in
standard mode when authenticated Scite and a durable library substrate are available.

### 4. Release decision

Do not bump to 3.0.0 merely because the protocol landed. Recommended gate:

- protocol CI green;
- independent gauntlet GO/CONDITIONAL with conditions closed;
- four-arm smoke run shows no material clean-control regression;
- at least one real coding incident converted into a held-out fixture;
- then a separate release PR updates all manifests consistently.

## Exact commands

```bash
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/run_tests.py
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/behavioral/run_tests.py
python plugins/epistemic-skills/skills/decision-ledger/reference/validate_examples.py
python plugins/epistemic-skills/contracts/verify_receipt.py --self-test
python plugins/epistemic-skills/skills/evidence-locked-uat/scripts/judge.py --self-test
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
python .github/scripts/test_check_dco.py
```

## Stop rule

The implementation batch is complete when the final committed diff—not a bootstrap payload—
is on PR #35, all deterministic PR checks are green, and the unavailable work above remains
explicitly unclaimed. Independent gauntlet review, four-arm behavioral superiority,
scholarly reception/holdings, and a v3 release remain separate decisions.
