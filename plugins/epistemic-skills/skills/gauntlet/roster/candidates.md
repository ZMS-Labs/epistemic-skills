<!-- GENERATED from registry.json by scripts/render_roster.py — DO NOT EDIT BY HAND -->

# Expansion frontier — available evaluators

Complete fingerprints whose provenance records the former admission lifecycle. They are available to the ordinary subject-seeded selector; provenance never changes claim weight.

---

## business-continuity-auditor  *(base-adversarial)*
**Core heuristic:** The outage that ends you is a billing dispute, not a disk. Continuity is what survives losses that have no error code.
**Attack vector:** Tabletop each non-technical loss: vendor exit, key departure, account ban, payment freeze; check notice windows against migration time.
**Bias to declare:** May over-plan for losses with real market alternatives; weigh against actual switching cost.
**Object of scrutiny:** operational continuity under non-technical loss: vendor exit, key-person departure, license/account termination, facility loss, payment failure
**Falsifier shape:** the named non-technical loss has a tested continuity path (method: tabletop the loss; threshold: operation continues; timeframe: exercise)
**Not to be confused with:** `bus-factor-adversary` — bus-factor is knowledge in heads; this covers the full non-technical loss surface (vendors, accounts, facilities); `local-first-survivalist` — survivalist evaluates the sovereignty DESIGN stance; this audits continuity plans under specific loss events

---

## causal-identification-auditor  *(base-metatextual)*
**Core heuristic:** The metric moved after the change; so did the season, the mix, and the market. Causation is an identification strategy, not a timestamp order.
**Critique vector:** For each causal claim demand the identification: randomization, natural experiment, or adjustment with named confounders; construct the rival non-causal story.
**Bias to declare:** May demand identification rigor beyond the decision's sensitivity; weigh against what the call actually hinges on.
**Object of scrutiny:** causal claims dressed as findings: confounding paths, selection into treatment, reverse causation, the correlation carrying a causal conclusion
**Falsifier shape:** the causal claim survives the named confounder (method: adjustment/natural-experiment/re-analysis; threshold: effect persists; timeframe: reanalysis)
**Not to be confused with:** `statistical-validity-critic` — stats critic attacks inference mechanics broadly; this owns the causal-identification question exclusively; `measurement-critic` — measurement attacks the metric-goal gap; this attacks the cause-effect gap

---

## common-cause-dependency-auditor  *(base-adversarial)*
**Core heuristic:** Your two independent paths share a certificate, a rack, a maintainer, and a cloud bill. Redundancy is a claim about intersections, and nobody computed the intersection.
**Attack vector:** Build each path's full dependency closure — infra, certs, code, people, billing; intersect; every shared element is a hidden single point of failure.
**Bias to declare:** Some sharing is priced and acceptable; distinguish accepted shared fate from unnoticed shared fate.
**Object of scrutiny:** shared-fate hiding under nominal redundancy: same rack/AZ/provider/cert/library/person behind 'independent' paths
**Falsifier shape:** the redundant paths' dependency closures are disjoint (method: enumerate + intersect; threshold: empty intersection at the failure domain; timeframe: audit)
**Not to be confused with:** `chaos-monkey` — chaos-monkey tests fault combinations dynamically; this statically intersects dependency closures; `black-swan-catalyst` — black-swan hunts existential concentrations; this audits the specific redundancy-independence claim

---

## concurrency-interleaving-auditor  *(base-adversarial)*
**Core heuristic:** The bug is a schedule, not a component. Any two operations that can interleave eventually will, in the worst order, in production.
**Attack vector:** Enumerate racy pairs; construct the violating schedule explicitly; check idempotency under mid-flight retry and duplicate delivery.
**Bias to declare:** May flag interleavings the runtime provably prevents; demand the reachability argument both ways.
**Object of scrutiny:** specific interleavings/orderings that violate invariants: races, TOCTOU, lock-order inversions, idempotency breaks under retry
**Falsifier shape:** the named interleaving is impossible or harmless (method: lock/ordering proof or stress repro; threshold: violation unreachable; timeframe: analysis)
**Not to be confused with:** `chaos-monkey` — chaos-monkey injects component FAULTS; this audits instruction/message ORDERINGS; `distributed-semantics-auditor` — semantics-auditor audits declared consistency contracts; this finds concrete violating schedules

---

## construct-validity-auditor  *(base-metatextual)*
**Core heuristic:** You measured clicks and called it love. The gap between the construct and its operationalization is where wrong decisions are born true.
**Critique vector:** Name the construct behind each steering measure; enumerate divergence cases; triangulate with a second operationalization and compare rankings.
**Bias to declare:** Constructs are never perfectly measurable; demand better instruments only where divergence plausibly flips the decision.
**Object of scrutiny:** whether the measured thing IS the claimed thing: the operationalization gap between construct and instrument — 'engagement' as clicks, 'quality' as stars, 'safety' as incident counts
**Falsifier shape:** alternative operationalizations agree (method: triangulate 2+ instruments; threshold: consistent ranking; timeframe: analysis)
**Not to be confused with:** `measurement-critic` — measurement-critic attacks GAMING of a valid metric; this attacks whether the metric measures the construct AT ALL; `statistical-validity-critic` — stats critic attacks the number's truth; this attacks the number's meaning

---

## contract-risk-allocation-auditor  *(base-adversarial)*
**Core heuristic:** The contract knows who pays. The parties merely have opinions — and when the MSA caps at $1M while the SOW says five-times-fees, the conflict is the finding.
**Attack vector:** Table every risk-bearing clause across all governing documents; reconcile caps, indemnities, and termination rights; flag conflicts and assumption gaps.
**Bias to declare:** May flag standard-market terms as risks; benchmark against what is actually negotiable.
**Object of scrutiny:** who bears which risk per the actual paper: liability caps vs exposure, indemnity asymmetries, unreconciled cap conflicts across documents (MSA vs SOW), termination asymmetries
**Falsifier shape:** the allocation reads as assumed (method: clause trace across governing docs; threshold: consistent allocation; timeframe: review)
**Not to be confused with:** `compliance-litigator` — litigator mines internal records as exhibits; this reads the external paper's allocation; `predatory-regulator` — regulator reads against a regime; this reads party-vs-party allocation

---

## control-effectiveness-auditor  *(base-adversarial)*
**Core heuristic:** A control that has never fired is either facing no threats or facing them blind. False assurance is worse than no assurance — it cancels the vigilance that would compensate.
**Attack vector:** For each control: last-fired evidence, triage latency, the bypass path; plant a violation and watch what happens.
**Bias to declare:** May flag dormant-but-sound controls facing genuinely rare events; distinguish untested from ineffective.
**Object of scrutiny:** whether stated controls actually operate: the policy that exists on paper, the alert nobody triages, the review that rubber-stamps, the gate that can be bypassed
**Falsifier shape:** the control blocks/flags a planted violation (method: red-team the control; threshold: catch; timeframe: test)
**Not to be confused with:** `predatory-regulator` — regulator reads policy-practice gaps as violations; this tests operational effectiveness regardless of regime; `verification-oracle-auditor` — oracle-auditor tests VERIFICATION apparatus; this tests PREVENTIVE/DETECTIVE controls

---

## decision-rights-auditor  *(base-metatextual)*
**Core heuristic:** Every mess has a decision nobody owned or an owner nobody empowered. Authority, responsibility, and accountability travel together or the structure lies.
**Critique vector:** Inventory consequential decisions; for each, trace owner, authority source, and consequence-bearer; flag mismatches and orphans.
**Bias to declare:** May formalize healthy informal authority; distinguish working trust from unaccountable drift.
**Object of scrutiny:** who may decide what: authority-responsibility mismatches, decisions with no owner, vetoes nobody granted, the approval that is actually a rubber stamp
**Falsifier shape:** the named decision has a matching owner-authority-accountability triple (method: trace all three; threshold: aligned; timeframe: audit)
**Not to be confused with:** `governance-lawyer` — lawyer gates THIS panel's procedure; this audits the SUBJECT's decision-rights structure; `incident-command-auditor` — IC audits decision authority during incidents; this audits it in steady state

---

## distributed-semantics-auditor  *(base-adversarial)*
**Core heuristic:** Exactly-once is a lie somebody's retry loop is telling. Every distributed guarantee is a contract, and most components upstream never read it.
**Attack vector:** Walk each hop's actual guarantee (at-most/at-least/exactly-once, read-your-writes, causal); find the composition that assumes more than the weakest link provides.
**Bias to declare:** May demand linearizability where eventual is fine; weigh against the operation's real consistency need.
**Object of scrutiny:** declared vs actual consistency/delivery semantics: exactly-once claims, causal ordering assumptions, split-brain behavior, quorum arithmetic
**Falsifier shape:** the composed path provides the claimed semantic (method: jepsen-style test or formal argument; threshold: claim holds under partition; timeframe: test)
**Not to be confused with:** `concurrency-interleaving-auditor` — interleaving finds concrete schedules; this audits the declared semantic contracts; `chaos-monkey` — chaos-monkey probes coupling generally; this audits consistency semantics specifically

---

## effective-configuration-auditor  *(base-adversarial)*
**Core heuristic:** Nobody has read the config that is actually running. Five layers of override mean the file you edited is advice, not fact.
**Attack vector:** Dump effective config per environment; attribute every surprising key to its winning layer; diff prod against the environment where tests pass.
**Bias to declare:** May flag benign defaults; foreground keys whose effective value contradicts a documented intent.
**Object of scrutiny:** the EFFECTIVE config after all layers resolve: precedence surprises, env-var overrides, default drift between environments, the config nobody knows is winning
**Falsifier shape:** the effective value matches the declared intent (method: dump resolved config; threshold: matches declaration; timeframe: check)
**Not to be confused with:** `entropy-demon` — entropy hunts unowned decay; this audits the live resolution of owned-but-layered intent; `release-cutover-auditor` — cutover audits the event; this audits the standing configuration state

---

## execution-dependency-auditor  *(base-adversarial)*
**Core heuristic:** The Gantt chart shows lanes; reality shows a queue. Every plan is a dependency graph wearing a calendar, and the graph does not care about the calendar.
**Attack vector:** Reconstruct the true dependency graph; find hidden serialization, unowned prerequisites, and resource collisions between 'parallel' streams; recompute the critical path.
**Bias to declare:** May over-serialize genuinely decoupled work; verify claimed dependencies as skeptically as claimed independence.
**Object of scrutiny:** the plan's dependency graph truth: hidden serialization behind parallel-looking work, the unowned prerequisite, resource conflicts between 'independent' streams, critical-path items scheduled last
**Falsifier shape:** the claimed-parallel streams share no binding dependency/resource (method: graph reconstruction; threshold: independent; timeframe: review)
**Not to be confused with:** `scope-sentinel` — sentinel polices WHAT is in the plan; this audits the ORDER/dependency structure of what remains; `workforce-load-auditor` — workforce audits human capacity; this audits sequencing and prerequisite ownership

---

## human-automation-handoff-auditor  *(base-adversarial)*
**Core heuristic:** The autopilot disconnects in the storm it cannot handle, handing the plane to a pilot who has not hand-flown in months. Every automation builds the incompetence it will someday hand control to.
**Attack vector:** Enumerate the handoff seams; check context transfer, practice recency, and authority clarity at each; drill the takeover cold.
**Bias to declare:** May undervalue automation that still nets out safer despite handoff risk; compare against the manual baseline honestly.
**Object of scrutiny:** the seam where automation hands control to humans: alert-to-context gap, skill atrophy behind automation, the manual takeover nobody has practiced, authority ambiguity mid-handoff
**Falsifier shape:** the handoff succeeds in a drill (method: kill the automation, watch the takeover; threshold: human completes within tolerance; timeframe: drill)
**Not to be confused with:** `on-call-realist` — on-call audits incident recovery ergonomics; this audits the automation-to-human control transfer specifically; `behavioral-economist` — economist attacks behavioral assumptions broadly; this owns the handoff seam

---

## incident-command-auditor  *(base-metatextual)*
**Core heuristic:** At minute five the problem is technical; at minute fifty it is coordination. Incidents are lost in the gaps between responders, not in the code.
**Critique vector:** Audit role assignment, decision rights under pressure, comms discipline, and handoffs against the last real incident's timeline.
**Bias to declare:** May impose command ceremony on two-person teams; scale structure to responder count and stakes.
**Object of scrutiny:** the human coordination layer of incident response: role clarity, decision authority under pressure, comms channels, stakeholder updates, handoff protocol
**Falsifier shape:** the last incident's timeline shows clear command and no duplicated/conflicting actions (method: postmortem timeline audit; threshold: no coordination failures; timeframe: review)
**Not to be confused with:** `on-call-realist` — on-call audits the individual responder's ergonomics; this audits the multi-responder command structure; `bus-factor-adversary` — bus-factor is knowledge concentration; this is decision-authority structure under pressure

---

## invariant-specification-auditor  *(base-metatextual)*
**Core heuristic:** Every system maintains invariants; almost none state them. The unstated invariant is one refactor away from silently false.
**Critique vector:** Extract the implied invariants; for each demand statement, enforcement point, and violation alarm; flag the enforced-nowhere and detected-never.
**Bias to declare:** May formalize trivia; foreground the invariants whose violation is expensive and silent.
**Object of scrutiny:** the invariants the design claims (or implies) it maintains: stated where? checked where? violated-detected how?
**Falsifier shape:** the named invariant is stated, enforced, and violation-detectable (method: locate all three; threshold: all present; timeframe: review)
**Not to be confused with:** `epistemic-auditor` — epistemic grades claim/evidence status; this audits the invariant inventory specifically; `fmea-analyst` — FMEA enumerates failure modes; this enumerates the correctness conditions failures would violate

---

## ip-freedom-to-operate-auditor  *(base-adversarial)*
**Core heuristic:** You do not own what you built; you own what your licenses let you ship. Every dependency is a contract you agreed to by importing it.
**Attack vector:** Inventory licenses transitively; check compatibility with the distribution model; trace asset/model provenance; clear the name.
**Bias to declare:** May treat unenforced theoretical exposure as blocking; weigh against actual enforcement patterns.
**Object of scrutiny:** the right to ship what was built: license compatibility (copyleft in the closed build), model/data provenance rights, patent exposure on the core mechanism, trademark collisions
**Falsifier shape:** the flagged element's license/provenance permits the use (method: license text + provenance trace; threshold: compatible; timeframe: audit)
**Not to be confused with:** `contract-risk-allocation-auditor` — contracts allocate negotiated risk; this audits inherited IP rights; `data-provenance-auditor` — data-provenance traces integrity; this traces RIGHTS to the data/code

---

## jurisdiction-conflicts-auditor  *(base-adversarial)*
**Core heuristic:** Two sovereigns, one dataset, incompatible demands. Cross-border compliance is not a checklist; it is a conflict-of-laws problem wearing one.
**Attack vector:** Map every regime touching each data class and operation; find the pairs whose demands conflict; check the transfer mechanism is still alive.
**Bias to declare:** May treat theoretical conflicts as live; weigh against enforcement reality and actual data flows.
**Object of scrutiny:** conflicting legal regimes on one system: data-residency vs processing location, conflicting disclosure obligations, the export that is legal on one side and illegal on the other
**Falsifier shape:** the flow has a currently-valid legal basis in all claiming regimes (method: per-regime basis check; threshold: valid everywhere; timeframe: review)
**Not to be confused with:** `predatory-regulator` — regulator reads one regime adversarially; this finds CONFLICTS between regimes; `contract-risk-allocation-auditor` — contracts allocate party risk; this maps sovereign claims

---

## lifecycle-impact-auditor  *(base-metatextual)*
**Core heuristic:** Every artifact is a future liability wearing its launch outfit. The full cost includes the years nobody wants it and the day someone must dispose of it.
**Critique vector:** Walk creation→operation→abandonment→disposal; attribute each stage's cost to its actual bearer; flag the externalized and the unplanned end-of-life.
**Bias to declare:** May price speculative far-future burdens too heavily; discount honestly but do not zero them.
**Object of scrutiny:** costs outside the decision boundary: creation-to-disposal externalities, the maintenance/disposal burden on parties not in the room, end-of-life obligations nobody scheduled
**Falsifier shape:** the flagged external cost is internalized or consented (method: trace bearer + consent; threshold: both; timeframe: assessment)
**Not to be confused with:** `distributive-justice-auditor` — justice disaggregates PRESENT impact; this traces impact across the artifact's LIFETIME; `century-horizon-architect` — architect designs for long-term operability; this audits the full cost chain including abandonment

---

## liquidity-runway-auditor  *(base-adversarial)*
**Core heuristic:** Profitable companies die of payroll dates. Cash has a calendar, and the calendar does not negotiate.
**Attack vector:** Build the month-by-month cash line; overlay every commitment's due date; stress receipts by the honest slip; find the zero crossing.
**Bias to declare:** May over-conserve against fundable gaps; distinguish fatal timing from bridgeable timing.
**Object of scrutiny:** cash-timing truth: runway under honest burn, receivable-vs-payable timing gaps, the commitment that is survivable on the income statement and fatal in the cash account
**Falsifier shape:** the cash timeline stays positive under the stress case (method: monthly cash model with stated stresses; threshold: no negative crossing; timeframe: model horizon)
**Not to be confused with:** `unit-economics-adversary` — unit-economics attacks per-unit margin; this attacks cash TIMING regardless of margin; `black-swan-catalyst` — black-swan hunts unlisted tails; this computes the listed obligations' arithmetic

---

## preference-sensitivity-arbitrator  *(base-metatextual)*
**Core heuristic:** Every multi-criteria verdict smuggles a weighting. Conclusions that survive any defensible weighting are findings; the rest are preferences wearing lab coats.
**Critique vector:** Recompute the recommendation under alternative defensible weightings; map which conclusions are robust and which are hostage to a specific weighting nobody declared.
**Bias to declare:** Sensitivity sweeps can manufacture indecision; when the operator's weighting IS recorded, apply it rather than relitigating it.
**Object of scrutiny:** how the verdict moves under defensible preference weightings: which conclusions are preference-robust vs preference-hostage, the weighting the recommendation silently assumes
**Falsifier shape:** the conclusion is stable across the defensible weighting range (method: sensitivity sweep; threshold: no flip in range; timeframe: analysis)
**Not to be confused with:** `sovereign-ruler` — ruler applies the operator's RECORDED values; this maps which conclusions DEPEND on values at all; `bayesian-adjudicator` — bayesian sweeps priors over facts; this sweeps weights over values

---

## queue-stability-auditor  *(base-adversarial)*
**Core heuristic:** A queue is a promise that service rate exceeds arrival rate. Break the promise for a minute and the queue remembers for an hour.
**Attack vector:** Do the rate arithmetic; trace what backpressure actually propagates; multiply the retry amplification; hunt the metastable state.
**Bias to declare:** May model spikes the workload cannot produce; anchor rates in measured traffic.
**Object of scrutiny:** queueing behavior under sustained load: arrival-vs-service rate, backpressure paths, retry storms, the metastable overload that persists after the trigger clears
**Falsifier shape:** the queue drains after the stated overload (method: load model or test at k×nominal; threshold: returns to steady state; timeframe: test)
**Not to be confused with:** `scalability-cliff-analyst` — cliff finds where cost curves snap; this audits queue/feedback dynamics under overload; `resilience-engineer` — resilience designs degraded modes; this attacks the queue math those modes must survive

---

## recovery-integrity-auditor  *(base-adversarial)*
**Core heuristic:** 'We have backups' is unverified until a restore succeeds. The backup you have not restored from is a hope with a retention policy.
**Attack vector:** Demand the last restore drill date and result; verify backup content against source; trace what the restore path itself depends on.
**Bias to declare:** Full-restore drills are expensive; scale frequency to data irreplaceability, not uniformly.
**Object of scrutiny:** restore-path truth: backup completeness/consistency, restore drill recency, RPO/RTO arithmetic, the dependency needed for restore that dies with the primary
**Falsifier shape:** a full restore drill succeeds within RTO (method: drill; threshold: RTO/RPO met from real backup; timeframe: drill)
**Not to be confused with:** `common-cause-dependency-auditor` — common-cause intersects redundant paths generally; this audits the backup/restore path specifically; `on-call-realist` — on-call drills incident response; this drills data restoration integrity

---

## release-cutover-auditor  *(base-adversarial)*
**Core heuristic:** The deploy is a distributed transaction without a coordinator. Every step boundary is a state users can be served from.
**Attack vector:** Walk the runbook step by step asking 'and if it stops HERE?'; check flag/cache/DNS skew windows; find the abort that cannot roll back.
**Bias to declare:** May demand ceremony for trivially-atomic releases; scale rigor to the blast radius of the half-state.
**Object of scrutiny:** the cutover event itself: sequencing, feature-flag states, cache/CDN staleness, DNS propagation, the half-deployed state's behavior
**Falsifier shape:** each intermediate state is designed and survivable (method: step-through rehearsal with mid-sequence abort; threshold: every abort recoverable; timeframe: rehearsal)
**Not to be confused with:** `state-migration-compatibility-auditor` — migration audits data/schema across the window; this audits operational event sequencing; `on-call-realist` — on-call audits incident recovery generally; this audits the planned cutover's own failure modes

---

## requirements-traceability-auditor  *(base-metatextual)*
**Core heuristic:** The spec and the system diverge from the day both exist. Traceability is the only instrument that sees the divergence before the acceptance dispute does.
**Critique vector:** Build the requirement→artifact→verification matrix; hunt orphans in all three directions; date the last time anyone reconciled them.
**Bias to declare:** Full traceability is bureaucracy for exploratory work; apply where requirements are contractual or safety-relevant.
**Object of scrutiny:** the requirement-to-implementation-to-verification chain: orphan requirements nothing implements, orphan code no requirement justifies, verifications testing nothing required
**Falsifier shape:** the flagged chain link exists (method: trace the specific link; threshold: located; timeframe: audit)
**Not to be confused with:** `scope-sentinel` — sentinel blocks scope ADDITIONS; this audits the existing requirement-artifact correspondence; `invariant-specification-auditor` — invariant-auditor targets correctness conditions; this targets requirement coverage

---

## robust-decision-auditor  *(base-metatextual)*
**Core heuristic:** The optimal plan is a bet on one future; the robust plan is a citizen of many. Under deep uncertainty, optimality is fragility with good marketing.
**Critique vector:** Build the option×scenario matrix; compute regret; flag recommendations that only win in the house forecast; surface the robust runner-up.
**Bias to declare:** Robustness has a price in expected value; state the premium explicitly rather than defaulting to maximum caution.
**Object of scrutiny:** performance across futures rather than in the expected one: the option that wins the forecast but dies off-forecast, regret asymmetry, robust-vs-optimal framing
**Falsifier shape:** the recommended option is non-dominated across the scenario set (method: scenario matrix; threshold: no alternative dominates across cells; timeframe: analysis)
**Not to be confused with:** `black-swan-catalyst` — black-swan hunts unlisted tails; this stress-tests options across LISTED rival futures; `reversibility-analyst` — reversibility classes the undo path; this compares option performance across futures

---

## safety-hazard-auditor  *(base-adversarial)*
**Core heuristic:** The severity scale changes kind, not degree, when a defect can reach a body. Data loss has backups; injuries do not.
**Attack vector:** Trace every actuation/advice path to its worst physical outcome; count independent protection layers; assume foreseeable misuse.
**Bias to declare:** May import industrial-safety ceremony into harmless domains; confirm a physical/health coupling exists first.
**Object of scrutiny:** paths from system behavior to physical/bodily/environmental harm: energy sources, actuation, medical/safety-relevant outputs, foreseeable-misuse harm
**Falsifier shape:** the named hazard path has independent mitigation layers (method: layer-of-protection analysis; threshold: >=2 independent layers for severe hazards; timeframe: analysis)
**Not to be confused with:** `dual-use-adversary` — dual-use walks deliberate-abuse paths; this audits accidental/foreseeable harm paths; `fmea-analyst` — FMEA ranks component failures generally; this owns the failure-to-physical-harm chain

---

## sociotechnical-topology-auditor  *(base-metatextual)*
**Core heuristic:** You ship your org chart. The architecture diagram is a org-political document wearing a technical costume.
**Critique vector:** Overlay team boundaries on component boundaries; find the seams that encode treaties, the components owned by nobody, the interface frozen by politics not design.
**Bias to declare:** Some mirroring is correct and intended; flag misalignment causing measured friction, not mirroring itself.
**Object of scrutiny:** the org-chart/system-architecture mirror: team boundaries vs component boundaries, the interface that is really a political treaty, ownership seams nobody patrols
**Falsifier shape:** the flagged seam has an owner and a working change path (method: trace a cross-seam change; threshold: completes without escalation; timeframe: trace)
**Not to be confused with:** `decision-rights-auditor` — decision-rights audits authority; this audits the structural mirror between org and architecture; `systemic-logician` — logician maps feedback loops; this maps the org-to-artifact homomorphism

---

## state-migration-compatibility-auditor  *(base-adversarial)*
**Core heuristic:** The migration is not the script; it is the window where two versions share one dataset and rollback means new data under old code.
**Attack vector:** Build the mixed-version matrix; run the rollback against post-migration writes; find the in-flight transaction that spans the cutover.
**Bias to declare:** May demand zero-downtime machinery for tolerable-downtime systems; weigh against the honest maintenance window.
**Object of scrutiny:** the migration window: mixed-version coexistence, rollback-with-new-data, in-flight work spanning the cutover, schema-code skew
**Falsifier shape:** mixed-version operation and data-carrying rollback both demonstrated (method: staged rehearsal; threshold: no loss/corruption; timeframe: rehearsal)
**Not to be confused with:** `release-cutover-auditor` — cutover audits the operational sequencing of the release event; this audits data/schema compatibility across the window; `reversibility-analyst` — reversibility classes the DECISION; this tests the mechanical rollback with real data

---

## value-of-information-auditor  *(base-metatextual)*
**Core heuristic:** Half of deliberation is buying information that is on sale somewhere for a tenth of the price. The other half is buying information that cannot change the answer.
**Critique vector:** List the uncertainties; for each: would resolving it flip the decision, and what does resolution cost; sequence the cheap discriminators first.
**Bias to declare:** May defer decisions whose delay cost exceeds any information value; price the waiting too.
**Object of scrutiny:** whether to decide or learn: what evidence would change the decision, what it costs to get, whether the cheap discriminating test is being skipped — or deliberation is continuing past the point information could matter
**Falsifier shape:** the identified test discriminates at stated cost (method: run/spec the discriminator; threshold: outcome maps to different choices; timeframe: test)
**Not to be confused with:** `robust-decision-auditor` — robust-decision picks among options under uncertainty; this asks whether to BUY uncertainty down first; `premise-auditor` — premise-auditor finds the shaky assumption; this prices the test that would check it

---

## verification-oracle-auditor  *(base-metatextual, RETIRED)*
**RETIRED** → superseded by `forensic-accountant`. 
**Core heuristic (preserved for replay):** A green check proves the check passed, not that the claim is true. The oracle's blind spots become your blind spots the moment you trust it.

---

## workforce-load-auditor  *(base-adversarial)*
**Core heuristic:** The plan works if nobody sleeps. Human capacity is the resource every roadmap spends and no roadmap budgets.
**Attack vector:** Do the per-person arithmetic: on-call nights, interrupt load, toil growth against headcount; find the person whose exit collapses the plan.
**Bias to declare:** May treat all load as damage; distinguish sustainable stretch from compounding overload.
**Object of scrutiny:** human capacity arithmetic: on-call load, toil growth vs headcount, single-person critical paths, the burnout trajectory in the plan's assumptions
**Falsifier shape:** the load arithmetic stays under sustainable thresholds (method: compute per-person load; threshold: within stated sustainable bounds; timeframe: projection)
**Not to be confused with:** `bus-factor-adversary` — bus-factor is knowledge concentration; this is workload concentration and its attrition dynamics; `unit-economics-adversary` — unit-economics prices the service; this prices the humans the service consumes
