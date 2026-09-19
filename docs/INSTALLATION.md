# Installation and compatibility

These instructions describe **v7.0.0**. They preserve the released installation
paths; packaged support and observed host behavior are separate. Consult the
[host coverage](release/v7-host-coverage.md) before relying on automatic loading.
For a quick route into the project, return to the [README](../README.md).


### One copy, one version, one canonical tree

Install with **exactly one mechanism per harness**. Native plugin **or** generic skill install—never both. For 7.0.0, replace an older untagged copy, reload, and verify both the skill count and source path. Duplicate copies create duplicate triggers and can silently mix contract versions.

| Harness | v7.0.0 surface | Required follow-through | Honest support boundary |
|---|---|---|---|
| Claude Code | Local marketplace from tagged checkout | Start a fresh task | Package discovery from one immutable checkout |
| Codex | Tagged plugin marketplace | Render five Gauntlet roles; start a new task | Manifest does not itself register custom collaboration-agent types |
| Cursor | Tagged local checkout or team marketplace | Reload window; verify the tag's full skill count (seventeen at v7.0.0) | Public listing unavailable; recorded behavioral epoch is `BLOCKED_EXTERNAL` |
| Gemini CLI | Tagged extension | Restart and validate extension | Uses root context and canonical symlinked tree |
| Antigravity (`agy`) | Tagged native local plugin | Validate with `agy` | Choose native, Gemini link, or import—only one |
| Kimi Code | Tagged repository plugin | `/reload` or new session | Plugin instructions map isolated-agent primitives |
| ZCode | Tagged local checkout, junction-projected into `~/.zcode/skills` | Start a fresh session; verify the tag's full skill count (seventeen at v7.0.0) | Session bootstrap junctions `~/.claude/skills` only — skills riding as Claude *plugins* are not auto-imported; limited local discovery evidence; native plugin installation unverified |
| ChatGPT / OpenAI | Generated bundle from the release (`packaging/openai/chatgpt-skill`) | Upload the generated zip per [the packaging guide](CHATGPT-AND-OPENAI-PACKAGING.md) | Generated-artifact bridge: a snapshot of the released tree, not self-updating; the bundle carries no live execution |
| Generic Agent Skills host | Tagged canonical skills URL | Reload host and verify source | Host must supply any runtime primitive the selected skill requires |

**Description loading:** hosts may limit the descriptions they load. Verify
discovery after installation, especially when using several skill collections.
The package's [description-budget check](../.github/scripts/check_description_budget.py)
measures its own metadata; it cannot establish a host's remaining capacity.

Full installation, migration, runtime-degradation, and troubleshooting guidance lives in the [installation handbook](https://github.com/ZMS-Labs/epistemic-skills/wiki/Installation-and-Harness-Compatibility).

### Claude Code

```bash
git clone --depth 1 --branch v7.0.0 https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-v7.0.0
```

```text
/plugin marketplace add /absolute/path/to/epistemic-skills-v7.0.0
/plugin install epistemic-skills@epistemic-skills
```

Use one marketplace source only, then start a fresh task. Prefer the immutable `v7.0.0` tag for stable installs; `main` may include post-tag corrective documentation and contract hardening.

### Codex

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref v7.0.0
codex plugin add epistemic-skills@epistemic-skills
python "$HOME/.codex/plugins/cache/epistemic-skills/epistemic-skills/7.0.0/skills/gauntlet/scripts/render_codex_agents.py" --out "$HOME/.codex/agents"
```

Start a new Codex task after rendering. The renderer converts the five canonical packaged Markdown roles into Codex's user-agent registry. The Gauntlet retains a hashed exact-role materialization fallback for tasks that started before registration.

### Cursor

Cursor packaging is present, but the plugin is **not publicly listed**. `/add-plugin epistemic-skills` is not a valid public-install claim until Cursor accepts the listing. Use a tagged local checkout or a Cursor Teams/Enterprise team-marketplace import.

Windows local install:

```powershell
git clone --depth 1 --branch v7.0.0 https://github.com/ZMS-Labs/epistemic-skills.git .\epistemic-skills-v7.0.0
Set-Location .\epistemic-skills-v7.0.0
if ((git describe --tags --exact-match) -ne 'v7.0.0') { throw 'expected v7.0.0' }
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.cursor\plugins\local" | Out-Null
$src = (Resolve-Path .\plugins\epistemic-skills).Path
$dest = Join-Path $env:USERPROFILE '.cursor\plugins\local\epistemic-skills'
if (Test-Path -LiteralPath $dest) { throw "destination already exists; inspect it before replacement: $dest" }
cmd /c mklink /J "$dest" "$src"
```

macOS/Linux local install:

```bash
git clone --depth 1 --branch v7.0.0 https://github.com/ZMS-Labs/epistemic-skills.git ./epistemic-skills-v7.0.0
cd ./epistemic-skills-v7.0.0
test "$(git describe --tags --exact-match)" = v7.0.0
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/epistemic-skills" ~/.cursor/plugins/local/epistemic-skills
```

Run **Developer: Reload Window**, verify the tag's full skill count (seventeen at v7.0.0) under Customize → Skills, and do not also install them into `~/.cursor/skills/`.

### Gemini CLI

```bash
gemini extensions install https://github.com/ZMS-Labs/epistemic-skills --ref v7.0.0 --consent
# Local development only:
gemini extensions link /path/to/epistemic-skills
```

Restart the session and run `gemini extensions validate` when validating a checkout. Stable users should use the tagged install, not the mutable development link.

### Antigravity (`agy`)

```bash
git clone --depth 1 --branch v7.0.0 https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-v7.0.0
agy plugin install /path/to/epistemic-skills-v7.0.0
agy plugin validate /path/to/epistemic-skills-v7.0.0
```

Use one of native `agy plugin install`, Gemini extension link, or `agy plugin import gemini`; do not combine them.

### Kimi Code

```text
/plugins install https://github.com/ZMS-Labs/epistemic-skills/tree/v7.0.0
# Local development only, from a clone:
/plugins install /path/to/epistemic-skills
```

Run `/reload` or start a new session. `.kimi-plugin/plugin.json` points to the canonical package tree and supplies the Kimi tool mappings.

### Generic harness

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/v7.0.0/plugins/epistemic-skills/skills
```

Use this only when the host has no native plugin or extension. Frontmatter `description` is the trigger; the body is the method. Compatibility means the host preserves the selected skill's capability, ordering, isolation, persistence, and fail-closed contracts—not merely that it can display Markdown.
