# VERDICT OF RECORD — Panel-2 Arbitration, es-v5.1.0 publication gauntlet (panel 2 of max 3)

**Subject:** annotated tag `v5.1.0` on `5906464397305f50d36c59cce91bb397ec7dff27` + non-draft Release, body = `docs/release/RELEASE-5.1.0.md` verbatim.

**Independence caveats (disclosed, binding):** (1) Same model family (GLM-5.3) as the lenses and the discharge author — disclosed, not configurable here; mitigation is that the arbitrator re-verified every load-bearing mechanical row live itself. (2) Chain-of-custody limit: the three panel-2 lens reports were not persisted at arbitrator dispatch time (the run harness's defect, filed as P4 below, since corrected — the seats' final messages are now persisted verbatim at `reports/`); the arbitrator ruled on dispatcher-attributed summaries, the binding prompts (proving the identical frozen dossier `d4988f41…` fed all three seats), and its own live re-verification of every mechanical fact. Lens judgment-layer reasoning carried `[I←V-dispatcher]`, not `[V]`.

## Evidence log (all verified live by the arbitrator, 2026-08-15, post-PR-#183 merge)

E1 `origin/main` = `5906464…`; chain `7ba1f19→8180554→2890ae6→fcf1f75→5906464` · E2 PR #183 merged, checks green (CodeQL ×3, DCO, secret-scan, stdlib-checks incl. live public-content gate) · E3 run 31899154663 (custody, dispatch @5906464): run-level FAILURE; `contract` SUCCESS; `contract-macos` FAILURE at "Custody mission lifecycle unit tests" · E4 openai-bundles 31899156583 SUCCESS; commission-watch 31899158039 SUCCESS; push runs 31899146197/31899146196/31899145807 SUCCESS · E5 run 31723939498 (dispatch @8aa4ffe, 2026-08-13): FAILURE — the "first-ever" falsifier confirmed · E6 in-tree at 5906464: item-5 cell with triple-confirm + 31723939498; known-limitations es#162 entry; GAUNTLET-SUMMARY correction; terminal item-8 GO row + coordinate + independence limits; item-7 tier row + junction pin; item-6 full-window dispositions · E7 runner matrix: ubuntu + macos-14 only, no Windows — "Linux included" bounding accurate · E8 wiki HEAD `14c7df9`; Installation page zero `5.0.0`/`v5.0.0` occurrences; "Applies to: v5.1.0", fifteen · E9 repo description: no router phrase · E10 es#162 OPEN; last comment = the correction addendum · E11 README shared-budget boundary note present; delta `8180554..5906464` docs + README +3 + one comment line, no code changes · E12 per-test identity of the contract-macos failures: step-level match across 4 runs; per-test log not re-parsed `[I←E3,E5]`.

## Conflict Ledger (digest; full reasoning in the arbitrator's record)

- **CL-1 — D/es#162 attack: UPHELD; ruling D recomputed** (the one permitted round). Item-5's claim is about the required suite; the probe-job red falsifies nothing the row asserts; the defect is real, pre-existing (E5), disclosed in-body with run IDs and named tests. Recomputed D: **required-job green at the final SHA + probe reds confined to the named es#162 failure-set + in-body disclosure = conforming.**
- **CL-2 — Exception keying: failure-set, NOT job identity** (decision-rights F#2 upheld). Binding form: *any red at or before tag time in any job of the at-final-SHA suites, except precisely the two named tests (`distinct-real-file-untouched`, `distinct-both-files-tracked-separately`) in the named step ("Custody mission lifecycle unit tests") in the named runs, → P1, revert to iterate.*
- **CL-3 — Lens GO-leans vs release-cutover CONDITIONAL: SPLIT resolved by events** — F#1/F#2 confirmed true and fixed (PR #183 in-tree; wiki 14c7df9); F#4 closed by the three final-SHA dispatches; the GO-lean converts.
- **CL-4 — Semantics-collision owner (decision-rights F#1): UPHELD as a genuine authority gap — P3-docketed, not blocking.** Named owner: the operator (release authority); deliverable: RELEASING.md amendment defining required-job semantics for workflows carrying optional probe jobs; honest dual-level reporting in the tag message (binding).
- **CL-5 — Panel-3 for the PR-#183 correction delta: NOT required** — the one-round bounded-reinstatement doctrine covers a docs-only correction that asserts exactly what the lenses demanded and was re-verified live by the arbitrator; 2 of 3 panels remain in reserve as the reversion path.
- **CL-6 — Ceremony bound: upheld** — no sixth candidate; the next SHA change on this branch is the tag, not a commit.
- **CL-7 — Missing lens reports: verdict proceeded on attribution + live re-verification; harness defect filed (P4), since corrected.**

## P1–P4 decisions

**P1 — none open.** P1-A discharged (strict path: terminal row + coordinate + limits in the immutable body). P1-B discharged (both live surfaces clean; extended by the Codex-cache-path fix at wiki `14c7df9`). The only P1-class candidate (D's escalation) dissolves under CL-1.

**P2 — discharged; binding execution conditions attach to the publication act.** The annotated tag message MUST carry (falsifier: `git cat-file tag v5.1.0`):
1. Final-SHA run IDs stated honestly — `mission-custody-contract` 31899154663: required `contract` job SUCCESS; `contract-macos` probe FAILED, **run-level conclusion: failure**, at the known es#162 step (the two named tests); `openai-bundles` 31899156583 success; `commission-watch-contract` 31899158039 success; push 31899146197/31899146196/31899145807 success.
2. **No "both suites success" claim** for the custody run.
3. Panel-2 verdict coordinate (`es-v510-publication-2026-08-15/panel2`, GO-binding-on-execution) + GO status + independence limits.
4. AP-3 mechanics: local annotated tag → push → API peel-verify at `5906464` → `gh release create --verify-tag --notes-file docs/release/RELEASE-5.1.0.md`.
5. The CL-2 re-escalation clause.

**P3 — post-tag docket:** (1) semantics-collision owner line (operator; RELEASING amendment); (2) post-tag record-mirror correction — known-limitations under-names the true final-SHA custody dispatch (31899154663; the row cites 31897018984/31898055755) — nothing false ships immutably because the tag message carries the true final runs; (3) standing docket unchanged (check_public_content RFC1918/UNC/email patterns + RED seeds; ALLOWLIST_PREFIXES narrowing; POSIX install guard; Kimi/plugin.json custody enumeration; path-filter ⊇ input-space guard; full v5.1.0 wiki packet; v5.0.0 release-body amendment execution; es#162 filesystem-probe fix).

**P4 — harness, not subject:** panel reports must be persisted at seat completion, before arbitrator dispatch.

## Computed verdict

**For: "create annotated tag `v5.1.0` on `5906464397305f50d36c59cce91bb397ec7dff27` and publish the non-draft Release with `docs/release/RELEASE-5.1.0.md` verbatim" → GO, binding on execution.**

Gate logic: P1 ×2 discharged; P2 C/E/F/G + AP-2 discharged; P2 D discharged as recomputed under CL-1/CL-2; no unresolved P1 or P2 remains → per panel-1 line-2's own conversion rule, the GO converts at re-affirmation. **Not CONDITIONAL:** no pre-tag work item is open — the tag-message content spec is a constraint on the publication act itself. **Reversion triggers:** any red outside the named es#162 failure-set at/before tag creation (→ NO-GO, revert to iterate, panel 3 in reserve); a tag message claiming both suites succeeded (= non-conforming release, erratum + amend obligation); any regression surfacing pre-tag. **Non-claims inherited:** not behavioral superiority; not a retrospective v5.0.0 GO; not a macOS fix for es#162 (settled and disclosed); satisfies no externally-enforced infra safety gate.

## GO coverage statement

Capability families exercised (arbitrator, live): git lineage/squash identity + SHA pinning; Actions API at run/job/step level (10 runs); PR merge/check state; open-world live surfaces (description, wiki HEAD + content); issue-trail verification; in-tree body/record text at the exact final SHA; runner-matrix reading; full delta file audit. Material assumptions: dispatcher attribution of lens judgment content (mechanical rows independently re-verified); panel-1 rulings on unchanged content stand per doctrine; "exactly 2 tests" rests on step-level match across four runs plus the committed record, not a fresh per-test parse. Known unknowns: per-test composition at 5906464; the same-family ceiling over everything non-mechanical; further commits landing on main before tagging (they do not move the tag target). Evidence freshness: all probes 2026-08-15 post-#183. Residual uncertainty: the publication act and same-session post-tag set (`-Verify` 15-junction receipt, junction bump, step-9 identity checks, post-tag record mirror) are unexecuted by design — carried obligations of this GO.

## Single most important next action

**Create the annotated tag now** (message per the binding conditions), push, API peel-verify the target is `5906464`, `gh release create v5.1.0 --verify-tag --notes-file docs/release/RELEASE-5.1.0.md`, then the same-session post-tag set. Every pre-tag obligation is discharged and verified. **There must be no sixth candidate.**
