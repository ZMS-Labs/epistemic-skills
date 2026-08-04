# Dependability and fault models

```yaml
module_id: dependability-fault-models
version: 1.0.0
property_families: [P5]
trigger_properties: [reliability availability durability recovery or fault-containment claim]
constructs: [fault error failure chain, crash omission timing and Byzantine faults, reliability, availability, recovery, correlated failure]
models: [components services and fault domains over a declared time horizon]
required_inputs: [service requirement, fault classes, independence or correlation assumptions, repair process, horizon]
applicability_template:
  model: define service states fault domains and time horizon
  preconditions: state fault occurrence and repair assumptions
  fact_mapping: anchor topology replication and recovery facts
derivation_templates: [fault to error to service failure, series or parallel reliability under justified independence, recovery-state analysis]
counterexample_obligations: [give an in-model fault sequence that violates the claimed service]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Avizienis et al. 2004 DOI 10.1109/TDSC.2004.2]
  official_product_docs: [pin platform and version for recovery guarantees]
known_exclusions: [unstated independence, security adversaries, legal obligations]
```

Do not collapse reliability, availability, safety, and durability into one
metric. Independence assumptions are load-bearing: shared power, region,
operator, or software lineage can invalidate multiplication of component
failure probabilities.
