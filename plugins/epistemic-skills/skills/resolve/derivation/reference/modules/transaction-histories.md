# Transaction histories

```yaml
module_id: transaction-histories
version: 1.0.0
property_families: [P1, P3]
trigger_properties: [concurrent transaction histories, isolation claims, serializability or recovery requirements]
constructs: [history, conflict graph, conflict serializability, recoverability, strictness, write skew, phantom, MVCC, OCC, locking]
models: [read-write transaction histories under a pinned implementation]
required_inputs: [operations and order, transaction boundaries, required invariant, product and version semantics]
applicability_template:
  model: construct the concrete history and implementation semantics
  preconditions: identify conflicts, dependency edges, and required guarantee
  fact_mapping: anchor operations and product guarantees to revisions
derivation_templates: [history to dependency graph to cycle test to anomaly, standard minimum to pinned implementation to concrete history]
counterexample_obligations: [provide an admitted history when refuting an isolation guarantee]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Berenson et al. 1995 DOI 10.1145/223784.223785]
  official_product_docs: [pin database product and exact version]
known_exclusions: [cross-service atomicity without a distributed model, authorization]
```

Never infer behavior from the isolation-level name. Derive:

```text
standard minimum → product + pinned version → concrete history or dependency graph
→ anomaly admitted or excluded → minimum mechanism meeting the requirement
```

For example, PostgreSQL 18 documents Repeatable Read as preventing phantoms
while still allowing serialization anomalies. That statement applies only with
the official PostgreSQL 18 source pinned and does not establish local runtime
configuration.
