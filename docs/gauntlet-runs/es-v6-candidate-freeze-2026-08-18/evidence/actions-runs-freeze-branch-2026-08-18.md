# GitHub Actions runs on branch cursor/v6-candidate-build-5c03 — recorded 2026-08-18 (this session, via GitHub API)

Query: actions list_workflow_runs filtered to branch `cursor/v6-candidate-build-5c03`.
Result: total_count 10; every run `skipped`; head SHAs are ONLY the two
post-freeze commits. **No workflow run of any kind exists at the candidate
SHA `00e5146e43ff9011153452b83fedda706723c52b` on this branch.**

| Run id | Workflow | Event | head_sha | Conclusion | Created |
|---|---|---|---|---|---|
| 32149796394 | mission-custody-contract | pull_request | 7de88fa | skipped | 2026-08-18T14:40:41Z |
| 32149796340 | epistemic-flexibility | pull_request | 7de88fa | skipped | 2026-08-18T14:40:41Z |
| 32149796460 | release-security | pull_request | 7de88fa | skipped | 2026-08-18T14:40:41Z |
| 32149795789 | DCO | pull_request_target | 7de88fa | skipped | 2026-08-18T14:40:41Z |
| 32149796346 | openai-bundles | pull_request | 7de88fa | skipped | 2026-08-18T14:40:41Z |
| 32149706759 | DCO | pull_request_target | 36df665 | skipped | 2026-08-18T14:39:50Z |
| 32149706808 | openai-bundles | pull_request | 36df665 | skipped | 2026-08-18T14:39:50Z |
| 32149706712 | release-security | pull_request | 36df665 | skipped | 2026-08-18T14:39:50Z |
| 32149706722 | epistemic-flexibility | pull_request | 36df665 | skipped | 2026-08-18T14:39:50Z |
| 32149706843 | mission-custody-contract | pull_request | 36df665 | skipped | 2026-08-18T14:39:50Z |

Separately, the CodeQL Analyze matrices reported success as CHECK RUNS on
both draft-PR heads (`7de88fa`, `e8a476c`) — see
`github-live-state-2026-08-18.md`. Those are the only green CI signals
anywhere on the candidate chain, and neither names `00e5146`.
