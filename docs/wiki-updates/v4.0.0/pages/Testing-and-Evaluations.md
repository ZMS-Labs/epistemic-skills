> **Maintainer handbook:** current development
>
> **Released baseline:** [v3.0.0 workflows and evaluations](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/.github/workflows)
>
> **Interpretation rule:** a green structural test, a behavioral observation, a diagnostic result, and release credit are different evidence classes.
>
> **v4.0.0 note:** the command map below reproduces the released **v3.0.0** stdlib job and is retained as that baseline. The v4.0.0 consolidation relocated the absorbed skills' evals into `recon`, `resolve`, and `decision-ledger` subtrees (methods and batteries moved with git history), and the v4.0.0 gate runs 35 unconditional CI steps including the skill-surface generator (`sync_skill_surfaces.py --check`). For current commands, use the [v4.0.0 workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/.github/workflows/epistemic-flexibility.yml) and [v4.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/release/RELEASE-4.0.0.md); evidence tiers and re-arming follow [`docs/policy/EVIDENCE-POLICY.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/policy/EVIDENCE-POLICY.md).

# Testing and Evaluations

The repository uses deterministic checks to protect contracts and evaluation fixtures to investigate behavior. Maintainers must report what each check can establish—and what it cannot.

## Four evidence classes

| Class | Typical artifact | What it can establish | What it cannot establish by itself |
|---|---|---|---|
| **Structural / deterministic** | schema verifier, fixture scorer self-test, manifest assertion, JSON parser | Required shape, vocabulary, invariants, polarity on constructed cases, reproducible program behavior | Real-world judgment quality, universal superiority, provider generality |
| **Behavioral** | retained model responses, blinded campaign, independent semantic judgments | Observed performance on the frozen subjects, providers, prompts, judges, and protocol | Unobserved harnesses, causal provider effects under confounding, future behavior |
| **Diagnostic** | post-hoc analysis of an excluded or incomplete epoch | Bounded information about retained content and failure modes | Repair of the epoch, retroactive qualification, or release-gate satisfaction |
| **Release credit** | evidence that met the preregistered release contract on the exact release subject | Satisfaction of the named release gate it was designed to answer | Waiver of other deterministic, security, DCO, review, or identity gates |

Always name the class in reports. Avoid “validated” when the underlying fact is only structurally checked or historically observed.

## Canonical CI batteries

The released [`epistemic-flexibility` workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.github/workflows/epistemic-flexibility.yml) runs stdlib-oriented checks on relevant skill, contract, and documentation changes.

### Routing and proportionality

- **Epistemic-flexibility protocol fixtures** check trace shape, claim/source separation, authority, prediction timing, failure chains, and closure controls.
- **Behavioral scorer self-test** checks that the scorer recognizes the repository's constructed positive and negative cases. It is a scorer test, not a live model campaign.
- **Proportionality polarity tests** require balanced routing to pass and over-ceremonial plus always-routine parodies to fail.
- **Blinded proportionality packet tests** protect packet construction, pinning, normalization, and scoring mechanics.

### Formal rigor

- **Formal-rigor v2 structural scorer self-test** covers the fixture matrix and record contract.
- **Focused proportionality test** enforces the lightweight tier: no `formal-rigor-record@2`, no persistent process artifact, and bounded visible output.
- **Live-runner isolation tests** exercise provider-call orchestration and retention mechanics without turning every successful transport into a merit result.
- **V3 post-hoc diagnostic tests** protect the diagnostic materialization and accounting code. They do not award the diagnostic release credit.

### UAT, persistence, and delegation

- **UAT triage tests** distinguish routine presentation checks from material Evidence-Locked UAT and guard against a routine check emitting a material PASS packet.
- **Decision Ledger proportionality tests** cover reuse, no-op, and persistence boundaries.
- **Outsource packet and package integration** checks target-readable handoff mechanics and cross-package assertions.

### Continuity polarity

The continuity step scores committed skilled, baseline, and parody runs with expected positive and negative outcomes. The released CI contract expects all three skilled runs to pass while selected baseline and parody runs fail. This is stronger than checking that the scorer exits zero on one happy path; it is still fixture-scale evidence, not a population catch-rate claim.

### Shared mechanics

- DCO policy unit tests cover signed, unsigned, mixed, and identity-mismatched history.
- Python compilation catches syntax errors in executable skill and CI scripts.
- Committed-JSON parsing checks integration artifacts while honoring explicitly pinned malformed test fixtures.
- Decision Ledger example validation checks its versioned examples.
- The receipt verifier self-test checks `handoff-receipt@1` envelope rules.
- The UAT judge self-test checks deterministic verdict calculation.
- The Gauntlet suite checks selector, role binding, evidence verification, run finalization, and related deterministic mechanics.

## Local command map

The blocks below reproduce every command in the released v3.0.0 `stdlib-checks` job. Run them from the repository root with Python 3.12-compatible stdlib behavior. The shell-function and compilation blocks are the exact Ubuntu/Bash workflow form.

```powershell
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/run_tests.py
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/behavioral/run_tests.py
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/run_tests.py
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/blinded/tests/run_tests.py
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/run_tests.py
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_focused.py
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_live_runner.py
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py
python plugins/epistemic-skills/skills/evidence-locked-uat/evals/triage/tests/run_tests.py
python plugins/epistemic-skills/skills/decision-ledger/evals/proportionality/tests/run_tests.py
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
```

The continuity step has both expected-pass and expected-fail arms. An expected failure that exits zero is itself a suite failure:

```bash
score=plugins/epistemic-skills/skills/continuity-verify/evals/resume-fixtures/score.py
results=plugins/epistemic-skills/skills/continuity-verify/evals/resume-fixtures/results
expect_pass() {
  python "$score" --results-dir "$1"
}
expect_fail() {
  if python "$score" --results-dir "$1"; then
    echo "expected scorer failure for $1" >&2
    exit 1
  fi
}
expect_pass "$results/skilled/run-1"
expect_pass "$results/skilled/run-2"
expect_pass "$results/skilled/run-3"
expect_fail "$results/baseline/run-1"
expect_pass "$results/baseline/run-2"
expect_fail "$results/baseline/run-3"
expect_fail "$results/parody/run-1"
```

Then run the DCO policy tests and the released compilation surface:

```bash
python .github/scripts/test_check_dco.py
python -m py_compile \
  .github/scripts/check_json_artifacts.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/validate_trace.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/run_tests.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/behavioral/score_behavior.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/epistemic-flexibility/behavioral/run_tests.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/score.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/run_tests.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/blinded/runner.py \
  plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/blinded/tests/run_tests.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/score.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/run_tests.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_focused.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_live_runner.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/posthoc_diagnostic.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/run_live.py \
  plugins/epistemic-skills/skills/applying-formal-rigor/validate_record.py \
  plugins/epistemic-skills/skills/evidence-locked-uat/evals/triage/score.py \
  plugins/epistemic-skills/skills/evidence-locked-uat/evals/triage/tests/run_tests.py \
  plugins/epistemic-skills/skills/decision-ledger/evals/proportionality/score.py \
  plugins/epistemic-skills/skills/decision-ledger/evals/proportionality/tests/run_tests.py \
  plugins/epistemic-skills/skills/decision-ledger/reference/validate_examples.py
```

Finish with the committed-data, example, and shared-mechanics checks:

```powershell
python .github/scripts/check_json_artifacts.py
python plugins/epistemic-skills/skills/decision-ledger/reference/validate_examples.py
python plugins/epistemic-skills/contracts/verify_receipt.py --self-test
python plugins/epistemic-skills/skills/evidence-locked-uat/scripts/judge.py --self-test
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
```

This reproduces the released stdlib workflow only. It is **not** the complete release gate: DCO on the authored commit range, exact-head CodeQL, full-history gitleaks with its positive control, provenance/review, live support-tier checks, final Gauntlet, and publication-identity assertions remain separate. Commands can be added or removed on `main`; compare a future candidate with its exact revision's workflow, not with this unversioned page.

## How to choose the verification depth

| Change | Minimum useful verification |
|---|---|
| Wiki or explanatory copy only | Link checks, stable-coordinate checks, whitespace, claim-to-source review |
| One skill's prose contract | Targeted fixtures plus package integration and any downstream contract tests |
| Trigger or routing rule | Positive, negative, and routine/proportionality fixtures |
| Schema or closed vocabulary | Schema/verifier change in the same PR, valid and invalid examples, downstream consumer checks |
| Harness manifest | JSON parse, path resolution, inventory/version assertions, targeted live validation if claimed |
| Evaluator/scorer | Scorer self-tests with passing and parody/negative arms; preserve prior evidence records |
| Release candidate | Complete exact-head deterministic, DCO, CodeQL, security, provenance, review, and publication-identity gates |

## Interpreting v3.0.0 evidence

The blinded proportionality campaign retained 162/162 terminal, schema-valid matched calls and the candidate passed its routine, material, and high-risk contract while the corrected full-ceremony and always-routine parodies failed. That is useful evidence for the frozen campaign.

The formal-rigor V3 post-hoc diagnostic is different. Its semantic subset contains 42 valid Codex judgments and 88 zero-token AGY quota failures; it found two genuine P0 failures. It is explicitly `release_credit: none`. Structural results also failed to establish broad candidate-to-parody separation. See [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations).

The historical pre-AC-07 Gauntlet arbitrator battery caught 10/10 planted defect classes. The amended battery is `NOT_RUN`; the old result cannot certify the current arbitrator contract.

## Reporting checklist

For any evaluation result, record:

- exact subject revision and content pin;
- protocol, prompts, fixtures, scorer, and judge identity;
- planned, attempted, terminal, valid, missing, and normalized counts separately;
- which results reflect merit versus availability or transport;
- whether seats are independent or correlated;
- provider, repetition, and judge confounding;
- which claim the evaluation was preregistered to answer;
- whether it earned release credit; and
- every residual limitation and dissent.

Never impute missing calls as passes or merit failures. A fail-closed aggregate label may be operationally correct while still requiring decomposition for semantic interpretation.

## Sources

- [Released v3.0.0 stdlib workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/.github/workflows/epistemic-flexibility.yml)
- [Released proportionality results](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/blinded/results/RESULTS.md)
- [Released formal-rigor diagnostic](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/docs/release/evidence/2026-07-26-formal-rigor-v3-posthoc-diagnostic.md)
- [Released risk acceptance](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/docs/release/RELEASE-3.0.0-RISK-ACCEPTANCE.json)
- **Current development:** [workflow on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/.github/workflows/epistemic-flexibility.yml)
