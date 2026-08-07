> **Maintainer handbook:** current development
>
> **Released baseline:** [v5.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-5.0.0.md)
>
> **Current development policy:** [`RELEASING.md` on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/RELEASING.md) is mutable, version-neutral, and controls the next release when it differs from this summary.
>
> **Honesty:** v5.0.0 published with item 6 PARTIALLY MET and item 8 WAIVED. Immutable tags are not moved; corrections ship under a new semantic version or mutable Release-body amend only.

# Release Process and Versioning

A release is an immutable support point: one semantic version maps to one Git commit, one annotated tag, one non-draft GitHub Release, aligned package surfaces, and committed release notes. `main` is the rolling channel; a tag is the reproducible channel.

## When it is time to release

Release when a coherent user-visible change has landed and the complete gate can bind it to a verified snapshot. Do not release internal audit prose, relay bookkeeping, or process artifacts alone.

| Version | Use when |
|---|---|
| Patch `x.y.Z` | Compatible correctness, packaging, installation, or documentation fixes that materially affect users. |
| Minor `x.Y.0` | A new skill, contract, harness capability, or materially expanded behavior that remains backward compatible. |
| Major `X.0.0` | An incompatible trigger, output contract, schema, or installation change. |

A release “means” that the tagged contracts, checks, install coordinates, notes, and publication identity agree. It does not mean every behavioral question is closed or that every harness is behaviorally proven.

## Release subject and evidence freeze

Before opening a release pull request:

1. Name the coherent user-visible release subject.
2. Freeze the exact intended source revision.
3. Inventory every version-bearing surface and immutable install example.
4. Keep historical evidence at the version and revision it actually evaluated.
5. Record known gaps with owner, scope, revisit trigger, and exit criterion.
6. Distinguish qualifying release evidence from diagnostic or historical evidence.

For v3.0.0, the subject was the proportional routine path, applying-formal-rigor v2, consolidated Gauntlet, and cross-harness package surfaces. It was the repository's first formal release, so no earlier tag served as a compatibility baseline.

## Non-waivable release gate

The exact candidate commit must satisfy all applicable gates:

1. Clean, synchronized `main` contains the intended changes.
2. Version parity holds across the README, nine package manifests, immutable install references, and package-integration `EXPECTED_VERSION`.
3. The complete deterministic repository suite passes.
4. Every release-PR commit passes author-matching DCO.
5. CodeQL succeeds on the exact release-PR head.
6. A redacted full-history secret scan passes, and a positive control proves the scanner can fail.
7. Public-content and provenance review covers the release diff.
8. Supported harness surfaces are exercised live or assigned an honest verification tier.
9. Known limitations and excluded evidence remain visible.
10. Helix routing is recorded and an independent Gauntlet publication review reaches GO.
11. The annotated tag, peeled tag target, GitHub Release target, final `main`, and committed release notes satisfy identity checks.

An operator may accept bounded behavioral risk. That decision cannot waive the deterministic, security, provenance, DCO, review, or publication-identity gates.

## Procedure

The released process is:

1. Create a release branch from the final intended `main`.
2. Align live version surfaces and finalize committed release notes. Do not rewrite historical evidence to the new version.
3. Run the full local gate.
4. Open the release pull request and require GitHub checks on its exact head.
5. Complete independent public-content, provenance, and publication review.
6. Merge the release PR.
7. Re-run the gate against the resulting `main` commit.
8. Run and record the Helix/Gauntlet publication gate.
9. Create and push an annotated tag on that exact commit.
10. Create a stable, non-draft, non-prerelease GitHub Release from the committed notes.
11. Verify by API that every identity coordinate agrees and that the normalized Release body equals the committed note file.

Do not tag a candidate before the exact-head gates have passed. Do not treat a draft Release or lightweight tag as equivalent.

## Version alignment

Version changes are release work, not held preparation. A release PR updates every live version-bearing surface together and verifies that package integration expects the same value.

Review at least:

- README version statement and install examples;
- Claude marketplace/package metadata;
- Codex package metadata;
- Cursor root, marketplace, and package metadata;
- Gemini extension metadata;
- Kimi root/package metadata where present; and
- any test constant that asserts expected package version.

The Antigravity marker schema does not necessarily contain a version field; verify the schema rather than adding unsupported metadata.

## Release notes and migration

Committed notes should include:

- release identity and date;
- coherent highlights;
- compatibility baseline;
- replace-versus-layer migration instructions;
- behavior integrations must change;
- exact deterministic and behavioral evidence coordinates;
- honest accepted limitations;
- no-credit diagnostic boundaries;
- support and marketplace constraints; and
- the publication-identity contract.

Stable install commands must use the immutable tag. Never document `main` as the reproducible channel.

## Partial-publication recovery

Never improvise around an immutable remote tag.

| Observed state | Recovery |
|---|---|
| No remote tag | Fix forward, rerun the complete gate on final `main`, then restart publication. |
| Correct remote tag, no GitHub Release | Create the Release from committed notes on that tag, then run every identity assertion. |
| Correct remote tag, malformed GitHub Release | Repair or recreate the Release object against the same correct tag, then rerun identity assertions. |
| Wrong remote tag | Stop. Do not move or reuse it; correct the cause and issue a new semantic version. |

Published tags are never moved. Corrections ship under a new version.

## Evidence interpretation during release

- Green deterministic checks establish the named invariants on the exact candidate.
- Behavioral campaigns establish only their frozen subjects and protocols.
- Diagnostics may inform risk acceptance but cannot be relabeled as qualifying evidence.
- Availability failures remain availability failures unless a valid semantic judgment exists.
- Historical audits remain dated evidence, not current certification.
- A prior Gauntlet or CodeQL result does not substitute for the exact release head when the gate requires exact-head evidence.

For v3.0.0 specifically, retain the two genuine P0 failures, the 88 zero-token AGY availability failures, Cursor `BLOCKED_EXTERNAL`, amended arbitrator battery `NOT_RUN`, and `release_credit: none` diagnostic status. See [Evidence, Status, and Known Limitations](Evidence-Status-and-Known-Limitations).

## Sources

- [Released v3.0.0 release policy](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/RELEASING.md)
- [Released v3.0.0 notes](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-3.0.0.md)
- [Released v3.0.0 machine-readable risk record](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/docs/release/RELEASE-3.0.0-RISK-ACCEPTANCE.json)
- [Released v3.0.0 security workflow](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.github/workflows/release-security.yml)
- **Current development:** [release policy on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/RELEASING.md)
