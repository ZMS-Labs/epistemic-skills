# Skill trust contracts + timing layer — design

**Date:** 2026-07-22
**Status:** v2 — amended after gauntlet run `trust-contract-design-2026-07-22`
(verdict: NO-GO as-written, 2 P1 findings; amended per the run's arbitration,
including its 15 conditions). The run's artifacts live under local-only
`outputs/` and are deliberately uncommitted; the run is cited by name and date,
not by repo path.
**Type:** Cross-cutting mechanism (artifact standard + verifier) plus per-skill emit/consume edits
**Basis:** nine-part audit of the collection at v2.6.0 (per-skill audits ×5, gap analysis, helix alignment review, gauntlet lens/verdict deep-dive, arc timing model). Findings cited by file:line throughout the audit reports; this doc records only the decisions and their derivations. The nine audit reports (or one consolidated doc with nine sections) are committed at PR-B1 under `docs/audits/2026-07-22-collection-audit/` with a synthesis index, so every constraint this design creates keeps its reasons recoverable.

## Problem

1. **Handoffs are prose.** The router's Consumes/Produces/Hands-to table
   (`using-epistemic-skills/SKILL.md:21-28`) names each skill's output but not its
   shape. Downstream skills cannot mechanically verify they received a well-formed
   input; every consuming step re-interrogates the session or re-runs checks.
2. **Checks are genuinely duplicated across skills** — blindspot-pass live-verifies
   premises that gauntlet Step 0 re-verifies; citation anchoring is prose in
   blindspot-pass but mechanical in gauntlet (`verify_evidence.py`); write-goal's
   integrity guards restate gauntlet's oracle-adequacy doctrine. Some duplication is
   deliberate freshness design; some is pure waste. Nothing distinguishes the two.
3. **Timing is silent where the arc is not.** Research has a start trigger and a
   paper budget but no completion criterion (its own cap is declared epistemically
   void, `evidence-research/SKILL.md:147-148`); no escalation rule between research
   modes; formal-rigor and evidence-research cohabit the `decide` stage with no
   ordering; only gauntlet has a drift rule ("if the subject moves, restart",
   `gauntlet/SKILL.md:138`); recon, matrices, and goal contracts go stale silently.
4. **Gauntlet runs are replayable in principle but not auditable in fact** — no hash
   chain over run artifacts, the ledger schema cannot record `docket_mode` /
   `independence_mode` / model identity though SKILL.md:363 mandates recording them,
   and nothing mechanically re-checks a run's selector record or verdict.

## Decision (summary)

Ship a **handoff-receipt standard**: a small JSON schema (`handoff-receipt@1`), a
stdlib verifier (`contracts/verify_receipt.py`) in the established
`select_lenses.py`/`verify_evidence.py` pattern, and one-line emit/consume
references in each skill. A receipt is a producer **self-issued declaration** of
**identity, well-formedness, provenance, and a validity window** — never
verdict-truth, never independence, never freshness beyond its window. The
verifier certifies the envelope only — binding and well-formedness — not origin,
not the truth of self-reported fields. **"Trust" in this document means exactly
that envelope and nothing more**: no field and no rule raises a consumer's
confidence in a judgment it did not make or re-verify. Pair it with a **timing
layer**: a validity column in the router's handoff table, a research convergence
criterion and escalation triggers, one sentence resolving the formal-rigor ↔
research ordering, and a general drift rule. Close the gauntlet audit gap with a
content-addressed run record and a mechanical post-run re-check.

Explicitly rejected: a ninth "trust-contract skill" (no epistemic moment — it is
machinery, and the collection's trust-critical checks are already scripts invoked
by skills, never skills themselves); verdict-carrying trust (would industrialize
the exact guard-weakening defect found twice in the audit: helix's trigger
narrowing and skip-gate softening); harness-specific hooks (violates "one tree,
manifests only").

## The attestation boundary (the core fork, weighed)

**Options:** (A) verdict-carrying trust — downstream accepts upstream judgments;
(B) envelope trust — identity / well-formedness / provenance / validity window
only; (C) status quo prose.

Lens sweep (7 lenses enumerated; details where fired):

1. *Relational/normalization — n/a*: no stored relation; the anomaly analysis lives
   in lens 7 (same theory applied to artifacts).
2. *Transaction/concurrency — fired (weak)*: skills in a chain are sequential,
   not concurrent; no schedule anomalies. The useful import is the **snapshot**
   idea: gauntlet's freeze is a serialization point; receipts generalize it.
3. *Distributed/consistency — fired*: a skill chain is a replicated-read system.
   Verdicts are **non-monotonic** under new evidence; copying them downstream
   violates monotonic-read semantics — the copy cannot be invalidated when the
   basis changes. Envelope metadata (producer, subject hash, timestamp, validity
   predicates) is **monotonic** — safe to cache and forward. Session guarantees:
   a receipt is read-your-writes valid within (same session ∧ same subject
   revision); outside that window it downgrades one evidence tier.
4. *Complexity — n/a*: no asymptotic question; the verifier is O(receipt size).
5. *Type theory — fired*: **make illegal states unrepresentable.** Under (A) the
   illegal state — inherited, unearned confidence in a judgment the consumer never
   made — is representable and will be used. Under (B) the schema has no field
   capable of carrying a truth claim about another skill's judgment, so the
   illegal state is unrepresentable by construction **at the field level** — and
   the bounded downgrade rule (below) closes it at the rule level, excluding
   judgment-carrying kinds from downgrade consumption. This lens carries the most
   weight.
6. *Information theory — fired*: receipts bind artifacts by sha256 (collision
   resistance ≈ 2^128 birthday bound); a hash is an immutable coordinate, a path
   or version tag is not (it drifts). Matches the in-repo exemplars: selector
   replay record (registry sha256), `gauntlet-role-binding@1` (role/persona/
   dossier/prompt hashes), UAT `manifest.json` (sha256 of gate + contracts).
7. *Architecture formalisms — fired*: **SSOT / normalization-for-code.** (A)
   creates a derived copy of judgment in every consumer — an update anomaly with
   no propagation path. (B) stores only references; the producer's artifact stays
   the single source. Also **blast radius**: (B) is fully reversible (receipts are
   additive; a skill ignoring them degrades to today's behavior).

**Verdict: (B) envelope trust.** Concession: downstream freshness re-checks for
time-sensitive data (reception tallies, environment reachability) are *not*
eliminated — that cost was never safely removable. The saving is confined to
idempotent-mechanical checks: schema conformance, citation anchoring, hash
equality, run-order facts, consent facts. (A)'s one advantage — zero re-work
downstream — is unrecoverable safely; (C)'s advantage — zero mechanism — is kept
for skills whose outputs stay prose (the receipt is one stamped block, not a
pipeline).

## The mechanism

New directory `plugins/epistemic-skills/contracts/` (collection-level machinery,
harness-agnostic, one tree):

- `handoff-receipt.schema.json` — the schema below.
- `verify_receipt.py` — stdlib-only validator, single-carrier (JSON only; the
  prose stamp below is not parsed by the verifier). Given a receipt file (+
  artifact root), it checks: schema conformance; every referenced artifact's
  sha256 resolves; `valid_while` predicates are from the closed vocabulary; the
  `never_attests` field is present and non-empty; a receipt with null
  `subject.revision` does not carry `subject-revision-unchanged`. **Fails
  closed**: any miss → nonzero exit + named reason. It never evaluates whether
  the *judgment* in an artifact is right; it certifies the envelope only.
- `README.md` — the contract in one page: the never-attest list; the self-issued
  disclosure ("receipts are self-issued by the producer; the verifier certifies
  binding and well-formedness, not origin, not the truth of self-reported
  fields"); the committed-artifact boundary (below); the producer content pin or
  its written rationale; the downgrade derivation and regime precedence; and the
  closed-vocabulary extension procedure (predicates are added only by
  schema-version bump + verifier release in the same PR — unknown predicates
  fail closed by design, so a misfit blocks loudly and is never silently
  absorbed).

### `handoff-receipt@1`

```json
{
  "receipt": "handoff-receipt@1",
  "producer": { "skill": "blindspot-pass", "version": "2.6.0", "sha256": "<sha256 of the producer SKILL.md>" },
  "run": { "id": "<slug>-<YYYYMMDD>-<seq>", "at": "<YYYY-MM-DD>", "session": "<keyed-hash-or-null>" },
  "trigger": { "matched": "<closed trigger-class>", "skip_gate": "passed|fired|n/a" },
  "subject": { "ref": "<hash-or-closed-subject-class>", "revision": "<git-SHA|doc-version|null>", "sha256": "<of frozen subject artifact or null>" },
  "artifacts": [
    { "kind": "rewritten-request|derived-verdict|claim-evidence-matrix|goal-contract|dossier|gauntlet-run-record|uat-packet|routing-record",
      "path": "<relative-to-artifact-root>", "sha256": "..." }
  ],
  "valid_while": ["subject-revision-unchanged", "session-continuous", "freeze-window-open"],
  "coverage_limits": ["<what this run did NOT check, verbatim from the skill's own degradation labels>"],
  "never_attests": ["verdict-truth", "independence-achieved", "freshness-beyond-window"]
}
```

Rules:

- **`valid_while` is a closed vocabulary of predicates**, evaluated by the
  *consumer*, cheaply and mechanically. Each predicate is defined as (name,
  holder, evaluation-time truth condition):
  `subject-revision-unchanged` — holder: any receipt; true iff the recorded
  `subject.revision` equals the subject's current revision at consume time.
  `session-continuous` — holder: any receipt; true iff the receipt's `session`
  keyed hash equals the consumer's current-session keyed hash (equality only;
  the raw harness session id is never persisted).
  `freeze-window-open` — holder: gauntlet receipts; true iff the dossier
  identified by `subject.sha256` has had no controlled reopen recorded since the
  freeze timestamp in the run record. (The dossier freezes at Step 0, before any
  receipt is emitted — this predicate guards post-freeze amendment, not the
  freeze itself.)
  `environment-reachable` — holder: UAT receipts; true iff the target
  environment answers at consume time.
  A receipt whose predicates fail is not wrong — it is **stale**, and the
  consumer re-runs exactly the freshness-sensitive check, nothing else.
- **Null subjects fail closed.** A receipt or stamp with null `subject.revision`
  MUST NOT carry `subject-revision-unchanged`; the verifier rejects that
  combination (nonzero exit, named reason). A null `session` makes
  `session-continuous` unevaluable. Any predicate that is unevaluable for a
  subject defaults to **stale** — stale-by-default, never silently valid.
- **Bounded downgrade rule.** A receipt from a prior session, or whose envelope
  facts predate a revision change, is not discarded; its **envelope fields**
  (identity, well-formedness, provenance — run-order facts, hash equality,
  consent facts) downgrade one evidence tier (verified → dated inference),
  matching evidence-research's existing freshness semantics ("library notes
  without a live re-check are `[I]` at best when dated and DOI-keyed",
  `evidence-research/SKILL.md:260-263`). **Judgment-carrying kinds do not
  downgrade**: stale `derived-verdict`, dossier, and gate/verdict artifacts are
  ENVELOPE-ONLY — their judgment content may not be consumed at one tier down;
  it is re-verified or void. Only envelope fields survive staleness.
- **Regime precedence.** When the two staleness regimes overlap, the
  predicate-failure regime wins: a failed or unevaluable `valid_while` predicate
  means stale → re-run exactly the freshness-sensitive check (gauntlet's freeze
  semantics — "premises re-verified when stale" — outrank the downgrade rule).
  The downgrade applies only to envelope attestation when predicates are
  unevaluable or the only change is the session boundary.
- **Supersession.** For the same producer+subject, a later receipt supersedes
  every earlier one (the `run.id` sequence gives the total order); a superseded
  receipt is not consumed at all — not even downgraded. This is what the drift
  rule's re-fire produces: a new head, not a fork.
- **Carrier: JSON receipts for artifact producers, 4-field stamps for prose.**
  File-producing skills (gauntlet, UAT, evidence-research matrix, file-written
  goal contracts) emit JSON receipts verified by `verify_receipt.py`.
  Prose-producing skills (blindspot-pass, formal-rigor, write-goal, router)
  emit a 4-line stamp — `subject.ref`, `subject.revision`, `valid_while` (same
  closed vocabulary), `coverage_limits`; the producer is the emitting skill by
  construction. The stamp IS the prose carrier for lowest-common-denominator
  harnesses; the verifier never parses prose.
- **Privacy minimization (necessity-passed fields).** `run.session` is a per-run
  keyed hash (an equality token), never the raw harness session id. `run.at` is
  day-granularity — every `valid_while` predicate consumes date precision and
  none consumes finer. `trigger.matched` is a closed trigger-class vocabulary
  and `subject.ref` is hash-or-class: no verbatim user prose is hash-bound into
  permanent artifacts.

### Data axis: persistence and retention

Receipts and stamps have **validity windows, not retention guarantees**: a
receipt's purpose is consumed at the next skill step, and nothing may archive a
receipt past staleness. What persists, where, and why:

- **Committed (public repo):** the schema, verifier, README, synthetic example
  receipts, and one synthetic example run (marked `"example": true`). These
  carry no operator data by construction.
- **Committed, minimized:** ledger lines — the one live record in the public
  repo — carry the derived pointer projection only (`run_dir` ref,
  `dossier_sha256`, lifecycle counts); per-seat `model` persists at **family
  granularity**. Retention: indefinite, as lifecycle telemetry — public by
  design, because the lifecycle thresholds consume counts over the full history.
- **Local-only (never committed):** run directories, dossiers, live receipts
  over real subjects, and screenshot-class captures. `.gitignore` covers the run
  output roots (`outputs/` and equivalents); live run records may keep exact
  timestamps and per-seat model identity because they never leave the operator's
  machine.

Every persisted identifier, timestamp, and descriptor in the shipped schema and
ledger v2 has a named mechanical consumer and either a retention rule or an
explicit public-by-design justification; the private/public telemetry split
ships **with** ledger v2 (PR-B6), not after it.

## Per-skill changes (emit / consume)

Each is a few lines in the skill plus, where noted, a schema or script.

| Skill | Emits | Consumes |
|---|---|---|
| **router** | routing record line per firing decision (`router: fired=[...] skipped=[skill(trigger-absent)]`) + 4-field stamp | — |
| **blindspot-pass** | stamped report header: subject, territory revision, date, `premises-verified` list of (claim, file:line, how-verified) tuples + 4-field stamp | — |
| **applying-formal-rigor** | structured verdict footer: 7-line lens ledger, `facts:` list with revision/date, verdict line + 4-field stamp | blindspot header as input facts (re-verified only if stale) |
| **evidence-research** | `matrix.schema.json` pinning the already-mandated §9 columns; JSON receipt over the matrix (file producer); run record gains receipt fields | Zotero/Consensus/Scite capability facts within run |
| **write-goal** | optional structured header on both templates: goal type, three proof layers present-or-waived, boundaries, stop rule, `approval: {by, at}`; JSON receipt when the contract is file-written, 4-field stamp otherwise; inbound evidence/design inputs **referenced by id/path, never paraphrased** | upstream receipts bound by hash into the contract's provenance layer |
| **gauntlet** | `gauntlet-run-record@1` (below) + receipt; Step 0 consumes upstream receipts: **provenance/well-formedness accepted when valid, premises re-verified when stale** — freshness semantics preserved, never attested away | all upstream receipts |
| **evidence-locked-uat** | manifest.json gains normative schema (P1); receipt emitted over the packet | write-goal contracts, requirement sources |
| **helix** | `helix-check` line upgraded: `fired(<artifact-ref>) | skipped(<reason-class>: <evidence>)`, reason classes `trigger-absent | already-ran(<ref>) | operator-override` | — |

## Timing layer (from the arc timing model)

Each line below is an initial calibration from a one-day model, not doctrine —
so each carries a **revisit gate** (the repo's FROZEN-comment precedent: an
uncertain line names the condition under which it is re-examined).

1. **Router handoff table gains a "Valid until" column**, one line per skill;
   each cell cites the closed `valid_while` predicate IDs it maps to, not free
   prose (recon: `subject-revision-unchanged` + next-stage-start; verdict:
   `subject-revision-unchanged` on named inputs; matrix: `session-continuous` —
   reception `[V]`-grade this run only, snapshot dated; contract:
   `subject-revision-unchanged` on intent/scope/environment; dossier:
   `freeze-window-open`). *Revisit gate:* the first recorded field incident of
   staleness or over-freshness against a cell, or 30 committed runs after merge,
   whichever first.
2. **Research convergence criterion** (evidence-research, after §4): a run
   converges when the counterevidence and boundary-condition query families
   surface no new relevant DOIs beyond the mode's reception dial; terminal-state
   label required — `saturated` / `capped-by-budget` / `contested-stable` —
   porting formal-rigor lens 4's fixed-point rule. `capped-by-budget` becomes an
   honest label instead of a silent exit. (The minimal form — labels only, no
   longitudinal reception-stability requirement — is the floor.) *Revisit gate:*
   the first run that exits `capped-by-budget` twice on the same question
   family (the reception dial is miscalibrated), or the first recorded field
   incident of premature convergence.
3. **Escalation triggers** (evidence-research Modes section): escalate one mode
   when any of — a load-bearing paper is contested; the decision is
   high-stakes/irreversible; Consensus↔Scite cross-validation diverges on the core
   question; the synthesis must support a gauntlet dossier. *Revisit gate:* the
   first gauntlet dossier built on an un-escalated run (trigger too weak) or the
   first operator-overridden escalation (trigger too strong).
4. **Rigor ↔ research ordering** (router, one sentence): within `decide`, run
   formal-rigor's lens sweep first to name precise constructs and expose which
   premises are empirical; research exactly those premises; then complete the
   derivation with the verified matrix. If the empirical premise is the decision's
   whole basis, research may lead — the derivation still closes the stage.
   *Revisit gate:* the first recorded decide-stage re-fire loop between
   formal-rigor and research.
5. **General drift rule** (router, as shared invariant 6): if a skill's subject
   materially changes after it ran, its output is void and the skill re-fires at
   its own trigger — never patch the old output. The downstream consumer owns the
   re-fire check (generalizing gauntlet's "subject moves → restart" and matching
   how Step 0 already compensates for stale upstream input). *Revisit gate:* the
   first downstream consumption of a superseded receipt.

## Gauntlet verification set

1. **`gauntlet-run-record@1`** — one JSON manifest per run: dossier sha256 +
   freeze timestamp, subject path/revision, evidence-root content pin, selection
   replay hash, per-lens report hashes, fingerprint ref, ruling-set ref, verdict +
   structured conditions array, depth, `docket_mode`, `independence_mode`,
   `role_binding`, per-seat `model` (full identity — the run record is
   local-only; any committed projection carries model at family granularity).
   Produced by `scripts/finalize_run.py` (hashes files that already exist; adds
   nothing to the run itself).
2. **`scripts/verify_run.py`** — given a run directory: re-run the selector against
   `prompts/selection.json`, re-derive GO/CONDITIONAL/NO-GO from `ruling-set@1`'s
   P1/P2 fields, verify the hash chain dossier→reports→arbitration→summary.
   Hard-fail on mismatch. Converts "computed verdict" from doctrine to check.
3. **Ledger schema v2 — a derived pointer, not a second writable record.** The
   ledger line gains a content-addressed `run_dir` ref + `dossier_sha256`
   pointer; the overlapping facts (`docket_mode`, `independence_mode`, per-lens
   `model`, `dossier_sha256`) have exactly one writable home — the run record —
   and are **derived** into the ledger line by `finalize_run.py` in the same pass
   (or cross-checked hard-fail by `verify_run.py`), never dual-writable. The
   public projection carries per-lens `model` at family granularity. This brings
   the ledger up to what SKILL.md:363 mandates (record the modes — once), and
   the private/public telemetry split ships with this PR, not after.
   Schema-versioned append; no backfill.
4. **Domain vocabulary normalization** — a controlled `domain_aliases` map in the
   registry + selector so `finance`/`cost`/`spend`, `ux`/`accessibility`,
   `infra`/`operations`/`ops` intersect; re-run the 1000-fixture self-test. The
   cheapest real candidate task-fit improvement while the fit layer stays frozen —
   it strengthens the gates and specialist seed, whose *constraint satisfaction*
   is mechanically tested. Note: the 1000-fixture battery asserts constraint
   satisfaction, not fit — the repo's FROZEN note records no measured fit benefit
   over random fill. This item therefore carries a **fit-sensitive fixture
   check** (a fixture where the correct alias mapping changes the selected
   panel); the constraint battery alone cannot validate it.
5. **Synthesis template** — CONDITIONAL emits a fenced JSON conditions array
   `{condition, falsifier{method,threshold,timeframe}, owner}` lifted from
   `ruling-set@1` acceptance criteria (template currently `[enumerate]` prose).
6. **Evidence-root pin** — Step 1 establishes the evidence root as a content hash,
   not only a path, so `[V path:line]` verifications are hash-bound and their
   invalidation is detectable.

Deferred (named, not built): the behavioral admission-battery run for
probation/migration/release/IP lens clusters (machinery exists; it is a *run*,
operator-gated). (The private/public telemetry split was formerly deferred here;
it now ships WITH ledger v2 in PR-B6 — see the data-axis section.)

## UAT changes

1. Normative `manifest.json` schema in `schemas.md` (reconciling SKILL.md's field
   list; adds `skill_version`, judge-code hash, directive-required fingerprint
   fields).
2. Honesty fields move into the deterministic judge: `known_limitations` and
   `coverage_omitted` emitted by the gate object, not added procedurally (closes
   the fail-open where a forgetful orchestrator produces a clean-looking gate and
   the manifest then pins the incomplete artifact); target commit SHA added to
   `gate.json`.
3. Manifest hashes extended to committed `actor-output.json` and `verifier/*.json`;
   one explicit sentence: screenshots are gitignored and unhashed — outside the
   integrity chain.
4. "Verifying a packet downstream" section in `schemas.md`: a consumer MAY
   recompute `release_decision` from committed actor/verifier outputs with the
   deterministic aggregation rules — documents the trust hook that exists de
   facto.
5. Extract the judge from `workflow-template.mjs` into a standalone stdlib script
   any harness runs identically; the `.mjs` stays as reference orchestration.
6. `calibration_status` vocabulary + transition condition
   (`uncalibrated | calibrated:<corpus-ref>@<date>`); the missing seeded-defect
   corpus named as the blocker — a path, not a dead end. The corpus itself is NOT
   built here (ceiling, not floor).

## What this design does NOT do

- No verdict-carrying trust. The schema has no field for it, and the bounded
  downgrade rule extends no credit to judgment-carrying kinds — verdict-trust is
  inexpressible by the schema and the rules, not merely unrecommended.
- No attestation of independence (lens isolation, blinded verifier) — procedural
  properties are recorded as metadata (`independence_mode`), never certified.
- No new skill. The router, helix, and the six disciplines keep their boundaries;
  receipts ride on existing outputs.
- No harness hooks, no Workflow dependency, no per-harness forks.
- No maximal ritual: prose skills emit one 4-field stamp; skills whose output
  stays prose stay prose.
- No live run outputs in the public repo. Run directories, dossiers, live
  receipts over real subjects, and screenshot-class captures stay local under
  the `.gitignore`d run output roots; only schemas, verifiers, READMEs, and
  synthetic examples commit (generalizing the screenshots precedent).
- No changes to superpowers; helix remains the only coupling point.
- No git history changes; all work lands as reviewed PRs.

## Phasing

- **Phase A (in flight):** four hygiene PRs — drift repairs only, independent of
  this design.
- **Phase B (this design), pilot-sequenced per the gauntlet arbitration:**
  - PR-B0 (timing layer — split out of the old PR-B2, ships first): router
    valid-until column citing `valid_while` predicate IDs with per-line revisit
    gates, evidence-research convergence criterion + escalation triggers,
    rigor↔research ordering sentence, drift-rule invariant 6. Pure prose edits,
    zero machinery.
  - PR-B1: `contracts/` skeleton — schema (with the privacy necessity pass:
    keyed-hash session, day-granularity timestamps, closed trigger/subject
    vocabularies, producer content pin), verifier, README (self-issued
    disclosure, committed-artifact boundary, downgrade derivation + regime
    precedence, extension procedure), example receipts, tests. Also commits the
    nine audit reports to `docs/audits/2026-07-22-collection-audit/` (+ synthesis
    index) and the `.gitignore` run-output-roots rule. **Non-waivable gate:** the
    audit reports land at this merge; waiving this reinstates the underlying
    finding at P1 per the arbitration.
  - PR-B2: router receipt machinery — artifact-shape column, routing-record line.
  - PR-B3: blindspot-pass (stamped header; blast-radius quiz placed in the arc as
    optional adjunct below gauntlet's triage threshold) + formal-rigor (structured
    footer). **Gated** (pilot gate below).
  - PR-B4: evidence-research (matrix schema, receipt fields in run record).
    **Gated.**
  - PR-B5: write-goal (structured header, inbound-by-reference). **Gated.**
  - PR-B6: gauntlet (run record, finalize/verify scripts, ledger v2 as derived
    pointer, domain aliases + fit-sensitive fixture, template conditions block,
    evidence-root pin) — the private/public telemetry split and the data-axis
    minimization ship WITH ledger v2 here.
  - PR-B7: evidence-locked-uat (manifest schema, judge honesty fields, sealed
    inputs, recomputability section, extracted judge, calibration vocabulary).
  - PR-B8: helix (`helix-check` receipt-ref form). **Gated.**
  - **Pilot-scope gate (arbitration condition 10):** receipts debut on the proven
    consumers — gauntlet Step 0 + UAT + router (PR-B1, B2, B6, B7, with the
    timing PR first). The emit-side prose PRs (B3–B5, B8) wait on ≥1 recorded
    field handoff in which a receipt was actually consumed (valid or stale),
    observable within 30 days of normal use after PR-B1/B2 merge.
- **Phase C (own specs, own gates):** two new skills — decision/assumption ledger
  (the arc's missing persistence moment), continuity-verify (post-interruption
  memory→artifact re-derivation, gated on resume fixtures). Proposed by the gap
  analysis; each must pass the family-resemblance test at spec time.

### Arbitration conditions attached to Phase B

The 15 conditions from the gauntlet arbitration (`trust-contract-design-2026-07-22`,
run artifacts local-only), mapped to where each lands:

| # | Condition | Lands | Falsifier check |
|---|---|---|---|
| 1 | Nine audit reports committed under `docs/` and path-referenced from Basis | PR-B1 merge | `git ls-tree` ≥9 audit docs (or 1 consolidated with 9 sections) + Basis reference |
| 2 | No raw session identifier (keyed hash / consume-time boolean); day-granularity timestamps | PR-B1 | grep schema + examples: 0 raw session ids |
| 3 | No verbatim user prose: `trigger.matched` → closed trigger-class; `subject.ref` → hash-or-class | PR-B1 | schema grep + example inspection: 0 free-text fields |
| 4 | Committed-artifact boundary: `.gitignore` run output roots + README + NOT-do sentence | PR-B1/B7 | rule present covering run outputs and screenshot-class captures |
| 5 | Data-axis paragraph: per-field retention rule or public-by-design justification; telemetry split with ledger v2; model at family granularity | spec amendment (done here) + PR-B6 | per-field purpose trace before PR-B6 merge |
| 6 | Bounded downgrade rule (envelope-only for judgment kinds) + regime precedence + AC2 semantic clause | spec amendment (done here); re-checked at PR-B1 review | trace a stale `derived-verdict` through Step 0; `confidence`-field counterexample rejected |
| 7 | Prose skills emit 4-field stamps; receipts single-carrier JSON for file producers | PR-B3/B5 | 10-handoff audit within 6 weeks of PR-B5; ≥2/10 non-stamp field changing an outcome → reversal |
| 8 | Null-revision semantics: no `subject-revision-unchanged` on null revision; verifier rejects fail-closed; unevaluable → stale | PR-B1 merge | verifier nonzero exit with named reason on the contradictory combination |
| 9 | Behavioral end-to-end acceptance criterion + semantic review-gate clause per AC + baseline count + retirement condition | spec amendment (done here) + Phase B close | ≥1 criterion exercises emit→consume→skip-a-recheck and stale→re-run |
| 10 | Pilot scope: receipts debut on gauntlet Step 0 + UAT + router; emit-side PRs gated on ≥1 recorded field consumption | phasing (above) | dated, skills-named receipt-consumption event within 30 days post-B1/B2 |
| 11 | Producer pin: `producer.sha256` (or path+git-SHA) or explicit README rationale for collection-version granularity | PR-B1 merge | pin field present OR named rationale paragraph |
| 12 | Ledger v2 = pointer + derived projection; one writable home; `finalize_run.py` derives or `verify_run.py` cross-checks hard-fail | PR-B6 | 5-run diff of overlapping fields: 0 disagreements via derivation |
| 13 | Standing SKILL.md↔schema congruence check (field names + `valid_while` vocabulary) in the test pass | by PR-B8 merge | nonzero exit naming the divergent skill and field on a mismatched fixture |
| 14 | Self-issued disclosure in contracts README; "trust" positively defined | spec amendment (done here) + PR-B1 | limitation sentence present; substitution test, zero behavioral change |
| 15 | "Demonstrably work" struck or sourced; domain-alias PR carries a fit-sensitive fixture check | spec amendment (done here) + PR-B6 | claim struck; ≥1 fit-direction assertion exists |

## Acceptance criteria

1. `verify_receipt.py` passes valid example receipts and fails closed (named
   reason, nonzero exit) on: schema violation, unresolvable hash, unknown
   `valid_while` predicate, missing `never_attests`, and the contradictory
   combination `revision: null` + `subject-revision-unchanged`.
2. The schema contains no field capable of carrying a verdict or an independence
   claim (greppable: no `verdict`, `trust`, `approved`, `independent` keys outside
   `never_attests`) — **and no field or rule whose effect is to raise a
   consumer's confidence in a judgment it did not make or re-verify.** The
   semantic clause is the binding half: judgment-carrying kinds
   (`derived-verdict`, dossier, gate/verdict artifacts) are excluded from
   downgrade consumption by the schema and the bounded downgrade rule, so a
   `confidence`/`outcome`/`score`-style field — or an unbounded downgrade rule —
   fails this criterion even when every key name greps clean.
3. Every skill's SKILL.md references the receipt contract in exactly one place
   (emit or consume); no skill restates another's trigger or guard content. A
   standing stdlib congruence check (SKILL.md receipt references ↔ schema field
   names + `valid_while` vocabulary) is wired into the test pass and fails naming
   the divergent skill and field.
4. Gauntlet: `verify_run.py` re-derives a shipped synthetic example run's verdict
   and selector output byte-identically; the example run ships one
   schema-conformant ledger v2 line marked `"example": true` (derived from the
   example run record, not hand-authored).
5. Timing: router table has the validity column citing `valid_while` predicate
   IDs with revisit gates; evidence-research has the convergence labels and
   escalation triggers; the ordering sentence and drift rule are in the router.
6. **Behavioral end-to-end:** at least one recorded case of a named consumer
   accepting a valid upstream receipt and verifiably skipping a named mechanical
   re-check it would otherwise run — and re-running exactly that check when the
   receipt is stale. Ships with a baseline count of eliminated re-checks and a
   retirement condition (if no consumer skip is ever observable, the receipt
   layer retires). Pilot falsifier for the stamp cut: if ≥2 of the first 10 real
   prose-stamp handoffs show a non-stamp field changing a consumer decision, the
   stamp cut reverses and prose skills restore full receipts.
7. All PRs DCO-signed, reviewed, no merges without operator approval. Each
   criterion above carries a semantic review gate at PR review: "could this pass
   while the property it names fails? — show the counterexample is impossible,
   or review it manually."
