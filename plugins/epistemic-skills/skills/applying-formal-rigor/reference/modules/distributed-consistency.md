# Distributed consistency

```yaml
module_id: distributed-consistency
version: 1.0.0
property_families: [P3, P4, P5]
trigger_properties: [replicated histories, client visibility or ordering guarantees, logical clocks, quorum or consensus claims]
constructs: [linearizability, sequential consistency, causal consistency, session guarantees, eventual convergence, happened-before, quorum, consensus, CRDT]
models: [scoped object session or transaction histories with explicit failures and availability]
required_inputs: [scope, history and client model, ordering and visibility relations, convergence requirement, failure assumptions]
applicability_template:
  model: declare objects clients histories failures and availability obligation
  preconditions: state the exact consistency predicate or clock condition
  fact_mapping: anchor operations and system guarantees to subject and product revisions
derivation_templates: [predicate implication or counterexample over a named history, quorum intersection under stated replica assumptions]
counterexample_obligations: [give a history witness for non-implication or violated visibility/order]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Viotti and Vukolic 2016 DOI 10.1145/2926965, Lamport 1978 DOI 10.1145/359545.359563]
  official_product_docs: [pin product and version for implementation guarantees]
known_exclusions: [one universal total consistency chain, unstated correlated faults]
```

Consistency predicates form scoped implication relationships, not one
universal strength chain. Record object/session/transaction scope, history and
client model, ordering and visibility relations, convergence, failures, and
availability before comparing them.

Lamport's clock condition is one-way: `a → b` implies `C(a) < C(b)`. The
converse is false; scalar timestamps do not distinguish causality from
concurrency. A process-id tie-break can extend clock order to a deterministic
total order consistent with happened-before, but that order is not causality.
