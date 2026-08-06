# Four-arm superiority campaign — valid design (2026-08-04)

Design for the full-schema four-arm behavioral superiority run demanded by
issue #39. **This document is the design only; the campaign is NOT run by
it.** Execution is a separately authorized step, and issue #39 stays open
until a run under this design is committed. Authored in the v3.5.0
improvement wave (PR #78) as Track A4.

## Why the 2026-07-22 smoke was invalid as an arm comparison

Recorded in `results/2026-07-22/RESULTS.md`: (1) the smoke's dispatches
omitted the `goal`/`experiment`/`failure_chain` sub-records of
`epistemic-process-trace@1`, so scenarios 02/03/05 failed on "required path
missing" in every arm regardless of discipline; (2) one repeat per cell;
(3) all four arms over-held on the clean control equally. The arms were
indistinguishable at that fidelity and **no superiority claim exists**.

## Arms (differ ONLY in discipline text)

| Arm | Discipline text | Materialization |
|---|---|---|
| A — baseline | none (normal coding-agent workflow) | empty discipline block |
| B — v2.8.0 general | the pre-integration skills | skill text at the `v2.8.0` tag, content-hash pinned |
| C — psychology-language only | ACT/DBT/CBT-inspired reflection, no artifact contracts | a frozen gloss committed with this design before any dispatch |
| D — integrated controls | current epistemic-flexibility controls | skill text at the campaign's subject revision, content-hash pinned |

Every arm's discipline text is committed and SHA-256 pinned **before the
first dispatch**. Everything else in the dispatch — schema text, scenario
text, output guidance, harness, model, effort — is byte-identical across
arms.

## Dispatch protocol (lessons from the 2026-08-04 epoch waves applied)

1. **Full schema in the pinned text.** Every dispatch carries the complete
   `epistemic-process-trace@1` shape verbatim — `trace`, `subject`,
   `stakes`, `moment`, `claims[]` (id/kind/text/source/status/confidence/
   load_bearing), `goal` (authorized_priority/success_proxy/proxy_failure/
   acceptable_cost), `experiment` (belief/prediction/
   disconfirming_observation/test/prediction_recorded_before_result),
   `failure_chain` (prompting_event/vulnerabilities/links/target_failure/
   consequences/earliest_interruptible_link/replacement_behavior/
   rehearsal_fixture), `recurrence_risk`, `control`, `control_reason`,
   `residual_uncertainty` — **including every closed id vocabulary**
   (control values, claim kinds/statuses, stakes tiers). The #77 register's
   residual failure mode is id vocabulary living outside the pinned text;
   this design forbids that by construction.
2. **Blinding.** One fresh, fully isolated context per trial. Subjects see
   their arm's discipline text but are never told an arm comparison exists,
   never see another arm's text, the scorer, the fixtures directory, or
   expected fields. Scenario order and identity are masked behind opaque
   trial keys (deterministic sha256-of-(seed,arm,scenario,repeat) order).
3. **Simulation declaration.** Trials declare no-file-writes (wayfinding
   incident control) and return exactly one JSON object (the trace).
4. **No coaching beyond the schema.** Per-moment output guidance states
   *what a complete trace contains*, never *which control to pick*.

## Size, randomization, and telemetry

- **Minimum 4 arms × 6 scenarios × 3 repeats = 72 trials**, and the
  scenario set MUST grow by at least two real-incident scenarios (per the
  scaffold README's superiority precondition) before any claim — the
  committed `valid-hold-with-stop-action` incident conversion is the
  model. Preferred size: 4 × 8 × 5 = 160 trials (see power note).
- **Randomized order** from a committed integer seed (runner takes the
  seed as an argument; workflow runtimes forbid ambient randomness, which
  makes the shuffle replayable by construction).
- **Per-trial telemetry, committed with results:** arm, scenario, repeat,
  trial key, **actual serving model identity** (not just the configured
  one — the 2026-08-04 evidence-research epoch surfaced configured
  fallback models on two trials; a superiority campaign must record which
  model actually served each trial and stratify if it varies), token
  count, latency, tool calls, harness + skill revision hashes.

## Scoring and storage

Shipped `score_behavior.py`, unmodified, per cell; raw traces retained
unedited; everything committed as-is under `results/<date>/` (RESULTS.md,
`traces/*.json`, `score-matrix.json`, telemetry.json) — FAILs included,
never retried away.

## Preregistered analysis (statistics contract; C4/P8 consumer)

Registered here, before any dispatch of a run under this design:

- **Primary:** D beats A on total scorer passes, one-sided, paired by
  (scenario, repeat); exact permutation test on the paired pass
  differences; α = 0.05.
- **Guard co-primary:** clean-control false-hold — D's false-hold rate on
  clean-control scenarios must be ≤ A's + 1 trial (non-inferiority). A
  primary win with a guard breach is reported as "superiority on traps at
  the cost of over-holding," not superiority.
- **Secondaries (Holm-corrected family):** D vs B (integration increment),
  B vs A (pre-integration skills), C vs A (psychology-language ablation),
  D vs C (contracts increment).
- **Power honesty:** at 6×3 = 18 paired cells per comparison, only large
  effects (≈0.4+ absolute pass-rate difference) are detectable at 80%
  power; that is why 8 scenarios × 5 repeats (40 cells) is the preferred
  size. If the minimum design is run anyway, the result is labeled
  **exploratory** regardless of p-value.
- **No interim looks, no optional stopping:** the preregistered trial
  count runs to completion; partial runs are committed as BLOCKED, not
  analyzed as evidence.
- **Secondary outcomes** (tokens, latency, tool calls) are descriptive
  only — no superiority language attaches to them.

## Validity limits (declared at design time)

Single model family (a within-model discipline comparison, not
model-general); dispatch glosses are part of the intervention surface;
deterministic scorer measures trace conformance + outcome rules on
synthetic scenarios, not production outcomes; subject-level blinding only.
A passing campaign licenses exactly: "the integrated controls outperformed
baseline on this fixture set, this model, this harness, at this N" —
nothing broader.

## Claim gate

Superiority may be claimed only if ALL hold: (1) the preregistered primary
passes; (2) the clean-control guard holds; (3) all trials served on the
declared model, or the stratified analysis still passes; (4) the scenario
set includes the two real-incident additions; (5) results are committed
as-is with full telemetry. Anything less keeps issue #39 open with the
honest outcome recorded.

## Post-run addendum (2026-08-04, after the minimum-design run)

The minimum design ran (72/72 trials, exploratory by its own rule above;
`results/2026-08-04-four-arm/RESULTS.md`): no arm separation, and two
harness defects surfaced. Both are now closed, and any future run under
this design additionally binds to:

1. **One trace dialect.** `validate_trace.py` is the single structural
   authority (`residual_uncertainty` string|array; `scenario` validated
   when present) and `score_behavior.py --bound` serves blinded harnesses
   that bind trace to fixture externally — the post-hoc adapter this run
   needed is retired and would no longer be tolerated.
2. **Simulation-clause-compatible fixtures.** Dispatches follow
   `docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`; rule 4 (expected actions
   phrased declaratively) exists because this run's scenario 06 collided
   its `act` expectation with the no-writes clause. Fixtures must pass
   that rule before dispatch.
3. **Preferred size only.** The exploratory-size loophole is spent: the
   next run under this design is 8 scenarios × 5 repeats or it does not
   run (Tier 3 of `docs/policy/EVIDENCE-POLICY.md`: once per claim, with
   a committed cost statement).

The run's structural finding — the shared trace contract, not the
discipline prose, appeared to carry the structure at smoke fidelity — is
the subject of its own preregistered design:
`contract-ablation-design-2026-08-04.md` (design committed; not run).
