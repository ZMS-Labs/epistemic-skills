# Decision theory and multiobjective synthesis

```yaml
module_id: decision-theory-multiobjective
version: 1.0.0
property_families: [P9]
trigger_properties: [multiple feasible alternatives, competing authorized objectives, priority change, value-of-information question]
constructs: [feasibility, dominance, Pareto set, lexicographic order, weighted utility, minimax, minimax regret, sensitivity, value of information]
models: [finite alternatives objectives constraints scenarios and authority-bound priority rules]
required_inputs: [alternatives including null, hard constraints, authorized objectives, authority reference, priority rule, uncertainties]
applicability_template:
  model: define feasible set objective vectors scenarios and decision authority
  preconditions: verify objective authorization and rule applicability
  fact_mapping: anchor values and authorizations separately from technical observations
derivation_templates: [constraint filter to Pareto frontier, authorized lexicographic comparison, sensitivity sweep, reversible-probe value comparison]
counterexample_obligations: [give a feasible option or priority setting that defeats a claimed dominance result]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [pin the exact decision rule source when a theorem rather than an operator rule bears load]
  official_product_docs: []
known_exclusions: [invented utility, engineering taste as authority, forced selection from a Pareto set]
```

Technical property results do not authorize priorities. Filter infeasible
options, compute only the comparison justified by the operator's rule, and
preserve a Pareto set when no tie-break exists. A priority-rule change voids
the normative synthesis even when the code revision is unchanged.

A `reversible-probe` is justified when a bounded preregistered observation has
greater expected decision value than more argument or irreversible action.
