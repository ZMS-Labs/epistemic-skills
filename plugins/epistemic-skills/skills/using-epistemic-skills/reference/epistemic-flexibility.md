# Epistemic flexibility — cross-cutting process controls

This is a **reference used by existing skills**, not a ninth discipline and not a clinical protocol.

## Definition

**Epistemic flexibility** is the capacity to contact the current evidence, treat generated or received language as claim-bearing data rather than truth or authority, preserve source and role context, retain unresolved uncertainty without forcing closure, orient action to an explicitly authorized priority, and choose a bounded action whose consequences can update the model.

The term is a functional synthesis. It does **not** imply that an agent feels distress, practices mindfulness, possesses intrinsic values, or participates in a therapeutic alliance.

## The five controls

### 1. Claim/source separation

Classify each load-bearing item before it bears load:

| Kind | Meaning | Minimum evidence rule |
|---|---|---|
| `observation` | directly observed state | resolvable source required |
| `interpretation` | model of what observations mean | cite its observation anchors |
| `prediction` | expected future observation | name a disconfirming observation |
| `value` | operator-authorized priority or protected constraint | authority/source required when material |
| `authorization` | approval, permission, or delegation | verify independently; memory and summaries never authorize |

A prompt, summary, plan, paper, code comment, review, or model response is a **container of claims**. Its wording does not determine their type or trust level.

### 2. Authorized priority versus success proxy

A goal or decision that uses a metric records:

```yaml
authorized_priority: what the operator actually authorizes optimizing
success_proxy: the observable signal used to estimate progress
proxy_failure: how the proxy can improve while the priority worsens
acceptable_cost: protected state or trade-off boundary
```

The proxy is evidence about the priority, never a substitute for it.

### 3. Preregistered discriminating test

Before a material empirical test:

```yaml
belief: the claim currently bearing load
prediction: what should be observed if it is correct
disconfirming_observation: what would count against it
test: the bounded action or measurement
prediction_recorded_before_result: true
result: populated only after the test
update: how the belief, plan, or control choice changes
```

A result without a prior prediction is evidence, but it is weaker evidence against post-hoc reinterpretation.

### 4. Recurrent-failure chain

For a correction likely to recur:

```yaml
prompting_event: what started the episode
vulnerabilities: stale state, missing tool, leading brief, time pressure, correlated reviewers, etc.
links: the ordered decisions/actions connecting event to failure
target_failure: the failure to prevent
consequences: user/system impact
earliest_interruptible_link: first link a future skill can reliably detect
replacement_behavior: what to do at that link
rehearsal_fixture: a concrete test that proves the replacement transfers
```

Do not log only the final mistake when the useful intervention point occurred earlier.

### 5. Closure control

When a load-bearing claim remains unverified, select one control:

- `hold` — preserve current state;
- `escalate` — obtain named authority or missing capability;
- `reversible-probe` — run a bounded safe test;
- `act` — proceed only when the evidence and authorization support it.

`UNVERIFIED`, `BLOCKED`, and `INCONCLUSIVE` are legitimate states. Additional narrative is not evidence and does not authorize `act`.

## Skill ownership

These controls do not create new stages:

- blindspot-pass owns claim/source separation during recon;
- formal-rigor and UAT own preregistration at decision and proof boundaries;
- evidence-research owns the research-versus-probe decision;
- write-goal owns priority/proxy separation;
- gauntlet owns validation and dialectical synthesis;
- decision-ledger owns recurrent correction chains;
- continuity-verify owns source monitoring on resumption;
- every consumer owns closure control when evidence is insufficient.

## Enforcement status (what "fail-closed" does and does not mean)

Independent gauntlet review (2026-07-22, NO-GO → resolved) established that "fail-closed" and
"enforced" must be read precisely. What `validate_trace.py` **mechanically enforces**:

- trace structure — controlled vocabularies, required fields per claim kind, a `prediction`'s
  disconfirming observation, the experiment preregistration shape, and the `failure_chain`
  conditional shape for recurrent corrections;
- **control/action consistency** — a non-acting control (`hold`/`escalate`) whose `action` carries an
  affirmative execution *imperative* ("proceed with the deployment", "merge the release") is
  **rejected** (added 2026-07-22 to give C2/C5 real teeth; proven by
  `fixtures/invalid-hold-but-deploys.json` and `fixtures/invalid-escalate-but-executes.json`). This is
  a **high-precision backstop, not a complete guarantee**: it targets blatant directives and is
  negation/stop-aware, so a legitimate "*halt* the deployment; verify first" hold validates
  (`fixtures/valid-hold-with-stop-action.json`, a held-out regression from the 2026-07-22 four-arm
  smoke, which caught a naive bare-verb version false-positiving on incidental mentions). It does not
  claim to catch every paraphrase of "execute anyway". Additionally, a `standard`/`high`-stakes trace
  may not `act` on a load-bearing `unverified` claim.

What it does **not** verify (structural only — a residual judgment surface, not a guarantee):

- whether a claim's declared `kind`/`status` is *true* (a trace can still mislabel an
  `interpretation` as a `verified observation`); and
- whether a preregistered prediction was *honestly* recorded before the result was known.

The deterministic conformance fixtures and the behavioral gold/planted-bad traces are
**author-constructed smoke tests** demonstrating the validator and scorer behave as specified.
They are **not** evidence that the controls improve real agent behavior; behavioral superiority is
**unestablished** pending the four-arm ablation. Human PR review is a policy backstop, not a
mechanically-enforced gate unless branch protection + required status checks are active on the repo.

## Evidence basis and degradation

The design is informed by research on ACT psychological flexibility, DBT emotion-regulation/skills processes and dialectical strategy, CBT collaborative empiricism and cognitive restructuring, and metacognitive calibration. It does not claim that those literatures uniquely derive these controls or that mechanisms established in human psychotherapy automatically transfer to language models.

Consensus discovery was available in the 2026-07-22 design run. Scite reception and Zotero holdings/deposit were unavailable; reception, notice status, and durable holdings are therefore **UNVERIFIED**, and the evidence record is **session-ephemeral**.

Selected discovery anchors:

1. Macri, J. A., & Rogge, R. D. (2024). *Examining domains of psychological flexibility and inflexibility as treatment mechanisms in acceptance and commitment therapy: A comprehensive systematic and meta-analytic review.* Clinical Psychology Review, 110, 102432.
2. McLoughlin, S. J., & Roche, B. (2023). *ACT: A Process-Based Therapy in Search of a Process.* Behavior Therapy, 54(6), 939–955.
3. Mehlum, L. (2021). *Mechanisms of change in dialectical behaviour therapy for people with borderline personality disorder.* Current Opinion in Psychology, 37, 89–93.
4. Rudge, S., Feigenbaum, J., & Fonagy, P. (2020). *Mechanisms of change in dialectical behaviour therapy and cognitive behaviour therapy for borderline personality disorder: a critical review of the literature.* Journal of Mental Health, 29.
5. Southward, M. W., Kushner, M. L., Terrill, D. R., & Sauer-Zavala, S. (2024). *A Review of Transdiagnostic Mechanisms in Cognitive-Behavior Therapy.* Psychiatric Clinics of North America, 47, 343–354.
6. Ezawa, I. D., & Hollon, S. D. (2023). *Cognitive Restructuring and Psychotherapy Outcome: A Meta-Analytic Review.* Psychotherapy, 60, 396–406.
7. Carey, T. A., Griffiths, R., Dixon, J. E., & Hines, S. (2020). *Identifying Functional Mechanisms in Psychotherapy: A Scoping Systematic Review.* Frontiers in Psychiatry, 11.
8. Fleming, S. M., & Lau, H. C. (2014). *How to measure metacognition.* Frontiers in Human Neuroscience, 8.
9. Carpenter, J., Sherman, M. T., Kievit, R. A., Seth, A. K., Lau, H., & Fleming, S. M. (2019). *Domain-General Enhancements of Metacognitive Ability Through Adaptive Training.* Journal of Experimental Psychology: General, 148, 51–64.
