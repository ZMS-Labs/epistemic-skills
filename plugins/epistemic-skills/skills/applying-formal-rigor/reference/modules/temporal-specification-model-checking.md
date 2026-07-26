# Temporal specification and model checking

```yaml
module_id: temporal-specification-model-checking
version: 1.0.0
property_families: [P1, P3, P5]
trigger_properties: [state-machine correctness, safety or liveness claim, fairness or progress obligation, refinement claim]
constructs: [transition system, invariant, safety, liveness, fairness, temporal logic, refinement, counterexample trace]
models: [labeled transition systems with initial states and fairness assumptions]
required_inputs: [state variables, initial states, transition relation, safety and liveness predicates, fairness assumptions]
applicability_template:
  model: define the transition system and execution semantics
  preconditions: state initiality transition and fairness obligations
  fact_mapping: anchor implementation transitions to the abstract model
derivation_templates: [inductive invariant proof, temporal counterexample trace, refinement mapping]
counterexample_obligations: [supply a finite or lasso-shaped trace when refuting universal temporal behavior]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Pnueli 1977 DOI 10.1109/SFCS.1977.32]
  official_product_docs: []
known_exclusions: [performance capacity, unmodeled scheduler behavior, physical fault probability]
```

Safety means that bad states do not occur; liveness means that required good
events eventually occur. Mutual exclusion proves neither starvation freedom
nor progress. If a schedule keeps an actor enabled while indefinitely denying
entry, it is a liveness counterexample even when the safety invariant holds.
