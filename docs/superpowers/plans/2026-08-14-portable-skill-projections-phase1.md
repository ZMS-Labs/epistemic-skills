# Portable Skill Projections Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local-only, deterministic, procedure-free `zms-skill-ir@1` and one canonical-layout suite projection while refusing package-bound `manifest` standalone output.

**Architecture:** Extract the existing OpenAI builder's filesystem discovery, frontmatter, regular-file, hash, canonical-JSON and deterministic-copy primitives into a shared stdlib module. A new portable builder combines that filesystem inventory with sparse exception metadata, writes typed IR, copies the complete canonical package into a staged local projection, and emits structural-only digest evidence. It never creates a ZIP, executes skill code, installs into a host, uses the network, or emits a release/runtime tier.

**Tech Stack:** Python 3 standard library, `unittest`, JSON, `pathlib`, `hashlib`, local Git CLI only for source labeling.

## Global Constraints

- The v2 design at `docs/superpowers/specs/2026-08-14-portable-skill-projections-v2-design.md` is authoritative.
- The filesystem glob of direct `plugins/epistemic-skills/skills/<name>/SKILL.md` children is the only authored inventory.
- `packaging/portability/dependencies.json` contains defaults and exceptions, never every skill name.
- The IR and projection are generated, deterministic, one-way, procedure-free and labeled `non_release: true`.
- Phase 1 has no network, remote, installer, live-host, executable-probe, stable/release, custody, guarded or deployment path.
- `manifest` standalone generation fails with `PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER`.
- No mission-custody implementation or schema changes.
- All production behavior follows RED → GREEN → REFACTOR; no production code before the corresponding failing test is observed.

---

## File structure

- `.github/scripts/skill_artifact_lib.py` — shared validation, discovery, hashing, canonical JSON and deterministic file-copy primitives.
- `.github/scripts/build_openai_bundles.py` — imports the shared primitives; OpenAI archive behavior remains unchanged.
- `.github/scripts/test_skill_artifact_lib.py` — direct contract tests for shared discovery and tree hashing.
- `packaging/portability/dependencies.json` — sparse defaults plus the `manifest` refusal override.
- `.github/scripts/build_portable_skill_projection.py` — metadata validation, IR derivation, staged suite projection, result evidence and CLI refusal.
- `.github/scripts/test_build_portable_skill_projection.py` — fixtures and behavior/negative tests for IR, projection, metadata, determinism and boundaries.
- `docs/PORTABLE-SKILL-PROJECTIONS.md` — exact Phase-1 usage and non-claims.

### Task 1: Shared artifact primitives without OpenAI behavior change

**Files:**
- Create: `.github/scripts/skill_artifact_lib.py`
- Create: `.github/scripts/test_skill_artifact_lib.py`
- Modify: `.github/scripts/build_openai_bundles.py`
- Test: `.github/scripts/test_build_openai_bundles.py`

**Interfaces:**
- Produces: `ArtifactError`, `SkillRecord`, `canonical_json_bytes(value)`, `sha256_bytes(data)`, `parse_skill_frontmatter(path)`, `regular_files(root)`, `tree_sha256(root)`, `discover_skills(package_root)`, and `copy_regular_tree(source, destination)`.
- Preserves: `build_openai_bundles.BundleError` remains an alias of `ArtifactError`; existing callers and error names remain valid.

- [ ] **Step 1: Write the failing shared-library tests**

Add tests that import `skill_artifact_lib.py`, discover fixture skills in sorted order, reject a symlink with `SYMLINK_NOT_PORTABLE`, produce the same tree hash regardless of file creation order, emit canonical compact JSON with a final newline, and copy only regular portable files.

- [ ] **Step 2: Run the shared-library test and verify RED**

Run:

```bash
python .github/scripts/test_skill_artifact_lib.py
```

Expected: FAIL because `.github/scripts/skill_artifact_lib.py` does not exist.

- [ ] **Step 3: Implement the minimal shared library**

Move the existing pure primitives out of `build_openai_bundles.py` without changing their error strings or hash behavior. Add canonical JSON and deterministic tree copy using sorted `regular_files`; refuse an existing symlink at either source or destination.

- [ ] **Step 4: Switch the OpenAI builder to shared imports**

Load the sibling module through the normal script directory import path, alias `BundleError = ArtifactError`, and retain only OpenAI-specific constants, marketplace validation, ZIP rendering and CLI code.

- [ ] **Step 5: Verify GREEN and unchanged OpenAI behavior**

Run:

```bash
python .github/scripts/test_skill_artifact_lib.py
python .github/scripts/test_build_openai_bundles.py
```

Expected: both PASS with no warnings.

- [ ] **Step 6: Commit the shared primitive boundary**

```bash
git add .github/scripts/skill_artifact_lib.py .github/scripts/test_skill_artifact_lib.py .github/scripts/build_openai_bundles.py
git commit -m "refactor: share deterministic skill artifact primitives"
```

### Task 2: Sparse metadata and procedure-free IR

**Files:**
- Create: `packaging/portability/dependencies.json`
- Create: `.github/scripts/build_portable_skill_projection.py`
- Create: `.github/scripts/test_build_portable_skill_projection.py`

**Interfaces:**
- Consumes: Task 1 `discover_skills`, `regular_files`, `tree_sha256`, `sha256_bytes`, and `canonical_json_bytes`.
- Produces: `ProjectionError`, `load_dependency_contract(repo_root)`, `derive_ir(repo_root, source_record, profile) -> dict`, `build_projection(...) -> BuildResult`, and CLI `--standalone-skill NAME` refusal.

- [ ] **Step 1: Write RED tests for sparse metadata and IR**

Create an isolated repository fixture with `alpha`, `beta`, and `manifest`. Assert:

```python
self.assertEqual("zms-skill-ir@1", ir["schema"])
self.assertEqual(["alpha", "beta", "manifest"], [s["name"] for s in ir["skills"]])
self.assertEqual("unverified", by_name["alpha"]["standalone"]["state"])
self.assertEqual("suite_only", by_name["manifest"]["standalone"]["state"])
self.assertEqual(
    "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER",
    by_name["manifest"]["standalone"]["refusal_code"],
)
self.assertNotIn("# manifest", json.dumps(ir))
```

Add separate tests for stale override names, malformed schema, absolute/escaping/missing/symlinked dependency roots, and an override that tries to provide procedure text.

- [ ] **Step 2: Run the portable-builder tests and verify RED**

Run:

```bash
python .github/scripts/test_build_portable_skill_projection.py
```

Expected: FAIL because the portable builder does not exist.

- [ ] **Step 3: Add the sparse repository contract**

Write `dependencies.json` with:

```json
{
  "schema": "zms-skill-dependencies@1",
  "defaults": {"standalone": {"state": "unverified"}},
  "skills": {
    "manifest": {
      "dependency_roots": ["plugins/epistemic-skills/contracts/mission-custody"],
      "standalone": {
        "state": "suite_only",
        "refusal_code": "PACKAGE_BOUND_NO_APPROVED_SKILL_LOCAL_LAUNCHER"
      }
    }
  }
}
```

- [ ] **Step 4: Implement metadata validation and IR derivation**

Validate a closed key set, exact schema, string/list/object types, discovered override names, normalized repository-relative roots, absence of symlinks, and no duplicate roots. Emit per-member path/digest records, dependency-root tree digests, source/profile bindings, explicit `structural_only: true`, and `non_release: true`. Do not include source file bodies.

- [ ] **Step 5: Verify metadata/IR GREEN**

Run:

```bash
python .github/scripts/test_build_portable_skill_projection.py -k metadata
python .github/scripts/test_build_portable_skill_projection.py -k ir
```

Expected: selected tests PASS.

- [ ] **Step 6: Commit the IR contract**

```bash
git add packaging/portability/dependencies.json .github/scripts/build_portable_skill_projection.py .github/scripts/test_build_portable_skill_projection.py
git commit -m "feat: derive procedure-free portable skill IR"
```

### Task 3: Deterministic local suite projection and refusal boundary

**Files:**
- Modify: `.github/scripts/build_portable_skill_projection.py`
- Modify: `.github/scripts/test_build_portable_skill_projection.py`
- Create: `docs/PORTABLE-SKILL-PROJECTIONS.md`

**Interfaces:**
- Consumes: Task 2 IR and the fixed local Phase-1 profile.
- Produces: `PORTABILITY-IR.json`, `PROJECTION-RESULT.json`, and `projection/plugins/epistemic-skills/**` under an explicit output directory.

- [ ] **Step 1: Write RED tests for projection output**

Assert that a build preserves canonical package layout, binds IR/profile/source/served digests, writes `structural-only` and `non_release: true`, has no runtime tier key, and yields identical file bytes across two clean builds. Assert `--standalone-skill manifest` returns non-zero with the named refusal and produces no output. Assert a pre-existing foreign output directory is refused and unchanged.

- [ ] **Step 2: Run projection tests and verify RED**

Run:

```bash
python .github/scripts/test_build_portable_skill_projection.py -k projection
python .github/scripts/test_build_portable_skill_projection.py -k standalone
```

Expected: FAIL because output staging and refusal behavior are absent.

- [ ] **Step 3: Implement staged local projection**

Stage beneath the output parent, copy the canonical package using Task 1 primitives, write canonical IR/result JSON, and rename the staged directory only when the destination is absent. Do not overwrite or prune an existing destination in this slice. Source labeling accepts only explicit `--working-tree` or a full local 40-hex `--source-revision`; committed mode extracts from local Git objects into a temporary tree and never reads network state.

- [ ] **Step 4: Implement CLI and negative capability boundary**

Expose:

```bash
python .github/scripts/build_portable_skill_projection.py --working-tree --out-dir <path>
```

and a test-only/negative `--standalone-skill` request that refuses every state except a future explicitly eligible state. The current repository has no eligible standalone output path.

- [ ] **Step 5: Document exact usage and non-claims**

Document output files, source modes, determinism domain, `manifest` refusal, and the absence of archive/release/install/runtime/custody/guard claims. Include commands for the focused tests and a warning that the output is not a host package.

- [ ] **Step 6: Verify GREEN and focused regression suite**

Run:

```bash
python .github/scripts/test_build_portable_skill_projection.py
python .github/scripts/test_skill_artifact_lib.py
python .github/scripts/test_build_openai_bundles.py
python .github/scripts/check_skill_inventory.py
python .github/scripts/sync_skill_surfaces.py --check
git diff --check
```

Expected: all commands PASS; working tree contains only planned files.

- [ ] **Step 7: Run a real local smoke build outside the repository**

Run:

```bash
phase1_out="$(mktemp -d)/portable-phase1"
python .github/scripts/build_portable_skill_projection.py --working-tree --out-dir "$phase1_out"
python -m json.tool "$phase1_out/PORTABILITY-IR.json" >/dev/null
python -m json.tool "$phase1_out/PROJECTION-RESULT.json" >/dev/null
```

Expected: success, `non_release: true`, `structural_only: true`, and the projected package tree exists. Remove the temporary parent after recording the result.

- [ ] **Step 8: Commit the bounded Phase-1 slice**

```bash
git add .github/scripts/build_portable_skill_projection.py .github/scripts/test_build_portable_skill_projection.py docs/PORTABLE-SKILL-PROJECTIONS.md
git commit -m "feat: build local portable skill projection"
```

### Task 4: Completion evidence without acceptance self-certification

**Files:**
- Modify only if needed: `docs/PORTABLE-SKILL-PROJECTIONS.md`

**Interfaces:**
- Consumes: all preceding task outputs.
- Produces: a local verification report and exact commit/diff inventory; it does not certify merge acceptance.

- [ ] **Step 1: Re-run the focused suite from a clean shell**

Run the Task 3 Step 6 commands plus:

```bash
python -m compileall -q .github/scripts
git status --short
git log -4 --oneline
```

- [ ] **Step 2: Inspect the final diff and boundary strings**

Run:

```bash
git diff main...HEAD --stat
rg -n "requests|urllib|socket|subprocess.*run|custody-capable|guarded|stable|release" \
  .github/scripts/build_portable_skill_projection.py \
  packaging/portability/dependencies.json \
  docs/PORTABLE-SKILL-PROJECTIONS.md
```

Every match must be an explicit refusal/non-claim or the local Git-object extraction path. No network/imported HTTP library or runtime tier emission is allowed.

- [ ] **Step 3: Record limits in the handoff**

State explicitly that tests establish deterministic local structural projection and refusal only. Live host conformance, manifest callability/custody, remote producer authorization, executable-probe isolation, installer transactions and guarded enforcement remain unverified and unauthorized.

- [ ] **Step 4: Request independent review before merge**

Do not merge or release. Provide the exact head commit, test commands and result, changed-file list, and the v2 design path to an independent reviewer.
