# Security, information flow, and privacy

```yaml
module_id: security-information-flow-privacy
version: 1.0.0
property_families: [P1, P6]
trigger_properties: [authorization boundary, confidentiality or integrity claim, information-flow or privacy guarantee]
constructs: [threat model, reference monitor, capability, least privilege, noninterference, cryptographic assumption, differential privacy]
models: [subjects objects actions trust boundaries attackers and observations]
required_inputs: [assets, principals, authority transitions, attacker capabilities, policy, trusted computing base]
applicability_template:
  model: define principals authority state transitions attacker and observable outputs
  preconditions: state enforcement completeness tamper resistance and cryptographic or privacy assumptions
  fact_mapping: anchor endpoint policy identity and implementation facts
derivation_templates: [authorization-state reachability, information-flow trace comparison, privacy-budget composition]
counterexample_obligations: [provide an unauthorized reachable transition or distinguishing observation]
result_vocabulary: [established, refuted, conditional, incomplete]
canonical_sources:
  primary_theory: [Saltzer and Schroeder 1975 DOI 10.1109/PROC.1975.9939, Dwork 2006 DOI 10.1007/11787006_1]
  official_product_docs: [pin identity cryptography and policy-engine products and versions]
known_exclusions: [legal compliance conclusions, unmodeled side channels, relational integrity as authorization]
```

Schema keys and foreign keys constrain stored relations; they do not prove
that a caller was authorized to cause a state transition. Model principals,
authority checks, and reachable writes separately. External legal meaning is
outside this software module and remains `unmapped` until supplied by an
authorized domain process.
