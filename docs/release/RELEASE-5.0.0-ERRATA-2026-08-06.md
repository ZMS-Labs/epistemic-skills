# Release 5.0.0 errata — 2026-08-06

This erratum supplements, but does not rewrite, the historical facts in
[`RELEASE-5.0.0.md`](RELEASE-5.0.0.md) and the published GitHub Release.

It exists because the original release record is materially honest about the
waived publication gate but contains stale exact-commit references and does not
account explicitly for every gate row in `RELEASING.md`.

## 1. Correct immutable identity

| Object | Correct value |
|---|---|
| release tag | `v5.0.0` |
| annotated-tag object | `441f12f8f5bd0943ae30bb96a355bc7789cfdcd5` |
| peeled tag target / release commit | `9c8d8dbb72418cedb1e4a617b2805bee0a0c4525` |
| `main` at publication | `9c8d8dbb72418cedb1e4a617b2805bee0a0c4525` |
| GitHub Release target | `9c8d8dbb72418cedb1e4a617b2805bee0a0c4525` |

The original table's repeated references to `3a18cd3` identify an intermediate
candidate, not the published release commit.

## 2. Exact-commit workflow evidence

The stale SHA does **not** mean the final tag escaped the claimed checks. The
following runs completed successfully on the exact release commit:

| Evidence | Run | Result on `9c8d8dbb72418cedb1e4a617b2805bee0a0c4525` |
|---|---:|---|
| deterministic / stdlib suite | `31128924884` | success; required steps passed and the merge-base-only step was correctly skipped outside a PR context |
| CodeQL | `31128924306` | success for Actions, JavaScript/TypeScript, and Python |
| release security | `31128925378` | success; the planted-secret positive control and full-history scan both passed |

Accordingly, the release note's top-level statement that items 5 and the secret-
scan portion of item 6 passed on the exact tag is supported. The table should cite
the final SHA and these runs.

## 3. Gate accounting corrected

| Gate | Correct historical status | Evidence limit |
|---|---|---|
| item 4 — version and pinned-link alignment | **MET** | the release record identifies the live surfaces and the repointed routine-fast-path link |
| item 5 — deterministic suite, DCO/manifest/JSON checks, CodeQL | **MET on the final tag** | exact workflow runs above; this does not establish design soundness |
| item 6a — redacted full-history secret scan | **MET on the final tag** | exact security run above, including positive control |
| item 6b — v5-specific public-content review | **NOT MET** | no pre-publication v5 artifact exists, and the post-release review found newly added private-repository and user-specific path references contrary to the repository's established scrub policy |
| item 6c — provenance/license review as a distinct v5 record | **UNESTABLISHED IN THE RELEASE RECORD** | no immutable v5-specific provenance review artifact was located |
| item 7 — supported harness live exercise or explicit verification tiers | **UNESTABLISHED IN THE RELEASE RECORD** | the notes discuss clean-room execution and installed-estate behavior but do not provide a complete harness-by-harness tier table |
| item 8 — independent Gauntlet publication review reaching GO | **WAIVED / NOT MET** | explicitly waived by the owner; no pre-publication panel, arbitrator, Conflict Ledger, or GO exists |
| publication identity | **MET** | annotated tag, peeled target, `main`, and GitHub Release target agree |

The item 6b correction is supported by
[`PUBLIC-CONTENT-POST-RELEASE-REVIEW-5.0.0-2026-08-06.md`](PUBLIC-CONTENT-POST-RELEASE-REVIEW-5.0.0-2026-08-06.md).
That review found a user-specific local path and direct private-fleet repository
coordinates in files added by v5. A passing credential-pattern scan does not
establish that public-content boundaries were respected.

`UNESTABLISHED IN THE RELEASE RECORD` remains deliberately narrower than
`FAILED`. It is used only where the missing immutable evidence coordinate prevents
a pass claim but no contrary artifact finding has been established. Item 6b is no
longer in that category.

## 4. Post-release judgment review

An independent cross-family post-release review is recorded at
[`POST-RELEASE-INDEPENDENT-REVIEW-5.0.0-2026-08-06.md`](POST-RELEASE-INDEPENDENT-REVIEW-5.0.0-2026-08-06.md).

Its status is:

- **post-release**, not pre-publication;
- **manual-degraded**, not a fully isolated Gauntlet panel;
- **NO-GO for retrospective certification or a claim of full design
  implementation**; and
- **not a recommendation to move or delete the immutable release tag**.

The review cannot satisfy item 8 retroactively. It adds the judgment record that
was missing and supplies conditions for a successor release.

## 5. Capability-language correction

The release says:

> watch notices, health assesses, triage diagnoses, did-it-land verifies the fix
> took.

The more exact statement is:

> `watch` specifies the external observer and governs its inert preparation,
> bounded enablement, kill-switch exercise, deliberate proof crossing, and alert
> receipt; `health` assesses observed state against declared bounds; `triage`
> identifies a cause from discriminating observations; and `did-it-land` verifies
> runtime effect.

The package ships agent disciplines in Markdown. It does not itself ship the
scheduler, probe, alert destination, or unattended runtime process.

## 6. Efficacy status is unchanged

Behavioral superiority remains **UNESTABLISHED**. The four-arm campaign found no
arm separation (`p=0.875`; A=5, B=4, C=7, D=4 of 18). Neither publication, this
erratum, nor the post-release review converts that result into support.

## 7. Publication-body maintenance

After this erratum is merged, the mutable GitHub Release body should be amended
only to:

1. replace the intermediate SHA with the final release SHA and run IDs;
2. link this erratum, the public-content review, and the post-release judgment
   review;
3. record item 6b as **NOT MET**, item 6c and item 7 as unestablished, and item 8
   as **WAIVED / NOT MET**;
4. identify the current-tree scrub and successor-release work without implying
   the tagged tree changed; and
5. preserve the statement that no GO existed at publication.

The tagged tree must not be changed or re-created. Any artifact correction ships
under a new semantic version.