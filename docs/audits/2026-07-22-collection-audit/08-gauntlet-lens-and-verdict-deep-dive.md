# Audit 08 — gauntlet lens & verdict machinery deep-dive

**Provenance:** 2026-07-22 collection audit, isolated read-only subagent against the working tree at 61fbf95 (v2.6.0). Registry v2.2.0, 102 entries, computed live from `roster/registry.json`. Base: `plugins/epistemic-skills/skills/gauntlet/`. Operator's question: are the gauntlet's results (1) trusted, (2) efficiently understood, (3) effectively implemented, (4) decisively verified — and are the lenses sufficient, proper, well-defined, substantial, and used in the right combinations suitable to the task? Prior-audit hygiene findings (empty ledgers, missing evals/README.md, 30-vs-24 drift, stale synthesis template, shadow-seat fail-open, dead roadmap pointer) treated as known.

---

## PART 1 — Trusted

**What actually makes a verdict trustworthy today, in descending order of strength:**

1. **The verdict gate is a rule, not a computation.** SKILL.md:347-348 defines the gate ("unresolved P1 → NO-GO; P2 open → CONDITIONAL; else GO") and SKILL.md:19 advertises "computed acceptance (you cannot set a status)". But there is no code that computes the verdict — the computation happens inside the arbitrator LLM's head against `ruling-set@1` (`reference/lens-registry.md:47-49`). No `verify_verdict.py` exists; nothing re-derives the verdict from the structured rulings after the fact. The only mechanical enforcement of gate-correctness is the `governance-lawyer` card ("the verdict gate (P1 unresolved → NO-GO) was applied correctly", `roster/arbitrators-and-specialists.md:82-84`) — itself an LLM, and **only seated at deep/max** (`scripts/select_lenses.py:299-300`). A standard-depth run — the default — has *no process-conformance gate at all*. So "computed verdict" is currently "prompt-constrained verdict, certified by battery, unverified per-run."

2. **The arbitrator certification is real but narrow — and certifies exactly one seat.** The battery (`evals/arbitrator-certification/battery.json`) is well-designed: 10 planted defect classes covering the arbitrator's own discipline, dispatched blind, deterministically scored, 10/10 catch with honest treatment of the 2 verdict divergences (`results-2026-07-17.md:35-55`). But its own scope note is decisive (`results-2026-07-17.md:68-76`): it certifies **the arbitrator seat's discipline only**. The lens reports in the battery are *authored/simulated*, not produced by real lenses — so the GENERATOR side (option quality) and the PANEL side (do real lenses find real defects?) are **uncertified**. The panel's behavioral battery has only a smoke subset, non-inferiority not superiority, and the smoke notes aren't even shipped in this package (SKILL.md:401-405). The trust chain is: certified janitor, uncertified detectives.

3. **[V]/[I]/[H] enforcement is half-mechanical.** `verify_evidence.py` mechanically checks `[V path:line]` anchoring and enforces the binary-medium guard by design (SKILL.md:290-291), and `[I]` anchors must resolve. But `[H] = zero weight at arbitration` is enforced by the arbitrator, not by code; oracle-adequacy (Step 6(3), SKILL.md:277-282) is an LLM judgment absorbed from a retired lens; falsifier well-formedness striking (SKILL.md:271-275) is likewise arbitrator-executed. The battery proves one arbitrator build does this reliably; nothing re-proves it per run.

4. **Oracle adequacy is the strongest single piece of doctrine.** The fail-closed oracle rules (SKILL.md:282-292 — verify the tool exists before trusting silence; match oracle to medium; plant-a-positive before believing a scan) are genuinely excellent, better than most professional audit standards, and two of them are battery-tested (AC-02, AC-05).

5. **The independence barrier is procedural, and no shipped artifact can prove it.** Step 5 demands concurrent context-isolated role-agents behind a barrier (SKILL.md:219-232), but the only replayable isolation proof exists in the Claude Code Workflow reference implementation's journal (SKILL.md:234-237). In the documented degrade fallback (SKILL.md:255-259) — "consecutive isolated agent calls with strict per-lens context partition" — nothing distinguishes real isolation from one agent role-playing five lenses. Deeper: all lenses typically run on the *same model*, so independence is contextual, never architectural; the mitigation is the correlated-claims rule (SKILL.md:300-302), which is battery-tested (AC-03) but again arbitrator-executed.

6. **Model-family separation of judge vs lenses is close to a dead letter.** "The judge seat must use a different model family than the lenses **when configurable**" (SKILL.md:215-216) — in the default harness everything is one family, so the qualifier swallows the rule. Step 7b exists precisely because of this (SKILL.md:313-316) but is optional, operator-gated, manual-handoff, and the skill itself deflates its value: "cross-vendor is not cross-independent (measured cross-family agreement ≈ within-model order-repeatability)" (SKILL.md:337-340). And **no artifact records which model/family ran any seat** — the ledger schema (`runs/README.md:17-38`) has no model fields, so the requirement is unverifiable post-hoc even when honored.

**Part 1 verdict: the machinery makes verdicts *defensible* — the gate, tiers, and shadow semantics are sound doctrine and the arbitrator is battery-proven — but per-run trust rests on LLM self-enforcement at exactly the points (gate computation, [H] zero-weight, oracle adequacy, standard-depth process conformance) where a mechanical check would be cheap.**

---

## PART 2 — Lens sufficiency and quality

### (a) Distribution (computed from registry.json)

- Lifecycle: 67 active / 5 probation / 24 candidate / 6 retired (matches `roster/INDEX.md:9-14`).
- Live (active+probation, 72): 62 evaluate, 4 generate_options, 2 gate, 4 adjudicate (`INDEX.md:18-23`). Live evaluator stances: **adversarial 27, metatextual 20, constructive 15** — constructive is the thin stance, and both mutex-pair members (`cloud-native-purist`, `local-first-survivalist`) are constructive, so an intentional-contrast panel burns 2 of the constructive allowance on one axis.
- Families (live, all roles): framing-epistemics 8, strategy-alternatives 6, operability 6, then human-factors/maintainability/reliability/security/governance-ethics 5 each, down to **four singleton families: incentives (game-theorist), interoperability (integration-weaver), risk-tails (black-swan-catalyst), simplicity (minimalist-zen-master)** (`INDEX.md:25-45`). Singletons are load-bearing: the deep/max ≥4-family repair pass (`select_lenses.py:188-222`) has no fallback if a singleton is axis- or stance-excluded.
- Cost classes: 66 standard / 6 heavy / **0 light** — the `light` tier in `COST_PENALTY` (`select_lenses.py:68`) is dead code, and with W_COST=0.5 the cost term differentiates almost nothing.
- **Domain vocabulary is uncontrolled free text: 172 unique domain strings across 72 live lenses** (`infra`/`operations`/`ops` are three different strings; `cost`/`cost-benefit`/`finance` don't intersect). Since domain fit is exact-set Jaccard (`select_lenses.py:86-87`), the largest-weighted fit term (W_DOMAIN=3.0, line 63) scores 0 for most plausible subject descriptions. This is the mechanistic root of the frozen fit layer (see Part 3).

### (b) Substance of sampled cards (11 sampled across roles)

| Card | Rating | Why |
|---|---|---|
| `chaos-monkey` (`adversaries.md:39-45`) | **substantial** | Concrete method (simultaneous-fault injection, N+1→N probe), mechanically runnable falsifier (replay/failover test, degraded-not-down threshold) |
| `bus-factor-adversary` (`adversaries.md:29-35`) | **substantial** | Distinct object (head-resident knowledge), cold-runbook-drill falsifier with success threshold |
| `compliance-litigator` (`adversaries.md:49-55`) | **substantial** | Genuinely disjoint from `predatory-regulator` (inward records-as-exhibits vs outward disclosures) — a real boundary, not flavor |
| `statistical-validity-critic` (`arbitrators-and-specialists.md:130-136`) | **substantial** | Names its attack classes (base rate, multiple comparisons, train/test leakage, Simpson); falsifier is a recompute |
| `fmea-analyst` (`arbitrators-and-specialists.md:60-66`) | **substantial** | Severity × likelihood × undetectability ranking; the "severe, plausible, SILENT" focus is a real prioritization method |
| `integration-weaver` (`visionaries.md:65-71`) | **substantial** | Concrete surface (idempotency keys, error semantics); naive-integrator walkthrough falsifier |
| `wcag-accessibility-expert` (`arbitrators-and-specialists.md:160-166`) | **substantial** | Anchored to an objective external standard; easy-fix vs structural triage |
| `game-theorist` (`metatextual.md:65-71`) | **moderate** | Real method (payoff/deviation analysis) but no procedure; falsifier "payoff computation" is analyst-judged |
| `semantic-critic` (`metatextual.md:152-158`) | **moderate-thin** | Plain-restatement test is real but soft; overlaps premise-auditor at the edges |
| `ecological-systems-analyst` (`metatextual.md:39-45`) | **thin** | "Map upstream pressures, regulatory weather" is generic environmental-scan advice; any lens could produce it |
| `polymath-inquisitor` (`metatextual.md:112-118`) | **thin** | "Ask whether that's the question that matters; surface analogies" — closest to a horoscope in the sample; falsifier ("reframing doesn't change the decision", method: analysis) is barely observable |

Systemic pattern: card quality tracks falsifier observability. Adversarial/specialist cards name drills, recomputes, traces, walkthroughs — mechanically executable. The **framing-epistemics family (the largest at 8)** leans on "method: analysis" falsifiers, which degrade to arbitrator judgment. The registry's own admission standard ("Persona flavor is not novelty", `reference/lens-registry.md:12`) is met by ~80% of sampled cards; the thin ones survive because the collision oracle is token-Jaccard, which "will under-flag paraphrase collisions" by its own admission (`lens-registry.md:103-106`).

That said, the *neighbors/boundary* discipline is the roster's standout quality feature: every sampled card has explicit "not to be confused with" edges with stated boundaries, and the 2026-07-10 merges (`lens-registry.md:108-127`) show the standard was actually enforced, not aspirational.

### (c) Coverage against representative subjects (selector executed live, zero constraint violations in all 7)

- **Infra/firewall change** (deep-relevant): panel = script-kiddie, cloud-native-purist, protocol-archeologist, entropy-demon, **angry-customer**. Angry-customer (domains `["product","ux","support"]`) on a firewall change is a plain mis-seat — it arrived via MMR fill because real-fit scores were all near zero. Also note `chaos-monkey`'s contraindication "pure document/policy subject" exists, but see Part 3: **contraindications are not gates**.
- **API design**: good panel (integration-weaver seated — the specialist rule fired correctly).
- **Data migration**: **structural hole.** Panel = data-provenance-auditor, adjacent-possible-explorer, analogical-historian, digital-forensicist, cloud-native-purist. The three on-point lenses — `state-migration-compatibility-auditor`, `release-cutover-auditor`, `recovery-integrity-auditor` — are candidate/probation and unselectable. The entire migration/cutover/restore capability cluster sits behind the behavioral admission gate **which has never been run for any candidate** (`lens-registry.md:89`, `candidates.md:5`).
- **Public-repo release**: `ip-freedom-to-operate-auditor` — the single most on-point lens — is a candidate. Panel got compliance-litigator (reasonable) plus bus-factor-adversary (off-target).
- **Cost/spend decision ($120k reserved cloud)**: **the selector missed both economics lenses.** `unit-economics-adversary` scored **−0.125** and `opportunity-cost-accountant` **−0.125** — below angry-customer (0.375) — because `finance` ≠ `cost` and `cost-benefit` ≠ `cost` under exact-string Jaccard. Panel has zero economics-family seats on a pure spend decision.
- **UI/UX change**: decent (ui-ux-polisher seated), but `wcag-accessibility-expert` missed because `ux` doesn't match `accessibility`/`wcag`/`inclusive-design`.
- **Legal/governance charter**: compliance-litigator + red-lines gate attached (good), but panel includes chaos-monkey — whose own contraindication ("pure document/policy subject") marks this exact subject — because contraindications only cost ~3 points of score, recoverable via family/stance gain.

### (d) Mutex/counter-mode design

The `leverage-vs-sovereignty` pair is well-chosen: genuinely opposite priors over the same decisions, and the ONE-diversity-unit rule is correctly implemented in both the selection path (`select_lenses.py:135-137`) and the post-hoc constraint check (lines 321-328, dedup before stance/family counting). Sound. Two caveats: (1) exactly **one** mutex group exists for 102 lenses — other near-counter-modes (e.g. performance-alchemist vs century-horizon-architect's "fashionable abstraction" attack) go unmodeled; (2) an intentional-contrast pair consumes 2 constructive seats (the scarcest stance) for 1 diversity unit, which the stance cap permits but doesn't warn about.

**Part 2 verdict: proper and well-defined at the registry-model level; substantial for ~80% of cards; NOT yet sufficient — distribution has four singleton families, the constructive stance is thin, and the best coverage for migration/release/IP/DR subject classes is frozen in candidate/probation status behind an admission gate that has never run.**

---

## PART 3 — Right combinations, suitable to the task

This is the weakest part of the system, and the code is more honest about it than the docs.

**The frozen fit layer.** `select_lenses.py:64-67` states plainly: the fit/MMR scoring layer showed **no detectable benefit over random fill under the same hard constraints** (v3 arm D control), and is retained only because it's deterministic, token-free, and auditable. Live runs confirm the mechanism: on the spend subject, the two most relevant lenses scored *negative*; on the firewall subject, angry-customer was seated. Panel selection today is **constraint-satisfaction + diversity-maximization, with task-fit carried almost entirely by three things**: the hard gates (role/status/axis), the domain-specialist seed (lines 151-158), and operator `include_ids`. The MMR fill among near-zero-fit lenses is effectively arbitrary within constraints.

**Is that honest in the docs? Partially — and partially not.** `reference/lens-registry.md:164-167` discloses "lexical — a documented v1 limitation" and that a keyword match "can mis-rank but never seat a candidate, a retired ID, or a wrong-role card". But SKILL.md — the file an operator actually reads — presents the selector as "scores fit + uncovered-capability gain + stance diversity − overlap − cost" (SKILL.md:178-180) with **no mention that the fit term is measured-no-better-than-random**. The null result lives only in a code comment. An operator reading SKILL.md would believe panel composition is task-tuned; it is task-gated and diversity-tuned. That's a transparency gap of exactly the kind this skill exists to catch.

**The domain-specialist rule does fire** — verified live (script-kiddie seeded first on the infra subject, compliance-litigator on the charter, integration-weaver on API design; `select_lenses.py:151-158`, constraint check lines 346-350). But it inherits the vocabulary fragmentation: it fired on the spend subject with a data-validity "specialist" (forensic-accountant) while both economics lenses went unseated, and it can't fire at all when subject domains use words no lens uses (`network` matches zero of 172 domain strings).

**Doc/code mismatch — contraindications.** SKILL.md:178 claims the selector "gates by lifecycle/role/axis/contraindications". The code gates on role/status/axis only (`select_lenses.py:102-119`); contraindications are a *score penalty* (−1.5×min(contra,2), lines 92-93) that family-gain (+1.5) and stance-gain (+1.0) can fully offset — which is exactly how chaos-monkey got seated on a "pure document/policy subject" it contraindicates. Either the doc or the code is wrong; given the frozen-scoring finding, the honest fix is the doc unless contraindications are promoted to gates.

**Minor soundness notes:** the ≥3/≥4 family floors plus stance cap are well-formed and 1000-fixture verified; the repair pass (lines 188-222) is stance-preserving; the shadow seat correctly sits outside all diversity math (lines 251-285). One real fragility: `MIN_FAMILIES` at deep/max = 4 while four families have exactly one member — the constraint surface depends on singleton lenses always being eligible.

**Part 3 verdict: the selector reliably produces *valid, diverse, replayable* panels; it does not produce measurably *task-suitable* ones, the fit layer is frozen as null, the operator-facing docs overstate this, and the domain vocabulary is too fragmented for even the gates and specialist seed to express task-fit reliably.**

---

## PART 4 — Efficiently understood + effectively implemented + decisively verified

**(a) Understood — mostly yes.** `assets/synthesis-template.md` is 46 lines; Executive Verdict + Conflict Ledger + P1–P4 matrix is genuinely 2-minute-consumable. The verdict vocabulary is tight (GO/CONDITIONAL/NO-GO with mechanical gate semantics), the honest-labeling line (template line 18; SKILL.md:359-360) sets correct expectations, and the mandatory GO coverage statement (SKILL.md:352-356 — families exercised, assumptions, known unknowns, freshness, residual uncertainty) is an excellent anti-false-GO device. Residual issues beyond the known staleness: the template's ruling enum at line 36 lists `UPHELD | OVERRULED | SPLIT` and **omits UPHELD-WITH-QUALIFICATIONS**, which the canonical contract (`lens-registry.md:47-48`) and SKILL.md:302-303 both require; and "Consensus Result" (line 14) is the wrong frame for a computed, dissent-preserving verdict — the template's vocabulary contradicts the skill's own anti-averaging doctrine.

**(b) Implemented — the weak half.** When CONDITIONAL, conditions are "[enumerate]" (template line 17) — free prose. Yet the structured form already exists one contract layer down: `ruling-set@1` requires `acceptance criteria · computed verdict · next action` per ruling (`lens-registry.md:47-49`), and every finding already carries a falsifier with method/threshold/timeframe (`finding-set@1`, lines 44-46). The summary template simply doesn't carry them up: no condition objects, no owner/deadline beyond a bare Owner column (template line 40-43), no machine-readable block a downstream stage could consume. So conditions rot as prose exactly as the operator feared. NO-GO path is clearer (the gate names the blocking P1s, and reinstatement is bounded to one round, SKILL.md:304-306), but there is no defined "what would change this verdict" field — each P1's falsifier *is* that, implicitly, and making it explicit is a template-line change.

**(c) Verified — the biggest gap.** Distinguish three claims:
- *The arbitrator seat is certified in general* — yes, battery-backed (Part 1).
- *A given run's selection is replayable* — yes, and this is genuinely good: the selector writes a full replay record (registry sha256, subject vector, scores, exclusions, ids@versions; `select_lenses.py:371-380`) and role-binding emits `gauntlet-role-binding@1` records (SKILL.md:241-249).
- *A given run was properly conducted* — **no artifact set proves this.** Concretely missing:
  1. **No content-hash chain.** Nothing binds dossier → reports → arbitration → summary → ledger line. A third party cannot detect post-hoc editing of any run artifact; the ledger line doesn't even name the run directory (`runs/README.md:17-38` — fields are ts/subject/depth/registry_sha/verdict/eligible/lenses only).
  2. **Schema/doctrine mismatch:** SKILL.md:363 requires recording "the docket mode + `independence_mode` + which depth ran"; the ledger schema has depth but **no docket-mode or independence-mode fields**. The two most audit-relevant facts about a run (was the docket replay-backed? was isolation degraded?) are unrecordable in the only mandated record.
  3. **No model identity anywhere** — seat-to-model mapping is unrecorded, so the judge-family rule (SKILL.md:215-216) and Step 7b's cross-family claim are unfalsifiable after the fact.
  4. **No replay enforcement** — nothing re-runs the selector against `prompts/selection.json` or recomputes the verdict from `ruling-set@1`; the replay record is written, never checked.
  5. At standard depth there is no governance-lawyer seat (`select_lenses.py:299-300`), so the default run has no process-conformance review of any kind.

"Decisively verified" would require: hash-chained run artifacts, ledger lines carrying run-dir path + dossier hash + docket/independence modes + per-seat model identity, and one mechanical post-run check (selector re-run + verdict recomputation from the ruling set). All of it is cheap; none of it exists.

---

## VERDICT SECTION

**The operator's four adjectives:**

- **Trusted — partial.** Sound doctrine (gate, tiers, shadow semantics, fail-closed oracles) + battery-proven arbitrator, but per-run enforcement of the gate, [H]-zero-weight, and oracle adequacy is LLM self-discipline; panel/generator sides uncertified; judge-family separation is "when configurable" and unrecorded. *Decisive evidence: SKILL.md:347-348 (gate has no code), select_lenses.py:299-300 (no process gate at standard depth), results-2026-07-17.md:68-76 (scope is one seat).*
- **Efficiently understood — solid (minor rot).** 46-line summary, tight vocabulary, mandatory GO coverage statement; template enum missing UPHELD-WITH-QUALIFICATIONS (synthesis-template.md:36 vs lens-registry.md:47-48).
- **Effectively implemented — partial.** CONDITIONAL conditions are prose despite structured acceptance-criteria/next-action fields existing in ruling-set@1; NO-GO path is clear. *Evidence: synthesis-template.md:17,40-43 vs lens-registry.md:44-49.*
- **Decisively verified — gap.** Runs are replayable in principle but not auditable in fact: no hash chain, no run-dir/dossier reference or docket/independence modes or model identity in the ledger schema (runs/README.md:17-38 vs SKILL.md:363), no replay enforcement, no process gate at default depth.

**The lens questions:**

- **Sufficient — partial.** 62 live evaluators across 19 families, but four singleton families, thin constructive stance (15), and migration/cutover/restore/IP coverage frozen behind a never-run admission gate (lens-registry.md:89).
- **Proper — solid.** Distinctness standard with teeth ("persona flavor is not novelty", lens-registry.md:12), enforced merges, neighbor boundaries on every sampled card, sound lifecycle with review-trigger (not auto-action) thresholds (lens-registry.md:75-79).
- **Well-defined — solid.** 23-field fingerprints, structured falsifier templates, output contracts; the neighbors/boundary edges are best-in-class.
- **Substantial — partial (leaning solid).** ~80% of sampled cards define real, differentiated attack methods with executable falsifiers; framing-epistemics (the largest family) skews to "method: analysis" horoscope-adjacent falsifiers (polymath-inquisitor, ecological-systems-analyst the thinnest).
- **Right combinations — gap (honestly documented in code, overstated in docs).** Fit scoring is frozen as no-better-than-random (select_lenses.py:64-67); task-fit rides on gates + specialist seed + 172-string uncontrolled domain vocabulary; contraindication "gate" claimed in SKILL.md:178 doesn't exist in code; live runs seated angry-customer on a firewall change and missed both economics lenses on a $120k spend decision.

**Minimal gap-closing set (each one focused PR, floors not ceilings):**

1. **Selector re-verification script** (~60 lines): given a run directory, re-run the selector against `prompts/selection.json` and re-derive GO/CONDITIONAL/NO-GO from `ruling-set@1`'s P1/P2 fields; hard-fail on mismatch. Converts "computed verdict" from doctrine to check. Closes most of the decisive-verification gap.
2. **Ledger schema v2 + backfill-free append**: add `run_dir`, `dossier_sha256`, `docket_mode`, `independence_mode`, per-lens `model` field to `runs/README.md` schema and the Step 9 checklist. Brings the schema up to what SKILL.md:363 already mandates.
3. **Domain vocabulary normalization**: add a controlled `domain_aliases` map (or canonicalize to ~40 terms) in registry + selector so `finance`/`cost`/`spend` and `ux`/`accessibility` intersect; re-run the 1000-fixture self-test. This is the cheapest real task-fit improvement available while the fit layer stays frozen — it strengthens the *gates and specialist seed*, which are the parts that demonstrably work.
4. **Doc honesty pass**: SKILL.md Step 4 gains one sentence stating the fit layer is frozen as unproven (mirroring select_lenses.py:64-67) and corrects "gates by … contraindications" to describe the score-penalty reality — or, if contraindication gating is intended, a 5-line selector change promoting hard contraindications to `eligible_evaluators`. Pick one; currently they diverge.
5. **Synthesis template: machine-readable conditions block** — CONDITIONAL emits a fenced JSON array of `{condition, falsifier{method,threshold,timeframe}, owner}` lifted from ruling-set@1 acceptance criteria; add UPHELD-WITH-QUALIFICATIONS to the ruling enum; s/Consensus Result/Computed Verdict/. Makes conditions consumable and fixes the vocabulary drift.
6. **Admission-gate ignition**: run the paired-blind behavioral admission for the 5 probation + the migration/release/IP candidate cluster first (they cover the demonstrable subject-class holes), using the existing shadow-seat telemetry format. This is the only item that isn't small in execution, but it's the single highest-leverage sufficiency fix and the machinery (battery harness, shadow seat, thresholds) already exists — it's a run, not a build.

**Bottom line:** the gauntlet's *design* is properly set up — registry model, lifecycle, constraints, and evidence doctrine are professional-grade and unusually self-honest. Its *results* are not yet fully trustworthy or decisively verifiable, for a simple reason: the certification and telemetry machinery has been built pointed at the arbitrator and the selector's constraint surface, but not yet at the panel's actual diagnostic yield or the individual run's artifact chain. The fixes above are all floors — none requires the unbuilt Phase 1–3 roadmap work.
