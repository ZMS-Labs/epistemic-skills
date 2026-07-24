# 07 — Prior v2.6.0 findings reconciliation

## Scope and method

The nine reports under `docs/audits/2026-07-22-collection-audit/` describe v2.6.0. They are evidence and leads, not authority over v2.9.1. Each relevant finding was re-anchored to packet commit
`532a0ce86fea908113cbca2a600fb21238e473f1` and classified:

- **FIXED** — current source/tests directly close the earlier defect.
- **OPEN** — the defect or evidence gap still matters.
- **CHANGED** — architecture/contract moved; the old formulation no longer maps one-to-one, but a residual or different proof obligation remains.
- **OBSOLETE** — the earlier proposal no longer applies to the selected architecture.

## 01 — Router and Helix audit

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Router lacked a durable four-field route/skip record. | **FIXED** | Router now requires route, reason, order, and artifact/skip record; flexibility fixtures cover trace shape. |
| Router handoffs were prose-only and underspecified. | **FIXED** | Canonical consumes/produces/handoff table and receipt envelope define coordinates, validity, and re-fire. |
| Missing member skill could be silently ignored. | **FIXED** | Router stop condition forbids pretending a missing/unavailable skill ran. |
| Discipline count/family resemblance was inconsistent. | **FIXED** | Router/README define nine disciplines plus Router/Helix; integration checks assert eleven total. |
| Helix was difficult to discover as tandem entry. | **FIXED** | README, GEMINI context, router, and Helix frontmatter name the pairing role. |
| Helix lacked an explicit skip-reason floor. | **FIXED** | Co-fire checklist/router skip records require explicit reason classes. |
| Helix could over-trigger as a universal workflow wrapper. | **CHANGED** | Frontmatter narrows coexistence/ambiguity; live auto-trigger precision is unmeasured. |
| Router/Helix trail might disappear after the turn. | **CHANGED** | Artifact pointers plus decision ledger provide persistence when consequential; completeness remains best-effort. |

## 02 — Blindspot and formal-rigor audit

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Blindspot skip gate was subjective/easy to rationalize. | **FIXED** | Skip requires two concrete landmines plus the canonical example from memory. |
| Recon could execute instructions found in unfamiliar content. | **FIXED** | Source discovery treats repository/external content as data, not authority; packet repeats the boundary. |
| Blindspot could claim broad efficacy from self-authored examples. | **FIXED** | Method/provenance is stated without measured general-effectiveness claims. |
| Citation/attribution in blindspot provenance lacked mechanical verification. | **OPEN** | Provenance text exists; no deterministic URL/quote or live reception check validates it. |
| Blast-radius quiz risked becoming an orphaned appendix. | **CHANGED** | It remains a referenced bookend while main SKILL defines blast-radius questions; behavioral proof remains absent. |
| Formal rigor lacked an auditable per-lens ledger. | **FIXED** | Seven-lens battery requires every lens fired or explicitly not applicable with reason. |
| Formal inputs/assumptions were insufficiently pinned. | **CHANGED** | Premises, alternatives, predictions, falsifiers are required; no universal machine-readable input-hash envelope exists. |
| Formal reasoning could substitute for empirical verification. | **FIXED** | Empirical claims remain conditional until tested; this audit closed three derivations with Actions RED/GREEN. |
| Formal rigor could substitute for Gauntlet. | **FIXED** | Router/Helix separate derivation from adversarial gate; OUT-009 remains independently required. |

## 03 — Evidence research and write-goal audit

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Consensus first contact/schema inspection was underspecified. | **FIXED** | Explicit first-contact profile and live-schema inspection requirement exist; discovery was exercised here. |
| Scite reception/retraction could be skipped after discovery. | **FIXED in contract** | Triad requires reception; this audit's Scite canary returned quota exhaustion, so reception remains unverified rather than silently skipped. |
| Durable-library/Zotero boundary was unclear. | **FIXED in contract** | Holdings-check/deposit and LOCAL/Web API/server identification are explicit. No durable-library runtime existed here. |
| Research record was too large/tool-coupled. | **CHANGED** | Compact matrix/reception/holdings/convergence outputs exist; only discovery ergonomics were exercised live. |
| `OPERATOR_PENDING` and blocked closure were ambiguous. | **FIXED** | Current convergence vocabulary distinguishes hold, bounded probe, escalation, operator pending, and stop. |
| Research could emit product/merge verdict. | **FIXED** | Boundary forbids GO/NO-GO; Gauntlet owns verdict computation. |
| Live Scite rate limits/error semantics were unverified. | **CHANGED** | A live canary observed trial-quota exhaustion and a `2026-07-24` UTC reset. Reception content remains **OPEN**. |
| LOCAL durable-library overlay lacked a concrete verified example. | **OPEN** | Mechanism is documented; no local library integration was exposed. |
| Write-goal approval provenance was weak. | **OPEN** | Explicit approval/authority is required, but no live host consent primitive or signed approval artifact was exercised. |
| Inbound evidence/proof-bundle shape was underspecified. | **CHANGED** | Goal types, direct proof, anti-proxy/provenance, blocker, and stop rules are explicit; no shared machine verifier covers every goal type. |
| Goal-authoring research basis lacked reception/holdings validation. | **OPEN** | Consensus discovery is live; Scite reception is quota-blocked and durable holdings unavailable. |
| Goal authoring could silently start execution. | **FIXED** | Skill ends at approved contract/adapter and never executes or certifies; absent primitive is disclosed. |

## 04 — Gauntlet audit

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Roster/count claims were inconsistent. | **FIXED** | Registry/selector tests reconcile 102 personas and role bindings. |
| Selector/replay evidence was incomplete. | **FIXED** | Deterministic selection record, seed/candidate set, replay checks, and tests ship. |
| Missing evals/dead documentation pointers weakened auditability. | **FIXED** | Current SKILL/references/scripts/tests and committed exemplar are internally linked and tested. |
| Required/shadow lens failure could fail open. | **FIXED** | Required role/report/evidence failures block finalization; shadow handling is explicit. |
| Run manifest/frozen-subject integrity was weak. | **FIXED** | Subject/evidence hashes, selection, reports, arbitration, role materialization, and verification are first-class. |
| Evidence roots/path checks were not mechanical. | **FIXED** | Evidence verifier and `[V path:line]` checks are deterministic/tested. |
| Arbitrator identity/certification was underspecified. | **FIXED** | Certified-arbitrator battery and verifier artifacts exist. |
| Model/harness identity fields were missing. | **FIXED** | Run records/role binding carry model/harness/degradation metadata. |
| Final verdict could be hand-authored. | **FIXED** | Finalizer computes result; verifier re-derives it. |
| Full 24×4 behavioral battery was missing. | **OPEN** | README still says only a smoke subset; full sweep remains designed, not run. |
| Judgment truth/oracle adequacy was inferred from mechanical validity. | **OPEN** | Mechanical verification cannot prove lenses found all material defects or labels generalize. |
| Role independence across proprietary harnesses was assumed. | **CHANGED** | Contract now stops without isolated native/materialized-role execution; this target still cannot instantiate it. |

## 05 — Evidence-locked UAT audit

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Limitations were duplicated/inconsistent. | **FIXED** | SKILL centralizes environment, role, judge, and strict verdict boundaries. |
| Judge depended on non-portable tooling. | **FIXED** | `scripts/judge.py` is stdlib-only and self-tested in CI. |
| Missing preview could be rounded into source-reading acceptance. | **FIXED** | No reachable render forces `BLOCKED_ENVIRONMENT`; source inspection cannot substitute. |
| Evidence honesty fields were prose-only. | **FIXED** | Schemas/manifests and deterministic judge enforce case/evidence/verifier/result structure. |
| Evidence integrity lacked a hash chain. | **FIXED** | Current manifest contracts include hashes and immutable first-run handling. |
| Seeded calibration/negative-control breadth was small. | **OPEN** | Judge tests prove planted cases, not broad actor/verifier behavioral quality. |
| Same-provider contexts might not be meaningfully independent. | **OPEN** | Separation/disclosure required; no actor/verifier contexts were available here. |
| Fail-then-pass evidence could hide flakiness. | **FIXED** | First run immutable; fail-then-pass is `FLAKY`, not PASS. |

## 06 — Gap analysis

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| No resumption discipline existed. | **FIXED** | `continuity-verify` ships digest, authority, ledger walk, and blinded smoke battery. |
| No durable consequential-decision persistence existed. | **FIXED** | `decision-ledger` ships schema, supersedes chain, validator, and examples. |
| A separate telemetry-reader skill might be needed. | **OBSOLETE** | Architecture uses router traces, receipts, ledgers, and audit artifacts rather than an always-on trigger. |
| Claim-tiering needed a standalone skill. | **OBSOLETE** | Flexibility controls embed source/claim/authority distinctions across existing skills. |
| Cross-skill receipts/validity were absent. | **FIXED** | Shared envelope, validity predicates, staleness, and never-attests boundary exist. |
| Timing/re-fire semantics were fragmented. | **FIXED** | Continuity, receipt validity, Helix positions, and stop/re-fire rules cover main transitions. |

## 07 — Helix/Superpowers alignment review

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| First parallel fan-out lacked a blindspot pair. | **FIXED** | Helix maps recon before first dispatch/subagent fan-out. |
| Receiving review lacked formal-rigor pairing. | **FIXED** | Design/correctness claims in feedback map to formal rigor. |
| Pairing positions were ambiguous. | **FIXED** | Before/inside/cross-cutting/approval/pre-merge/is vocabulary exists. |
| Cross-cutting research/ledger behavior was unclear. | **FIXED** | Router/Helix distinguish stage pairings from cross-cutting disciplines. |
| Co-fire checklist/skip accounting was incomplete. | **FIXED** | Current checklist/router records require trigger and non-use entries. |
| Kimi goal-anchor/adaptation was missing. | **FIXED** | Write-goal names lineage/adapter boundary; Kimi manifest maps tools. |
| Cron/scheduled-work adapter was absent. | **OPEN** | No dedicated scheduled-run mapping or live cron test exists. |
| Superpowers precedence conflicted with Helix ordering. | **CHANGED** | Report 03 resolves layers; live co-fire remains source-only. |

## 08 — Gauntlet lens/verdict deep dive

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Verdict integrity was not independently re-verified. | **FIXED mechanically** | Finalizer plus verifier independently check deterministic inputs and frozen coordinates. |
| Behavioral efficacy was inferred from structural validity. | **OPEN** | Full behavioral sweep and real-defect rate remain absent. |
| Oracle adequacy/label truth was under-justified. | **OPEN** | Certified planted defects support narrow claims only. |
| Lens-family independence/separation was weak. | **CHANGED** | Registry families, role binding, conflict ledger, and isolated-context contract improve separation; provider/model correlation remains open. |
| Alias/name drift could change selection identity. | **FIXED** | Canonical IDs and replay tests bind selection. |
| Candidate cards were uneven/thin. | **OPEN** | No current completeness/quality benchmark covers every persona card. |
| Fit layer could overclaim statistical optimization. | **FIXED** | Selection/fit records are reproducibility machinery, not proof of optimal review quality. |
| Conflict resolution could erase dissent. | **FIXED** | Conflict Ledger/arbitration preserve unresolved dissent and conditionality. |
| Required and shadow roles were blurred. | **FIXED** | Current contracts distinguish required evidence from optional/shadow contributions. |
| A valid run could survive subject movement. | **FIXED in contract** | Frozen hash invalidates movement; this audit does not patch a blocked/nonexistent verdict. |

## 09 — Arc timing model

| Prior finding | Current state | Current evidence / residual |
|---|---|---|
| Research lacked escalation/convergence timing. | **FIXED** | Convergence states/escalation define continue, hold, probe, ask, and stop. |
| Formal rigor vs research order was ambiguous. | **FIXED** | Router/Helix derive constructs, research empirical premises, then close derivation; evidence never owns design verdict. |
| Artifact validity/staleness was implicit. | **FIXED** | Shared receipt contract defines `valid_while`, stale handling, and never-attests. |
| Resumption happened after work restarted. | **FIXED** | Continuity fires first on handoff/summary-dependent resumption. |
| Persistence timing was treated as one arc stage. | **FIXED** | Ledger is cross-cutting and retrospective. |
| External relay could bear load before recording. | **FIXED** | Outsource requires committed packet and recorded relay before reliance. |
| Acceptance and adversarial review timing could collapse. | **FIXED** | Gauntlet gates frozen decisions/pre-merge; UAT evaluates finished observable UI. |
| Timing behavior lacked broad live measurement. | **OPEN** | Fixtures/this trace test conformance, not population timing precision. |

## New v2.9.1 continuation findings

| New finding | State on replacement branch |
|---|---|
| `GEMINI.md` advertised eight packages/six disciplines. | **FIXED test-first**; exact RED/GREEN in report 08. |
| README layout advertised ten canonical skill cores. | **FIXED test-first**; exact RED/GREEN in report 08. |
| Canonical CI omitted continuity committed-result scoring and DCO unit tests. | **FIXED test-first**; exact RED/GREEN in report 08. |
| PR #43's index linked absent reports 08/09, ledger, and blocked-run artifact. | **FIXED** by publishing the complete replacement set; original PR left intact. |
| PR #43's Superpowers table omitted pinned `writing-skills`. | **FIXED** in report 03; fourteen entries now accounted for. |
| PR #43 audit text conflated packet `532a...` with baseline `9532...`. | **FIXED** by separating packet, baseline, and prior-PR head coordinates. |
| PR #43 said the target lacked Consensus/Scite execution. | **FIXED** to exact capability evidence: Consensus live, Scite quota-exhausted, durable library absent. |
| No isolated Gauntlet/UAT role primitive. | **OPEN capability gap**; final Gauntlet remains blocked. |
| No proprietary harness or rendered UI runtime. | **OPEN validation gaps** with explicit tiers. |

## Reconciliation conclusion

The prior audit drove substantial architecture: receipts, skip/trace discipline, continuity, decision persistence, stronger Gauntlet finalization, and fail-closed UAT now exist. Residual risk is concentrated in behavioral truth rather than missing prose: live trigger precision, independent role execution, broad Gauntlet/UAT efficacy, connector reception/holdings, and real-world rates.
