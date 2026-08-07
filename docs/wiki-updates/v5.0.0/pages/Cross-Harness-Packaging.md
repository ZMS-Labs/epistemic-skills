> **Maintainer handbook:** current development
>
> **Released baseline:** [v3.0.0 package surfaces](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0)
>
> **Current development:** links explicitly labeled `main` describe mutable packaging state, not the stable release.

# Cross-Harness Packaging

The packaging rule is simple: **one canonical implementation, one installed copy per harness, thin adapters at the edges**. Maintainers should be able to compare every package surface without finding forked method text.

## Source topology

| Path | Kind | Maintainer invariant |
|---|---|---|
| `plugins/epistemic-skills/skills/` | canonical directory | All eleven skill cores and supporting files live here. |
| `plugins/epistemic-skills/agents/` | canonical directory | All five Gauntlet role definitions live here. |
| `skills` | repository symlink | Resolves to the canonical skills directory. |
| `agents` | repository symlink | Resolves to the canonical agents directory. |
| root/package manifests | adapter metadata | Point at canonical content; do not duplicate method bodies. |

On platforms that do not preserve repository symlinks, verify the checkout mechanism before claiming a root-scanner surface works. Do not solve a transport problem by committing copied skills.

## Manifest matrix

The v3.0.0 release aligns the version-bearing surfaces at `3.0.0`. Some markers, such as the root Antigravity `plugin.json`, have no version field under their schema; absence there is not drift.

| Harness | Released files | Path rule | Runtime-specific addition |
|---|---|---|---|
| Claude Code | [marketplace](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.claude-plugin/marketplace.json), [package manifest](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/.claude-plugin/plugin.json) | Marketplace source is `./plugins/epistemic-skills`. | None in the manifest beyond package discovery. |
| Codex | [marketplace](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.agents/plugins/marketplace.json), [package manifest](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/.codex-plugin/plugin.json) | Manifest `skills` is package-relative. | Run the released Gauntlet role renderer into the user-agent registry. |
| Cursor | [root plugin](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.cursor-plugin/plugin.json), [team marketplace](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.cursor-plugin/marketplace.json), [package plugin](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/.cursor-plugin/plugin.json) | Root paths include `plugins/epistemic-skills`; package-local paths are `./skills` and `./agents`. | Marketplace listing remains external; local and team-marketplace packaging are distinct from behavioral evidence. |
| Gemini CLI | [`gemini-extension.json`](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/gemini-extension.json), [`GEMINI.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/GEMINI.md) | Uses root context and root `skills` symlink. | Extension validation and session restart. |
| Antigravity | [`plugin.json`](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugin.json) | Native marker consumes the shared root trees. | Install and validate through `agy`; do not combine native, linked, and imported copies. |
| Kimi Code | [root Kimi manifest](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/.kimi-plugin/plugin.json) | Points to `./plugins/epistemic-skills/skills/`. | `skillInstructions` maps user questions and isolated role calls to native tools. |
| Generic host | [canonical skills tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/skills) | Direct Agent Skills loading. | Host must supply any runtime primitive required by the selected skill. |

## The one-copy invariant

Duplicate installs cause duplicate trigger discovery, ambiguous versions, and potentially different supporting files behind the same skill name. Maintainer documentation and tests should therefore enforce:

- native plugin **or** generic skill install, never both;
- tagged stable checkout **or** mutable development checkout, never an unlabeled mixture;
- replacement during migration, not layering;
- reload/new session after install; and
- inventory verification: exactly eleven released skills.

A report that “the skill appears” is insufficient if the harness can see two copies. Verification should establish source path or package version as well as inventory.

## Runtime role binding

The five Gauntlet roles are canonical Markdown files under [`agents/`](https://github.com/ZMS-Labs/epistemic-skills/tree/v5.0.0/plugins/epistemic-skills/agents). Role binding must preserve exact role content and isolated contexts.

Codex has a special packaging bridge: [`render_codex_agents.py`](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/gauntlet/scripts/render_codex_agents.py) renders the packaged Markdown roles into the native user-agent registry. This is required because the package manifest does not itself register collaboration-agent types. The Gauntlet also retains a hashed materialized-role fallback for tasks started before registration.

Other harnesses may register custom roles directly or paste exact role definitions into isolated calls. A single context emitting multiple role-labeled sections is not equivalent to isolated evaluators.

## Package-change checklist

For a manifest, path, or harness integration change:

1. Confirm the change does not create a second skills or agents tree.
2. Resolve every manifest path from the directory where that manifest lives.
3. Verify all expected names and the exact count of fourteen skills.
4. Verify the five Gauntlet roles where the surface advertises agents.
5. Keep description text consistent about router, nine disciplines, and Helix.
6. Run package integration and committed-JSON checks.
7. Exercise a live harness only when the release or change contract requires it; label source-only or deterministic-only verification honestly.
8. Test the upgrade path from one existing copy. Do not document a second install mechanism as an additive migration.
9. For a release, align every version-bearing surface and `EXPECTED_VERSION` on the exact candidate commit.
10. Record unsupported public-marketplace state as external availability, not as a source or merit failure.

## Development versus stable installs

Use the immutable tag for user support and reproduction. Use a branch checkout only to develop the adapter itself, and label it.

- [Stable v3.0.0 installation guide](Installation-and-Harness-Compatibility)
- **Current development:** [root manifests on `main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main)
- **Current development:** [package-local manifests on `main`](https://github.com/ZMS-Labs/epistemic-skills/tree/main/plugins/epistemic-skills)

Do not publish a current-development command as a stable install coordinate. A branch can move between installation and bug reproduction.

## Compatibility claims

Keep three questions separate:

1. **Packaging:** can the harness locate the intended files and metadata?
2. **Runtime contract:** can it provide the required isolation, tool, persistence, or structured-output primitive?
3. **Behavioral evidence:** has the skill's behavior been observed and evaluated in that harness?

Passing a manifest validator answers only the first question. Source inspection may answer part of the second. Neither proves the third. Cursor v3.0.0 packaging is present while the recorded behavioral epoch remains `BLOCKED_EXTERNAL`; those facts are compatible, not contradictory.

## Canonical sources

- [Released v3.0.0 repository layout](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/README.md#layout)
- [Released v3.0.0 installation contract](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/README.md#install)
- [Released runtime role-binding reference](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.0.0/plugins/epistemic-skills/skills/gauntlet/reference/runtime-role-binding.md)
- **Current development:** [packaging architecture on `main`](https://github.com/ZMS-Labs/epistemic-skills/blob/main/docs/superpowers/specs/2026-07-18-agentic-skills-packaging-architecture.md)
