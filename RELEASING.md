# Releasing epistemic-skills

A release is an immutable support point: one semantic version maps to one Git
commit, one annotated Git tag, and one GitHub Release. `main` is the rolling
channel; a release tag is the reproducible channel.

## When to release

- **Patch** (`x.y.Z`): compatible correctness, packaging, installation, or
  documentation fixes that materially affect users.
- **Minor** (`x.Y.0`): a new skill, contract, harness capability, or materially
  expanded behavior that remains backward compatible.
- **Major** (`X.0.0`): an incompatible trigger, output contract, schema, or
  installation change.

Do not release for internal audit prose or relay bookkeeping alone. Release
when a user-visible change has landed and the gate below can bind it to a
verified snapshot.

## Release gate

Before creating the tag:

1. `main` is clean, synchronized with `origin/main`, and contains the intended
   release changes.
2. `README.md`, all nine version-bearing manifests, the Codex cache-path
   example, and `EXPECTED_VERSION` in the package integration test agree.
3. The complete deterministic suite, DCO, and CodeQL pass on the exact release
   commit.
4. A redacted full-history secret scan passes, and public-content/provenance
   review covers changes since the preceding review.
5. Supported harness surfaces are either exercised live or assigned an honest
   verification tier in the release notes.
6. Known limitations are recorded. An unresolved release-blocking finding
   stops publication.
7. Helix routing is recorded; Gauntlet triage runs before publication and a
   full panel gates any genuinely irreversible or high-blast-radius release.

## Procedure

1. Prepare `agent/release-<version>` from current `main`.
2. Update the live version surfaces and add `docs/release/RELEASE-<version>.md`.
   Historical audits and handoff packets retain the versions they actually
   evaluated.
3. Run the full local gate, open a release PR, and require GitHub checks.
4. Merge the release PR and re-run the gate against the resulting `main` commit.
5. Run and record the Helix/Gauntlet publication gate.
6. Create annotated tag `v<version>` on that exact commit and push the tag.
7. Create a non-draft, non-prerelease GitHub Release from the committed release
   notes.
8. Verify through the GitHub API that the tag target, release target, and local
   `main` commit are identical. Verify the tagged package integration test.

Never move or reuse a published version tag. Corrections ship under a new
semantic version.
