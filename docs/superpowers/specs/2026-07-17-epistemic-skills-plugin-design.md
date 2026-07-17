# Epistemic Skills — packaging design (as shipped)

**Status: implemented** (plugin package **2.3.0**, 2026-07-17).

Make `ZMS-Labs/epistemic-skills` installable across Claude Code, Codex, Cursor,
Gemini CLI, and Antigravity while keeping a single nested skill tree.

## Decision (implemented)

| Path | Role |
|---|---|
| `plugins/epistemic-skills/skills/` | Canonical skill cores (six) |
| `plugins/epistemic-skills/agents/` | Gauntlet role-agents (five) |
| `skills/`, `agents/` | Root **symlinks** into the nested tree (Gemini / root scanners) |
| `.claude-plugin/marketplace.json` + nested `.claude-plugin/plugin.json` | Claude Code marketplace |
| `.agents/plugins/marketplace.json` + nested `.codex-plugin/plugin.json` | Codex marketplace |
| `.cursor-plugin/plugin.json` | Cursor whole-repo single plugin (path overrides into nested tree) |
| `.cursor-plugin/marketplace.json` + nested `.cursor-plugin/plugin.json` | Cursor team-marketplace index |
| `gemini-extension.json` + `GEMINI.md` | Gemini CLI extension |
| `plugin.json` (repo root) | Antigravity native plugin (`agy`; schema: name + description only) |

License for the repository is **GPL-3.0** ([LICENSE](../../../LICENSE)); harness
manifests that carry a `license` field should say `GPL-3.0`.

## Verification (done)

1. Manifest JSON valid; versions aligned at **2.3.0** where the format allows a version field (Antigravity root `plugin.json` does not — schema forbids extra properties).
2. `gemini extensions validate` passes; `agy plugin validate` reports 6 skills + 5 agents.
3. Cursor local install: junction `plugins/epistemic-skills` → `~/.cursor/plugins/local/epistemic-skills`, then Reload Window; skills visible and auto-trigger observed.
4. Public Cursor Marketplace listing: **not yet** — packaging ready; publisher sign-in required at cursor.com/marketplace/publish.

## Out of scope / deferred

- Official Cursor Marketplace acceptance (human publisher application + Cursor review).
- Native Antigravity marketplace catalog (agy has no curated catalog equivalent yet; GitHub/`agy plugin install` is the distribution path).
