# Supported-harness verification matrix — successor corrective branch

**Subject:** `cursor/v5-post-release-104-105-4cee` at the commit that contains this
file (record the exact SHA in the Gauntlet run that freezes the candidate).

**Purpose:** discharge issue #104 item 7's harness-evidence row with honest tiers.
A tier records what was actually exercised. It does not upgrade a blocked live
check into a pass.

## Tier vocabulary

| Tier | Meaning |
|---|---|
| `LIVE` | Harness loaded the packaged skills from this candidate and the inventory matched |
| `DETERMINISTIC` | Repository CI / stdlib checks prove the packaging surface and contracts |
| `STRUCTURAL` | Manifest/path/layout inspected; load behavior not exercised |
| `LIVE_BLOCKED_EXTERNAL` | Live harness unavailable in this environment; limitation named |

## Matrix

| Harness | Install source on candidate | Reload / cache behavior | Duplicate-install risk | Verification tier | Evidence |
|---|---|---|---|---|---|
| Claude Code | Local marketplace from tagged/branch checkout (`.claude-plugin/marketplace.json`) | Fresh task required after install; descriptions session-bound | Native marketplace **or** `~/.claude/skills` copy — never both | `DETERMINISTIC` + `LIVE_BLOCKED_EXTERNAL` | Marketplace member list points at `metacognate` and fourteen skills; phantom/inventory/description-budget/public-content gates green on candidate. Live load not exercised in this cloud agent. |
| Codex | Tagged/branch plugin marketplace (`plugins/epistemic-skills/.codex-plugin/plugin.json`) | New task after render; Gauntlet roles via renderer | Do not also generic-install | `DETERMINISTIC` + `LIVE_BLOCKED_EXTERNAL` | Manifest description uses entry-point phrasing; sync counts agree. Live Codex load blocked. |
| Cursor | Tagged/branch plugin (`.cursor-plugin/`) | Reload Window; verify Customize → Skills | Do not also install into `~/.cursor/skills/` | `DETERMINISTIC` + `STRUCTURAL` | This Cursor cloud agent consumed the candidate tree; packaging files present; full live skill-panel inventory capture not available → use `check_loaded_descriptions.py --capture` when an operator can dump the panel. |
| Gemini CLI | Root `gemini-extension.json` + `GEMINI.md` | Restart / validate extension | One extension tree only | `DETERMINISTIC` + `LIVE_BLOCKED_EXTERNAL` | `GEMINI.md` no longer instructs deleted seats; count phrasing synced. Live Gemini load blocked. |
| Kimi | `.kimi-plugin/plugin.json` | Per-harness reload | One install mechanism | `STRUCTURAL` + `LIVE_BLOCKED_EXTERNAL` | Manifest present and count-synced; no live Kimi session here. |
| Antigravity (`agy`) | Native local plugin **or** Gemini link **or** import — exactly one | Validate with `agy` | Combining mechanisms duplicates triggers | `STRUCTURAL` + `LIVE_BLOCKED_EXTERNAL` | Documented in README; not exercised live here. |
| Generic Agent Skills path | Symlinked `skills/` tree | Harness-specific | Must not stack on a native install | `STRUCTURAL` | Symlink/`skills` alias layout present; generic path documented. |

## Loaded-description inventory

Package-local ceiling (8230 UTF-8 bytes) is **not** estate headroom.

- Tool: `.github/scripts/check_loaded_descriptions.py`
- Without `--capture`: exits 0 and prints `LIVE_BLOCKED` (does not claim estate pass)
- With a harness dump: fails closed on missing skills or dropped/empty descriptions
- Self-test: `--self-test` plants empty and missing entries

## Known limitations (must remain visible)

1. No harness in this review environment authenticated a full live skill-panel dump
   for every supported surface.
2. Claude Code's estate-wide description budget can still drop skills when other
   packages consume the shared cap — only measurable on the operator machine.
3. Behavioral superiority remains **UNESTABLISHED** (`p=0.875` four-arm null).

## Successor release condition

A conforming successor release must either:

1. attach live capture receipts for each supported harness (or an explicit
   `LIVE_BLOCKED_EXTERNAL` tier with owner acknowledgment in the release notes); and
2. keep this matrix path immutable beside the release notes.
