# GitHub Wiki and README Handbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a comprehensive dual-track GitHub Wiki and merge a substantially improved README that make v3.0.0 usable and maintainable while keeping repository contracts authoritative and presenting Helix as the central passage between workflow and epistemic layers.

**Architecture:** The main repository owns the README, approved design, and implementation plan through a normal pull request. GitHub's separate `epistemic-skills.wiki.git` repository owns the curated handbook and its navigation. Stable guidance links to immutable `v3.0.0` sources; maintainer guidance labels `main` links as current development.

**Tech Stack:** GitHub-flavored Markdown, GitHub Wiki Git repository, PowerShell, Git, GitHub CLI, stdlib Python validation, existing repository CI.

## Global Constraints

- Preserve the README estate-governance block byte-for-byte and in its existing top-of-file position.
- Stable user guidance applies to `v3.0.0` and uses immutable tagged source links.
- `using-epistemic-skills` remains the epistemic router.
- Helix is the central passage between a workflow-skill layer and the epistemic router/disciplines; it is not a replacement router or mandatory ceremony.
- Routine work exits first; absent skill and Helix pairing triggers remain silent.
- Represent all eleven released skills exactly once in the skill-guide inventory. `Helix-Central-Passage.md` is also the Helix skill guide; do not create a duplicate `Skill-Helix.md`.
- Preserve the v3.0.0 no-credit boundaries: two genuine P0 failures, AGY quota failures as availability failures, Cursor `BLOCKED_EXTERNAL`, amended arbitrator certification `NOT_RUN`, and post-hoc `release_credit: none`.
- Do not change skill behavior, triggers, schemas, scripts, evaluations, or the immutable v3.0.0 tag/Release.
- Use `apply_patch` for main-repository and local wiki file edits.
- Keep the user's original `Y:\dev\epistemic-skills` checkout and its unrelated local commit untouched.
- Sign every authored Git commit with an author-matching DCO trailer.

---

## File structure

### Main repository

- Modify: `README.md` — polished project front door, quick start, Helix passage, skill selection, installs, architecture, trust boundaries, and handbook links.
- Existing: `docs/superpowers/specs/2026-07-26-github-wiki-and-readme-design.md` — approved design contract.
- Create: `docs/superpowers/plans/2026-07-26-github-wiki-readme-handbook.md` — this executable plan.

### Wiki repository

- Create/replace: `Home.md` — dual-track landing page.
- Create: `_Sidebar.md` — complete navigation with no orphaned pages.
- Create: `_Footer.md` — stable release and source-of-truth notice.
- Create: `Start-Here.md`
- Create: `Helix-Central-Passage.md`
- Create: `Choosing-a-Skill.md`
- Create: `Routine-Work-and-Proportionality.md`
- Create: `The-Epistemic-Arc.md`
- Create: `Workflow-Recipes.md`
- Create: `Installation-and-Harness-Compatibility.md`
- Create: `Skill-Catalog.md`
- Create: `Skill-Using-Epistemic-Skills.md`
- Create: `Skill-Blindspot-Pass.md`
- Create: `Skill-Applying-Formal-Rigor.md`
- Create: `Skill-Evidence-Research.md`
- Create: `Skill-Write-Goal.md`
- Create: `Skill-Continuity-Verify.md`
- Create: `Skill-Decision-Ledger.md`
- Create: `Skill-Outsource.md`
- Create: `Skill-Gauntlet.md`
- Create: `Skill-Evidence-Locked-UAT.md`
- Create: `Architecture-and-Contracts.md`
- Create: `Cross-Harness-Packaging.md`
- Create: `Testing-and-Evaluations.md`
- Create: `Evidence-Status-and-Known-Limitations.md`
- Create: `Contributing.md`
- Create: `Release-Process-and-Versioning.md`
- Create: `Security-Provenance-and-DCO.md`
- Create: `Design-History-and-Audits.md`
- Create: `Core-Concepts.md`
- Create: `Glossary.md`
- Create: `FAQ-and-Troubleshooting.md`
- Create: `Version-History.md`

---

## Global failure policy

- If Wiki bootstrap fails, stop before authoring against an unverified remote;
  repair bootstrap, clone the real Wiki repository, then continue.
- If a page, sidebar target, local link, stable coordinate, or claim check fails,
  fix it before pushing the Wiki or merging the README.
- If GitHub-rendered Markdown differs materially from the intended local
  content, correct the source and publish a new commit.
- If a released claim cannot be anchored to v3.0.0, omit it or label the
  uncertainty; do not infer a guarantee from design intent.
- Recover through new Git commits. Never rewrite the v3.0.0 tag or its Release.

---

### Task 1: Bootstrap and verify the GitHub Wiki repository

**Files:**
- Create through GitHub UI: `Home.md` with temporary text `epistemic-skills handbook bootstrap`
- Clone into: `Y:\dev\epistemic-skills.wiki`

**Interfaces:**
- Consumes: authenticated GitHub access with Wiki enabled on `ZMS-Labs/epistemic-skills`.
- Produces: a clean local clone whose `origin` is `https://github.com/ZMS-Labs/epistemic-skills.wiki.git` and whose branch is the remote default.

- [ ] **Step 1: Verify the Wiki is enabled and still uninitialized**

Run:

```powershell
gh repo view ZMS-Labs/epistemic-skills --json hasWikiEnabled --jq .hasWikiEnabled
git ls-remote https://github.com/ZMS-Labs/epistemic-skills.wiki.git
```

Expected: the first command prints `true`; before bootstrap, the second reports that the Wiki Git repository is not found.

- [ ] **Step 2: Create the first page through the authenticated GitHub Wiki interface**

Open `https://github.com/ZMS-Labs/epistemic-skills/wiki/_new`, create page title `Home`, body `epistemic-skills handbook bootstrap`, and save it.

Expected: `https://github.com/ZMS-Labs/epistemic-skills/wiki/Home` renders and the Wiki Git repository becomes cloneable.

- [ ] **Step 3: Clone the newly created Wiki repository under the authoritative development root**

Run:

```powershell
git clone https://github.com/ZMS-Labs/epistemic-skills.wiki.git Y:\dev\epistemic-skills.wiki
git -C Y:\dev\epistemic-skills.wiki status --short --branch
git -C Y:\dev\epistemic-skills.wiki remote -v
```

Expected: a clean branch, one bootstrap `Home.md`, and the exact Wiki `origin` URL.

- [ ] **Step 4: Record the bootstrap commit without changing it**

Run:

```powershell
git -C Y:\dev\epistemic-skills.wiki log -1 --oneline
```

Expected: one GitHub-created initial page commit. Do not amend or rewrite it.

---

### Task 2: Build the Wiki foundation, navigation, and central-passage pages

**Files:**
- Replace: `Y:\dev\epistemic-skills.wiki\Home.md`
- Create: `Y:\dev\epistemic-skills.wiki\_Sidebar.md`
- Create: `Y:\dev\epistemic-skills.wiki\_Footer.md`
- Create: `Y:\dev\epistemic-skills.wiki\Start-Here.md`
- Create: `Y:\dev\epistemic-skills.wiki\Helix-Central-Passage.md`
- Create: `Y:\dev\epistemic-skills.wiki\Choosing-a-Skill.md`
- Create: `Y:\dev\epistemic-skills.wiki\Routine-Work-and-Proportionality.md`
- Create: `Y:\dev\epistemic-skills.wiki\The-Epistemic-Arc.md`
- Create: `Y:\dev\epistemic-skills.wiki\Core-Concepts.md`

**Interfaces:**
- Consumes: released README; `using-epistemic-skills/SKILL.md`; `helix/SKILL.md`; `routine-fast-path.md`; `epistemic-flexibility.md` at tag `v3.0.0`.
- Produces: the navigation contract and the canonical Wiki explanation of router-versus-Helix boundaries used by every later page.

- [ ] **Step 1: Write the foundation pages with immutable source links**

Use the approved design sections `Helix as the central passage`, `Homepage design`, and `Source and version policy`. Each content page begins:

```markdown
> **Applies to:** epistemic-skills v3.0.0
> **Canonical source:** [released source](https://github.com/ZMS-Labs/epistemic-skills/tree/v3.0.0/plugins/epistemic-skills/skills)
```

`Helix-Central-Passage.md` must explicitly include:

```text
workflow skills  <->  Helix central passage  <->  epistemic router and disciplines
```

and state that routine work exits before Helix, absent pairs are silent, Helix pairs the layers, and the router decides within the epistemic layer.

- [ ] **Step 2: Write the complete sidebar before later pages exist**

List every filename in the File structure section using GitHub Wiki links, grouped under `Use the skills`, `Develop and maintain`, and `Shared reference`. Place `Helix: Central Passage` immediately after `Start Here`.

Expected: later validation initially fails because the sidebar names not-yet-created pages; this is the planned RED state.

- [ ] **Step 3: Prove the navigation inventory is initially incomplete**

Run this read-only check from the Wiki root:

```powershell
$targets = Select-String -Path _Sidebar.md -Pattern '\]\(([^)]+)\)' -AllMatches |
  ForEach-Object { $_.Matches.Groups[1].Value }
$missing = $targets | Where-Object { -not (Test-Path -LiteralPath (Join-Path $PWD (($_ -replace '/$','') + '.md'))) }
$missing
if (-not $missing) { throw 'expected later pages to be missing at this stage' }
```

Expected: the not-yet-authored skill, workflow, and maintainer pages are listed.

- [ ] **Step 4: Commit the foundation locally without pushing partial Wiki content**

Run:

```powershell
git add Home.md _Sidebar.md _Footer.md Start-Here.md Helix-Central-Passage.md Choosing-a-Skill.md Routine-Work-and-Proportionality.md The-Epistemic-Arc.md Core-Concepts.md
git commit -s -m "docs: establish wiki navigation and central passage"
```

Expected: a signed local Wiki commit; do not push yet.

---

### Task 3: Author all eleven skill guides

**Files:**
- Existing from Task 2: `Y:\dev\epistemic-skills.wiki\Helix-Central-Passage.md`
- Create the ten `Skill-*.md` files listed in File structure.

**Interfaces:**
- Consumes: each released `plugins/epistemic-skills/skills/<name>/SKILL.md` plus directly linked references and tests.
- Produces: exactly eleven guides using the approved ten-section template; the Skill Catalog and recipes link to these pages.

- [ ] **Step 1: Extract and review the released trigger contracts**

Run from the main-repository worktree:

```powershell
Get-ChildItem plugins/epistemic-skills/skills -Directory | Sort-Object Name | ForEach-Object {
  Write-Output "=== $($_.Name)"
  Get-Content (Join-Path $_.FullName 'SKILL.md') -TotalCount 8
}
```

Expected: eleven frontmatter descriptions. Treat them as use/do-not-use authority.

- [ ] **Step 2: Write the ten remaining guides**

Each page contains these exact headings:

```markdown
## What it does
## Use it when
## Do not use it when
## Inputs and prerequisites
## Normal workflow
## Outputs and durable artifacts
## Boundaries and failure modes
## Example prompts
## Related skills and handoffs
## Canonical sources and evidence
```

Use realistic examples. Do not describe skill names as mandatory incantations. Include record-free routine/focused outcomes wherever the released skill defines them.

- [ ] **Step 3: Validate exact skill coverage and template parity**

Run from the Wiki root:

```powershell
$guides = @(
  'Skill-Using-Epistemic-Skills.md','Helix-Central-Passage.md','Skill-Blindspot-Pass.md',
  'Skill-Applying-Formal-Rigor.md','Skill-Evidence-Research.md','Skill-Write-Goal.md',
  'Skill-Continuity-Verify.md','Skill-Decision-Ledger.md','Skill-Outsource.md',
  'Skill-Gauntlet.md','Skill-Evidence-Locked-UAT.md'
)
if ($guides.Count -ne 11) { throw 'expected eleven skill guides' }
$headings = @('What it does','Use it when','Do not use it when','Inputs and prerequisites','Normal workflow','Outputs and durable artifacts','Boundaries and failure modes','Example prompts','Related skills and handoffs','Canonical sources and evidence')
foreach ($guide in $guides) {
  if (-not (Test-Path -LiteralPath $guide)) { throw "missing $guide" }
  $text = Get-Content $guide -Raw
  foreach ($heading in $headings) { if ($text -notmatch "(?m)^## $([regex]::Escape($heading))$") { throw "$guide missing $heading" } }
}
```

Expected: PASS with no output.

- [ ] **Step 4: Commit the skill guides locally**

Run:

```powershell
git add Skill-*.md Helix-Central-Passage.md
git commit -s -m "docs: add comprehensive skill guides"
```

Expected: a signed local Wiki commit; do not push yet.

---

### Task 4: Author user workflows, installation, and shared reference

**Files:**
- Create: `Workflow-Recipes.md`
- Create: `Installation-and-Harness-Compatibility.md`
- Create: `Skill-Catalog.md`
- Create: `Glossary.md`
- Create: `FAQ-and-Troubleshooting.md`
- Create: `Version-History.md`

**Interfaces:**
- Consumes: released README install commands, release notes, manifest files, skill guides, and compatibility limits.
- Produces: task-based cross-skill paths, one-copy installation guidance, quick reference, and common recovery instructions.

- [ ] **Step 1: Write workflow recipes**

Include at least these recipes with entry decision, sequence, handoffs, stop condition, and routine alternative:

- reversible local edit;
- unfamiliar task whose two-read micro-recon exposes coupling;
- consequential design decision;
- research-backed design premise;
- persistent goal contract;
- high-stakes design or pre-merge gate;
- material UI acceptance;
- resumed work from a summary;
- consequential decision persistence;
- durable external model handoff;
- workflow plus epistemic operation through Helix.

- [ ] **Step 2: Write the harness installation and compatibility guide**

Cover Claude Code, Codex, Cursor, Gemini CLI, Antigravity, Kimi Code, and generic Agent Skills. Preserve the one-copy rule, immutable `v3.0.0` coordinates, reload/restart checks, Codex Gauntlet role rendering, Cursor marketplace limitation, and explicit degradation rules.

- [ ] **Step 3: Write the catalog and shared references**

`Skill-Catalog.md` uses columns `Skill`, `Entry trigger`, `Purpose`, `Output`, and `Guide`. `Glossary.md` defines at least routine path, micro-recon, positive trigger, central passage, router, discipline, epistemic arc, load-bearing claim, provenance, no-credit, fail-closed, blinded verifier, Conflict Ledger, and durable artifact. `FAQ-and-Troubleshooting.md` includes duplicate installs, absent triggers, missing subagents, unavailable research substrate, inconclusive UAT, blocked external handoff, and resumption uncertainty.

- [ ] **Step 4: Commit the user and reference pages locally**

Run:

```powershell
git add Workflow-Recipes.md Installation-and-Harness-Compatibility.md Skill-Catalog.md Glossary.md FAQ-and-Troubleshooting.md Version-History.md
git commit -s -m "docs: add workflows installation and reference handbook"
```

Expected: a signed local Wiki commit; do not push yet.

---

### Task 5: Author the maintainer handbook

**Files:**
- Create all eight maintainer pages listed under `Develop and maintain`.

**Interfaces:**
- Consumes: `README.md`, `CONTRIBUTING.md`, `RELEASING.md`, package manifests, `.github/workflows`, contracts, evaluations, design specs, audits, release evidence, and the v3.0.0 risk record.
- Produces: current-development documentation that clearly separates released contracts from mutable maintainer state.

- [ ] **Step 1: Write architecture and packaging pages**

Explain the single canonical skills tree, root symlinks, thin harness manifests, shared Gauntlet agents, contracts, and runtime role binding. Link released behavior to `v3.0.0`; label `main` links as current development.

- [ ] **Step 2: Write testing, evidence, and security pages**

Map the deterministic batteries, continuity polarity, UAT judge, Gauntlet suite, package integration, DCO, CodeQL, and full-history gitleaks positive control. Preserve the exact known limitations and distinguish structural tests, behavioral evidence, diagnostic evidence, and release credit.

- [ ] **Step 3: Write contributing, release, and design-history pages**

Summarize the routine contribution path, DCO, version rules, release gates, partial-publication recovery, major design specs, collection audits, and stress-test records. Never present a historical audit as current certification.

- [ ] **Step 4: Commit the maintainer handbook locally**

Run:

```powershell
git add Architecture-and-Contracts.md Cross-Harness-Packaging.md Testing-and-Evaluations.md Evidence-Status-and-Known-Limitations.md Contributing.md Release-Process-and-Versioning.md Security-Provenance-and-DCO.md Design-History-and-Audits.md
git commit -s -m "docs: add maintainer handbook"
```

Expected: a signed local Wiki commit; do not push yet.

---

### Task 6: Redesign the main README as the project front door

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: approved design, completed Wiki filenames, v3.0.0 release, workflow URLs, released install commands, and skill contracts.
- Produces: the merged entry point whose deep links target the public Wiki pages.

- [ ] **Step 1: Capture and protect the estate block**

Run:

```powershell
$before = (Get-Content README.md -Raw) -replace '(?s)^(.*?<!-- ZMS-ESTATE:END -->).*','$1'
$before | Set-Variable EstateBlock
```

Do not write `$EstateBlock` to disk. After editing, compare the same prefix byte-for-byte.

- [ ] **Step 2: Rewrite the README using the approved section order**

Add durable badges:

```markdown
[![Release](https://img.shields.io/github/v/release/ZMS-Labs/epistemic-skills?display_name=tag)](https://github.com/ZMS-Labs/epistemic-skills/releases/latest)
[![epistemic-flexibility](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/epistemic-flexibility.yml/badge.svg)](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/epistemic-flexibility.yml)
[![release-security](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/release-security.yml/badge.svg)](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/release-security.yml)
[![CodeQL](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ZMS-Labs/epistemic-skills/actions/workflows/github-code-scanning/codeql)
[![License](https://img.shields.io/github/license/ZMS-Labs/epistemic-skills)](LICENSE)
```

Include the dual audience paths, five-minute start, routine gate, Helix central-passage diagram, task-to-skill table, Mermaid arc, all-eleven skill catalog, compatibility matrix and detailed installs, architecture, trust limits, maintainer links, and license.

- [ ] **Step 3: Verify the estate block is unchanged**

Run in the same PowerShell session used in Step 1:

```powershell
$after = (Get-Content README.md -Raw) -replace '(?s)^(.*?<!-- ZMS-ESTATE:END -->).*','$1'
if ($after -cne $EstateBlock) { throw 'estate block changed' }
```

Expected: PASS with no output.

- [ ] **Step 4: Verify required README concepts and Wiki links**

Run:

```powershell
$text = Get-Content README.md -Raw
@('Version 3.0.0','Routine work','Helix','central passage','using-epistemic-skills','release_credit: none','GitHub Wiki') |
  ForEach-Object { if ($text -notmatch [regex]::Escape($_)) { throw "README missing $_" } }
$skills = Get-ChildItem plugins/epistemic-skills/skills -Directory | Select-Object -ExpandProperty Name
foreach ($skill in $skills) { if ($text -notmatch [regex]::Escape($skill)) { throw "README missing $skill" } }
```

Expected: PASS with no output.

- [ ] **Step 5: Commit the README locally**

Run:

```powershell
git add README.md
git commit -s -m "docs: make README a comprehensive project gateway"
```

Expected: a signed main-repository commit.

---

### Task 7: Run structural, link, and claim validation

**Files:**
- Test: all main-repository and Wiki Markdown files created or modified by this plan.

**Interfaces:**
- Consumes: complete local Wiki and README.
- Produces: fail-closed evidence that navigation, local links, stable refs, skill coverage, and claim boundaries are coherent before publication.

- [ ] **Step 1: Validate the complete Wiki page inventory and sidebar**

Run from the Wiki root:

```powershell
$content = Get-ChildItem -File -Filter *.md | Where-Object { $_.Name -notin @('_Sidebar.md','_Footer.md') }
$sidebar = Get-Content _Sidebar.md -Raw
foreach ($page in $content) {
  $slug = $page.BaseName
  $count = [regex]::Matches($sidebar,[regex]::Escape("($slug)")).Count
  if ($count -ne 1) { throw "sidebar references $($page.Name) $count times; expected exactly once" }
}
$targets = [regex]::Matches($sidebar,'\]\(([^)]+)\)') | ForEach-Object { $_.Groups[1].Value }
foreach ($target in $targets) {
  if ($target -match '^https?://') { continue }
  $path = Join-Path $PWD (($target -replace '/$','') + '.md')
  if (-not (Test-Path -LiteralPath $path)) { throw "missing sidebar target: $target" }
}
if ($content.Count -lt 30) { throw "expected at least 30 content pages, found $($content.Count)" }
```

Expected: PASS with no output and at least 30 content pages.

- [ ] **Step 2: Validate Markdown links that target local files**

Run from the main-repository worktree:

```powershell
@'
from pathlib import Path
from urllib.parse import unquote, urlparse
import re

sets = [
    (Path.cwd(), [Path("README.md")], False),
    (Path("Y:/dev/epistemic-skills.wiki"), sorted(Path("Y:/dev/epistemic-skills.wiki").glob("*.md")), True),
]
link = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
missing = []
for root, files, wiki_mode in sets:
    for source in files:
        source = source if source.is_absolute() else root / source
        for raw in link.findall(source.read_text(encoding="utf-8")):
            target = raw.strip().strip("<>").split()[0]
            parsed = urlparse(target)
            if parsed.scheme or target.startswith("#") or target.startswith("mailto:"):
                continue
            rel = unquote(target.split("#", 1)[0])
            if not rel:
                continue
            candidate = (source.parent / rel)
            if wiki_mode and not candidate.suffix:
                candidate = candidate.with_suffix(".md")
            if not candidate.exists():
                missing.append(f"{source}: {target} -> {candidate}")
if missing:
    raise SystemExit("\n".join(missing))
print("local Markdown links: PASS")
'@ | python -
```

Expected: zero missing local targets.

- [ ] **Step 3: Validate immutable stable coordinates**

Run:

```powershell
rg -n 'tree/main|blob/main|--ref main|--branch main' README.md Y:\dev\epistemic-skills.wiki
```

Expected: any matches occur only in explicitly labeled maintainer/current-development prose; stable install commands contain `v3.0.0`.

- [ ] **Step 4: Validate package/version consistency and repository artifacts**

Run:

```powershell
python plugins/epistemic-skills/skills/outsource/tests/run_tests.py
python .github/scripts/check_json_artifacts.py
python plugins/epistemic-skills/skills/using-epistemic-skills/evals/proportionality/blinded/tests/run_tests.py
python plugins/epistemic-skills/skills/gauntlet/tests/run_tests.py
git diff --check origin/main...HEAD
```

Expected: every command passes.

- [ ] **Step 5: Perform a focused claim audit**

Search README and Wiki for `superior`, `certified`, `Cursor`, `P0`, `quota`, `NOT_RUN`, and `release_credit`. Confirm every positive-sounding claim is bounded by the v3.0.0 release record and every required limitation appears on the evidence page and README trust section.

Expected: no unbounded superiority, cross-provider, Cursor-compatibility, or current-certification claim.

---

### Task 8: Publish and verify the complete Wiki

**Files:**
- Publish: all committed files in `Y:\dev\epistemic-skills.wiki`

**Interfaces:**
- Consumes: locally committed Wiki history passing Task 7.
- Produces: public Wiki pages at `https://github.com/ZMS-Labs/epistemic-skills/wiki/...` and a clean local clone aligned with the remote.

- [ ] **Step 1: Run final Wiki pre-push checks**

Run:

```powershell
git status --short --branch
git log --format='%h %s%n%b' --reverse
git diff --check origin/HEAD...HEAD
```

Expected: clean working tree; every authored commit has an author-matching `Signed-off-by` trailer.

- [ ] **Step 2: Push the complete Wiki history once**

Run:

```powershell
git push origin HEAD
```

Expected: the remote Wiki branch advances through all local handbook commits.

- [ ] **Step 3: Verify remote alignment**

Run:

```powershell
git fetch origin
$local = (git rev-parse HEAD).Trim()
$remote = (git rev-parse '@{upstream}').Trim()
if ($local -ne $remote) { throw 'Wiki remote does not match local HEAD' }
git status --short --branch
```

Expected: equal SHAs and a clean aligned branch.

---

### Task 9: Publish the README through a reviewed pull request

**Files:**
- Publish: `README.md`, approved design spec, and this implementation plan on `codex/wiki-readme-handbook`.

**Interfaces:**
- Consumes: complete public Wiki URLs and passing Task 7 checks.
- Produces: a reviewed, CI-green pull request merged to `main`.

- [ ] **Step 1: Update README Wiki links after public Wiki verification**

Confirm every link uses `https://github.com/ZMS-Labs/epistemic-skills/wiki/<Page-Slug>` and resolves publicly. Apply only link corrections; do not change approved content boundaries.

- [ ] **Step 2: Re-run main-repository validation and DCO audit**

Run Task 7 Step 4 again, then check every `origin/main..HEAD` commit for an author-matching sign-off using the repository's DCO policy.

Expected: all checks pass and no unsigned commit exists.

- [ ] **Step 3: Commit any public-link corrections and push the branch**

Run:

```powershell
git add README.md docs/superpowers/specs/2026-07-26-github-wiki-and-readme-design.md docs/superpowers/plans/2026-07-26-github-wiki-readme-handbook.md
$staged = git diff --cached --name-only
if ($staged) { git commit -s -m "docs: finalize public handbook links" }
git push -u origin codex/wiki-readme-handbook
```

Expected: branch is durable on GitHub.

- [ ] **Step 4: Open a draft pull request with exact verification and Wiki coordinates**

Create a draft PR titled `docs: build comprehensive README and GitHub Wiki handbook`. The body summarizes the dual audience paths, Helix central passage, Wiki page count and commit, source/version policy, validations, and known limitations.

- [ ] **Step 5: Run independent documentation review**

Review the frozen exact PR head for incorrect trigger boundaries, unsafe install instructions, mutable stable refs, stale certification claims, broken links, duplicated Helix/router roles, and omissions from the approved page map. Fix every actionable P1/P2 finding on the branch and rerun validation.

- [ ] **Step 6: Require exact-head GitHub checks and merge**

Require DCO, stdlib checks, release-security when triggered, and CodeQL checks to pass on the final head. Mark ready and merge only that reviewed head.

Expected: PR state `MERGED`, with `origin/main` containing the README, design, and plan.

---

### Task 10: Verify rendered GitHub documentation and close the work

**Files:**
- Verify only: merged `README.md` and public Wiki pages.

**Interfaces:**
- Consumes: merged README and pushed Wiki.
- Produces: rendered evidence and immutable commit coordinates for the operator.

- [ ] **Step 1: Verify required rendered Wiki pages**

Open and visually inspect:

- `https://github.com/ZMS-Labs/epistemic-skills/wiki/Home`
- `https://github.com/ZMS-Labs/epistemic-skills/wiki/Helix-Central-Passage`
- `https://github.com/ZMS-Labs/epistemic-skills/wiki/Skill-Applying-Formal-Rigor`
- `https://github.com/ZMS-Labs/epistemic-skills/wiki/Installation-and-Harness-Compatibility`
- `https://github.com/ZMS-Labs/epistemic-skills/wiki/Architecture-and-Contracts`

Expected: headings, tables, code fences, sidebar, footer, and cross-links render correctly.

- [ ] **Step 2: Verify the merged README rendering**

Open `https://github.com/ZMS-Labs/epistemic-skills#readme`. Confirm badges, Mermaid diagram, dual paths, tables, install commands, Wiki links, and trust limitations render correctly.

- [ ] **Step 3: Verify public reachability and final identities**

Run:

```powershell
gh api repos/ZMS-Labs/epistemic-skills/commits/main --jq .sha
git -C Y:\dev\epistemic-skills.wiki rev-parse HEAD
git -C Y:\dev\epistemic-skills.wiki rev-parse '@{upstream}'
```

Expected: main and Wiki identities are explicit; Wiki local and upstream SHAs match.

- [ ] **Step 4: Confirm the original checkout was preserved**

Run:

```powershell
git -C Y:\dev\epistemic-skills branch --show-current
git -C Y:\dev\epistemic-skills status --short --branch
```

Expected: the original user branch and its unrelated ahead commit remain unchanged.

- [ ] **Step 5: Report completion**

Return the public Wiki homepage, merged README PR, main commit, Wiki commit, page count, validation results, rendered smoke-test result, and the preserved v3.0.0 limitation summary.
