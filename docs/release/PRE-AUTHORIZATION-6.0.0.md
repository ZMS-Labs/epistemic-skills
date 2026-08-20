# Pre-authorization — v6.0.0

**STATUS: ADOPTED** — by operator direction under D23, transcribed by the
implementing lineage.

> The repository owner (GitHub login `SternOne`) pre-authorizes publication of
> v6.0.0 on the terms in this document: the commit produced by merging pull
> request **#206**, and only that commit, if and only if every condition in
> "The firing condition" holds.

**Provenance — read this before relying on the adoption.** This block was
written and committed by the implementing lineage on the operator's session
instruction, recorded verbatim as **D23** in
`docs/v6/operator-decision-record-2026-08-20.md`. It is **not** a commit
authored by the operator's own account. The earlier edition of this file
required that, and the operator amended the requirement — which they may do,
since both governing documents are repo-authored and the acceptance procedure
says so in terms.

An auditor who considers session-directed adoption insufficient should treat
this authorization as carrying that limit, and say so rather than assuming a
signature that is not here. Nothing in this file asserts the operator typed
these bytes.

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

## Superseding this adoption

The operator may replace the status block above with one committed under their
own account at any time. That would strengthen the provenance without changing
any term, and no act taken under this adoption needs to be undone for it.
