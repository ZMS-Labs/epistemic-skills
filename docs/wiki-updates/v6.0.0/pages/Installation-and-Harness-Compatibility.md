> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical source:** [released skill tree](https://github.com/ZMS-Labs/epistemic-skills/tree/v6.0.0/plugins/epistemic-skills/skills)
>
> Prefer immutable `v5.1.0` coordinates. `main` is current development and may move ahead of the tag.

# Installation and Harness Compatibility

Install exactly **one** copy of the v5.1.0 skills per harness. The skills have one canonical tree; harness manifests are thin entrypoints. Layering a native plugin and a generic skills install creates duplicate triggers.

## First: stable coordinates and migration

Use immutable `v5.1.0` coordinates for stable behavior claims. Existing untagged installs must be replaced rather than layered; then reload the harness or start a new task. Expect **fifteen** skills at v5.1.0.

Post-release corrective commits on `main` (after the immutable tag) may include documentation and contract hardening that are not in the annotated tag. Prefer the tag for reproducible installs; prefer `main` only when you intentionally want post-tag corrective work.

## Claude Code

```bash
git clone --depth 1 --branch v5.1.0 https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-v5.1.0
```

```text
/plugin marketplace add /absolute/path/to/epistemic-skills-v5.1.0
/plugin install epistemic-skills@epistemic-skills
```

Use one marketplace source only, then start a fresh task.

## Codex

```powershell
codex plugin marketplace add ZMS-Labs/epistemic-skills --ref v5.1.0
codex plugin add epistemic-skills@epistemic-skills
python "$HOME/.codex/plugins/cache/epistemic-skills/epistemic-skills/5.1.0/skills/gauntlet/scripts/render_codex_agents.py" --out "$HOME/.codex/agents"
```

Start a new Codex task after rendering.

## Cursor

The plugin is **not publicly listed**. Use a tagged local checkout or a Cursor Teams/Enterprise team-marketplace import. Verify fifteen skills after reload. Do not also install into `~/.cursor/skills/`.

```bash
git clone --depth 1 --branch v5.1.0 https://github.com/ZMS-Labs/epistemic-skills.git ./epistemic-skills-v5.1.0
cd ./epistemic-skills-v5.1.0
test "$(git describe --tags --exact-match)" = "v5.1.0"
mkdir -p ~/.cursor/plugins/local
ln -sfn "$(pwd)/plugins/epistemic-skills" ~/.cursor/plugins/local/epistemic-skills
```

## Gemini CLI

```bash
gemini extensions install https://github.com/ZMS-Labs/epistemic-skills --ref v5.1.0 --consent
```

Restart and validate. Prefer the tagged install over a mutable development link.

## Antigravity (`agy`)

```bash
git clone --depth 1 --branch v5.1.0 https://github.com/ZMS-Labs/epistemic-skills.git /path/to/epistemic-skills-v5.1.0
agy plugin install /path/to/epistemic-skills-v5.1.0
agy plugin validate /path/to/epistemic-skills-v5.1.0
```

Choose one of native install, Gemini extension link, or `agy plugin import gemini`.

## Kimi Code

```text
/plugins install https://github.com/ZMS-Labs/epistemic-skills/tree/v5.1.0
```

Run `/reload` or start a new session.

## Generic Agent Skills harness

```bash
npx skills add https://github.com/ZMS-Labs/epistemic-skills/tree/v5.1.0/plugins/epistemic-skills/skills
```

Use only when no native plugin or extension exists. Frontmatter `description` is the trigger; the body is the method.

## Further reading

- [README installation section at v5.1.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v5.1.0/README.md#installation-and-compatibility)
- [Cross-Harness Packaging](Cross-Harness-Packaging)
- [Harness verification matrix (successor)](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/release/HARNESS-VERIFICATION-MATRIX-SUCCESSOR-2026-08-07.md)
