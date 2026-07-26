# Formal-rigor Non-Cursor Degraded Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add and execute an explicit two-provider formal-rigor evaluation protocol that can close the v3.0.0 behavioral gate with a disclosed loss of third-provider breadth.

**Architecture:** Preserve the original frozen three-provider mapping as the runner default and add a named `noncursor-degraded-v1` allocation selected explicitly at the CLI. Allocation helpers, call records, and summaries carry the protocol identity; a new immutable root runs the unchanged 286 arm and 132 semantic tasks using Codex and agy/Gemini only.

**Tech Stack:** Python 3.12 standard library, unittest-style script assertions, Codex CLI, agy CLI, Git/GitHub Actions.

## Global Constraints

- Preserve every historical Cursor root and content pin; never repair, overwrite, relabel, or credit it.
- Change no fixture, ground truth, scorer, threshold, candidate skill, or formal module content during this protocol amendment.
- The new protocol has exactly 286 arm calls and 132 independently isolated semantic calls.
- A recorded `call.json` is terminal and is never retried.
- The passing claim is two-provider blinded conformance only, not three-provider robustness or Cursor reliability.
- All campaign source commits must be signed, pushed, clean, and recorded before calls begin.

---

### Task 1: Named provider-plan allocation and provenance

**Files:**
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_live_runner.py`
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/run_live.py`

**Interfaces:**
- Consumes: existing `ArmTask`, `SemanticTask`, `full_arm_plan()`, `full_semantic_plan()`, call-record and summary writers.
- Produces: `PROVIDER_PLANS`, `candidate_harness(repetition, provider_plan)`, `arm_harness(task, provider_plan)`, and `semantic_harness(task, provider_plan)` with explicit plan identity.

- [ ] **Step 1: Write failing allocation tests**

Add assertions equivalent to:

```python
degraded = "noncursor-degraded-v1"
assert [runner.candidate_harness(i, degraded) for i in (1, 2, 3)] == ["codex", "agy", "codex"]
assert {runner.arm_harness(task, degraded) for task in runner.full_arm_plan()} == {"codex", "agy"}
assert {runner.semantic_harness(task, degraded) for task in runner.full_semantic_plan()} == {"codex", "agy"}
for task in runner.full_semantic_plan():
    assert runner.semantic_harness(task, degraded) != runner.candidate_harness(task.repetition, degraded)
assert runner.candidate_harness(3, "frozen-three-provider") == "cursor"
```

Also assert exact degraded arm counts `{"codex": 154, "agy": 132}` and semantic counts `{"codex": 44, "agy": 88}`.

- [ ] **Step 2: Run the test and verify RED**

Run:

```text
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_live_runner.py
```

Expected: failure because the allocation helpers do not accept a provider plan and `noncursor-degraded-v1` is undefined.

- [ ] **Step 3: Implement the minimal allocation map**

Use immutable mappings equivalent to:

```python
DEFAULT_PROVIDER_PLAN = "frozen-three-provider"
PROVIDER_PLANS = {
    "frozen-three-provider": {
        "candidate": {1: "codex", 2: "agy", 3: "cursor"},
        "parodies": PARODY_HARNESSES,
        "semantic": {
            1: {"a": "agy", "b": "cursor"},
            2: {"a": "cursor", "b": "codex"},
            3: {"a": "codex", "b": "agy"},
        },
    },
    "noncursor-degraded-v1": {
        "candidate": {1: "codex", 2: "agy", 3: "codex"},
        "parodies": {
            "parody-always-cautious": "codex",
            "parody-always-decide": "agy",
            "parody-closed-taxonomy": "codex",
            "parody-formal-only": "codex",
            "parody-full-ceremony": "agy",
            "parody-jargon-only": "agy",
        },
        "semantic": {
            1: {"a": "agy", "b": "agy"},
            2: {"a": "codex", "b": "codex"},
            3: {"a": "agy", "b": "agy"},
        },
    },
}
```

Thread `provider_plan` through arm and semantic execution, include it in every `call.json` and run summary, and add `--provider-plan` with choices from `PROVIDER_PLANS` to `plan`, `run-arms`, and `run-semantic`. Default only the read-only `plan` command; require an explicit value for both live commands so a live epoch cannot silently choose a protocol.

- [ ] **Step 4: Add output-root conflict tests and implementation**

Before the first call, write `campaign-plan.json` containing the schema marker, provider plan, source commit, v1 commit, models, and exact task counts. If the file already exists, require byte-equivalent identity fields; otherwise raise before executing a call. Tests create a temporary root, verify idempotent reuse with the same identity, and verify a different plan or source commit fails closed.

- [ ] **Step 5: Verify GREEN and regression safety**

Run the live-runner test, structural scorer self-test, focused test, and `python run_live.py plan --provider-plan noncursor-degraded-v1`. Expected: all tests pass; plan output reports 286 arms, 132 semantics, and zero Cursor calls.

- [ ] **Step 6: Commit the tested runner change**

```text
git add plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/run_live.py plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_live_runner.py
git commit -s -m "feat: add degraded non-Cursor evaluation plan"
```

### Task 2: Prospective protocol and release-contract amendment

**Files:**
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/README.md`
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/results/BLOCKED.md`
- Modify: `docs/release/RELEASE-3.0.0.md`
- Modify: `RELEASING.md`

**Interfaces:**
- Consumes: protocol identity and allocations from Task 1; immutable Cursor coordinates already recorded in `RESULTS.md`.
- Produces: the prospective release rule under which the new epoch can count and the known limitation that survives release.

- [ ] **Step 1: Amend documentation before any live output exists**

Document `noncursor-degraded-v1`, its exact allocation, unchanged gates, 418 fresh-call size, no-retry rule, and two-provider claim boundary. Keep the original frozen allocation in place as historical protocol identity.

- [ ] **Step 2: Change the Cursor block's closure condition prospectively**

Append an operator-authorized protocol-amendment section: the Cursor capability block remains true, but it no longer blocks publication if a fully passing, content-pinned `noncursor-degraded-v1` epoch exists. State that a partial, repaired, or mixed-protocol root never qualifies.

- [ ] **Step 3: Amend the release gate and known limitation**

Require the unchanged structural and semantic acceptance gates under the named two-provider plan. State that Cursor was attempted and failed its structured-output transport contract, is excluded from the qualifying battery, and is a future targeted evidence gap.

- [ ] **Step 4: Check and commit the prospective contract**

Run `git diff --check`, the outsource/package integration test, and committed JSON check. Commit and push before any amended-epoch model call:

```text
git add RELEASING.md docs/release/RELEASE-3.0.0.md plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/README.md plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/results/BLOCKED.md
git commit -s -m "docs: preregister degraded formal evaluation"
```

### Task 3: Fresh degraded campaign and evidence closure

**Files:**
- Create outside Git: `C:\tmp\formal-rigor-noncursor-$($source.Substring(0,7))\`
- Modify after terminal success: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/results/RESULTS.md`
- Modify after terminal success: `docs/release/RELEASE-3.0.0.md`

**Interfaces:**
- Consumes: clean pushed source commit from Tasks 1-2 and the `noncursor-degraded-v1` runner mode.
- Produces: immutable arm/semantic evidence root, structural scores, semantic summary, content pin, and release-gate status.

- [ ] **Step 1: Verify the source boundary**

Require a clean worktree, local HEAD equal to the remote branch head, signed commits, and all deterministic tests passing. Record the source SHA before creating the output root.

- [ ] **Step 2: Run all arms from a new root**

```text
$source = git rev-parse HEAD
$root = "C:\tmp\formal-rigor-noncursor-$($source.Substring(0,7))"
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/run_live.py run-arms --provider-plan noncursor-degraded-v1 --output-root $root --workers 4 --source-commit $source
```

Stop that epoch on any terminal call failure. Do not resume or repair it.

- [ ] **Step 3: Score structural and control gates**

Materialize scores using the existing scorer. Require candidate 22/22 in all three repetitions and the preregistered baseline/parody polarity before semantic work begins.

- [ ] **Step 4: Run semantic seats**

```text
$source = git rev-parse HEAD
$root = "C:\tmp\formal-rigor-noncursor-$($source.Substring(0,7))"
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/run_live.py run-semantic --provider-plan noncursor-degraded-v1 --output-root $root --workers 4 --source-commit $source
python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/run_live.py summarize-semantic --provider-plan noncursor-degraded-v1 --output-root $root
```

Require two terminal isolated seat reports per candidate response and the unchanged agreement/P0 rules.

- [ ] **Step 5: Pin and commit the outcome**

Hash a canonical sorted manifest of every retained file, append exact counts, failures, semantic dissent, root, source SHA, and content pin to `RESULTS.md`, and update the release note. A failed epoch is recorded as failed and excluded; a passing epoch replaces the formal blocker with the documented two-provider limitation.

- [ ] **Step 6: Run the complete release-preparation verification**

Run every `stdlib-checks` command, DCO tests, committed JSON validation, manifest/version inspection, and GitHub checks at the exact evidence commit. The final independent Helix/Gauntlet publication gate remains a separate pre-release action; no tag or GitHub Release is created by this task.

## Recorded v1 exclusion and v2 follow-on (documentation preregistration)

The completed v1 epoch at source `a18e8ba41085c7d45b126e342b3222a19e497bc6`
with root pin `11eecc3d589a88ccb19dc5117a2a0cfdd5019252f4bc5c528a98581c61efbe5a`
is excluded: 286 terminal calls, 281 qualifying, and five failures. Two raw
telemetry user-profile-path leaks (one agy and one Codex) occurred despite clean
final responses; two agy records violated the frozen schema (v1-style shape and
object `uncertainty_posture`); one agy response contained self-talk/fence plus
two identical schema-valid envelopes. No scoring, semantics, release credit,
retry, repair, resume, or reuse is authorized for this root.

The next fresh campaign is `noncursor-degraded-v2`, not a v1 rewrite. Retain
the same two-provider allocation and 286 arm/132 semantic counts, all existing
thresholds, no-retry behavior, and two-provider-only release claim. Before
execution, reject an output-adjacent neutral packet root if profile-bound. Use
direct `agy --add-dir .`; configure agy arms at medium effort, agy semantics at
high effort, and Codex at high effort. Embed the exact frozen transport schema
in every non-native-schema arm prompt; every non-native-schema semantic prompt
receives only the exact semantic transport schema, never truth or scorer
material. Record the protocol identity, canonical packet root, and execution
policy/settings in the campaign plan and every call. Frozen and v1 identities
are inspectable but non-runnable under current source and require their pinned
historical commits. Active v2 Codex and agy harnesses reject Fleet-bridge
overrides; a bridge-backed evaluation needs its own preregistered protocol
identity. A full v2 epoch passing unchanged gates is required; release remains
HOLD and the Cursor blocker remains historical.

## Completed v2 exclusion and v3 follow-on

The completed v2 epoch at source `54d3bae4fe51a69cd9cab7658d703d695073006b`,
root `C:\tmp\formal-rigor-noncursor-v2-54d3bae`, and canonical pin
`ce8c7253c8bc2a18f93a2591a4566295b9d69468a4bc7911760bc182309397b0` is
excluded: 286 terminal arms, 154 qualifying Codex calls, and 132 failed agy
calls. The AGY failure is systemic and pre-execution:
`--model gemini-3.1-pro-high conflicts with --effort=medium`. No scoring,
semantic work, release credit, retry, repair, resume, or reuse is authorized.

The next distinct protocol is `noncursor-degraded-v3`, not a v2 repair. Keep
the same allocation/counts, gates/thresholds, no-retry behavior, and
two-provider-only claim. The exact matrix is arms: Codex `gpt-5.6-sol`/high and
agy `gemini-3.6-flash-medium`/medium; semantic: Codex `gpt-5.6-sol`/high and
agy `gemini-3.1-pro-high`/high; Cursor is zero/unavailable. Before fixture
calls, record an AGY 1.1.7 version/catalog/suffix capability preflight and
receipt for those exact AGY pairings—not for every provider. Codex has no
catalog preflight; its narrow invocation-compatibility basis is V2's 154/154
qualifying calls under the same `gpt-5.6-sol`/high binding, while V2 remains
excluded. Require a fresh source/root and v3 campaign manifest; the manifest
and every call must retain the phase-specific matrix, canonical packet root,
execution policy, schema-delivery mode, and AGY receipt. Do not claim v3
success or release credit unless a full fresh epoch passes every unchanged gate;
release remains HOLD.

## Completed v3 exclusion and bounded future transport pilot

V3 is now final evidence, not a prospective success claim. Source
`693c0fb26fa4e0c4f54e63b52497783c4ce60131`, root
`C:\tmp\formal-rigor-noncursor-v3-693c0fb`, and canonical pin
`87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1` recorded
286 terminal arms, with 204 qualifying calls: Codex 154/154 and AGY 50/132.
AGY has 82 invalid calls: eleven completed nonparseable raw outputs, four
AGY-internal roughly-302-second timeouts, and 67 quota failures. Each of the
eleven raw outputs contains only duplicate valid JSON frames rather than one
final object: eight have two byte-identical frames, two have three, and one has
five; none diverges. They fail the frozen fail-closed transport rule.

The entire root is excluded: do not score it structurally, run semantic
adjudication, or grant release credit; do not retry, repair, resume, or reuse
any terminal call. Release remains HOLD, and Cursor remains zero/unavailable.

After quota reset, a new separately preregistered bounded AGY transport pilot
may test AGY 1.1.7 with the exact phase models, `--output-format json`,
`--print-timeout 10m`, and runner `--timeout-seconds 720`. The explicit
720-second outer timeout exceeds the 600-second internal wait to avoid an
outer-kill race and preserve terminal evidence. The pilot retains
byte-preserving raw evidence and fail-closed one-final-object criteria. Only a
passing pilot may justify a fresh V4/full root; it cannot rehabilitate V3. The
Fleet Gemini bridge is unsuitable because
it ignores selected model/effort and likely shares quota; Ollama `qwen2.5` 7B
is exploratory only and cannot substitute for release evidence.
