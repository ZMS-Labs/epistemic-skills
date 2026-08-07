# Phase 0 counterpart reconnaissance — epistemic-calibration confirmed

**Date:** 2026-08-04
**Charter:** `docs/coordination/epistemic-calibration.md` (Phase 0 — establish the link)
**Subject (ours):** `ZMS-Labs/epistemic-skills`, v4.0.0 (`53ad6d5` merge; release tag `v4.0.0`)
**Counterpart:** `ZMS-Labs/epistemic-calibration`, immutable revision
`6d3668a94134d5891779c01332d2ee62a1854208`

## What changed

The charter was written when the calibration coordinate was an
operator-supplied naming inference: "all calibration-side state is
**unknown**, not absent." That posture is now retired. The counterpart
repository was reached, cloned, and read during the 2026-08-04 session. Every
fact below was observed directly in that clone at the revision named above.

## Observed counterpart facts

1. **Canonical coordinate confirmed.** `ZMS-Labs/epistemic-calibration`
   exists at the charter's named URL. Default branch `main`; observed HEAD
   `6d3668a94134d5891779c01332d2ee62a1854208` (merge of its PR #2,
   "codex/ecs-learning-loop-design", 2026-07-31).
2. **Private staging under publication hold.** `PUBLICATION-HOLD.md` keeps
   all publication gates closed (including an open "ownership and
   contributor-rights review" gate). The repository self-describes as the
   private development home of the portable ECS calibration kernel.
3. **It pins us — content-true and CI-enforced.** Its
   `docs/design/epistemic-skills-contract-lock.json` declares contract
   `epistemic-skills-event-contract@1` against this repository at commit
   `8d9b2f85bd8e081a547e33f4bb9b5eb880a4c2b0`, with SHA-256 digests for the
   three event-contract files (`epistemic-event.schema.json`,
   `epistemic-outcome.schema.json`, `skill-event-map.json`). All three
   digests were independently recomputed here from
   `git show 8d9b2f85:<path>` and **match**. Its CI (`verify.yml`) fetches
   this repository **by SHA, not by ref**, and runs
   `check_epistemic_contract.py --require-sibling`, so a moved branch or tag
   on our side cannot change what it verifies.
4. **Our pin tag is its reachability guarantee.** Commit `8d9b2f85` is
   exactly our published tag `pin/ecs-contract-2026-07-27`. The
   counterpart's own CI comment says that tag exists only to keep the SHA
   reachable. **That tag must never be deleted.**
5. **Ownership boundary is documented.** `docs/design/BOUNDARY.md` separates
   the public-core candidate from private product/operations, names the
   legacy private source (`<private-fleet-repo>@27f9dfa0…`) as provenance
   only, and forbids the core from assuming private state — consistent with
   the charter's ownership table.
6. **The exchange-unit protocol is not yet adopted there.** No file in the
   counterpart references `epistemic-product-calibration@1`. Its
   event-contract lock is a narrower, self-defined consumer pin (schemas +
   producer map), i.e. a de facto counter-proposal scoped to event
   collection — not the full cross-repository result-exchange protocol the
   charter defined.

## Phase 0 exit adjudication

Charter exit criterion: *"reciprocal immutable references and named owners
exist in both repos."*

| Attribute | Status |
|---|---|
| Counterpart → skills immutable reference | **Met.** Lock file at `8d9b2f85` with per-file SHA-256, CI-enforced by-SHA fetch; digests independently verified here. |
| Skills → counterpart immutable reference | **Met by this record.** Revision `6d3668a94134d5891779c01332d2ee62a1854208` is the frozen counterpart coordinate. |
| Named owners | **Substantially met.** Our side: ZMS-Labs epistemic-skills maintainers (charter header). Counterpart side: same organization, with a formal ownership/contributor-rights review still an open gate under `PUBLICATION-HOLD.md`. That open gate is theirs to close and does not block Phase 1. |

**Phase 0 is complete.** The link is established on observed facts, not
inference.

## Deltas the next phase must carry

- **The counterpart's pin predates v4.0.0.** At `8d9b2f85` (2026-07-27)
  the producer map enumerates the v3.0-era skill names. v4.0.0 consolidated
  the inventory to a different eleven (router, helix, nine disciplines);
  retired producer names in previously collected events validate against
  the pinned pre-4.0 contract revision, per the contract's own versioning
  rule (see `docs/release/RELEASE-4.0.0.md`). Re-pinning to a v4.0.0
  coordinate is **counterpart-owned work** under the charter's change
  protocol (propose → freeze → land independently); this repository must
  not force it and must keep both coordinates immutable in the meantime.
- **Exchange-unit adoption is open Phase 1 work.** The charter asked the
  counterpart to adopt or counter-propose `epistemic-product-calibration@1`.
  Observed state: a narrower event-contract lock exists; the result-exchange
  protocol has no counterpart-side surface yet. First joint slice remains
  the UAT seeded-defect pilot (charter Phase 2), which requires that
  adoption or an explicit counter-proposal first.
- **Reachability obligations are now bilateral.** We must keep
  `pin/ecs-contract-2026-07-27` (and every future pin tag) reachable
  forever; the counterpart must keep `6d3668a…` reachable for this record.

## Method note

Reconnaissance used a shallow clone of the counterpart's default branch in
the 2026-08-04 session environment; all quoted paths and digests were read
from that clone. No counterpart file was modified; no cross-repository
write occurred. This record and its ledger entry
(`calibration-phase0-recon-20260804-13`) are the skills-side half of the
reciprocal reference.
