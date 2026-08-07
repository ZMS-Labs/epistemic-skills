> **Maintainer handbook:** current development
>
> **Released archive:** [designs, audits, and evidence in v3.0.0](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/docs)
>
> A design describes intent; a plan describes intended execution; an audit describes a dated frozen subject. None automatically certifies current behavior.

# Design History and Audits

The repository keeps design rationale and failed or partial evaluations recoverable. This page is an index, not a replacement specification and not a current certification statement.

## How to read the archive

Use this precedence when documents disagree:

1. immutable released `SKILL.md`, schema, verifier, or executable check;
2. released reference files and release records;
3. dated design, plan, audit, handoff, or run artifact;
4. README and Wiki summaries.

Always read a historical record with its subject revision, date, status, and residuals. Later fixes may supersede a finding without changing what the original record observed.

## Architecture and collection designs

| Date | Record | Historical purpose | Interpretation boundary |
|---|---|---|---|
| 2026-07-17 | [Plugin design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-17-epistemic-skills-plugin-design.md) | Initial collection and plugin shape. | Design origin, not the complete v3.0.0 contract. |
| 2026-07-18 | [Agentic control-plane design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-18-agentic-control-plane-design.md) | Wider control-plane framing that influenced packaging and workflow boundaries. | Contains context beyond the shipped public plugin; use current skill contracts for behavior. |
| 2026-07-18 | [Cross-harness packaging architecture](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-18-agentic-skills-packaging-architecture.md) | One canonical tree and thin harness surfaces. | Check released manifests for implemented state. |
| 2026-07-20 | [Helix design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-20-helix-design.md) | Tandem workflow/epistemic pairing model. | Released `helix/SKILL.md` controls; Helix is the central passage, not the router. |
| 2026-07-22 | [Continuity Verify design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-22-continuity-verify-design.md) | Re-anchor state after summaries and handoffs. | Released skill and committed fixture results control. |
| 2026-07-22 | [Decision Ledger design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-22-decision-ledger-design.md) | Consequential-decision persistence without ritual logging. | Released reuse/no-op contract controls. |
| 2026-07-22 | [Epistemic-flexibility integration](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-22-epistemic-flexibility-integration.md) | Cross-cutting claim, authority, prediction, failure-chain, and closure controls. | Controls are not an additional skill or trigger. |
| 2026-07-22 | [Trust contract and timing design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-22-skill-trust-contract-and-timing-design.md) | Receipt envelope, validity windows, and temporal handoffs. | The released schema/verifier defines implemented behavior. |

## Formal-rigor design and evaluation sequence

| Date | Record | What it contributes | Current interpretation |
|---|---|---|---|
| 2026-07-23 | [Applying-formal-rigor v2 design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-23-applying-formal-rigor-v2-design.md) | Focused, standard, and high-assurance tiers plus open-world reasoning. | Released skill and validators control the final contract. |
| 2026-07-23 | [Formal-rigor fixture matrix](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-23-applying-formal-rigor-v2-fixture-matrix.md) | Testable scenarios and scorer expectations. | Fixture coverage is structural unless a retained behavioral campaign says otherwise. |
| 2026-07-25 | [Non-Cursor degraded evaluation design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-25-formal-rigor-noncursor-degraded-evaluation.md) | A provider campaign after Cursor transport was blocked. | The resulting epoch was excluded; do not promote its content. |
| 2026-07-26 | [Post-hoc diagnostic design](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/superpowers/specs/2026-07-26-formal-rigor-v3-posthoc-diagnostic-design.md) | Frozen, no-retry diagnostic analysis of retained content. | Diagnostic only, exactly `release_credit: none`. |
| 2026-07-26 | [Post-hoc diagnostic evidence](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/evidence/2026-07-26-formal-rigor-v3-posthoc-diagnostic.md) | Structural accounting and bounded semantic review. | Found two genuine P0 failures; AGY failures were quota availability, not merit judgments. |

## Collection audit — 2026-07-22

The [collection-audit index](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/audits/2026-07-22-collection-audit/00-INDEX.md) synthesizes nine isolated read-only reports against a v2.6.0-era subject. It informed the trust-contract/timing design, Decision Ledger, Continuity Verify, and later Gauntlet work.

Its own provenance notes include corrected citations, tooling limitations, and the original gate history. Treat the reports as reasons behind subsequent design changes—not as a certification of v3.0.0 or current `main`.

## Suite stress test — 2026-07-23

The [suite stress-test index](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/audits/2026-07-23-suite-stress-test/00-INDEX.md) records a v2.9.1-era eleven-skill audit, package reconciliation, and RED-to-GREEN integration fixes.

Its status was **PARTIAL**. Deterministic checks passed, but the required current Gauntlet stopped because the target exposed no auditable context-isolated exact-role invocation primitive. The [blocked record](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/gauntlet-runs/epistemic-skills-suite-stress-test-2026-07-23/BLOCKED.md) deliberately contains no fabricated reports, arbitration, or verdict.

Do not quote the stress test's skill dispositions as current certification. They belong to its frozen subject and verification tiers.

## Epistemic-flexibility Gauntlet — 2026-07-22

The initial [Gauntlet summary](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/GAUNTLET-SUMMARY.md) returned **NO-GO** after identifying a fail-closed claim without a control/action consistency check. The [post-fix bounded recomputation](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/gauntlet-runs/epistemic-flexibility-v3-2026-07-22/POST-FIX-VERDICT.md) closed that P1 deterministically and recomputed **CONDITIONAL**, carrying residuals forward.

This sequence is valuable because it preserves the negative finding and the exact evidence that closed it. It is not a blanket current Gauntlet certification.

## Public-release and provenance records

| Record | Frozen historical claim |
|---|---|
| [Public release review — 2026-07-17](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/PUBLIC-RELEASE-REVIEW-2026-07-17.md) | Ownership, license, secret scan, Actions-log scan, and DCO review through its named baseline. |
| [Review addendum — 2026-07-21](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md) | Later tracked-tree sweep and remediation of private-topology content through its named revision. |
| [DCO live proof — 2026-07-17](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/DCO-LIVE-PROOF-2026-07-17.md) | Historical negative and positive workflow exercise. |
| [v3.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-3.0.0.md) | First immutable support point, evidence coordinates, migration, limitations, and publication identity. |
| [v3.0.0 risk acceptance](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-3.0.0-RISK-ACCEPTANCE.json) | Bounded behavioral-risk acceptance and non-waivable gates. |

Every later release needs new exact-head checks and review. A clean historical review does not reach forward through Git history.

## Current documentation design

The Wiki/README handbook itself is documented in the approved design and implementation plan. These files were authored after the v3.0.0 support snapshot and therefore are deliberately labeled current development:

- **Current development:** [GitHub Wiki and README handbook design on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/superpowers/specs/2026-07-26-github-wiki-and-readme-design.md)
- **Current development:** [handbook implementation plan on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/superpowers/plans/2026-07-26-github-wiki-readme-handbook.md)

Their goal is navigation over released sources. They do not modify the v3.0.0 skill contract.

## Maintaining this index

When adding a design, audit, or run:

1. Preserve its date and exact subject revision.
2. State whether it is design, implementation plan, structural test, behavioral evidence, diagnostic, or release credit.
3. Retain original failures and dissent.
4. Link a fix as a later record rather than rewriting the earlier result.
5. State missing tools, blocked boundaries, and unrun steps.
6. Never summarize a historical GO, PASS, or clean scan as standing current certification.
7. Link stable behavior to an immutable release and label `main` as current development.

## Related handbook pages

- [Architecture and Contracts](Architecture-and-Contracts)
- [Testing and Evaluations](Testing-and-Evaluations)
- [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations)
- [Release Process and Versioning](Release-Process-and-Versioning)
- [Security, Provenance, and DCO](Security-Provenance-and-DCO)
