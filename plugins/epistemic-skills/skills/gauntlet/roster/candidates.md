<!-- GENERATED from registry.json by scripts/render_roster.py — DO NOT EDIT BY HAND -->

# Expansion frontier — available evaluators

Complete fingerprints whose provenance records the former admission lifecycle. They are available to the ordinary subject-seeded selector; provenance never changes claim weight.

---

## business-continuity-auditor  *(base-adversarial)*
**Method:** Nontechnical continuity (family `business-continuity-auditor`, mode `default`)
**Question:** Can critical operations continue through loss of a vendor, account, license or facility until a viable replacement exists?
**Mechanism:** Nontechnical dependency loss can outlast technical failover and exhaust the usable replacement window.
**Evidence needed:** Critical nontechnical dependencies, applicable terms and notice periods, interruption tolerance, egress/access rights and evidenced replacement windows.
**Procedure:** Identify critical nontechnical dependencies, current terms and loss scenarios. Compare interruption tolerance with evidenced replacement time, access and costs. Distinguish a tabletop plan from exercised continuity and reuse knowledge-succession evidence.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise the continuity gap when a supported replacement or exercised path fits the required window; discussion alone does not demonstrate continued operation.
**Limits:** local-first-survivalist compares ownership choices; bus-factor tests knowledge transfer; recovery-integrity tests restored-state correctness.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `bus-factor-adversary` — Succession examines knowledge and access transfer; continuity examines vendor, account, license and facility loss until replacement.; `local-first-survivalist` — Operating-model comparison chooses an arrangement; continuity checks its response to specific dependency loss.; `recovery-integrity-auditor` — Recovery integrity checks usable restored state; continuity checks the nontechnical window and replacement path.

---

## causal-identification-auditor  *(base-metatextual)*
**Method:** Causal identification (family `causal-identification-auditor`, mode `default`)
**Question:** Does the evidence support this intervention claim for the target population and horizon?
**Mechanism:** Confounding, selection, interference and implementation failures can make an observed association differ from an intervention effect.
**Evidence needed:** Estimand, target population, intervention/comparator, horizon, design implementation, identification assumptions and relevant sensitivity or discriminating evidence.
**Procedure:** State estimand, intervention, comparator, population and horizon. Identify assumptions and rival causal explanations. Check randomization implementation, attrition, noncompliance, measurement and transport where material. Use a discriminating design or sensitivity analysis at proportionate rigor.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise or narrow the claim when a plausible identification failure changes the decision-relevant effect; persistence after statistical adjustment alone does not establish identification.
**Limits:** Owns whether evidence licenses the intervention claim; statistics owns inference mechanics and provenance owns data integrity.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `statistical-validity-critic` — stats critic attacks inference mechanics broadly; this owns the causal-identification question exclusively; `measurement-critic` — measurement attacks the metric-goal gap; this attacks the cause-effect gap

---

## common-cause-dependency-auditor  *(base-adversarial)*
**Method:** Shared dependency analysis (family `common-cause-dependency-auditor`, mode `default`)
**Question:** Which shared dependencies defeat the claimed failure-domain protection?
**Mechanism:** Nominally redundant paths can share a dependency that disables the promised service.
**Evidence needed:** Dependency traces scoped to the claimed failure domains, known intersections, accepted sharing, consequential service effects and topology gaps.
**Procedure:** Trace dependency closure only as far as needed for the claimed failure domains. Identify intersections, accepted sharing, hidden exposure and missing topology evidence. Determine consequences for the promised service; reuse fault exercises with their original scope.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise the common-cause finding when supported dependency or consequence evidence shows the shared element cannot defeat the claimed outcome; absolute disjointness is not required.
**Limits:** Common-cause analysis statically traces dependency intersections and shared fate; chaos/fault injection dynamically exercises combinations. Their artifacts may be shared, but the same evidence cannot count twice.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `chaos-monkey` — Static intersection analysis and dynamic fault-combination exercises remain separately selectable; reuse of a drill is not new corroboration.; `black-swan-catalyst` — Shared-dependency analysis checks the promised failure-domain protection; fragility analysis examines viability thresholds.

---

## concurrency-interleaving-auditor  *(base-adversarial)*
**Method:** Reachable interleaving analysis (family `concurrency-interleaving-auditor`, mode `default`)
**Question:** Which reachable operation schedule violates a named invariant?
**Mechanism:** A permitted ordering of concurrent operations or retries can break an invariant that holds in isolated execution.
**Evidence needed:** Named invariant, relevant runtime guarantees and versioned transitions/code/configuration, concrete schedule and reachability argument; deterministic reproduction or bounded model evidence where available
**Procedure:** Name the invariant and code/configuration/runtime versions. Enumerate relevant operation pairs and write a stepwise thread or message schedule including retry points. Establish reachability under actual ordering guarantees before claiming a defect. Reproduce deterministically where possible; separately label counterexample reproduction, bounded search and formal proof. A guessed ordering is a hypothesis and a clean stress test does not prove unreachability.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Withdraw the specific counterexample if an applicable ordering proof excludes its schedule or the traced final state preserves the invariant; narrow confidence when a bounded search merely finds no witness.
**Limits:** distributed-semantics audits guarantees; invariant-specification finds required conditions; this constructs violating schedules.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `chaos-monkey` — chaos-monkey injects component FAULTS; this audits instruction/message ORDERINGS; `distributed-semantics-auditor` — semantics-auditor audits declared consistency contracts; this finds concrete violating schedules

---

## construct-validity-auditor  *(base-metatextual, mutex:measurement-fitness-modes)*
**Method:** Measurement fitness: construct fit (family `measurement-fitness`, mode `construct-fit`)
**Question:** Does the instrument cover the intended construct well enough for this decision?
**Mechanism:** An operational measure may omit or distort a decision-relevant dimension of the construct even before anyone optimizes it.
**Evidence needed:** the construct-to-instrument mapping per key measure, known divergence cases, alternative operationalizations compared
**Procedure:** Define the construct and intended decision; map instrument items or fields to covered and omitted dimensions. Examine known divergence cases and compare alternative instruments and option rankings. Check whether agreement reflects shared data, assumptions or the same flaw. Record decision sensitivity to divergences. Keep construct fit separate from the optimization-robustness question of measurement-critic; either mode may be used alone and their shared mechanism is not two independent confirmations.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a specific mismatch when relevant dimensions and divergence cases are adequately represented or cannot affect the decision; agreement of two instruments alone does not establish validity.
**Limits:** Construct fit examines meaning before optimization; gaming examines target-pressure effects. Either can be selected alone; both are explicit questions, not automatically independent votes.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `statistical-validity-critic` — Statistical inference checks sampling and inference; construct fit checks the meaning of the measure.; `measurement-critic` — Another discoverable mode of measurement-fitness; intentional contrast counts as one diversity unit, not independent corroboration.

---

## contract-risk-allocation-auditor  *(base-adversarial)*
**Method:** Contractual risk allocation (family `contract-risk-allocation-auditor`, mode `default`)
**Question:** For the named loss or exit scenario, which party bears which risk under the governing documents?
**Mechanism:** Definitions, amendments and precedence rules can allocate exposure differently from the parties assumptions.
**Evidence needed:** Available governing documents and versions, missing-document inventory, scenario-to-definition/clause/precedence trace and sources for any negotiability comparison
**Procedure:** Inventory available governing documents and missing amendments. Trace material loss and termination scenarios through definitions, caps, exclusions, indemnities and precedence clauses. Compare the resulting allocation with stated assumptions. Classify clear conflict, competing interpretation, missing document and legal uncertainty separately. Source any comparison about negotiability; neither standard wording nor a market label establishes safety or negotiability. Keep contractual allocation distinct from public-law compliance and present issue spotting rather than a legal opinion.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise an allocation finding when a governing amendment, precedence rule or supported interpretation resolves the named scenario; uncertainty remains where authority or documents are missing.
**Limits:** Issue spotting is not a legal opinion. Do not assume standard terms are safe or negotiable; keep party allocation distinct from public-law compliance.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `compliance-litigator` — litigator mines internal records as exhibits; this reads the external paper's allocation; `predatory-regulator` — regulator reads against a regime; this reads party-vs-party allocation

---

## control-effectiveness-auditor  *(base-adversarial)*
**Method:** Control effectiveness (family `control-effectiveness-auditor`, mode `default`)
**Question:** Does the named control adequately address its risk on the paths and time window claimed?
**Mechanism:** A well-designed control can leave coverage gaps or fail in operation or response, creating assurance beyond what the evidence supports.
**Evidence needed:** Control purpose and risk, implementation/configuration, covered paths, relevant operation and response history, scoped authorized test or inspection evidence
**Procedure:** Choose material security, financial, operational or procedural controls. Separate design adequacy, implemented coverage, observed operation, response and residual risk. Inspect configuration, relevant history and response records; absence of firing history alone is not failure. Use authorized fixtures or inspection when real violation or bypass tests are unavailable. Where authorized, test representative positive and negative cases and follow the response. Limit each planted violation result to its tested path; evaluate the observation method as shared evidence discipline.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise the specific design, coverage or operation concern with matching evidence; a successful planted case only rebuts that path and cannot establish all-control effectiveness.
**Limits:** Oracle adequacy is retired into Gauntlet discipline; make that discipline reusable. This method tests subject controls, not just the review apparatus.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `predatory-regulator` — Public-law compliance checks applicable obligations; this tests subject controls regardless of regime.

---

## decision-rights-auditor  *(base-metatextual)*
**Method:** Decision authority and accountability (family `decision-rights-auditor`, mode `default`)
**Question:** Who may make the consequential decision, on what evidence, and who bears its consequences?
**Mechanism:** An unsupported or contested allocation of authority can leave decisions unowned or separate power from accountability.
**Evidence needed:** the decision inventory with per-decision owner, authority source, and accountability bearer
**Procedure:** Select consequential decisions and trace the decision-maker, authority source and consequence bearers. Classify authority as documented, delegated, inferred, contested or missing. Preserve evidenced informal arrangements and working delegations. Distinguish accountability ownership from affected-party rights and participation. Report a concrete gap and its effect without inventing an approver or renewing authorization already settled.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a claimed gap when applicable records or demonstrated delegation establish effective authority; participation or rights questions are not settled merely by naming an owner.
**Limits:** Detect existing gaps without inventing approvers or renewing settled authorization. Distinguish ownership from affected-party rights and participation.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `governance-lawyer` — lawyer gates THIS panel's procedure; this audits the SUBJECT's decision-rights structure; `incident-command-auditor` — IC audits decision authority during incidents; this audits it in steady state

---

## distributed-semantics-auditor  *(base-adversarial)*
**Method:** Distributed guarantee composition (family `distributed-semantics-auditor`, mode `default`)
**Question:** Do versioned component guarantees compose to meet the operation's required semantics under the stated conditions?
**Mechanism:** Composition can assume stronger delivery, consistency or ordering guarantees than a dependency provides within its actual envelope.
**Evidence needed:** the semantic contract each component claims vs provides, partition/failover behavior evidence
**Procedure:** Define operation scope, required delivery/consistency semantics and assumptions. Read version-specific authoritative guarantees and configuration for each hop; compare required with provided behavior during partitions, retries and failover. Examine relevant histories or an explicit model of the composed path. Scope exactly-once claims to their operation and assumptions. Record checked histories and fault envelope; documentation or one successful fault test does not prove all composed semantics. Reuse concrete interleaving evidence without double-counting the finding.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a mismatch when version-specific guarantees and the composition argument cover its assumptions or a claimed violation is disproved; clean tested histories only support their bounded envelope.
**Limits:** concurrency-interleaving constructs violations; integration-weaver examines caller contract usability. Share evidence rather than repeat findings.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `concurrency-interleaving-auditor` — interleaving finds concrete schedules; this audits the declared semantic contracts; `chaos-monkey` — chaos-monkey probes coupling generally; this audits consistency semantics specifically

---

## effective-configuration-auditor  *(base-adversarial)*
**Method:** Effective configuration at the consumer (family `effective-configuration-auditor`, mode `default`)
**Question:** Which value or instruction actually reaches the consumer, and does it persist as intended?
**Mechanism:** Precedence, deployment state or reload behavior can separate stored intent from loaded and consumed configuration.
**Evidence needed:** Redacted supported effective-state/context inspection or discriminating probes, winning sources, process/host revisions, environment and persistence evidence
**Procedure:** Choose decision-bearing keys or instruction claims. Record process/host revision and environment; distinguish intended, stored, loaded and consumed state. Use supported resolved-value or context inspection, or a discriminating behavior probe, to identify the winning source and precedence. Redact sensitive values. Compare relevant environments and check restart or reschedule persistence through authorized evidence or tests. Apply instruction analysis only where the host exposes evidence; a declared file does not prove loading.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a specific mismatch when the identified consumer on the relevant revision receives the intended value and required persistence is evidenced; stored files alone cannot rebut a consumption or restart concern.
**Limits:** entropy checks decay; cutover checks transitions; did-it-land/context-audit can call this method instead of duplicating it.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `entropy-demon` — entropy hunts unowned decay; this audits the live resolution of owned-but-layered intent; `release-cutover-auditor` — cutover audits the event; this audits the standing configuration state

---

## execution-dependency-auditor  *(base-adversarial)*
**Method:** Execution prerequisites and sequencing (family `execution-dependency-auditor`, mode `default`)
**Question:** Which evidenced dependency or missing prerequisite threatens the intended sequence or completion?
**Mechanism:** A plan can miss a binding prerequisite or capacity constraint and consume its available slack before the dependent work can start.
**Evidence needed:** Small relevant dependency map with owners, evidenced edges, uncertainty, available slack and binding resource/timing evidence where claimed
**Procedure:** Build the smallest relevant map of tasks, owners, prerequisite edges, resources, uncertainty and slack. Source each consequential edge and check sequential prerequisites as well as parallel work. For a claimed collision, show the binding capacity or dependency and its timing effect; resource sharing alone does not require serialization. Identify unowned prerequisites and assess their effect without forcing a complete schedule graph.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a named concern when the prerequisite is supplied with ownership, the edge proves nonbinding, or evidenced slack/capacity absorbs the delay; match the check to the particular finding.
**Limits:** Do not force a full schedule graph or serialize work from resource sharing alone; show a binding dependency or missing prerequisite.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `scope-sentinel` — sentinel polices WHAT is in the plan; this audits the ORDER/dependency structure of what remains; `workforce-load-auditor` — workforce audits human capacity; this audits sequencing and prerequisite ownership

---

## human-automation-handoff-auditor  *(base-adversarial)*
**Method:** Automation takeover readiness (family `human-automation-handoff-auditor`, mode `default`)
**Question:** Can the intended person take control with sufficient context, authority and time?
**Mechanism:** When automation transfers control during an exceptional condition without usable context or practiced skills, a person may miss the response tolerance; atrophy is a hypothesis requiring evidence.
**Evidence needed:** the handoff inventory: each automated-to-manual transition, its context transfer, practice recency, authority definition
**Procedure:** List transition triggers, receiving roles, context, authority, access, practice recency and time/error tolerances. Include hazards needing intervention even if the design calls itself autonomous. Trace an incident or propose an authorized safe simulation exercising takeover and state its limits; never infer permission to stop a live system. Compare the manual baseline and any autonomous safety case before identifying a gap.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a named gap when representative takeover evidence meets that requirement within tolerance, or an adequate safety case shows intervention is unnecessary. A clean drill supports only exercised conditions.
**Limits:** Do not infer permission to stop a live system. A missing handoff may itself be a finding if hazards need intervention; autonomous labeling does not settle this.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `on-call-realist` — on-call audits incident recovery ergonomics; this audits the automation-to-human control transfer specifically; `behavioral-economist` — economist attacks behavioral assumptions broadly; this owns the handoff seam

---

## incident-command-auditor  *(base-metatextual)*
**Method:** Incident coordination (family `incident-command-auditor`, mode `default`)
**Question:** Can concurrent responders coordinate decisions, information and handoffs within incident objectives?
**Mechanism:** Conflicting decision rights or delayed information may cause parallel actions to interfere and worsen an incident; coordination need not use a particular command hierarchy.
**Evidence needed:** Scoped incident/drill timeline, concurrent actions, intended and actual decision rights, communication/handoff records, delays and consequences.
**Procedure:** Choose a consequential multi-responder incident or authorized drill. Reconstruct timestamped actions, decision rights, information arrival, handoffs and stakeholder updates. Compare practiced and intended coordination; link duplicated/conflicting work or delays to named consequences. Check proposed corrections against those consequences and proportionality. Reuse individual recovery and automation-transfer evidence while keeping coordination distinct.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a defect when corrected timeline or role evidence removes its mechanism or consequence; narrow it when a representative drill demonstrates timely coordinated action. One clean incident cannot establish future reliability.
**Limits:** Incident command examines coordination between responders; on-call recovery examines whether an individual can diagnose and restore safely. Decision-rights and human-automation handoff provide relevant inputs without compulsory repeat review.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `on-call-realist` — Individual safe diagnosis and recovery versus this distinct method for coordination among responders.; `human-automation-handoff-auditor` — Automation control transfer supplies evidence but does not establish multi-responder coordination.

---

## invariant-specification-auditor  *(base-metatextual)*
**Method:** Correctness property preservation (family `invariant-specification-auditor`, mode `default`)
**Question:** What material properties must hold, over which domain, and what establishes preservation?
**Mechanism:** A specification or formal model can diverge from implementation; the presence of specification, enforcement and monitoring does not prove protection.
**Evidence needed:** Explicit properties/domains, implementation paths, enforcement or proof assumptions, and meaningful preservation/violation evidence.
**Procedure:** State material properties and input/state domains, including pure transforms. Trace preservation through transitions and boundaries to enforcement, proof assumptions or tests. Examine meaningful violations and whether checks detect them; distinguish model proof from implementation compliance. For material runtime hazards inspect appropriate detection/response without demanding an alarm for every pure function. Report uncovered cases and discriminating evidence.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a violation claim when a valid scoped proof or representative counterexample test establishes preservation under disputed conditions, or an authorized requirement/domain correction removes the conflict. Merely locating artifacts is insufficient.
**Limits:** Owns correctness-property preservation. Traceability maps requirements to artifacts; oracle discipline limits what observations establish.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `epistemic-auditor` — epistemic grades claim/evidence status; this audits the invariant inventory specifically; `fmea-analyst` — FMEA enumerates failure modes; this enumerates the correctness conditions failures would violate

---

## ip-freedom-to-operate-auditor  *(base-adversarial)*
**Method:** Rights and permitted-use review (family `ip-freedom-to-operate-auditor`, mode `default`)
**Question:** Which rights and conditions apply to actual use and distribution?
**Mechanism:** Permissions or restrictions on components, data, names or mechanisms may not match intended use; permission in one rights category does not settle other categories.
**Evidence needed:** Asset/dependency and mechanism inventory, category-specific provenance/source terms, actual use/distribution, relevant jurisdictions and applicability gaps.
**Procedure:** Inventory code, assets, models, data, names and mechanisms with provenance and actual use/distribution. Separate copyright/license conditions, patents, trademarks and data rights. Map each to dated sources, context, jurisdictions, permissions, conditions and gaps. Internal use is no blanket exemption and copyleft alone is not infringement. Mark missing current authoritative research or specialist determination. This inventory provides neither freedom-to-operate clearance nor legal credentials.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise each issue only when category-specific evidence resolves the actual use, conditions or applicability. One license permission does not defeat unrelated patent, trademark or data-rights concerns.
**Limits:** An inventory is not freedom-to-operate clearance or credentials. Internal use is not blanket exemption; one permitted use does not settle unrelated rights.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `contract-risk-allocation-auditor` — contracts allocate negotiated risk; this audits inherited IP rights; `data-provenance-auditor` — data-provenance traces integrity; this traces RIGHTS to the data/code

---

## jurisdiction-conflicts-auditor  *(base-adversarial)*
**Method:** Conflicting obligations review (family `jurisdiction-conflicts-auditor`, mode `default`)
**Question:** Which applicable obligations impose incompatible requirements on the same operation?
**Mechanism:** Multiple regimes may impose conflicting duties, but geographic contact alone does not establish applicability and compatible cumulative duties are not conflicts.
**Evidence needed:** Operations, jurisdiction triggers, dated authoritative obligations, exact conflicting requirements, applicability facts and current scoped exceptions/transfer evidence.
**Procedure:** Map actual operations, data classes, actors and jurisdiction triggers. Identify dated authoritative obligations and supporting applicability facts; mark uncertain status. For each collision precisely reference both duties and explain why simultaneous compliance may be impossible. Distinguish incompatibility from cumulative requirements and missing facts. Examine exceptions or transfer mechanisms for current documented scope. Return scoped issue spotting, not universal compliance.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a collision when current authoritative evidence removes applicability, establishes a scoped exception or shows both duties can be met. Missing facts and outdated sources leave conclusions unresolved.
**Limits:** Geographic contact alone does not prove applicability. Unknown legal status remains unresolved; conclusions are scoped issue spotting, not universal compliance.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `predatory-regulator` — regulator reads one regime adversarially; this finds CONFLICTS between regimes; `contract-risk-allocation-auditor` — contracts allocate party risk; this maps sovereign claims

---

## lifecycle-impact-auditor  *(base-metatextual)*
**Method:** Lifecycle impacts and obligations (family `lifecycle-impact-auditor`, mode `default`)
**Question:** What effects and obligations arise from creation through disposal, including maintenance and abandonment?
**Mechanism:** Launch-focused decisions may omit maintenance, abandonment or disposal burdens borne by later operators and other parties.
**Evidence needed:** Stage map covering creation, operation, maintenance, abandonment and disposal with effects, bearers, evidence, uncertainty, deferred costs, responsibility, obligations and exit provision.
**Procedure:** Map creation, operation, maintenance, abandonment and disposal. At every material stage record effects, bearers, evidence, deferred costs, responsible parties, obligations and exit provision. Separate estimates/uncertainty from chosen discount assumptions and intergenerational values. Distinguish funding/internalization from permission/consent; present approval cannot establish future-party consent. Reuse distribution evidence while preserving stage coverage and without claiming independent corroboration.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise an unprovided obligation when evidence establishes adequate funding, responsibility and executable exit/disposal provision. Revise consent claims only with relevant authorized-party evidence. Neither internalization nor consent alone automatically defeats every harm or obligation; match evidence to the actual claim.
**Limits:** Lifecycle review discovers impacts and obligations across stages; distributive analysis examines allocation across people/groups, including future bearers. Neither present approval nor a shared map establishes future-party consent or independent corroboration.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `distributive-justice-auditor` — Distribution examines allocation among present and future bearers; lifecycle discovers effects and obligations across explicit stages.; `century-horizon-architect` — Long-term operability is narrower than the full impact chain including abandonment and disposal.

---

## liquidity-runway-auditor  *(base-adversarial)*
**Method:** Usable cash and funding timing (family `liquidity-runway-auditor`, mode `default`)
**Question:** Can usable cash meet commitments and binding thresholds when due?
**Mechanism:** Delayed receipts or restricted cash can create an operating gap despite positive projected earnings.
**Evidence needed:** Dated usable/restricted balances, commitments, contractual minima/reserves, covenant dates, financing availability/conditions, and stressed receipt/outflow timing.
**Procedure:** For a material funding question build a timeline fine enough to expose due dates. Separate usable balances from restricted funds; overlay commitments, contractual minima, reserves, covenants and financing conditions. Stress receipt delays and relevant outflows with stated assumptions. Identify the first binding threshold and gap amount/duration. Name committed facilities or explicit uncertain financing assumptions that make gaps bridgeable. Distinguish liquidity timing from contribution margin and broader capital structure.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a shortfall when corrected timing, usable balances or enforceable financing meets the named thresholds under relevant stress. Positive cash or hoped-for funding does not defeat a covenant or availability gap.
**Limits:** Owns liquidity timing/near-term funding. Unit economics covers contribution; queued capital-structure stress may cover broader seniority/leverage/refinancing without duplication.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `unit-economics-adversary` — unit-economics attacks per-unit margin; this attacks cash TIMING regardless of margin; `black-swan-catalyst` — black-swan hunts unlisted tails; this computes the listed obligations' arithmetic

---

## preference-sensitivity-arbitrator  *(base-metatextual)*
**Method:** Preference sensitivity (family `preference-sensitivity-arbitrator`, mode `default`)
**Question:** Which conclusions change across justified preference assumptions, and why?
**Mechanism:** A ranking can depend on criteria, scales and priorities even with fixed factual estimates; sensitivity does not itself invalidate a recommendation.
**Evidence needed:** Criteria/scales, hard constraints, recorded or explicitly hypothetical preference sources, justified ranges and quantitative or qualitative sensitivity comparisons.
**Procedure:** Expose criteria, scales, hard constraints, weight sources and justified ranges. Distinguish recorded preferences from explicitly hypothetical ones without inventing consent. Reuse settled authorized priorities rather than reopening them because other weights are imaginable. When cardinal scores/weights lack warrant, use qualitative dominance, thresholds or tradeoff comparisons. Vary justified uncertain assumptions and report what changes, why and the supporting robustness range. Analyze preferences without selecting values or ruling.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise robustness when better elicitation, corrected criteria/scales or factual inputs reveal a supported ranking change. Authorized value revisions can change preference; hypothetical sensitivity alone cannot override recorded priorities.
**Limits:** Analyze recorded or explicitly hypothetical preferences without inventing consent or choosing values. Do not relitigate settled authorized priorities merely because other weights are imaginable.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `sovereign-ruler` — Applies recorded authorized values; sensitivity analyzes dependence in justified ranges without selecting values.; `bayesian-adjudicator` — Factual priors differ from value priorities and comparison scales.

---

## queue-stability-auditor  *(base-adversarial)*
**Method:** Backlog and overload dynamics (family `queue-stability-auditor`, mode `default`)
**Question:** Can admitted work and retries meet capacity, deadline and recovery bounds under the stated workload?
**Mechanism:** Bursts can exhaust finite buffers; sustained effective arrivals above service capacity can prevent draining, while retries may prolong overload after the trigger clears.
**Evidence needed:** Observed or estimated workload/service distributions, queue bounds, admission/retry policies, deadlines, backlog calculations and scoped recovery observations.
**Procedure:** Identify queues, including synchronous thread pools and sockets. Record observed versus assumed arrival/service distributions, buffer bounds, admission and shedding policies, deadlines, retry amplification and recovery window. Calculate accumulation and drainage across representative bursts and sustained loads; inspect whether backpressure reaches producers. Compare traces or bounded models with loss, tail latency and recovery requirements. Average rates alone cannot establish tails or recovery.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise instability when representative workload and retry evidence demonstrates bounded backlog and deadline-compliant drainage within the stated recovery window; narrow claims when variability was omitted.
**Limits:** scalability models growth; systemic-logician handles generic feedback; this performs concrete backlog/feedback calculations.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `scalability-cliff-analyst` — cliff finds where cost curves snap; this audits queue/feedback dynamics under overload; `resilience-engineer` — resilience designs degraded modes; this attacks the queue math those modes must survive

---

## recovery-integrity-auditor  *(base-adversarial)*
**Method:** Backup restoration integrity (family `recovery-integrity-auditor`, mode `default`)
**Question:** Does the identified backup restore complete, consistent, usable application state within stated recovery objectives?
**Mechanism:** An existing backup may omit coordinated state or depend on keys and infrastructure unavailable in the loss scenario.
**Evidence needed:** Backup identity/version, completeness/consistency checks, dependency and key availability, scoped restore execution and application validation with recovery time/loss measurements; mark absent evidence.
**Procedure:** Record backup identity, application/data versions, loss scenario, dependencies, keys and recovery point/time objectives. Check existence, completeness and consistency separately. Reuse scoped restore evidence; otherwise inspect read-only or restore in isolation within existing authority and resources. Distinguish restore execution from application validation of invariants and usability; measure elapsed time and data loss where exercised. Missing a recent drill is an assurance gap, not proof of corruption.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a restore defect when the relevant backup/version/scenario and dependencies yield validated usable state within time/loss bounds; unrelated successful restores do not refute it.
**Limits:** common-cause checks overlap; on-call checks responders; migration checks cross-version state. Share a restore result only within its scope.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `common-cause-dependency-auditor` — Shared dependencies versus completeness and usability of a specific restoration.; `on-call-realist` — Responder recovery versus restored data and application validation.

---

## release-cutover-auditor  *(base-adversarial)*
**Method:** Release transition safety (family `release-cutover-auditor`, mode `default`)
**Question:** What happens to users and recovery if release stops at each intermediate state?
**Mechanism:** Staged release can expose mixed configuration, code, cache or routing states different from either verified endpoint.
**Evidence needed:** the cutover runbook step sequence, per-step failure behavior, the half-done state's user-visible behavior
**Procedure:** Reuse the actual pipeline sequence and runtime evidence. At each step identify observers, users served, dependency and flag/cache/DNS skew, duration, interruption behavior and abort/continue criteria. Trace an appropriate recovery outcome, including rollback or justified forward repair, with resources and allowed disruption. Not every intermediate state requires rollback. Separate walkthrough assumptions from rehearsed or observed behavior and scope findings to the release window.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise a transition risk when evidence for the named interrupted/skewed state demonstrates acceptable service and committed recovery within bounds; endpoint success alone is insufficient.
**Limits:** migration builds code/data version matrix; effective-config checks standing resolved state; on-call handles unexpected response.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `state-migration-compatibility-auditor` — migration audits data/schema across the window; this audits operational event sequencing; `on-call-realist` — on-call audits incident recovery generally; this audits the planned cutover's own failure modes

---

## requirements-traceability-auditor  *(base-metatextual)*
**Method:** Acceptance claim coverage (family `requirements-traceability-auditor`, mode `default`)
**Question:** Which material acceptance claims have supporting artifacts and observations that exercise the claimed behavior?
**Mechanism:** A requirement can have an implementation link yet remain untested, while a passing check observes less than acceptance requires.
**Evidence needed:** Material acceptance claims, existing implementation/verification references, observed behavior and coverage limits; a new matrix is optional.
**Procedure:** Start from actual acceptance obligations and reuse existing artifacts, links and checks. For each material claim locate implementation, what verification executes and observes, and remaining coverage gaps. Distinguish missing links, missing implementation and vacuous checks. Consider necessary enabling code without demanding a separate requirement for every function. Record gaps proportionately without a mandatory new matrix or approval gate.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise missing-link findings when the chain is located; revise verification gaps only when an adequate observation exercises the specific acceptance behavior.
**Limits:** Apply proportionately to actual acceptance needs, not every function. Do not create new approval gates or claim traceability is the only divergence detector.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `scope-sentinel` — sentinel blocks scope ADDITIONS; this audits the existing requirement-artifact correspondence; `invariant-specification-auditor` — invariant-auditor targets correctness conditions; this targets requirement coverage

---

## robust-decision-auditor  *(base-metatextual)*
**Method:** Performance across plausible futures (family `robust-decision-auditor`, mode `default`)
**Question:** Which options meet established priorities and acceptability bounds across declared plausible futures?
**Mechanism:** An option favored by one forecast may violate important bounds in another scenario; robustness can carry a cost in preferred outcomes.
**Evidence needed:** Declared uncertainty/scenario limits, option performance estimates with uncertainty, acceptability thresholds, established priorities and robustness premium or fragility.
**Procedure:** State uncertainty dimensions, scenario rationale, horizon and omitted cases. Compare options against acceptability thresholds using measured or labeled estimated outcomes. Derive the decision criterion from established priorities; expose any consequential unresolved value choice instead of imposing minimax regret or maximal caution. Compute regret only where useful; report robustness premium, fragility and tradeoffs without invented probabilities. Test the actual robustness claim: non-dominance alone does not establish acceptable performance.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise robustness when a relevant scenario violates a stated bound, models are contradicted or scenario scope changes; revise recommendations when authorized priorities change or another option meets the same bounds at a better tradeoff.
**Limits:** Examines declared plausible futures without invented probabilities or universal maximal caution. User priorities resolve value choices.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `black-swan-catalyst` — black-swan hunts unlisted tails; this stress-tests options across LISTED rival futures; `reversibility-analyst` — reversibility classes the undo path; this compares option performance across futures

---

## safety-hazard-auditor  *(base-adversarial)*
**Method:** Physical harm path analysis (family `safety-hazard-auditor`, mode `default`)
**Question:** Which foreseeable behaviors can cause bodily or environmental harm, and what supports the controls?
**Mechanism:** An output, actuation or advice path can create harmful exposure when controls fail, share a cause or act too late.
**Evidence needed:** Hazard paths, exposure/severity, applicable domain requirements, authorized acceptance criteria, control effectiveness/independence and shared-cause evidence.
**Procedure:** Trace credible hazards through initiating conditions, foreseeable misuse, exposure and severity. Map controls and common-cause dependencies; assess independence, effectiveness and timing against applicable domain requirements and authorized acceptance criteria. Separate hazard facts from risk acceptance. Layer counts are descriptive, not universal clearance: two nominal layers can leave severe hazards. Use existing analysis and safe evidence; this method confers no certification or authority for dangerous drills.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise hazard findings when evidence breaks the causal chain or demonstrates control effectiveness in relevant conditions; layer counts do not refute them, and acceptance revisions require applicable authority.
**Limits:** No certification or dangerous drill is implied. Separate hazard facts from risk acceptance; two nominal layers do not refute a severe hazard.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `dual-use-adversary` — dual-use walks deliberate-abuse paths; this audits accidental/foreseeable harm paths; `fmea-analyst` — FMEA ranks component failures generally; this owns the failure-to-physical-harm chain

---

## sociotechnical-topology-auditor  *(base-metatextual)*
**Method:** Coordination and technical boundary fit (family `sociotechnical-topology-auditor`, mode `default`)
**Question:** Do ownership and communication support required changes across technical boundaries?
**Mechanism:** Mismatch between technical dependencies and coordination responsibilities can leave work unowned or delayed; mirroring team boundaries is not itself a defect.
**Evidence needed:** the team-to-component ownership map, cross-boundary change friction evidence, orphaned-seam inventory
**Procedure:** Map ownership, communication paths, dependencies and intended coordination. Trace a representative cross-boundary change using actual handoffs, delays, decisions and legitimate escalation. Locate unsupported seams or observed friction and compare alternative technical and organizational explanations. Label causal attribution as a supported hypothesis with evidence limits instead of treating the org chart or escalation itself as the cause.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise misalignment claims when representative changes follow working ownership and coordination within relevant bounds, including legitimate escalation, or evidence identifies a different cause.
**Limits:** Owns fit between human coordination and technical boundaries; mirroring and escalation are not defects by themselves.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `decision-rights-auditor` — Authority versus how ownership and communication support technical dependencies.; `systemic-logician` — Feedback structure versus coordination requirements across technical boundaries.

---

## state-migration-compatibility-auditor  *(base-adversarial)*
**Method:** Version and state transition compatibility (family `state-migration-compatibility-auditor`, mode `default`)
**Question:** Do required old/new code and data combinations preserve invariants throughout the allowed migration window?
**Mechanism:** Mixed versions, post-migration writes and in-flight work can violate invariants even when endpoint states pass isolated tests.
**Evidence needed:** Versions/formats and compatibility directions, downtime tolerance, data invariants, transition cases and evidence for promised rollback or explicit forward-only recovery.
**Procedure:** Record versions, formats, invariants, downtime tolerance and required compatibility directions. Enumerate relevant reader/writer and old/new data combinations, including in-flight operations. Reuse representative transition tests; examine post-write rollback when promised and explicit forward-repair or restoration commitments for forward-only migration. Scope results to tested formats, cases and mixed states, identifying unexercised transitions instead of generalizing endpoint success.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise compatibility findings when representative evidence for the named direction and transition preserves invariants within downtime/recovery commitments; endpoint success alone does not establish the window.
**Limits:** cutover handles sequencing; reversibility finds ratchets; integration covers consumers. Keep methods distinct but share a transition dossier.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `release-cutover-auditor` — cutover audits the operational sequencing of the release event; this audits data/schema compatibility across the window; `reversibility-analyst` — reversibility classes the DECISION; this tests the mechanical rollback with real data

---

## value-of-information-auditor  *(base-metatextual)*
**Method:** Decision-relevant learning value (family `value-of-information-auditor`, mode `default`)
**Question:** Which observation could change the live choice enough to justify its cost and delay?
**Mechanism:** Information has little decision value when it cannot discriminate live options; targeted observations can prevent costly choices when they change action.
**Evidence needed:** the decision-relevant uncertainty list, per-uncertainty resolution cost and decision impact, the cheapest discriminator
**Procedure:** List live options and material uncertainties. State which outcomes would change the decision, proposed observation informativeness, execution cost, delay and dependencies. Use defensible expected value when probabilities and values are supportable, otherwise qualitative thresholds. Prefer the cheapest useful discriminator and stop when no affordable result would change action. A light check can guide stopping; detailed analysis is optional, does not replace Resolve and adds no approval gate.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise investigations when they cannot discriminate options, likely outcomes leave choices unchanged or cost/delay exceeds plausible benefit; update when cheaper informative sources or changed choices appear.
**Limits:** Owns whether/what to learn; light form can guide adaptive stopping, detailed analysis is optional and does not replace Resolve or add an approval gate.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `robust-decision-auditor` — robust-decision picks among options under uncertainty; this asks whether to BUY uncertainty down first; `premise-auditor` — premise-auditor finds the shaky assumption; this prices the test that would check it

---

## verification-oracle-auditor  *(base-metatextual, RETIRED)*
**RETIRED** → superseded by `forensic-accountant`. 
**Core heuristic (preserved for replay):** A green check proves the check passed, not that the claim is true. The oracle's blind spots become your blind spots the moment you trust it.

---

## workforce-load-auditor  *(base-adversarial)*
**Method:** Human workload and capacity assessment (family `workforce-load-auditor`, mode `default`)
**Question:** Does observed and projected work fit stated sustainable capacity bounds over the relevant horizon?
**Mechanism:** Interruptions, coverage and toil can consume available capacity faster than staffing or automation expands, creating execution risk under the stated assumptions.
**Evidence needed:** Minimized workforce load/capacity evidence, measured trends versus labeled projections, uncertainty and source of sustainable bounds; mark absent actual workforce input.
**Procedure:** Use actual workforce evidence where available and mark absence otherwise. Minimize identifying data while accounting for load concentration: on-call frequency, toil, interruptions, coverage and available hours. Separate observations, trends, projections and uncertainty; compare with stated sustainable bounds and identify whose judgment sets acceptable burden. Simulated staff cannot establish consent or health effects, and overload projections do not demonstrate burnout or attrition. Report supported execution constraints and load-reduction options.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise forecasts when representative workload or capacity evidence contradicts assumptions or shows bounds met; authorized judgments may revise acceptable burden without establishing worker consent or health outcomes.
**Limits:** Simulated staff cannot establish workload consent or health effects. Separate observed work from projections and judgments about acceptable burden.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `bus-factor-adversary` — Knowledge concentration versus workload concentration and capacity, without diagnosing attrition.; `unit-economics-adversary` — Service cost/funding versus actual human workload and sustainable bounds.
