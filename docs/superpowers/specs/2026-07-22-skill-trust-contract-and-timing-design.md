# Skill trust contracts + timing layer — design

**Date:** 2026-07-22
**Status:** Draft for operator review
**Type:** Cross-cutting mechanism (artifact standard + verifier) plus per-skill emit/consume edits
**Basis:** nine-part audit of the collection at v2.6.0 (per-skill audits ×5, gap analysis, helix alignment review, gauntlet lens/verdict deep-dive, arc timing model). Findings cited by file:line throughout the audit reports; this doc records only the decisions and their derivations.

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
references in each skill. A receipt attests **identity, well-formedness,
provenance, and a validity window** — never verdict-truth, never independence,
never freshness beyond its window. Pair it with a **timing layer**: a validity
column in the router's handoff table, a research convergence criterion and
escalation triggers, one sentence resolving the formal-rigor ↔ research ordering,
and a general drift rule. Close the gauntlet audit gap with a content-addressed
run record and a mechanical post-run re-check.

Explicitly rejected: a ninth "trust-contract skill" (no epistemic moment — it is
machinery, and the collection's trust-critical checks are already scripts invoked
by skills, never skills themselves); verdict-carrying trust (would industrialize
the exact guard-weakening defect found twice in the audit: helix's trigger
narrowing and skip-gate softening); harness-specific hooks (violates "one tree,
manifests only").

## The attestation boundary (the core fork, derived)

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
   illegal state is unrepresentable by construction. This is the decisive lens.
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
- `verify_receipt.py` — stdlib-only validator. Given a receipt file (+ artifact
  root), it checks: schema conformance; every referenced artifact's sha256
  resolves; `valid_while` predicates are from the closed vocabulary; the
  `never_attests` field is present and non-empty. **Fails closed**: any miss →
  nonzero exit + named reason. It never evaluates whether the *judgment* in an
  artifact is right; it certifies the envelope only.
- `README.md` — the contract in one page, including the never-attest list.

### `handoff-receipt@1`

```json
{
  "receipt": "handoff-receipt@1",
  "producer": { "skill": "blindspot-pass", "version": "2.6.0" },
  "run": { "id": "<slug>-<YYYYMMDD-HHMMSS>", "at": "<ISO-8601>", "session": "<harness-session-id-or-null>" },
  "trigger": { "matched": "<the observable trigger>", "skip_gate": "passed|fired|n/a" },
  "subject": { "ref": "<path-or-description>", "revision": "<git-SHA|doc-version|null>", "sha256": "<of frozen subject artifact or null>" },
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
  *consumer*, cheaply and mechanically: `subject-revision-unchanged` (compare
  recorded revision to current), `session-continuous` (same session id),
  `freeze-window-open` (gauntlet dossier not frozen / not reopened),
  `environment-reachable` (UAT). A receipt whose predicates fail is not wrong —
  it is **stale**, and the consumer re-runs exactly the freshness-sensitive check,
  nothing else.
- **Downgrade rule:** a receipt from a prior session or a changed revision is not
  discarded; it downgrades one evidence tier (verified → dated inference), matching
  evidence-research's existing freshness semantics ("library notes without a live
  re-check are `[I]` at best when dated and DOI-keyed",
  `evidence-research/SKILL.md:260-263`).
- **Carrier is hybrid** (lowest-common-denominator harnesses produce chat prose):
  file-producing skills (gauntlet, UAT) emit JSON receipts; prose-producing skills
  (blindspot-pass, formal-rigor, write-goal, router) emit a fenced
  `handoff-receipt@1` block with the same fields, hashes computed over the written
  artifact when one exists, `null` when it does not. Well-formedness of the prose
  form is checked structurally (fields present, vocabulary closed), not by hash.

## Per-skill changes (emit / consume)

Each is a few lines in the skill plus, where noted, a schema or script.

| Skill | Emits | Consumes |
|---|---|---|
| **router** | routing record line per firing decision (`router: fired=[...] skipped=[skill(trigger-absent)]`) | — |
| **blindspot-pass** | stamped report header: subject, territory revision, date, `premises-verified` list of (claim, file:line, how-verified) tuples + receipt block | — |
| **applying-formal-rigor** | structured verdict footer: 7-line lens ledger, `facts:` list with revision/date, verdict line + receipt block | blindspot header as input facts (re-verified only if stale) |
| **evidence-research** | `matrix.schema.json` pinning the already-mandated §9 columns + stamps; run record gains receipt fields | Zotero/Consensus/Scite capability facts within run |
| **write-goal** | optional structured header on both templates: goal type, three proof layers present-or-waived, boundaries, stop rule, `approval: {by, at}` + receipt block; inbound evidence/design inputs **referenced by id/path, never paraphrased** | upstream receipts bound by hash into the contract's provenance layer |
| **gauntlet** | `gauntlet-run-record@1` (below) + receipt; Step 0 consumes upstream receipts: **provenance/well-formedness accepted when valid, premises re-verified when stale** — freshness semantics preserved, never attested away | all upstream receipts |
| **evidence-locked-uat** | manifest.json gains normative schema (P1); receipt emitted over the packet | write-goal contracts, requirement sources |
| **helix** | `helix-check` line upgraded: `fired(<artifact-ref>) | skipped(<reason-class>: <evidence>)`, reason classes `trigger-absent | already-ran(<ref>) | operator-override` | — |

## Timing layer (from the arc timing model)

1. **Router handoff table gains a "Valid until" column**, one line per skill
   (recon: until territory changes or next stage starts; verdict: until a named
   input changes; matrix: reception `[V]`-grade this run only, snapshot dated;
   contract: until intent/scope/environment drifts; dossier: frozen subject only).
2. **Research convergence criterion** (evidence-research, after §4): a run
   converges when the counterevidence and boundary-condition query families
   surface no new relevant DOIs beyond the mode's reception dial; terminal-state
   label required — `saturated` / `capped-by-budget` / `contested-stable` —
   porting formal-rigor lens 4's fixed-point rule. `capped-by-budget` becomes an
   honest label instead of a silent exit. (The minimal form — labels only, no
   longitudinal reception-stability requirement — is the floor.)
3. **Escalation triggers** (evidence-research Modes section): escalate one mode
   when any of — a load-bearing paper is contested; the decision is
   high-stakes/irreversible; Consensus↔Scite cross-validation diverges on the core
   question; the synthesis must support a gauntlet dossier.
4. **Rigor ↔ research ordering** (router, one sentence): within `decide`, run
   formal-rigor's lens sweep first to name precise constructs and expose which
   premises are empirical; research exactly those premises; then complete the
   derivation with the verified matrix. If the empirical premise is the decision's
   whole basis, research may lead — the derivation still closes the stage.
5. **General drift rule** (router, as shared invariant 6): if a skill's subject
   materially changes after it ran, its output is void and the skill re-fires at
   its own trigger — never patch the old output. The downstream consumer owns the
   re-fire check (generalizing gauntlet's "subject moves → restart" and matching
   how Step 0 already compensates for stale upstream input).

## Gauntlet verification set

1. **`gauntlet-run-record@1`** — one JSON manifest per run: dossier sha256 +
   freeze timestamp, subject path/revision, evidence-root content pin, selection
   replay hash, per-lens report hashes, fingerprint ref, ruling-set ref, verdict +
   structured conditions array, depth, `docket_mode`, `independence_mode`,
   `role_binding`, per-seat `model`. Produced by `scripts/finalize_run.py`
   (hashes files that already exist; adds nothing to the run itself).
2. **`scripts/verify_run.py`** — given a run directory: re-run the selector against
   `prompts/selection.json`, re-derive GO/CONDITIONAL/NO-GO from `ruling-set@1`'s
   P1/P2 fields, verify the hash chain dossier→reports→arbitration→summary.
   Hard-fail on mismatch. Converts "computed verdict" from doctrine to check.
3. **Ledger schema v2** — add `run_dir`, `dossier_sha256`, `docket_mode`,
   `independence_mode`, per-lens `model` to `runs/README.md` and Step 9 (brings
   the schema up to what SKILL.md:363 already mandates). Schema-versioned append;
   no backfill.
4. **Domain vocabulary normalization** — a controlled `domain_aliases` map in the
   registry + selector so `finance`/`cost`/`spend`, `ux`/`accessibility`,
   `infra`/`operations`/`ops` intersect; re-run the 1000-fixture self-test. The
   cheapest real task-fit improvement while the fit layer stays frozen — it
   strengthens the gates and specialist seed, the parts that demonstrably work.
5. **Synthesis template** — CONDITIONAL emits a fenced JSON conditions array
   `{condition, falsifier{method,threshold,timeframe}, owner}` lifted from
   `ruling-set@1` acceptance criteria (template currently `[enumerate]` prose).
6. **Evidence-root pin** — Step 1 establishes the evidence root as a content hash,
   not only a path, so `[V path:line]` verifications are hash-bound and their
   invalidation is detectable.

Deferred (named, not built): the behavioral admission-battery run for
probation/migration/release/IP lens clusters (machinery exists; it is a *run*,
operator-gated); shadow-seat telemetry separation from the shipped package
(private/public telemetry split, belongs to the control plane).

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

- No verdict-carrying trust, ever. The schema has no field for it.
- No attestation of independence (lens isolation, blinded verifier) — procedural
  properties are recorded as metadata (`independence_mode`), never certified.
- No new skill. The router, helix, and the six disciplines keep their boundaries;
  receipts ride on existing outputs.
- No harness hooks, no Workflow dependency, no per-harness forks.
- No maximal ritual: prose-form receipts are one stamped block; skills whose
  output stays prose stay prose.
- No changes to superpowers; helix remains the only coupling point.
- No git history changes; all work lands as reviewed PRs.

## Phasing

- **Phase A (in flight):** four hygiene PRs — drift repairs only, independent of
  this design.
- **Phase B (this design):**
  - PR-B1: `contracts/` skeleton — schema, verifier, README, example receipts, tests.
  - PR-B2: router — artifact-shape + valid-until columns, routing-record line,
    drift-rule invariant 6, rigor↔research ordering sentence.
  - PR-B3: blindspot-pass (stamped header; blast-radius quiz placed in the arc as
    optional adjunct below gauntlet's triage threshold) + formal-rigor (structured
    footer).
  - PR-B4: evidence-research (matrix schema, convergence criterion, escalation
    triggers, receipt fields in run record).
  - PR-B5: write-goal (structured header, inbound-by-reference).
  - PR-B6: gauntlet (run record, finalize/verify scripts, ledger v2, domain
    aliases, template conditions block, evidence-root pin).
  - PR-B7: evidence-locked-uat (manifest schema, judge honesty fields, sealed
    inputs, recomputability section, extracted judge, calibration vocabulary).
  - PR-B8: helix (`helix-check` receipt-ref form).
- **Phase C (own specs, own gates):** two new skills — decision/assumption ledger
  (the arc's missing persistence moment), continuity-verify (post-interruption
  memory→artifact re-derivation, gated on resume fixtures). Proposed by the gap
  analysis; each must pass the family-resemblance test at spec time.

## Acceptance criteria

1. `verify_receipt.py` passes valid example receipts and fails closed (named
   reason, nonzero exit) on: schema violation, unresolvable hash, unknown
   `valid_while` predicate, missing `never_attests`.
2. The schema contains no field capable of carrying a verdict or an independence
   claim (greppable: no `verdict`, `trust`, `approved`, `independent` keys outside
   `never_attests`).
3. Every skill's SKILL.md references the receipt contract in exactly one place
   (emit or consume); no skill restates another's trigger or guard content.
4. Gauntlet: `verify_run.py` re-derives a shipped synthetic example run's verdict
   and selector output byte-identically; the example run ships one
   schema-conformant ledger v2 line marked `"example": true`.
5. Timing: router table has the validity column; evidence-research has the
   convergence labels and escalation triggers; the ordering sentence and drift
   rule are in the router.
6. All PRs DCO-signed, reviewed, no merges without operator approval.
