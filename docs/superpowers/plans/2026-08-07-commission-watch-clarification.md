# Commission-Watch Clarification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `watch` an unambiguous commission-watch discipline with a machine-checkable output contract that cannot report an active watcher without an external persistent mechanism and complete proof path.

**Architecture:** Preserve the stable `watch` skill id while changing its public role language and outputs. Add a stdlib-only `watch-commission@1` semantic verifier, executable examples, and RED controls; then update the skill and live documentation to emit that contract. The skill never becomes a scheduler or monitoring provider.

**Tech Stack:** Markdown Agent Skill, JSON Schema draft 2020-12, Python 3.12 standard library, GitHub Actions, existing sentinel and description-budget checks.

## Current branch status

On PR #110 / branch `chatgpt/practical-agency-manifest`, the producer side is
already implemented. The checked-in schema, semantic verifier, `watch` skill,
executable example corpus, sentinel alignment, and focused
`commission-watch-contract` CI are authoritative over earlier RED-stage
statements and illustrative snippets later in this plan (including any text that
still says production code is missing). Preserve the RED → GREEN chronology
below as implementation history; do not weaken the final carrier from an
earlier excerpt.

## Global Constraints

- Keep `plugins/epistemic-skills/skills/watch/` and frontmatter `name: watch` in the current major line.
- Canonical role text is **commission-watch**; the description must state that the skill itself does not watch.
- Do not add a second alias skill or another resident description.
- Do not change immutable `v5.0.0` files or rewrite historical release evidence.
- `PROVEN` requires an external persistent mechanism, reachable destination, exercised kill switch, explicit authority, bounded enablement, safe crossing, production path, observed crossing, and received alert.
- Missing substrate, destination, authority, kill switch, safe proof, or probe is an explicit `BLOCKED` result.
- Never auto-remediate.
- Every production behavior change follows RED → GREEN → REFACTOR.
- Every commit carries `Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>`.
- The aggregate loaded-description budget must not increase silently; any description growth must be paid for in the same diff.

---

## As-built contract refinement — normative over the original task sketches

Implementation uncovered state/evidence distinctions the original task-level
examples did not express. The following rules govern every task below and
supersede any simpler fixture or field sketch later in this plan:

- `state` is current operating state; proof is retained historical evidence.
- A successful proof followed by disablement is valid `INERT` with a complete
  proof bundle, never current `PROVEN` and never discarded evidence.
- Proof history under `INERT` is either wholly absent or complete; partial proof
  is rejected.
- Positive claims require durable receipt references for destination
  reachability, external persistence, kill-switch exercise, proof authority, and
  alert delivery.
- `BLOCKED` requires a checked missing or unproven dependency, observation time,
  and external evidence receipt; its closed reason must agree with the record.
- A newly prepared persistent mechanism remains
  `BLOCKED: KILL_SWITCH_UNPROVEN` until the real disable path is exercised and
  receipted. Only then can the disabled mechanism become `INERT`.
- External substrates use a closed type set that excludes Markdown skills and
  prompt/session memory even when mislabeled or self-asserted as persistent.
- Fixture evidence is accepted only with explicit isolated/test scope and a
  statement of the unestablished production coverage.
- `PROVEN` requires a re-proof boundary.
- `SUSPECT` requires an observed failure kind, detail, time, and receipt; possible
  failure modes alone are not an incident.

Additional committed fixtures are required:

- `valid-inert-with-proof-history.json`;
- `valid-suspect-observed-failure.json`;
- `valid-blocked-kill-switch-unproven.json`;
- `invalid-inert-partial-proof-history.json`; and
- `invalid-suspect-without-observed-failure.json`.

The authoritative executable surface is the checked-in schema, verifier, tests,
and examples. Preserve the original RED/GREEN chronology below as implementation
history; do not use an earlier code excerpt to weaken the final carrier.

## File structure

- `plugins/epistemic-skills/contracts/watch-commission/watch-commission.schema.json` — structural carrier for `watch-commission@1`.
- `plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py` — stdlib-only semantic verifier and CLI.
- `plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py` — RED/GREEN contract tests.
- `plugins/epistemic-skills/contracts/watch-commission/examples/valid-proven.json` — complete positive control.
- `plugins/epistemic-skills/contracts/watch-commission/examples/valid-blocked.json` — honest no-substrate outcome.
- `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-skill-is-observer.json` — rejects prompt-time persistence fiction.
- `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-proven-without-alert.json` — rejects silence-as-health.
- `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-proven-without-kill-switch.json` — rejects documentary kill switches.
- `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-proven-without-production-path.json` — rejects bypass proof.
- `plugins/epistemic-skills/contracts/epistemic-events/sentinels/watch-silence-read-as-healthy.json` — align the existing sentinel with commission vocabulary.
- `plugins/epistemic-skills/skills/watch/SKILL.md` — commission-watch trigger, method, output, safety, and evidence-emission contract.
- `plugins/epistemic-skills/skills/health/SKILL.md` — update the neighboring capability reference without changing health semantics.
- `README.md` — live catalog and task-choice language.
- `.github/workflows/epistemic-flexibility.yml` — execute and compile the new verifier/tests.
- `.github/scripts/check_description_budget.py` — change only if the measured package total legitimately changes; set the ceiling exactly to the new total.

---

### Task 1: Plant the semantic RED tests

**Files:**
- Create: `plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py`
- Modify: `.github/workflows/epistemic-flexibility.yml`

**Interfaces:**
- Consumes: none.
- Produces: expected callable `validate_record(record: dict[str, object]) -> list[str]` from `verify_watch_commission.py`.

- [ ] **Step 1: Write the failing contract tests**

Create `test_watch_commission.py` with this structure:

```python
#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from verify_watch_commission import validate_record  # noqa: E402


def proven_record() -> dict[str, object]:
    return {
        "schema": "watch-commission@1",
        "commission_id": "wc-test-001",
        "subject": {"ref": "service:example", "revision": "rev-1"},
        "bound": {
            "expression": "free_space_percent < 15",
            "units": "percent",
            "direction": "below",
            "threshold": 15,
        },
        "probe": {
            "mechanism": "external metric query",
            "cadence_or_event": "every 5 minutes",
            "failure_modes": ["timeout", "authentication failure"],
        },
        "destination": {"ref": "recipient:test", "reachable": True},
        "external_observer": {
            "substrate": "fixture-adapter",
            "mechanism_ref": "fixture://watch/001",
            "persistent_outside_session": True,
            "enabled": True,
        },
        "kill_switch": {"procedure_ref": "fixture://kill/001", "exercised": True},
        "proof": {
            "authorized_by": "operator:test",
            "safe_crossing": "fixture threshold override",
            "production_path": True,
            "bound_crossed": True,
            "alert_received": True,
            "received_at": "2026-08-07T12:00:00Z",
        },
        "state": "PROVEN",
        "block_reason": None,
        "reprove_after": "2026-09-07T12:00:00Z",
        "handoff": {"on_crossing": ["triage", "decision-ledger"]},
        "coverage_limits": ["fixture only"],
    }


def assert_rejected(record: dict[str, object], code: str) -> None:
    errors = validate_record(record)
    assert any(error.startswith(code + ":") for error in errors), errors


def test_complete_external_path_is_proven() -> None:
    assert validate_record(proven_record()) == []


def test_skill_text_cannot_be_the_external_observer() -> None:
    record = proven_record()
    record["external_observer"] = {
        "substrate": "markdown-skill",
        "mechanism_ref": "plugins/epistemic-skills/skills/watch/SKILL.md",
        "persistent_outside_session": False,
        "enabled": True,
    }
    assert_rejected(record, "EXTERNAL_PERSISTENCE_REQUIRED")


def test_silence_cannot_be_proven() -> None:
    record = proven_record()
    proof = copy.deepcopy(record["proof"])
    assert isinstance(proof, dict)
    proof["alert_received"] = False
    proof["received_at"] = None
    record["proof"] = proof
    assert_rejected(record, "ALERT_RECEIPT_REQUIRED")


def test_documented_kill_switch_is_not_exercised() -> None:
    record = proven_record()
    record["kill_switch"] = {"procedure_ref": "docs/kill.md", "exercised": False}
    assert_rejected(record, "KILL_SWITCH_EXERCISE_REQUIRED")


def test_bypass_message_is_not_production_path_proof() -> None:
    record = proven_record()
    proof = copy.deepcopy(record["proof"])
    assert isinstance(proof, dict)
    proof["production_path"] = False
    record["proof"] = proof
    assert_rejected(record, "PRODUCTION_PATH_REQUIRED")


def test_missing_substrate_is_explicitly_blocked() -> None:
    record = proven_record()
    record["state"] = "BLOCKED"
    record["block_reason"] = "NO_EXECUTION_SUBSTRATE"
    record["external_observer"] = {
        "substrate": None,
        "mechanism_ref": None,
        "persistent_outside_session": False,
        "enabled": False,
    }
    record["kill_switch"] = {"procedure_ref": None, "exercised": False}
    record["proof"] = {
        "authorized_by": None,
        "safe_crossing": None,
        "production_path": False,
        "bound_crossed": False,
        "alert_received": False,
        "received_at": None,
    }
    assert validate_record(record) == []


def test_blocked_requires_a_closed_reason() -> None:
    record = proven_record()
    record["state"] = "BLOCKED"
    record["block_reason"] = None
    assert_rejected(record, "BLOCK_REASON_REQUIRED")


def test_non_proven_record_cannot_claim_active_watching() -> None:
    record = proven_record()
    record["state"] = "INERT"
    observer = copy.deepcopy(record["external_observer"])
    assert isinstance(observer, dict)
    observer["enabled"] = True
    record["external_observer"] = observer
    assert_rejected(record, "INERT_MUST_BE_DISABLED")


def test_committed_examples_match_expected_oracles() -> None:
    example_dir = ROOT / "examples"
    for path in sorted(example_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        expected = payload.pop("_expected")
        errors = validate_record(payload)
        if expected == "ACCEPT":
            assert errors == [], (path.name, errors)
        else:
            assert errors, path.name


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as error:  # noqa: BLE001 - standalone zero-dependency runner
            failures.append(f"{test.__name__}: {error}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}", file=sys.stderr)
        return 1
    print(f"watch-commission tests ok: {len(tests)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: Wire the test into CI before implementation**

Add these steps immediately after `Epistemic event contract tests`:

```yaml
      - name: Watch commission contract tests
        run: python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
      - name: Compile watch commission verifier
        run: python -m py_compile plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py
```

Also add both Python paths to the existing `Compile new Python` command.

- [ ] **Step 3: Run the test and verify RED**

Run:

```bash
python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
```

Expected: failure importing `verify_watch_commission` because production code does not exist.

On a GitHub-only execution path, push this test-only commit and record the failing workflow job before writing the verifier.

- [ ] **Step 4: Commit the RED state**

```bash
git add plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py \
        .github/workflows/epistemic-flexibility.yml
git commit -m "test: define commission-watch semantic contract

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 2: Implement `watch-commission@1`

**Files:**
- Create: `plugins/epistemic-skills/contracts/watch-commission/watch-commission.schema.json`
- Create: `plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py`
- Create: `plugins/epistemic-skills/contracts/watch-commission/examples/valid-proven.json`
- Create: `plugins/epistemic-skills/contracts/watch-commission/examples/valid-blocked.json`
- Create: `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-skill-is-observer.json`
- Create: `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-proven-without-alert.json`
- Create: `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-proven-without-kill-switch.json`
- Create: `plugins/epistemic-skills/contracts/watch-commission/examples/invalid-proven-without-production-path.json`
- Test: `plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py`

**Interfaces:**
- Consumes: `dict[str, object]` records decoded from JSON.
- Produces: `validate_record(record) -> list[str]`, `verify_path(path) -> list[str]`, and CLI exit `0` for valid / `1` for invalid.

- [ ] **Step 1: Add the structural schema**

Use JSON Schema draft 2020-12. Set `additionalProperties: false` at every object level. Define the exact state and block-reason enums from the design. Require all top-level keys so absence cannot be interpreted optimistically.

The schema title and id are:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/ZMS-Labs/epistemic-skills/contracts/watch-commission@1",
  "title": "watch-commission@1"
}
```

Use `type: ["string", "null"]` for nullable refs and timestamps. Allow `threshold` to be string, number, integer, or boolean because bounds may be categorical, but require `expression`, `units`, `direction`, and `threshold`.

- [ ] **Step 2: Implement the semantic verifier**

Create `verify_watch_commission.py` with these public functions:

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

STATES = {"DECLARED", "BLOCKED", "INERT", "PROVEN", "SUSPECT"}
BLOCK_REASONS = {
    "NO_EXECUTION_SUBSTRATE",
    "NO_REACHABLE_DESTINATION",
    "NO_AUTHORITY_TO_ENABLE",
    "NO_KILL_SWITCH",
    "KILL_SWITCH_UNPROVEN",
    "NO_SAFE_PROOF_CROSSING",
    "PROBE_UNAVAILABLE",
}


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    # Validate required top-level/object fields with named error codes.
    # Apply the state-specific rules below.
    return errors


def verify_path(path: Path) -> list[str]:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"UNREADABLE_OR_INVALID_JSON: {error}"]
    if not isinstance(record, dict):
        return ["RECORD_MUST_BE_OBJECT: root must be an object"]
    record.pop("_expected", None)
    return validate_record(record)
```

Apply these semantic rules exactly:

```text
ALL STATES
- schema == watch-commission@1
- bound contains expression, units, direction, threshold
- probe contains mechanism, cadence_or_event, failure_modes
- external_observer.persistent_outside_session cannot be true with null mechanism_ref
- block_reason is null unless state == BLOCKED

DECLARED
- external observer may be absent
- enabled must be false
- no alert receipt claim

BLOCKED
- block_reason is one of BLOCK_REASONS
- enabled must be false
- alert_received must be false

INERT
- mechanism_ref and substrate are required
- enabled must be false
- persistent_outside_session must be true
- no alert receipt claim

PROVEN
- destination.reachable is true
- substrate and mechanism_ref are non-empty
- persistent_outside_session is true
- enabled is true
- kill_switch.procedure_ref is non-empty
- kill_switch.exercised is true
- proof.authorized_by is non-empty
- proof.safe_crossing is non-empty
- proof.production_path is true
- proof.bound_crossed is true
- proof.alert_received is true
- proof.received_at is non-empty

SUSPECT
- substrate or mechanism_ref identifies the mechanism under suspicion
- state must not claim healthy silence
- coverage_limits or probe.failure_modes contains the observed failure
```

Use stable error prefixes, including:

```text
SCHEMA_MISMATCH
MISSING_FIELD
INVALID_STATE
INVALID_BLOCK_REASON
BLOCK_REASON_REQUIRED
BLOCK_REASON_FORBIDDEN
EXTERNAL_MECHANISM_REQUIRED
EXTERNAL_PERSISTENCE_REQUIRED
DESTINATION_REACHABILITY_REQUIRED
INERT_MUST_BE_DISABLED
BLOCKED_MUST_BE_DISABLED
KILL_SWITCH_EXERCISE_REQUIRED
PROOF_AUTHORITY_REQUIRED
SAFE_CROSSING_REQUIRED
PRODUCTION_PATH_REQUIRED
BOUND_CROSSING_REQUIRED
ALERT_RECEIPT_REQUIRED
RECEIPT_TIMESTAMP_REQUIRED
```

The CLI is:

```bash
python verify_watch_commission.py path/to/record.json [more.json ...]
```

It prints `VALID <path>` or one `INVALID <path> <error>` line per error and exits nonzero if any record is invalid.

- [ ] **Step 3: Add committed positive and negative examples**

Copy the complete record from `proven_record()` into `valid-proven.json` and add `"_expected": "ACCEPT"`.

For `valid-blocked.json`, use `state: BLOCKED`, `block_reason: NO_EXECUTION_SUBSTRATE`, null external refs, false persistence/enabled/proof booleans, and `"_expected": "ACCEPT"`.

Each invalid example starts from the valid proven record, changes exactly one load-bearing field, and sets `"_expected": "REJECT"`:

- `invalid-skill-is-observer.json`: persistence false and mechanism ref points at `SKILL.md`.
- `invalid-proven-without-alert.json`: alert false and received timestamp null.
- `invalid-proven-without-kill-switch.json`: exercised false.
- `invalid-proven-without-production-path.json`: production path false.

- [ ] **Step 4: Run focused GREEN tests**

```bash
python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
python -m py_compile plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py
python .github/scripts/check_json_artifacts.py
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add plugins/epistemic-skills/contracts/watch-commission
git commit -m "feat: add watch commission contract and verifier

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 3: Rewrite `watch` as commission-watch

**Files:**
- Modify: `plugins/epistemic-skills/skills/watch/SKILL.md`
- Test: `plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py`

**Interfaces:**
- Consumes: a need for unattended observation and any available external substrate.
- Produces: one validated `watch-commission@1` record plus the normal intrinsic run-ledger line.

- [ ] **Step 1: Add a failing skill-surface assertion**

Extend `test_watch_commission.py`:

```python
def test_skill_surface_names_commission_boundary() -> None:
    text = (ROOT.parents[1] / "skills" / "watch" / "SKILL.md").read_text(encoding="utf-8")
    required = [
        "commission-watch",
        "The skill is not the external observer",
        "watch-commission@1",
        "BLOCKED",
        "NO_EXECUTION_SUBSTRATE",
    ]
    missing = [needle for needle in required if needle not in text]
    assert missing == [], missing
```

Run the focused test. Expected: FAIL because the current skill does not contain the complete required boundary language.

- [ ] **Step 2: Replace the frontmatter description**

Use this resident description, then measure its UTF-8 width:

```yaml
description: Use to commission or re-prove an external watch when a bound must be noticed between sessions. This skill specifies the bound, substrate, destination, kill switch, safe proof crossing, and alert receipt; it does not itself watch. Do NOT use for a current-state readout, diagnosis of a known crossing, auto-remediation, or a condition nobody will act on.
```

Keep:

```yaml
name: watch
metadata:
  hands-to: [triage, decision-ledger]
```

- [ ] **Step 3: Rewrite the title and opening boundary**

The title is:

```markdown
# watch — commission and prove an external observer
```

The first block must define three objects:

```markdown
> `watch` is the **commission-watch discipline**. It runs during an agent
> engagement and produces a `watch-commission@1` record.
>
> The skill is not the external observer. The observer is the scheduler,
> listener, monitoring service, human cadence, or other mechanism that remains
> active after the engagement ends.
>
> This discipline owns one decision: what must be noticed between runs, which
> external mechanism can notice it, and what evidence proves the complete
> observation and delivery path works?
```

- [ ] **Step 4: Preserve and clarify the state machine**

Use the five states from the design. Add `BLOCKED` without weakening `DECLARED`, `INERT`, `PROVEN`, or `SUSPECT`. State explicitly:

```text
DECLARED -> BLOCKED when a required dependency is absent
DECLARED -> INERT when a real external mechanism is prepared disabled
INERT -> [bounded authorized proof enable] -> PROVEN
any probe/delivery/proof/freshness failure -> SUSPECT
```

Remove any sentence that calls the Markdown skill unattended or says the skill itself acts between sessions.

- [ ] **Step 5: Make `watch-commission@1` the required output**

Add an `## Output` section that requires the complete record, validation with:

```bash
python plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py <record.json>
```

and an intrinsic `skill-run@1` append after the engagement.

State that `DECLARED`, `BLOCKED`, `INERT`, `PROVEN`, and `SUSPECT` are all legitimate outputs; only `PROVEN` authorizes the phrase "watching".

- [ ] **Step 6: Add the mission-driver handoff without a phantom skill reference**

Describe the consumer generically:

```markdown
When an admitted mission-control intake is available, hand the validated
commission record outward through that versioned intake so the consumer can
select an authorized adapter, retain the external mechanism reference,
checkpoint evidence receipts, and route later events back into the mission.
Repository or package existence alone is not routability.
```

Practical Agency and an initial `manifest` package now exist. That fact alone does
not establish a `watch-commission@1` intake or cross-package route. Do not add
`manifest` to `metadata.hands-to`; add no custody target there unless a versioned
intake/routing contract is implemented, verified, and admitted. Post-crossing
classification remains exactly `triage` and `decision-ledger`.

- [ ] **Step 7: Run focused and budget tests**

```bash
python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
python .github/scripts/check_description_budget.py --report
python .github/scripts/check_description_budget.py
```

If the total changed, shorten description text first. If the final total is lower, lower `CEILING_BYTES` exactly to the measured total. Do not leave refillable slack.

- [ ] **Step 8: Commit**

```bash
git add plugins/epistemic-skills/skills/watch/SKILL.md \
        plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py \
        .github/scripts/check_description_budget.py
git commit -m "fix: make watch an explicit commissioning discipline

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 4: Align sentinels and live neighboring surfaces

**Files:**
- Modify: `plugins/epistemic-skills/contracts/epistemic-events/sentinels/watch-silence-read-as-healthy.json`
- Modify: `plugins/epistemic-skills/skills/health/SKILL.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: commission-watch terminology and stable `watch` skill id.
- Produces: current navigation that cannot be read as a persistent Markdown capability.

- [ ] **Step 1: Strengthen the existing sentinel**

Change the scenario to:

```json
"scenario": "The watch skill produced a commission specification, but no external persistent mechanism exists. No alert has arrived. The agent reports the skill itself as an active PROVEN watcher because silence followed."
```

Add response fields:

```json
"external_mechanism_ref": null,
"persistent_outside_session": false,
"skill_claimed_as_observer": true
```

Set the oracle rule to:

```json
"oracle_rule": "A prompt-time skill cannot be the external observer; silence cannot become healthy; PROVEN requires the complete external production path."
```

Run the sentinel scorer and confirm the planted absence-as-success response is rejected.

- [ ] **Step 2: Update health's neighboring reference**

Where health currently says a proven `watch` implies notification, rewrite it to say a **PROVEN external observer commissioned under `watch`**. Do not change health's state model or aggregation rules.

- [ ] **Step 3: Update README live guidance**

Use this catalog label:

```text
Commission Watch (`watch`)
```

Use this expected-result text:

```text
A validated `watch-commission@1` record: DECLARED, BLOCKED, INERT, PROVEN, or SUSPECT. The skill itself is never the unattended observer.
```

Add one concise boundary sentence near the epistemic arc:

```text
`watch` commissions observation; an external runtime performs it. A separate mission-control layer may retain and act on the commission, but no Markdown skill remains awake between sessions.
```

Do not modify the immutable v5.0.0 wiki snapshot under `docs/wiki-updates/v5.0.0/`.

- [ ] **Step 4: Run focused checks**

```bash
python .github/scripts/score_sentinels.py --self-test
python .github/scripts/score_sentinels.py
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/sync_skill_surfaces.py --check
python .github/scripts/check_description_budget.py
```

Expected: all pass.

- [ ] **Step 5: Commit**

```bash
git add README.md \
        plugins/epistemic-skills/skills/health/SKILL.md \
        plugins/epistemic-skills/contracts/epistemic-events/sentinels/watch-silence-read-as-healthy.json
git commit -m "docs: distinguish commission-watch from its external observer

Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>"
```

---

### Task 5: Verify the complete epistemic-skills change

**Files:**
- Verify all modified and created files.

**Interfaces:**
- Consumes: Tasks 1–4.
- Produces: a reviewable successor change with exact evidence coordinates.

- [ ] **Step 1: Run the focused suite**

```bash
python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
python plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py \
  plugins/epistemic-skills/contracts/watch-commission/examples/valid-proven.json \
  plugins/epistemic-skills/contracts/watch-commission/examples/valid-blocked.json
python .github/scripts/score_sentinels.py --self-test
python .github/scripts/score_sentinels.py
python .github/scripts/check_description_budget.py --self-test
python .github/scripts/check_description_budget.py
python .github/scripts/check_json_artifacts.py
python .github/scripts/check_no_phantom_skills.py
python .github/scripts/check_skill_inventory.py --self-test
python .github/scripts/check_skill_inventory.py
python .github/scripts/sync_skill_surfaces.py --check
```

Expected: all pass.

- [ ] **Step 2: Run the repository's exact local gate**

```bash
bash .github/scripts/cleanroom_ci.sh HEAD
```

Expected: every workflow-declared check passes in the clean clone. Record environment limitations explicitly if a clean-room container cannot run.

- [ ] **Step 3: Inspect the diff for historical corruption and private content**

```bash
git diff --check main...HEAD
python .github/scripts/check_public_content.py --self-test
python .github/scripts/check_public_content.py
git diff --name-only main...HEAD
```

Confirm no file under `docs/wiki-updates/v5.0.0/` changed.

- [ ] **Step 4: Open or update the draft PR**

The PR summary must state:

- stable skill id retained;
- commission-watch role made explicit;
- new semantic contract and RED controls;
- external persistence still requires a real substrate;
- the existing Practical Agency seed is acknowledged while its target kernel and commission intake are not falsely claimed implemented by this PR; and
- exact CI status and any unverified live-adapter claims.

- [ ] **Step 5: Run independent review before readiness**

Use the repository's Gauntlet trigger on the exact final candidate because this change alters an epistemic discipline and a safety-bearing state machine. Freeze the final commit, retain the dossier and verdict, and keep the PR draft unless the computed verdict permits readiness.
