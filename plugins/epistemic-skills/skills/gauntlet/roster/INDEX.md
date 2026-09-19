<!-- GENERATED from registry.json by scripts/render_roster.py — DO NOT EDIT BY HAND -->

# Gauntlet lens registry — INDEX (all counts computed from registry.json)

Registry version: **4.0.0** · total entries: **105**

## Counts by lifecycle status

| status | count |
|---|---:|
| available | 99 |
| retired | 6 |

## Counts by workflow role (available)

| role | count | meaning |
|---|---:|---|
| evaluate | 88 | panel evaluators (the only seats that count toward panel diversity) |
| generate_options | 6 | candidate generation or synthesis; initial open-question Gauntlet phase uses option-set@1 |
| gate | 2 | categorical / process-conformance gates (can block regardless of weighing) |
| adjudicate | 3 | evidence or value adjudication (consume the record; never count as evaluators) |

## Active evaluator capability families (20 unique diagnostic capability atoms)

- **adjudication** (1): Preference sensitivity (`preference-sensitivity-arbitrator`)
- **data-validity** (7): Causal identification (`causal-identification-auditor`); Measurement fitness: construct fit (`construct-validity-auditor`); Derived-data lineage (`data-provenance-auditor`); Evidence-body synthesis (`evidence-synthesis-auditor`); Numeric sourcing and reconciliation (`forensic-accountant`); Measurement fitness: optimization robustness (`measurement-critic`); Quantitative inference assessment (`statistical-validity-critic`)
- **economics** (5): Usable cash and funding timing (`liquidity-runway-auditor`); Participation and user-value coupling (`network-effects-strategist`); Feasible resource allocation (`opportunity-cost-accountant`); Service economics at scale (`unit-economics-adversary`); Decision-relevant learning value (`value-of-information-auditor`)
- **framing-epistemics** (9): Reasoning robustness (`cognitive-bias-auditor`); Claim-to-evidence support (`epistemic-auditor`); Correctness property preservation (`invariant-specification-auditor`); Plan failure pathways (`inversion-thinker`); Problem framing (`polymath-inquisitor`); Unstated premise elicitation (`premise-auditor`); Historical constraint reconstruction (`protocol-archeologist`); Meaning and commitment analysis (`semantic-critic`); Reasoning robustness: continuation mode (`sunk-cost-liberator`)
- **governance-ethics** (8): Decision authority and accountability (`decision-rights-auditor`); Distribution of benefits and burdens (`distributive-justice-auditor`); Capability misuse analysis (`dual-use-adversary`); Ethical reasons and value conflicts (`ethicist`); Lifecycle impacts and obligations (`lifecycle-impact-auditor`); Data-practice harm review (`privacy-surveillance-critic`); Physical harm path analysis (`safety-hazard-auditor`); Stakeholder representation (`stakeholder-representation-auditor`)
- **human-factors** (7): Adoption and migration (`adoption-realist`); User obstruction and recovery (`angry-customer`); Behavioral assumptions (`behavioral-economist`); Automation takeover readiness (`human-automation-handoff-auditor`); Task-focused interface refinement (`ui-ux-polisher`); Scoped accessibility criterion assessment (`wcag-accessibility-expert`); Human workload and capacity assessment (`workforce-load-auditor`)
- **incentives** (1): Conditional incentive analysis (`game-theorist`)
- **interoperability** (1): Consumer contract compatibility (`integration-weaver`)
- **legal-compliance** (5): Decision-record consistency (`compliance-litigator`); Contractual risk allocation (`contract-risk-allocation-auditor`); Rights and permitted-use review (`ip-freedom-to-operate-auditor`); Conflicting obligations review (`jurisdiction-conflicts-auditor`); Disclosure and obligation review (`predatory-regulator`)
- **maintainability** (6): Knowledge and access succession (`bus-factor-adversary`); Lifetime replaceability (`century-horizon-architect`); Lifecycle maintenance coverage (`entropy-demon`); Task-oriented comprehension (`explainability-steward`); Clean reconstruction (`hermetic-reproducibility-auditor`); Deferred decision cost assessment (`tech-debt-curator`)
- **operability** (8): Nontechnical continuity (`business-continuity-auditor`); Operating model: managed services (`cloud-native-purist`); Effective configuration at the consumer (`effective-configuration-auditor`); Incident coordination (`incident-command-auditor`); Operating-model comparison: custody and continuity (`local-first-survivalist`); Actionable detection and diagnosis (`observability-advocate`); Individual operational recovery (`on-call-realist`); Release transition safety (`release-cutover-auditor`)
- **performance-scale** (3): Workload performance diagnosis (`performance-alchemist`); Backlog and overload dynamics (`queue-stability-auditor`); Capacity and growth analysis (`scalability-cliff-analyst`)
- **process-integrity** (5): Removal consequences (`chesterton-gate`); Control effectiveness (`control-effectiveness-auditor`); Execution prerequisites and sequencing (`execution-dependency-auditor`); Acceptance claim coverage (`requirements-traceability-auditor`); Authorized scope comparison (`scope-sentinel`)
- **reliability** (8): Fault-combination exercise (`chaos-monkey`); Shared dependency analysis (`common-cause-dependency-auditor`); Reachable interleaving analysis (`concurrency-interleaving-auditor`); Distributed guarantee composition (`distributed-semantics-auditor`); Failure-mode analysis (`fmea-analyst`); Backup restoration integrity (`recovery-integrity-auditor`); Degraded operation design (`resilience-engineer`); Version and state transition compatibility (`state-migration-compatibility-auditor`)
- **risk-tails** (1): Tail exposure and fragility (`black-swan-catalyst`)
- **security** (5): Post-incident evidence reconstruction (`digital-forensicist`); Adversary paths: authorized-access mode (`disgruntled-maintainer`); Opportunistic exposure inspection (`script-kiddie`); Adversary path analysis: persistent access mode (`state-sponsored-actor`); Structured trust-boundary threat modeling (`stride-security-modeler`)
- **simplicity** (1): Simplification while preserving value (`minimalist-zen-master`)
- **strategy-alternatives** (1): Historical comparison (`analogical-historian`)
- **systems-structure** (3): External environment and strategic fit (`ecological-systems-analyst`); Coordination and technical boundary fit (`sociotechnical-topology-auditor`); Relevant feedback structure analysis (`systemic-logician`)
- **temporal-consequence** (3): Restoration and commitment analysis (`reversibility-analyst`); Performance across plausible futures (`robust-decision-auditor`); Conditional downstream consequences (`second-order-forecaster`)

## Mutual-exclusion / counter-mode groups (each counts as ONE diversity unit)

- `adjudication-modes`: `bayesian-adjudicator`, `pragmatic-judge`
- `adversary-path-modes`: `disgruntled-maintainer`, `state-sponsored-actor`
- `leverage-vs-sovereignty`: `cloud-native-purist`, `local-first-survivalist`
- `measurement-fitness-modes`: `construct-validity-auditor`, `measurement-critic`
- `reasoning-robustness-modes`: `cognitive-bias-auditor`, `sunk-cost-liberator`

## Retired aliases (IDs preserved for replay; never re-add without behavioral evidence)

- `constraint-inverter` → `constraint-negotiator`
- `constraint-relaxer` → `constraint-negotiator`
- `first-principles-engineer` → `first-principles-rederiver`
- `meta-epistemic-auditor` → `epistemic-auditor`
- `premortem-facilitator` → `inversion-thinker`
- `verification-oracle-auditor` → `forensic-accountant`
