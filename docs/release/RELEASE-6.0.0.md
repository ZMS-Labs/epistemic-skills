# Release 6.0.0

**Support point:** `v6.0.0` — one semantic version, one immutable Git tag, one
evidence set. Supersedes `v5.1.0`.

**Candidate identity.** The v6 BUILD freeze was reviewed at candidate
`03e972c5d427238033cb90d66846adabaf11928d` with its packet at
`546ccc8e55eb060379d62198310145f7243ac7bd`; both are ancestors of the release
branch and are pinned by `pin/es-v6-rc5-candidate-2026-08-19` and
`pin/es-v6-rc5-freeze-2026-08-19`. The release candidate is the commit produced
by merging this release branch, and the publication gate runs against that
commit — not against this file's description of it.

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

**Why this file's evidence names its own parent.** Procedure step 4 makes the
merge commit the candidate and says any correction mints a new one, so a table of
exact-commit evidence can never sit *in* the commit it describes. The v5.1.0
precedent resolves this by keeping the delta enumerable: the runs above were
dispatched at `92b3ca6c`, and the **only** change between that commit and the one
carrying this table is this table. `git diff 92b3ca6c..HEAD -- docs/release/`
shows the whole of it. A delta-scoped re-check, not a full requalification, is
what that difference warrants.

**Authorization — NOT YET GIVEN.** `RELEASING.md` step 7 requires a line naming
the verdict read, the exact candidate SHA authorized, and the owner. That line is
the owner's to write and does not exist yet. Until it does, this file is a
release *preparation* record, not an authorization, and nothing here may be read
as one. The two publication reviews on record both returned NO-GO
(§ Provenance); a conforming publication requires a fresh gate at the final
candidate.

| Item | Status | Evidence |
|---|---|---|
| 1 — candidate identity and scope | **met** | Freeze candidate `03e972c5d427238033cb90d66846adabaf11928d`, packet commit `546ccc8e55eb060379d62198310145f7243ac7bd`, both ancestors of this branch and pinned by `pin/es-v6-rc5-candidate-2026-08-19` / `pin/es-v6-rc5-freeze-2026-08-19` (lightweight — see PG-17 below). The release candidate is the merge commit of this branch. |
| 2 — release decisions and risk acceptance | **UNMET** | Operator acceptance under `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` has not been recorded, and the packet carries no `operator_acceptance` object. The standing D8 cross-family consult is owed and not discharged. Both were ruled blocking by the publication panels. |
| 3 — evidence retention | **met** | All seven verdicts of this lineage are in-tree under `docs/gauntlet-runs/` with an index at `docs/gauntlet-runs/V6-VERDICT-LINEAGE.md` binding each to its exact subject commit. Previously they lived only on mutable branches while this file asserted otherwise — publication-gate finding PG-03, now closed. |
| 4 — version and link alignment | **met, after two stalenesses were found and fixed** | Ten version-bearing surfaces at 6.0.0; surface-sync `--check` green (15 skills / 14 disciplines). Fixed since the first candidate: `.kimi-plugin/marketplace.json` had pinned `tree/v3.4.0` for three major versions and was the one manifest no oracle read (PG-07); the README advertised `v6.0.0` as a published support point behind links that returned 404 (PG-18). Both marketplace "full collection" descriptions enumerated fourteen of fifteen skills, omitting `manifest` (PG-15). A new install-ref oracle now fails on any manifest ref that is not the current install pin, with a control asserting it is not vacuous. |
| 5 — deterministic and static-analysis evidence | **met at `92b3ca6c`, the parent of this commit** | All five gating workflows dispatched at `92b3ca6cf7009cb668146b526e3b35012f7454a6`: `epistemic-flexibility` **32325697974** success; `release-security` **32325699859** success; `openai-bundles` **32325701579** success; `commission-watch-contract` **32325704803** success; `mission-custody-contract` **32325702964** — required job `contract` **success** (all 12 steps), dispatch-only probe job `contract-macos` **failure**, see the RG-5(c) disclosure below. Earlier evidence at the freeze candidate `03e972c5` is superseded and does not transfer. |
| 6 — security, public content, provenance | **met** | `check_public_content.py` self-test (8 seeded RED controls, one per pattern) and live run both exit 0; the exact-file allowlist narrowed by one entry when the exemption's reason was remediated rather than renewed. Full-history secret scan green with its planted positive control and the record-path narrowness control. Provenance: `CONTRIBUTING.md` now states the DCO rule actually enforced, including both exemptions and the check's two limits (PG-13); the 250-commit endpoint fail-open is closed (PG-23). The 6.0.0 release-window public-content review is recorded below: 232 files, zero true defects, with each apparent hit dispositioned and each exemption's reason stated (PG-12). |
| 7 — supported harness evidence | **met via explicit tiers; no new live-fire** | Per-harness tiers below. No native-harness live-fire ran for this release; `KL-LIVE-ENV` records that, and the honest boundary column in the README install table carries each surface's limit. Cursor's recorded behavioral epoch remains `BLOCKED_EXTERNAL`. |
| 8 — independent publication judgment | **NO-GO ×2 — the gate is not passed** | Two independent reviews of the publication act, both against `186b16eb2c069d9e8f902579afa50e9f5460fc85`: a cross-family single seat (xAI/Grok, `docs/gauntlet-runs/es-v6-publication-grok-2026-08-19/`) and a same-family panel (`docs/gauntlet-runs/es-v6-publication-gate-2026-08-19/`). Neither adopted the other's reasoning; both returned **NO-GO**. That candidate is superseded, so neither verdict transfers — but neither is discharged either. A fresh publication gate at the final candidate is required. **Independence limit:** five of the seven reviews in this lineage shared a model family with the authors and recorded that as a limit, not as independence. |
| 9 — publication identity plan | **UNMET until the authorization line exists** | Tag `v6.0.0`, annotated, on the final candidate; release-note path `docs/release/RELEASE-6.0.0.md`; Release target the annotated tag, non-draft, body verbatim from this file. `protect-version-tags` carries `creation` with no bypass actors, so disarming it *is* the authorization act: disarm, tag, re-arm in the same sitting, then verify with a seeded probe rather than by reading the config back. The disarm and re-arm are recorded beside the authorization line. None of this has happened. |

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
condition requires the release record to name what failed. Naming it, **verified
at `92b3ca6c` rather than carried forward** from the freeze candidate:

- **Run** 32325702964, workflow `mission-custody-contract`, job **`contract-macos`**
  (`macos-14`).
- **Step 8**, "Custody mission lifecycle unit tests".
- **Failing tests, read from that run's log:** `distinct-real-file-untouched`
  and `distinct-both-files-tracked-separately` — exactly two, and the other three
  `distinct-*` cases (`distinct-recover-raised`, `distinct-decoy-did-not-discharge`,
  `distinct-real-recovery-discharges`) pass.
- **Cause:** macOS default filesystems are case-insensitive, so two
  contract-distinct filenames resolve to one physical file. This is `KL-MACOS-162`,
  settled negative before this release cycle, not a regression in it. The job's own
  es#162 probe step (step 5) passes — the filesystem behaves as the probe expects.
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
| `KL-SELF-GO` | The implementing lineage holds no acceptance seat. |
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
- **Revisit trigger:** before the v6.0.0 Release is created.
- **Exit criterion:** installation and catalog pages read fifteen skills with
  v6.0.0 install guidance, a `Skill-Manifest` page exists, and retired seats are
  described in the past tense. Measured starting state: 26 stale version banners,
  6 stale skill counts, 5 stale discipline counts, 9 present-tense retired seats,
  and no `Skill-Manifest` page.

Recorded here because `RELEASING.md` RG-2 forbids leaving an integrity gap
*unrecorded* at tag creation. This is a pre-existing condition, not a regression
introduced by this release — and the v5.1.0 note recorded a post-tag handbook
pass as a follow-up that was never performed, so "we will fix it after the tag"
has a 0-for-1 record here and should not be relied on again.

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

The v6 BUILD freeze was reviewed by **five panels** and produced **four NO-GO
verdicts** before its GO. "Independent" needs qualifying, and the GO record
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
operator adopting the verdict after the fact. That distinction is recorded in
`docs/v6/operator-decision-record-2026-08-20.md` rather than smoothed over, and
anyone auditing the PROVED status should read it and judge for themselves.

The binding is not decorative: removing the ref, pointing it at a verdict that
is not on disk, naming a different subject SHA, or hand-editing
`blocking_claims` are each refused by the validator with a named error.
