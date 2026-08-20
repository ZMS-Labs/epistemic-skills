# Pre-authorization — v6.0.0

> ## ⚠ STATUS: DRAFT — NOT ADOPTED. THIS AUTHORIZES NOTHING.
>
> Drafted by the implementing lineage for the repository owner's adoption. It
> takes effect only when the owner replaces this block with the ADOPTED block at
> the bottom of this file, **in a commit authored by their own account**, before
> the candidate is minted.
>
> A draft committed by the implementing lineage is not an authorization, and
> neither is any statement in a chat transcript. `RELEASING.md` and
> `OPERATOR-ACCEPTANCE-PROCEDURE.md` both say so in terms, and three independent
> gates have ruled on it.

## Why this document exists before the candidate does

`RELEASING.md` step 7 once required a committed line naming the candidate's own
SHA. Writing that line changed the tree and produced a different SHA, so the
exact-commit checks and the independent verdict described a commit that was no
longer the candidate. The sequence was not executable as written.

The cure, adopted 2026-08-20: **nothing that binds a SHA is written after that
SHA exists.** Authorization moves *before* the candidate, where it names a
determinate act rather than a hash; the resolved SHA is carried afterwards by
the annotated tag object, which names its target without altering it.

## What is being authorized

| Field | Value |
|---|---|
| Version | **6.0.0** |
| Pull request to be merged | **#206** |
| Merge method | **merge commit** (not squash — a squash attributes the commit to the merger, making any sign-off trailer a false attestation) |
| Candidate | the commit produced by merging #206, and no other commit |
| Release-note path | `docs/release/RELEASE-6.0.0.md` |
| Tag | `v6.0.0`, annotated, on that candidate |
| Release | non-draft, body verbatim from the release note, targeting that tag |

## The firing condition

This authorization fires **if and only if all** of the following hold against
the commit produced by merging #206:

1. **All five gating workflows run at that exact commit and report the expected
   conclusions** — `epistemic-flexibility`, `release-security`, `openai-bundles`,
   `commission-watch-contract`, and `mission-custody-contract`. Each must be
   explicitly dispatched; path-filtered workflows do not fire on a docs-only
   diff, and a missing run is not a passing run.
   - `mission-custody-contract` is expected **red at job level**: its
     dispatch-only `contract-macos` probe fails on case-insensitive filesystems
     (`KL-MACOS-162`). Its required `contract` job must be green. Any other
     failure voids this condition.
2. **An operator-dispatched independent publication gate returns GO** against
   that exact commit. A verdict against any other SHA does not transfer.
3. **The D8 Step-7b cross-family consult is run** at GO posture, or explicitly
   waived in writing by the owner with scope, revisit trigger and exit criterion.
4. **Operator acceptance is recorded** in the form
   `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` defines — the `operator_acceptance`
   object plus a consent artifact the owner authored or echo-certified. An
   acceptance in chat, in a commit message, or as an enum flip is not an
   acceptance.

If any condition fails, this authorization does not fire, and no tag may be
created. Fix forward, mint a new candidate, and a fresh pre-authorization is
required for it — this one names #206 and expires with it.

## What it does not authorize

Any commit other than the merge of #206. Any version other than 6.0.0. Moving or
reusing a tag. Altering `protect-version-tags` beyond the disarm/re-arm of the
tag act itself. Publishing on a CONDITIONAL or NO-GO verdict. Substituting the
implementing lineage's judgment for the independent gate's.

## The owner still holds the stop

This is an authorization of a conditional act, not a pre-commitment to publish.
The owner performs the tag act personally, and it is revocable up to the moment
of the push: an owner who reads the verdict and dislikes it simply does not
disarm the ruleset. That is the whole of the trade this design makes, and it is
stated here rather than buried.

---

## ADOPTED block — the owner replaces the status block above with this

```
STATUS: ADOPTED.

I, <GitHub login>, as repository owner, pre-authorize publication of v6.0.0 on
the terms in this document: the commit produced by merging pull request #206,
and only that commit, if and only if every condition in "The firing condition"
holds. Adopted <RFC3339 UTC timestamp>.
```

Adopt it in a commit authored by your own account. Nothing else in this file
needs to change; if any term above is wrong, edit that term rather than working
around it.
