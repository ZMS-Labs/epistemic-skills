# Live behavioral epoch — 2026-08-04 (first epoch for this battery)

**Outcome: FAIL — 12/14 fixtures pass the deterministic scorer.**
Supersedes `results/BLOCKED.md`. Failures are committed as results, not
retried away.

## Methodology

Protocol as the sibling 2026-08-04 epochs: fourteen fully isolated
general-purpose subagents (claude-fable-5, Claude Code harness, N=1), one
per fixture, subject-blinded (expected actions/trigger labels withheld),
subjects read exactly SKILL.md (evals/ forbidden), shipped `score.py`
unmodified, trials declared simulations with no file writes, README's
pinned response contract quoted verbatim in every dispatch. Fixture ids
were masked behind opaque trial keys (T01–T14, deterministic
sha256-of-id order; ids encode polarity) and remapped before scoring.
Mapping: T01=copy-paste-review-handoff-fires, T02=pointer-not-paste-state,
T03=hidden-chat-context-blocked-state, T04=colleague-agent-question-no-fire,
T05=capable-target-preflight-fires, T06=in-session-subagent-no-fire,
T07=beyond-origin-surface-fires, T08=packet-before-prompt-state,
T09=relay-claim-verified-state, T10=inbound-target-work-no-fire,
T11=readonly-target-preflight-blocked-state,
T12=explicit-superior-model-fires, T13=self-handoff-local-task-no-fire,
T14=unpushed-packet-blocked-state.

Preregistration before dispatch: predicted 11/14 — 1–2 `immutable_ref`
format misses on the publish-packet fixtures plus a bare-id vocabulary
miss on `claims_checked` (ids not stated in scenario prose, an
underspecification probe). Actual 12/14: the `immutable_ref` prediction
was **falsified** (all six publish-packets produced well-formed 40-hex
SHAs), and the vocabulary-miss prediction **confirmed in class but not
location** — it landed on the capability ids, not the relay-claim ids.

## Results

publish-packet 6 · verify-relay 1 · report-blocked 3 · no-fire 4; two
failures, both the same defect class:

- `capable-target-preflight-fires`: `capabilities_verified` named the four
  required capabilities as `runnable-test-shell`,
  `github-mutation-actions`, `isolated-execution-contexts` (plus extras)
  instead of the canonical `test-shell`, `github-mutation`,
  `isolated-context`.
- `readonly-target-preflight-blocked-state`: `capabilities_failed` same
  drift (`shell`, `test-execution`, `branch-commit-push`, …).

Both subjects ran the preflight, reached the correct conclusion, and
blocked/verified correctly — the divergence is that the canonical bare
capability ids appear only in the battery README (which subjects may not
read), while the scenarios and SKILL.md describe the capabilities in
prose. This is the reporting-vocabulary failure mode of the 2026-08-04
suite sweep (issue #77), reproduced under a born-pinned contract when the
id vocabulary lives outside the pinned text. The fix belongs in the
shared response-contract work item, not in retrying the epoch.

Conduct notes on the passing 12: every publish-packet reported
packet-before-prompt ordering with a pointer prompt (the full-paste
sketch in `pointer-not-paste-state` was corrected to a pointer); all
three blocks named the right single blocker and emitted no ready-looking
prompt; the relay reply was stored verbatim and re-verified with
`claims_checked` covering both fixture claims; all four no-fires produced
no truthy process artifacts (one carried explicit false-valued keys and a
rationale — non-truthy, scored silent, recorded here as a borderline the
shared contract should settle).

## Honest limits

Smoke-scale, N=1 per fixture, one model/harness, same model family
throughout; subject-level blinding only; dispatch glosses are part of the
intervention surface. This scores trigger/scope and record-shape
conformance on these 14 scenarios — no real packet was committed, no real
SHA resolved, no real relay verified.
