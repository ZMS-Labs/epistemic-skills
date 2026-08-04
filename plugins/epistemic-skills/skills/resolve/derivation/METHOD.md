<!-- resolve instrument: derivation (applying-formal-rigor) — consolidated into resolve (v4.0.0, 2026-08-04); this file is the instrument's full method, formerly its standalone SKILL.md -->


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

Focused is permitted only when all of these are true:

- the output resolves one bounded property inside a closed, supplied model;
- the conclusion is only that property's status, counterexample, or residual
  limit—not selection, mandate, or reversal of a persistent design, protocol,
  schema, architecture, or operational choice;
- the claim is not a whole-system or whole-protocol correctness certificate;
- no material premise depends on product/version semantics, runtime
  observation, an authority source, or stale/moved subject state; and
- no security/privacy boundary, safety exposure, compatibility contract,
  migration, high-blast-radius change, or material `unmapped` terrain bears
  load.

If any condition fails, use `standard` (or `high-assurance` when its trigger
fires). A short proof does not make a downstream decision lightweight. A
counterexample may remain focused only when it rejects the bounded proposition
without selecting or mandating what replaces it.

If more than one property family bears load, use `standard`; cross-family
reconciliation is not a focused answer. A system-level scalability, capacity,
or whole-protocol certificate is also `standard` even when one local operation
or invariant is simple. If a supposedly focused question lacks a closed,
supplied model or scope, that focused condition failed.
In particular, comparing asymptotic resource behavior with numerical stability crosses `P7` and `P8`
and therefore uses `standard`, even when one finite counterexample is enough to
refute the equivalence claim.
A comparison spanning distributed ordering/history and replica convergence crosses `P3` and `P4`
and therefore uses `standard`, even when a short counterexample refutes it.

Focused answers the bounded property only. If that result is being used to select,
mandate, or reverse a persistent schema, architecture, protocol, or operational decision,
use `standard` even when the proof itself is bounded.

- Return inline in at most six short bullets or 250 visible words.
- Before emitting, count the bullets and visible words; compress to the focused
  contract rather than adding a record solely because the draft is verbose.
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

Pinned product/version semantics alone require `standard`, not `high-assurance`.
Escalate only when a separate high-assurance trigger such as safety, security,
or irreversibility bears load.

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

A pending empirical premise does not make an applicable formal module `unmapped`.
When an adequate module and model exist but an observation is pending, mark the
family `fired`, keep the result `incomplete` or `conditional`, and close it
through `empirical_closure`. Reserve `unmapped` for missing formal apparatus,
semantics, or a model that cannot yet be instantiated even conditionally.

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

Cross-check these observable cues before marking a family:

- whole-protocol correctness, safety, liveness, transitions, or starvation
  fires `P1`; scheduling, histories, isolation, or happens-before also fires
  `P3`;
- facts, dependencies, schemas, keys, representation, or enforceability fires
  `P2`;
- distributed visibility, replication, session guarantees, convergence, or
  consensus fires `P4`; a distributed ordering claim may fire both `P3` and
  `P4`;
- reliability, durability, rollback, fault containment, or recovery fires
  `P5`;
- authentication, authorization, authority, confidentiality, privacy, or
  information flow fires `P6`;
- algorithms, complexity, capacity, latency budgets, queue stability, resource
  bounds, or lower bounds fires `P7`; an unknown accelerator or hardware
  resource model is `P7: unmapped`, not `not-applicable`;
- probability, measurement uncertainty, value of information, rounding,
  conditioning, or numerical stability fires `P8`; and
- product versions, external contracts, regulatory interfaces, migration,
  subject revision, staleness, compatibility, or lifecycle fires `P9`.

These cues are a discovery cross-check, not a closed taxonomy. Multiple rows
often fire; each fired row must name an adequate loaded module from the
registry, and missing theory or inputs must be recorded as `unmapped`.
Do not infer a property family from an implementation label alone; names such
as cache, database, accelerator, or protocol do not substitute for a material
property inside the declared boundary.
A module may appear only in families declared by its `property_families`.
Module adequacy is construct-specific, not merely family-compatible.
Independently load-bearing slices require each adequate specialist module; for
example, asymptotic complexity and numerical stability need both `algorithms-data-structures` and `numerical-analysis-floating-point`.
When correctness depends on an undocumented proprietary hardware execution or memory model,
mark the ordering slice `P3: unmapped` and the missing hardware resource/model apparatus `P7: unmapped`
until adequate semantics exist; the accelerator label alone still fires no
family.
For example, a value-of-information question with unmodeled measurement uncertainty marks `P8` as `unmapped` and `P9` as `fired`
with `decision-theory-multiobjective`; that P9 synthesis module does not become
a P8 statistics module. When the measurement model and its required inputs
(population, sampling mechanism, sample size, error tolerance) are available,
the P8 slice fires `probability-statistics-randomization` instead of staying
unmapped — but absent inputs still mean `unmapped`, never a borrowed module.
For mixed-domain claims, reconcile each material slice independently.
Do not let an unmapped external-semantic slice erase an adequately modeled engineering slice.
Fire the adequate engineering module, and separately mark the external semantic
or regulatory interface `unmapped` in its applicable family.
Concrete engineering privacy or information-flow mechanisms fire `P6` with `security-information-flow-privacy`;
missing authoritative external regulatory semantics remain `P9: unmapped`.
Do not swap those statuses or modules.

Coverage is complete only relative to the declared subject, boundary,
inventory, loaded modules, facts, and limits. It never means that the library
exhausts software-and-systems theory.

Load only modules for fired families from
[`reference/modules/index.md`](reference/modules/index.md). If no adequate
module exists, use `unmapped`; never coerce the property into a nearby module.
Coverage `modules` entries use the registry's exact unversioned `module_id`;
carry module versions in derivation/source provenance, not by changing the id.

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
In particular, when a selection depends on an absent or unauthorized external
semantic premise, assess the dependent selection claim as `incomplete` and use
an `underdetermined` synthesis. Refute only a premise or proposal contradicted
by supplied evidence or a hard constraint.
An invalid justification does not establish the opposite external meaning.

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

A `reversal` rejects a premise or proposal; it does not by itself select a replacement.
Keep `selected_option` null unless a separate authorized synthesis establishes
one of the stable alternative ids. `pareto-set` and `underdetermined` always
keep it null; `dominance` names the exact dominant alternative id.
`reversible-probe` keeps `selected_option` null because it authorizes bounded
evidence gathering, not a persistent design alternative.
A rejected current premise can use `reversal` even when replacement selection remains unresolved.
Put the unresolved replacement in residual mismatch and recovery moves rather
than changing the current-premise verdict to `underdetermined`.

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
- `never_attests` must contain at least the exact machine-readable boundaries
  `derivation-correctness-by-envelope`, `empirical-fact-without-observation`,
  and `gauntlet-independence`; additional subject-specific boundaries may be
  added.

Before emitting, rerun the tier gate and cue cross-check. Confirm that every
focused condition is explicitly true; that each material cue, objective,
constraint, uncertainty, authority, and lifecycle input has the correct family
status and adequate module; and that claim state and synthesis outcome answer
the current proposition without inventing a replacement.

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

- Product/version semantics require an exact official source pin at every tier that emits a record.
  When a source register is supplied, copy its exact source id into the
  load-bearing derivation instead of paraphrasing the citation.
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
