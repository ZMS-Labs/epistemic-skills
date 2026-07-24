# applying-formal-rigor v2 — software-and-systems decision discipline

**Date:** 2026-07-23  
**Status:** Draft design for operator review; production skill deliberately unchanged  
**Type:** Major redesign of an existing epistemic discipline  
**Subject:** `plugins/epistemic-skills/skills/applying-formal-rigor/` on the branch base revision  
**Companion:** [`2026-07-23-applying-formal-rigor-v2-fixture-matrix.md`](2026-07-23-applying-formal-rigor-v2-fixture-matrix.md)

## Decision summary

Preserve the current skill's three valuable behaviors:

1. **name the precise construct** rather than the first salient label;
2. **derive rather than assert**;
3. **sweep beyond the first salient concern**.

Replace the current implementation of those behaviors with an open-world,
model-aware discipline:

- a **decision frame** establishes the subject, alternatives, constraints,
  operator-authorized objectives, priority rule, assumptions, empirical
  premises, and rigor tier;
- a universal **property inventory** prevents single-lens reasoning without
  pretending its categories exhaust formal theory;
- extensible **specialist modules** carry the formal apparatus;
- every formal claim follows the applicability chain
  `model → preconditions → fact mapping → derivation → result → residual mismatch`;
- coverage is recorded as `fired`, `not-applicable`, or `unmapped`;
- formal results, empirical closure, and normative synthesis are separate;
- synthesis may end in `dominance`, `pareto-set`, `conditional`,
  `underdetermined`, `reversal`, or `reversible-probe`;
- every run emits a revision-bound `formal-rigor-record@2`.

“Exhaustive” means **exhaustive relative to the declared subject scope,
property inventory, loaded modules, input facts, and coverage limits**. It
never means that one fixed list exhausts software-and-systems theory.

## Problem

### 1. The current battery contains load-bearing formal errors

The existing worked example treats ranked contact methods as a nontrivial
multivalued dependency and concludes that the fixed-column representation is a
4NF violation. That derivation is invalid: a nontrivial MVD requires the
relevant attribute sets to vary independently. In the example, `method` and
`priority` are paired by the stated functional dependencies, so the claimed
MVD is not established. A fixed-cardinality representation can still be a bad
design, but it needs a representation, integrity, query-shape, and evolution
argument—not a false 4NF proof.

The current battery also:

- presents SQL isolation levels as if the standard's minimum phenomena were
  universal product behavior;
- renders consistency models as one total strength chain rather than a
  scoped partial order of predicates;
- describes Lamport clocks as “total order, no causality capture,” obscuring
  the happened-before relation, the one-way clock condition, and the separate
  tie-break used to construct a total order;
- states lower bounds without always fixing the computational model,
  preprocessing allowance, randomization, exactness, or resource model;
- treats architecture heuristics and formal results as one undifferentiated
  theory lens.

A discipline whose purpose is to prevent formal-sounding undershoot must not
ship canonical examples that commit it.

### 2. Property proof and decision choice are conflated

Formal theory can establish properties such as:

- option A is conflict-serializable under history model H;
- option B uses asymptotically less space in computational model M;
- option C violates invariant I;
- A and B are Pareto-incomparable.

It cannot by itself establish “therefore choose A” unless the decision also
records the hard constraints, operator-authorized objectives, priority or
trade-off rule, acceptable risk, and acceptable cost. The current output shape
normally forces a verdict and can therefore hide a value judgment inside a
formal derivation.

### 3. Seven enumerated lenses create a false closure signal

Accounting for every member of a fixed list proves completeness only over that
list. The present seven lenses are deep in relational and data-system topics,
but omit or thinly cover specification and temporal correctness, dependability
and fault models, security and privacy, queueing and capacity, real-time
scheduling, probability and statistics, numerical stability, and interface or
protocol evolution.

The repair is not an ever-growing encyclopedia. It is a stable universal
property inventory plus separately versioned specialist modules and an
`unmapped` state for material terrain the current library cannot cover.

### 4. Naming a theorem is not proving that it applies

The current “name → derive” rule lacks an explicit applicability proof. Every
formal result depends on a model and preconditions. The system facts must be
mapped to those preconditions before the theorem bears load. Without that
mapping, CAP, 4NF, the Master Theorem, linearizability, Little's Law, Amdahl's
Law, or an Ω lower bound can become theorem name-dropping.

### 5. The trigger and cost model are too coarse

“Two viable options” is not enough to justify a full theory sweep. Materiality,
uncertainty, reversibility, expected loss, downstream dependence, and analysis
cost are measurable axes. A local reversible choice should not pay the same
ceremony as a public protocol, storage migration, authorization boundary, or
safety-critical decision.

### 6. The output does not fulfill the router's revision-bound contract

The router describes formal-rigor output as a derived verdict with
`subject.ref`, `subject.revision`, `valid_while`, and `coverage_limits`, but the
skill's own output instructions do not require a structured record carrying
those fields or the facts from which the result was derived. Staleness is
therefore declared at the collection boundary but not detectable in the
member artifact.

### 7. Broad behavioral efficacy is untested

The suite's latest audit found the method sound for three narrow decisions but
conditional as a general behavioral discipline. Prose review alone cannot show
that the redesigned skill catches theorem misuse, missed terrain, forced
closure, overtriggering, stale subjects, and legitimate unmapped cases. A
blinded fixture battery must precede production edits.

## Scope

This skill governs **software-and-systems property analysis and decision
synthesis**. Its subjects include algorithms, data structures, schemas,
transactions, distributed protocols, caches, APIs, type and state models,
security and privacy boundaries, performance and capacity, numerical code,
reliability mechanisms, and architecture decisions whose claims can be made
falsifiable.

It does not claim to cover arbitrary mathematics, natural-science inference,
policy analysis, or moral choice. It may consume those results when another
discipline establishes them, but its own universal inventory is scoped to
software and systems.

## Non-goals and boundaries

- **Not reconnaissance.** When the territory is unfamiliar, `blindspot-pass`
  still runs first and rewrites the request.
- **Not literature review.** `evidence-research` remains the independent owner
  of scholarly discovery, reception, and durable holdings. Formal-rigor names
  the empirical or scholarly premise that needs support; research returns an
  evidence record; formal-rigor then closes or conditions the derivation.
- **Not an adversarial gate.** `gauntlet` independently attacks a frozen,
  consequential result. A well-formed formal-rigor record is dossier input,
  never proof that its derivation is correct or independent.
- **Not acceptance testing.** Runtime or UI completion claims remain with the
  workflow verification layer and `evidence-locked-uat` where applicable.
- **Not option-generation theater.** The skill requires an explicit null or
  status-quo option and surfaces an obviously incomplete option set, but broad
  ideation belongs upstream.
- **Not a universal theorem encyclopedia.** Modules are bounded references;
  `unmapped` is preferable to coercing unfamiliar terrain into a nearby label.
- **Not a forced-choice engine.** A Pareto set or underdetermined result is a
  successful result when the decision frame does not justify a unique choice.

## The three disciplines, redesigned

### Discipline 1 — Name the precise model and construct

A construct is precise only when the record identifies:

1. the formal object or predicate;
2. the model in which it is defined;
3. the construct's scope and parameters;
4. the theorem, definition, or official product guarantee being used;
5. the source version or edition when behavior can vary.

Examples:

- not “normalization,” but the declared relation schema, FDs/MVDs, keys, and
  exact normal-form condition;
- not “Repeatable Read prevents/allows phantoms,” but the SQL-standard minimum
  plus the actual database and version semantics and a concrete history;
- not “causal consistency is weaker than sequential consistency” as a scalar
  slogan, but the two predicates over a named history and scope;
- not “Ω(n log n),” but the problem, comparison or machine model, preprocessing
  allowance, randomization, exactness, and resource being lower-bounded;
- not “safe,” but a named safety property under a named fault and attacker
  model.

### Discipline 2 — Prove applicability, then derive

Every load-bearing construct follows this chain:

```text
model
  → preconditions
  → fact mapping
  → derivation
  → result
  → residual mismatch
```

**Model.** Name the formal world: relation schema, execution history,
transition system, failure model, attacker model, computational model,
queueing assumptions, scheduling model, numeric representation, or equivalent.

**Preconditions.** Enumerate every theorem or product-guarantee precondition
that bears load. Hidden preconditions are formal debt.

**Fact mapping.** Map each precondition to an observation, interpretation,
assumption, value, or authorization. Observations require revision-pinned
anchors. An unverified empirical premise cannot silently become a theorem
premise.

**Derivation.** Show the finite chain from the mapped premises to the result.
A theorem name with no instantiated steps is an assertion.

**Result.** State one of `established`, `refuted`, `conditional`, or
`incomplete` for that property claim. A counterexample or witness is required
when it is the shortest way to refute a universal claim.

**Residual mismatch.** State what the model omits or idealizes: clock behavior,
correlated faults, constants and I/O, workload nonstationarity, retries,
operator behavior, numerical conditioning, deployment skew, or other reality
outside the proof.

If the chain breaks, the result is conditional or incomplete. More formal
vocabulary does not repair a missing mapping.

### Discipline 3 — Sweep the property terrain, then synthesize without forced closure

Run the universal property inventory below. For each family, record exactly one
coverage state:

- `fired` — a material property in this family exists and one or more suitable
  specialist modules were loaded;
- `not-applicable` — no material property in this family exists inside the
  declared subject boundary; give a reason tied to the boundary;
- `unmapped` — a material property exists, but no adequate module, model, or
  input is available. Name the missing terrain and carry it into
  `coverage_limits`.

`unmapped` is not a softer synonym for `not-applicable`. A load-bearing
`unmapped` property prevents an unconditional dominance result. It yields
`underdetermined`, a conditional result, an escalation, or a bounded
`reversible-probe`.

## Definition of relative exhaustiveness

A run may claim **coverage-complete-relative-to-scope** only when:

1. the subject boundary and actors are explicit;
2. the universal property inventory has one recorded state per family;
3. every `fired` family names the loaded modules;
4. every module's required facts and preconditions are accounted for;
5. every material uncovered property is `unmapped`, not hidden;
6. the record states all coverage limits;
7. the subject revision and source versions are pinned.

This claim never means “no other formal theory exists” or “no defect exists.”
It means the declared property inventory has been honestly reconciled against
the declared subject and the current module library.

## Decision frame — required before synthesis

Every run records:

| Field | Requirement |
|---|---|
| `question` | The exact property or choice to resolve. |
| `subject.ref` | Repository path, design document, URL, named system, or content hash. |
| `subject.revision` | Git SHA, document version, product version, content hash, or `null` with a visible staleness limit. |
| `system_boundary` | Components, environment, time horizon, actors, and excluded territory. |
| `alternatives` | Every option under comparison, each with a stable id. |
| `null_option` | Status quo / do nothing / reject all; mandatory for a decision fork. |
| `hard_constraints` | Conditions an option must satisfy to remain feasible. |
| `authorized_objectives` | Outcomes the operator has authorized the analysis to optimize or protect. |
| `priority_rule` | How objectives are ordered or traded off. |
| `assumptions` | Stated premises not currently observed. |
| `empirical_premises` | Workload, latency, implementation, human-behavior, or environment claims requiring observation. |
| `uncertainty_posture` | Expected, worst-case, high-probability, minimax, risk bound, or other posture. |
| `rigor_tier` | `focused`, `standard`, or `high-assurance`, with trigger reason. |

Allowed priority rules at the floor are:

- `constraint-satisfaction` — choose any feasible option; no hidden ranking;
- `lexicographic` — objectives are ordered by operator authority;
- `weighted-utility` — weights are operator-authorized and sensitivity-tested;
- `minimax` — minimize the worst authorized loss;
- `minimax-regret` — minimize worst regret over named scenarios;
- `pareto-only` — report the non-dominated set and do not pick;
- `custom` — the operator's rule is quoted or referenced exactly.

Missing priorities are not inferred from engineering taste. When alternatives
trade authorized objectives and no rule resolves the trade, the synthesis is
`pareto-set` or `underdetermined`.

## Rigor tiers

### `focused`

Use for a bounded formal question or low-blast-radius, reversible choice:
Big-O under a named model, one normal-form test, one history/anomaly analysis,
one invariant proof, or a specific correctness challenge.

Floor:

- complete the decision-frame fields relevant to the question;
- include the null option only when a choice is being made;
- enumerate the nine property families compactly;
- load only the modules that fire;
- emit the full revision-bound record.

### `standard` — default for material forks

Use when two or more material alternatives differ on measurable properties or
a design justification will bear downstream load.

Floor:

- complete decision frame, including null option and priority rule;
- full property-family reconciliation with reasons;
- applicability chain for every load-bearing construct;
- formal/empirical/normative separation;
- explicit concessions and recovery moves;
- no unconditional choice with a load-bearing `unmapped` property.

### `high-assurance`

Use when any of the following is present: irreversible migration, security or
privacy boundary, safety or financial exposure, public compatibility contract,
cross-service consistency mechanism, high blast radius, model-sensitive proof,
or explicit operator request.

Adds:

- primary-theory source pins and official product/version documentation for
  every load-bearing construct;
- mechanized calculation, model check, proof assistant, database reproduction,
  or executable counterexample where feasible;
- preregistered empirical closure for every material runtime premise;
- sensitivity analysis over authorized priorities and uncertain parameters;
- explicit handoff recommendation to `gauntlet` when its independent trigger
  is present.

High assurance still does not certify itself. Gauntlet remains independent.

## Trigger and ceremony gate

The skill fires when:

- the operator explicitly asks for a formal derivation, complexity proof, or
  rigorous design comparison;
- a material design decision has multiple viable alternatives with different
  measurable or theorem-governed properties;
- a single proposed design needs a correctness confirmation or reversal;
- review feedback asserts a design theorem, lower bound, consistency guarantee,
  isolation property, safety property, or equivalent formal claim.

It does not fire for:

- pure preference where no measurable property or theorem distinguishes the
  options;
- a mechanical edit with one viable implementation;
- a low-cost reversible choice whose maximum plausible loss is below the cost
  of analysis, unless the operator explicitly requests rigor.

Tier selection uses the observable vector:

```text
cost of error × uncertainty × downstream dependence × irreversibility
versus
cost of analysis and cost of a reversible probe
```

A skipped or focused pass is not lower quality when the vector says ceremony
would cost more than the decision can lose.

## Universal property inventory

The inventory is stable enough to force breadth but intentionally broader than
any one theory taxonomy.

| ID | Property family | Canonical questions |
|---|---|---|
| `P1` | **Functional semantics and invariants** | What behaviors are allowed? What safety/liveness properties, pre/postconditions, state transitions, refinement obligations, or totality claims must hold? |
| `P2` | **State, data representation, and integrity** | What facts and dependencies exist? Which states are representable? Are decompositions lossless, constraints enforceable, and derived data coherent? |
| `P3` | **Time, ordering, and concurrency** | What histories, conflicts, happens-before relations, isolation anomalies, atomicity, scheduling, or progress properties matter? |
| `P4` | **Distribution, replication, and consistency** | What scope, failure assumptions, visibility/order predicates, quorum or consensus guarantees, merge semantics, and residual windows apply? |
| `P5` | **Dependability, faults, and recovery** | Which faults, errors, and failures are in model? What reliability, availability, safety, repair, rollback, durability, and correlated-failure properties follow? |
| `P6` | **Security, privacy, and information flow** | Who is the adversary? What authorization, confidentiality, integrity, noninterference, cryptographic, privacy-budget, and side-channel properties apply? |
| `P7` | **Algorithms, resources, capacity, and real time** | What computational/I/O/parallel model, workload, bounds, queue stability, saturation point, deadline, space-time trade, and lower bound apply? |
| `P8` | **Uncertainty, measurement, randomization, and numerical behavior** | What probability model, estimator, confidence/calibration, randomized guarantee, conditioning, rounding, stability, and measurement error apply? |
| `P9` | **Evolution, interfaces, and operations** | What compatibility, behavioral-subtyping, version-skew, migration, reversibility, observability, operability, failure-domain, and lifecycle properties apply? |

ISO/IEC 25010:2023 may be used as an independent quality-characteristic
cross-check, not as a substitute for formal derivation and not as proof that
this inventory is globally exhaustive.

## Specialist module architecture

The universal inventory routes to modules. A module is a bounded formal
apparatus, not a separate skill and not an invocation trigger of its own.

Initial module set proposed for v2:

| Module id | Primary families | Formal terrain |
|---|---|---|
| `relational-dependencies` | P2 | FDs, MVDs, JDs, keys, normal forms, lossless join, dependency preservation, relational algebra |
| `transaction-histories` | P1, P3 | histories, conflicts, dependency graphs, serializability, recoverability, isolation, MVCC/OCC/locking |
| `distributed-consistency` | P3, P4, P5 | scoped consistency predicates, session guarantees, clocks, quorums, consensus, CRDTs, transactions across services |
| `algorithms-data-structures` | P7 | asymptotic and amortized bounds, recurrences, lower bounds, data-structure profiles, external-memory and output-sensitive analysis |
| `types-program-logics` | P1, P2 | ADTs, refinements, Hoare logic, invariants, totality, illegal states, parametricity |
| `temporal-specification-model-checking` | P1, P3, P5 | transition systems, temporal logic, safety/liveness, refinement, model checking, counterexamples |
| `dependability-fault-models` | P5 | fault/error/failure taxonomy, crash/omission/timing/Byzantine models, reliability, availability, recovery, fault injection |
| `security-information-flow-privacy` | P1, P6 | threat models, authorization/capabilities, secure information flow, cryptographic assumptions, differential privacy |
| `queueing-capacity-parallelism` | P5, P7, P8 | arrival/service models, Little's Law, queue stability, backpressure, contention, Amdahl-style limits, tail behavior |
| `real-time-scheduling` | P3, P7 | deadlines, WCET, utilization bounds, schedulability, priority inversion |
| `probability-statistics-randomization` | P7, P8 | expected/high-probability bounds, randomized algorithms, estimation, power, calibration, Bayesian updating |
| `numerical-analysis-floating-point` | P7, P8 | conditioning, forward/backward error, stability, cancellation, overflow/underflow, IEEE 754 semantics |
| `interface-protocol-evolution` | P1, P5, P9 | behavioral subtyping, protocol state compatibility, schema/API migration, version skew, backward/forward compatibility |
| `architecture-quality-attributes` | P5, P7, P9 | coupling/cohesion, failure domains, derived/base state, reversibility, operability; every qualitative term must be operationalized or labeled heuristic |
| `decision-theory-multiobjective` | synthesis | feasibility, dominance, Pareto sets, utility, minimax/regret, sensitivity, value of information |

### Module contract

Every module must declare:

```yaml
module_id: <stable id>
version: <module version>
property_families: [P1, ...]
trigger_properties: [<observable property, not vague keywords alone>]
constructs: [<formal constructs>]
models: [<supported model classes>]
required_inputs: [<facts needed before derivation>]
applicability_template:
  model: ...
  preconditions: ...
  fact_mapping: ...
derivation_templates: [<bounded chains>]
counterexample_obligations: [<when a witness is required>]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [<DOI/edition>]
  official_product_docs: [<product + pinned version rule>]
known_exclusions: [<terrain this module does not cover>]
```

A module may say “this claim is heuristic unless measured.” It may not promote
an engineering slogan to theorem status merely because it lives in the module
library.

## Required formal corrections

### Correction 1 — MVD and 4NF

Remove the current ranked-contact 4NF proof.

A valid canonical 4NF example is:

```text
user_delivery(user_id, contact_method, notification_topic)
```

Suppose a user's set of contact methods varies independently of the user's set
of notification topics. Then:

```text
user_id ↠ contact_method
user_id ↠ notification_topic
```

The MVDs are nontrivial and `user_id` is not a superkey of the three-attribute
relation, so the schema is not in 4NF. The lossless decomposition is:

```text
user_contact_method(user_id, contact_method)
user_notification_topic(user_id, notification_topic)
```

The ranked-contact fork may remain as a separate example, but its derivation
must concern fixed cardinality, null/slot invariants, query and index shape,
migration cost, and evolution. It must not say fixed columns are inherently
“unindexable”: products such as PostgreSQL can combine multiple indexes with
bitmap `OR`; the relevant result is that the fixed-column design couples the
predicate and index plan to slot count.

### Correction 2 — isolation levels

Derive isolation behavior as:

```text
standard minimum definition
→ actual database + pinned version documentation
→ concrete history / dependency graph
→ anomaly admitted or excluded
→ minimum mechanism satisfying the requirement
```

Do not infer implementation behavior from the level name. PostgreSQL 18, for
example, documents Repeatable Read as preventing phantoms while still allowing
serialization anomalies. The product/version anchor is part of the fact
mapping.

### Correction 3 — consistency ordering

Do not render consistency as one total chain. Record:

- object, session, or transaction scope;
- history and client model;
- ordering and visibility relations;
- convergence requirements;
- failure and availability assumptions.

Compare predicates by implication only where the named definitions justify it.
Otherwise record incomparability or a scoped relation. A diagram may be a
partial order; a mnemonic chain must never carry a proof.

### Correction 4 — Lamport clocks

State the happened-before relation as a partial order. Lamport's clock
condition gives the one-way implication:

```text
a → b  implies  C(a) < C(b)
```

The converse does not hold; scalar timestamps alone cannot distinguish
causally ordered events from concurrent events. A deterministic tie-break such
as process id can extend the clock order to a total order consistent with
happened-before, but that total order is not the causal relation itself.

### Correction 5 — lower bounds and convergence

Every lower-bound claim records:

- exact problem and input/output contract;
- computational or resource model;
- allowed preprocessing and indexing;
- deterministic or randomized setting;
- exact or approximate result requirement;
- worst, average, amortized, expected, or high-probability posture;
- resource bounded: time, comparisons, I/O, communication, space, processors,
  energy, or another named measure.

“Optimization has converged” is valid only under a frozen problem,
computational model, constraints, and objective vector. Changing from exact to
approximate, sequential to parallel, online to preprocessed, comparison to
word-RAM, or one resource objective to another creates a new subject; it is not
another free optimization of the old one.

## Formal, empirical, and normative separation

Every report has three visibly separate layers.

### A. Formal result

What follows inside the named model from the mapped premises?

### B. Empirical closure

Do the implementation, workload, environment, and user-behavior facts satisfy
the premises? Runtime facts require observation. Before a discriminating test,
record:

```yaml
belief: <load-bearing empirical premise>
prediction: <observation expected if correct>
disconfirming_observation: <what counts against it>
test: <bounded action or measurement>
prediction_recorded_before_result: true
```

Then record `result` and `update`. A post-hoc prediction is labeled weaker.
Official product documentation establishes documented semantics for the pinned
version; it does not establish the local deployment's runtime state.

When a scholarly premise bears load, hand it to `evidence-research`. Its matrix
returns evidence and limitations, never the design verdict.

### C. Normative synthesis

Given established/conditional properties, hard constraints, authorized
objectives, and the priority rule, what action—if any—is justified?

No result may move directly from “formally better on metric X” to “choose A”
without showing that X is authorized and how it relates to the other objectives.

## Synthesis outcome vocabulary

### `dominance`

One feasible option is no worse on every authorized objective under the stated
priority rule and strictly better on at least one, with no load-bearing
`unmapped` property. Name what it concedes on non-authorized or out-of-scope
dimensions.

### `pareto-set`

Two or more feasible options are non-dominated. Report the set and the trade-off
frontier. Do not select one unless an authorized tie-break exists.

### `conditional`

A choice follows only if named assumptions, empirical premises, scenarios, or
priority settings hold. State the condition in the verdict itself.

### `underdetermined`

The available facts, option set, coverage, or authorized priorities do not
justify a choice. State exactly what is missing; this is not a request for more
prose.

### `reversal`

The proposed option or premise contradicts the derivation or violates a hard
constraint. For a single-option justification, this is the formal equivalent
of “the requested design is not correct as stated.”

### `reversible-probe`

A bounded experiment has greater expected decision value than more argument or
an irreversible choice. Preregister it, bound cost and blast radius, and state
which possible result changes which branch of the decision.

## Revision-bound output: `formal-rigor-record@2`

The normative artifact is JSON, inline or file-written. Human-readable prose
may accompany it, but downstream consumers rely on the record.

```json
{
  "record": "formal-rigor-record@2",
  "subject": {
    "ref": "<path|url|named subject>",
    "revision": "<git sha|doc version|product version|content hash|null>"
  },
  "valid_while": ["subject-revision-unchanged"],
  "coverage_limits": [],
  "rigor": {
    "tier": "focused|standard|high-assurance",
    "trigger": "<observable trigger>",
    "tier_reason": "<stakes/uncertainty/reversibility reason>"
  },
  "decision_frame": {
    "question": "...",
    "system_boundary": "...",
    "actors": [],
    "alternatives": [
      {"id": "null", "kind": "null-option", "description": "..."}
    ],
    "hard_constraints": [],
    "authorized_objectives": [],
    "priority_rule": {"kind": "pareto-only", "authority_ref": "..."},
    "assumptions": [],
    "empirical_premises": [],
    "uncertainty_posture": "..."
  },
  "coverage": [
    {
      "family": "P1",
      "status": "fired|not-applicable|unmapped",
      "modules": [],
      "reason": "..."
    }
  ],
  "derivations": [
    {
      "id": "d1",
      "module": "<module id + version>",
      "construct": "<precise construct>",
      "sources": {
        "primary_theory": [],
        "official_product_docs": []
      },
      "model": "...",
      "preconditions": [
        {"id": "p1", "statement": "...", "status": "verified|assumed|pending"}
      ],
      "fact_mapping": [
        {
          "precondition_id": "p1",
          "claim_class": "observation|interpretation|assumption|value|authorization",
          "anchor": "<revision-pinned coordinate>"
        }
      ],
      "steps": [],
      "result": {
        "state": "established|refuted|conditional|incomplete",
        "statement": "..."
      },
      "counterexample": null,
      "residual_mismatch": []
    }
  ],
  "empirical_closure": {
    "state": "not-required|pending|observed|post-hoc-weaker|blocked",
    "tests": []
  },
  "synthesis": {
    "outcome": "dominance|pareto-set|conditional|underdetermined|reversal|reversible-probe",
    "selected_option": null,
    "basis": [],
    "conditions": [],
    "concessions": [],
    "recovery_moves": []
  },
  "never_attests": [
    "derivation-correctness-by-envelope",
    "empirical-fact-without-observation",
    "gauntlet-independence"
  ]
}
```

### Record invariants

- Standard and high-assurance records contain exactly one coverage entry for
  every `P1`–`P9`; focused records do the same compactly.
- A decision fork includes exactly one `null-option` alternative.
- Every fired family names at least one module.
- Every derivation names a model, at least one precondition, fact mapping, a
  result state, and residual mismatch (which may be an explicit empty list).
- A load-bearing `unmapped` family appears in `coverage_limits` and forbids
  unconditional `dominance`.
- `pareto-set` and `underdetermined` have `selected_option: null` unless a later,
  separately authorized tie-break causes a new record.
- A null subject revision cannot claim `subject-revision-unchanged`; it carries
  an explicit freshness coverage limit instead.
- A material change to subject revision, system boundary, option set, hard
  constraints, authorized objectives, priority rule, formal model, or product
  version voids the record. Re-fire; do not patch the old verdict.
- The record's envelope attests structure, provenance, and validity window only.
  It never attests that the derivation is correct.

## Source policy

### Primary theory

Load-bearing definitions and theorems cite the canonical paper, standard, or
edition in the module source register. A secondary explanation may aid
readability but cannot be the only source for the formal claim.

### Product behavior

Behavior that can vary by implementation cites official documentation pinned
to product and version. “SQL Repeatable Read,” “Redis consistency,” “Java
memory model,” or “PostgreSQL index behavior” without a version and official
source is incomplete fact mapping.

### Local facts

Code, schemas, configuration, benchmarks, and environment state use immutable
or revision-bound coordinates. Documentation about a deployment is a claim;
observed deployment state requires a probe or recorded runtime artifact.

### Evidence-research boundary

Canonical theory sources are maintained in module source registers. When a
run relies on a material scholarly or empirical proposition—rather than a
formal definition or official implementation guarantee—it invokes
`evidence-research`. The evidence matrix returns to formal-rigor as input.
Formal-rigor retains synthesis ownership.

## Canonical source register for the v2 design

| Terrain | Canonical source or pinned documentation |
|---|---|
| MVD / 4NF | Ronald Fagin, “Multivalued Dependencies and a New Normal Form for Relational Databases,” ACM TODS 2(3), 1977, DOI [`10.1145/320557.320571`](https://doi.org/10.1145/320557.320571). |
| Isolation definitions and implementation gaps | Hal Berenson et al., “A Critique of ANSI SQL Isolation Levels,” SIGMOD 1995, DOI [`10.1145/223784.223785`](https://doi.org/10.1145/223784.223785). |
| PostgreSQL implementation semantics | [PostgreSQL 18 — Transaction Isolation](https://www.postgresql.org/docs/18/transaction-iso.html), version pinned to 18; [Combining Multiple Indexes](https://www.postgresql.org/docs/18/indexes-bitmap-scans.html), version pinned to 18. |
| Distributed consistency predicates | Paolo Viotti and Marko Vukolić, “Consistency in Non-Transactional Distributed Storage Systems,” ACM Computing Surveys 49(1), 2016, DOI [`10.1145/2926965`](https://doi.org/10.1145/2926965). |
| Logical clocks and happened-before | Leslie Lamport, “Time, Clocks, and the Ordering of Events in a Distributed System,” CACM 21(7), 1978, DOI [`10.1145/359545.359563`](https://doi.org/10.1145/359545.359563). |
| Program logic | C. A. R. Hoare, “An Axiomatic Basis for Computer Programming,” CACM 12(10), 1969, DOI [`10.1145/363235.363259`](https://doi.org/10.1145/363235.363259). |
| Temporal specification | Amir Pnueli, “The Temporal Logic of Programs,” FOCS 1977, DOI [`10.1109/SFCS.1977.32`](https://doi.org/10.1109/SFCS.1977.32). |
| Behavioral subtyping | Barbara Liskov and Jeannette Wing, “A Behavioral Notion of Subtyping,” ACM TOPLAS 16(6), 1994, DOI [`10.1145/197320.197383`](https://doi.org/10.1145/197320.197383). |
| Dependability taxonomy | Algirdas Avižienis et al., “Basic Concepts and Taxonomy of Dependable and Secure Computing,” IEEE TDSC 1(1), 2004, DOI [`10.1109/TDSC.2004.2`](https://doi.org/10.1109/TDSC.2004.2). |
| Protection principles | Jerome Saltzer and Michael Schroeder, “The Protection of Information in Computer Systems,” Proceedings of the IEEE 63(9), 1975, DOI [`10.1109/PROC.1975.9939`](https://doi.org/10.1109/PROC.1975.9939). |
| Differential privacy | Cynthia Dwork, “Differential Privacy,” ICALP 2006, DOI [`10.1007/11787006_1`](https://doi.org/10.1007/11787006_1). |
| Queueing relation | John D. C. Little, “A Proof for the Queuing Formula: L = λW,” Operations Research 9(3), 1961, DOI [`10.1287/opre.9.3.383`](https://doi.org/10.1287/opre.9.3.383). |
| Parallel speedup limit | Gene Amdahl, “Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities,” AFIPS 1967, DOI [`10.1145/1465482.1465560`](https://doi.org/10.1145/1465482.1465560). |
| Real-time scheduling | C. L. Liu and James Layland, “Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment,” JACM 20(1), 1973, DOI [`10.1145/321738.321743`](https://doi.org/10.1145/321738.321743). |
| Floating-point analysis | David Goldberg, “What Every Computer Scientist Should Know About Floating-Point Arithmetic,” ACM Computing Surveys 23(1), 1991, DOI [`10.1145/103162.103163`](https://doi.org/10.1145/103162.103163); [IEEE 754-2019](https://standards.ieee.org/ieee/754/6210/). |
| Quality coverage cross-check | [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html), edition pinned to 2023. |

**Evidence status, 2026-07-23:** Consensus discovery resolved the Fagin source;
Scite resolved the listed foundational papers and returned no retraction notice
in the checked records. This is a narrow source/reception check, not a claim
that the literature is exhaustively validated. No durable Zotero/equivalent
library action was available in this environment, so holdings and deposit are
`UNVERIFIED / SKIPPED` and remain a source-management coverage limit.

## Handoff contracts

### To `evidence-research`

Formal-rigor sends only the exact empirical or scholarly premise, its decision
impact, and what evidence would change the derivation. Evidence-research
returns a claim-evidence matrix with reception and holdings limitations. It
does not choose an option.

### Back from `evidence-research`

Map evidence rows to the affected preconditions. Preserve disputed,
incomplete, and unavailable states. Recompute the formal and normative layers;
do not append a confidence adjective to the old verdict.

### To `gauntlet`

A high-stakes `formal-rigor-record@2` may enter the frozen dossier. Gauntlet's
truth gate re-verifies freshness-sensitive facts; its independent panel attacks
the derivations and omitted failure modes. The formal-rigor envelope may prove
well-formedness and provenance only. It never proves independent judgment.

### To `decision-ledger`

A consequential synthesis outcome, load-bearing assumption, operator priority,
or correction may be recorded after the run. The ledger stores prior judgment;
it never upgrades the formal result.

## Anti-rationalizations

| Rationalization | Required response |
|---|---|
| “I named the theorem, so this is formal.” | Show its model, preconditions, fact mapping, derivation, and residual mismatch. |
| “All nine families are accounted for, so nothing is missing.” | The claim is only relative to the declared inventory and scope; material unknown terrain is `unmapped`. |
| “One option is technically superior, so choose it.” | Superior on which operator-authorized objective, under which priority rule? Otherwise report the Pareto set or underdetermination. |
| “The database calls it Repeatable Read.” | Pin the product/version documentation and derive against a concrete history. |
| “This algorithm meets the lower bound.” | Name the problem, model, preprocessing, randomization, exactness, and bounded resource. |
| “Another optimization exists, so the prior result was wrong.” | Did the problem, model, constraints, or objective change? If yes, it is a new subject. |
| “This property is probably covered by architecture.” | Load an adequate module or mark it `unmapped`; architecture is not a dumping ground. |
| “A winner is more useful than an inconclusive result.” | Use only the six synthesis states. Utility does not authorize fabricated determinacy. |
| “Formal reasoning means no benchmark is needed.” | Theory closes formal premises; runtime premises remain empirical and conditional until observed. |
| “The record is structured, so the reasoning is correct.” | Structure and provenance are envelope properties; Gauntlet or independent re-derivation owns adversarial correctness. |

## Fixture gate before production edits

The companion fixture matrix defines a blinded battery covering:

- theorem misuse;
- missed formal terrain;
- forced closure;
- overtriggering and tier inflation;
- stale subjects and moved decision frames;
- legitimate `unmapped` outcomes;
- clean controls where a focused or decisive result is correct.

The fixture implementation must land and produce a recorded RED baseline against
the current production skill before `SKILL.md` or `theory-battery.md` is edited.
The candidate v2 must then pass the declared gate in at least three pinned runs,
while parody strategies fail by design. These are smoke-scale conformance
results, not population accuracy claims.

## Phasing

### Phase A — this design PR

- add this design spec;
- add the fixture matrix;
- do not edit production skill, router, README, manifests, or battery;
- open as draft for operator review.

### Phase B — fixture implementation PR

- create `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/`;
- add staged scenarios/artifacts, scorer-only ground truth, output schema,
  deterministic structural scorer, semantic adjudication protocol, pinned
  arms, and parody probes;
- run and commit current-v1 and neutral baselines;
- preserve RED evidence; do not fix the production skill in the same commit
  that first introduces each failing assertion.

### Phase C — production redesign PR

- rewrite `SKILL.md` to this contract;
- decompose and correct `theory-battery.md` into modules or a module index plus
  bounded references;
- add `formal-rigor-record@2` examples and validation machinery;
- update router handoff shape and compatibility text;
- run the fixture battery until the candidate gate is GREEN;
- reconcile every source correction and every known v1 behavior.

### Phase D — freeze and gate

- freeze the design, implementation diff, fixture results, source register, and
  known coverage limits;
- run Gauntlet if its trigger is present;
- no merge or release is implied by a passing fixture battery.

## Acceptance criteria for this design

- **AC1 — preserved core:** the design retains precise naming, derivation, and
  breadth as explicit disciplines.
- **AC2 — corrected theory:** MVD/4NF, isolation, consistency ordering, Lamport
  clocks, and lower-bound corrections are normative.
- **AC3 — relative exhaustiveness:** subject scope, nine-family inventory,
  module set, `fired|not-applicable|unmapped`, and coverage limits are defined.
- **AC4 — decision authority:** alternatives, null option, hard constraints,
  authorized objectives, priority rule, assumptions, empirical premises, and
  rigor tier are required.
- **AC5 — applicability:** every load-bearing construct follows the six-link
  applicability chain.
- **AC6 — closure vocabulary:** all six synthesis outcomes are defined and
  forced winner selection is prohibited.
- **AC7 — artifact:** `formal-rigor-record@2` carries the router's exact subject,
  revision, validity, and coverage-limit fields.
- **AC8 — proportionality:** focused, standard, and high-assurance tiers have
  observable triggers and floors.
- **AC9 — sources:** canonical primary theory and pinned official product docs
  are required and seeded by the source register.
- **AC10 — independent boundaries:** evidence-research and Gauntlet remain
  separate stages with explicit input/output limits.
- **AC11 — behavioral gate:** the companion matrix specifies blinded traps,
  controls, baselines, parody probes, scoring, and ship thresholds.
- **AC12 — no premature production edit:** this phase changes design artifacts
  only.

## Open implementation decisions

These do not block approval of the conceptual design, but Phase B/C must resolve
them explicitly:

1. whether `formal-rigor-record@2` receives a JSON Schema and stdlib verifier in
   the collection-level `contracts/` directory or a skill-local validator;
2. whether specialist modules remain sections under one reference file or
   become one file per module with a registry index;
3. how semantic derivation judgments are independently adjudicated without
   leaking scorer-only ground truth to the run agent;
4. which module subset is required for the first v2 release versus honestly
   `unmapped` until a later version;
5. how official product-document snapshots are pinned without copying
   copyright-protected documentation into fixtures.

The fixture matrix proposes defaults for all five; operator approval may change
them before production work begins.
