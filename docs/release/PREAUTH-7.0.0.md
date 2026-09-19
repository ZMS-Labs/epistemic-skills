# V7 publication authorization

The repository owner authorized proceeding through the v7 release gates in the
current release session: publish the prepared branch, complete required checks,
merge, verify the exact merge commit, and publish its tag, release assets and Wiki.

- Pull request: https://github.com/ZMS-Labs/epistemic-skills/pull/250
- Version and annotated tag: `7.0.0` / `v7.0.0`.
- Release-note body: `docs/release/RELEASE-7.0.0.md` on the candidate.
- Candidate: the merge commit produced by this PR, after required PR checks pass.
- Firing condition: all exact-candidate integrity gates pass and the designated
  reviewer records GO for that same commit with the documented host/evidence tiers.
- Reviewer: the implementing Codex agent designated by the owner; shared context,
  no claim of independent or blinded review.
- Authorized publication: merge commit (no squash), annotated immutable tag,
  non-draft GitHub Release with the committed notes, revision-bound generated
  assets, and the matching Wiki handbook.
- Tag control: only the version-tag creation restriction may be temporarily
  disarmed for this publication. Preserve update/deletion restrictions, restore
  the original creation rule immediately, and verify rejection of a seeded probe.
  No branch protection or required check is waived.

The annotated tag and attached publication receipt must bind the actual candidate,
check runs and GO. Post-push re-arm facts belong in the publication receipt, not
in a rewritten tag. A failed gate holds dependent publication. The invalid
comparison remains disclosed and provides no behavioral superiority claim.

This authorization names no future merge SHA. It does not authorize moving an
existing release tag, publishing on a failing integrity gate, or erasing historical
evidence. It supersedes the earlier preparation-only PR #244 without merging that
obsolete candidate.
