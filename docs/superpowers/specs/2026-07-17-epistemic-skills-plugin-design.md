# Epistemic Skills Plugin Integration Design

Make the `epistemic-skills` repository installable as a plugin/extension for Gemini (Antigravity) and Cursor while retaining the nested directory layout.

## User Review Required

> [!NOTE]
> Symlinks will be created in the root of the repository to map `skills` and `agents` to `plugins/epistemic-skills/skills` and `plugins/epistemic-skills/agents` respectively. Git preserves symlinks natively, but clients on Windows must have symlink creation enabled (e.g., via Developer Mode or Git configuration) for them to checkout as real symlinks.

## Open Questions

None. The user has approved Approach 1 (Root Symlinks + Root Manifests).

## Proposed Changes

### Configuration Manifests

#### [NEW] [gemini-extension.json](file:///y:/dev/epistemic-skills/gemini-extension.json)
This manifest enables the Gemini CLI (Antigravity) to recognize the repository as an installable extension.

#### [NEW] [plugin.json](file:///y:/dev/epistemic-skills/.cursor-plugin/plugin.json)
This manifest enables Cursor to recognize the repository as a plugin, explicitly routing to the nested `skills` and `agents` directories.

### Symlinks

#### [NEW] `skills` (symlink pointing to `plugins/epistemic-skills/skills`)
#### [NEW] `agents` (symlink pointing to `plugins/epistemic-skills/agents`)

---

## Verification Plan

### Automated Tests
1. Run `gemini extensions validate y:\dev\epistemic-skills` to ensure the extension is valid.
2. Install the extension locally via `gemini extensions link y:\dev\epistemic-skills`.
3. Verify that the epistemic skills are loaded successfully in a test session.

### Manual Verification
1. Verify that `skills` and `agents` symlinks are correctly resolved.
2. Verify that `.cursor-plugin/plugin.json` contains the correct paths.
