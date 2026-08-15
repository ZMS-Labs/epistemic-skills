# Manifest and Mission-Custody Usability Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Preserve mission custody for every repository write.

**Goal:** Produce an implementation and real-consumer evidence set that supports exact, bounded `manifest` and mission-custody usability claims without enabling N-active custody, merging, releasing, or touching production before their separate gates.

**Architecture:** Canonical custody semantics remain in `contracts/mission-custody`; packaging emits deterministic per-profile projections and digest-bound results; generated schemas define claim, authority, invalidation, fault, inventory, workload, and evidence state; native harness adapters remain declarative. The singleton stays active while four concurrency-safety prerequisites land. A separately frozen and approved successor design is required before N-active implementation.

**Tech stack:** Python 3 standard library, JSON Schema, GitHub Actions, host-native skill/plugin installers, pytest/unittest-style existing contract tests, deterministic SHA-256 artifacts.

---

## Execution and PR boundaries

- PR-A: planning contract, gauntlet record, generated-schema validators, finite support baseline, and Stage-A spike harness. This extends PR #176 only where the portable boundary already belongs.
- PR-B: lifecycle/authority safety (#149, #138, #139, #148, #154) and duplicate fail-closed regression. No packaging changes.
- PR-C: contract@2 reconstruction and evidence integrity (#118, #124, #147, #151, #164, #169, #161, #150, #166).
- PR-D: issue #173's four prerequisites only. The singleton remains enabled and N-active paths remain unreachable.
- PR-E: per-profile projections/installers and exact conformance runners after the Stage-A spike passes.
- N-active successor PRs do not exist until a frozen design, separate gauntlet GO, and explicit operator decision are present.

Every task follows RED → minimal GREEN → full relevant suite → custody receipt → commit. A commit is not publication authority.

### Task 1: Add generated planning-contract schemas and validator

**Files:**

- Create: `packaging/portability/schemas/capability-claim.schema.json`
- Create: `packaging/portability/schemas/consumer-requirements.schema.json`
- Create: `packaging/portability/schemas/support-baseline.schema.json`
- Create: `packaging/portability/schemas/planning-dag.schema.json`
- Create: `packaging/portability/schemas/harness-profile.schema.json`
- Create: `packaging/portability/schemas/evidence-invalidation-map.schema.json`
- Create: `packaging/portability/schemas/operation-fault-matrix.schema.json`
- Create: `packaging/portability/schemas/inventory-completeness.schema.json`
- Create: `packaging/portability/schemas/conformance-result.schema.json`
- Create: `.github/scripts/validate_portability_contract.py`
- Create: `.github/scripts/test_validate_portability_contract.py`

**Step 1: Write failing fixture tests.** Cover missing claim dimensions, invalid tier/capacity pairs, `unverified` rendered usable, all-unverified product success, missing required consumer, unsigned scope reduction, reversed DAG edge, absent invalidation target, missing material cut, authored-empty inventory without independent enumeration, and unavailable checker without demotion.

Run:

```bash
python .github/scripts/test_validate_portability_contract.py
```

Expected: FAIL because validator and schemas do not exist.

**Step 2: Implement the smallest schemas and one deterministic validator.** Use one closed vocabulary for claim state, capacity compatibility, success terminals, edge kinds, inventory classes, and consequences. Do not duplicate claim logic in tests or renderers.

**Step 3: Run targeted tests.**

```bash
python .github/scripts/test_validate_portability_contract.py
```

Expected: PASS with planted negative fixtures rejected.

**Step 4: Run existing packaging tests.**

```bash
python .github/scripts/test_build_portable_skill_projection.py
python .github/scripts/test_skill_artifact_lib.py
python .github/scripts/test_build_openai_bundles.py
```

Expected: PASS.

### Task 2: Freeze the authoritative support denominator and planning DAG

**Files:**

- Create: `packaging/portability/consumer-requirements.json`
- Create: `packaging/portability/support-baseline.json`
- Create: `packaging/portability/planning-dag.json`
- Create: `packaging/portability/claim-vocabulary.json`
- Create: `packaging/portability/tests/invalid/` fixture set
- Create: `packaging/portability/tests/valid/` fixture set

**Step 1:** Seed the pinned Fleet surface kinds and explicit external/publisher profiles. Mark every entry with issuer/decision record, required/applicable disposition, minimum tier, capacity policy, and reason.

**Step 2:** Encode the Stage-A → Stage-B → Stage-C DAG from the reviewed contract. Add reverse-order, omitted-consumer, hidden-failure, scope-reduction, all-unverified-success, and premature-N-active fixtures.

**Step 3:** Validate.

```bash
python .github/scripts/validate_portability_contract.py --root packaging/portability
```

Expected: valid set PASS; every planted invalid fixture rejected with a stable code.

### Task 3: Build the Stage-A portability spike runner

**Files:**

- Create: `.github/scripts/run_portability_spike.py`
- Create: `.github/scripts/test_run_portability_spike.py`
- Modify: `.github/scripts/build_portable_skill_projection.py`
- Modify: `.github/scripts/skill_artifact_lib.py`

**Step 1:** Write failing tests for exact input digest binding, dependent-edge closure, stale epoch, source-checkout leakage, undeclared dependency, changed generator/transform, and reuse of spike evidence as exact conformance.

**Step 2:** Implement `stage-a-portability-spike@1` generation. Output only `proceed`, `pivot`, or `narrow`; bind source/IR/generator/transform/projection/profile/host/installer/installed/consumer digests and affected DAG edges.

**Step 3:** Run:

```bash
python .github/scripts/test_run_portability_spike.py
python .github/scripts/test_build_portable_skill_projection.py
```

Expected: PASS; stale and omitted-edge fixtures fail closed.

**Step 4:** Run the spike in disposable homes for Claude Code CLI plugin and Codex CLI project/user discovery if the native executables are available. If unavailable, record `unverified`; do not substitute archive shape for discovery.

### Task 4: Fix lifecycle and authority invariants test-first

**Files:**

- Modify: `plugins/epistemic-skills/contracts/mission-custody/custody_mission.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/custody_cli.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/custody_gate.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/mission-manifest.schema.json`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/test_custody_mission.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py`

**Step 1:** Invert the unsafe tests: draft effect denies; duplicate active state blocks rather than allow/inert; verification audit is non-mutating; empty cancellation reason denies; actual performing actor is recorded and cannot self-accept.

**Step 2:** Run targeted tests and confirm RED against current behavior.

```bash
python plugins/epistemic-skills/contracts/mission-custody/test_custody_mission.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_gate.py
python plugins/epistemic-skills/contracts/mission-custody/test_custody_cli.py
```

**Step 3:** Implement minimal lifecycle changes. Keep the singleton. Duplicate ambiguity must deny protected work and expose deterministic recovery/inspection; do not add N-active service.

**Step 4:** Run all seven custody scripts.

```bash
for test in plugins/epistemic-skills/contracts/mission-custody/test_*.py; do python "$test"; done
```

Expected: PASS, including planted legacy behavior that now goes RED.

### Task 5: Reconstruct contract@2 integrity on current main

**Files:**

- Modify: `plugins/epistemic-skills/contracts/mission-custody/checkpoint.schema.json`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/receipt.schema.json`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/acceptance-verdict.schema.json`
- Create: `plugins/epistemic-skills/contracts/mission-custody/custody_anchor.py`
- Create: `plugins/epistemic-skills/contracts/mission-custody/test_custody_anchor.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/custody_store.py`
- Modify: `plugins/epistemic-skills/contracts/mission-custody/verify_mission_custody.py`
- Modify: relevant examples and README

**Step 1:** Port design concepts, not commits, from `agent/contract2-impl`: chained receipt/verdict hashes, external tail anchor, version-aware degraded readers, pre-write migration checks, rollback, and anchor-repair refusal.

**Step 2:** Add mutation corpus: duplicate, reorder, truncate, splice, relocate, symlink, hard-link, resolved-path alias removal, partial parent creation, anchor loss, and stale-reader fixtures.

**Step 3:** Require untouched traces valid and every mutated trace rejected or explicitly invalidated. Benchmark the declared 800-receipt close path and enforce the finite deadline/admission rule.

### Task 6: Implement authority-equivalence, scope, and typed residuals

**Files:**

- Create: `plugins/epistemic-skills/contracts/mission-custody/principal.schema.json`
- Create: `plugins/epistemic-skills/contracts/mission-custody/residual-disposition.schema.json`
- Modify: mission, verdict, CLI, and acceptance code/tests

**Step 1:** Model actual principal and equivalence identity across delegated, recovered, shared, service, and impersonation-capable credentials.

**Step 2:** Add typed `{path, kind}` acknowledgements, resolved scope comparisons, uncompared-entry disclosure, enforceable effect conditions, and residual records that cannot waive tier invariants.

**Step 3:** Seed dual-controller, self-accept, out-of-scope, symlink, silent export, revoked-session, reinstall, and logical-alias fixtures.

### Task 7: Land issue #173 prerequisites without enabling concurrency

**Files:**

- Modify: `custody_mission.py`, `custody_gate.py`, schemas, README, and targeted tests
- Create: `plugins/epistemic-skills/contracts/mission-custody/CHARTER.schema.json` if absent

**Step 1:** Cross-mission drift suppression must precede any `load_all` path.

**Step 2:** Bound regex cost during validation with planted catastrophic patterns.

**Step 3:** Ship fail-open inversion and duplicate-resolution verbs above `Mission.load` atomically.

**Step 4:** Read and conjoin the root CHARTER; refuse unmigrated stores.

**Step 5:** Prove with two injected active records that protected actions block, neighboring controls follow the singleton policy, recovery is non-destructive, and no N-active operation is reachable.

Expected completion: prerequisite evidence only. Stop before N-active design or implementation.

### Task 8: Implement harness profiles, installers, and exact conformance

**Files:**

- Create one profile record per registered candidate host under `packaging/portability/profiles/`
- Create deterministic installer modules under `packaging/portability/installers/`
- Create `.github/scripts/run_exact_conformance.py` and tests

Each profile binds native root/discovery/reload, resource resolution, consent/trust, hook event/schema/CWD/output/failure, subagent visibility, exclusions, official source/date, installer behavior, and evidence retention. Exact conformance uses a fresh epoch and source-checkout-isolated installed bytes.

For U4, derive policy coverage from the exact hook config; test every claimed matcher/actuator/exclusion/interaction or emit a route-specific claim. Probe timeout/crash/malformed output, shared dependencies, timebase faults, workload boundaries, duplicates, upgrade/rollback/uninstall, inventory omissions, public-artifact/secret controls, replay, offboarding, and privileged read/export as applicable.

### Task 9: Fleet consumer UAT and independent acceptance

**Files:**

- Create digest-bound Fleet handoff/conformance artifacts under `outputs/`
- Add consumer-side UAT instructions and result schema

Fleet owns rollout state, not canonical procedures. UAT observes the deployed consumer and must not infer capability from reachability or repository YAML. A non-implementing acceptor reviews exact-head CI, served bytes, issue ledger, mutation corpus, conformance results, privacy, rollback/uninstall, and claim rendering.

### Task 10: Promotion decision — stop and ask

When and only when exact bounded claims pass all applicable gates, report:

- exact claim keys and achieved tiers;
- unsupported/unverified profiles;
- remaining residuals and their typed authority;
- exact-head CI/review state;
- independent acceptance; and
- observed rollback/uninstall state.

Then stop. Merge, release, publication, production installation, and N-active operation require their separate operator decisions and are not executed by this plan.
