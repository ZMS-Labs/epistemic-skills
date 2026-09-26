# V7.2 publication authorization

On 2026-09-26, the repository owner instructed the Codex agent in this task to
“verify/validate/confirm and then actually ensure real release, if its ready”
for Epistemic Skills 7.2. This is conditional authorization to finish the
release when the repository's exact-candidate gates and designated review pass.
It does not turn an unmet gate into a pass.

- Release pull request: [#263](https://github.com/ZMS-Labs/epistemic-skills/pull/263),
  from `release/7.2.0` into `main`.
- Version and annotated tag: `7.2.0` / `v7.2.0`.
- Committed release-note body: `docs/release/RELEASE-7.2.0.md`.
- Candidate: the merge commit produced by PR #263 after the required PR checks
  pass. No future merge SHA is asserted here.
- Reviewer: the Codex agent assigned in this task to verify the release. It
  prepared the release rotation and reviews from the same task context; the
  judgment is neither blind nor independent. The review record must identify
  the exact merge commit and any unresolved material finding.
- Firing condition: every exact-candidate integrity gate passes, each supported
  harness has an honest evidence tier, and the designated reviewer records GO
  for that same commit with no unresolved material P1/P2 finding.
- Authorized publication after that condition: merge PR #263 with a merge
  commit; create and push the immutable annotated tag; publish a non-draft
  GitHub Release using the committed note verbatim and revision-bound bundles;
  attach the exact-gate, review, and publication receipts; then publish and
  verify the matching Wiki handbook from a committed public documentation ref.
- Tag control: temporarily remove only the `creation` rule from
  `protect-version-tags` for this publication. Preserve update/deletion rules,
  restore the original rule in the same sitting, and verify rejection with a
  seeded probe. Record disarm in the tag message and re-arm/probe facts in the
  attached publication receipt. No branch rule or integrity gate is waived.

An incorrect candidate, adverse review, or failed integrity gate holds
publication. This authorization does not permit moving an existing tag or
rewriting earlier release evidence.
