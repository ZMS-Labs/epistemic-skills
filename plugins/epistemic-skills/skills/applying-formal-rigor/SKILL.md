---
name: applying-formal-rigor
description: 'Use when an operator explicitly requests a formal derivation or complexity proof; when a material software-or-systems decision has multiple viable alternatives with different measurable or theorem-governed properties; when a proposed design needs correctness confirmation or reversal; or when review feedback asserts a theorem, bound, consistency guarantee, isolation property, or safety property. Do not use for pure preference, one-answer mechanical edits, or low-cost reversible choices whose plausible loss is below the analysis cost unless rigor was explicitly requested.'
---

# Applying Formal Rigor

## Purpose

Establish software-and-systems properties and synthesize only the decision that
the evidence and operator-authorized priorities justify. Preserve three
disciplines:

1. name the precise model and construct;
2. prove applicability, then derive instead of asserting;
3. sweep the material property terrain without pretending a fixed library is
   exhaustive.

Formal theory establishes properties inside a model. It does not supply runtime
facts, operator priorities, or a winner by itself.

## Trigger and proportionality gate

Fire when any of these is observable:

- the operator requests a formal derivation, complexity proof, or rigorous
  comparison;
- material alternatives differ on measurable or theorem-governed properties;
- a single proposed design needs correctness confirmation or reversal;
- a review claim asserts a theorem, lower bound, consistency guarantee,
  isolation property, safety property, or equivalent formal result.

Do not fire for pure preference, a mechanical edit with one viable answer, or
a low-cost reversible choice whose maximum plausible loss is below the cost of
analysis unless the operator explicitly requests rigor.

Select the tier with this observable vector:

```text
cost of error × uncertainty × downstream dependence × irreversibility
versus
cost of analysis and cost of a reversible probe
```

A skipped or focused pass is correct when more ceremony would cost more than
the decision can plausibly lose.

## Rigor tiers

### `focused`

Use for one bounded formal question or a low-blast-radius reversible choice:
one complexity bound, normal-form test, concrete history, invariant proof, or
specific correctness challenge.

- Return inline in at most six short bullets or 250 visible words.
- Include subject/question, model, precise construct, minimum preconditions and
  fact mapping, finite derivation or counterexample, result, and residual
  limitation. Add a bounded empirical check only when material.
- Do not emit P1-P9 reconciliation, a full decision frame,
  `formal-rigor-record@2`, a receipt/stamp, a persistent process artifact, or
  standard/high-assurance source apparatus solely for the focused run.

### `standard`

Default for a material fork or a justification that will bear downstream load.
Require a complete decision frame, P1-P9 reconciliation, applicability chains,
formal/empirical/normative separation, explicit concessions, and a
`formal-rigor-record@2`.

### `high-assurance`

Use for an irreversible migration, security/privacy boundary, safety or
financial exposure, public compatibility contract, cross-service consistency
mechanism, high blast radius, model-sensitive proof, or explicit operator
request. Add:

- primary-theory pins and official product/version documentation for every
  load-bearing construct;
- executable calculation, model check, proof, reproduction, or counterexample
  where feasible;
- preregistered empirical closure for every material runtime premise;
- sensitivity analysis over authorized priorities and uncertain parameters;
- an explicit `gauntlet` handoff recommendation when its independent trigger
  is present.

High assurance never certifies itself.

## Method

### 1. Build the decision frame for standard/high-assurance work

Record:

- exact question;
- `subject.ref` and `subject.revision`;
- system boundary, actors, environment, horizon, and exclusions;
- stable alternatives and exactly one null/status-quo option for a fork;
- hard constraints;
- operator-authorized objectives;
- priority rule and its authority reference;
- assumptions and empirical premises;
- uncertainty posture;
- tier and observable tier reason.

Allowed priority rules are `constraint-satisfaction`, `lexicographic`,
`weighted-utility`, `minimax`, `minimax-regret`, `pareto-only`, or an exactly
quoted/referenced `custom` rule. Do not infer priorities from engineering taste.

### 2. Reconcile the universal property inventory

For standard/high-assurance work, record exactly one state per family:

- `fired`: a material property exists and an adequate specialist module is
  loaded;
- `not-applicable`: no material property exists inside the declared boundary;
  state the boundary-tied reason;
- `unmapped`: a material property exists but no adequate module, model, or
  input is available; carry it into `coverage_limits`.

| ID | Property family | Question |
|---|---|---|
| `P1` | Functional semantics and invariants | Allowed behavior, safety/liveness, transitions, refinement, totality? |
| `P2` | State, representation, and integrity | Facts, dependencies, representable states, decompositions, enforceability? |
| `P3` | Time, ordering, and concurrency | Histories, happens-before, isolation, atomicity, scheduling, progress? |
| `P4` | Distribution, replication, and consistency | Scope, failures, visibility/order, convergence, consensus, merge semantics? |
| `P5` | Dependability, faults, and recovery | Fault model, reliability, availability, rollback, durability, correlated failure? |
| `P6` | Security, privacy, and information flow | Adversary, authority, confidentiality, integrity, noninterference, privacy? |
| `P7` | Algorithms, resources, capacity, and real time | Model, workload, bounds, saturation, deadlines, lower bounds? |
| `P8` | Uncertainty, measurement, randomization, and numerics | Probability, estimation, calibration, conditioning, rounding, stability? |
| `P9` | Evolution, interfaces, and operations | Compatibility, version skew, migration, reversibility, observability, lifecycle? |

Coverage is complete only relative to the declared subject, boundary,
inventory, loaded modules, facts, and limits. It never means that the library
exhausts software-and-systems theory.

Load only modules for fired families from
[`reference/modules/index.md`](reference/modules/index.md). If no adequate
module exists, use `unmapped`; never coerce the property into a nearby module.

### 3. Prove applicability, then derive

Every load-bearing construct follows:

```text
model → preconditions → fact mapping → derivation → result → residual mismatch
```

- **Model:** name the formal world and scope.
- **Preconditions:** enumerate every theorem or product-guarantee condition
  that bears load.
- **Fact mapping:** map each precondition to an `observation`,
  `interpretation`, `assumption`, `value`, or `authorization`. Observations use
  revision-pinned anchors; values and authorizations require their source.
- **Derivation:** instantiate a finite chain. A theorem name alone is an
  assertion.
- **Result:** use `established`, `refuted`, `conditional`, or `incomplete`.
  Give a counterexample or witness when it is the shortest refutation.
- **Residual mismatch:** name what the model omits or idealizes.

If any link breaks, the result is conditional or incomplete. Vocabulary cannot
repair missing fact mapping.

### 4. Keep three layers separate

#### Formal result

State what follows inside the named model from mapped premises.

#### Empirical closure

Runtime, workload, environment, and human-behavior facts require observation.
Before a discriminating test, record:

```yaml
belief: <load-bearing empirical premise>
prediction: <observation expected if correct>
disconfirming_observation: <what counts against it>
test: <bounded action or measurement>
prediction_recorded_before_result: true
```

Then record `result` and `update`. A prediction written after the result is
`post-hoc-weaker`. Official documentation establishes documented semantics for
the pinned version, not the local deployment's runtime state.

#### Normative synthesis

Apply hard constraints, authorized objectives, and the priority rule to the
property results. Never move from “better on metric X” to “choose A” unless X
is authorized and its relation to other objectives is explicit.

### 5. End in one synthesis outcome

- `dominance`: one feasible option is no worse on every authorized objective
  and strictly better on at least one; forbidden with load-bearing `unmapped`.
- `pareto-set`: report the non-dominated set and frontier; select nothing
  without an authorized tie-break.
- `conditional`: the result holds only under named premises, scenarios, or
  priorities; state them in the verdict.
- `underdetermined`: facts, options, coverage, or authorized priorities do not
  justify a choice; name what is missing.
- `reversal`: the proposed option or premise contradicts the derivation or a
  hard constraint.
- `reversible-probe`: a bounded preregistered experiment has greater decision
  value than more argument or irreversible action.

Name concessions and recovery moves. A forced winner is a failure, not a more
useful answer.

## `formal-rigor-record@2`

Standard and high-assurance work emits JSON conforming to
[`evals/formal-rigor-v2-fixtures/formal-rigor-record.schema.json`](evals/formal-rigor-v2-fixtures/formal-rigor-record.schema.json).
Use [`examples/valid-formal-rigor-record.json`](examples/valid-formal-rigor-record.json)
as the minimal shape and `python validate_record.py <record.json>` for the
stdlib structural check.

The record contains:

- `subject`, `valid_while`, and `coverage_limits`;
- `rigor` and the full `decision_frame`;
- exactly one coverage row for each P1-P9;
- derivations carrying module/version, construct, sources, model,
  preconditions, fact mapping, steps, result, and residual mismatch;
- empirical closure state;
- one synthesis outcome with basis, conditions, concessions, and recovery
  moves;
- `never_attests` boundaries.

Record invariants:

- a fork has exactly one `null-option`;
- every fired family names at least one loaded module;
- non-fired families name no modules;
- every material `unmapped` family appears in `coverage_limits` and forbids
  unconditional `dominance`;
- `pareto-set` and `underdetermined` select no option;
- a null revision cannot claim `subject-revision-unchanged` and must carry a
  visible freshness limit;
- the envelope attests structure, provenance, and validity window only—never
  derivation correctness, an unobserved empirical fact, or Gauntlet
  independence.

## Required correctness rules

- **MVD/4NF:** an MVD requires the relevant sets to vary independently. Paired
  `method` and `priority` facts do not establish `user_id ↠ method`. A valid
  example is independent contact methods and notification topics in
  `user_delivery(user_id, contact_method, notification_topic)`; see the
  relational module.
- **Isolation:** derive from standard minimum → actual product and pinned
  version → concrete history/dependency graph → admitted or excluded anomaly.
  Never infer product behavior from an isolation-level name.
- **Consistency:** compare scoped predicates by implication only where their
  definitions justify it. Do not use one universal strength chain.
- **Lamport clocks:** `a → b` implies `C(a) < C(b)`; the converse is false.
  A tie-break may extend clock order to a total order, but that total order is
  not the causal relation.
- **Lower bounds:** fix the problem, computational/resource model,
  preprocessing, randomization, exactness, posture, and bounded resource.
  Changing any of these creates a new subject, not a free optimization.

## Source and boundary policy

- Load-bearing definitions and theorems cite a canonical paper, standard, or
  edition registered by the module. Secondary prose may aid readability but
  may not be the sole source.
- Variable implementation behavior cites official documentation pinned to
  product and version.
- Local code, schemas, configuration, and measurements use immutable or
  revision-bound coordinates.
- Material scholarly or empirical propositions go to `evidence-research`,
  which returns evidence and limitations but never the design verdict.
- A consequential high-stakes record may enter `gauntlet`; Gauntlet rechecks
  freshness and independently attacks the derivation.
- A durable decision may be reused by `decision-ledger`; persistence never
  upgrades its truth state.

## Staleness

A material change to subject revision, boundary, option set, constraints,
authorized objectives, priority rule, formal model, or product version voids
the record. Re-fire against the new subject; never patch the old verdict.

## Anti-rationalizations

| Thought | Required response |
|---|---|
| “I named the theorem.” | Show model, preconditions, fact mapping, derivation, and residual mismatch. |
| “All nine families are accounted for.” | Claim only relative coverage; expose unknown material terrain as `unmapped`. |
| “Technically superior means choose it.” | Identify the authorized objective and priority rule or preserve the Pareto set. |
| “The database calls it Repeatable Read.” | Pin product/version semantics and analyze a concrete history. |
| “This lower bound is universal.” | Freeze problem, model, preprocessing, randomization, exactness, and resource. |
| “A winner is more useful.” | Use the six outcomes; usefulness does not authorize fabricated determinacy. |
| “Formal proof replaces measurement.” | Keep runtime premises conditional until observed against a preregistration. |
| “The record validates, so the proof is correct.” | Structural validation never attests derivation correctness. |

## Local overlay

If a `LOCAL.md` exists beside this file, read it after this file. It may bind
paths, registries, and local authority, but it never overrides this protocol.
