# R8 ready-mark drill transcript — 2026-08-18 (acceptance evidence)

Drill per gauntlet ruling R8's acceptance criterion (run
`es-v6-candidate-freeze-2026-08-18`): with
`types: [opened, synchronize, reopened, ready_for_review]` added to the
five gating workflows (rc2 commit `f71f450`), a throwaway draft PR was
opened and then marked ready WITH NO NEW PUSH; each gating workflow had
to dispatch at the identical head SHA.

- Drill PR: #196 (head `claude/r8-ready-mark-drill` @
  `564a1e53748cae9f81f48787129ecaf0abaed447`, base
  `claude/v6-candidate-rc2`; closed unmerged, branch deleted).
- Touched paths hit every gating workflow's filter: a docs file
  (epistemic-flexibility), a mission-custody README (custody contract +
  openai-bundles via `plugins/epistemic-skills/**`), a watch-commission
  README (commission-watch); release-security is unfiltered.

## DRAFT state (opened 2026-08-18T20:45Z) — all gating jobs skipped

| Check | Conclusion | Run |
|---|---|---|
| stdlib-checks | skipped | 32184007807 |
| contract (custody) | skipped | 32184007823 |
| contract (commission-watch) | skipped | 32184007806 |
| build (openai-bundles) | skipped | 32184007779 |
| full-history-secret-scan | skipped | 32184007819 |
| DCO | skipped | 32184007795 |
| contract-macos | skipped (dispatch-only, by design) | 32184007823 |

## READY state (marked ready 2026-08-18T20:46Z, same head 564a1e5) — every gating workflow dispatched NEW runs

| Check | Conclusion | Run |
|---|---|---|
| stdlib-checks | **executed — failure** (see note) | 32184104218 |
| contract (custody) | **success** | 32184104186 |
| contract (commission-watch) | **success** | 32184104140 |
| build (openai-bundles) | **success** | 32184104194 |
| full-history-secret-scan | **executed** (in progress at snapshot) | 32184104164 |
| DCO | **success** | 32184105058 |
| contract-macos | skipped (dispatch-only, correct) | 32184104186 |

**Threshold met:** at least one NEW workflow run was created by the
ready_for_review action for each of the five gating workflows at the
unchanged head SHA, with every gating job conclusion != skipped.

**Note on the stdlib-checks failure:** it EXECUTED (the drill's point)
and failed at the `v6 workflow oracle audit` step with the known latent
`RuntimeError: PyYAML required` — the same defect PR #195's second
commit fixes on main (the step had never run in CI anywhere before
2026-08-18: masked on main by the fail-fast public-content failure and
skipped on drafts). The identical fix is applied to this branch in the
commit that lands this transcript. The failure is itself corroborating
evidence that the ready-mark takeover now dispatches real execution.
