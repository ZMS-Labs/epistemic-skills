# Releasing epistemic-skills

A release is an immutable support point: one semantic version maps to one Git
commit, one annotated Git tag, one committed release-note file, and one non-draft
GitHub Release. `main` is the rolling channel; a version tag is the reproducible
channel.

This document governs every future release. Release-specific risk acceptances,
review records, verification matrices, and migration notes belong under
`docs/release/` and must identify the exact version and commit they cover.
Historical release records remain authoritative for what happened at their own
coordinates; this procedure must not be rewritten to imply that an earlier gate
ran when it did not.

## When to release

- **Patch** (`x.y.Z`): compatible correctness, packaging, installation, security,
  or documentation fixes that materially affect users.
- **Minor** (`x.Y.0`): a new skill, contract, harness capability, or materially
  expanded behavior that remains backward compatible.
- **Major** (`X.0.0`): an incompatible trigger, output contract, schema,
  installation, routing, or package-boundary change.

Do not release internal audit prose or relay bookkeeping alone. Release when a
coherent user-visible change has landed and the gate below can bind it to a
verified snapshot.

## Terms

- **Release candidate:** the exact commit proposed for the version tag.
- **Conforming release:** every required gate is met on the release candidate.
- **Exception release:** the owner authorizes publication despite an explicitly
  named unmet judgment gate. An exception changes the publication decision; it
  does **not** change the gate's truth value.
- **Waived:** not run or not met, with explicit owner authorization to publish
  anyway. `WAIVED` is never a synonym for `MET`, `PASS`, or `GO`.
- **Verification tier:** the honest level assigned to a harness surface when live
  execution is unavailable. A tier records the limitation; it does not silently
  upgrade the surface to verified.

## Gate classes and exception semantics

The gate separates artifact integrity from publication judgment.

### Integrity gates

The version/link alignment, deterministic checks, CodeQL, provenance checks,
full-history secret scan, public-content review, and publication identity
assertions are integrity gates. Do not create a tag while one is failing or
unrecorded. Fix the candidate, rerun the gate on the new exact commit, and only
then publish.

### Harness-evidence gate

Supported harness surfaces must either be exercised live or assigned an explicit
verification tier in the release notes. Missing access may degrade the tier; it
may not disappear from the record.

### Designated-reviewer judgment gate (v7 onward)

The owner-designated reviewer judges the frozen candidate against accepted
requirements and recorded evidence. The owner may designate the implementing
agent. No independent panel or different model family is a release prerequisite.
Report actual reviewer identity, shared context and evidence limits; a self-check
does not become blinded or independent through a role label.

A conforming release requires a recorded GO on the exact candidate with material
findings resolved. Preserve dissent and distinguish unmet requirements, user-owned
tradeoffs and optional improvements. Recheck changed behavior and dependencies;
preserve unaffected evidence. Budget exhaustion does not establish GO or require
an unlimited review cycle. Publication authority and integrity gates remain
separate. A historical v6 independent-review exception remains historical; this
policy does not retroactively change it.

If the owner authorizes publication with an unmet current judgment gate, preserve
that unmet gate and the authorization in an explicit exception record. Missing
independence alone is not a v7 exception because it is no longer required.

#### Standing exception route and historical D25 terms

An owner exception remains available for an actual unmet publication-judgment
gate (gate 8). Before tagging, the committed release notes must identify the
unmet requirement, actual review verdict or missing review, evidence limits,
remaining material findings, and explicit owner authorization. Record the named
cost and any accepted gap's owner, scope, revisit trigger, and exit criterion.
The release notes, annotated tag message, and handbook entry must label the
result an exception release; `WAIVED` or `UNMET` never becomes `GO`, and adverse
verdicts remain in the evidence record.

No integrity gate is waivable. An accuracy defect is repaired rather than
excused, and every applicable integrity gate still runs on the exact candidate.
Missing independence alone creates neither an exception nor a standing
cross-family review obligation under the v7 designated-reviewer policy.

**Historical v6 policy:** D25 made the exception route permanently available
under the then-required independent-judgment gate. Its original five disclosures,
`KL-SELF-GO` treatment, and carried cross-family obligations are preserved in the
[immutable v6 release policy](https://github.com/ZMS-Labs/epistemic-skills/blob/9705f70aec1285597a6ef2a341cede80010c1dcb/RELEASING.md#the-exception-route-is-standing-not-emergency-d25).
Those terms describe the v6 regime and its historical records; they do not impose
independence requirements on v7 or retroactively change any v6 verdict.

## Release gate

Before creating the tag, record every row below against the exact release
candidate.

1. **Candidate identity and scope**
   - `main` is clean and synchronized with `origin/main`.
   - The intended changes and migration boundary are frozen.
   - The release-note path and proposed semantic version are named.
2. **Release-specific decisions and risk acceptance**
   - Any accepted gap has an owner, bounded scope, revisit trigger, and exit
     criterion.
   - Acceptance never overwrites contrary evidence or converts an invalid epoch
     into a pass.
   - No wildcard waiver is permitted.
3. **Evidence retention**
   - Blinded campaigns, negative controls, dissent, terminal failures, and prior
     null results remain at immutable coordinates.
   - A corrected epoch may supersede an earlier result but never erase it.
   - Before deleting a skill or capability directory, inventory `evals/`,
     `results/`, `runs/`, and references; relocate evidence whose subject is
     broader than the deleted seat.
4. **Version and link alignment**
   - Every version-bearing live manifest, README statement, install example,
     package-integration expectation, and release-note statement agrees on the
     proposed version.
   - Every repository path referenced by a rewritten version-pinned URL exists in
     the candidate tree. A blind version bump can mint immutable links to paths
     that never existed at that tag.
   - Live user-facing architecture words—entry point, router, skill counts,
     retired names—agree with the candidate.
5. **Deterministic and static-analysis evidence**
   - The complete deterministic suite, DCO checks, manifest parity,
     committed-JSON checks, and all required CodeQL matrices pass on the exact
     candidate commit.
   - A skipped step is acceptable only when its precondition is inapplicable and
     the reason is recorded; run-level green may not conceal a failed required
     step.
   - Suite verdicts key on the **required job set** of each workflow on its
     push/pull event, not on the run-level conclusion of a manual dispatch.
     A workflow may carry dispatch-only diagnostic jobs (for example, a probe
     built to settle a filed platform claim). Such a job's failure reddens the
     run conclusion without falsifying any required-step claim, provided
     (a) the job's non-gating purpose is documented in the workflow file,
     (b) the failure is the diagnostic's designed output — a settled, disclosed
     finding recorded on its issue — and (c) the release record names the exact
     failing step and tests. Any other red, in any job of a suite dispatched at
     the candidate, fails this gate. (Ruling lineage: the v5.1.0 publication
     gauntlet, panel 2, CL-1/CL-2 — `docs/gauntlet-runs/es-v510-publication-2026-08-15/`.)
6. **Security, public content, and provenance**
   - A redacted full-history secret scan passes on the exact candidate, including
     a positive control proving the scanner detects a planted secret.
   - A release-diff and current-tree public-content review covers private paths,
     internal topology, credentials, personal data, and accidental telemetry.
     Run `.github/scripts/check_public_content.py --self-test` and
     `.github/scripts/check_public_content.py` on the exact candidate; both must
     exit 0. Pattern hits outside the documented allowlist fail closed.
   - Public-content findings and dispositions are recorded at an immutable path.
   - Provenance and license surfaces remain accurate.
7. **Supported harness evidence**
   - Each supported harness is exercised live against the candidate or receives
     an explicit verification tier and limitation in the release notes.
   - Installation source, loaded copy, cache behavior, reload requirements, and
     duplicate-install risks are tested where material.
   - The notes disclose absent qualifying results rather than implying coverage.
8. **Designated-reviewer publication judgment**
   - Freeze the candidate before review and record the designated reviewer.
   - Judge requirement fulfillment, material findings and evidence limits.
   - A conforming release requires `GO` with no unresolved material P1/P2.
   - `CONDITIONAL`, `NO-GO` or an unperformed judgment holds conforming publication.
   - No additional actor or model family is mandatory. State actual separation.
   - Recheck only changed claims/dependencies after repair. Optional suggestions
     do not reopen accepted scope; new material evidence can reopen affected claims.
9. **Publication identity plan**
   - A **pre-authorization** is committed BEFORE the candidate is minted, naming
     the pull request to be merged, the version, the release-note path, the gate
     that must return GO, and the condition on which authorization fires. It
     names no SHA, because none exists yet.
   - The tag name, release-note path, and intended Release target are recorded
     before tag creation. The exact candidate SHA is carried by the **annotated
     tag object**, not by a post-candidate commit — see Procedure step 7.
   - The tag and GitHub Release will be verified after publication without moving
     or reusing the version.

## Procedure

1. **Choose the version and branch.** Prepare a release branch from the final
   intended `main` using a version-derived name such as
   `release/<version>` or the repository's current branch convention.
2. **Freeze the candidate content.** Align live version surfaces, finalize
   `docs/release/RELEASE-<version>.md`, record migration instructions from the
   immediately prior support point, and preserve historical evidence at its
   original coordinates.
3. **Run the full local gate and open the release PR.** Require GitHub checks and
   review the actual diff, not only generated summaries.
4. **Merge and re-run on the exact candidate.** The commit produced by the merge
   is the candidate. Re-run every exact-commit integrity workflow against that
   SHA. Any correction creates a new candidate and invalidates earlier
   exact-commit evidence.
   - **Dispatch every gating workflow explicitly.** Path-filtered workflows do
     not fire on a candidate whose diff misses their filters -- a release commit
     touching only `docs/` triggers none of them -- so relying on push-triggered
     runs leaves the evidence silently incomplete. A missing run is not a
     passing run.
   - **Record the run IDs in the annotated tag object, not in a commit.** The
     runs exist only once the candidate does, so committing them would mint a
     new candidate and void them -- the same fixed point step 7 cures for the
     authorization line. Post-candidate facts go where a post-candidate fact can
     go without changing the tree.
   - **Merge with a merge commit, not a squash.** A squash attributes the commit
     to whoever merged it, so a sign-off trailer naming any other identity is an
     author mismatch and a false attestation. A merge commit preserves the
     individually signed commits in history and is exempt under the DCO
     checker's `is_merge()` rule.
5. **Run and record the designated-reviewer publication judgment.** Freeze the
   exact candidate and retain the requirement dispositions, material findings,
   evidence references, reviewer identity and verdict. Gauntlet is available when
   plural scrutiny is useful; it is not a universal prerequisite.
   - Preserve the exact subject SHA. Review evidence may be attached to the
     release/PR or committed after the candidate; do not imply a changed tree
     is the unchanged subject of an earlier judgment.
   - The tagged tree need not contain its own exact-SHA verdict. Link the
     external or later evidence clearly from the release record.
6. **Resolve the publication decision.**
   - `GO`: proceed as a conforming release.
   - `CONDITIONAL` or `NO-GO`: fix forward, produce a new candidate, and recheck changed behavior
     and its affected dependencies while retaining unaffected evidence.
   - Owner exception: record `WAIVED`/`UNMET` and the authorization in the
     committed release notes **before** tagging. Do not describe the result as a
     GO or conforming release.
7. **Authorize publication explicitly, then disarm the tag rule.** A verdict is
   advice until an owner acts on it. Until 2026-08-13 nothing here recorded that
   act, and nothing prevented it from being skipped.
   - **The authorization is split across the candidate boundary, and this is
     deliberate.** Requiring a committed line to name the candidate's own SHA is
     not executable: writing it changes the tree and produces a different SHA,
     so the step-4 checks and the step-5 verdict would describe a commit that is
     no longer the candidate. That fixed point stood in this document until
     2026-08-20 and was found by an operator-dispatched independent gate.
   - **Before** the candidate is minted, the owner commits the pre-authorization
     of RG-9: the pull request to be merged, the version, the gate that must
     return GO, and the firing condition. It authorizes a determinate act.
   - **After** the gate returns GO, the owner records **in the annotated tag
     object** the verdict read (path and run id), the exact candidate SHA, their
     own identity, and the disarm timestamp. The subsequent re-arm timestamp and
     seeded rejection result belong in a publication receipt attached to the
     Release or PR: they occur after tag push and cannot truthfully be embedded
     in an already immutable tag. Never rewrite a tag to add those later facts.
     A tag names its target
     without altering it, so the candidate is identical across the step-4
     checks, the step-5 verdict, the authorization, and the tag target.
   - A verdict without a resolvable subject still authorizes nothing: a `GO` for
     one SHA is not a `GO` for the SHA about to be tagged unless they are the
     same string. The rule is unchanged; only where the string is written moves.
   - **No commit may be made between the candidate and the tag.** If one is
     required, the candidate is superseded and steps 4-6 re-run from the top.
   - The ruleset `protect-version-tags` carries `creation` with **no bypass
     actors**, so `refs/tags/v*` cannot be created by anyone — including an
     owner, and including automation acting with an owner's credential. That is
     deliberate: this repository is pushed with the same credential automation
     runs under, so an admin bypass would have exempted exactly the actors the
     rule exists to constrain.
   - **Disarming the rule is therefore the authorization act.** Remove the
     `creation` rule (or set the ruleset's enforcement to `disabled`), create and
     push the tag, then **re-arm it in the same sitting**. Record the disarm with the tag authorization and the later re-arm in
     the attached publication receipt, both bound to the same tag object and target.
   - Verify the rule is armed again before closing the release, with a seeded
     probe rather than by reading the config back. A release that ends with the
     gate left open has removed the control it was meant to satisfy.
8. **Create and push the annotated tag.** Tag `v<version>` on the exact candidate
   SHA. Never use a lightweight tag for a support point.
9. **Create the GitHub Release.** Use the committed release-note file verbatim as
   the body. The Release must be non-draft and must target the annotated tag.
10. **Verify publication identity.** Through the GitHub API, verify that:
    - the tag exists and is annotated;
    - the peeled tag target equals the candidate SHA;
    - the GitHub Release targets the same tag or exact candidate;
    - the committed release-note body and normalized GitHub Release body are
      equal; and
    - `main` contains the release commit or an explicitly documented fast-forward
      successor.
11. **Record any post-publication discovery honestly.** Correct documentation on
    `main`, add a clearly labeled erratum or post-release review, and ship artifact
    changes under a new semantic version. Never rewrite the immutable tag or imply
    a missing pre-publication event occurred.

## Release-note evidence table

Every release note should contain a table with at least these columns:

| Gate | Status | Exact subject | Evidence | Limits |
|---|---|---|---|---|
| version/link alignment | `MET` / `UNMET` | commit SHA | check or review path | coverage limits |
| deterministic + CodeQL | `MET` / `UNMET` | commit SHA | workflow run IDs | skipped-step rationale |
| security + public content | `MET` / `UNMET` | commit SHA and history range | scan and review artifact | patterns and exclusions |
| description-byte delta | signed byte count vs prior release | commit SHA | `check_description_budget.py --report` outputs at both releases | package-local only; the estate gate is retired (v5 design AMENDMENT 2026-08-18, hybrid Path 2) — `check_loaded_descriptions.py --require-capture` remains available on demand |
| harness evidence | tier per harness | tag/commit | live run or tier record | unavailable surfaces |
| designated-reviewer publication judgment | `GO` / `CONDITIONAL` / `NO-GO` / `WAIVED` | frozen commit | designated-reviewer record or owner exception | actual review/context limits |
| publication identity | `MET` / `UNMET` | tag + release | API identity receipt | normalization rules |

A row without an immutable evidence coordinate is not `MET` merely because the
work is remembered to have happened.

## Partial-publication recovery

Never improvise around an immutable remote tag.

| Observed state | Recovery |
|---|---|
| No remote tag | Fix forward, rerun the complete gate on the new final candidate, then restart publication. |
| Correct remote tag; no GitHub Release | Create the Release from the committed notes on that tag, then run every identity assertion. |
| Correct remote tag; malformed GitHub Release | Repair or recreate the Release object against the same correct tag, then rerun identity assertions. Do not change the tagged tree. |
| Wrong remote tag | Stop publication. Do not move or reuse it; correct the cause and issue a new semantic version. |
| Published release later found defective | Preserve the tag, publish an explicit erratum/post-release review, fix on `main`, and release the correction under a new version. |

## Historical note

The repository's first formal release was `3.0.0`. Its release-specific notes,
risk acceptance, and evidence remain under `docs/release/`. References in those
historical records to the architecture and gates of that release describe their
own time; they are not the current procedure.

`v5.0.0` was published as an explicit exception release because the independent
publication-judgment gate was waived and not run. A later post-release review may
assess the immutable tag, but item 8 remains historically unmet for `v5.0.0`.

Never move or reuse a published version tag. Corrections ship under a new semantic
version.
