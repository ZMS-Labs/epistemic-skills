# evidence-locked-uat — Schemas and Evidence Layout

Derived from `standard.md` §9 (verdicts), §47 (contracts), §59 (evidence layout), §38.3 (gate).
The Workflow script in `workflow-template.mjs` embeds these as JSON Schema constants —
this file is the human-readable contract; keep the two in sync. The deterministic judge
is `../scripts/judge.py` (canonical, stdlib Python, harness-agnostic); the `.mjs` embeds
a verified copy of its aggregation for the Workflow tool.

Note: the 7-word verdict vocabulary below deliberately substitutes `NOT_RUN` for the
standard §9's `NOT_APPLICABLE` / `SKIPPED_POLICY` — a recorded narrowing, not drift.

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

Canonical implementation: `../scripts/judge.py` (stdlib Python; run it in any harness).
The rules below are its contract; the `.mjs` embedded copy is verified against it by
`judge.py --self-test`.

- Case status: any criterion FAIL_PRODUCT → FAIL_PRODUCT; else worst non-PASS criterion
  status (severity order: FAIL_TEST_HARNESS > BLOCKED_ENVIRONMENT > FLAKY > INCONCLUSIVE >
  NOT_RUN); else PASS.
- Gate `release_decision`: FAIL if any critical/high case is FAIL_PRODUCT; PASS only if
  every case is PASS; otherwise INCONCLUSIVE. No averaging, ever.
- Completeness: every contract criterion must receive a verdict; a contract criterion with
  no verifier row is scored INCONCLUSIVE (never skipped). Unknown verifier ids are flagged,
  and single-orphan pairs are matched positionally with the mismatch noted.
- Honesty fields are emitted BY the judge, not appended procedurally: `known_limitations`
  is a Level-1 constant, `coverage_omitted` is computed (full release-tier contract×persona
  matrix minus the cases this tier runs), and `target_commit_sha` is pinned in the gate.
  A gate.json missing these fields is incomplete — treat it as suspect, not clean.

## gate.json

```json
{
  "release_decision": "PASS | FAIL | INCONCLUSIVE",
  "run_id": "uat-YYYYMMDD-HHMMSS-<slug>",
  "tier": "smoke | standard | release",
  "calibration_status": "uncalibrated",
  "target": "<base URL>",
  "target_commit_sha": "<target repo commit SHA under test>",
  "cases": [ { "case_id": "…", "criticality": "…", "status": "…", "criteria": [ … ] } ],
  "coverage_omitted": ["<case-id in the full matrix this tier does not run>"],
  "known_limitations": ["Level 1 constant — see scripts/judge.py KNOWN_LIMITATIONS"]
}
```

## manifest.json (normative)

The integrity anchor of the packet. `hashes` seals every committed JSON/YAML artifact —
gate, contracts, and the per-case actor/verifier outputs the gate was aggregated from —
so a downstream consumer can detect post-hoc tampering with the verdict OR its evidence
inputs. Screenshots are gitignored and unhashed — outside the integrity chain.

```json
{
  "run_id": "uat-YYYYMMDD-HHMMSS-<slug>",
  "tier": "smoke | standard | release",
  "target": "<base URL>",
  "target_commit_sha": "<target repo commit SHA under test>",
  "date": "<ISO 8601 run date>",
  "model": "<model/version for the LLM roles>",
  "skill_version": "<skill version string>",
  "judge_sha256": "<sha256 of the canonical judge: scripts/judge.py>",
  "calibration_status": "uncalibrated | calibrated:<corpus-ref>@<date>",
  "environment_fingerprint": "<build, deployment, feature flags, locale, account identity>",
  "seed": "<sampling seed, or null>",
  "sampling": "<temperature/sampling configuration, or null>",
  "tool_versions": { "<tool>": "<version>" },
  "hashes": {
    "gate.json": "<sha256>",
    "contracts.yaml": "<sha256>",
    "cases/<case-id>/actor-output.json": "<sha256 — one entry per case>",
    "verifier/<case-id>.json": "<sha256 — one entry per case>"
  }
}
```

`environment_fingerprint`, `seed`, `sampling`, and `tool_versions` are directive-required
fingerprint fields (`directive.md`: "Record seed, model/version, temperature or sampling
configuration, tool versions, and environment fingerprint"). Record them as `null` when
genuinely inapplicable — present-and-null is honest, omitted is a gap.

## Calibration status vocabulary

`calibration_status` is closed: `uncalibrated | calibrated:<corpus-ref>@<date>`.

- `uncalibrated` — the default and current state of every run. Disclosed, not hidden.
- `calibrated:<corpus-ref>@<date>` — permitted only after the actor→verifier→judge
  pipeline has been run against a named seeded-defect corpus (`<corpus-ref>`) and met the
  standard's pre-publication policy threshold (standard.md: "seeded-defect calibration
  within policy threshold"); `@<date>` is the date of the qualifying corpus run.

Transition: `uncalibrated` → `calibrated:<corpus-ref>@<date>` happens only via a recorded
corpus run; there is no other path, and a calibrated status silently reverts to
`uncalibrated` when the judge, verifier prompt, or contract schema changes materially.
**The seeded-defect corpus does not exist yet — it is the named blocker.** Building it is
deliberately out of scope here (a ceiling, not a floor); the vocabulary exists so the gap
is a path, not a dead end.

## Verifying a packet downstream

A consumer MAY recompute `release_decision` from a committed packet without re-running
any LLM role — the aggregation over the committed actor/verifier outputs is deterministic:

1. Convert `contracts.yaml` to JSON (stdlib Python ships no YAML parser by design; e.g.
   `python -c "import yaml,json,sys; json.dump(yaml.safe_load(open('contracts.yaml')), sys.stdout)" > contracts.json`).
2. Run the canonical judge against the packet:
   `python <skill>/scripts/judge.py --contracts contracts.json --tier <tier> --run-id <run_id> --target <target> --commit-sha <sha> --evidence-dir <packet dir> --output -`
3. Compare `release_decision` and per-case statuses against the committed `gate.json`;
   verify the manifest's `hashes` over the committed files first if tamper-evidence matters.

What this proves: the committed gate is the faithful deterministic aggregation of the
committed actor/verifier outputs. What it does NOT prove: that the verifier's judgments
were correct (they are LLM adjudications), that blinding held at run time, or anything
about the screenshots, which are gitignored and unhashed — outside the integrity chain.

## Evidence directory (`<target-repo>/artifacts/uat/<run-id>/`)

This is the Level-1 evidence layout; standard.md §59 describes the aspirational full-standard
layout for higher maturity levels — do not treat §59 as this skill's contract.

```
manifest.json          # normative schema above — run-id, tier, target, target_commit_sha,
                       # date, model, skill_version, judge_sha256, calibration_status,
                       # fingerprint fields, hashes of all committed artifacts — committed
contracts.yaml         # committed
cases/<case-id>/
  actor-output.json    # committed (hashed in manifest.json)
  screenshots/*.png    # gitignored and unhashed — outside the integrity chain
verifier/<case-id>.json # committed (hashed in manifest.json; one per case, criterion-level decisions)
gate.json              # committed
summary.md             # committed; final-report format per directive (critical failures first,
                       # predicted usability risks labeled as predicted, coverage omitted, assumptions)
```
