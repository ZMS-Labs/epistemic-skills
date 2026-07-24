# Algorithms and data structures

```yaml
module_id: algorithms-data-structures
version: 1.0.0
property_families: [P7]
trigger_properties: [complexity or optimality claim, data-structure choice, recurrence, amortized or lower-bound claim]
constructs: [O Theta Omega bounds, amortized analysis, recurrence, decision-tree lower bound, output sensitivity, external-memory complexity]
models: [comparison model, word RAM, external-memory model, randomized or deterministic algorithm]
required_inputs: [problem contract, input parameters, operation mix, model, preprocessing, exactness, resource and asymptotic posture]
applicability_template:
  model: freeze problem input output machine and resource
  preconditions: state preprocessing randomization exactness and workload assumptions
  fact_mapping: anchor operation profile and implementation facts
derivation_templates: [per-operation cost to aggregate workload, recurrence solution, counting or adversary lower bound]
counterexample_obligations: [name an out-of-model algorithm or input family when refuting universality]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [pin the canonical theorem or textbook edition used by the derivation]
  official_product_docs: [pin product and version for concrete index or runtime semantics]
known_exclusions: [queue stability, floating-point stability, model-free optimality]
```

Every lower bound fixes the exact problem, input/output contract,
computational/resource model, preprocessing, deterministic or randomized
setting, exactness, posture, and bounded resource. A comparison-sorting lower
bound does not govern word-RAM integer sorting.

“Converged” is relative to the frozen problem, model, constraints, and
objective vector. Changing exactness, preprocessing, parallelism, or resource
objective creates a new subject.
