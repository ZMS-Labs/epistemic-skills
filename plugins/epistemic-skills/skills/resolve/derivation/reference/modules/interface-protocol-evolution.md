# Interface and protocol evolution

```yaml
module_id: interface-protocol-evolution
version: 1.0.0
property_families: [P1, P5, P9]
trigger_properties: [public contract change, schema or protocol migration, version skew, backward or forward compatibility claim]
constructs: [behavioral subtyping, precondition weakening, postcondition strengthening, protocol state refinement, backward compatibility, forward compatibility]
models: [versioned clients servers messages states and deployment transitions]
required_inputs: [old and new contracts, supported client/server versions, rollout order, fallback and rollback semantics]
applicability_template:
  model: define versioned actors messages states and allowed traces
  preconditions: state substitutability compatibility and rollout obligations
  fact_mapping: anchor contracts versions deployment topology and migration steps
derivation_templates: [old-client/new-server trace inclusion, refinement or simulation, version-skew state reachability]
counterexample_obligations: [provide a supported version pair or trace that violates the compatibility claim]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Liskov and Wing 1994 DOI 10.1145/197320.197383]
  official_product_docs: [pin protocol schema runtime and platform versions]
known_exclusions: [legal or regulatory interpretation, unstated ecosystem consumers]
```

A small diff can alter a public or security-sensitive contract and therefore
require high assurance. Analyze supported version pairs, rollout and rollback
states, and counterexample traces. External regulatory semantics remain
outside this module even when the engineering controls are fully described.
