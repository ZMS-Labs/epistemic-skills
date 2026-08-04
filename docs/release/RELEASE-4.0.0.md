# Release 4.0.0 — the consolidation release

**Date:** 2026-08-04. **Breaking.** Eleven skills: the `using-epistemic-skills`
router, `helix`, and **nine disciplines** — recon, resolve, decision-ledger,
write-goal, outsource, open-questions, context-audit, gauntlet,
evidence-locked-uat. Operator-authorized (2026-08-04 session: consolidation
assessment approved; merge, resolution of PR #79, and release approved).

## What changed and why

v3.x grew to eighteen skills faster than evidence accumulated, and every new
seat cost ~12 hand-synced enumeration surfaces. 4.0.0 inverts both curves:

| v4.0.0 skill | Consolidates (as modes/instruments) |
|---|---|
| **recon** | blindspot-pass (brief mode) · wayfinding (initiative mode) · harvest-before-adopt (candidate mode) |
| **resolve** | applying-formal-rigor (derivation) · evidence-research (literature) · throwaway-prototyping (probe) |
| **decision-ledger** | continuity-verify (resume mode, pre-arc) + outcome reviews (first-class trigger) |
| *(craft doctrine, not disciplines)* | intent-traced-merge · agent-interface-design → `plugins/epistemic-skills/reference/craft/` |

Every absorbed method survives verbatim (mode/instrument files are the former
SKILL.md bodies, moved with git history); every old name survives as
mode/instrument vocabulary; every committed battery and epoch result moved
with its method as historical evidence.

## Migration from v3.4.0

- Install surfaces are unchanged in mechanism; the package now registers
  eleven skills. Remove any older copy first (one mechanism per harness).
- Trigger vocabulary maps 1:1: "run a blindspot pass" → recon (brief);
  "wayfind this" → recon (initiative); "should we adopt X" → recon
  (candidate); formal-rigor/evidence-research/prototyping requests →
  resolve's instruments; resumption re-anchoring → decision-ledger's resume
  mode. intent-traced-merge and agent-interface-design are reference
  doctrine, read on demand, no longer routed.
- The ECS contract enumerates the eleven producers; retired producer names
  in previously collected events validate against the pinned pre-4.0
  contract revision (immutable tags), per the contract's own versioning rule.

## Evidence posture (honest status)

- **Tier-0 deterministic:** 35 unconditional CI steps green at release,
  including the new skill-surface generator (`sync_skill_surfaces.py
  --check`) that derives every inventory surface from the filesystem glob +
  `skill-event-map.json`.
- **Trigger epochs:** the 2026-08-04 waves ran first live epochs for all ten
  pre-consolidation batteries (94.6% pass under born-pinned contracts; every
  failure reporting-shape over correct conduct; zero over-firing on 51+ hard
  negatives — register: issue #77). **These epochs predate the consolidation:
  the merged trigger surfaces of recon/resolve/decision-ledger are new
  subjects and re-arm at Tier 1 per `docs/policy/EVIDENCE-POLICY.md`.** No
  post-consolidation epoch has run at release time.
- **Arbitrator certification:** the amended planted-flaw battery (AC-07 =
  seat-provenance neutrality) ran blind 2026-08-04 — 10/10 catch, CERTIFIED
  at standard rigor (same-model-family caveat stands).
- **Behavioral superiority: UNESTABLISHED, now with evidence.** The four-arm
  campaign ran under its committed design (72/72 blinded seeded trials,
  preregistered, exploratory size): **no arm separation** (primary D>A
  p=0.875; A=5 B=4 C=7 D=4 of 18). The run surfaced two structural findings
  — the two-trace-dialect defect (declared uniform adapter; unification is
  open work) and that the shared trace contract, not discipline prose,
  carries the structure at smoke fidelity. Issue #39 remains open; no
  superiority language attaches to this release.
- **Risk acceptance:** `RELEASE-3.0.0-RISK-ACCEPTANCE.json` remains the
  controlling record, append-only (G3-R1's exit criterion met 2026-08-04 and
  recorded in `revisit_history`; all other accepted scopes unchanged). The
  upgrades-landing gauntlet run's rulings R1–R12 are all discharged.

## Governance shipped with this release

- `docs/policy/EVIDENCE-POLICY.md` — tests bind to claims, not calendars
  (subject-hash-armed epochs; once-per-claim campaigns; field-tier
  thresholds).
- `docs/superpowers/plans/2026-08-04-v4.0.0-consolidation.md` — the executed
  consolidation plan with its evidence-continuity rules.
- Creation-gate record `docs/audits/2026-08-04-creation-gate-revisit.md` —
  calibration-review DEFERRED behind a mechanical mint threshold;
  outcome-review promoted in place.

## What this release does not claim

No behavioral-superiority claim; no claim that consolidation improves
outcomes (the campaign motivates simplification and testability, not a
performance claim); no post-consolidation epoch evidence; single-model-family
evidence throughout. Every claim above cites its committed artifact, per the
evidence policy's rule 5.
