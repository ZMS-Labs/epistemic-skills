# Origin relay 0005

```yaml
schema: outsource-origin@1
work_id: epistemic-skills-suite-stress-test
subject_revision: operator-request-2026-07-23-r3-target-preflight
status: BLOCKED
blocker: target capability preflight not satisfied
intended_target: NONE_SELECTED
required_target_capabilities:
  - networked writable repository checkout
  - runnable repository test shell
  - authenticated GitHub branch, commit, push, and pull-request mutation
  - isolated Gauntlet contexts or contract-equivalent separation
packet_commit: "{packet_commit}"
active_pr: "https://github.com/ZMS-Labs/epistemic-skills/pull/43"
recorded_pr_head: "03c16761d67f047b0ffb8a73b9d0b09b65045127"
prompt_template: NONE_UNTIL_PREFLIGHT_PASSES
resume_condition: operator selects a target and verifies all four capabilities from its actual tool surface
origin_retains:
  - target-readiness determination
  - returned-claim verification
  - history-rewrite approval
  - merge and release authority
```

This turn intentionally stores no execution prompt. The next origin relay may restore the canonical
short prompt only after the target passes all four checks in `HANDOFF.md`.
