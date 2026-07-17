# Epistemic Skills Plugin Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the `epistemic-skills` repository installable as a plugin/extension for Gemini (Antigravity) and Cursor using root manifests and symlinks while maintaining the nested structure.

**Architecture:** Create root-level configuration files `gemini-extension.json` and `.cursor-plugin/plugin.json`. Use symlinks/junctions at the root pointing to the nested `skills` and `agents` directories to make them discoverable.

**Tech Stack:** PowerShell, git, JSON

---

### Task 1: Create Gemini Extension Manifest

**Files:**
- Create: `gemini-extension.json`

- [ ] **Step 1: Write the manifest content**
  Create `gemini-extension.json` with the following content:
  ```json
  {
    "name": "epistemic-skills",
    "description": "The full epistemic-discipline collection in one package: a router plus formal rigor, blindspot reconnaissance, scholarly evidence, evidence-locked UAT, and multi-lens adversarial review.",
    "version": "2.2.0"
  }
  ```

- [ ] **Step 2: Commit**
  Run:
  ```powershell
  git add gemini-extension.json
  git commit -m "feat: add gemini-extension.json manifest"
  ```

---

### Task 2: Create Cursor Plugin Manifest

**Files:**
- Create: `.cursor-plugin/plugin.json`

- [ ] **Step 1: Write the Cursor plugin manifest**
  Create `.cursor-plugin/plugin.json` with the following content:
  ```json
  {
    "name": "epistemic-skills",
    "displayName": "Epistemic Skills",
    "description": "The full epistemic-discipline collection in one package: a router plus formal rigor, blindspot reconnaissance, scholarly evidence, evidence-locked UAT, and multi-lens adversarial review.",
    "version": "2.2.0",
    "author": {
      "name": "ZMS Labs",
      "url": "https://github.com/ZMS-Labs"
    },
    "homepage": "https://github.com/ZMS-Labs/epistemic-skills",
    "repository": "https://github.com/ZMS-Labs/epistemic-skills",
    "license": "MIT",
    "skills": "./plugins/epistemic-skills/skills/",
    "agents": "./plugins/epistemic-skills/agents/"
  }
  ```

- [ ] **Step 2: Commit**
  Run:
  ```powershell
  git add .cursor-plugin/plugin.json
  git commit -m "feat: add .cursor-plugin/plugin.json manifest"
  ```

---

### Task 3: Create Skills and Agents Symlinks

**Files:**
- Create: `skills` (symlink/junction)
- Create: `agents` (symlink/junction)

- [ ] **Step 1: Create symlinks at the root**
  Run the following commands in PowerShell (under workspace root `y:\dev\epistemic-skills`):
  ```powershell
  cmd /c mklink /d skills plugins\epistemic-skills\skills
  cmd /c mklink /d agents plugins\epistemic-skills\agents
  ```

- [ ] **Step 2: Commit symlinks to Git**
  Run:
  ```powershell
  git add skills agents
  git commit -m "feat: add skills and agents symlinks at root"
  ```

---

### Task 4: Validate and Test Installation

**Files:**
- None (Verification task)

- [ ] **Step 1: Run Gemini extensions validation**
  Run:
  ```powershell
  gemini extensions validate y:\dev\epistemic-skills
  ```
  Expected: Extension is valid (Exit code 0).

- [ ] **Step 2: Link the extension locally**
  Run:
  ```powershell
  gemini extensions link y:\dev\epistemic-skills
  ```
  Expected: Successful link output, confirming the extension is loaded.

- [ ] **Step 3: Verify the skills list**
  Run:
  ```powershell
  gemini extensions list
  ```
  Expected: `epistemic-skills` listed as installed and enabled with the 6 epistemic skills loaded.
