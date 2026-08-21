# Triage of the non-blocking findings from the v6 review lineage

Two distinct sets were outstanding after v6.0.0 published, and the release note
conflated them by citing only one count. Both are dispositioned here.

- **R5-NF1 … R5-NF12** — the twelve P4 findings from run 5
  (`es-v6-rc5-narrow-review-2026-08-19`), which the release note refers to as
  "twelve further findings … all graded P4, three carrying preserved P3 dissents".
- **The publication panel's seven non-blocking findings** from run 9
  (`es-v6-publication-panel-2026-08-21`): RG4-01 … RG4-06 and RG1-03.

Nothing here was closed by assertion. Each row below was checked against the tree
at the time of triage.

## Closed by work already landed

| Finding | What it said | How it closed |
|---|---|---|
| **R5-NF4** (merge limb) | The DCO merge exemption's narrowness is "prose and review discipline, not an enforced control". Mutating `is_merge` to accept anything starting with "Merge" **survived** the self-test. | Exemption now narrowed to merges that author nothing, verified by recomputing the clean merge with `git merge-tree` and comparing trees. A merge that resolves a conflict requires a sign-off; one that cannot be classified fails closed. |
| **R5-NF4** (closure limb) | "This list is CLOSED" was asserted in a comment. Appending an arbitrary sixth SHA **survived**; deleting an exercised entry **survived**. | The exact set is digest-pinned in the self-test. Both mutations now fail. |
| **R5-NF5** | The attestation comment miscounted what it certifies. | Comment and list both read five; verified by counting entries. |
| **R5-NF6** | `CONTRIBUTING.md` still published the old rule after the enforced rule changed. | Rewritten to describe what is actually enforced, including the fail-closed behaviour. |
| **R5-NF12** | Latent pagination fail-open: `github_commits()` would silently under-read a pull request past GitHub's 250-commit cap. | `GITHUB_PR_COMMIT_CAP` fails closed with instructions. |
| **RG4-01** (residual) | `apply_v6_updates.py` had no path-existence check and no tag-existence guard, so it would carry 404s forward under a new tag. | Both guards added and self-tested. The blanket URL-rewrite rule that caused the underlying damage was removed outright, with a regression guard. |
| **RG4-02** | The README count check's selector matched **zero** lines — dead since v5.0.0. Surface correct, oracle vacuous. | Selector rewritten to key on the fenced block structurally, plus two non-vacuity controls. Independently found during the wiki pass before this triage read the finding. |
| **RG4-03** | PG-15 fixed in content, no oracle added; recurrence would be silent. | Marketplace enumeration oracle added, deriving the expected set from the skills directory, checking both directions, mutation-tested four ways. |
| **RG4-04** | 26 pre-existing v5.0.0-pinned dead URLs in the handbook. | Closed in the handbook pass; `check_wiki.py --links` now resolves every repository URL. |
| **RG4-05** | The post-tag install-ref obligation had no owner, trigger, or exit. | Recorded as a bounded RG-2 gap before tagging, then discharged in `PUBLICATION-RECORD-6.0.0.md` with the four URLs measured at HTTP 200. |

## Not a defect

| Finding | Disposition |
|---|---|
| **RG4-06** | "4 of 15 skills unnamed in manifest descriptions." Re-measured: the plugin manifest descriptions are prose blurbs that name some skills literally and others by function — "adversarial review" is `gauntlet`, "evidence-locked acceptance" is `evidence-locked-uat`, "goal authoring" is `write-goal`. They do not claim to enumerate, and their counts are correct. A first pass at re-measuring this scored literal substrings and reported 8–9 missing; that measurement was wrong, not the manifests. Forcing fifteen literal names into a blurb would make it worse. **No action.** |

## Historical — about superseded candidates, retained not reopened

`R5-NF1`, `R5-NF7`, `R5-NF8`, `R5-NF9`, `R5-NF10`, `R5-NF11`, `RG1-03`. Each
concerns the identity, authority, or sealing of a candidate that no longer
exists. They remain in their run directories, which is where verdicts about
superseded commits belong. None is reopened, and none is claimed to be
discharged — a finding about a commit that is gone is neither.

## Still open

| Finding | Status |
|---|---|
| **R5-NF3** | `KL-SEAL-MAIN-COUPLING`'s `release_consequence` is under-inclusive: a second main-side coupling channel is undisclosed. The limit itself was scoped down by v6.0.0's freeze-lifecycle fix (ACTIVE/LANDED), which narrows the window it applies to, but the disclosure text was not re-verified against the second channel. Carried to 6.1.0. |
| **R5-NF2** | The README's sweep-completeness sentence was judged to overstate, with zero `known_limits` entries mentioning the surface. Partially addressed by the v6.0.0 README pass; not re-verified against this finding's exact claim. Carried to 6.1.0. |

Two open findings, both P4, both disclosed rather than closed by assertion. They
are the honest remainder.
