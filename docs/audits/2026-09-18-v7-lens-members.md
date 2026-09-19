# V7 shared lens library: complete member inventory

**Status: accepted design direction, not implementation or behavioral validation.** This inventory covers all 102 canonical entries, including six already-retired identities. Current roles/statuses and recommendations are intentionally separate. A shared family, artifact or source does not by itself justify merging two methods.

[Machine-readable inventory](2026-09-18-v7-lens-members.json) contains the normalized fields and complete original assessor records. The detailed entries below retain each assessment's substantive reasoning and the final reconciliations.

Source: [canonical registry](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json) at commit `9705f70aec1285597a6ef2a341cede80010c1dcb`, registry version `3.0.0`. Registry SHA-256: `a71b7f30b937c433dc50c0c2a6b82212026161e2494398230c092fb156befa0d`.

## Contents

- [Coverage and counts](#coverage-and-counts)
- [How to read recommendations](#how-to-read-recommendations)
- [Member index](#member-index)
- [Retain distinct methods](#retain-distinct-methods)
- [Refine methods](#refine-methods)
- [Proposed combinations as modes](#proposed-combinations-as-modes)
- [Proposed role relocations](#proposed-role-relocations)
- [Preserve existing retirements](#preserve-existing-retirements)
- [Evidence limits](#evidence-limits)

## Coverage and counts

102 unique assessed IDs exactly equal the 102 current registry IDs; no missing IDs, duplicate IDs or extra IDs.

| Current status | Count |
| --- | ---: |
| available | 96 |
| retired | 6 |

| Current available role | Count |
| --- | ---: |
| adjudicate | 4 |
| evaluate | 86 |
| gate | 2 |
| generate_options | 4 |

| Recommended disposition | All entries | Currently available |
| --- | ---: | ---: |
| retain | 15 | 15 |
| refine | 68 | 68 |
| combine-as-mode | 7 | 7 |
| relocate-role | 6 | 6 |
| keep-retired | 6 | 0 |

The six existing retirements are not counted as new v7 reductions. These counts do not predict the eventual library size.

## How to read recommendations

- retain preserves a distinct directly selectable method; concrete wording or boundary corrections may still be recommended.
- refine keeps the capability while correcting its question, evidence requirements, uncertainty, boundary or output.
- combine-as-mode is a proposed packaging change preserving the substantive question and discoverable mode; it is not implemented or behaviorally validated.
- relocate-role changes where a capability contributes, such as generation, workflow discipline or adjudication; it does not imply the capability has no value.
- keep-retired preserves an already-retired historical coordinate and its successor/shared-discipline note; it is not a new v7 reduction.
- Shared family labels, artifacts or sources do not establish interchangeable mechanisms. Shared evidence must not be counted as independent corroboration.

## Member index

| Member | Current status / role | Recommendation |
| --- | --- | --- |
| [adjacent-possible-explorer](#adjacent-possible-explorer) | available / evaluate | relocate-role |
| [adoption-realist](#adoption-realist) | available / evaluate | refine |
| [analogical-historian](#analogical-historian) | available / evaluate | refine |
| [angry-customer](#angry-customer) | available / evaluate | refine |
| [bayesian-adjudicator](#bayesian-adjudicator) | available / adjudicate | combine-as-mode |
| [behavioral-economist](#behavioral-economist) | available / evaluate | refine |
| [black-swan-catalyst](#black-swan-catalyst) | available / evaluate | refine |
| [bus-factor-adversary](#bus-factor-adversary) | available / evaluate | retain |
| [business-continuity-auditor](#business-continuity-auditor) | available / evaluate | refine |
| [causal-identification-auditor](#causal-identification-auditor) | available / evaluate | refine |
| [century-horizon-architect](#century-horizon-architect) | available / evaluate | refine |
| [chaos-monkey](#chaos-monkey) | available / evaluate | refine |
| [chesterton-gate](#chesterton-gate) | available / evaluate | refine |
| [cloud-native-purist](#cloud-native-purist) | available / evaluate | combine-as-mode |
| [cognitive-bias-auditor](#cognitive-bias-auditor) | available / evaluate | refine |
| [common-cause-dependency-auditor](#common-cause-dependency-auditor) | available / evaluate | retain |
| [compliance-litigator](#compliance-litigator) | available / evaluate | refine |
| [concurrency-interleaving-auditor](#concurrency-interleaving-auditor) | available / evaluate | refine |
| [constraint-inverter](#constraint-inverter) | retired / none | keep-retired |
| [constraint-negotiator](#constraint-negotiator) | available / generate_options | refine |
| [constraint-relaxer](#constraint-relaxer) | retired / none | keep-retired |
| [construct-validity-auditor](#construct-validity-auditor) | available / evaluate | combine-as-mode |
| [contract-risk-allocation-auditor](#contract-risk-allocation-auditor) | available / evaluate | refine |
| [control-effectiveness-auditor](#control-effectiveness-auditor) | available / evaluate | refine |
| [data-provenance-auditor](#data-provenance-auditor) | available / evaluate | retain |
| [decision-rights-auditor](#decision-rights-auditor) | available / evaluate | refine |
| [dialectical-synthesizer](#dialectical-synthesizer) | available / adjudicate | relocate-role |
| [digital-forensicist](#digital-forensicist) | available / evaluate | retain |
| [disgruntled-maintainer](#disgruntled-maintainer) | available / evaluate | combine-as-mode |
| [distributed-semantics-auditor](#distributed-semantics-auditor) | available / evaluate | refine |
| [distributive-justice-auditor](#distributive-justice-auditor) | available / evaluate | refine |
| [dual-use-adversary](#dual-use-adversary) | available / evaluate | refine |
| [ecological-systems-analyst](#ecological-systems-analyst) | available / evaluate | refine |
| [effective-configuration-auditor](#effective-configuration-auditor) | available / evaluate | retain |
| [entropy-demon](#entropy-demon) | available / evaluate | refine |
| [epistemic-auditor](#epistemic-auditor) | available / evaluate | refine |
| [ethicist](#ethicist) | available / evaluate | refine |
| [execution-dependency-auditor](#execution-dependency-auditor) | available / evaluate | refine |
| [explainability-steward](#explainability-steward) | available / evaluate | refine |
| [first-principles-engineer](#first-principles-engineer) | retired / none | keep-retired |
| [first-principles-rederiver](#first-principles-rederiver) | available / generate_options | refine |
| [fmea-analyst](#fmea-analyst) | available / evaluate | refine |
| [forensic-accountant](#forensic-accountant) | available / evaluate | refine |
| [game-theorist](#game-theorist) | available / evaluate | refine |
| [governance-lawyer](#governance-lawyer) | available / gate | relocate-role |
| [human-automation-handoff-auditor](#human-automation-handoff-auditor) | available / evaluate | refine |
| [incident-command-auditor](#incident-command-auditor) | available / evaluate | retain |
| [integration-weaver](#integration-weaver) | available / evaluate | refine |
| [invariant-specification-auditor](#invariant-specification-auditor) | available / evaluate | refine |
| [inversion-thinker](#inversion-thinker) | available / evaluate | refine |
| [ip-freedom-to-operate-auditor](#ip-freedom-to-operate-auditor) | available / evaluate | refine |
| [jurisdiction-conflicts-auditor](#jurisdiction-conflicts-auditor) | available / evaluate | refine |
| [lifecycle-impact-auditor](#lifecycle-impact-auditor) | available / evaluate | refine |
| [liquidity-runway-auditor](#liquidity-runway-auditor) | available / evaluate | refine |
| [local-first-survivalist](#local-first-survivalist) | available / evaluate | combine-as-mode |
| [measurement-critic](#measurement-critic) | available / evaluate | refine |
| [meta-epistemic-auditor](#meta-epistemic-auditor) | retired / none | keep-retired |
| [minimalist-zen-master](#minimalist-zen-master) | available / evaluate | refine |
| [network-effects-strategist](#network-effects-strategist) | available / evaluate | refine |
| [null-hypothesis-advocate](#null-hypothesis-advocate) | available / generate_options | refine |
| [observability-advocate](#observability-advocate) | available / evaluate | refine |
| [on-call-realist](#on-call-realist) | available / evaluate | refine |
| [opportunity-cost-accountant](#opportunity-cost-accountant) | available / evaluate | retain |
| [opposite-steelman](#opposite-steelman) | available / generate_options | retain |
| [performance-alchemist](#performance-alchemist) | available / evaluate | refine |
| [polymath-inquisitor](#polymath-inquisitor) | available / evaluate | refine |
| [pragmatic-judge](#pragmatic-judge) | available / adjudicate | relocate-role |
| [predatory-regulator](#predatory-regulator) | available / evaluate | refine |
| [preference-sensitivity-arbitrator](#preference-sensitivity-arbitrator) | available / evaluate | refine |
| [premise-auditor](#premise-auditor) | available / evaluate | retain |
| [premortem-facilitator](#premortem-facilitator) | retired / none | keep-retired |
| [privacy-surveillance-critic](#privacy-surveillance-critic) | available / evaluate | refine |
| [protocol-archeologist](#protocol-archeologist) | available / evaluate | refine |
| [queue-stability-auditor](#queue-stability-auditor) | available / evaluate | refine |
| [recovery-integrity-auditor](#recovery-integrity-auditor) | available / evaluate | retain |
| [red-lines-arbitrator](#red-lines-arbitrator) | available / gate | relocate-role |
| [release-cutover-auditor](#release-cutover-auditor) | available / evaluate | retain |
| [requirements-traceability-auditor](#requirements-traceability-auditor) | available / evaluate | refine |
| [resilience-engineer](#resilience-engineer) | available / evaluate | retain |
| [reversibility-analyst](#reversibility-analyst) | available / evaluate | retain |
| [robust-decision-auditor](#robust-decision-auditor) | available / evaluate | refine |
| [safety-hazard-auditor](#safety-hazard-auditor) | available / evaluate | refine |
| [scalability-cliff-analyst](#scalability-cliff-analyst) | available / evaluate | refine |
| [scope-sentinel](#scope-sentinel) | available / evaluate | refine |
| [script-kiddie](#script-kiddie) | available / evaluate | refine |
| [second-order-forecaster](#second-order-forecaster) | available / evaluate | refine |
| [semantic-critic](#semantic-critic) | available / evaluate | refine |
| [sociotechnical-topology-auditor](#sociotechnical-topology-auditor) | available / evaluate | refine |
| [sovereign-ruler](#sovereign-ruler) | available / adjudicate | relocate-role |
| [state-migration-compatibility-auditor](#state-migration-compatibility-auditor) | available / evaluate | retain |
| [state-sponsored-actor](#state-sponsored-actor) | available / evaluate | combine-as-mode |
| [statistical-validity-critic](#statistical-validity-critic) | available / evaluate | refine |
| [stride-security-modeler](#stride-security-modeler) | available / evaluate | retain |
| [sunk-cost-liberator](#sunk-cost-liberator) | available / evaluate | combine-as-mode |
| [systemic-logician](#systemic-logician) | available / evaluate | refine |
| [tech-debt-curator](#tech-debt-curator) | available / evaluate | refine |
| [ui-ux-polisher](#ui-ux-polisher) | available / evaluate | refine |
| [unit-economics-adversary](#unit-economics-adversary) | available / evaluate | refine |
| [value-of-information-auditor](#value-of-information-auditor) | available / evaluate | refine |
| [verification-oracle-auditor](#verification-oracle-auditor) | retired / none | keep-retired |
| [wcag-accessibility-expert](#wcag-accessibility-expert) | available / evaluate | refine |
| [workforce-load-auditor](#workforce-load-auditor) | available / evaluate | refine |

## Retain distinct methods

### bus-factor-adversary

Current: **available / evaluate**, version 2. Capability: `maintainability`. Recommendation: **retain**.

**Rationale:** Knowledge concentration can exist in a legible system; the cold non-author procedure attempt is a concrete method.

**Concrete edits:**

- Replace the assertion that failure arrives when the holder leaves with a conditional risk.
- Use the relevant successor role/task, not an unconditional second-person requirement; preserve automation and access-succession evidence.

**Boundary:** explainability-steward examines artifact legibility; workforce-load-auditor examines capacity; business-continuity-auditor examines operation after dependency loss. Reuse drills without double-counting evidence.

**Evidence limits:** Needs procedure inventory, role/access availability, and a bounded unaided attempt. Reading a runbook is not demonstrated transfer. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 404](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L404); [entry at line 404](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L404).

### common-cause-dependency-auditor

Current: **available / evaluate**, version 1. Capability: `reliability`. Recommendation: **retain**.

**Rationale:** Static dependency-closure/intersection analysis is a concrete method distinct from exercising fault combinations. Preserve it as directly selectable; sharing a risk family or downstream finding with chaos-monkey does not establish that the methods should be merged.

**Concrete edits:**

- Retain a separately selectable static dependency-analysis method.
- Scope dependency closure to the claimed failure domains; state completeness and uncertainty rather than demanding absolute disjointness.
- Determine whether shared elements defeat the promised service, distinguishing accepted sharing from hidden exposure. Reuse fault-injection evidence without counting it as independent corroboration.

**Boundary:** Common-cause analysis statically traces dependency intersections and shared fate; chaos/fault injection dynamically exercises combinations. Their artifacts may be shared, but the same evidence cannot count twice.

**Evidence limits:** An empty intersection of incomplete lists does not establish independence; expose dependency coverage and uncertainty. Source inspection and design inference; behavioral benefit untested.

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. The source comparison establishes different operations and evidence collection. A packaging merger is not established merely because both concern shared failures.

**Original assessor rationale:** Intersecting dependency closures is a clear cheap procedure; preserve it, but do not count it as a separate independent perspective when chaos-monkey examines the same shared dependency.

**Original assessor proposed edit:**

- Retain the explicit closure/intersection procedure as a selectable mode.
- Scope closure to claimed failure domains; absolute disjointness is neither universally possible nor necessary.
- Assess whether a shared element defeats the promised service, distinguishing accepted sharing from hidden exposure.

**Original assessor boundary:** chaos exercises combinations; black-swan addresses broader severe concentrations; recovery-integrity adds data recovery correctness.

**Sources:** [id at line 848](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L848); [entry at line 848](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L848).

### data-provenance-auditor

Current: **available / evaluate**, version 2. Capability: `data-validity`. Recommendation: **retain**.

**Rationale:** Tracing transformations, joins, units, missingness and defaults is distinct from summary arithmetic and statistical inference.

**Concrete edits:**

- Preserve the method; bound traces to load-bearing fields and relevant failure classes rather than every datum. Report sampled versus complete coverage and unresolved lineage. A clean sample does not prove zero silent loss everywhere.

**Boundary:** Owns source-to-derived-data integrity; numeric reconciliation and inference remain different checks.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1304](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1304); [entry at line 1304](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1304).

### digital-forensicist

Current: **available / evaluate**, version 2. Capability: `security`. Recommendation: **retain**.

**Rationale:** Surviving evidence integrity, time alignment, provenance and custody ask a different question from ordinary telemetry.

**Concrete edits:**

- Use a named event and needed reconstruction granularity instead of a universal complete-timeline threshold.
- Include minimization, retention authority and access limits; more logging is not always better.
- Separate preservation design from successful reconstruction.

**Boundary:** observability supports diagnosis; adversary-path modes identify compromise paths; this checks trustworthy evidence remaining afterward.

**Evidence limits:** Needs logs/retention/integrity controls and bounded reconstruction. Restricted evidence requires redacted metadata or declared limitations. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1466](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1466); [entry at line 1466](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1466).

### effective-configuration-auditor

Current: **available / evaluate**, version 1. Capability: `operability`. Recommendation: **retain**.

**Rationale:** Tracing winning values through precedence to actual consumers is a concrete mechanism relevant to configuration and instruction/skill activation.

**Concrete edits:**

- Replace nobody-knows-the-config assertion with a question.
- Include effective source, process/host revision, restart persistence and redaction of sensitive values.
- Apply to assembled instructions only where the host exposes evidence; declared files do not prove loading.

**Boundary:** entropy checks decay; cutover checks transitions; did-it-land/context-audit can call this method instead of duplicating it.

**Evidence limits:** Needs supported resolved-value/context inspection or discriminating behavior probes. Distinguish intended, stored, loaded and consumed states. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1797](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1797); [entry at line 1797](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1797).

### incident-command-auditor

Current: **available / evaluate**, version 1. Capability: `operability`. Recommendation: **retain**.

**Rationale:** Multi-responder coordination, authority, information transfer and conflicting actions are a distinct method from an individual recovery walkthrough. Shared incident artifacts are a reason to reuse evidence, not sufficient grounds to merge the capabilities.

**Concrete edits:**

- Keep a directly selectable coordination method for concurrent responders, decisions and handoffs.
- Examine decision rights and communication timing without assuming a mandatory command hierarchy.
- Replace universal no-coordination-failures thresholds with named consequences and scoped incident/drill evidence.

**Boundary:** Incident command examines coordination between responders; on-call recovery examines whether an individual can diagnose and restore safely. Decision-rights and human-automation handoff provide relevant inputs without compulsory repeat review.

**Evidence limits:** Needs actual/drill timeline, role/handoff records and delays. A single clean incident does not establish future coordination reliability. Source inspection and design inference; behavioral benefit untested.

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. Coordination across people introduces failure mechanisms not established by a single-operator recovery check; retain the distinct entry.

**Original assessor rationale:** Its incident timeline review of authority, information transfer and conflicting actions is an important multi-responder extension to recovery walkthroughs.

**Original assessor proposed edit:**

- Preserve explicit multi-responder mode within operational recovery, selected for parallel actions/handoffs.
- Keep decision rights and communication timing without mandatory command hierarchy.
- Replace universal no-coordination-failures threshold with named consequences and scoped incident evidence.

**Original assessor boundary:** on-call handles individual recovery; decision-rights covers general authority; human-automation-handoff checks transfer of control. Consume relevant outputs.

**Sources:** [id at line 2506](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2506); [entry at line 2506](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2506).

### opportunity-cost-accountant

Current: **available / evaluate**, version 2. Capability: `economics`. Recommendation: **retain**.

**Rationale:** A displaced best feasible use is distinct from status quo and margin. Existing warning against using opportunity cost to veto everything is appropriate.

**Concrete edits:**

- Keep named feasible alternatives, comparable resources/time, uncertainty and further-comparison cost. Say best known alternative instead of global optimum; reuse priorities and stop when more comparison cannot change the choice.

**Boundary:** Compares feasible allocation; does not reopen settled priorities without new material evidence or turn every forgone possibility into a blocker.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3363](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3363); [entry at line 3363](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3363).

### opposite-steelman

Current: **available / generate_options**, version 2. Capability: `strategy-alternatives`. Recommendation: **retain**.

**Rationale:** Giving a dismissed branch its strongest supported case is distinct option generation. Existing warning that advocacy does not decide the winner is sound.

**Concrete edits:**

- Keep advocacy label, symmetric criteria/costs and checked rejection assumptions. Mark missing evidence instead of inventing support; present chosen path fairly too; allow the rejected branch to remain inferior.

**Boundary:** Develops a specified alternative; adjacent exploration searches nearby options and rederivation starts from constraints. Subsequent comparison is a separate contribution.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3419](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3419); [entry at line 3419](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3419).

### premise-auditor

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **retain**.

**Rationale:** Eliciting unstated load-bearing assumptions differs from grading an explicit claim inventory. Existing impact/uncertainty ranking and warning against questioning everything support retaining a direct method.

**Concrete edits:**

- Separate assumed fact from selected value/requirement. Rank plausible decision impact; reuse claim/evidence representation once explicit. Show how the hidden premise was inferred rather than attributing unsupported beliefs.

**Boundary:** Owns elicitation/testing within the current frame; epistemic audit grades warrant once explicit; metacognate can regulate whether this method is needed.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3745](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3745); [entry at line 3745](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3745).

### recovery-integrity-auditor

Current: **available / evaluate**, version 1. Capability: `reliability`. Recommendation: **retain**.

**Rationale:** Checking whether a real backup yields a consistent usable restored state within time/loss requirements is more specific than response or failover.

**Concrete edits:**

- Separate existence, completeness, consistency, restore execution and application validation.
- Bind conclusion to tested backup, version, dependencies and scenario.
- Use isolated restoration or read-only inspection proportionately; drills require appropriate authority/resources.

**Boundary:** common-cause checks overlap; on-call checks responders; migration checks cross-version state. Share a restore result only within its scope.

**Evidence limits:** Needs actual backup, restored-state validation, key/dependency access and RPO/RTO evidence. Missing a recent drill is an assurance gap, not proof of corruption. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4006](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4006); [entry at line 4006](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4006).

### release-cutover-auditor

Current: **available / evaluate**, version 1. Capability: `operability`. Recommendation: **retain**.

**Rationale:** Walking each deployment step and asking what happens if it stops is a distinct transition-state method.

**Concrete edits:**

- Include observers, skew, abort/continue criteria and forward repair.
- Every intermediate state need not allow rollback; require an appropriate justified recovery outcome.
- Reuse existing pipeline/runtime evidence rather than require new ceremony.

**Boundary:** migration builds code/data version matrix; effective-config checks standing resolved state; on-call handles unexpected response.

**Evidence limits:** Needs actual sequence, dependencies, windows and rehearsal/runtime evidence for behavioral claims. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4116](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4116); [entry at line 4116](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4116).

### resilience-engineer

Current: **available / evaluate**, version 2. Capability: `reliability`. Recommendation: **retain**.

**Rationale:** Constructing acceptable partial service and recovery answers a different question from finding faults.

**Concrete edits:**

- Start with essential outcomes and tolerable degradation before choosing breakers, fallbacks or redundancy.
- Price complexity; not every dependency requires fallback.
- Keep designed, simulated and rehearsed behavior separate.

**Boundary:** FMEA/fault-combination methods identify conditions; this constructs responses; continuity covers loss beyond technical operation.

**Evidence limits:** Needs failure-to-outcome mapping, constraints and demonstrated behavior for effective-resilience claims. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4226](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4226); [entry at line 4226](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4226).

### reversibility-analyst

Current: **available / evaluate**, version 2. Capability: `temporal-consequence`. Recommendation: **retain**.

**Rationale:** Undo path, deadline and ratchets are distinct from loss magnitude or sunk costs. The method appropriately connects decision properties to effort and optionality.

**Concrete edits:**

- Preserve but remove always-single-most-important rhetoric. Assess technical, social, financial and informational restoration separately, with residual effects. Reuse checked undo paths; reversibility being an explicit goal is not itself verification.

**Boundary:** Owns what can be restored, by whom, until when and at what cost. Reversible does not automatically mean low impact.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4282](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4282); [entry at line 4282](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4282).

### state-migration-compatibility-auditor

Current: **available / evaluate**, version 1. Capability: `reliability`. Recommendation: **retain**.

**Rationale:** Old/new code-data matrices, post-write rollback and in-flight crossings are concrete mechanisms distinct from operational sequencing.

**Concrete edits:**

- Specify downtime tolerance, data invariants, versions and compatibility direction.
- Allow forward-only migration with explicit recovery commitments.
- Scope claims to tested formats, cases and mixed-version states.

**Boundary:** cutover handles sequencing; reversibility finds ratchets; integration covers consumers. Keep methods distinct but share a transition dossier.

**Evidence limits:** Needs schemas/serialization, representative old/new data and cross-version behavior. End-state tests cannot establish all transitions. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4837](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4837); [entry at line 4837](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4837).

### stride-security-modeler

Current: **available / evaluate**, version 2. Capability: `security`. Recommendation: **retain**.

**Rationale:** Systematic asset/flow/boundary analysis through threat classes remains a recognizable coverage method alongside concrete exposure/path methods.

**Concrete edits:**

- Specify modeling procedure and scope rather than universal coverage claims.
- Reuse/audit current models rather than exclude the method when a model exists.
- Separate possibility, exploitability, impact, control evidence and accepted residual risk.
- Detection does not make a threat harmless; assess response timing and consequence.

**Boundary:** Adversary profiles deepen paths; exposure inspection checks reachable known hazards. These are complementary methods, not interchangeable votes.

**Evidence limits:** Needs architecture, assets, flows, assumptions and actual controls. A populated table proves enumeration, not protection. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 5008](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5008); [entry at line 5008](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5008).


## Refine methods

### adoption-realist

Current: **available / evaluate**, version 2. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** The shipped-to-used path is distinct from in-product failure. Captive-user exclusion overlooks mandatory migration burdens.

**Concrete edits:**

- Retain steps, habits, trust, fallbacks and observed adoption; state whose adoption matters and the outcome it serves. Remove laggard stereotypes and adoption-as-sufficient-success claims.

**Boundary:** Label predicted behavior as hypothesis. Mandatory use still has learning and avoidance questions; simulated users cannot prove voluntary adoption.

**Evidence limits:** No comparative evidence establishes whether institutional readiness requires a separate method. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared migration/adoption method

**Preserve:** Constructive on-ramp design.

**Comparators:** angry-customer: in-use failure; behavioral-economist: behavior assumptions; queued organizational-readiness: wider institutional capability

**Sources:** [id at line 65](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L65); [object_of_scrutiny at line 82](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L82); [contraindications at line 96](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L96); [heuristic at line 113](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L113); [bias at line 116](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L116).

### analogical-historian

Current: **available / evaluate**, version 2. Capability: `strategy-alternatives`. Recommendation: **refine**.

**Rationale:** Documented precedents and structural force mapping are useful. The claim that the precedent knows how this ends biases the card toward deterministic, cherry-picked failure narratives.

**Concrete edits:**

- Require documented outcomes, contrasting outcomes where practical, source/selection limits, shared mechanisms, decisive differences and a transfer-strength judgment. Where a reference class exists, report its denominator/base rate. Allow no informative precedent as a valid result.

**Boundary:** Historical analogy supports conditional comparison; it does not by itself establish causation, generalizability or a forecast probability.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 121](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L121); [entry at line 121](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L121).

### angry-customer

Current: **available / evaluate**, version 2. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** Dead ends, false status and obstructive cancellation are inspectable. Universal non-reading and public humiliation are unsupported population priors.

**Concrete edits:**

- Walk a specified user goal, capabilities, failure path and recovery. Prefer a neutral display name while retaining the historical ID.

**Boundary:** Agent walkthroughs are inspection, not actual customer testimony. Distinguish obstruction from justified security friction.

**Evidence limits:** Actual user observation may reverse predicted confusion or intolerance of friction. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared failure-focused journey method

**Preserve:** Adversarial attention to hostile failure and exit paths.

**Comparators:** adoption-realist: entering use; ui-ux-polisher: constructive surfaces; behavioral-economist: behavioral model

**Sources:** [id at line 177](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L177); [object_of_scrutiny at line 194](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L194); [falsifier_template at line 202](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L202); [heuristic at line 229](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L229); [vector at line 230](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L230).

### behavioral-economist

Current: **available / evaluate**, version 2. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** Defaults and incentive assumptions merit scrutiny; the core presets a lazy biased human and declares every rational-actor system mistaken.

**Concrete edits:**

- Name the behavior assumption and context, then compare plausible explanations with observed rates or explicitly hypothetical models.

**Boundary:** Expertise and stakes are variables, not automatic exemptions. A persona supplies neither credentials nor experimental evidence.

**Evidence limits:** No behavior run compares the persona against a neutral method; contrary behavior should update the hypothesis. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared behavioral-assumption method

**Preserve:** Falsifiable default and incentive analysis.

**Comparators:** game-theorist: payoffs; adoption-realist: migration; queued cultural-portability: transfer across populations

**Sources:** [id at line 288](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L288); [required_evidence at line 306](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L306); [heuristic at line 340](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L340); [vector at line 341](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L341); [bias at line 343](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L343).

### black-swan-catalyst

Current: **available / evaluate**, version 2. Capability: `risk-tails`. Recommendation: **refine**.

**Rationale:** Cross-domain catastrophic exposure differs from operational redundancy, but the card conflates enumerable concentrations, a 99th-percentile stress and unknowable surprises. Common-cause, continuity and resilience already cover much of its inventory.

**Concrete edits:**

- Use functional description tail exposure and fragility. Identify loss tolerance, named concentrations, nonlinear thresholds, plausible stresses, recovery limits and costed mitigations. Label unsupported probabilities unknown; remove invented quantiles and claims to find all unlisted events.

**Boundary:** Owns conditions crossing a viability or irrecoverable-loss threshold. Reuse dependency/continuity evidence; do not count reuse as fresh independent corroboration.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 348](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L348); [entry at line 348](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L348).

### business-continuity-auditor

Current: **available / evaluate**, version 1. Capability: `operability`. Recommendation: **refine**.

**Rationale:** Vendor/account/license/facility loss can defeat healthy technical failover; current terms and replacement windows provide a distinct method.

**Concrete edits:**

- Narrow to critical nontechnical dependencies and the window between loss and viable replacement; delegate knowledge concentration.
- Separate tabletop plausibility from exercised continuity; discussion does not demonstrate continued operation.
- Remove the predetermined billing-dispute rather than disk failure slogan.

**Boundary:** local-first-survivalist compares ownership choices; bus-factor tests knowledge transfer; recovery-integrity tests restored-state correctness.

**Evidence limits:** Needs current notice/termination terms, egress constraints, replacement time and exercise evidence. Unknown terms remain unknown. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 460](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L460); [entry at line 460](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L460).

### causal-identification-auditor

Current: **available / evaluate**, version 1. Capability: `data-validity`. Recommendation: **refine**.

**Rationale:** Causal identification differs from precision and construct validity. Proper randomization is not categorical immunity: attrition, interference, noncompliance, measurement and transport can still defeat a claim. Effect persistence after adjustment alone is not identification.

**Concrete edits:**

- Start with estimand, target population, intervention/comparator and horizon. Name identification assumptions and rival causal stories; check randomization implementation where relevant. Use claim-specific discriminating/sensitivity checks and proportional rigor.

**Boundary:** Owns whether evidence licenses the intervention claim; statistics owns inference mechanics and provenance owns data integrity.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 515](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L515); [entry at line 515](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L515).

### century-horizon-architect

Current: **available / evaluate**, version 2. Capability: `maintainability`. Recommendation: **refine**.

**Rationale:** Checking replacement paths across the actual expected life of a foundational choice is distinct from pricing existing debt. Literal century language and boring-versus-fashion framing prejudge it.

**Concrete edits:**

- Use explicit service/data lifetime rather than fixed 2125, 2040, or decade assumptions.
- Replace speculative dependency half-life with maintenance/standard commitments, exportability and concrete substitution paths.
- Compare near-term benefit and migration cost; standards are evidence, not automatic winners.

**Boundary:** tech-debt-curator values current deferrals; explainability-steward checks present comprehension; reversibility-analyst classifies undo consequences. Horizon alone is not a distinct mechanism.

**Evidence limits:** A replacement plan is weaker than an exercised replacement; unknown future behavior requires scenario-based claims. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 570](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L570); [entry at line 570](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L570).

### chaos-monkey

Current: **available / evaluate**, version 2. Capability: `reliability`. Recommendation: **refine**.

**Rationale:** Constructing fault combinations and checking degraded behavior is useful; its hidden-dependency claim substantially overlaps common-cause-dependency-auditor.

**Concrete edits:**

- Expose dependency-intersection and fault-combination exercise as explicit modes of one family.
- Use neutral functional discovery such as fault-combination analysis; random injection is optional.
- Distinguish desk analysis, simulation, isolated exercise and actual injection; the card does not authorize disruption.
- Replace the strange bias claiming it underweights correlated faults and assumes automation works with limits from incomplete topology and tested scenarios.

**Boundary:** common-cause is the cheap static mode; FMEA enumerates component failures; resilience-engineer constructs acceptable responses. Preserve these latter methods.

**Evidence limits:** Needs bounded fault hypotheses, topology, envelope and observed outcomes for survivability claims; a topology argument is not automatically runtime failover evidence. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 627](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L627); [entry at line 627](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L627).

### chesterton-gate

Current: **available / evaluate**, version 2. Capability: `process-integrity`. Recommendation: **refine**.

**Rationale:** A specific deletion trigger differs usefully from broad archaeology. Approve/block authority and provably obsolete origins are too restrictive where replacement guarantees or reversible experiments exist.

**Concrete edits:**

- Trace present consumers, guarantees, known origin, replacement protection and reversibility; return supported consequences and decision conditions rather than grant approval.

**Boundary:** Unknown origin is uncertainty, not endless veto. Reuse archaeological evidence during deletion; remove the exclusive boundary forbidding relevant reconstruction once deletion is proposed.

**Evidence limits:** Keep separate entry if its change-time trigger helps; combine only if that activation survives as a mode. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared proposed-deletion consequence method

**Preserve:** Protection against removing misunderstood load-bearing behavior.

**Comparators:** protocol-archeologist: reusable provenance; minimalist-zen-master: candidates; reversibility-analyst: undo cost

**Sources:** [id at line 683](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L683); [object_of_scrutiny at line 700](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L700); [falsifier_template at line 708](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L708); [contraindications at line 714](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L714); [neighbors at line 718](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L718); [vector at line 732](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L732); [contraindications at line 3930](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3930); [vector at line 3944](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3944).

### cognitive-bias-auditor

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Observable anchoring and asymmetric evidence treatment merit testing. Diagnosing an authors psychology from a sentence is underdetermined; unchanged conclusions after restatement do not establish sound reasoning. Full card includes sunk-cost questions despite explicit fingerprint exclusion.

**Concrete edits:**

- Recast as reasoning robustness: identify observable asymmetry, apply a concrete intervention such as reverse order or contrary evidence, and report changes. Treat psychological labels tentatively. Host sunk-cost continuation as a named mode; synchronize card and fingerprint.

**Boundary:** Tests reasoning procedures and sensitivity, not mental traits. A bias label cannot invalidate a conclusion; sunk-cost mode is discoverable without counting as independent diversity.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 792](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L792); [entry at line 792](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L792).

### compliance-litigator

Current: **available / evaluate**, version 2. Capability: `legal-compliance`. Recommendation: **refine**.

**Rationale:** Contradictions among policies, decisions and records differ from external disclosures. Discovery-is-forever and a universally signed record add unjustified legal and process assumptions.

**Concrete edits:**

- Trace material decisions to applicable record, approval and retention requirements with source, scope and date. Separate missing records, contradictions and uncertain legal consequences.

**Boundary:** No persona is counsel or creates a signature requirement. Preserve truthful records and applicable retention; never recommend concealment or deletion to improve litigation appearance.

**Evidence limits:** Legal significance depends on applicable authority and facts; no jurisdiction or actual dispute was researched. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared decision-record consistency method

**Preserve:** Accountable and retrievable decision evidence.

**Comparators:** predatory-regulator: external claims; governance-lawyer: current panel; digital-forensicist: incident evidence integrity

**Sources:** [id at line 903](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L903); [object_of_scrutiny at line 920](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L920); [falsifier_template at line 928](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L928); [heuristic at line 951](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L951); [vector at line 952](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L952).

### concurrency-interleaving-auditor

Current: **available / evaluate**, version 1. Capability: `reliability`. Recommendation: **refine**.

**Rationale:** Constructing a reachable schedule violating a named invariant is a distinct concrete method.

**Concrete edits:**

- State invariant, schedule and reachability before claiming a defect.
- Remove the universal assertion that every possible schedule eventually happens.
- Separate counterexample reproduction, bounded search and proof; a clean stress test cannot prove the schedule unreachable.

**Boundary:** distributed-semantics audits guarantees; invariant-specification finds required conditions; this constructs violating schedules.

**Evidence limits:** Needs runtime guarantees, transitions, relevant code/config and preferably a deterministic schedule/model. Guessed ordering is hypothesis. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 959](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L959); [entry at line 959](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L959).

### constraint-negotiator

Current: **available / generate_options**, version 1. Capability: `strategy-alternatives`. Recommendation: **refine**.

**Rationale:** Changing constraints is distinct from deriving within them. Physics/negotiable/phantom overlooks user values, legal obligations and authority; requiring a fully costed path can suppress a useful explicit hypothesis.

**Concrete edits:**

- Record source, owner, hardness, change authority and evidence status for each constraint. Distinguish physical, obligation/value, resource and assumed constraints. Compare removal/retention costs as ranges; mark contingent relaxations hypothetical.

**Boundary:** May question source/cost, but only authorized decision-makers change real requirements. Can inform constructive revision without silently reopening scope.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1048](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1048); [entry at line 1048](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1048).

### contract-risk-allocation-auditor

Current: **available / evaluate**, version 1. Capability: `legal-compliance`. Recommendation: **refine**.

**Rationale:** Caps, indemnities and termination conflicts across documents form a distinct mechanism. Textual consistency alone does not establish enforceability or who ultimately pays.

**Concrete edits:**

- Trace scenarios through definitions, precedence and governing documents. Classify clear conflict, competing interpretation, missing document and legal uncertainty; source negotiability comparisons.

**Boundary:** Issue spotting is not a legal opinion. Do not assume standard terms are safe or negotiable; keep party allocation distinct from public-law compliance.

**Evidence limits:** A precedence clause or omitted amendment may settle the reported conflict. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared contractual-allocation trace

**Preserve:** Clause-level allocation across actual agreements.

**Comparators:** compliance-litigator: internal records; jurisdiction-conflicts-auditor: regimes; ip-freedom-to-operate-auditor: rights

**Sources:** [id at line 1194](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1194); [object_of_scrutiny at line 1211](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1211); [falsifier_template at line 1219](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1219); [heuristic at line 1241](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1241); [bias at line 1244](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1244).

### control-effectiveness-auditor

Current: **available / evaluate**, version 1. Capability: `security`. Recommendation: **refine**.

**Rationale:** Testing preventive/detective operation is distinct from documenting a control or assuming compliance, and useful beyond security.

**Concrete edits:**

- Broaden discovery beyond security while retaining security examples.
- Replace theater/bypass-presuming language with neutral checks.
- Separate design adequacy, implemented coverage, operation, response and residual risk. One planted violation tests only that path.
- Respect test authority; use fixtures or inspection when real bypass/violation tests are unavailable.

**Boundary:** Oracle adequacy is retired into Gauntlet discipline; make that discipline reusable. This method tests subject controls, not just the review apparatus.

**Evidence limits:** Needs configuration, history, relevant cases and response records. No firing history is not by itself evidence of ineffectiveness. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1249](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1249); [entry at line 1249](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1249).

### decision-rights-auditor

Current: **available / evaluate**, version 1. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** Subject decision authority differs from this panel or incident command. Ownership alone does not settle consequences borne by outsiders.

**Concrete edits:**

- Classify authority as documented, delegated, inferred, contested or missing; trace decision, source and consequence bearer while preserving evidenced informal arrangements.

**Boundary:** Detect existing gaps without inventing approvers or renewing settled authorization. Distinguish ownership from affected-party rights and participation.

**Evidence limits:** A demonstrated working delegation may refute a gap; informal-power specialization needs a distinct method. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared authority/accountability trace

**Preserve:** Owner, authority-source and accountability mapping.

**Comparators:** governance-lawyer: panel; incident-command-auditor: crisis; sociotechnical-topology-auditor: seams; queued institutional-power/stakeholder-representation

**Sources:** [id at line 1360](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1360); [object_of_scrutiny at line 1377](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1377); [falsifier_template at line 1385](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1385); [contraindications at line 1391](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1391); [vector at line 1408](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1408); [bias at line 1410](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1410).

### distributed-semantics-auditor

Current: **available / evaluate**, version 1. Capability: `reliability`. Recommendation: **refine**.

**Rationale:** Mapping actual delivery/consistency guarantees against application requirements is a meaningful contract-composition method, separate from finding a particular race.

**Concrete edits:**

- Remove exactly-once-is-a-lie; specify operation scope and assumptions.
- Compare required/provided guarantees during partition, retries and failover.
- A successful fault test is not proof of all semantics; name checked histories and envelope.

**Boundary:** concurrency-interleaving constructs violations; integration-weaver examines caller contract usability. Share evidence rather than repeat findings.

**Evidence limits:** Needs version-specific authoritative guarantees and relevant histories/model; documentation alone does not prove composed behavior. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1578](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1578); [entry at line 1578](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1578).

### distributive-justice-auditor

Current: **available / evaluate**, version 2. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** Disaggregated benefits and harms reveal losses hidden by averages. Compensation does not make a loss absent, and imagined acceptance is not actual consent.

**Concrete edits:**

- Table observed/predicted impacts by group, missing groups and tail risks; identify the fairness criterion and its value source. Separate loss, compensation, acceptability and consent.

**Boundary:** Normative disagreement is not empirically falsified by compensation or aggregate gain. Simulated perspectives generate questions, not stakeholder representation.

**Evidence limits:** Lifecycle consolidation is tentative; retain discoverable stage coverage. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared impact-distribution method

**Preserve:** Concentrated losses and excluded groups remain visible.

**Comparators:** ethicist: values; lifecycle-impact-auditor: stage distribution; queued stakeholder-representation/intergenerational-stewardship

**Sources:** [id at line 1633](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1633); [object_of_scrutiny at line 1650](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1650); [falsifier_template at line 1658](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1658); [vector at line 1678](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1678); [contraindications at line 1664](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1664).

### dual-use-adversary

Current: **available / evaluate**, version 2. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** Harm through legitimate features differs from boundary compromise. Current falsifier conflates flagged abuse with blocked abuse.

**Concrete edits:**

- Trace plausible actors, access, scale, victims and deterrents; separate prevention, detection, rate reduction and residual harm. Use safe hypothetical walkthroughs unless real tests are authorized.

**Boundary:** Capability alone does not prove likely harm. Detection is not prevention, and beneficial uses remain relevant.

**Evidence limits:** Population and control evidence can change plausibility; source walkthroughs do not prove enforcement. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared intended-capability abuse method

**Preserve:** Concrete harmful uses that work as designed.

**Comparators:** stride-security-modeler: boundaries; privacy-surveillance-critic: data exposure; safety-hazard-auditor: physical consequences

**Sources:** [id at line 1685](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1685); [object_of_scrutiny at line 1702](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1702); [falsifier_template at line 1710](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1710); [heuristic at line 1733](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1733); [vector at line 1734](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1734).

### ecological-systems-analyst

Current: **available / evaluate**, version 2. Capability: `systems-structure`. Recommendation: **refine**.

**Rationale:** External competition, regulation and dependency changes differ from internal feedback. A hedge existing does not establish its adequacy; ecological naming can be confused with environmental-impact assessment.

**Concrete edits:**

- Add plain label external environment and strategic fit. State horizon, controllable factors, plausible changes, exposure and adaptation paths. Test hedge coverage; reuse current adequate analysis rather than claiming exhaustive exclusion.

**Boundary:** Owns external conditions changing viability/opportunity. Internal feedback, lifecycle harms and physical hazards remain neighboring methods.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1741](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1741); [entry at line 1741](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1741).

### entropy-demon

Current: **available / evaluate**, version 2. Capability: `maintainability`. Recommendation: **refine**.

**Rationale:** Ownerless expiry/refresh/rebuild processes differ from deliberate debt; current greenfield exclusion prevents useful prospective maintenance review.

**Concrete edits:**

- Permit review before launch when future obligations are known.
- Replace time-is-primary-destroyer with a coverage question.
- Match refresh/rotation policy to the artifact/threat model rather than require rotation merely because a secret exists.
- Owner plus fresh record rebuts a specific unowned-expiry concern, not every drift/rebuild concern.

**Boundary:** tech-debt handles chosen deferral; bus-factor checks transfer; queued hermetic-reproducibility would make clean reconstruction the main method.

**Evidence limits:** Needs obligations, ownership, records and current rebuild evidence where claimed. Missing monitor-view telemetry does not prove nobody looks. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1852](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1852); [entry at line 1852](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1852).

### epistemic-auditor

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Claim/evidence/status mapping is valuable, but measured/modeled/asserted/assumed are not mutually exclusive grades. Producing a source does not establish a claim, and evidence tags alone are not checks.

**Concrete edits:**

- Separate claim type, source, inference, uncertainty and disposition. Prioritize decision-bearing claims and permit reasoned common ground. Check actual source-to-claim support and use fitting revision conditions rather than mandatory numeric thresholds.

**Boundary:** Grades explicit claims; premise-auditor elicits missing assumptions. Does not replace metacognate or shared minimum evidence discipline.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1908](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1908); [entry at line 1908](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1908).

### ethicist

Current: **available / evaluate**, version 2. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** The core usefully separates can from should. Informed acceptance does not settle every means or precedent question; exclusive specialist deferral can discard the normative layer.

**Concrete edits:**

- State value premises, affected interests, arguments, alternatives and factual assumptions. Separate evidence against facts from reasons to revise a normative conclusion.

**Boundary:** Actual consultation records views, not universal moral resolution. Connect specialist findings to ethical questions; never manufacture consent or rule from private morality.

**Evidence limits:** Reasonable value disagreement can persist after factual agreement; no doctrine is established by this registry. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared explicit ethical-argument method

**Preserve:** Autonomy, means, precedent and explicit value conflict.

**Comparators:** distributive-justice-auditor: allocation; privacy-surveillance-critic: harm; preference-sensitivity-arbitrator: weights; queued procedural-rights-remedies

**Sources:** [id at line 1965](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1965); [object_of_scrutiny at line 1982](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1982); [falsifier_template at line 1990](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1990); [contraindications at line 1996](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1996); [vector at line 2018](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2018); [bias at line 2020](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2020).

### execution-dependency-auditor

Current: **available / evaluate**, version 1. Capability: `process-integrity`. Recommendation: **refine**.

**Rationale:** Sequencing and unowned prerequisites differ from scope and staffing quantity. Single-stream exclusion and parallel-independence-only falsifier omit linear prerequisite failures.

**Concrete edits:**

- Build the smallest relevant map with owners, evidenced edges, uncertainty and slack; check sequential prerequisites as well as parallel work and match falsifiers to findings.

**Boundary:** Do not force a full schedule graph or serialize work from resource sharing alone; show a binding dependency or missing prerequisite.

**Evidence limits:** Sufficient slack can defeat the concern; no schedule or timing was measured. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared prerequisite/dependency method

**Preserve:** Concrete execution ordering and ownership.

**Comparators:** scope-sentinel: work included; workforce-load-auditor: capacity; queued organizational-readiness: prerequisites

**Sources:** [id at line 2025](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2025); [object_of_scrutiny at line 2042](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2042); [falsifier_template at line 2050](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2050); [contraindications at line 2056](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2056); [vector at line 2073](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2073); [bias at line 2075](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2075).

### explainability-steward

Current: **available / evaluate**, version 2. Capability: `maintainability`. Recommendation: **refine**.

**Rationale:** Target-maintainer comprehension and safe modification are distinct from another person possessing operational knowledge.

**Concrete edits:**

- Replace one-head/one-afternoon thresholds with target experience, task and realistic learning budget.
- Assess rationale and local reasoning, not comment-count proxies.
- One successful newcomer change is bounded evidence for that task.

**Boundary:** bus-factor tests transfer; minimalist generates deletion; long-term replaceability examines substitution. Clarity alone does not justify deletion.

**Evidence limits:** Needs representative walkthrough/modification with observation. An agent simulation is expert walkthrough, not a real onboarding study. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2080](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2080); [entry at line 2080](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2080).

### first-principles-rederiver

Current: **available / generate_options**, version 2. Capability: `strategy-alternatives`. Recommendation: **refine**.

**Rationale:** Clean-slate construction inside verified constraints is distinct. Discarding convention universally is poor guidance; constraints already verified are good inputs, not an exclusion. Values and tacit requirements may not reduce to physics/economics.

**Concrete edits:**

- Understand conventional designs before stripping choices. State outcomes, values, constraints and assumptions; derive meaningful alternatives when useful; compare transition costs from the actual present. Permit re-deriving the existing solution as best.

**Boundary:** Works inside accepted constraints; constraint-negotiator changes the set. Generates candidates without authorizing rewrite or replacing evaluation.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2171](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2171); [entry at line 2171](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2171).

### fmea-analyst

Current: **available / evaluate**, version 2. Capability: `reliability`. Recommendation: **refine**.

**Rationale:** Component/function failure enumeration with consequence and detection analysis is worth retaining. Mandatory multiplicative rankings can hide severe risks or imply unjustified precision.

**Concrete edits:**

- Define ordinal/ranking semantics; preserve severe credible failures despite low composite score.
- Do not make arbitrary severity x likelihood x undetectability arithmetic disposition authority.
- Distinguish detection before harm from prevention/mitigation; detection does not rebut every consequence.
- Allow process/function decomposition when appropriate.

**Boundary:** chaos covers combined faults; safety-hazard tracks harm/control interactions; resilience constructs response. Literature review should check limits of conventional FMEA prioritization.

**Evidence limits:** Needs scoped decomposition, evidence/assumptions and timing. Unknown likelihood remains unknown instead of becoming a convenient score. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2227](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2227); [entry at line 2227](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2227).

### forensic-accountant

Current: **available / evaluate**, version 2. Capability: `data-validity`. Recommendation: **refine**.

**Rationale:** Recomputing figures and checking units/baselines differs from pipelines and inference. Calling all unreconciled figures rhetoric rejects legitimate labelled estimates. Its nearest-absorber status for oracle adequacy overstates its numeric remit.

**Concrete edits:**

- Classify measured, estimated, projected and rounded numbers before tolerances. Missing primary data limits confidence rather than automatically falsifying a figure. Keep general oracle adequacy shared, not absorbed solely by this lens.

**Boundary:** Owns numeric sourcing and reconciliation, not all evidential truth or behavioral verification.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2286](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2286); [entry at line 2286](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2286).

### game-theorist

Current: **available / evaluate**, version 2. Capability: `incentives`. Recommendation: **refine**.

**Rationale:** Payoff mapping and profitable deviations are distinct incentives analysis. The card presumes dominant strategies exist and imposes a static boundary even when repeated interaction, incomplete information and commitments determine the actual mechanism.

**Concrete edits:**

- State actors, objectives, information, actions, horizon and enforcement assumptions. Analyze deviations/stable behavior conditionally; allow no dominant strategy or multiple equilibria. Include repeated-game/coalition effects where material.

**Boundary:** Owns incentives under an explicit model. Behavioral-economist checks population assumptions; downstream forecasting examines broader consequences. Shared payoff maps are not independent evidence.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2342](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2342); [entry at line 2342](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2342).

### human-automation-handoff-auditor

Current: **available / evaluate**, version 1. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** Context, practice and authority at control transfer are distinct. Universal atrophy and kill-the-automation language exceed source evidence and test authorization.

**Concrete edits:**

- Map triggers, context, authority and tolerances; propose authorized safe simulations or drills with stated limits. Treat atrophy as a hypothesis.

**Boundary:** Do not infer permission to stop a live system. A missing handoff may itself be a finding if hazards need intervention; autonomous labeling does not settle this.

**Evidence limits:** A representative drill or adequate autonomous safety case may make further use unnecessary. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared takeover-readiness method

**Preserve:** Practiced takeover and explicit control authority.

**Comparators:** on-call-realist: ergonomics; incident-command-auditor: coordination; safety-hazard-auditor: harm chain

**Sources:** [id at line 2451](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2451); [object_of_scrutiny at line 2468](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2468); [falsifier_template at line 2476](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2476); [contraindications at line 2482](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2482); [heuristic at line 2498](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2498).

### integration-weaver

Current: **available / evaluate**, version 2. Capability: `interoperability`. Recommendation: **refine**.

**Rationale:** Reading/exercising an interface from the caller position exposes incompatibility and semantic ambiguity missed by internal correctness review.

**Concrete edits:**

- Remove single-consumer internal code blanket exclusion.
- Do not imply idempotency keys or webhooks are always required.
- Specify preconditions, error/retry semantics, version compatibility and migration commitments. Documentation walkthrough success alone does not prove compatibility.

**Boundary:** distributed semantics examines guarantees; state migration tests stored-format transitions; UI/UX addresses human-facing interaction.

**Evidence limits:** Needs caller needs, actual provider behavior, contract examples and relevant version combinations. Simulated integrator is not an actual newcomer. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2561](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2561); [entry at line 2561](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2561).

### invariant-specification-auditor

Current: **available / evaluate**, version 1. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Correctness properties and their enforcement are useful and distinct. Pure transforms can have invariants, and a formal specification does not prove implementation compliance. Finding three locations does not prove they work.

**Concrete edits:**

- Remove stateless/formally-specified blanket exclusions. State property/domain, enforcement or proof and meaningful violation evidence. Trace preservation and relevant counterexample detection for material risks; do not demand an alarm for every pure function.

**Boundary:** Owns correctness-property preservation. Traceability maps requirements to artifacts; oracle discipline limits what observations establish.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2613](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2613); [entry at line 2613](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2613).

### inversion-thinker

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Failure-path construction is useful elicitation. Perfect sabotage and guaranteed-failure rhetoric can create implausible catastrophes; overlap with a plan does not alone establish causality.

**Concrete edits:**

- Generate plausible failure paths with mechanisms, enabling conditions and discriminating observations; compare against actual plan and prioritize live vulnerabilities. Permit prospective hindsight as an alternative prompt, not an extra diversity seat.

**Boundary:** Elicits plan-failure hypotheses. FMEA covers component failures; separated ordinary lens passes should not be claimed equivalent to a structured panel premortem.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2668](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2668); [entry at line 2668](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2668).

### ip-freedom-to-operate-auditor

Current: **available / evaluate**, version 1. Capability: `legal-compliance`. Recommendation: **refine**.

**Rationale:** Rights provenance differs from data integrity. Internal-only exclusion and a single license-permits-use falsifier are too broad for a method spanning patents, trademarks, copyright and data rights.

**Concrete edits:**

- Separate rights categories and actual use/distribution; map permissions, conditions, gaps and sources. Remove categorical copyleft-equals-infringement assumptions.

**Boundary:** An inventory is not freedom-to-operate clearance or credentials. Internal use is not blanket exemption; one permitted use does not settle unrelated rights.

**Evidence limits:** Applicability depends on context and jurisdiction; no legal research or clearance occurred. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared rights/license issue-spotting method

**Preserve:** Transitive licenses and asset/model/data rights provenance.

**Comparators:** data-provenance-auditor: integrity; contract-risk-allocation-auditor: negotiated risk

**Sources:** [id at line 2721](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2721); [object_of_scrutiny at line 2738](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2738); [causal_mechanism at line 2740](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2740); [falsifier_template at line 2746](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2746); [contraindications at line 2752](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2752); [heuristic at line 2768](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2768).

### jurisdiction-conflicts-auditor

Current: **available / evaluate**, version 1. Capability: `legal-compliance`. Recommendation: **refine**.

**Rationale:** Competing obligations warrant a distinct method. Valid-in-all-claiming-regimes implies completeness that bounded source inspection rarely establishes.

**Concrete edits:**

- Map operations, jurisdiction triggers, dated authoritative obligations and exact collisions; distinguish incompatibility from compatible multiple requirements or missing facts.

**Boundary:** Geographic contact alone does not prove applicability. Unknown legal status remains unresolved; conclusions are scoped issue spotting, not universal compliance.

**Evidence limits:** Queue specializations require distinct fingerprints; no current legal status was researched. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared conflicts-among-regimes method

**Preserve:** Genuine incompatible-obligation detection.

**Comparators:** predatory-regulator: one regime; contract-risk-allocation-auditor: party allocation; queued trade-controls-sanctions/cross-border-escalation: possible specialties

**Sources:** [id at line 2776](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2776); [object_of_scrutiny at line 2793](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2793); [required_evidence at line 2794](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2794); [falsifier_template at line 2801](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2801); [vector at line 2824](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2824).

### lifecycle-impact-auditor

Current: **available / evaluate**, version 1. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** Systematic coverage from creation through operation, abandonment and disposal is a distinct method from distributing a known set of impacts among their bearers. Both can use one impact map, but the proposed packaging combination has not been established.

**Concrete edits:**

- Retain explicit creation, operation, maintenance, abandonment and disposal stages, including obligations, uncertainty and exit provision.
- For each material stage, identify effects, bearers, evidence, deferred costs and responsible parties; preserve stage coverage instead of reducing the method to generic who-pays questions.
- Separate estimates, chosen discount assumptions and intergenerational values. Resolve the current internalized-or-consented versus both threshold inconsistency.

**Boundary:** Lifecycle review discovers impacts and obligations across stages; distributive analysis examines allocation across people/groups, including future bearers. Neither present approval nor a shared map establishes future-party consent or independent corroboration.

**Evidence limits:** No comparative behavioral test establishes equivalent coverage after combining lifecycle and distribution methods. Explicit lifecycle-stage coverage is retained; packaging equivalence remains unestablished. Source inspection and design inference; behavioral benefit untested.

**Original assessor uncertainty:** Tentative source-overlap judgment only. Reverse if a distribution mode loses distinct stage obligations; do not retire before deciding that design question.

**Proposed home:** shared lifecycle-impact method with explicit stage coverage

**Original assessor proposed home:** tentative lifecycle mode of distributive-justice-auditor

**Preserve:** Historical identity and systematic end-of-life coverage.

**Comparators:** distributive-justice-auditor: future-bearer language; century-horizon-architect: operability; queued decommissioning-exit/intergenerational-stewardship

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. A distinct temporal/lifecycle inventory is valuable; source overlap alone does not show that a distribution mode preserves it.

**Original assessor rationale:** Both attribute impacts to bearers. Its present-versus-lifetime boundary conflicts with the distribution card already naming future maintainers and externalities. Stage coverage remains valuable.

**Original assessor proposed edit:**

- Keep a discoverable creation/operation/abandonment/disposal mode with bearer, obligations, uncertainty and exit provision; do not compress it into generic who-pays prose.

**Original assessor boundary:** Separate estimates, chosen discount assumptions and intergenerational values. Present approval is not future-party consent. Resolve the current internalized-or-consented versus both threshold inconsistency.

**Sources:** [id at line 2831](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2831); [object_of_scrutiny at line 2848](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2848); [falsifier_template at line 2856](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2856); [neighbors at line 2865](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2865); [vector at line 2879](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2879); [vector at line 1678](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1678).

### liquidity-runway-auditor

Current: **available / evaluate**, version 1. Capability: `economics`. Recommendation: **refine**.

**Rationale:** Cash timing is distinct from margin and tail risk. Zero cash is not the only failure threshold: covenants, restricted balances, reserves and borrowing conditions may bind first.

**Concrete edits:**

- Keep optional domain lens. Model usable cash, commitments, contractual minima, financing and timing slips at a suitable granularity; name the assumption making a gap bridgeable.

**Boundary:** Owns liquidity timing/near-term funding. Unit economics covers contribution; queued capital-structure stress may cover broader seniority/leverage/refinancing without duplication.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2886](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2886); [entry at line 2886](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2886).

### measurement-critic

Current: **available / evaluate**, version 2. Capability: `data-validity`. Recommendation: **refine**.

**Rationale:** Gaming paths and missing objectives matter, but the card overlaps construct validity while neighbor text claims gaming-only. Previously valid measures can fail after optimization. Goodhart is a conditional mechanism, not a universal prediction.

**Concrete edits:**

- Use shared measurement-fitness method with construct-fit and optimization-robustness modes. For gaming name actor, incentive, feasible action, metric movement, goal harm and mitigation. Detection alone may not remove harm; replace that weak falsifier.

**Boundary:** Keep meaning and optimization effects explicit. Prior validation is not categorical immunity; selecting both modes is not automatic independent corroboration.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2994](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2994); [entry at line 2994](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2994).

### minimalist-zen-master

Current: **available / evaluate**, version 2. Capability: `simplicity`. Recommendation: **refine**.

**Rationale:** Simplification candidates are useful beyond blocking new scope. Recent non-use does not establish that rare-use safeguards lack value, and nonzero use does not automatically defeat a simpler replacement.

**Concrete edits:**

- Use a plain simplification label plus optional historical alias. Compare preserved outcomes, contingency value, maintenance burden, alternatives and transition cost. Treat deletion as a candidate pending relevant origin, consumer and replacement evidence.

**Boundary:** Generates simpler ways to preserve value; does not authorize deletion or equate absent telemetry with absent use. Reuse history work without a compulsory separate gate.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3085](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3085); [entry at line 3085](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3085).

### network-effects-strategist

Current: **available / evaluate**, version 2. Capability: `economics`. Recommendation: **refine**.

**Rationale:** Adoption/value coupling, cold start and congestion are distinct. Cohort value correlated with network size does not establish network effects: selection, product improvement and cohort mix can explain it.

**Concrete edits:**

- State same-side/cross-side mechanism and value unit; distinguish network effects from scale economies/product improvement. Treat observational coupling as suggestive and use causal-identification checks for load-bearing claims.

**Boundary:** Owns how participation changes others value and when that relation holds. Does not manufacture network claims for all multi-user products.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3141](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3141); [entry at line 3141](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3141).

### null-hypothesis-advocate

Current: **available / generate_options**, version 2. Capability: `strategy-alternatives`. Recommendation: **refine**.

**Rationale:** A fair status-quo comparator matters. Mandatory baseline inclusion is confused with mandatory specialist use; the name also suggests a statistical null test. Starting versus continuing is not a hard boundary for inaction analysis.

**Concrete edits:**

- Use status-quo/inaction label with preserved alias. Include delay, limited maintenance or stop where relevant; price dynamic deterioration and benefits. Reuse an adequate baseline rather than invoke again; dedicated use is for weak/unfair baselines.

**Boundary:** Supplies a fair comparator, not a statistical test or required evaluator seat. Applicable to initiation and continuation when inaction is a live option.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3193](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3193); [entry at line 3193](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3193).

### observability-advocate

Current: **available / evaluate**, version 2. Capability: `operability`. Recommendation: **refine**.

**Rationale:** Testing whether failures yield discriminating actionable signals is distinct from recovery ergonomics and forensic custody.

**Concrete edits:**

- Use appropriate detection/diagnosis objectives rather than universal before-users-notice.
- Include noise, missingness, sampling, propagation gaps, cardinality, cost, privacy and response ownership.
- High telemetry volume is not a contraindication when the needed distinction remains invisible.

**Boundary:** on-call handles response; forensicist trustworthy reconstruction; control-effectiveness checks the complete control/response function.

**Evidence limits:** Needs scoped failures and actual signals. Instrumentation presence is weaker than exercised diagnosis/detection. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3247](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3247); [entry at line 3247](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3247).

### on-call-realist

Current: **available / evaluate**, version 2. Capability: `operability`. Recommendation: **refine**.

**Rationale:** A realistic recovery walkthrough under actual responder constraints is a distinct method, suitable for individual and coordinated modes.

**Concrete edits:**

- Replace half-asleep stranger and one-command rollback with explicit experience, safe steps, escalation and recovery objectives.
- Allow forward repair or bounded downtime when rollback is inappropriate.
- Retain manual failure paths even when automation usually works.
- Absorb incident-command as explicit coordinated mode while linking automation handoff.

**Boundary:** observability supplies signals; resilience absorbs failures; bus-factor covers general transfer; command mode adds coordination.

**Evidence limits:** Needs runbook/access/tooling and incident/drill evidence. No escalation is not inherently a requirement; a non-author drill remains bounded evidence. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3303](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3303); [entry at line 3303](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3303).

### performance-alchemist

Current: **available / evaluate**, version 2. Capability: `performance-scale`. Recommendation: **refine**.

**Rationale:** Profile-first analysis of current workload bottlenecks differs from future capacity modeling.

**Concrete edits:**

- Replace P99-always-matters-more with actual latency/throughput/memory/energy/cost objectives.
- Require representative workload, uncertainty, warm/cold behavior and relevant before/after comparison.
- Familiar N+1/index/allocation patterns remain hypotheses until supported.

**Boundary:** scalability projects demand; queue-stability studies feedback; unit economics studies viability.

**Evidence limits:** Needs representative profiles/traces/plans. Without runtime evidence return suspected mechanisms and a discriminator, not measured bottleneck claims. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3473](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3473); [entry at line 3473](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3473).

### polymath-inquisitor

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Reframing differs from premise testing, but requiring cross-field analogy encourages clever ornament when actual goals or scope already reveal the problem. The statement most failures are category errors overclaims prevalence.

**Concrete edits:**

- Use plain problem-framing label; analogy is optional. Compare stated problem, actual user objective, boundary, unit of analysis and alternative formulations; show a concrete decision affected. Remove required cleverness and prevalence claim.

**Boundary:** Questions aim of inquiry while respecting authoritative objectives; no philosophical dissolution of requirements or relitigation without new evidence.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3525](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3525); [entry at line 3525](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3525).

### predatory-regulator

Current: **available / evaluate**, version 2. Capability: `legal-compliance`. Recommendation: **refine**.

**Rationale:** External claims versus practice is useful. The quota-driven regulator stereotype biases scrutiny; policy concordance alone does not establish legality.

**Concrete edits:**

- Prefer neutral display name with historical ID retained. Check factual accuracy separately from dated applicable obligations; mark uncertain legal significance.

**Boundary:** Adversarial reading is neither enforcement testimony nor prediction. Honest policy can describe harmful conduct; operational-control testing is a different method.

**Evidence limits:** Actual applicable guidance may change interpretation; none was verified here. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared disclosure/regulatory-challenge method

**Preserve:** Literal challenge to misleading disclosures and policy/practice gaps.

**Comparators:** compliance-litigator: inward records; control-effectiveness-auditor: operation; privacy-surveillance-critic: harm

**Sources:** [id at line 3634](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3634); [object_of_scrutiny at line 3651](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3651); [falsifier_template at line 3659](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3659); [heuristic at line 3682](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3682); [bias at line 3685](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3685).

### preference-sensitivity-arbitrator

Current: **available / evaluate**, version 1. Capability: `adjudication`. Recommendation: **refine**.

**Rationale:** Already an evaluator despite arbitrator name. Its robustness distinction is useful, but robust conclusions still depend on criteria, scale and chosen weighting ranges.

**Concrete edits:**

- Expose criteria, scales, weight sources, hard constraints and defensible ranges; use qualitative comparisons when cardinal weights lack warrant. Report what changes and why.

**Boundary:** Analyze recorded or explicitly hypothetical preferences without inventing consent or choosing values. Do not relitigate settled authorized priorities merely because other weights are imaginable.

**Evidence limits:** Preference sensitivity does not make a recommendation invalid; better elicitation or criteria may reverse robustness. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared preference-sensitivity method

**Preserve:** Visibility of value-dependent recommendations.

**Comparators:** sovereign-ruler: applies values; bayesian-adjudicator: facts; robust-decision-auditor: uncertain futures

**Sources:** [id at line 3690](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3690); [workflow_role at line 3693](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3693); [object_of_scrutiny at line 3707](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3707); [falsifier_template at line 3715](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3715); [heuristic at line 3737](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3737); [vector at line 3738](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3738); [bias at line 3740](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3740).

### privacy-surveillance-critic

Current: **available / evaluate**, version 2. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** Purpose, retention and linkability are distinct from compliance. Eventual exposure is asserted universally; necessity plus retention alone does not defeat the full harm inventory.

**Concrete edits:**

- Inspect purpose, sensitivity, access, retention, linkability, recipients and future-use controls. Match each harm to its actual defeating observation.

**Boundary:** Necessary retained data may still expose or enable harmful joins. Distinguish risk from inevitability and permission from imagined consent; reuse audits only within scope and freshness.

**Evidence limits:** Architecture/control evidence can defeat a specific path, not establish blanket harmlessness. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared data-practice harm method

**Preserve:** Minimization, purpose limitation and future-owner scrutiny.

**Comparators:** dual-use-adversary: capability abuse; predatory-regulator: obligations; ethicist: values

**Sources:** [id at line 3839](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3839); [object_of_scrutiny at line 3856](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3856); [falsifier_template at line 3864](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3864); [contraindications at line 3870](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3870); [heuristic at line 3891](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3891); [vector at line 3892](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3892).

### protocol-archeologist

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Historical reasons/current consumers matter. Full card demands justification for removal despite a HARD BOUNDARY excluding all deletion; that prevents reuse of the same history in a deletion judgment.

**Concrete edits:**

- Make historical reconstruction shareable wherever provenance matters. Remove deletion adjudication from its output, but permit that output to feed deletion review; synchronize card/fingerprint. Missing records mean unknown, not keep forever.

**Boundary:** Owns supported history and whether originating conditions remain. A change judgment consumes it without mandatory duplicate historical research.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3899](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3899); [entry at line 3899](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3899).

### queue-stability-auditor

Current: **available / evaluate**, version 1. Capability: `performance-scale`. Recommendation: **refine**.

**Rationale:** Arrival/service/backpressure/retry dynamics form a distinct method general scale analysis can miss.

**Concrete edits:**

- Distinguish temporary rate excess from sustained instability; buffers, bursts, variability and recovery matter.
- Remove synchronous request-bounded systems blanket exclusion: thread pools, sockets and retry feedback can queue.
- Name observed/assumed rates, bounds, admission policy, deadlines and recovery window.

**Boundary:** scalability models growth; systemic-logician handles generic feedback; this performs concrete backlog/feedback calculations.

**Evidence limits:** Needs workload distributions and retry/limit behavior. Average-rate approximations do not prove tails or recovery. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 3951](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3951); [entry at line 3951](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3951).

### requirements-traceability-auditor

Current: **available / evaluate**, version 1. Capability: `process-integrity`. Recommendation: **refine**.

**Rationale:** Requirement/artifact/verification gaps matter. Finding a link is not proving it exercises the requirement; necessary enabling code may have no separate requirement.

**Concrete edits:**

- Trace material acceptance claims to supporting artifacts and an adequate observation. Distinguish missing links from vacuous checks; reuse existing evidence instead of mandatory new matrices.

**Boundary:** Apply proportionately to actual acceptance needs, not every function. Do not create new approval gates or claim traceability is the only divergence detector.

**Evidence limits:** Existing acceptance artifacts may suffice; no real requirement was verified here. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared acceptance-coverage trace

**Preserve:** Coverage of obligations, implementation and meaningful verification.

**Comparators:** invariant-specification-auditor: maintained conditions; scope-sentinel: additions; retired verification-oracle-auditor: adequacy remains workflow discipline

**Sources:** [id at line 4171](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4171); [object_of_scrutiny at line 4188](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4188); [falsifier_template at line 4196](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4196); [heuristic at line 4218](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4218); [vector at line 4219](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4219); [bias at line 4221](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4221).

### robust-decision-auditor

Current: **available / evaluate**, version 1. Capability: `temporal-consequence`. Recommendation: **refine**.

**Rationale:** Scenario performance is distinct, but privileging minimax regret imposes an unapproved decision rule. Non-dominance does not prove robustness: an option may be non-dominated and disastrous in a relevant case.

**Concrete edits:**

- State uncertainty dimensions, scenario limits, acceptability thresholds and tradeoffs. Derive criterion from established priorities or expose consequential choice. Report robustness premium/fragility and test the actual robustness claim.

**Boundary:** Examines declared plausible futures without invented probabilities or universal maximal caution. User priorities resolve value choices.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4338](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4338); [entry at line 4338](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4338).

### safety-hazard-auditor

Current: **available / evaluate**, version 1. Capability: `governance-ethics`. Recommendation: **refine**.

**Rationale:** System-action-to-bodily-harm chains are distinct from generic component failure. A universal two-layer threshold proves neither domain compliance nor acceptable residual risk.

**Concrete edits:**

- Trace hazards, exposure, severity, controls and common causes; use applicable domain requirements and authorized acceptance criteria. Evaluate independence and effectiveness rather than count alone.

**Boundary:** No certification or dangerous drill is implied. Separate hazard facts from risk acceptance; two nominal layers do not refute a severe hazard.

**Evidence limits:** A domain rule may require a particular architecture; none was researched or validated here. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared physical-harm-path method

**Preserve:** Physical consequences and foreseeable misuse.

**Comparators:** fmea-analyst: component failure; common-cause-dependency-auditor: shared failure; dual-use-adversary: deliberate abuse

**Sources:** [id at line 4393](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4393); [object_of_scrutiny at line 4410](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4410); [required_evidence at line 4411](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4411); [falsifier_template at line 4418](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4418); [vector at line 4441](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4441).

### scalability-cliff-analyst

Current: **available / evaluate**, version 2. Capability: `performance-scale`. Recommendation: **refine**.

**Rationale:** Growth-to-resource/coordination analysis is useful; requiring cliffs, quadratic cost and exact 10x/100x/1000x breakpoints prejudges behavior and encourages invented precision.

**Concrete edits:**

- Include smooth degradation and hard limits; discontinuity is one result.
- Use actual workload envelope/horizon with uncertainty.
- Do not exclude bounded systems whose bounds may exceed capacity.
- Derive thresholds from measured constants or explicitly provisional models.

**Boundary:** performance profiles current behavior; queue stability models overload. Refine this member instead of reintroducing rejected capacity-envelope-auditor.

**Evidence limits:** Needs growth dimensions, limits, functions, measurements and forecast ranges. Coarse estimates do not justify exact breakpoints. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4448](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4448); [entry at line 4448](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4448).

### scope-sentinel

Current: **available / evaluate**, version 2. Capability: `process-integrity`. Recommendation: **refine**.

**Rationale:** Added scope differs from existing complexity. Requiring a decision and paid-for estimate for every addition can renew permissions for necessary implementation choices.

**Concrete edits:**

- Compare against approved outcome and constraints; distinguish necessary support, materially new outcomes and optional improvements with proportionate costs.

**Boundary:** Authorization persists through handoffs. Ask only for material undecided differences; a document or estimate alone is not authority, and required quality is not scope creep.

**Evidence limits:** A necessary dependency may justify an apparent addition; evaluate against the actual outcome. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared authorized-scope method

**Preserve:** Minimum coherent delivery without gratuitous additions.

**Comparators:** minimalist-zen-master: existing complexity; opportunity-cost-accountant: whole effort; requirements-traceability-auditor: acceptance

**Sources:** [id at line 4504](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4504); [object_of_scrutiny at line 4521](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4521); [falsifier_template at line 4529](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4529); [vector at line 4553](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4553); [bias at line 4555](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4555).

### script-kiddie

Current: **available / evaluate**, version 2. Capability: `security`. Recommendation: **refine**.

**Rationale:** Reachable services checked against insecure defaults and current exploit conditions constitute a concrete method distinct from generic threat enumeration.

**Concrete edits:**

- Use functional discovery title; preserve old alias.
- Remove universal within-hours/no-delay claims.
- Use current authoritative advisories, configuration and exploit prerequisites.
- Negative scans/version checks do not prove safe/unreachable/patched; expose coverage limits.

**Boundary:** STRIDE enumerates classes; adversary path analysis traverses access chains. Exposure inspection has an independently useful observable procedure.

**Evidence limits:** Needs authorized exposure/version/configuration evidence. Card does not authorize external scans or credential attempts. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4560](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4560); [entry at line 4560](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4560).

### second-order-forecaster

Current: **available / evaluate**, version 2. Capability: `temporal-consequence`. Recommendation: **refine**.

**Rationale:** Downstream intervention effects are distinct from static incentives and existing structure. Requiring three hops creates unsupported chains; one quiet window may not refute a delayed or masked outcome.

**Concrete edits:**

- Use only warranted steps, each with mechanism, conditions, evidence, uncertainty and observable sign. Include benefits and harms. Reuse metric/incentive analyses; reduce confidence instead of extending unsupported narrative.

**Boundary:** Provides conditional downstream forecasts, not inevitabilities. Observation window and sensitivity must match the forecast.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4615](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4615); [entry at line 4615](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4615).

### semantic-critic

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **refine**.

**Rationale:** Plain restatement of load-bearing commitments is distinct and useful. Claiming wording reveals what an author cannot or will not see over-infers intent; technical vocabulary may be precise.

**Concrete edits:**

- Focus on material ambiguity, omitted commitments, inconsistent terms and likely misunderstanding. Show faithful readings/restatements and concrete action differences; leave intent unknown without evidence.

**Boundary:** Owns meaning-dependent action differences, not generic style editing, anti-jargon preference or motive diagnosis.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4675](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4675); [entry at line 4675](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4675).

### sociotechnical-topology-auditor

Current: **available / evaluate**, version 1. Capability: `systems-structure`. Recommendation: **refine**.

**Rationale:** Team/component mapping differs from authority or feedback. Political-treaty rhetoric overstates causality; completion without escalation is not required for a legitimate working process.

**Concrete edits:**

- Map ownership, communication, dependencies, intended coordination and observed friction. Trace a representative change including legitimate escalation. Use supported hypotheses rather than automatic org-chart causation.

**Boundary:** Owns fit between human coordination and technical boundaries; mirroring and escalation are not defects by themselves.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4727](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4727); [entry at line 4727](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4727).

### statistical-validity-critic

Current: **available / evaluate**, version 2. Capability: `data-validity`. Recommendation: **refine**.

**Rationale:** Sampling, leakage, multiplicity and uncertainty deserve a distinct method. The card implies most numbers are false and treats persistence under correction as sufficient; inference is not truth certified by p-value.

**Concrete edits:**

- State estimand/population, selection, missingness, effect size, uncertainty, dependence and analytic choices. Ask whether corrected inference changes the decision. Separate no clear effect from evidence of negligible effect.

**Boundary:** Owns quantitative inference; causal, construct and provenance checks address other failure mechanisms.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4948](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4948); [entry at line 4948](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4948).

### systemic-logician

Current: **available / evaluate**, version 2. Capability: `systems-structure`. Recommendation: **refine**.

**Rationale:** Feedback/delay/stock-flow models are useful for recurrence. Structure-rather-than-components is too absolute; diagrams can become unsupported explanations. No displacement in a short window does not validate the model.

**Concrete edits:**

- Separate observations, model assumptions and hypothesized loops; name explained pattern and discriminating observation. Use only relevant structure. Permit containment during investigation and stop at useful depth.

**Boundary:** Owns relevant feedback structure, not every surrounding system. A forecast consuming the model is not an independent corroboration.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 5120](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5120); [entry at line 5120](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5120).

### tech-debt-curator

Current: **available / evaluate**, version 2. Capability: `maintainability`. Recommendation: **refine**.

**Rationale:** Pricing deliberate deferral supports refactor/continuation decisions and differs from ownerless maintenance decay.

**Concrete edits:**

- Evaluate ongoing/avoided cost, risk, opportunity cost and horizon without requiring literal compounding.
- A flat servicing trend can still be intolerably high or precede a known discontinuity.
- Revisit priced/scheduled debt when assumptions change.
- Preserve justified choices to defer.

**Boundary:** entropy audits ownerless work; long-term replaceability checks new commitments; opportunity-cost compares uses of resources.

**Evidence limits:** Needs cost/incident observations or labeled estimates with attribution limits. Co-occurring slowdown alone does not establish causation. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 5176](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5176); [entry at line 5176](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5176).

### ui-ux-polisher

Current: **available / evaluate**, version 2. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** Concrete copy and recovery improvements are useful. The fixed 80/20 assertion is unsupported; no-visual-surface excludes text and voice UX.

**Concrete edits:**

- Offer specific improvements tied to a task; distinguish preference, usability hypothesis and standard violation. Replace the fixed ratio with a qualitative possibility.

**Boundary:** Allow bounded repairs without mandatory prior lenses. Visual polish does not establish accessibility conformance.

**Evidence limits:** Real users may perform worse with a polished alternative; task evidence can reverse the recommendation. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared constructive interface-clarity method

**Preserve:** Constructive copy, affordance and recovery design.

**Comparators:** angry-customer: flow failure; wcag-accessibility-expert: criterion tests

**Sources:** [id at line 5231](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5231); [object_of_scrutiny at line 5248](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5248); [contraindications at line 5262](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5262); [heuristic at line 5279](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5279); [vector at line 5280](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5280).

### unit-economics-adversary

Current: **available / evaluate**, version 2. Capability: `economics`. Recommendation: **refine**.

**Rationale:** Per-unit viability differs from cash timing and alternative allocation. Positive marginal contribution need not cover fixed cost; declared loss leading needs examination rather than automatic exclusion.

**Concrete edits:**

- Separate incremental, contribution and allocated costs, fixed/step costs, acquisition/retention and financing horizon as relevant. Evaluate subsidy/payback explicitly. Replace margin >= 0 universal clearance with the stated business model.

**Boundary:** Owns economic mechanism at relevant scale; immediate profit is not mandatory for funded activity and positive margin is not sufficient sustainability.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 5287](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5287); [entry at line 5287](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5287).

### value-of-information-auditor

Current: **available / evaluate**, version 1. Capability: `economics`. Recommendation: **refine**.

**Rationale:** Discriminator value versus delay fits bounded adaptation. Current falsifier says the test discriminates, which supports rather than refutes the recommendation. Cheapest-first also ignores informativeness and test dependencies.

**Concrete edits:**

- State live options, uncertainty, decision-changing outcomes, informativeness, execution cost, delay and dependencies. Use defensible expected value or qualitative threshold comparison. Refutation is no discrimination, excessive cost/delay or decision insensitivity.

**Boundary:** Owns whether/what to learn; light form can guide adaptive stopping, detailed analysis is optional and does not replace Resolve or add an approval gate.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 5343](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5343); [entry at line 5343](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5343).

### wcag-accessibility-expert

Current: **available / evaluate**, version 2. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** Criterion-to-element checking is useful; the core hardcodes an edition and exempts an operator-accepted gap in an expert internal tool.

**Concrete edits:**

- Require applicable version, level and surface as inputs. Distinguish automated, manual, assistive-technology and untested coverage; retain easy-versus-structural remediation.

**Boundary:** Acceptance does not convert failure into conformance or consent for affected users. Do not imply credentials or full conformance from a partial audit; internal users can have access needs.

**Evidence limits:** No web check was made; this assessment does not claim which WCAG edition applies now. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared scoped accessibility-criteria method

**Preserve:** Standards-based checks and constructive repairs.

**Comparators:** ui-ux-polisher: perceived quality; distributive-justice-auditor: exclusion impact

**Sources:** [id at line 5454](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5454); [object_of_scrutiny at line 5471](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5471); [required_evidence at line 5472](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5472); [contraindications at line 5484](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5484); [vector at line 5498](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5498); [bias at line 5500](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5500).

### workforce-load-auditor

Current: **available / evaluate**, version 1. Capability: `human-factors`. Recommendation: **refine**.

**Rationale:** On-call, interruption and toil arithmetic differs from unique knowledge and service cost. Predicted burnout or exit is not a demonstrated psychological conclusion.

**Concrete edits:**

- Use load, trends, uncertainty and stated sustainable bounds; obtain actual workforce evidence or mark absence. Minimize identifying data.

**Boundary:** Simulated staff cannot establish workload consent or health effects. Separate observed work from projections and judgments about acceptable burden.

**Evidence limits:** Measured representative workloads can refute the forecast; no workload was measured here. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared human-capacity method

**Preserve:** Human capacity as an execution constraint.

**Comparators:** bus-factor-adversary: knowledge; unit-economics-adversary: service cost; queued organizational-readiness: broader capability

**Sources:** [id at line 5505](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5505); [object_of_scrutiny at line 5522](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5522); [required_evidence at line 5523](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5523); [falsifier_template at line 5530](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5530); [vector at line 5553](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5553).


## Proposed combinations as modes

### bayesian-adjudicator

Current: **available / adjudicate**, version 2. Capability: `adjudication`. Recommendation: **combine-as-mode**.

**Rationale:** Already alternate final judge. Its distinctive work is explicit probability updating, not a separate source of authority; falsifier-or-lose language is unsuitable for value commitments.

**Concrete edits:**

- Retain defensible or explicitly elicited priors, justified likelihoods, dependence checks, ranges and posterior calculations as optional adjudication mode. Perspective can reuse the analysis without a verdict.

**Boundary:** Never invent numerical precision or empirically falsify pure normative premises. Missing frequency base rate alone need not preclude an explicitly subjective model, but unsupported numbers confer no authority.

**Evidence limits:** Source-based combination, not measured equivalence. Keep distinct entry if mode selection loses probability-input preconditions. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** Gauntlet probability-adjudication mode; reusable evidence-update method

**Preserve:** Historical ID and warranted probability analysis.

**Comparators:** pragmatic-judge: final role; statistical-validity-critic: inference; preference-sensitivity-arbitrator: values; queued forecast-calibration: historical predictions

**Sources:** [id at line 237](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L237); [workflow_role at line 240](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L240); [object_of_scrutiny at line 253](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L253); [required_evidence at line 254](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L254); [contraindications at line 266](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L266); [vector at line 280](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L280); [bias at line 282](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L282).

### cloud-native-purist

Current: **available / evaluate**, version 2. Capability: `operability`. Recommendation: **combine-as-mode**.

**Rationale:** Already a mutex pair with local-first-survivalist: opposite priors on the same ownership/dependency/cost decision, not distinct mechanisms.

**Concrete edits:**

- Combine under neutral operating-model comparison while retaining aliases and intentional contrast modes.
- Remove assertions that managed substrates eliminate drift/toil, state belongs in databases not disks, and GitOps/horizontal scaling are predetermined answers.
- Compare total burden, failure behavior, exit cost, control requirements and actual workload.

**Boundary:** local-first-survivalist is the existing leverage-vs-sovereignty partner. Continuity tests loss response; this family chooses a sustainable arrangement.

**Evidence limits:** Needs priced alternatives, responsibilities, incident/toil evidence and availability/exit requirements; do not invent provider costs or superiority. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 739](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L739); [entry at line 739](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L739).

### construct-validity-auditor

Current: **available / evaluate**, version 1. Capability: `data-validity`. Recommendation: **combine-as-mode**.

**Rationale:** Construct fit must remain explicit and differs from metric gaming. Measurement-critic already asks whether the number means the true objective, so current fingerprints overlap. Two selectable modes preserve mechanisms without claiming independent coverage.

**Concrete edits:**

- Create construct-fit and optimization-robustness modes of measurement fitness. Preserve historical ID as alias/mode reference. Compare definition, covered dimensions, divergence and alternative instruments; remove agreement of two instruments as proof since they can share a flaw.

**Boundary:** Construct fit examines meaning before optimization; gaming examines target-pressure effects. Either can be selected alone; both are explicit questions, not automatically independent votes.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1139](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1139); [entry at line 1139](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1139).

### disgruntled-maintainer

Current: **available / evaluate**, version 2. Capability: `security`. Recommendation: **combine-as-mode**.

**Rationale:** Substantive method is access-to-action path analysis; insider initial access and motive are scenario parameters. Preserve the mode, not an independent claim based on character flavor.

**Concrete edits:**

- Consolidate with persistent-adversary path analysis; make initial authorized access explicit.
- Remove detection-is-the-only-control: least privilege, separation, limits and revocation also matter.
- Replace motive/personnel speculation with capabilities and consequential paths.
- Do not exclude sole-owner systems when delegated accounts, automation or credential compromise matter.

**Boundary:** state-sponsored-actor traverses similar paths from different initial conditions; STRIDE enumerates classes; opportunistic exposure audit has a separate observable procedure.

**Evidence limits:** Needs access matrix, privilege propagation, sensitive actions and control evidence. Log replay alone cannot demonstrate preventive blocking. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 1522](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1522); [entry at line 1522](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1522).

### local-first-survivalist

Current: **available / evaluate**, version 2. Capability: `operability`. Recommendation: **combine-as-mode**.

**Rationale:** Opposes cloud-native-purist on the same question. Retain custody, exit and offline questions without treating dependencies as inherently unacceptable.

**Concrete edits:**

- Combine with managed mode under neutral operating-model comparison.
- Compare operating cost, off-site recovery, revocation, trust roots and actual offline requirements.
- No self-host option is not a reason to ignore exit/custody risk: export, terms or accepted risk can be relevant.
- Preserve deliberate contrast but do not count two slogans as distinct evidence streams.

**Boundary:** cloud-native is existing mutex partner; continuity tests loss response; recovery-integrity verifies restored state.

**Evidence limits:** Needs dependency/custody maps, required core functions and outage/exit evidence. A local copy alone establishes neither recoverability nor sovereignty. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 2941](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2941); [entry at line 2941](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2941).

### state-sponsored-actor

Current: **available / evaluate**, version 2. Capability: `security`. Recommendation: **combine-as-mode**.

**Rationale:** Identity/supply-chain pivots and evasion matter, but sponsorship is an assumed actor label. The same path-analysis technique underlies the insider profile.

**Concrete edits:**

- Use one neutral method with explicit initial access, capability, objective, persistence and resource assumptions.
- Remove will-not-trigger-detections and owns-supply-chain assertions.
- Use plausible exposure/value at risk rather than hobby/high-value categorical labels.
- Separate blocked, detected, triaged and contained; an alert within retention does not establish timely protection.

**Boundary:** insider is authorized-access mode; script-kiddie becomes exposure inspection; forensicist checks evidence; STRIDE enumerates classes.

**Evidence limits:** Needs trust/access graphs, dependencies, credential lifetime, detection/response evidence and bounded actor assumptions. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 4892](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4892); [entry at line 4892](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4892).

### sunk-cost-liberator

Current: **available / evaluate**, version 2. Capability: `framing-epistemics`. Recommendation: **combine-as-mode**.

**Rationale:** Forward-looking continuation checks matter but specialize reasoning-bias intervention, already duplicated in cognitive-bias card. Zero-history phrasing may wrongly erase current assets, knowledge, options and switching obligations.

**Concrete edits:**

- Preserve ID as continuation/sunk-cost mode of reasoning robustness. Compare feasible choices from actual present: ignore irrecoverable expenditure itself while retaining current assets, remaining costs, exit liabilities, learning and credible payoff.

**Boundary:** Reassesses forward value, not a fictitious greenfield. Remains discoverable but does not count beside cognitive-bias as independent evidence.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 5064](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5064); [entry at line 5064](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5064).


## Proposed role relocations

### adjacent-possible-explorer

Current: **available / evaluate**, version 2. Capability: `strategy-alternatives`. Recommendation: **relocate-role**.

**Rationale:** Its object, questions and card construct a nearby alternative. The evaluate/finding-set role obscures this and lets invention count as evaluation diversity. Nearby recombination differs from clean-slate derivation and advocating an already rejected option.

**Concrete edits:**

- Expose as a generative method usable in Perspective and constructive Gauntlet phases; return an option with retained requirements, changed mechanism, costs, assumptions and discriminator. Remove the presumption that a dominating variant usually exists and that sunk commitment categorically excludes it. Preserve ID/history.

**Boundary:** Searches feasible local variants; does not verify their dominance or authorize expanded scope. Evaluation is a separate contribution, not necessarily a separate agent.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Sources:** [id at line 9](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L9); [entry at line 9](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L9).

### dialectical-synthesizer

Current: **available / adjudicate**, version 2. Capability: `adjudication`. Recommendation: **relocate-role**.

**Rationale:** Demonstrated contradiction: object and neighbor say never rules; output is ruling-set and vector commands rule SPLIT or make a clean call.

**Concrete edits:**

- Output candidate syntheses with supported insights, changed assumptions, residual conflicts and discriminators; adopt option/synthesis contract and remove ruling commands.

**Boundary:** Do not presume both sides partly correct or force reconciliation. New options remain hypotheses needing appropriate scrutiny; the synthesizer cannot approve its own invention.

**Evidence limits:** Textual contradiction proved, behavioral effect untested. Separate synthesis schema versus option-set depends on integration. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** shared constructive synthesis method; Gauntlet pre-adjudication option role

**Preserve:** Constructive reframing and preservation of supported minority insights.

**Comparators:** pragmatic-judge: rules; opposite-steelman: develops one alternative; adjacent-possible-explorer: nearby options

**Sources:** [id at line 1415](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1415); [object_of_scrutiny at line 1431](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1431); [output_contract at line 1438](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1438); [neighbors at line 1448](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1448); [heuristic at line 1457](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1457); [vector at line 1458](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1458).

### governance-lawyer

Current: **available / gate**, version 2. Capability: `process-integrity`. Recommendation: **relocate-role**.

**Rationale:** Selection replay, dissent preservation and verdict arithmetic inspect this review process, not the subject. They are legitimate assurance tasks without being a perspective.

**Concrete edits:**

- Check the actually selected procedure and applicable instructions; automate mechanical invariants where possible. State material mismatch and its effect instead of treating all imperfection as illegitimacy.

**Boundary:** No mandatory new reviewer, model family or permission cycle follows from role name or depth. Preserve useful role separation without counting process assurance as lens diversity or legal expertise.

**Evidence limits:** No runtime audit or selector defect established; recommendation concerns the shared library. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** Gauntlet protocol-conformance role

**Preserve:** Dissent preservation, reproducibility and correct verdict computation.

**Comparators:** decision-rights-auditor: subject authority; red-lines-arbitrator: bounds; compliance-litigator: subject records

**Sources:** [id at line 2398](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2398); [workflow_role at line 2401](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2401); [object_of_scrutiny at line 2414](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2414); [required_evidence at line 2415](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2415); [contraindications at line 2427](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2427); [heuristic at line 2443](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2443); [vector at line 2444](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2444).

### pragmatic-judge

Current: **available / adjudicate**, version 2. Capability: `adjudication`. Recommendation: **relocate-role**.

**Rationale:** Conflict ledger and deciding on the record are legitimate Gauntlet functions. A judge is not a subject lens or a Perspective prerequisite.

**Concrete edits:**

- Preserve reasoned dispositions, quality weights, uncertainty and dissent. Permit insufficient evidence or bounded reopening rather than unsupported forced certainty.

**Boundary:** Do not silently invent evidence during synthesis. Useful functional role separation does not mandate independent model families or new permission gates.

**Evidence limits:** Existing selector already distinguishes judges; no mis-selection shown. Uncertainty result must fit the chosen workflow contract. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** Gauntlet evidence-based adjudication role

**Preserve:** Evidence-weighted conflicts, preserved dissent and coherent next action.

**Comparators:** bayesian-adjudicator: probability mode; dialectical-synthesizer: candidates; sovereign-ruler: authorized value choices

**Sources:** [id at line 3581](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3581); [workflow_role at line 3584](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3584); [object_of_scrutiny at line 3597](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3597); [falsifier_template at line 3605](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3605); [vector at line 3626](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3626); [bias at line 3628](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3628).

### red-lines-arbitrator

Current: **available / gate**, version 2. Capability: `governance-ethics`. Recommendation: **relocate-role**.

**Rationale:** Already a gate rather than an evaluator. Legitimate categorical constraints must survive, but a shared lens persona should not grant decision authority.

**Concrete edits:**

- Record each constraint, source, scope, authority and applicability; test paths against binding instructions/adopted bounds while distinguishing alleged obligations or proposed preferences.

**Boundary:** Irreversibility is not automatically a ban. A model cannot downgrade explicit user prohibitions for failing its philosophical justification test. Missing applicability is uncertainty, not permission.

**Evidence limits:** No current runtime mis-seating is alleged; relocation concerns the future shared-library interface. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** Gauntlet constraint-application role plus reusable constraint inventory

**Preserve:** Established constraints with provenance before optimization.

**Comparators:** governance-lawyer: panel rules; ethicist: values; sovereign-ruler: authorized choices; constraint-negotiator: negotiable bounds

**Sources:** [id at line 4061](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4061); [workflow_role at line 4064](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4064); [object_of_scrutiny at line 4078](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4078); [falsifier_template at line 4086](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4086); [vector at line 4109](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4109).

### sovereign-ruler

Current: **available / adjudicate**, version 2. Capability: `adjudication`. Recommendation: **relocate-role**.

**Rationale:** Core correctly restricts rulings to recorded values or a memo. Operator-bears-consequences language erases third parties; explicit reasoning cannot make a technical fact false.

**Concrete edits:**

- Trace value premises and delegated choices to source. Separate facts, preferences and authority; apply settled priorities within scope, otherwise surface the unresolved tradeoff.

**Boundary:** Do not impersonate stakeholders or infer unlimited authority from ownership. Preference may change the chosen option, not waive others rights or falsify an empirical finding.

**Evidence limits:** Existing authorization may settle choice; reuse it rather than renew approval. No actual third-party right was assessed. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** Gauntlet decision-owner interface and authorized preference application

**Preserve:** Recorded priorities and explicit memo when a real choice remains.

**Comparators:** pragmatic-judge: evidence; red-lines-arbitrator: bounds; decision-rights-auditor: real authority; preference-sensitivity-arbitrator: dependency

**Sources:** [id at line 4782](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4782); [object_of_scrutiny at line 4798](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4798); [falsifier_template at line 4806](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4806); [contraindications at line 4811](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4811); [heuristic at line 4828](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4828); [vector at line 4829](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4829); [bias at line 4831](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L4831).


## Preserve existing retirements

### constraint-inverter

Current: **retired / none**, version 2. Capability: `historical`. Recommendation: **keep-retired**.

**Rationale:** The successor already tests removal versus accommodation costs. Hostile stance alone is not a distinct mechanism.

**Concrete edits:**

- Keep the expensive-contortion challenge with sourced constraint, authority and feasible costed removal path.

**Boundary:** A hard obligation does not become negotiable because removal is cheap. Preserve retired ID/version/card/provenance/superseded_by; never count alias as another diversity unit.

**Evidence limits:** Reactivation needs a distinct mechanism, not persona tone; none was established. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** remain retired; critical mode of constraint-negotiator

**Preserve:** Historical coordinate and critical accommodation-cost question.

**Comparators:** constraint-negotiator: absorber; constraint-relaxer: same operation constructive; red-lines-arbitrator: binding bounds

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. This is an existing historical retirement, not a proposed new v7 reduction. Preserve any useful successor, mode or shared-discipline note without counting the old merger again.

**Historical identity:** Preserve the retired ID, version, card, provenance and superseded_by so historical runs remain interpretable. Do not select or reactivate the retired coordinate. Existing successor: `constraint-negotiator`.

**Historical note:** Merged 2026-07-10 with constraint-relaxer into constraint-negotiator: same mechanism from the critical direction; merged.

**Sources:** [id at line 1013](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1013); [status at line 1015](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1015); [vector at line 1039](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1039); [bias at line 1041](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1041); [superseded_by at line 1043](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1043); [notes at line 1044](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1044).

### constraint-relaxer

Current: **retired / none**, version 2. Capability: `historical`. Recommendation: **keep-retired**.

**Rationale:** Free/infinite/gone can unlock options; successor already pairs it with real removal-versus-retention cost. Optimism and criticism are modes of one operation.

**Concrete edits:**

- Retain explicitly hypothetical relaxation, then demand a feasible path and actual costs before recommendation.

**Boundary:** Imagining an option is not authority to change its constraint. Preserve historical identity and successor mapping without a selectable duplicate.

**Evidence limits:** Only a genuinely different mechanism warrants reactivation. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** remain retired; constructive mode of constraint-negotiator

**Preserve:** Constructive possibility generation and historical interpretation.

**Comparators:** constraint-negotiator: absorber; constraint-inverter: critical counterpart; first-principles-rederiver: within constraints

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. This is an existing historical retirement, not a proposed new v7 reduction. Preserve any useful successor, mode or shared-discipline note without counting the old merger again.

**Historical identity:** Preserve the retired ID, version, card, provenance and superseded_by so historical runs remain interpretable. Do not select or reactivate the retired coordinate. Existing successor: `constraint-negotiator`.

**Historical note:** Merged 2026-07-10 with constraint-inverter into constraint-negotiator: same what-if-the-constraint-were-gone mechanism; the merged card prices removal vs retention explicitly.

**Sources:** [id at line 1104](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1104); [status at line 1106](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1106); [heuristic at line 1129](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1129); [vector at line 1130](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1130); [superseded_by at line 1134](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1134); [notes at line 1135](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L1135).

### first-principles-engineer

Current: **retired / none**, version 2. Capability: `historical`. Recommendation: **keep-retired**.

**Rationale:** The recorded merger identifies identical re-derivation with different tone. Successor retains verified constraints and migration comparison.

**Concrete edits:**

- Preserve challenge to inherited choices with verified requirements and all-in transition cost rather than assuming convention false.

**Boundary:** Keep historical identity and mapping, not an independent seat. Compatibility and obligations remain evidence, not disposable tradition.

**Evidence limits:** Textual overlap supports continued retirement; no behavioral equivalence test was run. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** remain retired; first-principles-rederiver mode

**Preserve:** Historical critical re-derivation framing.

**Comparators:** first-principles-rederiver: absorber; protocol-archeologist: provenance; constraint-negotiator: changes constraints

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. This is an existing historical retirement, not a proposed new v7 reduction. Preserve any useful successor, mode or shared-discipline note without counting the old merger again.

**Historical identity:** Preserve the retired ID, version, card, provenance and superseded_by so historical runs remain interpretable. Do not select or reactivate the retired coordinate. Existing successor: `first-principles-rederiver`.

**Historical note:** Merged 2026-07-10 into first-principles-rederiver: identical re-derivation mechanism, differing only in stance flavor (hostile vs generative). Persona flavor is not novelty.

**Sources:** [id at line 2136](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2136); [status at line 2138](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2138); [vector at line 2162](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2162); [bias at line 2164](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2164); [superseded_by at line 2166](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2166); [notes at line 2167](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L2167).

### meta-epistemic-auditor

Current: **retired / none**, version 2. Capability: `historical`. Recommendation: **keep-retired**.

**Rationale:** Measured/modeled distinctions, uncertainty and update conditions are already in the successor; another uncertainty persona duplicates one claim inventory.

**Concrete edits:**

- Retain unknowns, defeating evidence and supported confidence ranges; prefer qualitative uncertainty over fabricated error bars.

**Boundary:** Preserve identity/mapping. Connect uncertainty to the real decision and deadline rather than unbounded humility or process.

**Evidence limits:** Reconsider if combined use drops update conditions; source inspection cannot prove runtime retention. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** remain retired; epistemic-auditor uncertainty/update mode

**Preserve:** Failure conditions of knowledge claims and updating.

**Comparators:** epistemic-auditor: absorber; statistical-validity-critic: inference; value-of-information-auditor: whether further learning matters

**Reconciliation:** Original assessor recommendation: `combine-as-mode`. This is an existing historical retirement, not a proposed new v7 reduction. Preserve any useful successor, mode or shared-discipline note without counting the old merger again.

**Historical identity:** Preserve the retired ID, version, card, provenance and superseded_by so historical runs remain interpretable. Do not select or reactivate the retired coordinate. Existing successor: `epistemic-auditor`.

**Historical note:** Merged 2026-07-10 into epistemic-auditor v2: claim/evidence/status grading and uncertainty/update-threshold auditing are one diagnostic act on one object (the claim inventory), not two lenses.

**Sources:** [id at line 3050](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3050); [status at line 3052](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3052); [vector at line 3076](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3076); [bias at line 3078](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3078); [superseded_by at line 3080](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3080); [notes at line 3081](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3081).

### premortem-facilitator

Current: **retired / none**, version 2. Capability: `historical`. Recommendation: **keep-retired**.

**Rationale:** Retirement distinguishes prospective hindsight from independent participant narratives. Treating the independent-lens barrier as participant input risks confusing simulations with real stakeholder knowledge.

**Concrete edits:**

- Keep solo failure counterfactuals in inversion-thinker. Offer actual participant narratives before cross-talk when requested/available; record source and uncertainty before synthesis.

**Boundary:** Several model narratives are not affected people or proof of agreement. Do not claim everyone already knows failure; preserve retired selection status and historical coordinate.

**Evidence limits:** No participant session observed. Real elicitation may reveal local knowledge absent from model-only inversion; preserve this distinct function. Source inspection and design inference; behavioral benefit untested.

**Proposed home:** remain retired evaluator; actual participant elicitation protocol plus solo inversion mode

**Preserve:** Diverse causal stories and genuinely participatory facilitation.

**Comparators:** inversion-thinker: solo absorber; queued stakeholder-representation: actual voices; dialectical-synthesizer: supported inputs

**Reconciliation:** Original assessor recommendation: `relocate-role`. This is an existing historical retirement, not a proposed new v7 reduction. Preserve any useful successor, mode or shared-discipline note without counting the old merger again.

**Historical identity:** Preserve the retired ID, version, card, provenance and superseded_by so historical runs remain interpretable. Do not select or reactivate the retired coordinate. Existing successor: `inversion-thinker`.

**Historical note:** Retired as a standalone evaluator 2026-07-10: single-agent prospective hindsight duplicates inversion-thinker's mechanism. The distinct value of a premortem — independent participant narratives elicited BEFORE cross-talk — is a PANEL METHODOLOGY (the gauntlet's independent-lens barrier already implements it) and is documented in reference/execution-model.md, not a lens card.

**Sources:** [id at line 3804](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3804); [status at line 3806](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3806); [heuristic at line 3829](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3829); [vector at line 3830](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3830); [superseded_by at line 3834](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3834); [notes at line 3835](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L3835).

### verification-oracle-auditor

Current: **retired / none**, version 1. Capability: `data-validity`. Recommendation: **keep-retired**.

**Rationale:** Keep retired identity: oracle adequacy is already shared Gauntlet discipline. Shared library must also make that discipline accessible to Perspective. Forensic-accountant is a nearest historical lens, not a full semantic replacement.

**Concrete edits:**

- Preserve retired ID/version/card/provenance/superseded_by; add explicit shared-discipline destination. Map claim to exercised behavior, observation and blind spots; use negative control/seeded violation proportionately. Direct observation also has coverage limits.

**Boundary:** Evidence discipline, not diversity seat or mandatory mutation campaign. Perspective can apply a focused oracle check without reviving a retired evaluator.

**Evidence limits:** Source inspection does not establish better model behavior, activation reliability, false-positive rate or cost-benefit. Source inspection and design inference; behavioral benefit untested.

**Reconciliation:** Original assessor recommendation: `relocate-role`. This is an existing historical retirement, not a proposed new v7 reduction. Preserve any useful successor, mode or shared-discipline note without counting the old merger again.

**Historical identity:** Preserve the retired ID, version, card, provenance and superseded_by so historical runs remain interpretable. Do not select or reactivate the retired coordinate. Existing successor: `forensic-accountant`.

**Sources:** [id at line 5398](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5398); [entry at line 5398](../../plugins/epistemic-skills/skills/gauntlet/roster/registry.json#L5398).

## Evidence limits

- The member recommendations are source inspection and design inference. They do not establish comparative model benefit, trigger reliability, false-positive rates, merger equivalence or favorable runtime cost-benefit.
- Literature can support or challenge a mechanism without validating an exact prompt or this library as a package. This inventory makes no such validation claim.
- Every current status and role is reported separately from the recommendation. No canonical registry, generated roster, skill implementation, installed copy or release was changed by this assessment.
- Role and disposition counts describe this snapshot. Proposed combinations or relocations are not arithmetic forecasts of the final library size.
- Original assessor recommendations and full substantive records remain included where reconciliation changes the proposed disposition. Historical provenance is retained as historical text, not current admission policy.
