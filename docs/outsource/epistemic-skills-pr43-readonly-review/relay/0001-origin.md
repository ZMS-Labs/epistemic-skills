# Origin relay 0001

```yaml
schema: outsource-origin@1
work_id: epistemic-skills-pr43-readonly-review
status: READY
target: ChatGPT with public GitHub read access
subject_revision: 03c16761d67f047b0ffb8a73b9d0b09b65045127
required_capabilities:
  - read public GitHub repository files at exact commits
  - inspect pull-request diff, commits, and check metadata
not_required:
  - git clone or local shell
  - tests or command execution
  - GitHub mutation
  - isolated-role execution
packet_commit: "{packet_commit}"
prompt_template: "Read and follow https://github.com/ZMS-Labs/epistemic-skills/blob/{packet_commit}/docs/outsource/epistemic-skills-pr43-readonly-review/HANDOFF.md. Review PR #43 only at the pinned head using GitHub read access. Return only the required outsource-relay@1 envelope."
origin_retains:
  - implementation and test execution
  - repository and pull-request mutation
  - Gauntlet execution and final verification
  - merge and release authority
```

The origin reconstructs the short prompt by replacing `{packet_commit}` with the commit that
contains this packet. The Git object cannot embed its own hash.
