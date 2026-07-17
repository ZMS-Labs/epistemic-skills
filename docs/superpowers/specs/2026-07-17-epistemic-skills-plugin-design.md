# Epistemic Skills Plugin Integration Design

Make the `epistemic-skills` repository installable as a Cursor plugin (and keep Claude/Codex packaging) while retaining the nested directory layout under `plugins/epistemic-skills/`.

## Decision (implemented)

Ship **both** Cursor discovery shapes so clone-as-plugin and team-marketplace import both work:

| Path | Role |
|---|---|
| `.cursor-plugin/plugin.json` | Whole-repo single plugin (explicit `skills`/`agents` paths into the nested tree) |
| `.cursor-plugin/marketplace.json` | Team / multi-plugin marketplace index |
| `plugins/epistemic-skills/.cursor-plugin/plugin.json` | Nested plugin manifest when marketplace resolves `./plugins/epistemic-skills` |

No root symlinks — Cursor supports explicit component paths, which avoids Windows symlink fragility.

Claude (`.claude-plugin/`) and Codex (`.agents/plugins/` + `.codex-plugin/`) keep the same nested source tree.

## Verification

1. Manifest JSON is valid; `skills/` and `agents/` resolve under `plugins/epistemic-skills/`.
2. Local install: junction/symlink `plugins/epistemic-skills` → `~/.cursor/plugins/local/epistemic-skills`, then **Developer: Reload Window**.
3. Customize → Skills lists all six: `using-epistemic-skills`, `applying-formal-rigor`, `blindspot-pass`, `evidence-research`, `evidence-locked-uat`, `gauntlet`.
4. Agents listed: `gauntlet-adversary`, `gauntlet-constructive`, `gauntlet-metatextual`, `gauntlet-generator`, `gauntlet-arbitrator`.

## Out of scope (this change)

- Gemini / Antigravity extension packaging (can follow later via `gemini-extension.json`).
- Cursor Marketplace public listing (submit at cursor.com/marketplace/publish after push).
