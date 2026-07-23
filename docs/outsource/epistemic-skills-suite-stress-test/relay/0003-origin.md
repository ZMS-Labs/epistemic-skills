# Origin relay 0003

```yaml
schema: outsource-origin@1
work_id: epistemic-skills-suite-stress-test
subject_revision: operator-request-2026-07-23-r2-pr43-continuation
intended_target: operator-selected capable model, agent, or process continuing and independently verifying existing PR 43
target_capabilities:
  - networked GitHub repository checkout and test shell
  - live PR 43 inspection plus authorized branch or replacement-PR publication
  - repository-local deterministic-test execution
  - isolated contexts or contract-equivalent separation for Gauntlet
packet_commit: "{packet_commit}"
active_pr: "https://github.com/ZMS-Labs/epistemic-skills/pull/43"
recorded_pr_head: "03c16761d67f047b0ffb8a73b9d0b09b65045127"
prompt_template: "Read and follow https://github.com/ZMS-Labs/epistemic-skills/blob/{packet_commit}/docs/outsource/epistemic-skills-suite-stress-test/HANDOFF.md. Use the linked repository documents at that exact commit. Return only the Relay response contract defined there."
origin_retains:
  - returned-claim verification
  - history-rewrite approval
  - merge and release authority
  - direct-main publication
  - installed-harness synchronization
```

The target must re-resolve PR #43 before acting. The recorded head is a continuity anchor, not an
instruction to overwrite newer work. The final prompt is reconstructed by substituting the packet
commit from the readiness receipt for `{packet_commit}`.
