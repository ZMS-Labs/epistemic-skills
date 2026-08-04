> **Applies to:** epistemic-skills v4.0.0
>
> **Canonical source:** [released installation guide](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/README.md#installation-and-compatibility)

# Installation and Harness Compatibility

Install exactly **one** copy of the v4.0.0 skills per harness. The skills have one canonical tree; harness manifests are thin entrypoints. Layering a native plugin and a generic skills install creates duplicate triggers.

## First: stable coordinates and migration

Use immutable `v4.0.0` coordinates, not a mutable branch. Existing untagged installs must be replaced rather than layered; then reload the harness or start a new task. Integrations must accept silent routine/absent-trigger paths, inline record-free focused formal rigor, and `formal-rigor-record@2` only for standard/high-assurance work.

## Claude Code

```bash
git clone --depth 1 --branch v4.0.0 https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-v4.0.0
```

```text
/plugin marketplace add /absolute/path/to/epistemic-skills-v4.0.0
/plugin install epistemic-skills@epistemic-skills
```

Use the dedicated tagged checkout as the only installation source. Start a fresh task after installation.

## Codex

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref v4.0.0
codex plugin add epistemic-skills@epistemic-skills
python "$HOME/.codex/plugins/cache/epistemic-skills/epistemic-skills/4.0.0/skills/gauntlet/scripts/render_codex_agents.py" --out "$HOME/.codex/agents"
```

Start a new Codex task after rendering. Codex plugin manifests do not register custom collaboration-agent types; the renderer materializes the five canonical Gauntlet Markdown roles into Codex's user-agent TOML registry. A task that began before rendering has only the released hashed exact-role materialization fallback, so do not claim native role registration there.

## Cursor

**Public marketplace:** the v4.0.0 packaging is ready, but the plugin is not publicly listed, so `/add-plugin epistemic-skills` is unavailable until Cursor lists it. Until then, use a local tagged checkout or a Cursor Teams/Enterprise team-marketplace import.

**Behavioral evidence:** separately, the retained Cursor behavioral/runtime evaluation epoch remains `BLOCKED_EXTERNAL`; that status describes only the retained evaluation evidence.

```powershell
git clone --depth 1 --branch v4.0.0 https://github.com/ZMS-Labs/epistemic-skills.git .\epistemic-skills-v4.0.0
Set-Location .\epistemic-skills-v4.0.0
if ((git describe --tags --exact-match) -ne 'v4.0.0') { throw 'expected v4.0.0' }
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\plugins\local" | Out-Null
$src  = (Resolve-Path .\plugins\epistemic-skills).Path
$dest = Join-Path $env:USERPROFILE '.cursor\plugins\local\epistemic-skills'
if (Test-Path -LiteralPath $dest) { throw "Cursor plugin destination already exists; move or remove it manually after verifying its contents: $dest" }
cmd /c mklink /J "$dest" "$src"
```

On macOS/Linux, clone the same tag, verify `git describe --tags --exact-match`, and symlink `plugins/epistemic-skills` into `~/.cursor/plugins/local/epistemic-skills`. Then run **Developer: Reload Window**. Verify eleven skills under Customize → Skills and a matching positive trigger. Do not separately install them into `~/.cursor/skills/`.

## Gemini CLI

```bash
gemini extensions install https://github.com/ZMS-Labs/epistemic-skills --ref v4.0.0 --consent
# local development only:
gemini extensions link /path/to/epistemic-skills
```

Restart the Gemini session. Entrypoints are `gemini-extension.json`, `GEMINI.md`, and the root `skills/` symlink; validate with `gemini extensions validate`.

## Antigravity (`agy`)

```bash
git clone --depth 1 --branch v4.0.0 https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-v4.0.0
agy plugin install /path/to/epistemic-skills-v4.0.0
agy plugin validate /path/to/epistemic-skills-v4.0.0
```

The root `plugin.json` is the native marker. Choose one of native install, Gemini extension link, or `agy plugin import gemini`; never several copies.

## Kimi Code

```text
/plugins install https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0
# local development, from a clone:
/plugins install /path/to/epistemic-skills
```

Run `/reload` or begin a new session. `.kimi-plugin/plugin.json` points to the canonical skills tree and maps Gauntlet roles plus the UAT actor/verifier/judge through isolated `Agent` contexts. If the plugin manager is unavailable, junction the skill directories into the user skills directory instead—but choose one mechanism.

## Generic Agent Skills harness

Use this only if the harness has no native plugin or extension path:

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/skills
```

Load `plugins/epistemic-skills/skills/` (or the root `skills/` symlink). Frontmatter `description` is the trigger; the body is the method. Apply the routine gate before loading a process container.

## Runtime contracts and explicit degradation

Harness compatibility is contractual, not a promise of identical built-in tools.

| Need | Contract and degradation |
|---|---|
| Gauntlet | Concurrent, context-isolated exact-role agents behind a barrier; sequential isolated calls are the stated degradation. Use the materialized-role adapter where custom agent registration is unavailable. |
| Evidence-Locked UAT | Separate actor, blinded verifier, and deterministic judge for a material acceptance run. Without them, do not issue a ready-looking PASS packet. |
| Resolve (literature instrument) | Consensus + Scite MCP + durable Zotero/equivalent library. If any layer is unavailable, state the missing layer and evidence limit explicitly. |
| Write Goal | Persistent-goal inspection/creation and preferably a user-question primitive. Without lifecycle tooling, return the approved contract without pretending it started. |
| Outsource | Repository read/write plus Git/GitHub publication/verification. Without a pushed, target-readable packet, return `BLOCKED`, not a prompt that looks ready. |
| Resolve (derivation instrument) / Recon | Pure methods; no special runtime dependency. |

Missing optional skills do not block the routine path. A missing discipline at a positive high-stakes boundary fails closed: hold, escalate, or take only a bounded reversible probe. See [FAQ and Troubleshooting](FAQ-and-Troubleshooting) for recovery paths.

## Canonical sources

- [v4.0.0 README install section](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/README.md#installation-and-compatibility)
- [v4.0.0 release record](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/docs/release/RELEASE-4.0.0.md)
- [Agent Skills specification](https://agentskills.io/specification)
