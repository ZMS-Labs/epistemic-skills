# 2026-07-22 collection audit — synthesis index

**What this is:** the evidence base for the trust-contract + timing-layer design
(`docs/superpowers/specs/2026-07-22-skill-trust-contract-and-timing-design.md`,
spec PR #24). Nine isolated-subagent audit reports against the collection at
v2.6.0 (baseline 61fbf95; origin/main advanced to 6deee81 during the audit —
plugin manifests only, no skill-content drift). Committed at PR-B1 per the
gauntlet arbitration's non-waivable condition: every constraint the design
creates keeps its reasons recoverable.

**Method:** each report was produced by a context-isolated read-only subagent
with a file:line citation mandate, against the five shared invariants
(floors-not-ceilings; derive/verify-don't-assert; boundary discipline;
fail-closed/explicit degradation; provenance & independence). Improvement
proposals were constrained to minimal one-PR fixes — maximal ritual is a
defect, not an improvement.

## The nine reports

| # | Report | Scope |
|---|---|---|
| 01 | [Router + helix audit](01-router-and-helix-audit.md) | Handoff contracts, trigger narrowing, skip-gate softening, trust-contract readiness |
| 02 | [blindspot-pass + applying-formal-rigor audit](02-blindspot-pass-and-formal-rigor-audit.md) | Missing injection guard, orphaned blast-radius quiz, theory-battery load rule, unstructured outputs |
| 03 | [evidence-research + write-goal audit](03-evidence-research-and-write-goal-audit.md) | The exemplar handoff (§9 extended matrix), schema drift at the gauntlet boundary, approval provenance, research debt |
| 04 | [gauntlet audit](04-gauntlet-audit.md) | Boundary contract, empty telemetry (scrubbed 2026-07-21), fail-open shadow rotation, missing evals/README.md |
| 05 | [evidence-locked-uat audit](05-evidence-locked-uat-audit.md) | Manifest sha256 envelope analysis, judge portability, calibration dead-end, honesty-field fail-open |
| 06 | [Gap analysis](06-gap-analysis.md) | Missing-skill candidates vs family resemblance + creation gates; trust contract is machinery, not a skill |
| 07 | [helix ↔ superpowers alignment review](07-helix-superpowers-alignment-review.md) | Pairing-map coverage, position precision, co-fire checklist, Kimi-harness portability |
| 08 | [Gauntlet lens & verdict deep-dive](08-gauntlet-lens-and-verdict-deep-dive.md) | Lens sufficiency/quality/combinatorics, frozen fit layer, decisive-verification gap |
| 09 | [Arc timing model](09-arc-timing-model.md) | Per-skill temporal semantics, research optimality/escalation/completion, rigor↔research ordering, drift rules |

## The convergent findings (what the design acts on)

1. **Handoffs are prose; only gauntlet and UAT emit machine-checkable
   artifacts** (reports 01, 03, 04, 05). The receipt standard generalizes the
   in-repo exemplars: selector replay record, `gauntlet-role-binding@1`, UAT
   manifest sha256 chain, evidence-research's §9 extended matrix.
2. **Duplicated checks split cleanly into idempotent-mechanical (safe to
   attest once: schema conformance, citation anchoring, hash equality,
   run-order and consent facts) vs freshness-sensitive (must re-run or carry
   validity windows: premise freshness, reception tallies, environment
   reachability)** (all per-skill audits, §3 tables). This split is the
   attestation boundary the schema encodes.
3. **Never-attest list** (every report's §4): verdict-truth, derivation
   correctness, independence achieved, freshness beyond window, skip-gate
   self-assessments, best-guess answers.
4. **Timing silences** (report 09): no research convergence criterion, no
   mode-escalation rules, no rigor↔research ordering, no validity windows
   outside gauntlet's freeze, no general drift rule. All five land as the
   timing layer (PR-B0, PR #25).
5. **Gauntlet verification gap** (reports 04, 08): no hash chain over run
   artifacts, ledger schema can't record what SKILL.md:363 mandates, no
   replay enforcement, fit layer frozen as null with docs overstating
   task-fit. Lands as the gauntlet verification set (PR-B6).
6. **Two new skills earn design investment** (report 06): decision/assumption
   ledger (the arc's missing persistence moment) and continuity-verify
   (post-interruption memory→artifact re-derivation, gated on resume
   fixtures). Phase C, own specs, own gates. Calibration-reader and
   claim-tiering rejected/deferred.

## Gate history for the design built on this base

- Gauntlet run `trust-contract-design-2026-07-22` (standard panel, 5 lenses +
  shadow + arbitrator, 33 findings): **NO-GO as-written** — 2 P1s (public
  telemetry substrate; downgrade-rule verdict-trust back door), 15 conditions.
- v2 amendment → re-gate `trust-contract-design-v2-2026-07-22` (quick panel,
  99.26% citation fingerprint): **CONDITIONAL** — no new P1s; pre-review
  conditions C-A…C-E landed in spec v2.1; C-F…C-H ride as Phase B PR
  requirements.
- Operator approved the spec 2026-07-22. Run artifacts are local-only by
  design (the spec's committed-artifact boundary); the runs are cited by name
  and date.

## Provenance notes

- The reports reproduce the subagents' outputs verbatim (headers added).
  Audit 03's `scite-profile.md:148` citation was later corrected by the
  hygiene implementer to `scite-first-contact.md:37-38`; the underlying
  finding (no Consensus profile file) was real and fixed in PR #20.
- Audit 06 could not enumerate the *installed* superpowers tree (tooling
  failure); it used the upstream listing. Audit 07 read the installed tree in
  full and confirms the set.
- Round-1 gauntlet lens reports had 39/45 [V] citation failures that were
  path-FORM failures (shorthand `spec:` and `.../` paths), zero fabrications
  on a 43/43 full-sample spot-check; the re-gate lenses used
  evidence-root-relative paths and reached 135/136 verified.
