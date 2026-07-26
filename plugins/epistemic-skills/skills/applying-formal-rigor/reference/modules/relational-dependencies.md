# Relational dependencies

```yaml
module_id: relational-dependencies
version: 1.0.0
property_families: [P2]
trigger_properties: [declared dependencies, keys, normal-form claims, decomposition or integrity claims]
constructs: [functional dependency, multivalued dependency, join dependency, candidate key, BCNF, 4NF, 5NF, lossless join, dependency preservation]
models: [finite relation schema with declared dependency set]
required_inputs: [relation attributes, dependency set, candidate-key evidence, intended legal instances]
applicability_template:
  model: declare schema and dependency semantics
  preconditions: establish dependencies and nontriviality conditions
  fact_mapping: anchor each dependency and key claim to the subject revision
derivation_templates: [attribute closure to keys to normal-form test, dependency witness to lossless decomposition]
counterexample_obligations: [supply a legal relation instance when refuting a universal dependency or decomposition claim]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Fagin 1977 DOI 10.1145/320557.320571]
  official_product_docs: [pin database product and version for enforceability or index-plan claims]
known_exclusions: [authorization semantics, workload performance, legal meaning]
```

An MVD `X ↠ Y` requires the Y-values to vary independently of the remaining
attributes given X. Paired `method` and `priority` values do not establish
`user_id ↠ method`.

Canonical 4NF witness: in
`user_delivery(user_id, contact_method, notification_topic)`, if contact
methods and notification topics vary independently, the nontrivial MVDs
`user_id ↠ contact_method` and `user_id ↠ notification_topic` violate 4NF when
`user_id` is not a superkey. The lossless decomposition is
`user_contact_method(user_id, contact_method)` and
`user_notification_topic(user_id, notification_topic)`.

Fixed ranked-contact columns may still lose on slot invariants, query/index
shape, migration cost, or evolution. They are not inherently unindexable;
product/version behavior such as bitmap index combination must be pinned.
