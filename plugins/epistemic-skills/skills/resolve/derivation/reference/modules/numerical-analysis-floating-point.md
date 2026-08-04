# Numerical analysis and floating point

```yaml
module_id: numerical-analysis-floating-point
version: 1.0.0
property_families: [P7, P8]
trigger_properties: [floating-point equivalence, numerical accuracy conditioning stability cancellation overflow or underflow claim]
constructs: [conditioning, forward error, backward error, numerical stability, catastrophic cancellation, rounding, IEEE 754 semantics]
models: [real-valued problem plus finite floating-point representation and operation semantics]
required_inputs: [formula or algorithm, input domain and scale, precision and rounding mode, required error metric]
applicability_template:
  model: separate the mathematical problem from floating-point execution
  preconditions: state conditioning range precision rounding and exceptional-value behavior
  fact_mapping: anchor implementation operations and platform semantics
derivation_templates: [condition number to data-error amplification, forward or backward error bound, cancellation counterexample]
counterexample_obligations: [supply an input family exposing instability overflow underflow or cancellation]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Goldberg 1991 DOI 10.1145/103162.103163, IEEE 754-2019]
  official_product_docs: [pin language compiler and hardware floating-point semantics when material]
known_exclusions: [same Big-O as proof of numerical equivalence, undocumented fast-math behavior]
```

Equal asymptotic running time does not imply equal numerical behavior. Compare
conditioning and the algorithm's forward/backward error under a named
floating-point model; surface cancellation and exceptional-value witnesses.
