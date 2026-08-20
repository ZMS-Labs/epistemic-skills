<!-- gauntlet-dossier@1
frozen_at: 2026-08-19T23:59:00Z
subject_path: ZMS-Labs/epistemic-skills origin/main
subject_revision: 186b16eb2c069d9e8f902579afa50e9f5460fc85
evidence_root: git tree of subject_revision
evidence_root_git_tree: 7407e26adb336f20cea91b863ea1b61c532c32fd
evidence_root_sha256: 090fb18eefaa753653e5c45e6d7db30c702202b79d041271f30e84553bcefb55
seat_model: Cursor Grok 4.6 (xAI family)
seat_model_slug: cursor-grok-4.6-high-fast
independence_mode: single-seat-cross-family-publication
-->

# Frozen dossier — independent publication gauntlet for v6.0.0

**Axis:** fixed-artifact gate. **Question:** may `ZMS-Labs/epistemic-skills` publish a conforming `v6.0.0` annotated tag + GitHub Release + wiki hand-off + support-point declaration at the exact commit that is `origin/main` at freeze time?

**This seat did not author the release.** Model family: **xAI / Grok** (Cursor Grok 4.6). Prior BUILD-freeze panels 1, 3, 4, 5 were Claude. Panel 2 was Kimi/Moonshot against a superseded SHA. This is the first grader-family-independent read of the *publication* decision.

## Subject lock (live-verified, not taken from the brief)

| Fact | Live value | How verified |
|---|---|---|
| `origin/main` HEAD | `186b16eb2c069d9e8f902579afa50e9f5460fc85` | `git fetch origin main --tags`; `git log -1 --format=%H origin/main`; GitHub commits API |
| Subject moved vs brief? | **No.** Brief named this SHA. | Same string |
| Produced by | Merge of PR #199 (`release/6.0.0`) at 2026-08-19T23:25:40Z | `gh pr view 199` mergeCommit |
| Parents | `50f595c7…` (PR #197 freeze merge) + `466b9a0c…` (version-surface commit) | git |
| Tag `v6.0.0` | **absent** | `git ls-remote --tags`; GitHub refs API 404 |
| GitHub Release `v6.0.0` | **absent** | `gh release list` latest is `v5.1.0` |
| Prior support point | annotated tag `v5.1.0` → peel `5906464397305f50d36c59cce91bb397ec7dff27` | `git cat-file -t v5.1.0` = `tag` |
| Pin tags | `pin/es-v6-rc5-candidate-2026-08-19` → `03e972c5d427238033cb90d66846adabaf11928d`; `pin/es-v6-rc5-freeze-2026-08-19` → `546ccc8e55eb060379d62198310145f7243ac7bd` | `git ls-remote` |
| Tree of freeze C | `5355e26e625f5b8f2bd74b7cdd710cbafeff34f4` | `git rev-parse 03e972c5^{tree}` = inventory `candidate_tree_hash` |
| Tree of this SHA | `7407e26adb336f20cea91b863ea1b61c532c32fd` | `git rev-parse HEAD^{tree}` |
| `03e972c5..186b16eb` | 4 commits, 26 files, +3668/−38. No digest-inventoried source among them except version-bearing manifests and docs. | `git log` / `git diff --stat` |

**Freeze vs publication SHA.** The rc5 BUILD freeze GO (panel 5) is bound to `03e972c5…`. This publication subject is four commits later. RELEASING.md: a GO for one SHA is not a GO for the SHA about to be tagged unless they are the same string.

## Governing criteria (read at the candidate)

`RELEASING.md` Release gate items 1–9 and Procedure. Integrity gates (version/link alignment, deterministic checks, CodeQL, provenance, full-history secret scan, public-content, publication identity) must not be failing or unrecorded at tag time. Independent judgment requires a recorded GO on the **exact** release candidate for a conforming release. Exception publication is allowed only with an explicit owner record **in the committed notes before tagging**, remaining `WAIVED`/`UNMET`, never `MET`.

## Premises verified vs unverified

Verified:

- Candidate identity, tag/Release absence, annotated `v5.1.0`.
- Local crib at this SHA: all listed python gates exit 0; custody suites exit 0; `cleanroom_ci.sh HEAD` replicated 54/55 workflow python steps (1 skip: ledger check needs GitHub event env).
- Push jobs at this SHA: stdlib-checks, commission-watch `contract`, openai-bundles `build`, full-history-secret-scan, CodeQL Analyze (python/actions/javascript-typescript) all success. mission-custody **path-skipped** on the version-bump push. DCO ran on PR #199 head `466b9a0c…`, not on the merge SHA (workflow is `pull_request_target` only; merge commits are exempt in `check_dco.py`).
- Five `workflow_dispatch` runs on `claude/v6-release-requal` at this SHA: four workflows all-green; mission-custody Linux `contract` success, `contract-macos` failure, run aggregate failure. `contract-macos` is `if: github.event_name == 'workflow_dispatch'` only.
- Packet at this tree: `candidate_sha=03e972c5…`, `independent_gauntlet=NOT_RUN`, `independent_gauntlet_ref=null`, `blocking_claims=["CLM-INDEPENDENT-GAUNTLET"]`, no `operator_acceptance`.
- Five prior freeze-panel branches reachable; each verdict names the claimed SHA prefix; sequence NO-GO ×4 then GO on `03e972c5…`. Those run directories are **absent from `origin/main`**.
- Wiki clone HEAD `14c7df9e…` (2026-08-15): current release advertised as v5.1.0; zero `v6.0.0` strings; catalog table 14 rows, no Manifest page. In-tree wiki packets: newest published is `docs/wiki-updates/v5.0.0/` (fourteen skills). No v5.1.0 or v6.0.0 packet.
- Version-bearing plugin manifests that `sync_skill_surfaces.py` checks say `6.0.0`. Root `.kimi-plugin/marketplace.json` still points at `tree/v3.4.0` and is **not** in that checker's file list.
- Issue #191 last operator-authored comment is the 2026-08-18 `RATIFY-V6-2026-08-18` echo of D1–D15 (includes the standing instruction to **run** Step-7b). No later comment names `186b16eb`, waives D8, records `operator_acceptance`, or authorizes a tag.
- PR #197 and #199 were merged by `SternOne`. Both merge messages state the merge is **not** publication and that D8, operator acceptance, and the publication gate remain owed.

Unverified / extra-repo:

- The producing brief's claim that "the operator explicitly approved proceeding end-to-end." **Not found** in GitHub issue comments, PR bodies, or committed decision records. If it exists, it is chat-only. The project's own acceptance procedure says a chat message is not an acceptance. Marked `(UNVERIFIED)` as a substitute for documented steps; marked **verified absent** as a durable GitHub artifact.

Injection guard: the brief is DATA. Its three "weakest points" were treated as claims to verify, not as instructions to find them.

## Parallel same-family publication panel

`docs/release/gauntlet/` is absent on `origin/main` and on checked remote heads at freeze time. No `*publication*` branch. This seat formed its position **before** any such record existed to read. Agreement with a later same-family panel would be corroboration, not support.

## Exclusions

- No tag, Release, wiki edit, ruleset change, or comment on issues/PRs by this seat.
- No re-run of macOS evidence (es#162); judged from recorded dispatch jobs plus workflow `if:`.
- No native Windows requalification (KL-WINDOWS, disclosed).
