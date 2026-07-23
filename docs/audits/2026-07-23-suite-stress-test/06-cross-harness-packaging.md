# 06 — Cross-harness packaging

## Validation tiers

- **LIVE** — the named harness actually discovered/executed the package in its native runtime.
- **DETERMINISTIC** — repository scripts/static integration checks ran in a clean GitHub Actions checkout.
- **SOURCE-ONLY** — manifests/instructions were inspected, but the harness was not run.
- **NOT TESTED** — neither runtime nor a material static contract was available.

A lower tier is never reported as a higher one. GitHub Actions is the deterministic execution environment for repository checks; it is not a proxy for any proprietary agent harness.

## Harness matrix

| Harness | Version / discovery surfaces at packet commit | Agent/role mapping | Validation performed | Tier | Gaps and result |
|---|---|---|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json`; `plugins/epistemic-skills/.claude-plugin/plugin.json`; version `2.9.1`; canonical `skills/` and `agents/` package paths. | Five canonical Gauntlet role Markdown files are package agents; skills remain one shared tree. | JSON parsed through package integration surfaces; version/outsource exposure asserted. No `/plugin install`, discovery listing, auto-trigger, or agent dispatch was available. | **DETERMINISTIC + SOURCE-ONLY** | Packaging metadata is internally consistent. Native discovery/runtime and role independence are **NOT TESTED**. |
| Codex | `.agents/plugins/marketplace.json`; `plugins/epistemic-skills/.codex-plugin/plugin.json`; version `2.9.1`; `skills: "./skills/"`. | Manifest does not directly register collaboration-agent types; `render_codex_agents.py` bridges canonical role Markdown into Codex user-agent TOML, with materialized-role fallback. | Package/manifest integration and full Gauntlet deterministic tests, including Codex rendering checks, passed in CI. No Codex plugin install or native role dispatch occurred. | **DETERMINISTIC + SOURCE-ONLY** | Renderer contract is tested; native discovery, rendered-agent registration, and isolated panel are **NOT TESTED**. |
| Cursor | Root and package `.cursor-plugin/plugin.json`; root `.cursor-plugin/marketplace.json`; version `2.9.1`; same canonical skills tree. | No separate role copy; package agents remain canonical. README explicitly distinguishes local/team installation from public marketplace listing. | Manifests parsed and version/outsource exposure asserted. No Cursor reload, Customize → Skills enumeration, marketplace install, or auto-trigger run. | **DETERMINISTIC + SOURCE-ONLY** | Source packaging is coherent. Public listing and live discovery remain **NOT TESTED**; no claim of public marketplace availability is made. |
| Gemini CLI | `gemini-extension.json` version `2.9.1`; `GEMINI.md`; root `skills/` symlink. | Context file directs the router/Helix entry; canonical skills remain under the package tree. | A stale `GEMINI.md` inventory (“eight packages / six disciplines”) was caught RED, corrected to eleven/nine, and guarded by integration checks. No `gemini extensions validate`, install/link, restart, or auto-trigger occurred in this target. | **DETERMINISTIC + SOURCE-ONLY** | Static adapter defect fixed with RED→GREEN. Native extension validation/discovery remains **NOT TESTED**. |
| Antigravity | Root `plugin.json` native marker plus root `skills/` and `agents/` links. The stated marker schema contains name/description and no version field. | Reuses the canonical skills/agents tree; no harness-specific method copy. | Root description was checked for outsource exposure; file structure/source inspected. No `agy plugin validate/install` or runtime invocation. | **DETERMINISTIC + SOURCE-ONLY** | Absence of a version field is a schema characteristic, not silently treated as version parity. Native validation/discovery is **NOT TESTED**. |
| Kimi Code | Root and package `.kimi-plugin/plugin.json`; version `2.9.1`; canonical skills path. | `skillInstructions` maps Gauntlet lenses and UAT actor/verifier/judge to separate `Agent` calls/contexts. | Manifests parsed and version/outsource exposure asserted. No `/plugins install`, `/reload`, skill enumeration, or isolated `Agent` calls occurred. | **DETERMINISTIC + SOURCE-ONLY** | Mapping is explicit, but actual context isolation and discovery are **NOT TESTED**. |
| Generic Agent Skills | `plugins/epistemic-skills/skills/<name>/SKILL.md`; root `skills/` symlink; frontmatter `name`/`description`; eleven directories. | Runtime-specific primitives are contracts with labeled adapters; pure-method skills have no runtime dependency. | Integration test enumerated eleven directories and required each `SKILL.md`; router/flexibility/contract suites ran in CI. No generic third-party loader was exercised. | **DETERMINISTIC + SOURCE-ONLY** | Standard file shape is present; loader interoperability and auto-trigger quality are **NOT TESTED**. |

## Cross-harness invariants checked

| Invariant | Observation | Status |
|---|---|---|
| One canonical method tree | All manifests point to/reuse `plugins/epistemic-skills/skills/`; root links expose the same tree. | **SOUND — source** |
| Version parity where schema supports it | Claude/Codex/Cursor/Gemini/Kimi versioned manifests declare `2.9.1`; Antigravity marker has no version field. | **SOUND — deterministic/source** |
| All eleven skills exposed | Directory enumeration and README/Gemini integration assertions now agree on eleven skills / nine disciplines. | **SOUND — deterministic** |
| External handoff advertised | Versioned manifests and Antigravity description include outsource/handoff semantics. | **SOUND — deterministic** |
| No duplicate-install recommendation | README says exactly one mechanism per harness and documents the shared tree. | **SOUND — source** |
| Role isolation honestly represented | Codex renderer/materialization and Kimi Agent mappings are documented; no target-level isolation claim was inferred. | **CONDITIONAL** |
| Live parity across harnesses | No proprietary harness executable/session was available. | **OPEN / NOT TESTED** |

## Defects and changes

1. **Gemini context inventory drift — fixed.** `GEMINI.md` contradicted the canonical inventory. The regression assertion failed before the source correction and passes afterward.
2. **README layout inventory drift — fixed.** The tree comment said “canonical skill cores (ten)” while eleven directories exist. A failing assertion was added before the one-word correction.
3. **Deterministic CI omission — fixed.** The canonical workflow did not execute continuity committed-result scoring or DCO policy unit tests. Assertions failed first; the workflow now executes both.

## Residual harness risk

Static consistency cannot establish native loader behavior, trigger quality, tool mapping correctness under execution, UI availability, or context isolation. A release/merge decision should therefore treat this report as packaging **source assurance plus deterministic integration**, not cross-harness runtime certification.
