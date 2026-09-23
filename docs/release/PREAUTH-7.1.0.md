# V7.1 publication authorization

The repository owner authorized proceeding through the v7.1.0 release gates in
the current release session (2026-09-23): merge the content change once green,
prepare and merge the version-rotation release PR, verify the exact merge
commit, and publish its tag, release assets and matching Wiki handbook so
7.1.0 is fully and properly live.

- Pull request (content): https://github.com/ZMS-Labs/epistemic-skills/pull/259
  (merged as `6423157` before this authorization was exercised).
- Pull request (release): the version-rotation PR opened from
  `release/7.1.0` carrying this file and the finalized release note.
- Version and annotated tag: `7.1.0` / `v7.1.0`.
- Release-note body: `docs/release/RELEASE-7.1.0.md` on the candidate.
- Candidate: the merge commit produced by the release PR, after required PR
  checks pass.
- Firing condition: all exact-candidate integrity gates pass (deterministic,
  DCO, security/public-content, packaging where applicable) and the designated
  reviewer records GO for that same commit with the documented host/evidence
  tiers.
- Reviewer: the implementing ZCode agent (GLM-5.3) designated by the owner;
  shared context, no claim of independent or blinded review.
- Authorized publication: merge commit (no squash), annotated immutable tag,
  non-draft GitHub Release with the committed notes, revision-bound generated
  assets, and the matching Wiki handbook published from a committed public
  docs ref after the tag exists.
- Tag control: only the version-tag creation restriction may be temporarily
  disarmed for this publication. Preserve update/deletion restrictions,
  restore the original creation rule immediately, and verify rejection of a
  seeded probe. No branch protection or required check is waived.
- Post-publication main commits: rotating the handbook `Applies to` pins, the
  editorial stager `TAG`, the v7.1.0 wiki snapshot, and README receipt links
  is authorized after the tag exists, following the v7.0.0 precedent (the
  current handbook and stager landed after that tag).

The annotated tag and attached publication receipt must bind the actual
candidate, check runs and GO. Post-push re-arm facts belong in the
publication receipt, not in a rewritten tag. A failed gate holds dependent
publication.

This authorization names no future merge SHA. It does not authorize moving an
existing release tag, publishing on a failing integrity gate, or erasing
historical evidence.
