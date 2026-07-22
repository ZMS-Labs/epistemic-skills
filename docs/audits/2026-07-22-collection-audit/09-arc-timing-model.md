# Audit 09 — arc timing model

**Provenance:** 2026-07-22 collection audit, isolated read-only subagent against the working tree at 61fbf95 (v2.6.0). Operator's question: "We need to think hard about the exact 'timing' of every single one of these skills. When is research actually optimal? When is researching 'more' really important? When is research actually and genuinely completed? When should formal rigor be applied — before, during, or after research?"

---

## 1. Temporal semantics each skill already has

### using-epistemic-skills (router)
- **(a) Fires when:** a task might need more than one discipline, or sequencing is ambiguous (`SKILL.md:3`).
- **(b) Must not fire when:** only one discipline clearly applies — "Most work fires zero or one of these" (`:36`); "If none match, none fire — this router does not manufacture work" (`:68`).
- **(c) Arc position:** outside the arc; it *is* the arc. The arc is declared at `:40-44`: `recon → decide → contract → build → gate → prove`.
- **(d) Timing semantics:** The arc itself is the router's only temporal content, plus one sequencing rule: "If two match, run them in arc order… and pass each output to the next" (`:69-70`), and the gauntlet/UAT co-fire rule: "gauntlet gates first, evidence-locked-uat proves after" (`:72-73`). Notably, the arc diagram places formal-rigor and evidence-research in the *same* stage (`decide`, `:41-42`) with **no intra-stage ordering**.

### helix
- **(a) Fires when:** both layers are installed and a task begins, or a workflow stage just fired and its epistemic pair is unchecked (`SKILL.md:3`).
- **(b) Must not fire when:** single-collection routing, or trivial fully-held-context work (`:3`, `:80-81`).
- **(c) Position:** a *pairing layer* on top of the arc; positions are its core vocabulary: *before* / *inside* / *at approval* / *pre-merge* / *cross-cutting* (`:48-52`).
- **(d) Timing semantics — the richest in the collection:**
  - The governing rule: "At every stage boundary, **the epistemic member fires first**, then the workflow member carries the stage out" (`:26-31`). This is the collection's one general *ordering axiom*.
  - Two temporal failure modes are named: "recon after design is **archaeology**, and evidence after the verdict is **rationalization**" (`:31`).
  - Pairing table positions (`:35-46`): blindspot-pass is *before* brainstorming; formal-rigor is *inside* brainstorming/debugging; evidence-research is ***cross-cutting* — "called at the moment a qualifying premise appears, at any stage"** (`:39`, `:51-52`); gauntlet is *at approval* and *pre-merge*; write-goal is *before* persistent execution; UAT *is* verification-before-completion's UI instance.
  - The co-fire checklist is temporally reactive: pairs are checked "right now" at each boundary (`:57-73`).

### blindspot-pass
- **(a) Fires when:** "about to commit effort into territory you do not fully hold in context" (`:46-52`) — vague brief, pre-planning, pre-subagent-dispatch, pre-multi-agent fan-out, and crucially "**before locking the subject of an adversarial review**" (`:50`).
- **(b) Must not fire when:** well-understood reversible work, factual lookups, mechanical edits (`:53-55`); gated by a *checkable* skip gate: name ≥2 landmines (file:line) + the canonical example from memory right now (`:56-59`).
- **(c) Arc position:** `recon`, strictly first — "fires when there is **not yet a subject to freeze**" (`:35`).
- **(d) Timing semantics:**
  - **Recon floor:** "read at least 2–3 real artifacts… a pass that opens zero files isn't a pass" (`:77-78`).
  - **Recon ceiling:** "if recon is running long, that is itself a landmine — report it and hand off rather than continuing indefinitely" (`:79-80`). This is the collection's only *duration ceiling* on any skill.
  - **No validity window.** Nothing says how long a blindspot pass stays good; a pass from an hour ago in a session where the code changed is silently treated as current.

### applying-formal-rigor
- **(a) Fires when:** any decision with ≥2 viable options, or asserting "correct/better/cleaner/faster," or any complexity/Big-O question (`:18-21`).
- **(b) Must not fire when:** pure preference — falsifiable test: "no theorem or measurable property distinguishes the options" (`:23`).
- **(c) Arc position:** `decide`; helix: *inside* brainstorming and *inside* systematic-debugging (helix `:38`, `:43`).
- **(d) Timing semantics:**
  - **Convergence requirement (lens 4):** "an optimization analysis must reach a **fixed point** — always finding another gain signals a hallucination, an uncounted trade-off, or a missed bound" (SKILL.md `:55`; theory-battery.md `:85`). Terminal states: `improvable` / `trade-off` / `converged` / `optimal-for-constraints` (theory-battery.md `:85`). This is the collection's only **done criterion** for an open-ended analytic process.
  - **"Prove the lower bound, then stop"** (theory-battery.md `:83`) — a stop rule keyed to the Ω bound.
  - **Completeness-with-termination:** all 7 lenses enumerated and marked fired/not-applicable on the first pass (`:48`) — the sweep *ends* by construction.
  - No ordering rule vs evidence-research despite sharing the `decide` stage.

### evidence-research
- **(a) Fires when:** a claim rests on "the research says…", or **mandatorily before every scholarly-connector tool call** — "No direct-call exception" (`:61-69`). Helix position: *cross-cutting* — "the moment a qualifying premise appears, at any stage" (helix `:39`, `:51-52`).
- **(b) Must not fire when:** claims about completed work, general web search, single trusted internal lookup, pre-work recon (`:43-57`).
- **(c) Arc position:** `decide` (co-resident with formal-rigor); also feeds gauntlet's Step-0 evidence gate (`:40`, gauntlet `:101-111`).
- **(d) Timing semantics:**
  - **Freshness semantics (the strongest in the collection outside gauntlet):** "Reception data itself is `[V]`-grade **only when pulled live this run**; remembered tallies are `[H]`. Library notes without a live re-check are `[I]` at best when dated and DOI-keyed" (`:260-263`). This is a per-claim *validity window*: live-this-run = verified; dated = inference; remembered = hypothesis.
  - **Holdings-before-rediscovery:** the Zotero holdings check runs *before* discovery (`:135-141`) — temporal discipline against re-paying for prior judgment.
  - **Mode dials:** quick (3-5 papers) / standard (8-12) / deep (15-20, + second-order contrasting-citer reads) / formal-support (`:90-97`). These are **budgets, not escalation rules** — nothing states what moves you from quick to standard to deep.
  - **Pre-freeze/post-freeze boundary:** the matrix must be returned "before the dossier freezes" (`:244-245`); "After freeze, reviewers use only the frozen record (no ad hoc searches); a material gap triggers the review's controlled dossier-reopen, which may re-invoke this skill — never a silent amendment" (`:265-267`).
  - **No convergence criterion.** §4's multi-query sweep (`:143-149`) ends at the mode's paper cap — "`Top N of M` is a plan cap, not scarcity evidence" (`:147-148`) — which is explicitly acknowledged as *not* a completeness signal. There is no saturation test.

### write-goal
- **(a) Fires when:** **explicit user request only** — goal authoring, "what would count as done," persistent-goal creation (`:3`, `:28-30`).
- **(b) Must not fire when:** ordinary tasks ("fix this bug" is not permission, `:29-30`); never auto-create; drafting and starting are separate state changes requiring separate consent (`:32-34`, `:261`).
- **(c) Arc position:** `contract`, after `decide`, before `build`. Router: "runs after intent is sufficiently de-risked" (router `:46-47`).
- **(d) Timing semantics:**
  - **"Sufficiently de-risked" has no threshold.** Router `:46` and the consumes-row (`:21`) both assume de-risking happened; neither says what counts. The goal-type table partially compensates: `Not goal-ready` if "the user has not chosen among materially different outcomes" (`:42`), and learning-first goals must "name the decision it will unlock and its exit condition" (`:46`) — a *conversion* timing rule (learning-first → performance goal is a second, explicit state change).
  - **Consent ordering:** draft → user review → approve → start (`:118-135`); skip review only if the request states all contract fields verbatim (`:131-135`).

### gauntlet
- **(a) Fires when:** irreversible / one-way-door / infra / security / non-refundable spend / architecture commit / high-stakes hard-to-verify claim (`:47-50`); positions *at approval* and *pre-merge* (helix `:40`, `:45`).
- **(b) Must not fire when:** reversible low-stakes, lookups, ordinary code review, deterministic test triage (`:51-52`); triage (Step 2) can skip after firing with an evidence-cited reason (`:143-148`).
- **(c) Arc position:** `gate`, between `build` and `prove`; can also gate at design-approval before planning (helix `:40`).
- **(d) Timing semantics — the collection's temporal core:**
  - **The freeze (Step 0):** live-verify premises, then "write the **frozen verified dossier**… All downstream argument uses only this record" (`:95-121`). The freeze is a hard **time boundary**: pre-freeze evidence gathering is open; post-freeze argument is closed-world.
  - **Controlled reopen:** "a bounded post-freeze reopen is allowed only for a provenance-grade contradiction" (`:121`); "never silently amend an existing verdict" (`:110-111`).
  - **The drift rule:** "If the subject moves, restart" (`:138`). The collection's only general *invalidation* semantics.
  - **Scholarly-evidence gate:** evidence-research runs *before* freezing; contrasting-heavy papers enter labeled `disputed`; retracted excluded (`:101-111`). This is an explicit cross-skill *ordering*: research-then-freeze.
  - **Bounded reinstatement:** one round only at arbitration (`:305-306`) — a termination guarantee on dispute loops.
  - **Evidence freshness in the verdict:** every GO/CONDITIONAL must state "evidence freshness" (`:354-355`) — the verdict itself is timestamped epistemically.

### evidence-locked-uat
- **(a) Fires when:** UI-facing work about to be claimed done / merged (`:3`); "strictly post-work" (router `:50`).
- **(b) Must not fire when:** backend-only, docs, test refactors with no runtime surface (`:3`); no reachable rendered surface → `BLOCKED_ENVIRONMENT`, never substitute code reading (`:23-24`).
- **(c) Arc position:** `prove`, terminal.
- **(d) Timing semantics:**
  - **First-run immutability:** "The first run's gate is immutable" (`:75-77`).
  - **FLAKY rule:** a rerun that passes after a failed run makes the aggregate FLAKY — "report both run-ids and the FLAKY status; diagnose before trusting either result" (`:76-78`). Retry-until-green is a named anti-pattern (`:90`).
  - **Tier immutability:** "NEVER silently downgraded mid-run" (`:22-23`).
  - These are *history* semantics: UAT is the only skill whose verdict depends on the ordered sequence of prior runs.

---

## 2. The operator's research-timing questions, answered with evidence

### When is research optimal?
The collection's placement is **stated, and stated twice, consistently**:
1. Arc: `decide` stage, alongside formal-rigor (router `:41-42`).
2. Helix: *cross-cutting* — "reception-check the literature **before the premise bears load**" (helix `:39`); "called at the moment a qualifying premise appears, **at any stage**" (helix `:51-52`).

The "too early / too late" framing maps cleanly onto helix's two named failure modes (`:31`): research after the verdict is *rationalization* (too late); the premature case is covered by the trigger itself — a premise that isn't yet load-bearing isn't yet a qualifying premise, so "too early wastes" is guarded by the trigger definition, not by a timer. The optimal window is therefore **defined trigger-wise, not clock-wise**: the instant a premise becomes load-bearing and before any downstream artifact (design, dossier, goal contract) commits to it. Gauntlet adds a hard upper bound: research must complete *before the dossier freezes* (evidence-research `:244-245`, gauntlet `:108-109`).

### When is researching MORE important — escalation signals?
Escalation **signals** exist; escalation **rules** do not. The signals:
- Contested reception: "A finding whose key papers carry heavy, substantive contrasting reception is *contested*" (`:219-221`) — but the response is "say so," not "go deeper."
- `deep` mode's distinctive mechanic — second-order reading of contrasting citers (`:96`) — has no stated entry condition beyond "high-stakes synthesis" in the mode label.
- Stakes-based gating exists for gauntlet (`:143-148`) and UAT tiers (`:16-21`) but **not** for research modes. The mode choice in §1 Frame is "Choose and label the mode" (`:103`) — selection is a judgment call with a paper-count dial. **Mode choice is, in the operator's terms, a vibe with a budget.** The nearest thing to an escalation trigger is gauntlet's Step 0: "when peer-reviewed evidence is **material** to a premise or decision" (gauntlet `:101-102`) — a materiality gate, but it gates *whether* research runs, not how deep.

### When is research genuinely COMPLETE?
**It isn't defined. This is the collection's single biggest timing hole.** Compare:
- formal-rigor lens 4: analysis is done at a **fixed point** — re-derivation yields no new gain, else the terminal state is diagnosed as hallucination / miscounted trade-off / missed bound (theory-battery.md `:85`; "Prove the lower bound, then stop" `:83`).
- evidence-research: done at a **paper-count cap** (`:90-97`). Worse, the skill itself flags the cap as epistemically void: "`Top N of M` is a plan cap, not scarcity evidence" (`:147-148`). The skill *knows* the cap doesn't mean "no more evidence exists" yet provides no alternative termination test.
- Candidate fixed-point analogues are latent in the protocol but never assembled into a criterion: §4's query families run broad→narrow→counterevidence→boundary (`:144-146`) — a saturation signal would be "the counterevidence and boundary-condition queries surface no new relevant DOIs"; §5's reception semantics suggest "reception ratios stable across the last N papers pulled"; §7's cross-validation divergence could bound "coverage mapped." None is stated. The skill has a start trigger, a mid-run freshness rule, and a budget — but no fixed point.

### Formal rigor vs research ordering
**No skill says.** They cohabit the `decide` stage (router `:41-42`) and the router's two-match rule orders by *arc* order, which is silent *within* a stage (`:68-70`). Helix assigns formal-rigor *inside* and research *cross-cutting* (`:38-39`) — different position types, no relative order.

The correct ordering from first principles, with a dependency test:
1. **If the derivation consumes the empirical premise** (e.g., "choose index strategy because research says workload is read-heavy"), research fires first — the premise must be `[V]`-grade before it bears load in the derivation, per helix's own "before the premise bears load" rule (`:39`). Formal-rigor's DERIVE discipline (`:40-45`) requires its inputs to be facts, not hypotheses; unverified empirical premises would enter as `[H]` and taint the verdict.
2. **If the research question depends on the derived constructs** (e.g., you can't frame "does the literature favor snapshot isolation for this workload?" until the derivation names the anomaly at stake), rigor fires first — §1 Frame (`:101-103`) needs the claim framed, and the precise construct is what makes the frame non-vacuous. This is blindspot-pass's "vocabulary the codebase doesn't actually use" failure transposed: researching an unprecise question retrieves literature about the wrong construct.
3. **General rule:** research is *cross-cutting* (helix `:51`), so the natural encoding is: **derive first to name the precise constructs and identify which premises are empirical and load-bearing; research exactly those premises; then complete the derivation with `[V]`-grade inputs.** Rigor's lens sweep (`:48`) is the enumeration step that *discovers* the empirical premises — it's the natural trigger generator for research. The collection currently encodes fragments of this (research before premise bears load; research before freeze) but never the rigor→research→rigor sandwich.

---

## 3. Pairwise ordering matrix (6 disciplines + router + helix)

Legend: **E** = explicit in the collection, **C** = emergent but consistent, **A** = ambiguous/undefined, **X** = contradictory.

| Ordering | Status | Evidence |
|---|---|---|
| blindspot-pass → everything | **E** | Arc position `recon`, first (router `:41`); "fires when there is not yet a subject to freeze" (blindspot `:35`); helix *before* brainstorming (`:37`) |
| blindspot-pass → gauntlet | **E** | "before locking the subject of an adversarial review" (blindspot `:50`) |
| blindspot-pass → evidence-research | **E (callable)** | "May *call* this skill when a landmine/question needs scholarly grounding" (evidence-research `:38`, `:53-55`). So blindspot recon may *invoke* research mid-pass — the one sanctioned intra-skill nesting. Direction is one-way; research never calls blindspot |
| formal-rigor ↔ evidence-research | **A** | Same arc stage, no intra-stage order (router `:41-42`); helix gives different position types but no relative order — see §2 above |
| evidence-research → gauntlet | **E** | Research returns matrix "before the dossier freezes" (`:244-245`); gauntlet Step 0 scholarly gate (`:101-111`) |
| write-goal after blindspot/formal-rigor/research | **E (weak)** | "runs after intent is sufficiently de-risked" (router `:46-47`); consumes "de-risked context, and any evidence/design inputs" (write-goal `:21`) — but "sufficiently" unquantified |
| gauntlet → evidence-locked-uat | **E** | "gauntlet gates first, evidence-locked-uat proves after" (router `:72-73`) |
| evidence-locked-uat terminal | **E** | Arc `prove` stage, post-work (router `:50`); helix: UAT *is* verification-before-completion's UI instance (`:44`) |
| helix → (all disciplines) | **E** | "the epistemic member fires first at a stage boundary; the workflow member carries the stage out" (router `:96-98`; helix `:26-31`) |
| router → helix | **E** | "read helix now — it carries the full stage-pairing map" (router `:94-98`); helix "sits between" the two routers (helix `:111`) |
| gauntlet vs write-goal | **C** | Goal contract before execution (helix `:41`); gauntlet gates irreversible commits *within* execution (router `:48-49`). Consistent: contract, then gate during execution |
| blindspot-pass vs write-goal | **C** | De-risked request is write-goal's input (router `:23`, `:26`); consistent via the handoff table |
| formal-rigor re-fire in debugging | **E** | helix `:43` — rigor fires *inside* systematic-debugging too; the only discipline with two sanctioned arc positions |
| UAT vs gauntlet on same merge | **E** | router `:72-73` (both can fire; order fixed) |
| Re-firing any skill when the subject drifts | **A** (gauntlet only: **E**) | gauntlet: "If the subject moves, restart" (`:138`). No other skill has a drift rule — see §4 |

No contradictory (**X**) pairs found — the collection is internally consistent where it speaks; its defects are silences.

### The freeze as the model temporal gate
Gauntlet's Step 0 freeze is the collection's **one hard temporal boundary** with full semantics: a defined pre-state (open evidence gathering), the boundary event (freeze, `:119-121`), a defined post-state (closed-world argument, `:120`), a sanctioned exception (controlled reopen for provenance-grade contradiction, `:121`), and an invalidation rule (subject moves → restart, `:138`). Evidence-research plugs into it with matching freshness tiers (`:260-263`). It is exactly the shape the other skills lack: **a named validity window with an expiry rule.** Yes — this is the model the others should copy, scaled down to one or two lines each (see §5).

---

## 4. Timing defects and holes (concrete list)

1. **No research-convergence criterion.** evidence-research terminates on a paper-count budget (`:90-97`) that the skill itself declares epistemically void (`:147-148`). No saturation/fixed-point test analogous to lens 4's (theory-battery.md `:85`). *The biggest hole.*
2. **No escalation rule between research modes.** quick→standard→deep thresholds are unstated; mode selection is "choose and label" (`:103`). Contested reception (`:219-221`) and high stakes are signals with no wired response.
3. **formal-rigor ↔ evidence-research ordering unspecified.** Same stage (router `:41-42`), no intra-stage rule; the dependency direction (which consumes whose output) is determinable case-by-case but never encoded.
4. **No validity window on blindspot-pass recon.** A pass is consumed "downstream" (`:104-110`) with no staleness semantics. How long does a rewritten request stay de-risked? Only gauntlet downstream protects itself (its own Step 0 live-verifies premises, `:96-100`) — meaning the system *compensates* for stale recon at the gate rather than expiring the recon.
5. **write-goal's "sufficiently de-risked" has no threshold** (router `:46-47`). The `Not goal-ready` row (`:42`) covers an unchosen outcome but not an under-reconned one.
6. **No general drift/re-fire rule.** Only gauntlet has "if the subject moves, restart" (`:138`). If the codebase changes after blindspot-pass, or the literature premise is refuted after the design commits, or the goal's environment shifts mid-run — nothing says re-fire. UAT's FLAKY rule (`:75-78`) is adjacent but is about verdict history, not subject drift.
7. **Freshness semantics exist for exactly one data type.** Reception data is `[V]` only live-this-run (`:260-263`); nothing equivalent for blindspot recon facts, formal-rigor verdicts (a verdict derived against N is void if N changes), or goal contracts.
8. **helix's co-fire check is boundary-triggered, not time-triggered** (`:57-73`). Between boundaries, drift is invisible to the pairing layer.
9. **Recon ceiling is a vibe** — "if recon is running long" (blindspot `:79`) names no unit (turns? artifacts? wall-clock?). It's the only ceiling in the collection and it's unmeasurable.

---

## 5. Proposed minimal timing layer (floors, not ceilings)

Five additions, each a few lines, no new mechanisms:

**(a) Validity column in the router's handoff table** (router `:21-28`). Add one column, "Valid until," one line per skill:
- blindspot-pass: "valid until the territory changes or the next stage starts — re-run the skip gate (`:56-59`) if either happens"
- formal-rigor: "valid until a named input (parameter, dependency, workload) changes"
- evidence-research: "reception `[V]`-grade this run only (already `:260-263`); the matrix is a snapshot — date it"
- write-goal: "valid until intent, scope, or environment drifts; drift → re-draft, not silent amendment"
- gauntlet: "valid for the frozen subject only (already `:138`)"

**(b) A convergence criterion for evidence-research, modeled on lens 4's fixed point** (insert after `:147-149`). Three lines: *A research run converges when the counterevidence and boundary-condition query families surface no new relevant DOIs beyond the mode's reception dial, and reception ratios on the load-bearing papers are stable across the last two pulls. A run that always finds another relevant paper has the same three failure modes as an unconverged optimization: an ill-framed question, a scope trade-off miscounted as coverage, or an underestimated literature. Label the terminal state: `saturated` / `capped-by-budget` / `contested-stable`.* This directly ports `improvable/trade-off/converged/optimal-for-constraints` into research vocabulary and makes "capped-by-budget" an honest label rather than a silent exit.

**(c) An escalation trigger list for research modes** (insert into the Modes section, `:90-97`). One line: *Escalate one mode when any of: a load-bearing paper is contested (substantive contrasting reception); the decision is high-stakes/irreversible; Consensus↔Scite cross-validation diverges on the core question; the synthesis must support a gauntlet dossier. De-escalate only when the claim is directional and no load-bearing paper is contested.* Mirrors UAT's tier table (`:16-21`) in shape — a pattern the collection already uses.

**(d) One sentence resolving formal-rigor ↔ research ordering** (router, after `:69-70`): *Within the decide stage, run formal-rigor's lens sweep first to name the precise constructs and expose which premises are empirical; research exactly those premises; then complete the derivation with the verified matrix as input. If the empirical premise is the decision's whole basis, research may lead — but the derivation still closes the stage.* Encodes the dependency test from §2 without a new mechanism.

**(e) A drift rule generalizing gauntlet's "subject moves → restart"** (`:138`) into the router's shared invariants (`:76-92`), one line as invariant 6: *If a skill's subject materially changes after the skill ran, its output is void and the skill re-fires at its own trigger — never patch the old output. The downstream consumer, not the producer, owns the re-fire check.* This extends the collection's best temporal semantics (freeze + restart) to the skills that currently go stale silently (blindspot recon, research matrices, goal contracts), and placing the check on the consumer matches how gauntlet's Step 0 already compensates for stale upstream inputs (`:96-100`).

**Ambiguity flagged for the operator:** the proposal in (b) assumes "convergence" is checkable within a session; the reception-stability half requires pulling reception incrementally, which the current §5 flow does per-paper rather than longitudinally — it's a one-line semantics change, but it does slightly raise the floor of every `standard`+ run. If that's too heavy, the minimal version is just the terminal-state label (`saturated` / `capped-by-budget`) with no stability requirement — honest naming alone closes most of the hole.
