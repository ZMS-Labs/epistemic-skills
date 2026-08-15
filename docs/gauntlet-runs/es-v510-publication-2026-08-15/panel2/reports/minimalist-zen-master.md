# Panel-2 finding-set — minimalist-zen-master (constructive), delta `8180554..fcf1f75`

> Persisted post-hoc by the dispatcher (the seat's final message, verbatim); the panel-2 arbitrator originally received it as dispatcher attribution — the non-persistence is the arbitrator's P4 finding, corrected here.

## F1 [P1] The D/es#162 bounded-reinstatement attack succeeds: the `contract-macos` red does not block the tag; green-required-job + disclosed-limitation is conforming

**Claim.** Ruling D's "any red → P1" clause, purposively read, binds the *required* gate — and the required gate is green at the final SHA. Four independently verified facts close the question:
1. **Structural:** `contract-macos` is `if: github.event_name == 'workflow_dispatch'` — it can never fire on push or PR, so it is definitionally outside the push-gate the release law requires. `[V .github/workflows/mission-custody-contract.yml:78]`
2. **Self-blocking reductio:** D's own acceptance action is `gh workflow run mission-custody-contract.yml` — the *only* mechanism that can ever fire the probe job. The literal reading makes the discharge's required action trigger the discharge's own P1 escalation; a rule whose ordered execution self-blocks cannot be the intended rule. `[I <- V arbitration.md:50 (D's text); workflow_dispatch trigger at :4]`
3. **Pre-existing, not delta-caused:** the delta is docs-only plus one comment line (`14→15` in a comment, no code) — it cannot have introduced a filesystem case-sensitivity defect. `[V git diff 8180554..fcf1f75 --name-status + .github/scripts/check_description_budget.py hunk]`
4. **Deterministic and disclosed:** identical 2 failures (`contract-macos`, step "Custody mission lifecycle unit tests") across two independent dispatch runs at two SHAs (`2890ae6` run 31897018984, `fcf1f75` run 31898055755 — live-verified job-level); disclosed in the release body known-limitations (`[V docs/release/RELEASE-5.1.0.md:168]`), in item-5 (`:90`), and on es#162 (evidence addendum 2026-08-15T17:27:33Z citing the final-SHA run). `[V gh api runs/31897018984/jobs, runs/31898055755/jobs, issues/162]`

The required `contract` job succeeded at **both** dispatch SHAs. `[V same API calls]` The red produced true content (the es#162 settlement) that the release now carries; blocking on it would punish the discharge for producing exactly the evidence D's dispatch was ordered to generate, and "revert to iterate" is empty — no in-delta action could green a pre-existing code defect whose fix panel 1 explicitly docketed post-tag (GAUNTLET-SUMMARY non-claim: "Not a macOS fix for es#162").

**Validation kernel.** A red blocks the tag iff it is a red in the required push-gate at the final SHA. This red is (a) structurally outside the required gate, (b) deterministic across two dispatches, (c) diagnosed to a pre-existing defect the docs-only delta did not introduce, (d) disclosed in body + issue + (per item-5/AP-3) the tag message. All four bounds hold; the carve-out is tight — a job that fails on push, or any required-job red, still blocks.

**Falsifier.** Statement: this ruling would be wrong if `contract-macos` were push/PR-triggered, or the required `contract` job had failed at either dispatch SHA, or the 2 failures were non-deterministic. Method: `gh api .../actions/runs/{id}/jobs` on both dispatch runs plus trigger inspection of the workflow file. Threshold: any required-job failure, any push-triggered macOS job, or failure-set divergence between the two dispatches. Timeframe: pre-tag (both dispatch runs already executed; conditions checked and absent as of 2026-08-15).

## F2 [P1] Discharge-set completeness: every panel-1 P1/P2 acceptance criterion is satisfied as written (D under F1's bounded reading)

**Claim.** Per-criterion, verified against the delta and live surfaces:
- **P1-A** — terminal item-8 row with status GO, record coordinate, and independence-limits sentence: `[V docs/release/RELEASE-5.1.0.md:93]` (all three elements present; GO record committed at `fcf1f75`; this panel is the re-affirmation the row itself names, with "a regression there reverts to iterate, no tag").
- **P1-B** — repo description re-probed live 2026-08-15: no router phrase `[V gh api repos/ZMS-Labs/epistemic-skills --jq .description]`; wiki install page: "Applies to: epistemic-skills v5.1.0", fifteen ×2, `tree/v5.1.0` URLs, zero `tree/v5.0.0`, wiki HEAD `710dd2b` matching the dossier `[V live fetch of the rendered page; git ls-remote]`.
- **P2-C** — full-window review with dispositions: 266 files / +35,354/−466 matches `git diff --shortstat v5.0.0..8180554` exactly; the 8 RFC1918-bearing files enumerate identically to the disposition and spot-check as new-since-v5.0.0; recorded in the file (`[V RELEASE-5.1.0.md:124ff]`) and in PR #181 notes. `[V]`
- **P2-D** — both suites dispatched at the final SHA `fcf1f75`: `openai-bundles` run 31898057134 conclusion success `[V]`; `mission-custody-contract` run 31898055755 required-job success, run-level failure via F1's carve-out `[V]`. Run IDs recorded in item-5 and bound for the tag message.
- **P2-E** — item-7 re-pointed to `HARNESS-VERIFICATION-MATRIX-SUCCESSOR-2026-08-07.md` with the fourteen-count bounded for fifteen `[V :92]`; README bridge row `[V README.md:231]`.
- **P2-F** — referent pinned verbatim ("mechanism was verified at v5.0.0 content... no recorded procedure"; tier not upgraded) `[V :92]`; post-tag `-Verify` receipt correctly still pending.
- **P2-G** — README budget boundary row naming silent-drop + the 8,636-byte consumption `[V README.md:234]`.
- **AP-2 rider** — budget-script comment 14→15 `[V diff]`.

**Validation kernel.** Each criterion's named elements were located in the delta or on the live surface; mechanical rows were re-verified at run and job level via live API, not taken from the dossier.

**Falsifier.** Statement: any named acceptance element is absent or stale. Method: diff inspection (`git diff 8180554..fcf1f75`) for tree elements; live re-probe (description, wiki page) for B. Threshold: any single element missing, or any install-affecting line on the wiki pointing at v5.0.0. Timeframe: pre-tag; B re-probed again at tag time per the criterion's own requirement.

## F3 [P2] Wiki Codex render-script path still says `5.0.0` against a `5.1.0` plugin manifest — instruction-breaking residual inside the docketed packet pass

**Claim.** The wiki Codex instructions pin `--ref v5.1.0` but the documented render path is `.../epistemic-skills/5.0.0/skills/gauntlet/scripts/render_codex_agents.py`; the plugin manifest at the candidate declares `5.1.0`, so a fresh install's cache path will not match the documented one and the verbatim instruction breaks. `[V live wiki fetch; V plugins/epistemic-skills/.codex-plugin/plugin.json:3 ("version": "5.1.0")]` Also present: "Current skills (v5.0.0)" heading and a v5.0.0 navigation link (cosmetic). This is not a P1-B discharge failure — the criterion's three named elements are met and the full handbook pass is named-and-bounded as post-tag in the record — but it is the one residual in the class that is *instruction-breaking* rather than cosmetic, and it should be first in the post-tag packet, not buried in it. Not a delta regression: the string carried over from the v5.0.0-era page; the delta never touched it.

**Validation kernel.** Install-critical lines verified at v5.1.0 (marketplace ref, applies-to, fifteen); the breakage is confined to one path literal contradicted by the candidate's own manifest.

**Falsifier.** Statement: my "stale" claim is wrong if the Codex plugin cache actually versions that path component independently of the manifest (so the documented path resolves at a fresh v5.1.0 install). Method: fresh install per the page on any host, check the documented path exists. Threshold: render script found at the `5.0.0` path post-install → claim falsified, downgrade to cosmetic. Timeframe: the post-tag wiki packet pass.

## F4 [P3] Item-5's parenthetical pre-records this panel's ruling in the would-be-immutable body

**Claim.** `RELEASE-5.1.0.md:90` says the "red blocks the tag" clause "is ruled there against the probe-job attack" — written *before* this panel ruled. Self-protecting (item-8's "a regression there reverts to iterate, no tag" means an opposite ruling ships no tag, so no immutable falsehood is constructible), and with this panel's actual ruling (F1) the sentence is accurate. But the adjudication lives in the panel-2 record; the body needed only "adjudicated by panel-2" — the stronger phrasing is presumptuous wording the release will carry forever. No pre-tag action (minting a new candidate to soften one accurate-if-this-panel-conforms clause would be ceremony, not safety); erratum-eligible with the packet. `[V RELEASE-5.1.0.md:90; I <- V item-8 :93 reversion clause]`

**Validation kernel.** The wording risk is conditional-on-panel-2-disagreement, and the disagreement world ships no tag; therefore the residual is stylistic, not factual.

**Falsifier.** Statement: this is harmless only while the body's parenthetical matches the archived panel-2 record. Method: compare the tagged commit's panel-2 record against the item-5 parenthetical. Threshold: any contradiction between them at tag time. Timeframe: at tag creation (AP-3 peel-verify step).

## F5 [P3] Durable lesson: write red-blocks-tag rules against required jobs, not run labels

**Claim.** Ruling D was authored at run-level ("both `conclusion=success`... any red → P1") while its own ordered dispatch fires a diagnostic job outside the required gate — the ambiguity consumed a panel-2 seat to resolve. Future discharge rulings should scope the blocker to per-job conclusions of the push-gated job set, with dispatch-only diagnostics non-blocking-with-disclosure under F1's four bounds. Zero new mechanism needed; this is a one-sentence drafting convention. `[I <- V arbitration.md:50; V workflow :78]`

**Validation kernel.** The failure mode is structural (rule granularity coarser than the artifact it governs), and it recurs by default unless the convention changes.

**Falsifier.** Statement: the convention is unnecessary if future workflow designs keep diagnostics out of gated workflows entirely. Method: inspect the next release's ruling text and any new diagnostic jobs. Threshold: a dispatch-only job inside a gated workflow with no job-level scoping in the ruling → recurrence. Timeframe: next release cycle.

## Verdict-lean

**GO.** (1) Every P1/P2 acceptance criterion in `arbitration.md` is satisfied as written — P2-D at required-job level under F1's bounded reading, which is the only defensible reading given the dispatch-only topology and the self-blocking reductio of the literal one. (2) The `contract-macos` red is the es#162 settlement, deterministic, pre-existing, and disclosed in body, issue, and (by AP-3 obligation) the tag message — it does not block. (3) No delta regression: docs-only delta, all push CI and PR checks green at the identical tree (`66ef527` tree ≡ `fcf1f75` tree, verified), required custody job green at both dispatch SHAs, and the public-content gate demonstrably still bites (run 31897515108 failed on the "Public-content gate" step and was fixed in-repo before the green runs).

Constructive note, plainly: this delta is what a minimal discharge looks like — zero new capability, one comment line touched outside `docs/`, ~954 insertions of which the bulk is the transparency record itself. Nothing here should be deleted and nothing was over-built; the ambition was right. Ship via AP-3's pinned mechanics with the tag message carrying the item-5 run IDs *including the `contract-macos` red and its es#162 coordinate* plus this panel's verdict coordinate, then the same-session post-tag receipts (junction bump, `-Verify` 15-junction record per F), with F3 first in the wiki packet pass. Reversion triggers that would flip this lean: any *required*-job red discovered at the tag SHA, or either P1-B live surface found regressed at the tag-time re-probe.

## Coverage note

Verified live at run+job/step level: 31898057134 (success @ `fcf1f75`), 31898055755 (contract success / contract-macos failure, failing step named), 31897018984 (same shape at `2890ae6`), 31898047761/770/31898045807/113 (push CI @ `fcf1f75`), 31897970380/31897970410 (PR checks @ tree-identical `66ef527`), 31897515108 (gate-catch failure step). Not individually re-peeled: S1 `openai-bundles` 31897020113 (covered by its verified S2 twin at the final, gating SHA), the three transient-stall runs 31897841618/616/565 (immaterial — PR checks at the identical tree are green), CodeQL matrix steps beyond run-level success, the wiki Home banner, and the sanitized-report text diff (gate-catch run verified instead). Same-family ceiling (GLM-5.3 across lenses, arbitrator, discharge author, and this seat) stands as recorded in GAUNTLET-SUMMARY — mechanical rows re-verified here independently; judgment rows (F1's purposive reading foremost) remain bounded by it.
