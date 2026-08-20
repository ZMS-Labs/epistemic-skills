# VERDICT OF RECORD — independent publication gate, v6.0.0

**Run:** `es-v6-publication-gate-2026-08-19`
**Subject:** the PUBLICATION act for `v6.0.0` at exact commit `186b16eb2c069d9e8f902579afa50e9f5460fc85` — annotated tag, non-draft GitHub Release from `docs/release/RELEASE-6.0.0.md`, wiki hand-off package, any ruleset/settings change, and the SUPPORT-POINT declaration.
**Governing gate:** `RELEASING.md` at the candidate, items RG-1…RG-9 and the Procedure section, read in full by this seat.
**Date:** 2026-08-19/20 (UTC boundary crossed during the review).

---

## 1. Computed verdict

> ## **NO-GO** for publishing `v6.0.0` at `186b16eb2c069d9e8f902579afa50e9f5460fc85`.

Seven of nine gate items fail. Six of the failures are **integrity gates**, which `RELEASING.md` places outside the exception mechanism entirely: *"Do not create a tag while one is failing or unrecorded. Fix the candidate, rerun the gate on the new exact commit, and only then publish."*

**The candidate is superseded.** Every cure for the blocking findings requires text committed to the tree — an authorization line, an evidence table, a `.kimi-plugin/marketplace.json` URL, the v6 verdict lineage, an exception or waiver record. Procedure step 4 is explicit: *"Any correction creates a new candidate and invalidates earlier exact-commit evidence."* Therefore `186b16eb` cannot become a conforming release by any sequence of acts, and the five exact-commit requalification runs gathered at it (32313229574 / 32313232046 / 32313238605 / 32313240639 / 32313248657) will be void the moment the first cure lands. Say it plainly: **this SHA is not fixable; it is replaceable.**

**Nor is an exception release available here.** `RELEASING.md` scopes exception semantics to the independent judgment gate alone — *"the owner authorizes publication despite an explicitly named unmet **judgment** gate."* RG-4, RG-5, RG-6 and RG-9 are integrity gates. An owner override cannot lawfully carry them, and in any case the exception record itself must be *in the committed notes before tag creation*, which again mints a new candidate.

**What is not wrong.** The engineering is strong and I could not falsify its substance. The deterministic suite passes in my own fresh clone (54/55 replicated steps, 0 fail, 1 named ci-context skip). Every required job at the candidate is green, CodeQL included. The v6-assurance seal genuinely binds. The in-tree version bump is complete and every `v6.0.0`-pinned repository path resolves. Fifteen skills, counted two ways. The 8,636-byte description claim matches the oracle exactly. This NO-GO is not about the code. It is about the release record and two procedural acts that have not happened — which is precisely the standard this release exists to establish.

---

## 2. Seat independence and authority

| Property | Value |
|---|---|
| Structure | Isolated judge over four gate-seat reports plus one adversarial challenger, all author-dispatched. |
| Authorization | The dispatcher prepared the release under review and assembled this panel. The operator approved the promotion gauntlet (scope: full v6.0.0 publication). |
| Family | Single model family (Claude/Anthropic) for dispatcher, all reporting seats, and this judge. **This is a disclosed independence limit, not independence.** |
| Cross-family status | One genuinely cross-family publication read exists on this exact SHA — the xAI/Grok single-seat review at `docs/gauntlet-runs/es-v6-publication-grok-2026-08-19/` (PR #200, verified live). It is not this panel's product and I adopt none of its reasoning; I record its existence and verdict as a primary fact. |
| D8 status | The standing Step-7b cross-family consult for the rc5 BUILD GO is **OWED and NOT DISCHARGED**. The Grok publication review does not discharge it — D8 is keyed to the BUILD GO-posture verdict at `03e972c5` and to operator acceptance, a different subject and a different gate. |
| Method | No seat's word was adopted for any load-bearing fact. Twenty-two register items were re-executed from primary sources: git objects in my own fresh clone, live unauthenticated GitHub REST, the wiki repository, and the repo's own oracles run locally. |
| Writes | None. No push, tag, comment, dispatch, or any write to GitHub was performed by this seat. |

**What this verdict authorizes:** nothing. A verdict is an artifact, not an act. The tag, the Release, the wiki hand-off, any ruleset change, and the support-point declaration remain operator acts under `RELEASING.md`, performed in a separate PROMOTION_RUN with its own consent.

---

## 3. RG-1 … RG-9 dispositions

### RG-1 — Candidate identity and scope · **PASS-QUALIFIED**

`git rev-parse HEAD` in a fresh clone = `186b16eb2c069d9e8f902579afa50e9f5460fc85`, equal to live `origin/main` (REST, `default_branch=main`, `visibility=public`). Working tree clean. The candidate is a two-parent merge of `50f595c7` (PR #197 freeze) and `466b9a0c` (release/6.0.0), authored SternOne, 2026-08-19T23:25:39Z — i.e. the commit produced by merging release PR #199, exactly as Procedure step 4 specifies. Release-note path `docs/release/RELEASE-6.0.0.md` exists; line 1 `# Release 6.0.0`, line 3 `Support point: v6.0.0`. Release scope is frozen and confined: PR #199 touched 12 files (eleven version surfaces plus the new note); no skill, contract, or workflow content moved.

**Qualification:** the note *describes* the candidate ("the commit produced by merging this release branch") rather than *naming* it. `grep -c 186b16e docs/release/RELEASE-6.0.0.md` = **0**. RG-1's three bullets are satisfied as written; the identity defect is graded under RG-9, where `RELEASING.md` puts it. I record that the note's SHA claims that *are* present are TRUE and carefully drawn: `03e972c5` and `546ccc8e` both exist, are described correctly, are ancestors of the candidate, and the two rc5 pins peel to them. The sentence "the publication gate runs against that commit — not against this file's description of it" is precise and honest, and I want that on the record.

### RG-2 — Release-specific decisions and risk acceptance · **FAIL**

Four gaps ship with no owner, no bounded scope, no revisit trigger, and no exit criterion, and none is disclosed in the committed notes:

1. **The owed acts.** The GO of record's own `run-record.json` lists under `owed_before_acceptance` (fetched from `origin/claude/es-v6-rc5-review`, commit `a07231e3`): *"D8 Step-7b cross-family consult — OWED and NOT discharged by this single-family panel. The prior kimi consult was against superseded candidate 6db8c50 and does not transfer to 03e972c"*; operator acceptance per items 1–5; operator confirmation/echo-certification of D16–D19; freeze hygiene. Items 1–3 are undischarged. The release note discloses none of them.
2. **`.kimi-plugin/marketplace.json` pinned to `v3.4.0`** (PG-07) — pre-existing, never recorded as an accepted gap.
3. **The live wiki two majors stale** (PG-08) — the note never mentions the wiki at all.
4. **The sealed packet shipping `NOT_READY` / `NOT_RUN` / non-empty `blocking_claims`** inside the tag (PG-09) — undisclosed.

`RELEASING.md` RG-2: *"Any accepted gap has an owner, bounded scope, revisit trigger, and exit criterion… No wildcard waiver is permitted."* No exception record exists either: `grep -niE 'authoriz|WAIVED|UNMET|exception'` over the note returns nothing responsive.

### RG-3 — Evidence retention · **FAIL**

`git ls-tree --name-only HEAD docs/gauntlet-runs/` at the candidate returns exactly seven directories — `commission-watch-pr110-2026-08-07`, `epistemic-flexibility-v3-2026-07-22`, `epistemic-skills-suite-stress-test-2026-07-23`, `es-v510-publication-2026-08-15`, `successor-104-105-2026-08-07`, `upgrades-landing-2026-08-03`, `v4.0.0-step7b`. **Zero v6 records.** The GO and all four NO-GOs live only on unmerged branches; I confirmed `git merge-base --is-ancestor origin/claude/es-v6-rc5-review 186b16eb` returns **not an ancestor**.

RG-3: *"Blinded campaigns, negative controls, dissent, terminal failures, and prior null results remain at immutable coordinates."* Four terminal failures and three preserved P3 dissents sit on force-pushable, deletable refs inside a namespace no ruleset covers (live `/rulesets`: `protect-version-tags` scopes to `refs/tags/v*`; `fleet-baseline-default-branch` to `~DEFAULT_BRANCH`).

Compounding this into a falsehood at an immutable coordinate: **RELEASE-6.0.0.md:122-124 states "Run records live under `docs/gauntlet-runs/`. The verdicts are retained at their original coordinates."** In the tree a user installs from the tag, that is untrue. The precedent cuts the other way — v5.1.0's panel record *is* in-tree at `docs/gauntlet-runs/es-v510-publication-2026-08-15/`, which is the only reason `RELEASING.md:123` can cite it today as binding ruling lineage.

**Not falsified:** the "none was rewritten" clause. Each arbitration has exactly one commit in its branch history and each names a subject SHA matching its run-record. A force-push to an unprotected branch is undetectable from a clone; that is the risk, not an observed rewrite.

### RG-4 — Version and link alignment · **FAIL**

**Bullet 1 — FAIL.** Programmatic walk of every tracked manifest: `.claude-plugin/marketplace.json` 6.0.0, `.cursor-plugin/marketplace.json` 6.0.0, `.cursor-plugin/plugin.json` 6.0.0, `.kimi-plugin/plugin.json` 6.0.0, `gemini-extension.json` 6.0.0, and all four `plugins/epistemic-skills/.*-plugin/plugin.json` 6.0.0; `EXPECTED_VERSION = "6.0.0"`; README line 13 `**Version 6.0.0.**`. But **`.kimi-plugin/marketplace.json` still installs `https://github.com/ZMS-Labs/epistemic-skills/tree/v3.4.0`** — a live, tracked, version-bearing install source, and the *one* manifest omitted from the nine-path `manifests` tuple in `outsource/tests/run_tests.py:318-332` that enforces version alignment. I re-executed both: the file's URL and the tuple's contents. v3.4.0 ships seventeen skills and predates the es#137 fixes the note calls "the reason to upgrade."

**Bullet 2 — PASS.** Three `v6.0.0`-pinned URLs exist in the tree; I resolved each repository path with `git cat-file -e` at the candidate: `plugins/epistemic-skills/skills` OK, `plugins/epistemic-skills/skills/metacognate/reference/routine-fast-path.md` OK, tree root OK. **No link will 404 at the tag.** This is the failure mode a blind bump usually produces and it did not happen here.

**Bullet 3 — FAIL, three ways.**
- *Live wiki:* cloned from `epistemic-skills.wiki.git`, HEAD `14c7df9e` dated 2026-08-15. `Skill-Catalog.md:7` "exactly **fourteen** skills"; `Home.md:17` "v5.0.0 ships **fourteen** skills"; `Glossary.md:41` "v5.0.0 support boundary — Current immutable support point (fourteen skills)"; `FAQ-and-Troubleshooting.md:9` gives actionable install guidance pinned to v5.0.0; `Contributing.md:51` "the collection contains fourteen skills: router, Helix, and nine disciplines" — present tense, both names retired. Nine retired-seat pages remain; **no `Skill-Manifest` page exists** for the seat carrying this release's headline security fix. README:236 designates this wiki the practical handbook.
- *Shipped package routes to a retired seat at a path that does not exist:* `evidence-locked-uat/SKILL.md:23` and `recon/reference/mode-brief.md:49` both send the reader to `using-epistemic-skills/reference/routine-fast-path.md`; `metacognate/reference/routine-fast-path.md:3` says "This reference is part of `using-epistemic-skills`" — **and that third file is the exact file README pins at `blob/v6.0.0/`.** No such directory exists in the package (15 dirs, verified). `check_no_phantom_skills.py` exits 0 because its path regex is anchored to the full package path; I did not re-plant the challenger's probes but I verified the three references, the absent directory, and the green oracle myself.
- *Marketplace enumeration:* both `.claude-plugin/marketplace.json` and `.cursor-plugin/marketplace.json` say "fifteen self-triggering skills" then enumerate fourteen. Programmatic membership scan against the 15 packaged names: **missing `manifest`** in both.

**Not falsified (recorded because a NO-GO is only useful if its clean rows are trustworthy):** residual 5.1.0 occurrences are all legitimately historical; the live GitHub repo description is current and carries no retired seat name; the skill count is fifteen by two independent countings; the "same fifteen skills as v5.1.0" claim is exactly true; the 8,636-byte figure matches `check_description_budget.py --report` to the byte.

### RG-5 — Deterministic and static-analysis evidence · **FAIL**

**The substance is green.** I re-ran the deterministic suite in my own fresh clone: `bash .github/scripts/cleanroom_ci.sh 186b16eb…` → exit 0, "replicated 54 of 55 workflow python steps, pass=54 fail=0 need-args=0 ci-context=1 missing-dep=0"; the single skip is the `$RUNNER_TEMP` variant of the ledger oracle, named with its reason, and the same oracle passes via `--base-git-ref FETCH_HEAD`. All five requalification runs verified live at `head_sha=186b16eb2c069d9e8f902579afa50e9f5460fc85`, branch `claude/v6-release-requal`, `event=workflow_dispatch`, `run_attempt=1`. CodeQL at the candidate: `Analyze (python)`, `Analyze (actions)`, `Analyze (javascript-typescript)` all success. **No gating job is red anywhere at this candidate.**

**The gate still fails, on its own terms.** Run `32313232046` (mission-custody-contract) concluded **failure**: job `contract` success; job `contract-macos` failure at **step 8 "Custody mission lifecycle unit tests"**, with steps 9–12 (CLI black-box, gate unit, enforcement hook, three-subprocess continuity proof) **skipped**. I pulled the per-step conclusions from the jobs API myself. RG-5's carve-out is conjunctive:

| Condition | Ruling |
|---|---|
| (a) non-gating purpose documented in the workflow file | **MET** — `mission-custody-contract.yml` documents `contract-macos` as dispatch-only, "this job exists to SETTLE a filed claim, not to gate merges." |
| (b) failure is the diagnostic's designed output, settled and disclosed on its issue | **MET** — es#162, five comments, reproduced across four macOS runs, same step, same two tests. |
| (c) **the release record names the exact failing step and tests** | **UNMET** — `git grep` for each of the five run IDs across the whole candidate tree returns zero files. RELEASE-6.0.0.md names no run, no job, no step, no test; `KL-MACOS-162` describes only the phenomenon. |

RG-5's next sentence governs: *"Any other red, in any job of a suite dispatched at the candidate, fails this gate."* v5.1.0 did this correctly, naming both tests. The defect is silence, not sickness — but the gate is written to fail on silence, deliberately, and `RELEASING.md` adds: *"A row without an immutable evidence coordinate is not MET merely because the work is remembered to have happened."*

**Residual worth recording:** because step 8 aborted, four custody suites — including the three-subprocess continuity proof — went **unmeasured on macOS at this candidate**, for a release whose headline is a custody permission-boundary fix. `KL-MACOS-162` discloses only the case-distinctness class and understates that.

### RG-6 — Security, public content, and provenance · **FAIL** (record and accuracy limbs)

**Mechanical limbs — the strongest evidence in this release.** Full-history secret scan green with the pinned scanner; the one `.gitleaks.toml` path exemption independently probed and proven rule-scoped, path-anchored, and narrow, with provider-branded credentials still firing inside it; `check_public_content.py --self-test` and the live run both exit 0 in my clean-room (7 seeded RED controls; 7 patterns; 37 digest-verified allowlist entries, independently recomputed by the RG-5/RG-6 seat with 0 mismatches and 0 inert entries). License surfaces consistent (GPL-3.0-or-later across LICENSE, README, and three plugin manifests). I affirm all of this.

**Bullet 3 — FAIL.** No 6.0.0 public-content *review* artifact exists. `docs/release/` holds `PUBLIC-RELEASE-REVIEW-2026-07-17.md`, its 2026-07-21 addendum, and the 5.0.0 post-release review — nothing for 6.0.0. The packet's `evidence/public-content.json` is a mechanical receipt bound to `03e972c5`, not a release-diff review at the candidate. RG-6 requires findings and dispositions "recorded at an immutable path."

**Bullet 4 — FAIL.** `CONTRIBUTING.md` states an unqualified universal — every commit in a PR must carry an author-matching `Signed-off-by` — while the enforced `check_dco.py` carries an unconditional merge-commit exemption and a closed five-SHA attestation list it never mentions. That inaccurate provenance surface would ship at an immutable tag. Aggravating and independently established by the RG-6 seat: `dco.yml` triggers only on `pull_request_target`, so the object certified is the PR head that squash-merge discards; **no DCO check-run attaches to the candidate** (13 check-runs, none named DCO — I confirmed the census), and 19 commits with no sign-off line landed on main *after* the gate existed.

### RG-7 — Supported harness evidence · **FAIL**

RG-7: *"Each supported harness is exercised live against the candidate or receives an explicit verification tier and limitation **in the release notes**."* RELEASE-6.0.0.md has no harness section, no tier table, no per-harness row, and no cross-reference to `docs/release/HARNESS-VERIFICATION-MATRIX-SUCCESSOR-2026-08-07.md`. Its only harness-adjacent text is `KL-LIVE-ENV`. README:222-233 does carry a nine-row table with honest boundaries — but three rows carry verification statements and six carry design or install prose, and the gate names the notes, not the README. v5.1.0 satisfied this row and stated plainly "No new live plugin-harness executions in this release."

### RG-8 — Independent publication judgment · **FAIL**

No `GO` exists on `186b16eb`. The BUILD GO of record is bound to `03e972c5` and states in its own binding statements that promotion — merge, pin registration, tag, release — is not authorized by it. Two publication-scoped verdicts now exist against this exact SHA and **both are NO-GO**: the xAI/Grok cross-family review (PR #200, `state=open`, `draft=true`, head `65f81697`, record at `docs/gauntlet-runs/es-v6-publication-grok-2026-08-19/`, verdict text verified by me from the branch object — "Computed verdict: NO-GO for publishing v6.0.0 at 186b16eb…"), and this one. RG-8: *"`NO-GO`, unresolved P1/P2, or an unrun gate holds a conforming publication."*

I note without adopting it that the Grok seat reached its NO-GO independently and its per-gate table converges with mine on RG-7, RG-8 and RG-9. Convergence across model families on a NO-GO is weak evidence, but it is the only cross-family signal available, and it points the same way.

### RG-9 — Publication identity plan · **FAIL**

*"The exact candidate SHA, tag name, release-note path, and intended Release target are recorded before tag creation."* `git grep 186b16e` at the candidate returns **nothing**; the SHA appears nowhere in its own tree, on any branch, or on the tracker. Procedure step 7 additionally requires, in the committed notes, *"a line naming the verdict read, the exact candidate SHA authorized, and the owner"* — absent, along with any disarm/re-arm record. And the mandated seven-row evidence table is absent entirely: `grep -n '^|'` over the note yields only the nine-row known-limits table.

The bootstrap objection ("a commit cannot contain its own SHA") does not excuse this and I reject it: v5.1.0 solved the identical problem, and `RELEASING.md` step 7's whole point is that a GO for one SHA is not a GO for another unless they are the same string.

**Publication state, verified:** `git/ref/tags/v6.0.0` → 404; `releases/tags/v6.0.0` → 404; latest release v5.1.0. Ruleset `protect-version-tags` id 20090781, target=tag, `enforcement=active`, rules `[update, deletion, creation]`, `bypass_actors=null`, conditions `refs/tags/v*` — the disarm-as-authorization control is armed exactly as `RELEASING.md` describes. **The one-way door is still closed. Nothing here is irreversible yet.**

---

## 4. Findings adjudicated

Severity is this panel's, not any seat's. "Blocks" means blocks a *conforming* publication at this SHA.

| ID | Sev | Blocks | Finding | Source seats |
|---|---|---|---|---|
| **PG-01** | P1 | yes | **No publication identity or authorization record.** Note never writes `186b16eb`; no line naming verdict read, SHA authorized, and owner; no disarm/re-arm plan. RG-9 + Procedure step 7. | RG14-F3, RG2-02, F1, ADV-01 |
| **PG-02** | P1 | yes | **No GO on this SHA; two publication NO-GOs of record** (Grok cross-family, and this panel). BUILD GO is bound to `03e972c5`. RG-8. | F4, ADV-08 |
| **PG-03** | P1 | yes | **v6 verdict lineage absent from the tagged tree** — four NO-GOs, one GO, three preserved dissents on unprotected mutable refs — while the note asserts they live under `docs/gauntlet-runs/`. False statement made immutable. RG-3. | RG14-F1, RG3-01, F6, ADV-03 |
| **PG-04** | P1 | yes | **No gate evidence table; zero immutable evidence coordinates in the note.** No run IDs, no CodeQL row, no description-byte-delta row, no publication-identity row. Regression from RELEASE-5.1.0.md. | RG5-F1, RG3-06, F2, ADV-02 |
| **PG-05** | P1 | yes | **D8 Step-7b consult owed and not run; operator acceptance never recorded; no exception record.** GO's own `owed_before_acceptance` names both; #191's last comment (2026-08-18T20:41:38Z) predates the rc5 candidate and the GO; packet has no `operator_acceptance` key. See §5A for the full ruling. | RG2-03, F4, ADV-07 |
| **PG-06** | P2 | yes | **RG-5 carve-out (c) unmet**: `contract-macos` red at the candidate, release record names neither step nor tests. Substance benign; the gate fails on the silence. | RG5-F1, RG14-F4, F3, RG2-07, ADV-06 |
| **PG-07** | P2 | yes | **`.kimi-plugin/marketplace.json` installs `tree/v3.4.0`** and is the one manifest omitted from the version oracle. Pre-existing; never recorded as an RG-2 accepted gap. | RG14-F2 |
| **PG-08** | P2 | yes | **Live wiki two majors stale** — fourteen skills, v5.0.0 install guidance, retired seats in present tense, no `Skill-Manifest` page — and **no v6.0.0 package in `docs/wiki-updates/`** though the wiki hand-off is inside the intended publication act. Discharged by wiki-repo edits alone; the *record* of the gap is what needs a commit. | RG14-F5, RG2-10, F7 |
| **PG-09** | P2 | yes | **The tag would ship `promotion-packet.json` reading `readiness=NOT_READY`, `independent_gauntlet=NOT_RUN`, `blocking_claims=['CLM-INDEPENDENT-GAUNTLET']`** (P1 UNPROVED in the matrix), with no in-tree rebuttal and no disclosure in the note. Structurally un-flippable here: the validator requires the verdict artifact on disk. | F5, ADV-03, HON-12 |
| **PG-10** | P2 | yes | **RG-7: no per-harness verification tier in the release notes.** | RG7-05, F8 |
| **PG-11** | P2 | yes | **"Reviewed by five independent panels"** is denied by the GO record's own `seat_structure` ("an independence LIMIT, not independence"; single family throughout); and the note records **no independence limits at all**, a column v5.1.0 filled honestly. Each panel also judged a different candidate; only panel 5 saw `03e972c5`. | RG2-04, F12 |
| **PG-12** | P3 | no | **No 6.0.0 public-content review artifact** at an immutable path (RG-6 bullet 3). | RG6-F6 |
| **PG-13** | P3 | no | **Provenance surface inaccurate**: `CONTRIBUTING.md` states an unqualified DCO rule the enforced checker does not apply; DCO never runs against any commit that lands; 19 no-sign-off commits landed post-gate. | RG6-F5, RG6-F7, RG2-09 |
| **PG-14** | P3 | no | **Three shipped package files route to retired `using-epistemic-skills/…`, a path absent from the package** — including `metacognate/reference/routine-fast-path.md`, the file README pins at `blob/v6.0.0/`. The anti-phantom gate is structurally blind to the bare-path form. Pre-existing since v5.0.0. | ADV-04 |
| **PG-15** | P3 | no | **Marketplace "full collection" descriptions enumerate 14 of 15, omitting `manifest`** — the seat carrying the headline security fix. Count linter validates the numeral, never the enumeration. | RG14-F6 |
| **PG-16** | P3 | no | **Migration section understates the change.** "The one behavioral change to expect is stricter custody refusals" is false: nine SKILL.md files newly instruct appending to `runs/ledger.jsonl` after every engagement (v5.1.0 5/15 → candidate 14/15; I diffed each). Disclosed under "What ships," so the note contradicts itself rather than conceals. No rollback pointer, no failure shape, no enumeration of the closed bypasses. | ADV-05, HON-08 |
| **PG-17** | P3 | no | **rc5 pin tags are lightweight** (`ls-remote` shows no `^{}` peel) in a namespace no ruleset protects, a discipline regression from the annotated rc2 pins one day earlier. Mitigated: both SHAs are ancestors of the candidate, so deletion orphans nothing. | HON-11, F10 |
| **PG-18** | P3 | no | **Live `main` already advertises v6.0.0 as an existing support point** behind links that 404 today. Real user-facing defect — and a source of pressure to publish that must not be mistaken for evidence for publishing. | F9 |
| **PG-19** | P3 | no | **Support-point promise over-reaches on platform**: macOS custody lifecycle unmeasured/red at the candidate with no README row naming macOS; Windows recipe shipped with `KL-WINDOWS` disclosing no native requalification; `KL-GUARD-LEXICAL` residual symlinked-parent false-allow sits in the limits table but not adjacent to "this is the reason to upgrade." | F11 |
| **PG-20** | P4 | no | Note cites the assurance contract as `contracts/v6-assurance`; the real path is `plugins/epistemic-skills/contracts/v6-assurance/`. "Twenty-six class claims" is accurate for the class family but the matrix holds 72 claims. | HON-13 |
| **PG-21** | P4 | no | `check_pin_tags.py` exits 0 while its registry names only the superseded rc2 pins. **Downgraded from the reporting seat's framing:** I read the registry comment, which documents a deliberate one-freeze registration lag with a stated rationale (kimi ruling S5 / CL-3). This is a documented discipline, not an unrecorded gap. The rc5 pins do resolve correctly (`ls-remote` verified). | RG14-F7 |
| **PG-22** | P4 | no | DCO merge-commit exemption realized: 2 of 24 reachable merges diverge from `git merge-tree` of their parents, one authoring 69 insertions across 19 files with **zero conflict markers** — so the note's framing of the gap as "a conflict resolution" does not cover it. | RG6-F8 |
| **PG-23** | P4 | no | `check_dco.py` self-contradictory count ("these five" / "exactly these six", `len==5`); `github_commits()` pages against a 250-cap endpoint, a latent fail-open on >250-commit PRs, undisclosed. | RG2-09 |
| **PG-24** | P4 | no | Two tracked files embed build-host scratchpad absolute paths with session UUIDs; the public-content pattern set is structurally blind to that class. No credential, host, or personal data exposed. | RG6-F9 |

### Dissents preserved

- **Wiki severity.** The RG-8/RG-9 seat grades PG-08 P2 rather than P1 because the wiki is mutable and repairable post-tag without a new version; the RG-1/RG-4 seat grades it a blocking RG-4 failure outright. **I adopt P2-blocking** and preserve both positions. The aggravator that moved me: v5.1.0 recorded a post-tag handbook pass as a follow-up and it was never performed — "we will fix it after the tag" is 0-for-1 in this project.
- **PG-07 and PG-08 as pre-existing conditions.** The RG-1/RG-4 seat records in fairness that neither is a regression introduced by this release. I agree on the facts and preserve the mitigation, and still hold both blocking: RG-2 forbids leaving an integrity gap *unrecorded* at tag creation, and honest recording — not silent inheritance — is the cheap discharge.
- **PG-21.** The reporting seat graded it an oracle-coverage gap; I downgraded it on reading the registry's own documented lag rule. The seat's fact is correct; my reading of its significance differs.

---

## 5. Rulings on the procedural questions

### 5A. The D8 consult and operator acceptance — **BLOCKING; publication may NOT proceed before them**

Verified as fact, not adopted: (i) D8's text at `docs/v6/operator-decision-record-2026-08-18.md:52-54` — *"Standing instruction: run Step 7b (manual-handoff consult) at the next GO-posture verdict, before operator acceptance"*; (ii) `OPERATOR-ACCEPTANCE-PROCEDURE.md` Sequence steps 3–5, ending *"Promotion… is a separate PROMOTION_RUN under RELEASING.md. Nothing in steps 1–4 starts it"*; (iii) no Step-7b artifact exists for v6 anywhere (only the historical `docs/gauntlet-runs/v4.0.0-step7b/`); (iv) no `operator_acceptance` object in the packet, and #191's last comment predates both the rc5 candidate and the GO; (v) the GO record itself declares D8 owed and the earlier kimi consult non-transferable.

**Ruling.** Publication may not proceed before both. I name them as blocking conditions on any conforming publication.

The operator's end-to-end approval of the promotion gauntlet does **not** cure them, for four independent reasons:

1. **Form, not authority.** The operator plainly *can* substitute — acceptance item 2 expressly permits "an explicit operator waiver" of the Step-7b consult. But the same document forecloses informal substitutes in terms: *"An acceptance recorded any other way (chat message, commit message, enum flip) is not an acceptance under this procedure."* A general approval to run the gauntlet is neither an explicit waiver of a named standing instruction nor the recorded acceptance artifact.
2. **Scope.** The approval authorized *this review*. This review's output is NO-GO. An approval to run a gate is not an approval of its result.
3. **The dispatcher is not the operator.** This panel is author-dispatched and the disclosure at the head of my prompt instructs me to treat its framing as potentially self-serving. A claim of operator approval arriving inside a dispatch prompt is exactly the class of claim that must resolve to a durable artifact, and it does not.
4. **It would not help anyway.** Even a perfectly recorded waiver of D8 and a perfectly recorded acceptance leave RG-3, RG-4, RG-5, RG-6 and RG-9 failing. Those are integrity gates, and `RELEASING.md` places them outside the exception mechanism: an owner may authorize publication despite an unmet **judgment** gate, not despite a failing or unrecorded integrity gate.

I record the substantive stake, not merely the procedural one. D8 exists to correct correlated-blindspot risk in a lineage that is single-family from dispatcher through judge and says so about itself. This project's own history at `docs/superpowers/plans/2026-07-22-epistemic-flexibility-v3.md` records a Step-7b consult **reopening a P1** and producing two accepted dissents after a single-family panel had closed them. Skipping it also silently discharges nothing: the GO routed R5-NF7, R5-NF8 and R5-NF11 to the acceptance gate, so bypassing acceptance leaves three findings with no remaining gate — including an unratified DCO attestation of five commits authored by the identity it authorizes, which publication would make permanent.

### 5B. Is the shipped `NOT_READY` packet defensible at a tag? — **No, as shipped; yes, if disclosed**

The packet is an honest document and its refusal to certify itself is the v6 assurance contract working. `validate_v6_assurance.py` exits 0 **because** the packet declares non-readiness — that green is the packet correctly reporting it is not ready, and must never be cited as support for publication. But an immutable support point that contains a machine-readable P1 UNPROVED release-blocking claim, with the artifact that would discharge it living outside the tag, is not defensible. The correct discharge is either the arbitration in-tree and the packet regenerated against the new candidate, or an explicit sentence in the notes telling the reader what that file is and why it reads NOT_READY at a published tag. Both require a commit.

---

## 6. Re-verification register

Every row below I executed myself, in `…/scratchpad/judge/repo` (fresh clone, detached at the candidate) and `…/scratchpad/judge/wiki`, against git objects, live unauthenticated GitHub REST, or the repo's own scripts. No seat's word was adopted.

| # | Item | Method | Result |
|---|---|---|---|
| 1 | Candidate is head of default branch | `git rev-parse HEAD`; REST repo | `186b16eb…` = origin/main; public; default `main` — **confirmed** |
| 2 | Candidate is the PR #199 merge commit | `git log -1 --format='%H %P'` | parents `50f595c7` + `466b9a0c`, SternOne, 2026-08-19T23:25:39Z — **confirmed** |
| 3 | All version surfaces read 6.0.0 | JSON walk of every tracked manifest + `EXPECTED_VERSION` + README | 10 surfaces = 6.0.0 — **confirmed** |
| 4 | No stale current-version claim | grep 5.1.0 outside history dirs | all hits historical/deliberate — **confirmed clean** |
| 5 | **`.kimi-plugin/marketplace.json`** | read file; read `manifests` tuple at run_tests.py:318 | pinned `tree/v3.4.0`; **omitted from the oracle** — finding **confirmed** |
| 6 | Every `v6.0.0`-pinned path exists | extract 3 URLs; `git cat-file -e` each | all resolve — **confirmed PASS** |
| 7 | Skill count | `ls-tree` dirs (15) and `ls-files '*/SKILL.md'` (15) | fifteen — **confirmed** |
| 8 | `docs/gauntlet-runs/` at candidate | `git ls-tree --name-only HEAD` | 7 dirs, **zero v6** — **confirmed** |
| 9 | GO branch not an ancestor | `git merge-base --is-ancestor` vs `a07231e3` | **NOT ancestor** — confirmed |
| 10 | GO record's owed items | `git show FETCH_HEAD:…/run-record.json` | verdict GO, subject `03e972c5`, four `owed_before_acceptance` incl. D8 — **confirmed verbatim** |
| 11 | Five requalification runs | REST run + jobs + steps for each | all real, dispatch, `head_sha=186b16eb`, attempt 1; four success; `32313232046` **failure**, `contract-macos` step 8, steps 9–12 skipped — **confirmed** |
| 12 | CodeQL at candidate | REST check-runs (13) | three Analyze matrices success — **confirmed** |
| 13 | Deterministic suite, fresh clone | `cleanroom_ci.sh 186b16eb…` | exit 0, 54/55, 1 named ci-context skip — **confirmed PASS** |
| 14 | Packet readiness fields | parse `promotion-packet.json` | `NOT_READY` / `refused` / `NOT_RUN` / ref `null` / `blocking_claims=['CLM-INDEPENDENT-GAUNTLET']` / `candidate_sha=03e972c5` / **no `operator_acceptance` key** — confirmed |
| 15 | `CLM-INDEPENDENT-GAUNTLET` | parse matrix | UNPROVED, oracle requires on-disk verdict bound to the SHA — confirmed |
| 16 | Operator acceptance | REST #191 comments (5, last 2026-08-18T20:41:38Z); tree grep | **none exists** — confirmed |
| 17 | D8 text and acceptance sequence | read both docs at the candidate | quoted verbatim in §5A — confirmed |
| 18 | Release note content | full read + greps | no candidate SHA (count 0), no authorization line, no evidence table, no run IDs, no harness tiers, no independence limits; `docs/gauntlet-runs/` claim present at :122 — **confirmed** |
| 19 | Tag/Release absent; ruleset armed | REST 404 ×2; `/rulesets/20090781` | closed door; active, `refs/tags/v*`, create+update+delete, **no bypass actors** — confirmed |
| 20 | Pin tag types | `git ls-remote --tags` | rc5 pins **lightweight** (no `^{}`); rc2 and v5.1.0 annotated — confirmed |
| 21 | Live wiki | clone; HEAD `14c7df9e` 2026-08-15; greps | fourteen skills, v5.0.0 install guidance, 9 retired-seat pages, **no `Skill-Manifest`** — confirmed |
| 22 | Retired-name routing in package | grep + `ls skills/` + run the gate | 3 files route to absent `using-epistemic-skills/…`; `check_no_phantom_skills.py` exits 0 — **confirmed** |
| 23 | Evidence-emission delta | per-file diff vs `v5.1.0` | 5/15 → 14/15; nine skills newly instruct writing `runs/ledger.jsonl` — **confirmed** |
| 24 | Marketplace enumeration | membership scan vs 15 names | both files **missing `manifest`** — confirmed |
| 25 | Description-byte claim | `check_description_budget.py --report` | 8636 across 15 (ceiling 8636) = README's figure — **confirmed PASS** |
| 26 | `check_pin_tags.py` | run it; read registry | exit 0, four ok lines, rc5 absent — **confirmed**, and lag documented in-file (basis for PG-21 downgrade) |
| 27 | **PR #200 / cross-family NO-GO** | REST PR; `git ls-tree` + `git show` on `cursor/es-v6-publication-gauntlet-63a8` | open, draft, head `65f81697`, record present, arbitration reads "Computed verdict: NO-GO … at 186b16eb…", seat xAI/Grok — **confirmed as primary fact** |

**Not established by me:** raw Actions job-log text (the proxy blocks the blob host for at least one seat and I did not need it — per-step conclusions from the jobs API were sufficient, and no ruling of mine depends on log text); live harness execution on any of the nine surfaces; whether an operator waiver of D8 exists outside the repository — I searched every durable in-repo artifact and the tracker and found none, and a waiver recorded only in conversation is expressly insufficient under the project's own procedure.

---

## 7. Verdict gate trace

```
INPUT   subject = 186b16eb2c069d9e8f902579afa50e9f5460fc85
        act     = annotated tag + Release + wiki hand-off + support-point declaration

STEP 1  One-way-door check .......... tag 404, Release 404, ruleset armed
                                       -> return path OPEN; delay is cheap, tag is not
STEP 2  Integrity gates (RG-4, RG-5, RG-6, RG-9, plus RG-3 retention)
          RG-3 FAIL   RG-4 FAIL   RG-5 FAIL   RG-6 FAIL   RG-9 FAIL
        RELEASING: "Do not create a tag while one is failing or unrecorded."
                                       -> CONFORMING RELEASE FORECLOSED
STEP 3  Exception-release availability
        Exception semantics scope to the JUDGMENT gate only.
        Integrity failures are not exception-eligible.
        An exception record must be in the committed notes BEFORE tagging.
                                       -> EXCEPTION RELEASE UNAVAILABLE AT THIS SHA
STEP 4  Judgment gate (RG-8)
        GO on this SHA?               none
        Publication verdicts on SHA?  2, both NO-GO (Grok cross-family; this panel)
        RELEASING: "NO-GO ... holds a conforming publication."
                                       -> RG-8 FAIL
STEP 5  Procedural predecessors
        D8 Step-7b consult            OWED, NOT RUN
        Operator acceptance           NOT RECORDED (procedure-conformant form)
        Chat/dispatch approval        expressly not an acceptance
                                       -> BLOCKING CONDITIONS
STEP 6  Unresolved P1/P2 count
        P1: PG-01..PG-05    P2 blocking: PG-06..PG-11
                                       -> 5 P1 + 6 P2 unresolved
STEP 7  Cure analysis
        Every P1/P2 cure requires committed text.
        Procedure step 4: "Any correction creates a new candidate and
        invalidates earlier exact-commit evidence."
                                       -> CANDIDATE SUPERSEDED

COMPUTED VERDICT ................... NO-GO
```

---

## 8. Next actions

### 8A. OPERATOR ONLY — no agent may perform these

1. **Decide whether to proceed at all.** A NO-GO here is a legitimate outcome; four earlier NO-GOs in this lineage did real work. Nothing about `main`'s current state requires a tag today.
2. **Discharge or explicitly waive D8.** Either run the Step-7b cross-family manual-handoff consult at the new candidate and commit its record beside the `docs/gauntlet-runs/v4.0.0-step7b/` precedent, **or** record an explicit waiver naming scope, revisit trigger, and exit criterion. Only the operator may waive it.
3. **Record operator acceptance** in the form `OPERATOR-ACCEPTANCE-PROCEDURE.md` defines — the `operator_acceptance` object plus a consent artifact you author or echo-certify on #191. An acceptance in chat, in a commit message, or as an enum flip is not an acceptance.
4. **Author the authorization line** for the committed notes: the verdict read, the exact candidate SHA authorized, and your identity. This cannot be delegated.
5. **Perform the tag act**: disarm `protect-version-tags`, create and push the **annotated** tag on the exact new candidate, re-arm in the same sitting, verify with a seeded probe, record disarm and re-arm.
6. **Create the GitHub Release** from the committed note verbatim, non-draft, targeting the annotated tag; then run every Procedure step 10 identity assertion.
7. **Publish the wiki hand-off** and, if a fresh support point is not imminent, decide what to do about `main`'s README already advertising v6.0.0 behind 404 links (PG-18). If this hold stands, the correct remedy is a README correction — **not** a tag created to make the README true.

### 8B. An agent may prepare (all of it produces a new candidate C′)

Batch these into **one** amendment and requalify **once**; fixing them serially mints candidates needlessly.

1. Commit the rc5 arbitration and the four NO-GO run records under `docs/gauntlet-runs/`, or pin each with an **annotated** tag in a protected namespace. (PG-03)
2. Regenerate the assurance packet against C′ and bind `independent_gauntlet` / `independent_gauntlet_ref` to the on-disk verdict; or, if the packet stays sealed, add the disclosing sentence to the notes. (PG-09)
3. Write the full RELEASING evidence table into the notes with real coordinates: the five requalification run IDs at C′ with per-job conclusions, the CodeQL run, the freeze-PR check set, and a description-byte-delta row (measured 8,636; delta 0 vs v5.1.0). (PG-04)
4. Add the RG-5(c) sentence naming run `32313232046` (re-run at C′), job `contract-macos`, step 8 "Custody mission lifecycle unit tests", tests `distinct-real-file-untouched` and `distinct-both-files-tracked-separately`, and the four skipped suites. (PG-06)
5. Add per-harness verification tiers and the plain statement that no native-harness live-fire ran. (PG-10)
6. Replace "five independent panels" with the GO record's own characterization and add the independence-limits paragraph. (PG-11)
7. Repoint `.kimi-plugin/marketplace.json` to `tree/v6.0.0` and **add it to the `manifests` tuple** so the oracle covers it. (PG-07)
8. Record the wiki gap in the notes with owner, scope, revisit trigger, and exit criterion; build `docs/wiki-updates/v6.0.0/`. (PG-08)
9. Add `manifest` to both marketplace enumerations. (PG-15)
10. Rewrite the migration section: the evidence-emission side effect, the closed bypass classes, the refusal's failure shape, a rollback pointer to v5.1.0, and the macOS/Windows caveats. (PG-16, PG-19)
11. Repair the three `using-epistemic-skills/…` references and, ideally, widen the anti-phantom gate to catch bare retired paths. (PG-14)
12. Amend `CONTRIBUTING.md` to state the DCO rule actually enforced; write the 6.0.0 public-content review. (PG-12, PG-13)
13. Re-cut both rc5 pins annotated; fix `contracts/v6-assurance` → `plugins/epistemic-skills/contracts/v6-assurance`; fix the five/six miscount in `check_dco.py`. (PG-17, PG-20, PG-23)
14. **Then** re-run the five exact-commit workflows at C′ and re-run this publication gate at C′ — ideally with at least one cross-family seat, since the correlated-family limit is the one this lineage has never retired.

### 8C. Forbidden

No agent may tag, create a Release, disarm or alter `protect-version-tags`, flip a readiness enum, record an acceptance, or describe this outcome as a GO, a CONDITIONAL, or a conforming release.

---

```json
{
  "ruling_set": "ruling-set@1",
  "run": "es-v6-publication-gate-2026-08-19",
  "subject_sha": "186b16eb2c069d9e8f902579afa50e9f5460fc85",
  "proposed_tag": "v6.0.0",
  "review_mode": "publication gate (RELEASING.md step 5)",
  "seat": {
    "structure": "isolated judge over four author-dispatched gate seats plus one adversarial challenger; judge adopted no seat's word for any load-bearing fact and re-executed 27 register items from primary sources (fresh clone git objects, live unauthenticated GitHub REST, wiki clone, repo oracles run locally)",
    "authorization": "author-dispatched: the dispatcher prepared the release under review and assembled this panel; operator approved the promotion gauntlet (scope: full v6.0.0 publication). Approval to run a gate is not approval of its result, and no dispatcher framing was treated as authority.",
    "family": "single model family (Claude/Anthropic) across dispatcher, all reporting seats, and this judge — a disclosed independence LIMIT, not independence. One cross-family publication read exists on this SHA (xAI/Grok, PR #200), not produced by this panel; recorded as fact, reasoning not adopted.",
    "d8": "OWED and NOT DISCHARGED. No Step-7b cross-family consult artifact exists for v6 at any ref; the prior kimi consult was against superseded candidate 6db8c50 and does not transfer to 03e972c. The Grok publication review does not discharge D8: different subject (186b16eb vs 03e972c) and different gate (publication judgment vs BUILD acceptance consult)."
  },
  "releasing_gate_dispositions": {
    "RG-1": {
      "disposition": "PASS-QUALIFIED",
      "evidence": "Fresh clone HEAD = 186b16eb2c069d9e8f902579afa50e9f5460fc85 = live origin/main; clean tree; two-parent merge of 50f595c7 + 466b9a0c per Procedure step 4. Release-note path docs/release/RELEASE-6.0.0.md exists, names v6.0.0, supersedes v5.1.0. PR #199 scope frozen at 12 files. Qualification: the note describes rather than names the candidate; grep -c 186b16e = 0 (graded under RG-9). The note's own SHA claims (03e972c5, 546ccc8e, both pins) are TRUE and verified."
    },
    "RG-2": {
      "disposition": "FAIL",
      "evidence": "Four gaps carry no owner, bounded scope, revisit trigger, or exit criterion and none is disclosed in the notes: (1) the GO record's four owed_before_acceptance items, of which D8 consult, operator acceptance and D16-D19 echo-certification are undischarged; (2) .kimi-plugin/marketplace.json pinned to tree/v3.4.0; (3) the live wiki two majors stale with no v6 hand-off package; (4) the sealed packet shipping NOT_READY/NOT_RUN/non-empty blocking_claims inside the tag. No exception record exists in the notes."
    },
    "RG-3": {
      "disposition": "FAIL",
      "evidence": "git ls-tree HEAD docs/gauntlet-runs/ returns 7 pre-v6 directories and zero v6 records. GO and all four NO-GOs live only on unmerged branches; merge-base --is-ancestor origin/claude/es-v6-rc5-review 186b16eb = NOT ancestor. Live /rulesets cover only refs/tags/v* and ~DEFAULT_BRANCH, so the holding refs are deletable and force-pushable. RELEASE-6.0.0.md:122-124 asserts the run records live under docs/gauntlet-runs/ — false in the tagged tree. Four terminal failures and three preserved P3 dissents are the evidence at risk. No rewriting observed: each arbitration has exactly one commit naming a matching subject SHA."
    },
    "RG-4": {
      "disposition": "FAIL",
      "evidence": "Bullet 1 FAIL: .kimi-plugin/marketplace.json installs tree/v3.4.0 and is the one manifest omitted from the nine-path manifests tuple in outsource/tests/run_tests.py:318-332 (both re-read). Bullet 2 PASS: all three v6.0.0-pinned repository paths resolve via git cat-file -e at the candidate. Bullet 3 FAIL x3: live wiki (HEAD 14c7df9e, 2026-08-15) says fourteen skills / v5.0.0 install guidance / retired seats present tense / no Skill-Manifest page; three shipped package files route to using-epistemic-skills/reference/routine-fast-path.md, a path absent from the package, one of them the file README pins at blob/v6.0.0/; both marketplace descriptions say fifteen then enumerate fourteen, omitting manifest. Clean rows re-verified: 10 version surfaces read 6.0.0; 15 skills counted two ways; 8,636-byte claim matches check_description_budget.py exactly; live repo description current."
    },
    "RG-5": {
      "disposition": "FAIL",
      "evidence": "Substance green: cleanroom_ci.sh at the candidate exits 0 in my own fresh clone (54/55 steps, 0 fail, 1 named ci-context skip); five dispatch runs verified live at head_sha=186b16eb, branch claude/v6-release-requal, attempt 1; CodeQL Analyze python/actions/javascript-typescript all success; no gating job red anywhere. Gate fails on the carve-out: run 32313232046 conclusion=failure, job contract-macos failed at step 8 'Custody mission lifecycle unit tests' with steps 9-12 skipped (per-step conclusions pulled from the jobs API). Conditions (a) and (b) MET; condition (c) UNMET — git grep for each of the five run IDs across the candidate tree returns zero files and the note names no job, step, or test. RELEASING: 'Any other red, in any job of a suite dispatched at the candidate, fails this gate.'"
    },
    "RG-6": {
      "disposition": "FAIL",
      "evidence": "Mechanical limbs PASS and are affirmed: full-history secret scan green with the pinned scanner, the single .gitleaks.toml path exemption independently probed and proven narrow with provider-branded credentials still firing inside it, check_public_content.py --self-test and live both exit 0 in my clean-room (7 seeded RED controls; 37 digest-verified allowlist entries, 0 mismatches, 0 inert), license surfaces consistent. Bullet 3 FAIL: no 6.0.0 public-content review artifact at an immutable path (docs/release/ holds only 07-17, 07-21 and 5.0.0 records; the packet's public-content.json is a mechanical receipt bound to 03e972c5). Bullet 4 FAIL: CONTRIBUTING.md states an unqualified DCO rule while check_dco.py applies an unconditional merge exemption and a closed five-SHA attestation list; dco.yml triggers only on pull_request_target so no DCO check-run attaches to the candidate (13 check-runs, none named DCO); 19 no-sign-off commits landed after the gate existed."
    },
    "RG-7": {
      "disposition": "FAIL",
      "evidence": "RELEASE-6.0.0.md contains no harness section, no per-harness verification tier, no limitation row, and no cross-reference to docs/release/HARNESS-VERIFICATION-MATRIX-SUCCESSOR-2026-08-07.md; the only harness-adjacent text is KL-LIVE-ENV. README:222-233 carries a nine-row table but RG-7 names the release notes. RELEASE-5.1.0.md satisfied this row with tiers plus the explicit statement that no new live plugin-harness executions ran."
    },
    "RG-8": {
      "disposition": "FAIL",
      "evidence": "No GO exists on 186b16eb. The BUILD GO of record is bound to 03e972c5 (run-record.json subject_sha verified from origin/claude/es-v6-rc5-review) and states promotion is not authorized by it. Two publication-scoped verdicts exist against this exact SHA and both are NO-GO: the xAI/Grok cross-family review (PR #200 open/draft, head 65f81697, record at docs/gauntlet-runs/es-v6-publication-grok-2026-08-19/, verdict text read directly from the branch object) and this panel. RELEASING RG-8: NO-GO, unresolved P1/P2, or an unrun gate holds a conforming publication. Five P1 and six blocking P2 findings are unresolved."
    },
    "RG-9": {
      "disposition": "FAIL",
      "evidence": "git grep 186b16e at the candidate returns nothing; the SHA appears nowhere in its own tree, on any branch, or on the tracker. No line naming the verdict read, the exact SHA authorized, and the owner (Procedure step 7); no disarm/re-arm record. No release-note evidence table at all — grep -n '^|' yields only the nine-row known-limits table; zero workflow run IDs in the file. Publication state verified: git/ref/tags/v6.0.0 404, releases/tags/v6.0.0 404, ruleset protect-version-tags id 20090781 active on refs/tags/v* with rules [update, deletion, creation] and bypass_actors null."
    }
  },
  "findings": [
    {"id": "PG-01", "severity": "P1", "blocks_publication": true, "gate": "RG-9", "claim": "No publication identity or authorization record: the committed notes never name 186b16eb, carry no line naming verdict read / SHA authorized / owner, and record no disarm-re-arm plan.", "sources": ["RG14-F3", "RG2-02", "F1", "ADV-01"]},
    {"id": "PG-02", "severity": "P1", "blocks_publication": true, "gate": "RG-8", "claim": "No GO on the release candidate; two publication-scoped NO-GO verdicts of record against this exact SHA (xAI/Grok cross-family, and this panel).", "sources": ["F4", "ADV-08"]},
    {"id": "PG-03", "severity": "P1", "blocks_publication": true, "gate": "RG-3", "claim": "The v6 verdict lineage — four NO-GOs, one GO, three preserved dissents — is absent from the tagged tree and lives only on unprotected mutable refs, while the release note asserts the run records live under docs/gauntlet-runs/. A false statement would be made immutable.", "sources": ["RG14-F1", "RG3-01", "F6", "ADV-03"]},
    {"id": "PG-04", "severity": "P1", "blocks_publication": true, "gate": "RG-9", "claim": "No release-note gate evidence table and zero immutable evidence coordinates: no run IDs, no CodeQL row, no description-byte-delta row, no publication-identity row. Regression from RELEASE-5.1.0.md.", "sources": ["RG5-F1", "RG3-06", "F2", "ADV-02"]},
    {"id": "PG-05", "severity": "P1", "blocks_publication": true, "gate": "RG-2", "claim": "The D8 Step-7b cross-family consult is owed and not run, operator acceptance was never recorded in the procedure-conformant form, and no exception or waiver record exists. The GO's own owed_before_acceptance names both; #191's last comment predates the rc5 candidate and the GO; the packet has no operator_acceptance key.", "sources": ["RG2-03", "F4", "ADV-07"]},
    {"id": "PG-06", "severity": "P2", "blocks_publication": true, "gate": "RG-5", "claim": "A suite dispatched at the candidate is RED (contract-macos, step 8) and RG-5's dispatch-only-diagnostic carve-out fails condition (c): the release record names neither the failing step nor the tests. Substance benign; the gate fails on the record's silence. Four custody suites went unmeasured on macOS at this candidate.", "sources": ["RG5-F1", "RG14-F4", "F3", "RG2-07", "ADV-06"]},
    {"id": "PG-07", "severity": "P2", "blocks_publication": true, "gate": "RG-4", "claim": ".kimi-plugin/marketplace.json still installs tree/v3.4.0 and is the one version-bearing manifest omitted from the version oracle. Pre-existing, never recorded as an accepted gap.", "sources": ["RG14-F2"]},
    {"id": "PG-08", "severity": "P2", "blocks_publication": true, "gate": "RG-4", "claim": "The live README-linked wiki advertises fourteen skills, v5.0.0 install guidance, and two retired seats in the present tense, with no Skill-Manifest page; and no v6.0.0 package exists in docs/wiki-updates/ although the wiki hand-off is inside the intended publication act. The notes never mention the wiki.", "sources": ["RG14-F5", "RG2-10", "F7"]},
    {"id": "PG-09", "severity": "P2", "blocks_publication": true, "gate": "RG-2", "claim": "The tag would ship promotion-packet.json reading readiness=NOT_READY, independent_gauntlet=NOT_RUN, blocking_claims=['CLM-INDEPENDENT-GAUNTLET'] (P1 UNPROVED), with the discharging artifact outside the tag and no disclosure in the notes. Structurally un-flippable at this candidate because the validator requires the verdict on disk.", "sources": ["F5", "ADV-03", "HON-12"]},
    {"id": "PG-10", "severity": "P2", "blocks_publication": true, "gate": "RG-7", "claim": "No per-harness verification tier or limitation appears in the release notes.", "sources": ["RG7-05", "F8"]},
    {"id": "PG-11", "severity": "P2", "blocks_publication": true, "gate": "RG-2", "claim": "'Reviewed by five independent panels' is denied by the GO record's own seat_structure ('an independence LIMIT, not independence'; single family throughout), and the notes record no independence limits at all — a column v5.1.0 filled honestly. Each panel also judged a different candidate; only panel 5 reviewed 03e972c.", "sources": ["RG2-04", "F12"]},
    {"id": "PG-12", "severity": "P3", "blocks_publication": false, "gate": "RG-6", "claim": "No 6.0.0 public-content review with findings and dispositions exists at an immutable path; the packet's evidence is a mechanical receipt bound to the BUILD-freeze candidate.", "sources": ["RG6-F6"]},
    {"id": "PG-13", "severity": "P3", "blocks_publication": false, "gate": "RG-6", "claim": "Provenance surfaces are inaccurate: CONTRIBUTING.md states an unqualified DCO rule the enforced checker does not apply; dco.yml certifies PR-head objects that squash-merge discards so no DCO check-run attaches to any landed commit; 19 no-sign-off commits landed after the gate existed.", "sources": ["RG6-F5", "RG6-F7", "RG2-09"]},
    {"id": "PG-14", "severity": "P3", "blocks_publication": false, "gate": "RG-4", "claim": "Three shipped package files route readers to using-epistemic-skills/reference/routine-fast-path.md, a path absent from the package, including the file README pins at blob/v6.0.0/. The anti-phantom gate is structurally blind to the bare-path form and exits 0.", "sources": ["ADV-04"]},
    {"id": "PG-15", "severity": "P3", "blocks_publication": false, "gate": "RG-4", "claim": "Both marketplace 'full collection' descriptions enumerate 14 of the 15 packaged skills, omitting manifest — the seat carrying this release's headline security fix. The count linter validates the spelled numeral, never the enumeration.", "sources": ["RG14-F6"]},
    {"id": "PG-16", "severity": "P3", "blocks_publication": false, "gate": "RG-4", "claim": "The migration section's 'one behavioral change to expect' is false: nine SKILL.md files newly instruct appending to runs/ledger.jsonl after every engagement (5/15 at v5.1.0 -> 14/15 at the candidate). The section also lacks enumeration of the closed bypasses, the refusal's failure shape, and a rollback pointer.", "sources": ["ADV-05", "HON-08"]},
    {"id": "PG-17", "severity": "P3", "blocks_publication": false, "gate": "RG-3", "claim": "The two rc5 pin tags the release note relies on are lightweight and sit in an unprotected namespace, a discipline regression from the annotated rc2 pins cut one day earlier. Mitigated: both SHAs are ancestors of the candidate.", "sources": ["HON-11", "F10"]},
    {"id": "PG-18", "severity": "P3", "blocks_publication": false, "gate": "RG-4", "claim": "Live main already advertises v6.0.0 as the current immutable support point behind links and install commands that 404 today. A real defect, and a source of pressure to publish that is not evidence for publishing.", "sources": ["F9"]},
    {"id": "PG-19", "severity": "P3", "blocks_publication": false, "gate": "RG-7", "claim": "The support-point promise over-reaches on platform: macOS custody lifecycle is red/unmeasured at the candidate with no README row naming macOS; a Windows install recipe ships while KL-WINDOWS discloses no native requalification; KL-GUARD-LEXICAL's residual symlinked-parent false-allow is disclosed in the limits table but not adjacent to 'this is the reason to upgrade'.", "sources": ["F11"]},
    {"id": "PG-20", "severity": "P4", "blocks_publication": false, "gate": "RG-4", "claim": "The note cites contracts/v6-assurance, a path that does not exist (real path plugins/epistemic-skills/contracts/v6-assurance); and 'twenty-six class claims' is accurate for the class family while the matrix holds 72 claims.", "sources": ["HON-13"]},
    {"id": "PG-21", "severity": "P4", "blocks_publication": false, "gate": "RG-3", "claim": "check_pin_tags.py exits 0 while its registry names only the superseded rc2 pins. DOWNGRADED by this panel: the registry comment documents a deliberate one-freeze registration lag with a stated rationale (kimi ruling S5 / CL-3), so this is a documented discipline, not an unrecorded gap; the rc5 pins resolve correctly on origin.", "sources": ["RG14-F7"]},
    {"id": "PG-22", "severity": "P4", "blocks_publication": false, "gate": "RG-6", "claim": "The DCO merge-commit exemption's disclosed risk is realized: 2 of 24 reachable merges diverge from the mechanical merge of their parents, one authoring 69 insertions across 19 files with zero conflict markers, so the note's framing of the gap as 'a conflict resolution' does not cover it.", "sources": ["RG6-F8"]},
    {"id": "PG-23", "severity": "P4", "blocks_publication": false, "gate": "RG-6", "claim": "check_dco.py contains a self-contradictory count ('these five' / 'exactly these six' against len(ATTESTED_UNSIGNED)==5) inside the digest-inventoried file defining a security-relevant exemption, and its github_commits() pagination is a latent fail-open above 250 commits, undisclosed.", "sources": ["RG2-09"]},
    {"id": "PG-24", "severity": "P4", "blocks_publication": false, "gate": "RG-6", "claim": "Two tracked files embed build-host scratchpad absolute paths carrying session UUIDs, a class the public-content pattern set cannot see. No credential, private host, or personal data exposed.", "sources": ["RG6-F9"]}
  ],
  "computed_verdict": "NO-GO",
  "verdict_binding": {
    "run_id": "es-v6-publication-gate-2026-08-19",
    "subject_sha": "186b16eb2c069d9e8f902579afa50e9f5460fc85",
    "verdict_path": "docs/release/gauntlet/es-v6-publication-gate-2026-08-19/arbitration.md",
    "statements": [
      "A GO authorizes no act by itself; this is a NO-GO and it likewise commands nothing. A verdict is an artifact, not an act.",
      "The annotated v6.0.0 tag, the GitHub Release, the wiki hand-off package, any ruleset or settings change, and the SUPPORT-POINT declaration remain operator acts under RELEASING.md, performed in a separate PROMOTION_RUN with its own consent. No agent may perform any of them.",
      "This verdict binds to subject_sha 186b16eb2c069d9e8f902579afa50e9f5460fc85 and to no other string. It does not transfer to any successor candidate; a corrected candidate requires a fresh publication gate.",
      "The D8 Step-7b cross-family consult is OWED and NOT DISCHARGED at these coordinates. The prior kimi consult was against superseded candidate 6db8c50 and does not transfer to 03e972c. The xAI/Grok publication review at PR #200 does not discharge it: different subject and different gate.",
      "Operator acceptance under docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md has NOT been recorded. The packet carries no operator_acceptance object and issue #191's last comment (2026-08-18T20:41:38Z) predates both the rc5 candidate and the GO. An acceptance recorded as a chat message, a dispatch-prompt assertion, a commit message, or an enum flip is not an acceptance under that procedure.",
      "Publication may NOT proceed before the D8 consult (or an explicit operator waiver of it) and a procedure-conformant operator acceptance. Both are named here as blocking conditions.",
      "The operator's end-to-end approval of the promotion gauntlet authorized this review, not its result, and cannot substitute for either owed act. It would also be insufficient on its own: RELEASING.md scopes exception releases to the independent judgment gate only, and RG-3, RG-4, RG-5, RG-6 and RG-9 are integrity gates that must not be tagged while failing or unrecorded.",
      "Candidate 186b16eb2c069d9e8f902579afa50e9f5460fc85 is SUPERSEDED. Every blocking cure requires committed text, and Procedure step 4 provides that any correction creates a new candidate and invalidates earlier exact-commit evidence — including requalification runs 32313229574, 32313232046, 32313238605, 32313240639 and 32313248657.",
      "At the time of this verdict no v6.0.0 tag and no v6.0.0 Release exist, and protect-version-tags is armed with no bypass actors. The one-way door is closed and the return path is open at zero cost.",
      "Nothing in this verdict impugns the engineering. The deterministic suite passes in a fresh clone, every required job at the candidate is green including CodeQL, the assurance seal binds, and every v6.0.0-pinned path resolves. What is not ready is the release record and two procedural acts."
    ]
  },
  "rulings": [
    {"id": "RG-1", "ruling": "Candidate identity and scope satisfied as written; the note describes rather than names the candidate, which is graded under RG-9.", "status": "PASS-QUALIFIED"},
    {"id": "RG-2", "ruling": "Four accepted gaps ship with no owner, bounded scope, revisit trigger, or exit criterion, and no exception record exists.", "status": "FAIL"},
    {"id": "RG-3", "ruling": "Four terminal failures, one GO, and three preserved dissents sit on deletable refs outside the tagged tree, under a release-note statement that says otherwise.", "status": "FAIL"},
    {"id": "RG-4", "ruling": "In-tree bump and pinned paths are clean; bullet 1 fails on the kimi marketplace v3.4.0 pin and bullet 3 fails on the wiki, the retired-name routing, and the marketplace enumeration.", "status": "FAIL"},
    {"id": "RG-5", "ruling": "All required jobs green and the deterministic suite reproduced in a fresh clone, but the dispatch-only-diagnostic carve-out fails condition (c), so the gate's own fallback applies.", "status": "FAIL"},
    {"id": "RG-6", "ruling": "Mechanical security limbs pass and are the strongest evidence in this release; the public-content review record and the provenance-surface accuracy limbs fail.", "status": "FAIL"},
    {"id": "RG-7", "ruling": "No per-harness verification tier or limitation in the release notes.", "status": "FAIL"},
    {"id": "RG-8", "ruling": "No GO on this SHA; two publication-scoped NO-GO verdicts of record against it; five P1 and six blocking P2 findings unresolved.", "status": "FAIL"},
    {"id": "RG-9", "ruling": "No publication identity record, no authorization line, no evidence table; the candidate SHA appears nowhere in its own tree.", "status": "FAIL"},
    {"id": "PG-01", "priority": "P1", "status": "OPEN", "ruling": "SUSTAINED and blocking. Cure requires committed text and therefore a new candidate."},
    {"id": "PG-02", "priority": "P1", "status": "OPEN", "ruling": "SUSTAINED and blocking. RG-8 holds a conforming publication on NO-GO alone."},
    {"id": "PG-03", "priority": "P1", "status": "OPEN", "ruling": "SUSTAINED and blocking. The decisive finding: it converts an untrue evidence-location statement into an immutable one and leaves four NO-GO verdicts on deletable refs."},
    {"id": "PG-04", "priority": "P1", "status": "OPEN", "ruling": "SUSTAINED and blocking. RELEASING is explicit that remembered work is not a MET row."},
    {"id": "PG-05", "priority": "P1", "status": "OPEN", "ruling": "SUSTAINED and blocking. Operator approval can cure by explicit waiver plus recorded acceptance, but not informally and not retroactively; see section 5A."},
    {"id": "PG-06", "priority": "P2", "status": "OPEN", "ruling": "SUSTAINED and blocking. Substance benign, record silent; the carve-out is conjunctive by design."},
    {"id": "PG-07", "priority": "P2", "status": "OPEN", "ruling": "SUSTAINED and blocking. Pre-existing since v3.4.0 and not a regression, but never recorded as an accepted gap; honest recording or repair is the discharge."},
    {"id": "PG-08", "priority": "P2", "status": "OPEN", "ruling": "SUSTAINED and blocking, at P2 not P1 — the wiki is mutable and repairable without a new version. Dissent preserved that it is a P1 RG-4 failure. The record of the gap still needs a commit."},
    {"id": "PG-09", "priority": "P2", "status": "OPEN", "ruling": "SUSTAINED and blocking. Validator-green is the packet correctly reporting non-readiness and must never be cited as support for publication."},
    {"id": "PG-10", "priority": "P2", "status": "OPEN", "ruling": "SUSTAINED and blocking. Discharged in the same edit that writes the evidence table."},
    {"id": "PG-11", "priority": "P2", "status": "OPEN", "ruling": "SUSTAINED and blocking. One sentence of cure; an affirmative overclaim at an immutable coordinate until then."},
    {"id": "PG-12", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. Ride the same amendment."},
    {"id": "PG-13", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. Direction of the CONTRIBUTING.md mismatch is safe, but it would ship as published contributor law."},
    {"id": "PG-14", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. Pre-existing since v5.0.0; the gate that should catch it is structurally blind, which is itself worth fixing."},
    {"id": "PG-15", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. One description string."},
    {"id": "PG-16", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. The note contradicts itself rather than conceals, but the migration section is the surface an upgrader reads."},
    {"id": "PG-17", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. The 'never lightweight' clause is scoped to support points; pins are not support points. Re-cut annotated anyway."},
    {"id": "PG-18", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. On a hold the remedy is a README correction on main, never a tag created to make the README true."},
    {"id": "PG-19", "priority": "P3", "status": "OPEN", "ruling": "SUSTAINED, not independently blocking. Disclosure-adjacency and completeness, not concealment."},
    {"id": "PG-20", "priority": "P4", "status": "OPEN", "ruling": "SUSTAINED. Cheap to fix in the same amendment."},
    {"id": "PG-21", "priority": "P4", "status": "OPEN", "ruling": "SUSTAINED at reduced significance. DOWNGRADED by this panel after reading the registry's documented one-freeze lag rule; the reporting seat's fact stands, its framing as an unrecorded gap does not."},
    {"id": "PG-22", "priority": "P4", "status": "OPEN", "ruling": "SUSTAINED. Records the note's framing of the gap as understating the class."},
    {"id": "PG-23", "priority": "P4", "status": "OPEN", "ruling": "SUSTAINED. Both defects sit inside the oracle that defines a security-relevant exemption."},
    {"id": "PG-24", "priority": "P4", "status": "OPEN", "ruling": "SUSTAINED. Minimal impact; recorded for coverage completeness of the public-content pattern set."},
    {"id": "ADV-01", "priority": "P1", "status": "SUSTAINED", "ruling": "Independently re-executed: grep -c 186b16eb in the note = 0; no authorization line; the only GO names 03e972c. Adopted as PG-01."},
    {"id": "ADV-02", "priority": "P1", "status": "SUSTAINED", "ruling": "Independently re-executed: the note's only table is the known-limits table; zero run IDs. Adopted as PG-04."},
    {"id": "ADV-03", "priority": "P1", "status": "SUSTAINED", "ruling": "Packet fields parsed directly; gauntlet-runs listing confirmed. Split into PG-03 (retention) and PG-09 (packet). Severity held at P2 for the packet limb since the note honestly retires KL-MAIN-137 and the packet self-labels as a BUILD freeze."},
    {"id": "ADV-04", "priority": "P3", "status": "SUSTAINED", "ruling": "Three references verified, the target directory confirmed absent, and the anti-phantom gate confirmed green. I did not re-plant the four probes; the finding stands on the verified references alone. Adopted as PG-14 at P3, not blocking on its own."},
    {"id": "ADV-05", "priority": "P3", "status": "SUSTAINED", "ruling": "Per-file diff against v5.1.0 reproduced: 5/15 -> 14/15 SKILL.md carrying Evidence emission, nine newly. The migration statement is false as written. Adopted as PG-16."},
    {"id": "ADV-06", "priority": "P2", "status": "SUSTAINED", "ruling": "Run, job and step conclusions re-fetched. Adopted as PG-06. Condition (c) is the sole failing limb."},
    {"id": "ADV-07", "priority": "P1", "status": "SUSTAINED AND ELEVATED", "ruling": "The challenger graded it non-blocking on the ground that RG-1..RG-9 do not name D8. I elevate to P1 blocking: the acceptance procedure is the project's own written sequence, its step 5 forecloses promotion from steps 1-4, RG-2 independently requires undisclosed gaps to carry an owner and exit criterion, and the GO record itself declares both owed. Adopted as PG-05."},
    {"id": "ADV-08", "priority": "P1", "status": "SUSTAINED", "ruling": "PR #200 verified live and the arbitration text read directly from the branch object. A cross-family publication NO-GO of record stands against this exact SHA. Adopted as PG-02. Recorded as a primary fact; none of its reasoning adopted."},
    {"id": "REF-01", "priority": "P4", "status": "AFFIRMED", "ruling": "The dead-immutable-link attack is refuted. I independently resolved all three v6.0.0-pinned repository paths at the candidate; every one exists. This is the failure mode a blind bump usually produces and it did not happen."},
    {"id": "REF-02", "priority": "P4", "status": "AFFIRMED", "ruling": "The assurance seal genuinely binds. Two seats independently established it — one by recomputing all 141 digests and the tree hash, one by tampering an inventoried source and observing the validator flip from exit 0 to 'R5 DIGEST MISMATCH'. I affirm, with the challenger's qualifier preserved: none of PR #199's 12 changed files is inventoried, so the seal proves nothing about the release delta itself."},
    {"id": "REF-03", "priority": "P4", "status": "AFFIRMED", "ruling": "CodeQL did run green on the exact candidate — I re-verified all three Analyze matrices in the check-run census. The dispatcher's five-run list omitted it; the omission is not a defect in the evidence."},
    {"id": "REF-04", "priority": "P4", "status": "AFFIRMED", "ruling": "No fabrication in the run list. All five runs verified real, at the exact SHA, dispatch event, attempt 1. The dispatcher itself directed verification of per-job conclusions rather than concealing the red."},
    {"id": "REF-05", "priority": "P4", "status": "AFFIRMED", "ruling": "The package is not broken for users at pinned paths. Fifteen skills each with a SKILL.md; README-referenced paths resolve; the OpenAI bundle builds; the 8,636-byte claim reproduces exactly."},
    {"id": "REF-06", "priority": "P4", "status": "AFFIRMED", "ruling": "The tag-protection control is real and armed exactly as RELEASING.md describes, with no bypass actors — re-read live by this panel. Nothing has been published."},
    {"id": "REF-07", "priority": "P4", "status": "AFFIRMED", "ruling": "The secret-scan exemption and the public-content gate are not shaped around this candidate. Both oracles exit 0 in my own clean-room; the exemption was proven narrow by independent probing beyond what CI does."},
    {"id": "REF-08", "priority": "P4", "status": "AFFIRMED", "ruling": "The custody fixes are uniformly fail-closed and 'stricter custody refusals' accurately characterizes the contract. The undisclosed behavior change lies elsewhere and is carried as PG-16."},
    {"id": "REF-09", "priority": "P4", "status": "AFFIRMED", "ruling": "User-facing surfaces carry no moving-branch links and no live-state prose; all repository links are v6.0.0-pinned. The genuine immutability traps are inside the sealed packet and are carried as PG-09."}
  ]
}
```