# Releasing epistemic-skills

A release is an immutable support point: one semantic version maps to one Git
commit, one annotated Git tag, and one non-draft GitHub Release. `main` remains
the rolling channel; a version tag is the reproducible channel.

The repository has not yet published its first formal release. The intended
first release is **3.0.0**. See `docs/release/RELEASE-3.0.0.md`; it is a held
draft, not evidence that 3.0.0 exists.

## When to release

- **Patch** (`x.y.Z`): compatible correctness, packaging, installation, or
  documentation fixes that materially affect users.
- **Minor** (`x.Y.0`): a new skill, contract, harness capability, or materially
  expanded behavior that remains backward compatible.
- **Major** (`X.0.0`): an incompatible trigger, output contract, schema, or
  installation change.

Do not release internal audit prose or relay bookkeeping alone. Release when a
coherent user-visible change has landed and the gate below can bind it to a
verified snapshot. For 3.0.0, the proportional routing and formal-rigor and
Gauntlet contract changes form the coherent release subject.

## Release gate

Before creating the first tag:

1. `main` is clean, synchronized with `origin/main`, and contains the intended
   release changes.
2. Formal-rigor v2 has a genuine neutral/current-v1 RED result captured before
   its production edit, then passes its candidate fixture contract. A blocked
   scaffold is not a production implementation.
3. The five blinded proportionality arms are run through the pinned isolated
   harness and retained without repairing or discarding failures.
4. Every version-bearing live manifest, README version statement, install
   example, and package-integration expected version agrees on 3.0.0. This
   alignment happens in the release PR, not during held preparation.
5. The complete deterministic suite, DCO, CodeQL, manifest parity, and
   committed-JSON checks pass on the exact release commit.
6. A redacted full-history secret scan passes, and public-content/provenance
   review covers the release diff.
7. Supported harness surfaces are exercised live or assigned an honest
   verification tier in the release notes; known limitations are recorded.
8. Helix routing is recorded and an independent Gauntlet publication review
   reaches GO. An unresolved high-severity or release-blocking finding stops
   publication.

## Procedure

1. Prepare `agent/release-3.0.0` from the final intended `main`.
2. Align the live version surfaces and finalize
   `docs/release/RELEASE-3.0.0.md`. Historical evidence retains the versions it
   actually evaluated.
3. Run the full local gate, open a release PR, and require GitHub checks.
4. Merge the release PR and re-run the gate against the resulting `main`
   commit.
5. Run and record the Helix/Gauntlet publication gate.
6. Create annotated tag `v3.0.0` on that exact commit and push the tag.
7. Create a non-draft, non-prerelease GitHub Release from the committed notes.
8. Verify through the GitHub API that the tag, peeled tag target, release
   target, and local `main` commit are identical, and that the normalized
   release body equals the committed release-note file.

## Partial-publication recovery

Never improvise around an immutable remote tag.

| Observed state | Recovery |
|---|---|
| No remote tag | Fix forward, rerun the complete gate on final `main`, then restart publication. |
| Correct remote tag; no GitHub Release | Create the Release from the committed notes on that tag, then run every identity assertion. |
| Correct remote tag; malformed GitHub Release | Repair or recreate the Release object against the same correct tag, then run every identity assertion. |
| Wrong remote tag | Stop publication. Do not move or reuse it; correct the cause and issue a new semantic version. |

Never move or reuse a published version tag. Corrections ship under a new
semantic version.
