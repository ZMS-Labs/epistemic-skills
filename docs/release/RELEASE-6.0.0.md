# Release 6.0.0

**Support point:** `v6.0.0` — one semantic version, one immutable Git tag, one
evidence set. Supersedes `v5.1.0`.

**Candidate identity.** The v6 BUILD freeze was reviewed at candidate
`03e972c5d427238033cb90d66846adabaf11928d` with its packet at
`546ccc8e55eb060379d62198310145f7243ac7bd`; both are ancestors of the release
branch and are pinned by `pin/es-v6-rc5-candidate-2026-08-19` and
`pin/es-v6-rc5-freeze-2026-08-19`. The release candidate is the commit produced
by merging this release branch, and the publication gate runs against that
commit — not against this file's description of it.

## Why 6.0.0

The skill surface did not grow: v6.0.0 ships the same **fifteen** skills as
v5.1.0. The major version marks something else — a security fix in the custody
contract, the completion of the v5 design commitments, and a new assurance
contract that changes what a release of this project is allowed to claim.

The honest summary: v5 claimed things about itself that nothing checked. v6
makes those claims mechanical, and where a claim could not be made mechanical,
it is written down as a limit with an owner.

## What ships

**Security — mission-custody (es#137).** Three P1 false-allow bypasses and four
P2 refusal gaps are closed. These are real permission-boundary defects: paths
that the custody guard should have refused and did not. If you rely on
mission-custody to bound where an agent may write, this is the reason to
upgrade.

**The v5 design commitments, completed.** All four were implemented and are now
enforced rather than asserted:

- `ROUTING.md` is generated solely from `metadata.hands-to`, byte-verified in
  CI, and the hand-authored-routing-table ban is mechanically enforced.
- Every packaged skill carries the intrinsic evidence-emission step
  (`skill-run@1`) with a schema-validated tracked exemplar; live ledgers are
  runtime-local by amended design.
- Sentinel corpora exist for every skill, with `event_kind` bound into each
  fixture and a scorer that fails closed in both directions.
- Skill membership has one source of truth: per-skill frontmatter event
  metadata derives the event map, its schema, the verifier inventory, and every
  count surface. Membership drift fails closed.

**A new assurance contract (`contracts/v6-assurance`).** A release candidate is
now sealed against an exact commit: per-file sha256 digests of every
inventoried source plus the candidate tree hash, recomputed by a validator that
turns CI red if any inventoried file changes after the freeze. The packet's
readiness state cannot be reached by editing a field — the independent verdict
must exist as an on-disk artifact naming the exact candidate SHA, and operator
acceptance must be recorded separately.

**Deterministic-gate hardening.** The durable decision ledger is byte-append-only
against the merge base; the DCO check gained planted self-test controls; the
secret scan's one path exemption is anchored and proven narrow in CI on every
run; the clean-room replicates the workflow's Python steps with a completeness
assertion rather than a hand-maintained copy.

## Release gate status for 6.0.0

Twenty-six class claims carry structured severities and named oracles. At the
freeze: twenty PROVED, five LIMITED, one UNPROVED by construction
(`CLM-INDEPENDENT-GAUNTLET` — a packet may not certify its own review; the GO
verdict is a separate artifact).

Requalification ran all five gating workflows against the exact candidate via
`workflow_dispatch`, with step-level confirmation that the two newest oracles
executed rather than skipped. The full required-job set then ran green against
the sealed head on the freeze pull request.

## Known limitations, carried honestly

Shipped in the packet with named owners:

| Limit | What it means |
|---|---|
| `KL-SELF-GO` | The implementing lineage holds no acceptance seat. |
| `KL-LIVE-ENV` | Behavioral epochs and native-harness live-fire were not run. |
| `KL-MACOS-162` | Measured APFS Unicode-fold collision: two contract-distinct filenames are one physical file. Custody distinctness claims exclude case-insensitive APFS. |
| `KL-WINDOWS` | No native-Windows requalification was run. |
| `KL-DRAFT-CI` | Draft pull requests skip all five gating workflows until ready-mark. |
| `KL-RESTAMP` | A recorded candidate SHA is an observation of the tree it was generated from, never a target to restamp. |
| `KL-GUARD-LEXICAL` | Custody guard path matching is lexical; a write spelled through a symlinked parent can resolve inside a guarded tree while the guard does not match. |
| `KL-SEAL-MAIN-COUPLING` | The freeze seal binds inventoried sources; a default-branch change to any of them turns the freeze red on its pull request's merge ref. |
| `KL-MAIN-137` | **Retired by this release.** It disclosed that the es#137 fixes existed only in the candidate tree. The freeze merge landed them on the default branch. |

Twelve further findings from the final review are open, all graded P4, three
carrying preserved P3 dissents. They are recorded in that run's arbitration
rather than summarized away here. The largest is honest to state plainly: the
DCO checker's merge-commit exemption is unconditional, so a merge commit that
authors content — a conflict resolution — is uncertified by it.

## Migration from 5.1.0

Install surfaces change version only; the skill inventory is unchanged, so no
skill is renamed, retired, or added. Replace an older copy with a `v6.0.0`
tagged checkout or plugin install, reload the harness, and verify the skill
count and source path — one install mechanism per harness, never two.

The one behavioral change to expect is stricter custody refusals. Paths the
guard previously allowed through the es#137 bypasses are now refused. If a
workflow depended on one of those writes succeeding, it will now fail closed;
that is the fix working.

## Provenance notes

The v6 BUILD freeze was reviewed by **five independent panels** and produced
**four NO-GO verdicts** before its GO. Each NO-GO was found by a panel
reviewing the previous repair, and every P1 in the sequence belonged to one
class: a gate that had never actually executed against the sealed head.

1. Freeze panel — 18 rulings, 15 acceptance criteria.
2. Cross-family panel (Kimi/Moonshot) — rulings S1–S10.
3. Delta review — the candidate commit had byte-rewritten published
   append-only ledger lines.
4. Fourth panel — six commits in the freeze pull request carried no DCO
   sign-off, so a required job would have gone red at ready-mark.
5. Fifth panel — GO, with the discharge re-executed from primary sources.

Run records live under `docs/gauntlet-runs/`. The verdicts are retained at
their original coordinates; none of them was rewritten to match a later
outcome.
