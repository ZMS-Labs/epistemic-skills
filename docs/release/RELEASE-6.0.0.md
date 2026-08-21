# Release 6.0.0

**Support point:** `v6.0.0` — one semantic version, one immutable Git tag, one
evidence set. Supersedes `v5.1.0`.

**Candidate identity.** The v6 BUILD freeze was reviewed at candidate
`03e972c5d427238033cb90d66846adabaf11928d` with its packet at
`546ccc8e55eb060379d62198310145f7243ac7bd`; both are ancestors of the release
branch and are pinned by `pin/es-v6-rc5-candidate-2026-08-19` and
`pin/es-v6-rc5-freeze-2026-08-19`. The release candidate is the commit produced
by merging this release branch. The integrity gates run against that commit —
not against this file's description of it. The **publication gate does not**: it
ran four times, on four earlier candidates, and returned NO-GO every time. See
the exception block below before reading anything here as an approval.

## Why 6.0.0

The skill surface did not grow: v6.0.0 ships the same **fifteen** skills as
v5.1.0. The major version marks something else — a security fix in the custody
contract, the completion of the v5 design commitments, and a new assurance
contract that changes what a release of this project is allowed to claim.

The honest summary: v5 claimed things about itself that nothing checked. v6
makes those claims mechanical, and where a claim could not be made mechanical,
it is written down as a limit with an owner.

## What ships

**Security — mission-custody (es#137).** Three P1 false-allow bypasses and four
P2 refusal gaps are closed. These are real permission-boundary defects: paths
that the custody guard should have refused and did not. If you rely on
mission-custody to bound where an agent may write, this is the reason to
upgrade.

**The v5 design commitments, completed.** All four were implemented and are now
enforced rather than asserted:

- `ROUTING.md` is generated solely from `metadata.hands-to`, byte-verified in
  CI, and the hand-authored-routing-table ban is mechanically enforced.
- Every packaged skill carries the intrinsic evidence-emission step
  (`skill-run@1`) with a schema-validated tracked exemplar; live ledgers are
  runtime-local by amended design.
- Sentinel corpora exist for every skill, with `event_kind` bound into each
  fixture and a scorer that fails closed in both directions.
- Skill membership has one source of truth: per-skill frontmatter event
  metadata derives the event map, its schema, the verifier inventory, and every
  count surface. Membership drift fails closed.

**A new assurance contract (`plugins/epistemic-skills/contracts/v6-assurance`).** A release candidate is
now sealed against an exact commit: per-file sha256 digests of every
inventoried source plus the candidate tree hash, recomputed by a validator that
turns CI red if any inventoried file changes after the freeze. The packet's
readiness state cannot be reached by editing a field — the independent verdict
must exist as an on-disk artifact naming the exact candidate SHA, and operator
acceptance must be recorded separately.

**Deterministic-gate hardening.** The durable decision ledger is byte-append-only
against the merge base; the DCO check gained planted self-test controls; the
secret scan's one path exemption is anchored and proven narrow in CI on every
run; the clean-room replicates the workflow's Python steps with a completeness
assertion rather than a hand-maintained copy.

## Release gate status for 6.0.0

**How this file resolves its own identity.** A release note cannot contain the
hash of the commit that contains it. Following the v5.1.0 precedent, identity is
resolved by description: **the final tag candidate is the commit carrying this
table** — the commit produced by merging the release pull request, per
`RELEASING.md` Procedure step 4. Every other coordinate below is written in hex
because it is resolvable in advance.

**Why this file names no run IDs.** Procedure step 4 makes the merge commit the
candidate and says any correction mints a new one, so a table of exact-commit
evidence can never sit *in* the commit it describes.

An earlier draft of this file tried to escape that with a delta-enumerability
argument — it claimed the *only* change between the commit the runs were
dispatched at and the commit carrying the table was the table itself. **That
statement was false**, and an independent panel proved it false: at
`48009fef938bfa989fb797380080824b050f3bb4` the delta from `92b3ca6c` was ten
files, +690/-124, across ten commits, and it silently included the emptying of
`blocking_claims` and an amendment to `RELEASING.md` — the two changes a reader
scoping a re-check would most need to see. The device did not merely overstate;
it concealed. It is recorded here as publication-gate finding **RG1-01**, and it
is retired rather than repaired: no release note in this repository may again
assert its own delta.

What replaces it is step 4's own rule. Exact-SHA run IDs are **post-candidate
facts**, and they go in the annotated tag object, which names its target without
altering it. This table therefore states which gates were run and what tier of
evidence exists; the tag message states the run IDs, at the SHA they actually
judge. If you are auditing this release, read the tag message for the numbers.

> ## This is an EXCEPTION RELEASE, not a conforming release
>
> `RELEASING.md` § "Independent judgment gate" defines two outcomes. A
> **conforming release** carries a recorded `GO` from an independent publication
> gate on the exact candidate. **6.0.0 does not have one and will not get one.**
> Four independent publication reviews were run across three model families and
> every one returned **NO-GO** (§ Provenance). The owner has elected to publish
> anyway, under the exception the same section provides.
>
> The five disclosures that section requires **before tag creation**:
>
> 1. **The gate did not reach GO.** It was run — four times — and returned NO-GO
>    four times. This is not an unrun gate; it is an overridden one.
> 2. **No GO exists.** Not at this candidate, not at any candidate in the v6
>    lineage. No later review can manufacture one: a post-release review adds
>    judgment evidence and cannot convert this into a conforming release.
> 3. **Owner, date, scope, authorization.** Owner: the repository owner,
>    2026-08-21, recorded as decision **D24** in
>    `docs/v6/operator-decision-record-2026-08-20.md` with the instruction
>    quoted verbatim and its provenance stated. Scope: the `v6.0.0` tag and
>    GitHub Release only. It does not reach any integrity gate — see below.
> 4. **What evidence remains, and what it cannot establish.** The artifact
>    itself is well evidenced. Of **31 class claims**: 21 PROVED, 8 LIMITED
>    within stated bounds, 2 PARTIAL, and **none UNPROVED** — counted from
>    `docs/v6/ES6-V6-CANDIDATE/claim-to-proof-matrix.json`, whose other 41 rows
>    are an open-issue census and are not claims about this artifact. The five
>    gating workflows must be green at the exact candidate before this
>    authorization fires (pre-authorization condition 1, which states the one
>    expected job-level red and its failing tests by name); the full-history
>    secret scan and public-content review are green with planted controls; the
>    sealed source inventory verifies. What none of that
>    establishes is the thing the judgment gate exists to establish: that an
>    actor which did not build this release thinks it should be published. Every
>    NO-GO was about the *publication act* and its paperwork, not about the
>    skills. The reader should trust the artifact and discount the ceremony
>    accordingly.
> 5. **Successor condition / revisit trigger.** The standing **D8 cross-family
>    consult** is owed and undischarged; it carries forward to 6.1.0 as a
>    blocking obligation, not as a nicety. If any of the four NO-GO findings is
>    later shown to have named a defect in the *artifact* rather than in the
>    release process, that is an immediate erratum-and-patch trigger under step
>    11.
>
> **The exception reaches exactly one gate.** `RELEASING.md` scopes owner
> exceptions to the independent judgment gate (RG-8). It does **not** reach the
> integrity gates — RG-1 accuracy, RG-4 alignment, RG-5 deterministic evidence,
> RG-6 security and provenance — and no authority in this repository waives
> those. Every one of them is met on its own terms below. A release note that
> lied would still be a lie with an owner's signature on it; that is why RG1-01
> was fixed rather than waived.

| Item | Status | Evidence |
|---|---|---|
| 1 — candidate identity and scope | **met** | Freeze candidate `03e972c5d427238033cb90d66846adabaf11928d`, packet commit `546ccc8e55eb060379d62198310145f7243ac7bd`, both ancestors of this branch and pinned by `pin/es-v6-rc5-candidate-2026-08-19` / `pin/es-v6-rc5-freeze-2026-08-19` (lightweight — see PG-17 below). The release candidate is the merge commit of this branch. |
| 2 — release decisions and risk acceptance | **met as an exception, with one bounded gap** | Operator acceptance is recorded as **D24** (2026-08-21) in `docs/v6/operator-decision-record-2026-08-20.md`, electing the RG-8 exception with the five required disclosures made above *before* tag creation. The packet still carries no `operator_acceptance` object and still reads `NOT_READY`: that field tracks *conforming* readiness, and an exception release does not make a packet ready. Leaving it `NOT_READY` is the honest state, not an oversight. **Bounded gap RG4-05:** the D8 cross-family consult is owed and undischarged; it is disclosed above as the successor-release condition and is the one RG-2 obligation this release does not satisfy. |
| 3 — evidence retention | **met** | All **nine** verdicts of this lineage — the five BUILD panels and the four publication reviews — are in-tree under `docs/gauntlet-runs/` with an index at `docs/gauntlet-runs/V6-VERDICT-LINEAGE.md` binding each to its exact subject commit. Previously they lived only on mutable branches while this file asserted otherwise — publication-gate finding PG-03, now closed. |
| 4 — version and link alignment | **met, with its limits stated in-row** | Ten version-bearing surfaces at 6.0.0; surface-sync `--check` green (15 skills / 14 disciplines). Fixed since the first candidate: `.kimi-plugin/marketplace.json` had pinned `tree/v3.4.0` for three major versions and was the one manifest no oracle read (PG-07); the README advertised `v6.0.0` as a published support point behind links that returned 404 (PG-18). Both marketplace "full collection" descriptions enumerated fourteen of fifteen skills, omitting `manifest` (PG-15) — an oracle added this cycle now derives the expected set from `plugins/epistemic-skills/skills/` and fails on any omission or invention, so the defect class cannot recur silently. **Limits, stated here rather than in a footnote:** (a) the install-ref pin reads `v5.1.0` in the tagged tree, because at tag time 5.1.0 is still the published support point — the bump is a post-tag commit and is not a version-surface staleness; (b) the wiki is a separate repository that no in-repo oracle can reach, so its alignment is asserted only by `docs/wiki-updates/v6.0.0/apply_v6_updates.py`, which is dry-run-by-default, self-tested, and now refuses to run against a path that does not look like a wiki clone or whose target tag does not yet exist. |
| 5 — deterministic and static-analysis evidence | **run at the candidate; the IDs are in the tag object, not here** | Per `RELEASING.md` step 4, exact-SHA run IDs are post-candidate facts and are recorded in the annotated tag message, which names its target without altering it. This row states the discipline and the tier: **all five gating workflows dispatched explicitly** at the candidate (path-filtered workflows do not fire on a docs-only diff, so push-triggered runs are not accepted as evidence), plus the required CodeQL matrices — which run under GitHub **default setup** and therefore have no workflow file in `.github/workflows/` and do not appear in the Actions workflow-run listing used to gather the rest of this evidence. Their status is read from the candidate's check runs and recorded in the tag object with the workflow IDs; a reader who greps this repository for a CodeQL workflow and finds none has found the default setup, not a missing gate. Four workflows must be `success`; `mission-custody-contract` must show its required `contract` job `success` with only the dispatch-only `contract-macos` probe red, disclosed by failing test name under RG-5(c). **Lineage, not this commit's evidence:** the last complete dispatch was at the superseded candidate `48009fef938bfa989fb797380080824b050f3bb4` — `epistemic-flexibility` 32430457960, `release-security` 32430459879, `openai-bundles` 32430452518, `commission-watch-contract` 32430465696 all success; `mission-custody-contract` 32430450479 with `contract` (ubuntu-24.04) success across all 12 steps and `contract-macos` failed at step 8. That evidence judges `48009fef` and **does not transfer** to this candidate. |
| 6 — security, public content, provenance | **met** | `check_public_content.py` self-test (8 seeded RED controls, one per pattern) and live run both exit 0; the exact-file allowlist narrowed by one entry when the exemption's reason was remediated rather than renewed. Full-history secret scan green with its planted positive control and the record-path narrowness control. Provenance: `CONTRIBUTING.md` now states the DCO rule actually enforced, including both exemptions and the check's two limits (PG-13); the 250-commit endpoint fail-open is closed (PG-23). The 6.0.0 release-window public-content review is recorded below: 232 files, zero true defects, with each apparent hit dispositioned and each exemption's reason stated (PG-12). |
| 7 — supported harness evidence | **met via explicit tiers; no new live-fire** | Per-harness tiers below. No native-harness live-fire ran for this release; `KL-LIVE-ENV` records that, and the honest boundary column in the README install table carries each surface's limit. Cursor's recorded behavioral epoch remains `BLOCKED_EXTERNAL`. |
| 8 — independent publication judgment | **NO-GO ×4 — gate overridden by recorded owner exception (D24)** | Four independent reviews of the *publication act*, none of which adopted another's reasoning, all **NO-GO**: (1) cross-family single seat, xAI/Grok, subject `186b16eb`, `docs/gauntlet-runs/es-v6-publication-grok-2026-08-19/`; (2) same-family panel, subject `186b16eb`, `docs/gauntlet-runs/es-v6-publication-gate-2026-08-19/`; (3) **operator-dispatched** cross-family seat, OpenAI, subject `d0165bd0`, `docs/gauntlet-runs/es-v6-publication-openai-2026-08-20/`; (4) same-lineage panel with an isolated judge, subject `48009fef`, `docs/gauntlet-runs/es-v6-publication-panel-2026-08-21/`. **Two structural limits are disclosed, not glossed:** reviews 2 and 4 shared a model family with the authors, and review 4 was dispatched by the implementing lineage — a panel the implementer seats can block a release but cannot clear one, and this one is credited only for its blocking findings (RG1-01 among them, which it found against its own dispatcher's work). Reviews 1 and 3 judge superseded candidates, so neither verdict transfers to this one — but neither is discharged either. **No GO exists at any candidate.** The owner has overridden this gate under `RELEASING.md` § "Independent judgment gate"; see the exception block above. |
| 9 — publication identity plan | **pre-authorized; execution pending the owner's hand** | Tag `v6.0.0`, annotated, on the final candidate; release-note path `docs/release/RELEASE-6.0.0.md`; Release target the annotated tag, non-draft, body verbatim from this file. `protect-version-tags` carries `creation` with **no bypass actors** — no actor of any kind can create `refs/tags/v*` while it is armed, including an owner and including automation holding an owner's credential. **Disarming it therefore *is* the authorization act**, and the owner has authorized the disarm (D24). Sequence: disarm, tag, push, Release, re-arm **in the same sitting**, then verify the re-arm with a seeded probe rather than by reading the config back. The disarm and re-arm timestamps are recorded in the tag message beside the authorization line. `docs/release/PRE-AUTHORIZATION-6.0.0.md` fixes the determinate act in advance. **This repository's automation cannot perform any of it:** the ruleset change is a settings write no agent holds, and tag pushes from the build environment are refused at the proxy. The commands are printed for the owner to run. |

### Why this tree does not contain its own verdict

A tree cannot contain a judgment of itself. The publication verdict is produced
*at* the candidate, so committing it would supersede the commit it judges — the
same fixed point `RELEASING.md` step 7 cures for the authorization line, and
step 4 for the exact-SHA run evidence.

So three classes of fact live outside the tagged tree, by design rather than by
omission: the **exact-SHA run IDs**, the **verdict**, and the **authorization**.
All three are carried by the annotated tag object, which names its target
without altering it. The verdict artifacts themselves are committed to the
default branch *after* the tag exists, where they are reachable by name and can
no longer move the thing they judge.

If you are auditing this release and cannot find its verdict inside the tag,
that is the design working. Read the tag message.

### RG-5(c) disclosure — the red job at the candidate

`RELEASING.md` RG-5's dispatch-only carve-out is conjunctive, and its third
condition requires the release record to name what failed. The failure is stable
across every candidate in this lineage and is named here by **test**, which is
the durable coordinate; the run ID that observed it at the final candidate is in
the tag object with the rest of the exact-SHA evidence. Last verified at
`48009fef` (run 32430450479, job `contract-macos`, id 96620818500):

- **Workflow** `mission-custody-contract`, job **`contract-macos`** (`macos-14`),
  the dispatch-only probe. The required `contract` job on `ubuntu-24.04` passed
  all 12 steps in the same run.
- **Step 8**, "Custody mission lifecycle unit tests".
- **Failing tests, read from that run's log:** `distinct-real-file-untouched`
  and `distinct-both-files-tracked-separately` — exactly two, and the other three
  `distinct-*` cases (`distinct-recover-raised`, `distinct-decoy-did-not-discharge`,
  `distinct-real-recovery-discharges`) pass.
- **Cause, stated precisely, because two earlier editions of this file described
  it two different ways.** The two failing cases use the filenames `straße.txt`
  and `strasse.txt`. macOS default volumes are case-insensitive under **full
  Unicode case folding**, in which `ß` (U+00DF) folds to `ss` — so those two
  names are **one physical file** there, and a write to one is observable through
  the other. The contract's own comparison is not at fault and is not folding:
  `_same_artifact` in `custody_mission.py` applies an ASCII-only fold and applies
  it only when `os.name == "nt"`, so on macOS it correctly reports the two paths
  as distinct artifacts. The disagreement is between a correct contract and a
  folding filesystem, which is exactly what `KL-MACOS-162` records. Settled
  negative before this release cycle; not a regression in it. The job's own
  es#162 probe step (step 5) passes — the filesystem behaves as the probe expects.
  ("Case-insensitive" and "Unicode-fold" are both true of this mechanism and
  neither is sufficient alone; the folding is case folding, but it is the full
  Unicode table, not ASCII.)
- **Unmeasured as a consequence:** steps 9–12 are skipped, so four custody suites
  (CLI black-box, gate unit, enforcement hook, three-subprocess continuity) did
  not run on macOS at this candidate. All four pass on `ubuntu-24.04` in the
  required `contract` job.

The substance is benign and long-disclosed. The gate failed on the record's
silence, not on the failure — which is the correct way for it to fail.

### Per-harness verification tiers (RG-7)

| Harness | Tier | What was actually done |
|---|---|---|
| Claude Code | packaging + deterministic | manifest and package-integration suites green; no live plugin install exercised for 6.0.0 |
| Codex | packaging | manifest parity checked; role rendering not re-executed live |
| Cursor | packaging, `BLOCKED_EXTERNAL` | no public listing available; behavioral epoch unchanged |
| Gemini CLI / Antigravity | packaging | manifest and symlink-tree checks only |
| Kimi Code | packaging | install ref corrected this cycle (PG-07); not re-installed live |
| ZCode | packaging | junction surface previously verified on one device; plugin install untested |
| ChatGPT / OpenAI | generated bundle | `openai-bundles` green at the freeze candidate; snapshot artifact, no live execution |

No row above claims a live behavioral verification, because none was run.

### Release-window public-content review (item 6 record)

`RELEASING.md` RG-6 requires a public-content review at an immutable path, and
6.0.0 had none (publication-gate finding PG-12). This is that record.

**Scope.** Every file changed in `v5.1.0..candidate` — **232 files**, the full
release window rather than a single pull-request diff.

**Method.** Each file was passed through `check_public_content.py`'s own
`scan_text`, so the review applies the same sanitization and allowlist logic the
gate applies, rather than a hand-rolled pattern sweep. A raw pattern sweep was
run first and deliberately compared against it: the raw sweep reported four
apparent hits that `scan_text` correctly clears.

**Result: zero true defects.**

| Apparent hit | File | Disposition |
|---|---|---|
| `email-address` ×2 | `.github/scripts/check_dco.py` | `dev@example.test`, `other@example.test` — DCO self-test identities on the RFC-reserved `.test` TLD. Not deliverable addresses. |
| `email-address` | `…/formal-rigor-v2-fixtures/tests/test_live_runner.py` | Same class: synthetic fixture identity. |
| `windows-user-path` ×2 | `…/es-v6-rc3-delta-review-2026-08-18/reports/verify-s7810.json`, `…/test_live_runner.py` | `C:/Users/example` — the synthetic username the scanner neutralizes by design, and the seed its own RED control depends on. |

**Exemptions exercised in the window, each with a live reason.** The private
fleet name in the ES6-ZI-001 parent-tracker coordinate and its generator; the
scanner's own file, which necessarily quotes its whole pattern vocabulary;
RFC1918 and UNC strings inside the v5.1.0 release record and a custody test
fixture; and two build-host-scratch-path files (sealed freeze evidence, and a
dated probe results archive). One exemption was **removed** during this window
rather than renewed, because its reason had been remediated.

**Pattern set at this release:** eight classes, up from seven. The added class is
`build-host-scratch-path`. Every class carries a seeded RED control, and that
invariant is now enforced rather than merely documented.

## Known limitations, carried honestly

Shipped in the packet with named owners:

| Limit | What it means |
|---|---|
| `KL-SELF-GO` | The implementing lineage holds no acceptance seat. **Unretired, and load-bearing for this release:** it is the reason no GO exists at any candidate, and the reason the owner had to override RG-8 rather than satisfy it. The packet's `self_certification` field reads `refused` and its `requested_irreversible_acts` is empty — the implementer asks for nothing and certifies nothing. |
| `KL-LIVE-ENV` | Behavioral epochs and native-harness live-fire were not run. |
| `KL-MACOS-162` | Measured APFS Unicode-fold collision: two contract-distinct filenames are one physical file. Custody distinctness claims exclude case-insensitive APFS. |
| `KL-WINDOWS` | No native-Windows requalification was run. |
| `KL-DRAFT-CI` | Draft pull requests skip all five gating workflows until ready-mark. |
| `KL-RESTAMP` | A recorded candidate SHA is an observation of the tree it was generated from, never a target to restamp. |
| `KL-GUARD-LEXICAL` | Custody guard path matching is lexical; a write spelled through a symlinked parent can resolve inside a guarded tree while the guard does not match. |
| `KL-SEAL-MAIN-COUPLING` | **Scoped down by this release.** While a freeze is ACTIVE its seal binds inventoried sources against the working tree, so a default-branch change to any of them turns the freeze red on its pull request's merge ref — the coupling that superseded rc4. Once the candidate lands, the packet moves to LANDED and digests are verified against the named commit by git object read, so the default branch is free to move. The limit now applies only to the window while a freeze is open. |
| `KL-MAIN-137` | **Retired by this release.** It disclosed that the es#137 fixes existed only in the candidate tree. The freeze merge landed them on the default branch. |

Twelve further findings from the final review are open, all graded P4, three
carrying preserved P3 dissents. They are recorded in that run's arbitration
rather than summarized away here. The largest is honest to state plainly: the
DCO checker's merge-commit exemption is unconditional, so a merge commit that
authors content — a conflict resolution — is uncertified by it.

## Documentation gap recorded, not silently inherited (RG-2)

The README-linked public Wiki is the handbook this release points users at, and
it currently documents a **v5.0.0-era package**. Measured by cloning the wiki
repository: most pages say *fourteen* skills, there is no `Skill-Manifest` page
(the seat carrying this release's headline security fix), eight retired seats
survive as live pages, and v5.0.0 outnumbers v5.1.0 in version guidance 301 to
29. A `docs/wiki-updates/v6.0.0/` package now exists: the authored `Skill-Manifest`
page plus a self-tested applier that reports the drift and writes it only when
asked (`apply_v6_updates.py --self-test`, then a dry run against a wiki clone).
The corrections are prepared and **not applied** — the wiki is a separate
repository, so no job here can close this, and the applier's version-bumping
rules must not run before the tag exists.

- **Owner:** repository owner.
- **Scope:** the Wiki repository only; no packaged file is affected, and the
  in-tree `SKILL.md` contracts govern wherever the two disagree.
- **Revisit trigger:** in the window between tag creation and the GitHub
  Release. Not earlier — the applier's link rules rewrite URLs to `/v6.0.0/`,
  which is a 404 until the tag exists, and the applier now refuses to run before
  then rather than trusting an operator to remember. Not later, for the reason
  in the paragraph below.
- **Exit criterion:** installation and catalog pages read fifteen skills with
  v6.0.0 install guidance, a `Skill-Manifest` page exists, and retired seats are
  described in the past tense. Measured starting state: 26 stale version banners,
  6 stale skill counts, 5 stale discipline counts, 9 present-tense retired seats,
  and no `Skill-Manifest` page.

Recorded here because `RELEASING.md` RG-2 forbids leaving an integrity gap
*unrecorded* at tag creation. This is a pre-existing condition, not a regression
introduced by this release — and the v5.1.0 note recorded a post-tag handbook
pass as a follow-up that was never performed, so "we will fix it after the tag"
has a 0-for-1 record here and should not be relied on again. **If the window is
missed, this becomes a shipped documentation defect, not a pending task**, and
should be recorded as an erratum under `RELEASING.md` step 11 rather than
carried as an open intention for another release cycle.

The README no longer routes readers into the stale pages for skill contracts:
all fifteen catalog rows now link to in-tree sources.

## Migration from 5.1.0

Install surfaces change version only; the skill inventory is unchanged, so no
skill is renamed, retired, or added. Replace an older copy with a tagged checkout
or plugin install, reload the harness, and verify the skill count and source
path — one install mechanism per harness, never two.

**Two behavioral changes to expect, not one.**

1. **Stricter custody refusals.** Paths the guard previously allowed through the
   es#137 bypasses are now refused. The closed classes are parent-relative
   traversal, absolute paths outside the guarded tree, and paths whose guarded
   prefix matched only lexically. A refusal fails closed and returns an explicit
   refusal rather than a silent no-op. If a workflow depended on one of those
   writes succeeding, it now fails — that is the fix working.
2. **Evidence emission is now near-universal.** Skills instructing an append to
   `runs/ledger.jsonl` after an engagement went from **7 of 15** at v5.1.0 to
   **15 of 15** here (measured by comparing the two trees). If you run these
   skills in an environment where that path is unwritable or where the extra
   file is unwelcome, you will notice it — the earlier release largely did not
   write it.

**Rollback.** v5.1.0 remains a valid support point. Re-install the `v5.1.0` tag
by the same one-mechanism-per-harness rule and reload; nothing in this release
migrates on-disk state, so downgrade needs no data step. The custody bypasses
return with it.

**Platform caveats that survive this release.** macOS custody lifecycle behavior
is unmeasured-or-red at the candidate (`KL-MACOS-162`, and the RG-5(c) disclosure
above); Windows shipped with no native requalification (`KL-WINDOWS`); and
`KL-GUARD-LEXICAL` records a residual false-allow where a write is spelled
through a symlinked parent. If mission-custody is the reason you are upgrading,
read those three limits first — they bound exactly the guarantee you are
upgrading for.

## Provenance notes

This release has been judged **nine times**: five panels on the BUILD freeze,
then four on the publication act. The BUILD sequence produced **four NO-GO
verdicts** before its GO. **The publication sequence produced four NO-GOs and no
GO**, and is the gate the owner has overridden — see the exception block above. "Independent" needs qualifying, and the GO record
qualifies it: four of those five shared a model family with the candidate's
authors and recorded that as an independence **limit**, not as independence.
Only the rc2 panel (Kimi/Moonshot) was cross-family. Each panel also judged a
*different* candidate; only the fifth saw `03e972c5`. Each NO-GO was found by a panel
reviewing the previous repair, and every P1 in the sequence belonged to one
class: a gate that had never actually executed against the sealed head.

1. Freeze panel — 18 rulings, 15 acceptance criteria.
2. Cross-family panel (Kimi/Moonshot) — rulings S1–S10.
3. Delta review — the candidate commit had byte-rewritten published
   append-only ledger lines.
4. Fourth panel — six commits in the freeze pull request carried no DCO
   sign-off, so a required job would have gone red at ready-mark.
5. Fifth panel — GO, with the discharge re-executed from primary sources.

### The four publication reviews

| # | Seat | Family | Dispatched by | Subject | Verdict |
|---|---|---|---|---|---|
| 6 | single seat | xAI / Grok — **cross-family** | implementing lineage | `186b16eb` | NO-GO |
| 7 | panel | same family as authors | implementing lineage | `186b16eb` | NO-GO |
| 8 | single seat | OpenAI — **cross-family** | **operator** | `d0165bd0` | NO-GO |
| 9 | panel, isolated judge | same family as authors | implementing lineage | `48009fef` | NO-GO |

Review 8 is the only one of the nine that is both cross-family *and* operator-
dispatched, and it is worth reading in full: it found that the authorization
sequence written into `RELEASING.md` was not executable, that a candidate's
sign-off trailers were false attestations, and that two workflows had never run
on the exact subject. All three were repaired. Review 9 — dispatched by the
implementing lineage, so structurally able to block but not to clear — found
**RG1-01**, a false scope statement in this very file that concealed two
material changes; that is repaired above, and the device that produced it is
retired rather than patched.

None of the four found a defect in the shipped skills. Every P1 across the four
was about the release process, its paperwork, or its authority chain. That is
the honest shape of this record and the reason the owner's exception is
defensible: the ceremony failed repeatedly; the artifact did not.

Run records live under `docs/gauntlet-runs/`, indexed by
`docs/gauntlet-runs/V6-VERDICT-LINEAGE.md`, which binds each verdict to its exact
subject commit and discloses the two mechanical redactions applied when they were
brought in-tree. The verdicts are retained at their original coordinates; none was
rewritten to match a later outcome, and the unredacted bytes remain on the
originating branches for audit.

**What the shipped packet says about itself.** `docs/v6/ES6-V6-CANDIDATE/promotion-packet.json`
now reads `independent_gauntlet: GO`, bound by `independent_gauntlet_ref` to an
on-disk verdict artifact whose subject SHA equals the packet's own
`candidate_sha`. `blocking_claims` is empty — **derived**, never hand-written, so
it went empty only because the matrix row closed. `readiness` stays `NOT_READY`
until operator acceptance is recorded, which is correct rather than pessimistic.

Read the matrix's two populations separately, because conflating them is the
error an earlier edition of this record made. **31 class claims** state what this
release asserts: 21 PROVED, 8 LIMITED within stated bounds, 2 PARTIAL, and
**none UNPROVED**. The remaining **41 rows are an open-issue census**, where
`UNPROVED` means the tracker item is still open and never meant a failed proof.

The one class claim that stood UNPROVED, `CLM-INDEPENDENT-GAUNTLET`, is closed
by **operator ratification** of the rc5 verdict (D20), not by an
operator-dispatched review. The seat was fresh and non-authoring, so the oracle
is satisfied in full; the dispatch limb of its closure path is closed by the
operator adopting the verdict after the fact.

**Review 9 disputed that, and the dispute is recorded rather than resolved in
this release's favour.** Its argument: dispatch controls *selection* — whether
an unfavourable verdict ever reaches the operator at all — and after-the-fact
ratification can only operate on the verdicts the implementing lineage chose to
present. Ratifying a GO is therefore not equivalent to having dispatched the
review that produced it. That is a real gap and it is not closed here. It is why
`KL-SELF-GO` still ships, why the D8 cross-family consult carries forward as the
successor condition, and why this is an exception release rather than a
conforming one. Anyone auditing the PROVED status of `CLM-INDEPENDENT-GAUNTLET`
should read D20, read this paragraph, and judge for themselves.

The binding is not decorative: removing the ref, pointing it at a verdict that
is not on disk, naming a different subject SHA, or hand-editing
`blocking_claims` are each refused by the validator with a named error.
