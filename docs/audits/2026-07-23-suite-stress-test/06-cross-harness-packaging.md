# 06 — Cross-harness packaging

## Validation tiers

- **LIVE** — the named harness actually discovered/executed the package in its native runtime.
- **DETERMINISTIC** — repository scripts or static integration checks ran in a clean GitHub Actions checkout.
- **SOURCE-ONLY** — manifests/instructions were inspected, but the harness was not run.
- **NOT TESTED** — neither runtime nor a material static contract was available.

A lower tier is never reported as a higher one. GitHub Actions is deterministic repository execution, not a proxy for a proprietary agent harness.

## Seven-harness matrix

| Harness | Version / discovery surfaces at packet commit | Agent/role mapping | Validation performed | Tier | Gaps and result |
|---|---|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json`; `plugins/epistemic-skills/.claude-plugin/plugin.json`; version 2.9.1; canonical skills/agents paths. | Five Gauntlet role Markdown files are package agents; one canonical method tree. | JSON/package integration checks and version/outsource exposure ran in CI. No plugin install, discovery listing, auto-trigger, or role dispatch. | **DETERMINISTIC + SOURCE-ONLY** | Metadata internally consistent; native discovery and role independence **NOT TESTED**. |
| Codex | `.agents/plugins/marketplace.json`; package `.codex-plugin/plugin.json`; version 2.9.1; `skills: "./skills/"`. | `render_codex_agents.py` bridges canonical role Markdown to user-agent TOML; materialized-role fallback is documented. | Package checks and full deterministic Gauntlet tests, including renderer behavior, passed in CI. No Codex plugin install or native isolated panel. | **DETERMINISTIC + SOURCE-ONLY** | Renderer contract tested; native registration/discovery/independence **NOT TESTED**. |
| Cursor | Root/package `.cursor-plugin/plugin.json`; root marketplace file; version 2.9.1; same canonical tree. | No copied roles; package agents remain canonical. README distinguishes local/team install from public listing. | Manifests parsed; version/outsource exposure checked. No Cursor reload, Customize → Skills enumeration, marketplace install, or auto-trigger. | **DETERMINISTIC + SOURCE-ONLY** | Source packaging coherent; public listing and live behavior **NOT TESTED**. |
| Gemini CLI | `gemini-extension.json` version 2.9.1; `GEMINI.md`; root `skills/` symlink. | Context file directs router/Helix entry while canonical skills remain in package tree. | Stale `GEMINI.md` inventory was caught RED, corrected to eleven/nine, and guarded by package integration. No extension validate/install/link/restart or auto-trigger. | **DETERMINISTIC + SOURCE-ONLY** | Static adapter defect fixed test-first; native discovery **NOT TESTED**. |
| Antigravity | Root `plugin.json` marker plus root skills/agents links; stated schema has name/description and no version field. | Reuses canonical skills/agents; no harness fork. | Root description checked for outsource exposure; source/file structure inspected. No `agy plugin validate/install` or runtime invocation. | **DETERMINISTIC + SOURCE-ONLY** | Missing version is a schema characteristic, not treated as version parity. Native behavior **NOT TESTED**. |
| Kimi Code | Root/package `.kimi-plugin/plugin.json`; version 2.9.1; canonical skills path. | `skillInstructions` maps Gauntlet lenses and UAT actor/verifier/judge to separate `Agent` calls/contexts. | Manifests parsed; version/outsource exposure asserted. No plugin install/reload, enumeration, or isolated Agent calls. | **DETERMINISTIC + SOURCE-ONLY** | Mapping explicit, actual isolation/discovery **NOT TESTED**. |
| Generic Agent Skills | `plugins/epistemic-skills/skills/<name>/SKILL.md`; root symlink; frontmatter name/description; eleven directories. | Runtime-specific primitives are contracts with labeled adapters; pure-method skills need none. | Integration enumerated eleven directories and required every `SKILL.md`; router/flexibility/contracts ran in CI. No third-party loader executed. | **DETERMINISTIC + SOURCE-ONLY** | Standard shape present; loader interoperability and trigger quality **NOT TESTED**. |

## Cross-harness invariants

| Invariant | Observation | Status |
|---|---|---|
| One canonical method tree | Manifests/links reuse `plugins/epistemic-skills/skills/`; no harness-specific SKILL fork was added. | **SOUND — source** |
| Version parity where schema supports it | Claude/Codex/Cursor/Gemini/Kimi versioned manifests declare 2.9.1; Antigravity marker has no version field. | **SOUND — deterministic/source** |
| Eleven skills exposed | Directory enumeration and corrected README/Gemini inventory agree on eleven skills/nine disciplines. | **SOUND — deterministic** |
| External handoff advertised | Versioned manifests and Antigravity description expose outsource/handoff semantics. | **SOUND — deterministic** |
| Exactly one install mechanism recommended | README warns against duplicate installation and documents shared-tree mechanisms. | **SOUND — source** |
| Role separation honestly represented | Codex renderer/materialization and Kimi mappings are documented, but no target-level independence is inferred. | **CONDITIONAL** |
| Live parity | No proprietary harness or generic loader session was available. | **OPEN / NOT TESTED** |

## Verified defects and corrections

1. **Gemini context inventory drift.** Packet source said eight packages/six disciplines. A failing assertion preceded the correction to eleven/nine.
2. **README tree inventory drift.** Layout comment said ten canonical skill cores while eleven directories exist. A failing assertion preceded the one-word correction.
3. **Canonical CI coverage gap.** Workflow omitted continuity committed-result scoring and DCO unit tests. Failing assertions preceded addition of both steps.

The source corrections are identical to the verified PR #43 GREEN blobs and are carried on a clean DCO-oriented replacement branch. No `SKILL.md` semantics or per-harness method copies changed.

## Residual risk

Static consistency cannot establish native loader behavior, auto-trigger quality, tool mapping under execution, UI reachability, provider/model independence, or role-context separation. This report is packaging source assurance plus deterministic integration—not cross-harness runtime certification.
