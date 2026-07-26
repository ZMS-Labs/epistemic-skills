# Formal-rigor V3 Post-hoc Diagnostic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and execute a non-promotable diagnostic that structurally scores all 215 recoverable V3 arm responses and obtains two blinded semantic judgments for each of 65 recoverable candidate responses.

**Architecture:** Add one diagnostic-only CLI beside the frozen scorer and live runner. It reads the excluded V3 root, creates hash-bound response views in a separate root, reuses pure scorer/packet/rubric helpers, dispatches diagnostic-specific at-most-once semantic calls, and emits conditional plus full-population reports without writing any production campaign filename.

**Tech Stack:** Python 3 standard library, existing `score.py` and pure helpers from `run_live.py`, Codex CLI 0.144.6, AGY 1.1.7, SHA-256 tree pins, standalone stdlib tests, GitHub Actions.

## Global Constraints

- The source root is `C:\tmp\formal-rigor-noncursor-v3-693c0fb` at pin `87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1` and source commit `693c0fb26fa4e0c4f54e63b52497783c4ce60131`.
- The source root is read-only; recompute the exact tree pin before and after the diagnostic.
- The population is 286 planned, 204 originally qualifying, 11 recoverable identical-frame responses, 71 no-content responses, and 215 structurally scorable responses.
- The candidate population is 65 of 66: run 1 has 22, run 2 has 21, and run 3 has 22.
- Semantic allocation is exactly 42 Codex `gpt-5.6-sol`/high calls and 88 AGY `gemini-3.1-pro-high`/high calls, two isolated seats per available candidate.
- AGY uses `--output-format json --print-timeout 10m`; the subprocess timeout is 720 seconds.
- Every diagnostic call is at-most-once: `call.json` presence is terminal and never retried in the same diagnostic identity.
- The diagnostic always records `post_hoc: true`, `source_epoch_excluded: true`, `release_eligible: false`, and `release_credit: "none"`.
- Never create `arm-run-status.json`, `campaign-plan.json`, `semantic-summary.json`, or any file beneath the V3 root.
- The existing `verify_arm_phase_complete`, `call_qualifies`, structural scorer, semantic prompt, semantic rubric, schemas, and release gates remain unchanged.
- Missingness is non-random; the three absent AGY parody arms remain unobserved and are never imputed.

---

### Task 1: Diagnostic source inventory and structural views

**Files:**
- Create: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/posthoc_diagnostic.py`
- Create: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py`

**Interfaces:**
- Consumes: V3 `campaign-plan.json`, per-call evidence directories, `score.load_inventory()`, `score.score_fixture()`, `run_live.validate_json_schema()`, and the frozen transport schema.
- Produces: `tree_sha256(root: Path) -> str`, `extract_identical_frames(raw: bytes, fixture: str, schema: dict) -> tuple[bytes, dict]`, `inventory_source_calls(source_root: Path, expected_pin: str) -> list[dict]`, `prepare_structural(source_root: Path, output_root: Path, expected_pin: str, source_commit: str) -> dict`, `diagnostic-manifest.json`, `arm-inventory.json`, response views, per-response structural scores, and `structural-report.json`.

- [ ] **Step 1: Write the failing extraction, safety, and provenance tests**

Create a standalone test that imports the diagnostic module with
`importlib.util`, builds synthetic call directories in `tempfile.TemporaryDirectory`,
and asserts these concrete cases:

```python
view, meta = diagnostic.extract_identical_frames(
    canonical_frame + b"\n" + canonical_frame,
    "tm-01-false-mvd",
    transport_schema,
)
require(view == canonical_frame, "two identical frames changed bytes")
require(meta["frame_count"] == 2, "frame count was not retained")
require(meta["normalization"] == "normalized_identical_repeated_frames",
        "normalization identity drifted")

for rejected in (
    canonical_frame + b" " + semantically_equal_different_bytes,
    canonical_frame + b"\n" + divergent_frame,
    b"prefix" + canonical_frame,
    canonical_frame + b"suffix",
    wrong_fixture_frame + b"\n" + wrong_fixture_frame,
    wrong_marker_frame + b"\n" + wrong_marker_frame,
):
    require_raises(ValueError, diagnostic.extract_identical_frames,
                   rejected, "tm-01-false-mvd", transport_schema)
```

Also assert that output roots nested inside the source, nonempty new roots,
response-hash mismatches, secret-screen failures, and call-identity mismatches
fail before a view is written.

- [ ] **Step 2: Run the new test and verify RED**

Run:

```powershell
python plugins\epistemic-skills\skills\applying-formal-rigor\evals\formal-rigor-v2-fixtures\tests\test_posthoc_diagnostic.py
```

Expected: nonzero because `posthoc_diagnostic.py` does not exist.

- [ ] **Step 3: Implement deterministic tree pinning and strict frame extraction**

Implement the same tree hash as
`plugins/epistemic-skills/skills/gauntlet/scripts/finalize_run.py::tree_sha256`:

```python
def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii")
        digest.update(relative + b"\0" + file_hash + b"\n")
    return digest.hexdigest()
```

Parse consecutive JSON values with `json.JSONDecoder().raw_decode`. Accept only
two or more complete values separated solely by whitespace where every exact
frame byte slice is identical, every value passes the frozen transport schema,
and `response` plus `fixture` match the expected identity. Return the first exact
frame bytes and hashes/count metadata. Reject any prefix, suffix, empty frame,
semantic-only equality, ambiguity, or identity/schema mismatch.

- [ ] **Step 4: Implement source inventory and view materialization**

Drive inventory from all 286 `campaign-plan.json.arm_tasks`. For each task,
resolve exactly:

```python
call_dir = source_root / "arms" / arm / f"run-{repetition}" / "calls" / fixture
call_path = call_dir / "call.json"
raw_path = call_dir / "response.json"
view_path = output_root / "views" / arm / f"run-{repetition}" / f"{fixture}.response.json"
```

Classify rows as `original_qualifying`,
`normalized_identical_repeated_frames`, or `missing_no_content`. Copy exact raw
bytes for qualifying views; extract one exact frame for normalized views; write
no response for missing rows. Every row records source-relative coordinate,
call/raw/view hashes, arm, repetition, fixture, origin harness/provider,
normalization proof, and exclusion reason. Reject any unrecognized fourth class.

- [ ] **Step 5: Implement structural scoring and aggregate reporting**

For every view, parse its JSON and call:

```python
truth = score.load_inventory(FIXTURES_ROOT)[row["fixture"]]
result = score.score_fixture(truth, response)
```

Write one score per row and aggregate by arm, repetition, fixture, origin
provider, priority, and fixture kind. Report conditional-on-content and
intent-to-test denominators, candidate sensitivity excluding normalized views,
candidate P0/trap/control gate components, each observed parody's intended
failure evidence, and the three unavailable parody arms. Hard-code the four
non-release fields in every top-level report.

- [ ] **Step 6: Run deterministic tests and commit Task 1**

Run the new test twice and compare emitted bytes, then run `git diff --check`.
Commit with DCO sign-off:

```powershell
git add -- plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/posthoc_diagnostic.py plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py
git commit -s -m "test: add V3 post-hoc structural diagnostic"
```

---

### Task 2: Blinded diagnostic semantic orchestration

**Files:**
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/posthoc_diagnostic.py`
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py`

**Interfaces:**
- Consumes: Task 1 view manifest, `run_live.build_adjudication_packet()`, `semantic_prompt()`, `execution_prompt()`, `codex_command()`, `codex_prompt_transport()`, `semantic_harness()`, `validate_json_schema()`, `validate_adjudication()`, and `sensitive_markers()`.
- Produces: `semantic_tasks(manifest: dict) -> list[dict]`, `agy_semantic_command(...) -> list[str]`, `extract_agy_adjudication(raw: bytes, fixture: str) -> tuple[bytes, dict]`, `run_semantic(...) -> dict`, `summarize_semantic_diagnostic(output_root: Path) -> dict`, `semantic-plan.json`, `semantic-diagnostic/**/call.json`, and `semantic-diagnostic-report.json`.

- [ ] **Step 1: Extend tests with exact seat mapping and transport contracts**

Assert the plan contains exactly these groups:

```python
require(counts == {"codex": 42, "agy": 88}, f"seat map drifted: {counts}")
require(candidate_counts == {1: 22, 2: 21, 3: 22},
        f"candidate availability drifted: {candidate_counts}")
require(all(task["judge_harness"] != task["origin_harness"] for task in tasks),
        "cross-provider judge boundary failed")
```

Assert the AGY argv contains the exact model, `high`, `--output-format json`,
`--print-timeout 10m`, and the prompt. Assert the Codex argv remains ephemeral,
read-only, user-config/rules/plugins/apps disabled, and native-schema constrained.
Assert packet manifests exclude `ground-truth.json`, priority, class, thresholds,
arm/provider identity, scorer code, other responses, and other-seat output.

- [ ] **Step 2: Add RED tests for aggregate AGY JSON extraction**

Accept a direct adjudication object or exactly one recursively contained or
string-encoded adjudication object. Record its JSON coordinate and extraction
method. Reject zero, multiple, divergent, wrong-fixture, wrong-marker, malformed,
schema-invalid, duplicate-row, and contradictory-`VALID` envelopes.

The verdict consistency rule is:

```python
if value["verdict"] == "VALID":
    require(all(row["status"] == "SATISFIED" for row in value["obligations"]),
            "VALID contains a non-satisfied obligation")
    require(not any(row["present"] for row in value["forbidden_propositions"]),
            "VALID contains a forbidden proposition")
```

Every expected obligation and forbidden proposition must occur exactly once.

- [ ] **Step 3: Implement diagnostic plan/preflight freezing**

Write `semantic-plan.json` before inference. Bind it to the implementation
commit, source coordinate and pin, manifest/view-manifest hashes, prompt/schema/
rubric hashes, all 130 ordered task identities, model/effort matrix, CLI versions,
AGY catalog receipt, command policy, and timeout policy. Reject a mismatched
existing plan or orphan `call.json`. Verify the checked-out commit is the pushed
remote branch head and DCO-signed before allowing inference.

- [ ] **Step 4: Implement isolated at-most-once call execution**

Build a fresh random packet per seat with the existing redacted packet builder.
For Codex, deliver the prompt over stdin and use native output schema plus
`--output-last-message`. For AGY, use the exact preregistered argv and cwd packet,
capture aggregate JSON stdout as raw bytes, and extract the one semantic envelope
fail closed. Use `subprocess.run(..., timeout=720, check=False)`.

Retain `stdout.bin`, `stderr.bin`, parsed `response.json` when valid, packet
manifest, timings, exit code, transport, hashes, schema/adjudication errors,
secret-screen result, exact identity, and `retry_policy: at-most-once`. Write
`call.json` last as the terminal seal and remove the temporary packet.

- [ ] **Step 5: Implement diagnostic semantic aggregation**

For each available candidate, apply the frozen rule: any `INVALID` is `FAIL`,
`VALID`/`VALID` is `PASS`, any P0 disagreement or inconclusive result is `FAIL`,
and any non-P0 unresolved disagreement is `ARBITRATION_REQUIRED`. Do not invent
an arbitration outcome. Report verdicts, validation errors, dissent, P0 findings,
origin/judge provider breakdowns, completion coverage, and the missing 66th
candidate separately from merit.

- [ ] **Step 6: Run tests and commit Task 2**

Run the diagnostic test, `test_live_runner.py`, and `git diff --check`. Confirm
`run_live.py` and `score.py` have no diff. Commit with DCO sign-off:

```powershell
git add -- plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/posthoc_diagnostic.py plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py
git commit -s -m "feat: add blinded post-hoc semantic diagnostic"
```

---

### Task 3: CI integration and pushed execution source

**Files:**
- Modify: `.github/workflows/epistemic-flexibility.yml`
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/README.md`

**Interfaces:**
- Consumes: Task 1 and Task 2 deterministic test/CLI.
- Produces: CI execution of `test_posthoc_diagnostic.py`, Python compilation of both new files, diagnostic usage/non-release documentation, and a pushed DCO-clean inference source.

- [ ] **Step 1: Add the standalone test and compilation to CI**

Add one step immediately after the live-runner isolation test:

```yaml
      - name: Formal-rigor V3 post-hoc diagnostic tests
        run: python plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py
```

Add `posthoc_diagnostic.py` and `tests/test_posthoc_diagnostic.py` to the existing
`python -m py_compile` command.

- [ ] **Step 2: Document diagnostic commands and non-release boundary**

Document the diagnostic identity, source/root pin, required empty output root,
`prepare-structural`, provider-filtered `run-semantic`, and `summarize` commands.
State that the outputs are post-hoc confidence evidence and can never make V3 or
3.0.0 pass.

- [ ] **Step 3: Run the full deterministic repository gate**

Run the same commands as `.github/workflows/epistemic-flexibility.yml`, including
the formal-rigor tests, JSON parse check, DCO policy tests, receipt verifier, UAT
judge self-test, and Gauntlet tests. Run `git diff --check` and Python compilation.

- [ ] **Step 4: Commit, push, and verify checks**

Commit with DCO sign-off, push `codex/v3-rigor-gauntlet`, verify remote HEAD
equals local HEAD, and wait for draft PR #48 checks to pass before inference.

---

### Task 4: Execute, pin, review, and report the diagnostic

**Files:**
- Generated outside Git: a new empty root under `C:\tmp`.
- Modify: `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/results/RESULTS.md`
- Modify: `docs/release/RELEASE-3.0.0.md`
- Create: a bounded committed diagnostic summary under `docs/release/evidence/` if the existing result documents cannot carry the exact tables readably.

**Interfaces:**
- Consumes: pushed Task 3 commit and immutable V3 source root.
- Produces: 215 structural scores, up to 130 terminal semantic calls, diagnostic aggregate, pre/post source pins, diagnostic tree pin, confidence interpretation, limitations, and independent review.

- [ ] **Step 1: Prepare structural evidence**

Run `prepare-structural` into a new empty diagnostic root with the exact source
coordinate, source pin, and pushed source commit. Verify exact counts
`286/204/11/71/215` and candidates `65/66`. Stop if any count differs.

- [ ] **Step 2: Run the 42 Codex semantic seats**

Run only `--harness codex` with bounded parallelism. Confirm exactly 42 terminal
call records and no AGY call records before proceeding.

- [ ] **Step 3: Run the 88 AGY semantic seats**

Run only `--harness agy` with bounded parallelism and the exact 720/600-second
outer/inner timeout pair. Do not retry a terminal failure. Preserve quota,
timeout, transport, schema, and merit outcomes as distinct classes.

- [ ] **Step 4: Summarize and pin**

Run the diagnostic summarizer, recompute the V3 tree pin and require it remains
`87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1`, then
compute the diagnostic tree pin over all retained files. Report structural
results, available control polarity, semantic outcomes, normalized-view
sensitivity, provider breakdowns, and full-population missingness.

- [ ] **Step 5: Obtain independent read-only review**

Give the reviewer the frozen design, implementation diff, diagnostic manifest,
aggregate reports, and exact root pins. Require explicit checks for source-root
mutation, normalization overreach, hidden release promotion, provider/seat
identity, rubric leakage, verdict consistency, and unsupported confidence claims.

- [ ] **Step 6: Commit and push the bounded result**

Append exact results and limitations to the existing release/result documents,
including any reviewer dissent. Commit with DCO sign-off, push to draft PR #48,
and wait for all checks. Keep the release state `HOLD` regardless of the outcome.
