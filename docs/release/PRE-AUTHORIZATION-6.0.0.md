# Pre-authorization — v6.0.0 (exception release)

**STATUS: ADOPTED** — by operator direction under **D24**, transcribed by the
implementing lineage. This edition **supersedes** the edition that named pull
request #206; that candidate is superseded and its authorization expired with it.

> The repository owner pre-authorizes publication of v6.0.0 on the terms in this
> document: the commit produced by merging the pull request named below, and only
> that commit, if and only if every condition in "The firing condition" holds.
>
> This is an **exception release** under `RELEASING.md` § "Independent judgment
> gate". The owner has read four NO-GO verdicts and elected to publish anyway.

**Provenance — read this before relying on the adoption.** This block was
written and committed by the implementing lineage on the operator's session
instruction, recorded verbatim as **D24** in
`docs/v6/operator-decision-record-2026-08-20.md`. It is **not** a commit authored
by the operator's own account, and — because this repository is pushed with the
same credential its automation runs under — it could not be made
byte-distinguishable from one even if it claimed to be. Nothing in this file
asserts the operator typed these bytes.

The one act that cannot be transcribed is the disarm. See "Why the disarm is the
authorization" below.

## Why this document exists before the candidate does

`RELEASING.md` step 7 once required a committed line naming the candidate's own
SHA. Writing that line changed the tree and produced a different SHA, so the
exact-commit checks and the independent verdict described a commit that was no
longer the candidate. The sequence was not executable as written; an
operator-dispatched cross-family review found it.

The cure, adopted 2026-08-20: **nothing that binds a SHA is written after that
SHA exists.** Authorization moves *before* the candidate, where it names a
determinate act rather than a hash; the resolved SHA is carried afterwards by the
annotated tag object, which names its target without altering it.

## Why the disarm *is* the authorization

The `protect-version-tags` ruleset carries `creation` with **no bypass actors**.
No actor can create `refs/tags/v*` while it is armed — not automation, not an
admin, not the owner. That was deliberate: with a shared push credential, an
admin bypass would have exempted exactly the actors the rule exists to constrain.

The consequence, which the fourth review stated and this document accepts rather
than works around: **every other artifact of authorization in this repository is
forgeable by the implementing lineage, and the ruleset change is not.** A
decision record can be transcribed. A commit trailer can be written. A pre-
authorization can be adopted by direction. None of them requires the operator's
hands. Disarming a repository ruleset requires settings access no agent in this
environment holds.

So the disarm is not a step *before* the authorization. It is the authorization,
in the only form this repository can make unforgeable. This file fixes what the
disarm will mean; the operator's hand supplies that it happened.

## What is being authorized

| Field | Value |
|---|---|
| Version | **6.0.0** |
| Pull request to be merged | **#207**, the v6.0.0 final release PR from `release/v6.0.0-final` |
| Merge method | **merge commit** (not squash — a squash attributes the commit to the merger, making any sign-off trailer a false attestation) |
| Candidate | the commit produced by that merge, and no other commit |
| Release-note path | `docs/release/RELEASE-6.0.0.md` |
| Tag | `v6.0.0`, annotated, on that candidate |
| Release | non-draft, body verbatim from the release note, targeting that tag |
| Release class | **exception release** — the notes must say so; they must never say "conforming" |

## The firing condition

This authorization fires **if and only if all** of the following hold against the
commit produced by that merge:

1. **All five gating workflows run at that exact commit and report the expected
   conclusions** — `epistemic-flexibility`, `release-security`, `openai-bundles`,
   `commission-watch-contract`, and `mission-custody-contract`. Each must be
   explicitly dispatched; path-filtered workflows do not fire on a docs-only
   diff, and a missing run is not a passing run.
   - `mission-custody-contract` is expected **red at job level**: its
     dispatch-only `contract-macos` probe fails at step 8, on the tests
     `distinct-real-file-untouched` and `distinct-both-files-tracked-separately`,
     because macOS default volumes fold `straße.txt` and `strasse.txt` to one
     physical file under full Unicode case folding (`KL-MACOS-162`).
     Its required `contract` job must be green across all 12 steps. **Any other
     failure, in any job, voids this condition.**
2. **The release note carries the exception block** — all five disclosures
   `RELEASING.md` § "Independent judgment gate" requires, present in the
   committed file *before* the tag is created, and the release described as an
   exception release rather than a conforming one.
3. **Every integrity gate is met on its own terms.** RG-1 accuracy, RG-4
   alignment, RG-5 evidence, RG-6 security and provenance. **D24 does not reach
   these and cannot waive them.** If any integrity finding is open at the
   candidate, this authorization does not fire, regardless of the owner's wish to
   ship.
4. **The D8 cross-family consult is recorded as owed and carried forward** to
   6.1.0, with scope, revisit trigger and exit criterion, in both the release
   note and the decision record. It is *not* discharged by this release and this
   condition does not pretend otherwise — it requires the debt to be visible, not
   paid.

If any condition fails, this authorization does not fire and no tag may be
created. Fix forward, mint a new candidate, and a fresh pre-authorization is
required for it — this one names **#207** and expires with it.

### What changed from the superseded edition, and why

The prior edition's conditions 2 and 4 required an **operator-dispatched GO** and
an **operator acceptance object plus consent artifact**. Neither can be satisfied
on this lineage: four gates have returned NO-GO and none will return GO, and the
acceptance procedure's own text ("an acceptance in chat is not an acceptance")
made the second condition unsatisfiable by the only channel available. Together
they made the prior edition circular — it could not fire on either branch.

They are not quietly relaxed here. They are **replaced by an exception the
release documents state in full**, which is the path `RELEASING.md` already
provides for exactly this situation. The difference between relaxing a condition
and invoking a documented exception is that the exception leaves a record saying
what was not done. That record is conditions 2 and 4 above.

## What it does not authorize

Any commit other than the merge of **#207**. Any version other than
6.0.0. Moving or reusing a tag. Altering `protect-version-tags` beyond the
disarm/re-arm of the tag act itself, or leaving it disarmed past the sitting.
Describing the result as a conforming release, or the NO-GO verdicts as
superseded, discharged, or resolved. Waiving any integrity gate. Publishing
6.1.0 under a second RG-8 exception without first discharging D8.

## The owner still holds the stop

This is an authorization of a conditional act, not a pre-commitment to publish.
The owner performs the tag act personally, and it is revocable up to the moment
of the push: an owner who changes their mind simply does not disarm the ruleset.
That is the whole of the trade this design makes, and it is stated here rather
than buried.

---

## Superseding this adoption

The operator may replace the status block above with one committed under their
own account at any time. Given the shared-credential concession stated above,
that would change the provenance narrative but not the cryptographic facts, and
no act taken under this adoption needs to be undone for it. The disarm remains
the load-bearing act either way.
