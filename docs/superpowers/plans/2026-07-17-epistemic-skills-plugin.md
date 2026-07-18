# Epistemic Skills Plugin Integration — plan (completed)

> **Status: completed 2026-07-17.** This plan is retained as a historical record.
> Current packaging truth: [2026-07-17-epistemic-skills-plugin-design.md](../specs/2026-07-17-epistemic-skills-plugin-design.md) and the root [README.md](../../../README.md).

**Goal:** Make the repository installable as a Gemini extension, Antigravity plugin, and Cursor plugin while keeping the nested `plugins/epistemic-skills/` layout.

**Shipped outcome (v2.3.1; initial cross-harness package was v2.3.0):**

| Task | Result |
|---|---|
| Gemini `gemini-extension.json` + `GEMINI.md` | Done; `gemini extensions validate` passes |
| Root `skills/` + `agents/` symlinks | Done (git symlinks → nested tree) |
| Cursor `.cursor-plugin/plugin.json` + `marketplace.json` + nested plugin manifest | Done |
| Antigravity root `plugin.json` | Done; `agy plugin validate` / install OK |
| README multi-harness install | Done |
| Public Cursor Marketplace listing | Deferred — packaging ready; publisher application requires operator sign-in |

**Version note:** Early draft snippets below said `2.2.0`; current package version is **2.3.1**. License is **GPL-3.0-or-later** (see root `LICENSE`), not MIT.

---

### Task 1: Gemini Extension Manifest — [x]

- [x] `gemini-extension.json` with name, description, version, `contextFileName: GEMINI.md`
- [x] Commit

### Task 2: Cursor Plugin Manifest — [x]

- [x] `.cursor-plugin/plugin.json` with skills/agents path overrides into nested tree
- [x] `.cursor-plugin/marketplace.json` for team marketplace import
- [x] `plugins/epistemic-skills/.cursor-plugin/plugin.json`
- [x] Commit

### Task 3: Root skills/agents symlinks — [x]

- [x] `skills` → `plugins/epistemic-skills/skills`
- [x] `agents` → `plugins/epistemic-skills/agents`
- [x] Commit

### Task 4: Validate — [x]

- [x] `gemini extensions validate`
- [x] `agy plugin validate` / local install
- [x] Cursor local plugin junction + reload (skills visible; auto-trigger observed)

### Task 5: Antigravity native plugin — [x]

- [x] Root `plugin.json` per https://antigravity.google/schemas/v1/plugin.json
- [x] Documented in README
