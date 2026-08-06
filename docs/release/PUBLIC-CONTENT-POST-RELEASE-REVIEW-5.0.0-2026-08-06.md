# Public-content post-release review — v5.0.0

**Review date:** 2026-08-06  
**Immutable subject:** `v4.1.0..v5.0.0`  
**Release commit:** `9c8d8dbb72418cedb1e4a617b2805bee0a0c4525`  
**Status:** post-release review; not evidence that gate item 6b ran before publication

## Verdict

**Gate item 6b was not merely unrecorded; it was not met.**

A targeted review of the v5 additions found public-tree content that conflicts
with the repository's previously recorded public-content policy. The July 21
review explicitly treated direct private-fleet repository identifiers and
user-specific local checkout or profile paths as scrub targets, retaining only a
local path that referred to this public repository itself.

`v5.0.0` added new files containing both classes of information. A conforming
pre-publication review applying the established policy should have caught and
scrubbed them before tag creation.

This finding is a **P2 release-integrity and privacy-boundary defect**. No
credential value or private key is alleged here, and the exact-tag full-history
secret scan passed. The problem is disclosure of private-repository identity,
user-specific path structure, and operator-estate topology in a public artifact.

The exact identifiers are intentionally **not duplicated in this review**. Their
file locations and disclosure classes are sufficient to audit and remediate the
current tree without reproducing the material in a second public document.

## Governing prior policy

`docs/release/PUBLIC-RELEASE-REVIEW-ADDENDUM-2026-07-21.md` records that the public
review swept, among other things:

- private fleet-repository identifiers;
- user-specific local checkout and profile paths;
- internal topology and device identifiers; and
- accidental fleet telemetry.

That review relocated private fleet material and scrubbed direct private-repo
paths from public design documents. Its only explicit local-path exception was a
path to the public `epistemic-skills` checkout itself.

This post-release review applies that already-adopted boundary; it does not invent
a stricter rule after publication.

## Confirmed v5 regressions

### 1. User-specific absolute path in newly added evidence

`docs/evidence/2026-08-06-context-audit-firing-probe.md` was added between the two
release tags and contains a user-specific absolute profile/plugin path.

The username and absolute home-directory prefix are not required to preserve the
experimental result. The public form should use a platform-neutral placeholder,
for example:

```text
<user-home>/.claude/plugins/**/skills/*/SKILL.md
```

**Current-tree disposition:** scrubbed on the draft corrective branch in commit
`1eab8d47649fffb3f47c81863803c4c5ca225ba6`; not yet on `main` until the PR is
merged.

### 2. Private repository coordinate in newly added evidence

The same newly added evidence file records a private fleet-repository identifier
paired with an exact private commit coordinate.

The public result needs only the fact that superseded commands were removed from
the operator's private command estate. The public form should be:

```text
<private-fleet-repo>@<commit>
```

The exact reciprocal coordinate may be preserved in the private repository or
another owner-controlled record if provenance is still needed.

**Current-tree disposition:** scrubbed on the draft corrective branch in commit
`1eab8d47649fffb3f47c81863803c4c5ca225ba6`; not yet on `main` until the PR is
merged.

### 3. Private checkout identity in the newly added design document

`docs/superpowers/specs/2026-08-06-epistemic-skills-v5-design.md` was added in the
same release and names a private fleet checkout while locating a vendored Helix
copy beneath its skills directory.

The public design decision is that a duplicate exists in a private fleet checkout
and requires disposition. The public form should be:

```text
<private-fleet-checkout>/skills/
```

**Current-tree disposition:** open and tracked in issue #105. It is not silently
classified as resolved by the two evidence-file scrubs above.

### 4. Operator-estate telemetry requiring an explicit classification

The two files also contain detailed installed-estate observations and private
command names: loaded skill counts, command-estate counts, cache/marketplace
behavior, and names of operator-specific commands.

Some of that evidence has genuine public methodological value. Unlike the three
direct references above, it is not automatically classified as private by this
review. It must, however, receive an explicit line-by-line disposition rather
than being implicitly accepted because the secret scanner stayed green.

The classification choices are:

1. retain because the public explanatory value exceeds the disclosure cost;
2. generalize names/counts while preserving the measured relationship;
3. relocate the operator-specific receipt to a private evidence store and retain
   only a redacted public summary; or
4. remove if it has no durable public value.

## What the security workflows do and do not establish

The exact-tag release-security workflow passed, including its planted-secret
positive control and full-history scan. That is strong evidence that the tagged
history did not match the scanner's credential patterns.

It is not a public-content review. A private repository identifier, a local
username, or a detailed estate receipt need not resemble a secret token. The
passing scan therefore does not conflict with this finding; it answers a
different question.

## Required remediation

### Current public tree

- [x] scrub the user-specific absolute profile/plugin path on the draft corrective
  branch;
- [x] scrub the private repository coordinate on the draft corrective branch;
- [ ] scrub the private checkout identity in the design document;
- [ ] merge the completed direct-reference scrubs to `main` after review;
- [ ] review every operator-estate detail added by v5 and record retain,
  generalize, relocate, or remove for each material category;
- [ ] rerun the July public-content pattern set across the full current tree and
  the full `v4.1.0..HEAD` diff;
- [ ] add seeded positive controls proving the review automation detects both a
  private-repository identifier and a user-specific local path; and
- [ ] ensure future release notes point to the immutable public-content review
  receipt for the exact candidate.

### Historical release

- do **not** move, recreate, or rewrite the `v5.0.0` tag;
- describe item 6b as **NOT MET**, not `MET` or merely unestablished;
- link this review from the mutable GitHub Release body after the corrective PR
  merges; and
- ship any corrected artifact under a new semantic version.

### Git history

Scrubbing `main` does not remove the strings from the published tag or prior Git
objects. History rewriting is an owner-gated risk decision and is not performed
by this review. Because the confirmed disclosures are identifiers/topology rather
than credentials, the immediate action is current-tree remediation and an honest
record, followed by a separate owner decision on history treatment.

## Corrected gate accounting

| Gate component | Historical status for v5.0.0 | Reason |
|---|---|---|
| full-history credential-pattern scan | **MET** | exact-tag workflow passed with a positive control |
| v5-specific public-content review | **NOT MET** | no pre-publication artifact exists and post-release review found content contrary to the established scrub policy |
| provenance/license review | **UNESTABLISHED AS A DISTINCT v5 RECORD** | no immutable v5-specific artifact located |

## Bottom line

The release's security evidence remains valid within its scope. The broader item
6 claim does not. `v5.0.0` shipped public-content regressions that a conforming
application of the repository's own prior policy should have removed.

The durable record is:

> **Secret scan passed; v5 public-content gate did not; direct private-repository
> and user-specific-path references require current-tree remediation; immutable
> tag remains unchanged; history treatment remains an explicit owner decision.**