# ChatGPT and OpenAI packaging

This repository has one canonical runtime package:
`plugins/epistemic-skills/`. OpenAI-facing artifacts are generated from that
package; no second skill inventory is maintained.

## What is generated

Run:

```bash
python .github/scripts/build_openai_bundles.py \
  --out-dir dist/openai \
  --source-revision "$(git rev-parse HEAD)"
```

The builder emits:

- `epistemic-skills-chatgpt-skill.zip` — a single Personal Skill upload bridge.
  Its top-level `SKILL.md` reads a generated index and then loads the applicable
  canonical skill files included under `package/`.
- `epistemic-skills-openai-plugin.zip` — a self-contained marketplace/plugin
  package preserving `.agents/plugins/marketplace.json` and
  `plugins/epistemic-skills/` at their repository-relative paths.
- `SHA256SUMS` — hashes for both revision-bound archives.

The archives are deterministic for identical source bytes and the same supplied
source revision.

## Why additions and removals flow automatically

The builder discovers direct
`plugins/epistemic-skills/skills/<name>/SKILL.md` children at build time. It
extracts each skill's current frontmatter, verifies that `name` matches its
directory, hashes the complete skill subtree, and generates the index. There is
no Python constant, manifest array, README table, or wrapper list to update when
a skill is added, renamed, or removed.

The plugin marketplace already points to `./plugins/epistemic-skills`, and the
package manifest points to `./skills/`. The builder fails closed if either path
is changed to a copied snapshot.

## Continuous regeneration

`.github/workflows/openai-bundles.yml` runs on relevant pull requests, pushes to
`main`, published releases, and manual dispatch. Every successful run tests the
builder, validates the live package, and uploads freshly generated bundles for
the exact workflow revision.

This makes repository-to-bundle synchronization automatic. It does **not** make
an already uploaded Personal Skill self-updating: that installation is a
snapshot and must be replaced with a newer generated archive. An OpenAI plugin
imported from a marketplace is the durable source-linked route; OpenAI's current
workspace guidance provides a **Refresh** action to pull updates from the
original marketplace source.

## Installing the immediate ChatGPT bridge

OpenAI currently documents Personal Skill upload through:
**Plugins → Skills → Create → Upload from your computer**. Upload
`epistemic-skills-chatgpt-skill.zip`, review the scan result, and install it.
Then use it explicitly with an `@Epistemic Skills` mention when desired; ChatGPT
may also select an installed Skill automatically when its description applies.

Official references, checked 2026-08-06:

- <https://help.openai.com/en/articles/20001066-skills-in-chatgpt>
- <https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex>

## Plugin-directory boundary

The repository and generated plugin archive are structurally ready for a
skill-only OpenAI plugin import or directory submission. Publication itself is
an OpenAI control-plane action, not a Git commit. The public documentation does
not expose a universal repository-to-public-directory submission API, so this
project does not claim that a workflow run publishes the plugin automatically.
Once the plugin is imported or accepted, its source remains the canonical
package rather than a manually synchronized copy.

## Maintainer checks

```bash
python .github/scripts/test_build_openai_bundles.py
python .github/scripts/build_openai_bundles.py --check
```

A change is not package-ready if either command fails.
