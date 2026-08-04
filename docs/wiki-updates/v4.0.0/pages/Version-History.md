> **Applies to:** epistemic-skills v4.0.0
>
> **Canonical source:** [v4.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/release/RELEASE-4.0.0.md)

# Version History

The Wiki is unversioned navigation over immutable released sources. For exact behavioral contracts, schemas, test results, and install coordinates, use the tagged repository—not this summary.

## v4.0.0 — 2026-08-04 — the consolidation release

**Breaking.** Eleven skills: the `using-epistemic-skills` router, `helix`, and nine disciplines — recon, resolve, decision-ledger, write-goal, outsource, open-questions, context-audit, gauntlet, evidence-locked-uat. Operator-authorized (2026-08-04 session).

### What changed and why

v3.x grew to eighteen skills faster than evidence accumulated, and every new seat cost ~12 hand-synced enumeration surfaces. 4.0.0 inverts both curves by consolidating the collection into fewer, mode-structured disciplines:

| v4.0.0 skill | Consolidates (as modes/instruments) |
|---|---|
| **recon** | blindspot-pass (brief mode) · wayfinding (initiative mode) · harvest-before-adopt (candidate mode) |
| **resolve** | applying-formal-rigor (derivation) · evidence-research (literature) · throwaway-prototyping (probe) |
| **decision-ledger** | continuity-verify (resume mode, pre-arc) + outcome reviews (first-class trigger) |
| *(craft doctrine, not disciplines)* | intent-traced-merge · agent-interface-design → `plugins/epistemic-skills/reference/craft/` |

Every absorbed method survives verbatim (mode/instrument files are the former `SKILL.md` bodies, moved with git history); every old name survives as mode/instrument vocabulary; every committed battery and epoch result moved with its method as historical evidence. The [Skill Catalog](Skill-Catalog) links the current guides and the historical pages.

### Migration from v3.4.0

- Install surfaces are unchanged in mechanism; the package now registers eleven skills. Remove any older copy first (one mechanism per harness).
- Trigger vocabulary maps 1:1: "run a blindspot pass" → recon (brief); "wayfind this" → recon (initiative); "should we adopt X" → recon (candidate); formal-rigor/evidence-research/prototyping requests → resolve's instruments; resumption re-anchoring → decision-ledger's resume mode. intent-traced-merge and agent-interface-design are reference doctrine, read on demand, no longer routed.
- The ECS contract enumerates the eleven producers; retired producer names in previously collected events validate against the pinned pre-4.0 contract revision (immutable tags), per the contract's own versioning rule.

### Evidence posture (honest status)

- **Tier-0 deterministic:** 35 unconditional CI steps green at release, including the new skill-surface generator (`sync_skill_surfaces.py --check`) deriving every inventory surface from the filesystem glob plus `skill-event-map.json`.
- **Trigger epochs:** the 2026-08-04 waves ran first live epochs for all ten pre-consolidation batteries (94.6% pass under born-pinned contracts; every failure reporting-shape over correct conduct; zero over-firing on 51+ hard negatives — register: issue #77). These epochs predate the consolidation: the merged trigger surfaces of recon/resolve/decision-ledger are new subjects and re-arm at Tier 1 per `docs/policy/EVIDENCE-POLICY.md`. No post-consolidation epoch has run at release time.
- **Arbitrator certification:** the amended planted-flaw battery (AC-07 = seat-provenance neutrality) ran blind 2026-08-04 — 10/10 catch, CERTIFIED at standard rigor (same-model-family caveat stands).
- **Behavioral superiority: UNESTABLISHED, now with evidence.** The four-arm campaign ran under its committed design (72/72 blinded seeded trials, preregistered, exploratory size): no arm separation (primary D>A p=0.875). Issue #39 remains open; no superiority language attaches to this release.
- **Risk acceptance:** `RELEASE-3.0.0-RISK-ACCEPTANCE.json` remains the controlling record, append-only (G3-R1's exit criterion met 2026-08-04 and recorded in `revisit_history`; all other accepted scopes unchanged).

### What this release does not claim

No behavioral-superiority claim; no claim that consolidation improves outcomes (the campaign motivates simplification and testability, not a performance claim); no post-consolidation epoch evidence; single-model-family evidence throughout. Every claim above cites its committed artifact, per the evidence policy's rule 5.

## v3.0.0 — 2026-07-26

The first formal immutable support point. It packages the routine-work exit, applying-formal-rigor v2, consolidated Gauntlet, and cross-harness plugin surfaces at the `v3.0.0` tag.

Highlights:

- routine work is reversible, local, directly checkable, and non-precedential; unfamiliar routine-looking work uses two-read micro-recon;
- eleven released skills: router, Helix, and nine disciplines;
- focused formal rigor is inline/record-free; standard and high-assurance work uses `formal-rigor-record@2`;
- material UI acceptance uses the actor/blinded-verifier/deterministic-judge contract;
- durable handoff requires a context-complete, exact-ref, target-readable repository packet;
- immutable install coordinates are pinned to `v3.0.0`.

### Compatibility baseline

There is no earlier tagged compatibility baseline. Replace untagged installations rather than layering copies, reload/start a fresh task, and rerun the Codex Gauntlet role renderer from the v3.0.0 cache path. The Cursor plugin is not publicly listed, so public-marketplace installation is unavailable.

Separately, the retained Cursor behavioral/runtime evaluation epoch remains `BLOCKED_EXTERNAL`; that status describes only the retained evaluation evidence.

### Honest release boundaries

This support point does not claim universal behavioral superiority or cross-provider generality. The release record preserves two genuine P0 behavioral failures (`tm-02`, `tm-03`), AGY zero-token quota availability failures, the blocked Cursor epoch, broad structural polarity not established, an amended Gauntlet arbitrator-certification battery marked `NOT_RUN`, and a post-hoc diagnostic marked exactly `release_credit: none`. Accepted risk does not waive deterministic, security, provenance, review, or publication gates.

### Release identity

The annotated `v3.0.0` tag and GitHub Release must agree with the final `main` commit and committed release notes. Tags are immutable; corrections publish as new commits rather than moving stable release history.

## Sources

- [v4.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/release/RELEASE-4.0.0.md)
- [v4.0.0 README](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/README.md)
- [Evidence policy at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/policy/EVIDENCE-POLICY.md)
- [Executed consolidation plan at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/superpowers/plans/2026-08-04-v4.0.0-consolidation.md)
- [v3.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/docs/release/RELEASE-3.0.0.md)
- [v3.0.0 README](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.0.0/README.md)
