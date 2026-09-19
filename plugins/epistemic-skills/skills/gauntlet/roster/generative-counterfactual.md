<!-- GENERATED from registry.json by scripts/render_roster.py — DO NOT EDIT BY HAND -->

# Roster Group E — Generative & Counterfactual (pre-panel option generators + alternative-surfacing evaluators)

Generative methods propose alternatives or syntheses for scrutiny. In an open-question Gauntlet the initial phase uses `option-set@1`, including a fair status-quo option; focused use may return a bounded candidate. Generation never supplies evaluator diversity.

---

## adjacent-possible-explorer  *(base-generative, generate_options)*
**Method:** Nearby alternatives (family `adjacent-possible-explorer`, mode `default`)
**Question:** Which feasible nearby alternative better serves the accepted outcome, if any?
**Mechanism:** Recombining available capabilities can change costs or value without a full redesign; dominance is an empirical comparison, not a premise.
**Evidence needed:** capability inventory of what exists in-hand, cost/value estimate of the sideways variant vs the proposal
**Procedure:** Inventory available capabilities and retained requirements. Construct a nearby variant, identify its changed mechanism, assumptions and all-in costs, and compare it with the current proposal under the same criteria. Return the candidate and a discriminating observation; no better variant is a valid result.
**Possible results:** candidate, no-material-finding, uncertainty
**Revise when:** Revise or drop a variant if the like-for-like comparison removes its benefit, violates a retained requirement or reveals prohibitive transition cost.
**Limits:** Searches feasible local variants; does not verify their dominance or authorize expanded scope. Evaluation is a separate contribution, not necessarily a separate agent.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `opposite-steelman` — steelman advocates the explicitly-rejected branch; explorer searches the unexamined neighborhood; `first-principles-rederiver` — rederiver rebuilds from constraints ground-up; explorer perturbs the existing proposal locally

---

## analogical-historian  *(base-metatextual)*
**Method:** Historical comparison (family `analogical-historian`, mode `default`)
**Question:** Which documented precedents inform this decision, and where does the analogy fail?
**Mechanism:** Shared mechanisms can make precedents informative, while selection and decisive contextual differences can defeat transfer.
**Evidence needed:** the named precedent with its documented outcome, the force-by-force mapping showing the analogy is structural, the divergence risks
**Procedure:** Find sourced outcomes and a contrasting case where feasible. Map shared mechanisms and decisive differences. Report selection limits and the denominator or base rate when a defensible reference class exists. State transfer strength or no informative precedent.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Reduce or withdraw the analogy when source verification, contrasting outcomes or mechanism differences defeat the proposed transfer; do not infer a forecast probability from resemblance alone.
**Limits:** Historical analogy supports conditional comparison; it does not by itself establish causation, generalizability or a forecast probability.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `polymath-inquisitor` — Problem framing may use analogy to change the question; historical comparison checks documented outcomes and transfer limits.; `second-order-forecaster` — Downstream forecasting traces prospective mechanisms; historical comparison begins with sourced precedents.

---

## constraint-inverter  *(base-metatextual, RETIRED)*
**RETIRED** → superseded by `constraint-negotiator`. Merged 2026-07-10 with constraint-relaxer into constraint-negotiator: same mechanism from the critical direction; merged.
**Core heuristic (preserved for replay):** Every design optimizes *within* a fixed constraint set, but the biggest wins come from changing the constraints, not solving inside them. The question the proposal never asks is "what if the thing we are working around simply were not there?"

---

## constraint-negotiator  *(base-generative, generate_options)*
**Method:** Constraint change options (family `constraint-negotiator`, mode `default`)
**Question:** Which constraint could be changed with authority, and how do removal costs compare with accommodation costs?
**Mechanism:** An assumed or changeable constraint can impose avoidable complexity, while relaxing a binding obligation without authority can invalidate the option.
**Evidence needed:** Constraint inventory with sources, owners, hardness, change authority and evidence status; removal and retention cost ranges; feasibility and actual cost evidence before recommending change
**Procedure:** Inventory binding constraints with source, owner, hardness, change authority and evidence status. Distinguish physical constraints, obligations or values, resources and assumptions. Ask both what becomes possible if a constraint is relaxed and whether present accommodation costs exceed a feasible removal path. Compare cost ranges including transition and retained obligations. Label contingent relaxations hypothetical; require verified feasibility, actual cost evidence and appropriate authority before recommending a real change. Cheap removal does not make an obligation negotiable or silently reopen agreed scope.
**Possible results:** candidate, no-material-finding, uncertainty
**Revise when:** Revise an option when source verification makes its constraint binding, a feasible path fails, or all-in costs favor retention; revise a value or obligation constraint only through its authorized decision-maker.
**Limits:** May question source/cost, but only authorized decision-makers change real requirements. Can inform constructive revision without silently reopening scope.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `first-principles-rederiver` — rederiver derives within the TRUE constraint set; negotiator changes the SET itself; `adjacent-possible-explorer` — explorer varies the design; negotiator varies the constraints the design serves
**Note:** Historical merger of constraint-relaxer and constraint-inverter remains preserved: hypothetical opportunity and critical accommodation-cost questions share one constraint-change method. Hypotheses may precede cost evidence; real recommendations require feasible paths, actual cost evidence and authority.

---

## dialectical-synthesizer  *(base-generative, generate_options)*
**Method:** Conflict synthesis options (family `dialectical-synthesizer`, mode `default`)
**Question:** Can a candidate option preserve supported insights while making its changed assumptions and residual conflicts explicit?
**Mechanism:** A disagreement can sometimes depend on different assumptions or frames, permitting an alternative; other conflicts remain substantive or one side lacks support.
**Evidence needed:** Conflicting claims and their support, differing assumptions, candidate synthesis with retained insights and residual conflicts, discriminating evidence
**Procedure:** For each material conflict, trace claims and support separately without presuming both sides partly correct. Identify assumptions that differ. Construct a candidate synthesis only where coherent; specify retained supported insights, changed assumptions, residual conflicts and an evidence discriminator. Return an option candidate for separate scrutiny, or state that no useful synthesis emerged. Do not force reconciliation, issue a ruling or approve the generated option.
**Possible results:** candidate, no-material-finding, uncertainty
**Revise when:** Withdraw or revise the candidate when either side's supported evidence defeats its assumptions or it hides an irreducible conflict; preserve the conflict rather than splitting the difference by default.
**Limits:** Do not presume both sides partly correct or force reconciliation. New options remain hypotheses needing appropriate scrutiny; the synthesizer cannot approve its own invention.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `pragmatic-judge` — Synthesis generates candidate options for scrutiny; adjudication decides among supported findings and does not turn a candidate into evidence.

---

## first-principles-rederiver  *(base-generative, generate_options)*
**Method:** Derivation within accepted constraints (family `first-principles-rederiver`, mode `default`)
**Question:** What designs meet the accepted outcomes and constraints, including the best existing design?
**Mechanism:** An inherited choice can outlive its rationale, but convention can also encode obligations, compatibility or operating knowledge that a clean-sheet design misses.
**Evidence needed:** Outcomes, values, verified requirements and accepted constraints; existing design rationale, derived alternatives and all-in transition comparison from the present
**Procedure:** Understand the rationale of conventional designs first. State outcomes, values, verified requirements, accepted constraints and assumptions, including compatibility and obligations. Derive meaningful alternatives where useful inside that constraint set. Compare each with the present solution using all-in transition, operation and recovery costs from the actual current state. Allow re-deriving the existing solution as best; candidates neither authorize a rewrite nor replace evaluation. Route proposed constraint changes to constraint-negotiator.
**Possible results:** candidate, no-material-finding, uncertainty
**Revise when:** Revise an alternative when an overlooked requirement or conventional rationale defeats it, or all-in transition costs favor the present design; changing the constraint set requires its authorized decision-maker.
**Limits:** Works inside accepted constraints; constraint-negotiator changes the set. Generates candidates without authorizing rewrite or replacing evaluation.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `adjacent-possible-explorer` — explorer perturbs the proposal locally; rederiver rebuilds from constraints ground-up; `constraint-negotiator` — negotiator changes the CONSTRAINT SET itself; rederiver derives fresh WITHIN the true set
**Note:** Absorbs first-principles-engineer (merged 2026-07-10): the evaluator variant duplicated this derivation with a hostile tone — persona flavor, not a distinct mechanism.

---

## null-hypothesis-advocate  *(base-generative, generate_options)*
**Method:** Status quo and inaction options (family `null-hypothesis-advocate`, mode `default`)
**Question:** What would retaining, delaying, minimally maintaining or stopping actually preserve and cost?
**Mechanism:** A proposal can benefit from an unfair baseline that omits current value; the status quo can also deteriorate and require maintenance.
**Evidence needed:** Current benefits/burdens, horizon-specific deterioration/uncertainty, feasible inaction variants, comparable criteria and freed resources.
**Procedure:** Reuse an adequate current baseline. When weak or unfair, state the horizon and construct relevant retain, delay, limited-maintenance or stop variants for initiation or continuation. Record preserved benefits, dynamic deterioration, effort, risks and freed resources, separating measurements from estimates. Compare using the same criteria as active options and preserve authorized priorities. This supplies a fair comparator, not a statistical test, required evaluator seat or decision authority.
**Possible results:** candidate, no-material-finding, uncertainty
**Revise when:** Revise a baseline when observed deterioration, corrected benefits/costs or changed feasible options affect the authorized comparison. Inaction can remain inferior. Do not repeat specialist use merely because the workflow requires a baseline.
**Limits:** Supplies a fair comparator, not a statistical test or required evaluator seat. Applicable to initiation and continuation when inaction is a live option.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `sunk-cost-liberator` — Continuation review addresses irrelevant sunk costs; this supplies fair inaction options for initiation or continuation.; `opportunity-cost-accountant` — Allocation comparison uses feasible alternatives; this develops the status-quo/inaction comparator.

---

## opposite-steelman  *(base-generative, generate_options)*
**Method:** Supported advocacy for a rejected option (family `opposite-steelman`, mode `default`)
**Question:** What is the strongest supported case for the specified rejected branch?
**Mechanism:** An option given weaker scrutiny or asymmetric assumptions/costs may appear inferior without a fair comparison.
**Evidence needed:** Specified rejected/chosen branches, supported features, checked rejection assumptions, shared criteria/symmetric costs and marked evidence gaps.
**Procedure:** Identify the rejected branch and label this contribution advocacy. Build its best supported form, check rejection assumptions and mark missing evidence rather than inventing support. Present the chosen path fairly with the same criteria, constraints, horizon and symmetric costs. Deliver an option and comparison inputs, not a ruling or evaluator-diversity claim. The rejected branch may remain inferior after fair treatment.
**Possible results:** candidate, no-material-finding, uncertainty
**Revise when:** Revise advocacy when supported constraints or symmetric comparison defeats its claimed advantage, or revise rejection assumptions when contrary evidence changes them. Rhetoric alone cannot select a winner.
**Limits:** Develops a specified alternative; adjacent exploration searches nearby options and rederivation starts from constraints. Subsequent comparison is a separate contribution.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `adjacent-possible-explorer` — explorer searches the unexamined neighborhood; steelman advocates the explicitly-rejected branch; `null-hypothesis-advocate` — null-advocate defends doing nothing; steelman defends doing the OTHER thing

---

## premise-auditor  *(base-metatextual)*
**Method:** Unstated premise elicitation (family `premise-auditor`, mode `default`)
**Question:** Which unstated assumptions materially support the conclusion within the accepted frame?
**Mechanism:** An inference may depend on a hidden factual premise whose failure changes the decision; selected values or requirements are not unsupported factual beliefs.
**Evidence needed:** Text/inference supporting each elicited premise, fact versus selected-value/requirement classification, decision impact, uncertainty and scoped evidence/discriminators.
**Procedure:** Trace the inference and show where a missing premise is needed, citing text or reasoning rather than attributing private beliefs. Separate assumed facts from selected values and authoritative requirements. Rank plausible premises by decision impact and uncertainty; show consequences if the few material ones fail. Reuse shared claim/evidence representation once explicit and identify proportionate discriminators. Stop when further elicitation cannot materially change the decision.
**Possible results:** finding, no-material-finding, uncertainty
**Revise when:** Revise when the inference does not depend on the alleged premise, relevant evidence supports it, or corrected facts change the conclusion. Values and requirements change by authorized revision, not imagined contrary preference.
**Limits:** Owns elicitation/testing within the current frame; epistemic audit grades warrant once explicit; metacognate can regulate whether this method is needed.
**Stop and return:** Return when the scoped question is answered, existing adequate evidence is confirmed, or the remaining material evidence gap is explicit. Acknowledge actual use and continue the authorized task; do not manufacture findings or authority.
**Not to be confused with:** `polymath-inquisitor` — inquisitor challenges the frame's category; premise-auditor audits premises WITHIN the accepted frame; `epistemic-auditor` — epistemic-auditor grades STATED claims; premise-auditor excavates UNSTATED ones; `semantic-critic` — semantic-critic targets the words carrying claims; premise-auditor targets the propositions beneath them
