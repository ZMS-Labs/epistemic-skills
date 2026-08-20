# Proposal — a non-self-invalidating publication authority sequence

**Status: PROPOSAL. Not adopted, not in force.** It amends `RELEASING.md`, a
governing document, so it requires the repository owner's decision and — per
ruling **OAI-P1-03** — prospective independent review *before* the next
candidate is cut. Nothing here may be relied on until both happen.

## The defect being cured

`RELEASING.md` Procedure steps 4, 5 and 7 form a fixed-point contradiction:

- **Step 4** — the merge commit is the candidate; every exact-commit workflow
  re-runs against that SHA; "any correction creates a new candidate and
  invalidates earlier exact-commit evidence."
- **Step 5** — the independent gate freezes that exact candidate as its subject.
- **Step 7** — a line naming "the exact candidate SHA authorized" must be
  **in the committed release notes** before the tag act.

Committing the step-7 line changes the tree, producing a new SHA. The checks
from step 4 and the verdict from step 5 then describe a commit that is no
longer the candidate. The sequence cannot be executed as written.

The v6.0.0 lineage attempted to resolve this inside the release note, by
resolving identity by description and enumerating the one-commit delta.
OAI-P1-03 rejected that: *"The release note may not self-waive the governing
text."* It is correct. A subordinate document cannot grant itself an exemption
from the document that governs it. The cure has to be in `RELEASING.md`.

## The proposed sequence

The principle: **nothing that binds a SHA may be written after that SHA
exists.** Authorization moves to a conditional act committed *before* the
candidate is minted, plus a tag object written *after* — and a tag object can
name its own target without changing it.

1. **Pre-authorization (committed, before the candidate exists).** The owner
   commits an authorization record naming: the pull request to be merged, the
   version, the release-note path, the gate that must return GO, and the
   explicit condition — "I authorize publication of the commit produced by
   merging PR #N, and only that commit, if and only if the independent
   publication gate returns GO against it." It names no SHA because none
   exists yet. It is an authorization of a *determinate act*, not of an
   unknown artifact.
2. **Mint the candidate.** Merge. The merge commit is the candidate, `C`.
3. **Exact-SHA evidence at `C`.** Every gating workflow runs at `C`, including
   any whose path filters would not otherwise fire (see below).
4. **Independent gate at `C`.** Operator-dispatched, cross-family where
   available.
5. **The tag act.** If GO: disarm, create the annotated tag on `C`, re-arm,
   seeded probe. **The annotated tag object carries the resolved
   authorization**: verdict path and run id, the exact 40-hex `C`, the owner's
   identity, and the disarm/re-arm timestamps. The tag names `C` without
   altering it.
6. **The Release** is created from the committed note verbatim, targeting the
   tag.

`C` is identical across steps 3, 4, 5 and 6. Nothing is committed between the
candidate and the tag. The fixed point is gone.

### Falsifier for this proposal

Simulate the amended steps from a frozen candidate through tag creation;
recompute the SHA after every required write. **The proposal fails if any
required write occurs after step 2.** By construction there is exactly one —
and it is a tag object, which is not part of the tree.

### What this trades away, stated plainly

The owner authorizes a *conditional act* before reading the verdict, rather
than authorizing an artifact after reading it. That is a real reduction in the
authorization's information content, and it should not be waved past. Two
things bound it: the condition is strict (GO, at that exact commit, from an
operator-dispatched independent gate — anything else and the authorization
does not fire), and the owner still personally performs the tag act, which
remains revocable up to the moment of the push. An owner who reads the verdict
and dislikes it simply does not disarm.

The alternative — a defined verdict-transfer rule permitting an
authorization-only delta — was considered and is weaker: it requires the
governing text to declare some commits' evidence transferable, which
reintroduces exactly the judgment call OAI-P1-03 says must not live in a
subordinate document.

## Two companion corrections

**Author-matching DCO on the candidate (OAI-P1-01).** Squash-merging attributes
the commit to whoever merged it, so a sign-off trailer naming anyone else is an
author mismatch — and asserting a sign-off for an identity that did not author
the commit is a false attestation, worse than an absent trailer. Two lawful
remedies: the owner signs off their own merge commit, or the release candidate
is created with a **merge commit** rather than a squash. A merge commit is
exempt under the existing `is_merge()` rule (the same default GitHub's own DCO
app applies), and it preserves the individually signed commits in history
rather than discarding their authorship. The second is recommended.

**Path-filtered workflows never fire on a docs-only candidate (OAI-P1-02).** A
release candidate whose diff touches only `docs/` will not trigger any
path-filtered workflow, so its exact-SHA evidence is silently incomplete —
which is exactly what happened at `d0165bd0`, where two of five gating
workflows never ran. Step 3 above must therefore require an explicit
`workflow_dispatch` of every gating workflow at the candidate, and the release
record must show all of them at that one SHA. A missing run is not a passing
run.
