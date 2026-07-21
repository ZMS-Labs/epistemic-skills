# evidence-locked-uat — Schemas and Evidence Layout

Derived from `standard.md` §9 (verdicts), §47 (contracts), §59 (evidence layout), §38.3 (gate).
The Workflow script in `workflow-template.mjs` embeds these as JSON Schema constants —
this file is the human-readable contract; keep the two in sync.

## Verdict vocabulary (closed set)

`PASS | FAIL_PRODUCT | INCONCLUSIVE | FAIL_TEST_HARNESS | BLOCKED_ENVIRONMENT | FLAKY | NOT_RUN`

Rules: only PASS is a pass. INCONCLUSIVE / FLAKY / BLOCKED_ENVIRONMENT / FAIL_TEST_HARNESS
never convert to PASS. First run result is immutable — a rerun that passes after a failed
run makes the aggregate FLAKY (reruns get a fresh run-id; both gates are retained).

## Acceptance contract (compiler output → `contracts.yaml`)

```yaml
contracts:
  - id: REQ-<AREA>-<NNN>            # stable ID
    user_goal: "<what the user is trying to achieve>"
    criticality: critical|high|medium|low
    provisional: false               # true when inferred, not sourced from requirements
    preconditions: ["<verifier-checkable starting conditions>"]
    task_prompt: "<the ONLY task text the actor receives>"
    criteria:
      - id: REQ-<AREA>-<NNN>-C1
        statement: "<what must become visibly/persistently true>"
        required_oracles: [rendered-ui, business-state]   # critical ⇒ rendered-ui + ≥1 non-visual
        invariants: ["<what must remain unchanged>"]
        timeout_ms: 5000
    prohibited_side_effects: ["<e.g. duplicate mutation>"]
    ambiguity_notes: ["<unresolved questions — never improvised into a pass>"]
```

Oracle enum: `rendered-ui | accessibility-semantic | business-state | network | invariant | persistence | metamorphic`.

## Actor output (structured, per case) — NO VERDICT BY CONSTRUCTION

`additionalProperties: false` everywhere. There is no verdict, success, or confidence
field; `completed` means "the actor finished attempting the task actions", not success.

```json
{
  "case_id": "REQ-X-001--returning-desktop",
  "completed": true,
  "stop_reason": "task actions finished | stop-condition name",
  "knowledge_ledger": ["facts the persona legitimately learned"],
  "steps": [
    {
      "n": 1,
      "subgoal": "…",
      "precommit": {
        "target_visible_label": "Save changes",
        "target_role": "button",
        "target_region": "lower-right of form",
        "expected_immediate": "busy state",
        "expected_stable": "confirmation visible",
        "prohibited_effects": ["email changes"]
      },
      "action": "click | type '<text>' | press Tab | …",
      "screenshots": {
        "before": "cases/<case>/screenshots/001-before.png",
        "target_crop": "…-target.png",
        "immediate_after": "…-immediate-after.png",
        "stable_after": "…-stable-after.png"
      },
      "observed_after": "what actually rendered (description of observation, not judgment)",
      "annotation": { "noticed": "…", "expected": "…", "discrepancy": "…", "confusion": false }
    }
  ]
}
```

## Verifier output (per case, criterion-level)

```json
{
  "criteria": [
    {
      "criterion_id": "REQ-X-001-C1",
      "status": "PASS",
      "evidence_for": ["cases/<case>/screenshots/003-stable-after.png: new name visible in profile summary"],
      "evidence_against": [],
      "uncertainty": null
    }
  ]
}
```

The verifier may not emit FLAKY (cross-run aggregate only).

## Judge aggregation (deterministic, in script — never an agent)

- Case status: any criterion FAIL_PRODUCT → FAIL_PRODUCT; else worst non-PASS criterion
  status (severity order: FAIL_TEST_HARNESS > BLOCKED_ENVIRONMENT > FLAKY > INCONCLUSIVE >
  NOT_RUN); else PASS.
- Gate `release_decision`: FAIL if any critical/high case is FAIL_PRODUCT; PASS only if
  every case is PASS; otherwise INCONCLUSIVE. No averaging, ever.
- Completeness: every contract criterion must receive a verdict; a contract criterion with
  no verifier row is scored INCONCLUSIVE (never skipped). Unknown verifier ids are flagged,
  and single-orphan pairs are matched positionally with the mismatch noted.

## gate.json

```json
{
  "release_decision": "PASS | FAIL | INCONCLUSIVE",
  "run_id": "uat-YYYYMMDD-HHMMSS-<slug>",
  "tier": "smoke | standard | release",
  "calibration_status": "uncalibrated",
  "target": "<base URL>",
  "cases": [ { "case_id": "…", "criticality": "…", "status": "…", "criteria": [ … ] } ],
  "coverage_omitted": ["<journeys/personas not run at this tier>"],
  "known_limitations": ["Level 1: no pairwise coverage; verifier same-provider; a11y = scan + keyboard only"]
}
```

## Evidence directory (`<target-repo>/artifacts/uat/<run-id>/`)

This is the Level-1 evidence layout; standard.md §59 describes the aspirational full-standard
layout for higher maturity levels — do not treat §59 as this skill's contract.

```
manifest.json          # run-id, tier, target, commit, model, calibration_status, hashes — committed
contracts.yaml         # committed
cases/<case-id>/
  actor-output.json    # committed
  screenshots/*.png    # gitignored
verifier/<case-id>.json # committed (one per case, criterion-level decisions)
gate.json              # committed
summary.md             # committed; final-report format per directive (critical failures first,
                       # predicted usability risks labeled as predicted, coverage omitted, assumptions)
```
