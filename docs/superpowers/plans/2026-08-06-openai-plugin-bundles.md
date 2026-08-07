# Dynamic OpenAI Bundles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate current, deterministic ChatGPT and OpenAI plugin bundles from the canonical epistemic-skills package with no hand-maintained skill list.

**Architecture:** A stdlib Python builder discovers canonical skill directories, validates existing source-linked manifests, generates an index, and writes two deterministic archives. A dedicated workflow tests and rebuilds those archives on every relevant repository revision.

**Tech Stack:** Python 3.12 stdlib, `unittest`, ZIP, JSON, GitHub Actions.

## Global Constraints

- `plugins/epistemic-skills/` is the only canonical runtime package.
- Direct `skills/<name>/SKILL.md` children define the inventory.
- Do not commit generated ZIP files.
- Fail closed on malformed inputs, source-path drift, or non-portable symlinks.
- Every PR commit carries an author-matching DCO signoff.

---

### Task 1: Define the dynamic bundle contract

**Files:**
- Create: `docs/superpowers/specs/2026-08-06-openai-plugin-bundles-design.md`
- Create: `packaging/openai/chatgpt-skill/SKILL.md`

**Interfaces:**
- Consumes: canonical skill frontmatter and existing package layout.
- Produces: a wrapper contract that reads a generated `skill-index.json` and loads `package/<canonical_path>`.

- [x] Write the approved design without enumerating current skills.
- [x] Write the ChatGPT wrapper template with explicit snapshot and degradation boundaries.
- [x] Review both files for a hidden fixed inventory or unsupported publication claim.

### Task 2: Test dynamic discovery and deterministic packaging

**Files:**
- Create: `.github/scripts/test_build_openai_bundles.py`
- Create: `.github/scripts/build_openai_bundles.py`

**Interfaces:**
- Consumes: `repo_root`, `out_dir`, and `source_revision`.
- Produces: `BuildResult(chatgpt_skill, openai_plugin, checksums, skill_count)`.

- [x] Write failing tests for inventory discovery, archive layout, determinism, YAML single-quote handling, malformed names, and marketplace drift.
- [x] Run the tests and confirm failure because the builder does not exist.
- [x] Implement the smallest stdlib builder satisfying the tests.
- [x] Run `python .github/scripts/test_build_openai_bundles.py` and confirm all tests pass.
- [x] Run `python -m py_compile` on both Python files.

### Task 3: Add continuous revision-bound generation

**Files:**
- Create: `.github/workflows/openai-bundles.yml`

**Interfaces:**
- Consumes: the exact checked-out PR, `main`, release, or manually dispatched revision.
- Produces: one Actions artifact containing both bundles and `SHA256SUMS`.

- [x] Trigger on every path that can change package bytes or packaging behavior.
- [x] Pin checkout, setup-python, and upload-artifact actions to immutable commits.
- [x] Run unit tests, live-package validation, build, and artifact upload in order.
- [x] Keep permissions read-only.

### Task 4: Document installation and refresh boundaries

**Files:**
- Create: `docs/CHATGPT-AND-OPENAI-PACKAGING.md`

**Interfaces:**
- Consumes: generated archives and current OpenAI Skills/Plugins product behavior.
- Produces: maintainer commands and an honest operator installation path.

- [x] Document Personal Skill upload as the immediate snapshot route.
- [x] Document marketplace/plugin refresh as the durable source-linked route.
- [x] State that public directory publication remains an OpenAI control-plane action.
- [x] Record local validation commands.

### Task 5: Publish for review

**Files:**
- Modify append-only: `plugins/epistemic-skills/skills/metacognate/runs/ledger.jsonl`

**Interfaces:**
- Consumes: verified branch diff and DCO identity.
- Produces: a signed commit and draft PR against `main`.

- [ ] Append the bounded metacognate engagement record.
- [ ] Commit all files with `Signed-off-by: SternOne <89846440+SternOne@users.noreply.github.com>`.
- [ ] Open a draft PR with validation evidence and explicit platform boundaries.
- [ ] Inspect the resulting PR diff and CI state; correct any deterministic failure.
