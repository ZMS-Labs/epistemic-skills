# Origin relay 0001

```yaml
schema: outsource-origin@1
work_id: epistemic-skills-suite-stress-test
subject_revision: operator-request-2026-07-23-r1
intended_target: operator-selected superior or specialized model, agent, or process
target_capabilities:
  - public GitHub read access
  - branch or fork creation and pull-request publication
  - repository command and deterministic-test execution
  - isolated contexts or contract-equivalent separation when independence is required
packet_commit: "{packet_commit}"
prompt_template: "Read and follow https://github.com/ZMS-Labs/epistemic-skills/blob/{packet_commit}/docs/outsource/epistemic-skills-suite-stress-test/HANDOFF.md. Use the linked repository documents at that exact commit. Return only the Relay response contract defined there."
origin_retains:
  - returned-claim verification
  - merge and release authority
  - direct-main publication
  - installed-harness synchronization
```

The final operator-facing prompt is reconstructed by substituting the packet commit from the
`PACKET` readiness receipt for `{packet_commit}`. This committed template plus that immutable SHA
determines the exact prompt without requiring a Git commit to contain its own hash.
