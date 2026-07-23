# 07 — Prior v2.6.0 findings reconciliation

## Scope and method

The prior collection audit under `docs/audits/2026-07-22-collection-audit/` is evidence about version 2.6.0, not authority over version 2.9.1. Each relevant finding below was re-anchored to packet commit `9532a57199fc8d4747a91916d59d1ea86c34d838` and classified only as `FIXED`, `OPEN`, `CHANGED`, or `OBSOLETE`.

- **FIXED** — current source/tests directly close the earlier defect.
- **OPEN** — the defect or evidence gap still matters.
- **CHANGED** — the architecture/contract moved; the old formulation no longer maps one-to-one, but a residual remains or the proof obligation differs.
- **OBSOLETE** — the earlier finding no longer applies to the current architecture or was explicitly rejected by current design.

## 01 — Router and Helix audit

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Router lacked a durable four-field route/skip record. | `FIXED` | `using-epistemic-skills/SKILL.md` now requires route, reason, order, and artifact/skip record; flexibility fixtures cover trace shape. |
| Router handoffs were prose-only and underspecified. | `FIXED` | Canonical consumes/produces/handoff table and receipt envelope define artifact coordinates, validity, and re-fire. |
| Missing member skill could be silently ignored. | `FIXED` | Router stop condition forbids pretending a missing skill ran and requires explicit degradation/blocking. |
| Discipline count/family resemblance was inconsistent. | `FIXED` | Router and README consistently define nine disciplines plus router/Helix; integration checks assert counts. |
| Helix was difficult to discover as the tandem entry point. | `FIXED` | README, GEMINI context, router, and Helix frontmatter all name the workflow/epistemic pairing role. |
| Helix had no explicit skip-reason floor. | `FIXED` | Helix co-fire checklist and router skip records require explicit non-use reasoning. |
| Helix could over-trigger as a universal workflow wrapper. | `CHANGED` | Current frontmatter narrows it to coexistence/ambiguity between layers; live auto-trigger precision remains unmeasured. |
| Router/Helix audit trail might disappear after the turn. | `CHANGED` | Artifact pointers and decision ledger supply persistence when consequential; no dedicated telemetry store is mandated. Completeness remains best-effort. |

## 02 — Blindspot and formal-rigor audit

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Blindspot skip gate was too subjective/easy to rationalize. | `FIXED` | Skip requires naming two concrete landmines plus the canonical example from memory; otherwise recon runs. |
| Recon could execute instructions found in unfamiliar content. | `FIXED` | Source-discovery step treats repository/external content as data, not authority; handoff repeats the injection boundary. |
| Blindspot could claim broad efficacy from self-authored examples. | `FIXED` | Current contract describes method/provenance without claiming measured general effectiveness; no rate is asserted. |
| Citation/attribution in blindspot provenance lacked mechanical verification. | `OPEN` | Provenance text exists, but no deterministic URL/quote verifier or live scholarly reception check was added. |
| Blast-radius quiz could become an orphaned optional appendix. | `CHANGED` | It remains a referenced bookend/check, while the main skill directly defines blast-radius questions. No independent behavioral proof exists. |
| Formal rigor lacked an auditable per-lens ledger. | `FIXED` | Current seven-lens battery requires every lens to be fired or explicitly marked not applicable with reason. |
| Formal inputs/assumptions were not pinned strongly enough. | `CHANGED` | Current method requires premises, alternatives, predictions, and falsifiers, but no universal machine-readable input-hash envelope exists. |
| Formal reasoning could substitute for empirical verification. | `FIXED` | Empirical claims remain conditional until preregistered test; this audit closed derivations with RED/GREEN CI. |
| Formal rigor could substitute for Gauntlet on high-impact decisions. | `FIXED` | Router/Helix distinguish derivation from adversarial gate; final Gauntlet remains separately required. |

## 03 — Evidence research and write-goal audit

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Consensus first contact and schema inspection were underspecified. | `FIXED` | Evidence-research has explicit first-contact profiles and requires inspecting live schemas before use. |
| Scite reception/retraction layer could be skipped after discovery. | `FIXED` | Triad contract requires discovery, reception, and durable holdings; missing layer must be disclosed. |
| Zotero/holdings behavior lacked an explicit durable-library boundary. | `FIXED` | Current skill defines holdings-check, deposit, and explicit LOCAL/Web API/server identification. |
| Research run record was too large or too coupled to one tool response. | `CHANGED` | Compact claim matrix/reception/holdings/convergence outputs are defined, but no live connector run was available here to validate ergonomics. |
| `OPERATOR_PENDING` and blocked closure paths were ambiguous. | `FIXED` | Current convergence vocabulary distinguishes hold, bounded probe, escalation, operator pending, and stop. |
| Research could emit a product/merge verdict. | `FIXED` | Boundary explicitly forbids GO/NO-GO; Gauntlet consumes evidence and owns verdict computation. |
| Live Scite rate limits/error semantics were unverified. | `OPEN` | No live Scite schema/call occurred in this target. |
| LOCAL durable-library overlay lacked a verified concrete example. | `OPEN` | Contract names the mechanism; no target-local library integration was available. |
| Write-goal approval provenance was weak. | `OPEN` | Current skill requires explicit approval and authority, but no live host consent primitive or signed approval artifact was exercised. |
| Inbound evidence/proof-bundle shape was underspecified. | `CHANGED` | Goal types, direct proof, anti-proxy guard, provenance, blocker and stop rules are now explicit; no shared machine verifier covers all goal types. |
| Research basis for goal authoring lacked reception/holdings validation. | `OPEN` | Source cites a research basis, but this audit could not execute the Consensus/Scite/library triad. |
| Goal authoring could silently start execution. | `FIXED` | Skill ends at approved contract/host adapter and never executes or certifies completion; absent primitive is disclosed. |

## 04 — Gauntlet audit

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Roster/count claims were inconsistent. | `FIXED` | Registry/selector tests reconcile the 102-persona roster and role bindings. |
| Selector/replay evidence was incomplete. | `FIXED` | Deterministic selection record, seed/candidate set, replay checks, and verifier tests are shipped. |
| Missing evals/dead documentation pointers weakened auditability. | `FIXED` | Current SKILL/references/scripts/tests and the committed exemplar are internally linked; deterministic suite checks them. |
| Shadow/required-lens failure could fail open. | `FIXED` | Required role/report/evidence failures block finalization; shadow handling is explicit. |
| Run manifest and frozen-subject integrity were weak. | `FIXED` | Subject hash, role materialization hashes, selection, report evidence, arbitration, and run verification are first-class. |
| Evidence roots/path checks were not mechanical enough. | `FIXED` | Evidence verifier and `[V path:line]` checks are deterministic and tested. |
| Arbitrator identity/certification was under-specified. | `FIXED` | Certified-arbitrator battery, certification artifact, and verifier checks exist. |
| Model/harness identity fields were missing. | `FIXED` | Current run records/role bindings carry actual model/harness/degradation metadata. |
| Final verdict could be hand-authored rather than computed. | `FIXED` | Finalizer computes vocabulary/result from verified reports and arbitration; run verifier rechecks. |
| Full 24×4 behavioral battery was missing. | `OPEN` | README still states only a smoke subset; full sweep remains design work. |
| Judgment truth/oracle adequacy was inferred from mechanical validity. | `OPEN` | Mechanical verifier cannot establish that lenses found all material defects or that oracle labels generalize. |
| Role independence across proprietary harnesses was assumed. | `CHANGED` | Contract now stops without isolated native/materialized-role dispatch, but this target could not execute it. |

## 05 — Evidence-locked UAT audit

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Limitations were duplicated/inconsistent across docs. | `FIXED` | Current SKILL centralizes environment/role/judge boundaries and strict verdict vocabulary. |
| Judge depended on non-portable tooling. | `FIXED` | `scripts/judge.py` is stdlib-only and its self-test runs in CI. |
| Missing preview could be rounded into code-reading acceptance. | `FIXED` | No reachable rendered environment forces `BLOCKED_ENVIRONMENT`; source inspection cannot substitute. |
| Evidence honesty fields were prose-only. | `FIXED` | Schemas/manifests and deterministic judge enforce case/evidence/verifier/result structure. |
| Evidence integrity lacked a hash chain. | `FIXED` | Current packet/manifest contracts include evidence hashes and immutable first-run handling. |
| Seeded calibration/negative-control breadth was too small. | `OPEN` | Judge self-tests prove planted cases, not broad actor/verifier behavioral quality. |
| Same-provider contexts might not be meaningfully independent. | `OPEN` | Contract requires separation and disclosure; no independent actor/verifier contexts were available here. |
| Fail-then-pass evidence could hide flakiness. | `FIXED` | First run is immutable; fail-then-pass is `FLAKY`, not silently PASS. |

## 06 — Gap analysis

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| No resumption discipline existed. | `FIXED` | `continuity-verify` now ships with state-digest contract, acceptance authority, ledger walk, and blinded smoke battery. |
| No durable consequential-decision persistence existed. | `FIXED` | `decision-ledger` now ships schema, supersedes chain, validator, and examples. |
| A separate telemetry-reader skill might be needed. | `OBSOLETE` | Current architecture deliberately uses router traces, receipts, ledgers, and audit artifacts rather than adding an always-on telemetry discipline. |
| Claim-tiering needed a new standalone skill. | `OBSOLETE` | Current flexibility controls embed claim/source/authority distinctions across existing skills; not another trigger. Measurement quality remains open. |
| Cross-skill receipts/validity were absent. | `FIXED` | Shared receipt envelope, validity predicates, staleness, and never-attests boundary now exist. |
| Timing/re-fire semantics were fragmented. | `FIXED` | Continuity, receipt validity, Helix positions, and explicit stop/re-fire rules cover the main transitions. |

## 07 — Helix/Superpowers alignment review

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| First parallel fan-out lacked a blindspot pairing. | `FIXED` | Helix maps reconnaissance before first dispatch/subagent fan-out. |
| Receiving review lacked formal-rigor pairing. | `FIXED` | Helix maps design/correctness claims in received feedback to formal rigor. |
| Pairing positions were ambiguous. | `FIXED` | Helix uses before/inside/cross-cutting/approval/pre-merge/is positions. |
| Cross-cutting evidence research and ledger behavior were unclear. | `FIXED` | Helix and router distinguish stage pairings from cross-cutting disciplines. |
| Co-fire checklist/skip accounting was incomplete. | `FIXED` | Current checklist and router stamps require trigger and non-use records. |
| Kimi goal-anchor/adaptation was missing. | `FIXED` | Write-goal names the Kimi lineage and adapter boundary; Kimi manifest maps tools. |
| Cron/scheduled-work adapter was absent. | `OPEN` | No dedicated cron harness mapping or live scheduled-run test exists; outside this packet's minimal fixes. |
| Superpowers precedence conflicted with Helix ordering. | `CHANGED` | `03` resolves layers: discover routers/process first, then epistemic member first inside a matched stage. Live co-fire behavior remains source-only. |

## 08 — Gauntlet lens/verdict deep dive

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Verdict integrity was not independently re-verified. | `FIXED` | Finalizer plus run verifier independently check computed verdict inputs and frozen-subject coordinates. |
| Behavioral efficacy was inferred from structural validity. | `OPEN` | Full behavioral sweep and real-defect rate remain absent. |
| Oracle adequacy/label truth was under-justified. | `OPEN` | Certified planted defects support narrow claims only; no universal truth oracle exists. |
| Lens-family independence/separation was weak. | `CHANGED` | Registry families, role binding, conflict ledger, and isolated-context contract improve separation; model/provider correlation remains open. |
| Alias/name drift could change selection identity. | `FIXED` | Registry/selector tests bind canonical IDs and replayable selection. |
| Candidate cards were uneven/thin. | `OPEN` | Large registry exists, but no current completeness/quality benchmark for every persona card is committed. |
| Fit layer could overclaim statistical optimization. | `FIXED` | Deterministic selection/fit records are treated as reproducibility machinery, not proof of optimal review quality. |
| Conflict resolution could erase dissent. | `FIXED` | Conflict Ledger and arbitration preserve unresolved dissent and encode conditionality. |
| Required vs shadow roles were blurred. | `FIXED` | Current contracts distinguish required panel evidence from shadow/optional contributions. |
| A valid run could survive subject movement. | `FIXED` | Frozen hash/verification invalidates moved subjects; this audit stopped rather than patching a nonexistent verdict. |

## 09 — Arc timing model

| Prior finding | Current status | Packet-commit evidence and residual |
|---|---|---|
| Evidence research lacked escalation/convergence timing. | `FIXED` | Current convergence states and escalation rules define when to continue, hold, probe, ask, or stop. |
| Formal rigor vs research order was ambiguous. | `FIXED` | Router/Helix place derivation and scholarly premise grounding according to the claim; evidence does not own design verdict. |
| Artifact validity/staleness was implicit. | `FIXED` | Shared receipt contract defines `valid_while`, stale handling, and never-attests boundary. |
| Resumption happened after work had already restarted. | `FIXED` | Continuity fires first on handoff/summary-dependent resumption. |
| Persistence timing was treated as a single arc stage. | `FIXED` | Decision ledger is cross-cutting and appends after consequential moments; readers re-anchor later. |
| External relay could bear load before durable recording. | `FIXED` | Outsource requires committed packet and recorded relay before downstream reliance. |
| Acceptance and adversarial review timing could collapse. | `FIXED` | Gauntlet gates frozen decisions/pre-merge; UAT evaluates finished observable UI; each has separate stop conditions. |
| Timing behavior had no broad live measurement. | `OPEN` | Current fixtures and this trace test contract conformance, not population-level timing precision. |

## Current-version findings not present in v2.6.0

| New finding | Status at audit branch |
|---|---|
| `GEMINI.md` still described eight packages / six disciplines after the suite grew to eleven/nine. | **FIXED test-first**; see `08`. |
| README layout comment said “canonical skill cores (ten)” while eleven skill directories exist. | **FIXED test-first**; see `08`. |
| Canonical CI omitted continuity committed-result scoring and DCO unit tests despite the handoff's full-suite claim. | **FIXED test-first**; see `08`. |
| No target primitive for isolated Gauntlet/UAT roles. | **OPEN capability gap**; see blocked run and `05`. |
| No proprietary harness, scholarly triad, or rendered UI runtime. | **OPEN validation gaps**, explicitly tiered in `06`. |

## Reconciliation conclusion

The v2.6.0 audit drove substantial current architecture: shared receipts, trace/skip discipline, continuity, decision persistence, stronger Gauntlet finalization, and fail-closed UAT are now present. Remaining risk is concentrated less in missing prose contracts and more in **behavioral truth**: live trigger precision, independent role execution, broad Gauntlet/UAT efficacy, connector behavior, and real-world rates.
