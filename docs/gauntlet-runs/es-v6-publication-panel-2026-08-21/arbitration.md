<!-- Transcribed record. See TRANSCRIPTION.md in this directory for provenance
     and for the structural limit that bounds what this verdict can establish. -->

# ARBITRATION — v6.0.0 PUBLICATION GATE

**Subject:** `48009fef938bfa989fb797380080824b050f3bb4` (= `origin/main`; merge of PR #206; parents `190e57f7`, `e2610ef1`)
**Seat:** isolated judge, did not author the candidate, did not produce the seat reports
**Date:** 2026-08-21

## VERDICT: **NO-GO**

Not CONDITIONAL. The distinction is load-bearing and I want it on the record: CONDITIONAL would imply a set of conditions **this SHA** could come to satisfy. None exists. `RELEASING.md` Procedure step 7 states "No commit may be made between the candidate and the tag. If one is required, the candidate is superseded and steps 4-6 re-run from the top." Every cure identified below requires a commit. Therefore this candidate is not conditionally publishable — it is terminally superseded the moment anyone acts on any finding. NO-GO is the honest verdict shape.

Three independent grounds, any one sufficient:

1. **The candidate's own release record grades three of nine gates unmet** — RG-2 `UNMET`, RG-8 `NO-GO ×2`, RG-9 `UNMET`. I did not have to find this; the candidate says it.
2. **Two P2 findings survived adversarial refutation**, and RG-8's own text is dispositive: "A conforming release requires `GO` with no unresolved P1 or P2."
3. **The candidate's own pre-authorization does not fire.** Of its four firing conditions I verified condition 1 satisfied and conditions 2, 3, and 4 unsatisfied. By its own terms: "If any condition fails, this authorization does not fire, and no tag may be created."

No `v6.0.0` tag and no `v6.0.0` Release exist (9 releases, newest `v5.1.0`). Nothing has been published; this is a live pre-publication hold, not a post-hoc erratum.

---

## 1. Facts I re-executed myself

I adopted no seat's word on anything load-bearing. Eleven checks, all from primary sources:

| # | Fact | Method | Result |
|---|---|---|---|
| 1 | Candidate identity | `git rev-list --parents`, `git ls-remote` | `48009fef` = `origin/main`, merge of #206, parents `190e57f7`/`e2610ef1`. **No `v6.0.0` tag.** |
| 2 | RG1-01 scope claim | `git diff --stat 92b3ca6c 48009fef` | **10 files, +690/−124, 10 commits.** Note claims "the **only** change… is this table." **FALSE.** Scoped to `docs/release/`: 2 files, not 1. |
| 3 | RG1-01 parentage claim | `git rev-parse 48009fef^1 ^2` | Parents are `190e57f7`/`e2610ef1`. `92b3ca6c` is an **ancestor, not a parent**. **FALSE as written.** |
| 4 | RG1-02 third verdict | `ls`, `git ls-remote` | `es-v6-publication-openai-2026-08-20` **absent from candidate tree**; exists only at `refs/heads/review/v6.0.0-publication-gate-openai-2026-08-20` (`ac0a91e1dc51`), a mutable branch. Read its summary: **NO-GO** on `d0165bd0`, rulings OAI-P1-01/02/03, OAI-P2-01. Lineage table carries **7** rows. |
| 5 | RG-5 substance | GitHub API `actions/runs?head_sha=48009fef` | **9 runs at the exact candidate.** All five gating workflows dispatched: `epistemic-flexibility` 32430457960 ✓, `release-security` 32430459879 ✓, `openai-bundles` 32430452518 ✓, `commission-watch-contract` 32430465696 ✓, `mission-custody-contract` 32430450479 (run-level red). |
| 6 | **CodeQL — resolving the seat's UNVERIFIED** | API `commits/48009fef/check-runs` | **`Analyze (python)`, `Analyze (javascript-typescript)`, `Analyze (actions)` — all success at the exact candidate.** No workflow file; runs via GitHub default setup. **RG-5's CodeQL limb is satisfied.** Resolved in the candidate's favor. |
| 7 | Red-job carve-out | API `runs/32430450479/jobs` | `contract` **success**; `contract-macos` **failure at step 8** "Custody mission lifecycle unit tests". Matches the disclosed carve-out shape. |
| 8 | **D20's actual effect** | packet diff `92b3ca6c`→`48009fef` | `independent_gauntlet`: `NOT_RUN` → **`GO`**; `blocking_claims`: `["CLM-INDEPENDENT-GAUNTLET"]` → **`[]`**. `readiness` remains `NOT_READY`. |
| 9 | Pre-authorization authorship | `git log -1 -- docs/release/PRE-AUTHORIZATION-6.0.0.md` | Committed at `e2610ef1` by **`Claude <noreply@anthropic.com>`**, msg "adopt … by operator direction (D23)". Step 7 requires "**the owner** commits the pre-authorization." Names no SHA (compliant on that limb). |
| 10 | Firing condition 4 | `grep operator_acceptance` packet; `OPERATOR-ACCEPTANCE-PROCEDURE.md:100` | `operator_acceptance` object **ABSENT**. Procedure excludes "acceptance recorded any other way (chat message, commit message, enum…)". |
| 11 | RG4-01 refutation spot-check | `git cat-file -e v5.0.0:<path>` | `helix/SKILL.md`, `using-epistemic-skills/SKILL.md` **absent at v5.0.0** (14 skills there). The 29 links are **already dead**. Refutation upheld. |

Also confirmed from primary source: `RELEASING.md` step 9 ("Use the committed release-note file **verbatim** as the body"), step 4 ("Any correction creates a new candidate and **invalidates earlier exact-commit evidence**"), and line 238 ("this repository is pushed with the **same credential automation runs under**").

---

## 2. Gate classes — and what an owner exception can actually carry

From `RELEASING.md` lines 43-73, read directly:

- **Integrity gates** (line 47): "version/link alignment, deterministic checks, CodeQL, provenance checks, full-history secret scan, public-content review, and **publication identity assertions**" → **RG-4, RG-5, RG-6, RG-9**. "Do not create a tag while one is failing **or unrecorded**."
- **Harness-evidence gate** → **RG-7**.
- **Independent judgment gate** → **RG-8**, and RG-8 alone.
- **Unclassed by that section** → RG-1, RG-2, RG-3.

**The decisive reading.** The exception mechanism is defined *only* for the judgment gate: "**Exception release:** the owner authorizes publication despite an explicitly named unmet **judgment** gate." There is no defined mechanism by which an owner exception carries an integrity gate, and none by which it carries the unclassed gates either. So:

- **RG-8 (NO-GO) — CARRYABLE.** An owner exception can publish over it. Doing so makes this an exception release; step 6 forbids describing it as a GO or conforming release, and RG-8 requires it stay `WAIVED`/`UNMET`, "never `MET`."
- **RG-1, RG-2, RG-3, RG-5-as-recorded, RG-9 — NOT CARRYABLE.** Integrity or unclassed; no exception mechanism reaches them.

**Consequence:** even a maximally permissive owner exception does not reach publication at this SHA. The judgment gate is the only door an exception opens, and four other doors are shut. This is the single most important structural finding in the arbitration.

---

## 3. Per-gate disposition — RG-1 … RG-9 at `48009fef`

| Gate | Class | Note's grade | **My disposition** | Basis |
|---|---|---|---|---|
| **RG-1** candidate identity & scope | unclassed → not carryable | met | **FAIL** | Bullets 1 and 3 hold (`main` = `origin/main`; path and version named). But the row's scope account is materially false (fact 2/3), and step 9 publishes it verbatim. A row recorded falsely is not "recorded against the exact candidate." |
| **RG-2** decisions & risk acceptance | unclassed → not carryable | **UNMET** | **FAIL** (self-declared) | `operator_acceptance` absent (fact 10); D8 consult owed. Aggravated by RG4-05: the post-tag install-ref obligation has no owner/trigger/exit anywhere. |
| **RG-3** evidence retention | unclassed → not carryable | met, "PG-03 now closed" | **FAIL** | The 8th and most load-bearing verdict lives solely on a mutable branch (fact 4). PG-03 reproduces exactly. Gate requires dissent "at immutable coordinates." |
| **RG-4** version & link alignment | **integrity** | met | **PASS with limits** | Bullet 2 passes: no rewritten version-pinned URL in the candidate tree. RG4-01 refuted to P4. Limits owed in the row: RG4-02, -03, -04, -06 (below). |
| **RG-5** deterministic & static-analysis | **integrity** | "met at `92b3ca6c`, the parent" | **SUBSTANCE MET / RECORD FAILS** | I verified all five workflows **and all three CodeQL matrices** green at the exact candidate (facts 5-7). But the committed row names superseded `323256xxxxx` runs at an ancestor, and step 4 invalidates them. The facts are good; the record is not. Curable — but only by a commit, which supersedes. |
| **RG-6** security, public content, provenance | **integrity** | met | **PASS (recorded)** | `full-history-secret-scan` success at candidate. *Limit: I did not re-execute the public-content self-test or the planted-secret control.* |
| **RG-7** supported harness evidence | harness-evidence | met via tiers | **PASS** | Tiers explicit; no live-fire, disclosed as such rather than implied. Honest. |
| **RG-8** independent publication judgment | **judgment** | NO-GO ×2 | **FAIL — NO-GO ×3** | Count is wrong: three publication reviews, all NO-GO. No GO exists at `48009fef`. **Carryable by owner exception only.** |
| **RG-9** publication identity plan | **integrity** | **UNMET** | **FAIL** (self-declared, plus one more) | Authorization line absent. **Additionally:** step 7 requires *the owner* to commit the pre-authorization; it was committed by `Claude` under D23 (fact 9). |

**Score: 3 PASS, 1 PASS-with-limits, 5 FAIL** — of which only RG-8 is exception-carryable.

---

## 4. Ruling on the two authority shortcuts

This is the question the lineage most wants answered yes. I weighed it accordingly and the answer is **no** for both — though not for the reason either seat anticipated, and with real credit given where earned.

### D20 (ratification of `CLM-INDEPENDENT-GAUNTLET`) — **NOT ADEQUATE for the use it is put to**

The claim's `closure_path` reserves closure to an **operator-dispatched** independent Gauntlet. D20 substitutes operator **ratification** of an author-dispatched verdict.

**Why the substitution does not hold.** Dispatch is not ceremony — it controls **selection**: who is asked, what they are asked, on which packet, and above all *whether an unfavorable verdict ever surfaces*. Ratification operates only on the verdicts the implementing lineage chose to present. The rc5 seat's freshness, isolation, and non-authorship satisfy the claim's **oracle**; none of them recovers the **selection** property, and selection is exactly what the dispatch limb protects. The record concedes this in terms and invites the reader to decide — I decide it is not sufficient.

**Aggravating.** The rc5 verdict is scoped **"GO (BUILD freeze only)"** on subject `03e972c5`, now superseded. It was used to flip `independent_gauntlet` to `GO` and **empty `blocking_claims`** (fact 8) — a broader effect than its own scope supports.

**Materially aggravating, and this is my finding rather than any seat's:** that flip occurred **inside the ten-commit window the release note describes as containing "only this table."** So RG1-01 is not cosmetic staleness. The false scope statement conceals — unintentionally, but in the immutable body — the single most consequential state change in the window: a blocking claim emptied on the strength of an authority shortcut. That raises RG1-01's weight above the seat's own framing.

**Credit where due.** `readiness` stayed `NOT_READY`. The `closure_note` records "seat was author-dispatched" rather than laundering it. D22 explicitly denies D20 any publication-authorizing role. A revisit trigger exists. This is honest work, and it is why D20 is *inadequate* rather than *deceptive*.

**Ruling.** Adequate as a disclosed, bounded operator judgment about the assurance contract — **if** the operator's instruction is genuine. **Not** adequate as independent evidence for any gate whose purpose is independence from the lineage. It must not be counted toward RG-8, and the `blocking_claims` flip should be re-examined against the rc5 verdict's actual BUILD-freeze scope.

### D23 (standing session authority) — **NOT ADEQUATE, and structurally uncurable by commit**

**The self-defeating limb — the strongest thing I found.** The pre-authorization *adopted under D23* contains **firing condition 4**, requiring operator acceptance "plus a consent artifact the owner authored or echo-certified," and stating: "**An acceptance in chat, in a commit message, or as an enum flip is not an acceptance.**" D23 is precisely an acceptance in chat. So:

- If D23's amendment **reaches** condition 4, the instrument amends away its own precondition — the sequence is circular and authorizes nothing.
- If it **does not reach** condition 4, condition 4 is unsatisfied — and I verified `operator_acceptance` is absent from the packet (fact 10), so this branch is not hypothetical.

**Both branches block.** There is no reading on which the authorization fires.

**The structural point that matters most.** `RELEASING.md` line 238 concedes the repository "is pushed with the **same credential automation runs under**." I confirmed the operator's account authors non-merge commits in this very lineage (`d0165bd`, `92b3ca6`). Under a shared credential, **commit authorship cannot establish operator authorship at all.** Therefore D23's stated provenance limit is *not* curable by "the operator commits it under their own account" — such a commit would be byte-indistinguishable from an agent commit. This cuts both ways and I want both recorded:

- Against the lineage: no committed artifact, however solemn, can carry operator authority here. Paper authority in this repository is worth less than these documents assume.
- For the design: the lineage saw this and built the one control that *does* bind — `protect-version-tags` with `creation` and **no bypass actors**, disarmable only by a repository-settings change. D23 concedes it cannot amend this. That control is real, and it holds. **The entire residual integrity of this release rests on it.**

**Ruling.** **Not adequate** to satisfy RG-2 or RG-9. D23 may stand as a disclosed operator preference governing agent behavior *in session*; it may **not** stand as the acceptance artifact condition 4 requires, nor as the owner's commit under step 7. Its own honesty about its limits is the reason it fails cleanly rather than dangerously.

**On the pre-authorization's condition 2 — and on my own seat.** Condition 2 requires "an **operator-dispatched** independent publication gate returns GO." I was dispatched by the implementing lineage. **Even a GO from me would not have satisfied it.** My seat can block; it cannot clear. I state this asymmetry plainly because it is the most important limit on what this document is worth.

---

## 5. Findings table

| ID | Sev | Gates | Class | Blocks | Disposition |
|---|---|---|---|---|---|
| **RG1-01** | **P2** | RG-1, RG-5, RG-8 | **integrity** | **YES** | **UPHELD**, weight *increased*. Scope statement and parentage claim both false (facts 2, 3); step 9 publishes verbatim. Refuter's gate correction to RG-1/RG-5/RG-8 (not RG-4) is right. **My addition:** the denied delta contains the `blocking_claims` emptying and `RELEASING.md` itself (+58) — the governing gate changed inside the window the note calls "only this table." |
| **RG1-02** | **P2** | RG-1, RG-3, RG-8 | **integrity/unclassed** | **YES** | **UPHELD.** Three publication NO-GOs, not two. The 8th verdict — the only operator-dispatched cross-family one — is on a mutable branch. PG-03 reproduces exactly while the note declares it closed. |
| RG-2 unmet | **P1-equiv** | RG-2 | unclassed | **YES** | Self-declared. `operator_acceptance` absent; D8 consult owed. Not exception-carryable. |
| RG-9 unmet | **P1-equiv** | RG-9 | **integrity** | **YES** | Self-declared, **plus** the owner-commit defect at fact 9. |
| RG-8 NO-GO | **P1-equiv** | RG-8 | **judgment** | **YES** | The only blocker an owner exception can carry. |
| **RG4-01** | **P4** | RG-4 | integrity | no | **REFUTED — refutation upheld** on my own check (fact 11). Mints 0 new dead links; repairs 8. Residual kernel preserved below. |
| RG1-03 | P3 | RG-1 | — | no | Dispatch packet off-tree; its step-0 tripwire destroyed by SHA substitution. Corroborates RG1-01. |
| RG4-02 | P3 | RG-4 | integrity | no | **Independently confirmed:** selector matches **0** lines; `router` appears **0** times in README. Check dead since v5.0.0. Surface currently correct → durability defect. Belongs in RG-4's **limits** column, not "met". |
| RG4-03 | P3 | RG-4 | integrity | no | PG-15 fixed in content, no oracle added. Recurrence silent. |
| RG4-04 | P3 | RG-4 | integrity | no | 26 pre-existing v5.0.0-pinned dead URLs; outside bullet 2's "rewritten" scope. |
| RG4-05 | P3 | RG-4, RG-2 | integrity | no | Post-tag install-ref obligation has no owner/trigger/exit. **Should be an RG-2 accepted gap before tagging.** |
| RG4-06 | P4 | RG-4 | integrity | no | 4 of 15 skills unnamed in manifest descriptions; pre-existing. |

---

## 6. Preserved dissents

Recorded, not resolved away:

1. **RG-4 seat vs. refuter on RG4-01.** The seat graded the blind bump **P2/blocking**; the refuter reduced it to **P4**. I side with the refuter on my own evidence — but the seat's kernel survives and I preserve it: `apply_v6_updates.py` has **no path-existence check and no tag-existence guard**, so it carries 29 pre-existing 404s forward under a new tag instead of surfacing them, and **3 of the 10 affected pages** fall outside its own retired-seat advisory, so nothing in the package names them. The seat's stated de-escalation condition was in fact already satisfied by a committed RG-2 record the seat did not engage. The seat's `x9` breakdown was arithmetically wrong (6 paths / 14 occurrences); headline numbers were right.
2. **RG-5 seat's dissent that the substance is sound.** Upheld and independently reproduced. This is why RG-5 is a *record* failure, not an artifact failure — and why the cure is cheap in work and expensive only in candidate identity.
3. **The RG-1/RG-4 seat expressly declined to rule D20/D23** ("that judgment belongs to the RG-2/RG-8/RG-9 seats; I record it, I do not rule it"). That deferral was correct seat discipline. I have now ruled it in §4; the seat's abstention is preserved as the reason the question reached me undecided.
4. **Seat UNVERIFIED items I resolved.** CodeQL — resolved **in the candidate's favor** (fact 6): all three matrices green at the exact candidate. The seat was right not to assert it absent.
5. **Items I could not resolve and do not assert either way:** operator authorship of D20/D23 beyond the lineage's transcription (structurally unresolvable — §4); the future annotated tag object's contents (cannot exist pre-tag by design); ruleset protection on the two lightweight `pin/` tags; live harness install behavior; the public-content self-test and planted-secret control, which I did not re-execute.

---

## 7. Independence statement

Stated plainly, because this document is worth exactly what these limits allow:

- **I share a model family with the candidate's authors.** Every substantive commit in the disputed delta is authored by `Claude <noreply@anthropic.com>`; I am Claude. My verdict carries the same family-correlation limit the note's own RG-8 row records for five of the seven prior reviews. It is a limit, not independence.
- **I was dispatched by the implementing lineage, not by the operator.** The pre-authorization's firing condition 2 requires an operator-dispatched gate. **My verdict cannot satisfy it.** A NO-GO from me still holds (a hold needs no authority it lacks); a GO from me would have been worthless for firing the authorization. My seat can block but cannot clear.
- **I refuse any implementer-authored GO,** and I did not accept one. No seat's recommendation was adopted; every load-bearing fact in §1 was re-executed from primary sources. Where the evidence favored the candidate (CodeQL, RG-5 substance, RG4-01) I said so.
- **I did not author the candidate** and **did not produce the seat reports.**
- **I performed no writes.** No merge, tag, Release, ruleset change, packet mutation, operator acceptance, branch push, or publication authorization. I created one read-only detached worktree under my scratchpad and made read-only GitHub API calls.
- **This verdict judges `48009fef` only.** It does not transfer to any successor candidate.

---

## 8. Next actions

### OPERATOR-ONLY — cannot be delegated to any agent

1. **Settle D20/D23 through a channel the lineage does not control.** Per §4, a commit will *not* settle it: the credential is shared, so an operator-authored commit is indistinguishable from an agent one. Use a channel that is: the GitHub Release/issue UI under your own session, or simply treat the ruleset disarm as the authorization act — which is what the design already concedes it is.
2. **Dispatch the independent publication gate yourself** at the successor candidate. Firing condition 2 requires operator dispatch. **No agent can supply this, including me.**
3. **Record operator acceptance** in the form `OPERATOR-ACCEPTANCE-PROCEDURE.md` defines (the `operator_acceptance` object **plus** an authored-or-echo-certified consent artifact) — **or** amend that procedure explicitly under your own hand if you intend chat to suffice. Do not leave the circularity in §4 unresolved; it currently blocks on both branches.
4. **Run or explicitly waive the D8 Step-7b cross-family consult**, with scope, revisit trigger, and exit criterion.
5. **Decide the two RG-2 gaps:** the wiki hand-off (with the RG4-01 kernel disclosed) and the post-tag install-ref advance (RG4-05).
6. **The tag act:** disarm `protect-version-tags`, tag, re-arm in the same sitting, verify with a seeded probe. Not delegable — and per §4 this is now the *only* control carrying real weight.

### AGENT-MAY-PREPARE — **all of these supersede the candidate; batch into exactly ONE successor**

Step 7 supersedes the candidate on any commit, so preparing these piecemeal is the one way to make this worse. One commit, one new candidate, one full re-run of steps 4-6.

1. **Rewrite the RG-5 row** to name the verified candidate runs — `epistemic-flexibility` 32430457960, `release-security` 32430459879, `openai-bundles` 32430452518, `commission-watch-contract` 32430465696, `mission-custody-contract` 32430450479 (`contract` green, `contract-macos` step 8) — and record the three CodeQL matrices. **Delete** the "only change … is this table" paragraph and the "the parent of this commit" phrase (RG1-01).
2. **Correct the publication-review count to three**, name the openai NO-GO, and add it to `V6-VERDICT-LINEAGE.md` (RG1-02).
3. **Commit the openai verdict artifacts in-tree.** Note the distinction that makes this permissible now: step 5 defers verdict artifacts until after the tag because *a tree cannot contain a judgment of itself* — but this verdict judges `d0165bd0`, a **superseded** candidate. It is historical evidence, not self-judgment. Committing it is the genuine PG-03 cure.
4. **Close the RG-4 durability gaps:** add a non-vacuity control to the mermaid check mirroring PG-07's `require(seen_refs >= 1, …)`; add an oracle for the marketplace "full collection" enumeration; add `--check-paths` and a tag-existence guard to `apply_v6_updates.py`.
5. **Record RG4-05** as a bounded RG-2 accepted gap with owner, revisit trigger, and exit criterion.
6. **Move the RG-4 limits into the RG-4 row** rather than grading it flatly "met."
7. **Draft — do not adopt —** a pre-authorization for the successor. The current one names #206 and expires with it.

---

**Bottom line.** The *artifact* is in better shape than the *record of the artifact*. I verified that requalification genuinely happened at this exact commit, CodeQL included — the engineering holds. What fails is the paperwork that must become immutable, and the authority chain beneath it. Two of the three publication gates this project has run said the same thing in different words; this is the third, and it agrees. The lineage built the one control that binds regardless of what any document claims — the tag ruleset with no bypass actors — and that control is why a NO-GO here is a hold rather than an emergency.