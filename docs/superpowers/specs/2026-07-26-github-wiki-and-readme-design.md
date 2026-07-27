# GitHub Wiki and README Handbook Design

**Status:** approved design
**Repository:** `ZMS-Labs/epistemic-skills`
**Stable baseline:** `v3.0.0`
**Audience:** users/adopters and developers/maintainers with equal first-class paths

## Goal

Create a comprehensive GitHub Wiki and a substantially improved repository
README that together make epistemic-skills understandable, usable, auditable,
and maintainable without creating a second specification that can silently
drift away from the released repository.

The README is the polished front door. The wiki is the deeper handbook. The
versioned repository remains authoritative for skill contracts, schemas,
scripts, tests, evaluation evidence, release records, and design history.

## Success criteria

The documentation succeeds when a new reader can:

1. understand what problem epistemic-skills solves and what it does not claim;
2. choose the routine path, the epistemic router, or Helix correctly;
3. install exactly one copy for their harness using an immutable release;
4. select and use any of the eleven skills without reading its implementation;
5. understand outputs, handoffs, failure modes, and degradation boundaries;
6. find canonical contracts and evidence without confusing summaries for proof;
7. understand the architecture, packaging, test suites, and release process; and
8. contribute without introducing duplicated skills, stale claims, or ceremony
   that defeats the proportionality contract.

## Documentation roles

### README

The README is the project landing page and rapid orientation path. It remains
detailed enough to install and begin using the project without visiting the
wiki, but it does not reproduce every skill guide or evaluation record.

### GitHub Wiki

The wiki is the curated handbook. It provides concept explanations, task-based
guides, skill-by-skill usage, workflow recipes, maintainer documentation,
glossary material, and troubleshooting. It links into immutable repository
sources wherever exact behavior matters.

### Repository

The repository is the source of truth. In a disagreement, the following order
controls:

1. the immutable released `SKILL.md`, contract, schema, or executable check;
2. released reference files and release records;
3. the README and wiki summaries.

Wiki language must never promote a design, incomplete evaluation, or historical
result into a current behavioral guarantee.

## Helix as the central passage

Helix is intentionally presented as a centralized passage between a
workflow-skill layer and the epistemic layer:

```text
workflow skills  <->  Helix central passage  <->  epistemic router and disciplines
```

This prominence must not blur the boundary between Helix and
`using-epistemic-skills`:

- `using-epistemic-skills` is the router inside the epistemic collection. It
  applies the routine gate, identifies positive epistemic triggers, sequences
  disciplines, and defines their handoffs.
- `helix` is the tandem entry point when a workflow system such as superpowers
  is also active. It pairs workflow stages with positively triggered epistemic
  disciplines and passes through the correct contracts.
- Helix is not a requirement to run every skill, not a new process container,
  and not a replacement for the routine exit.
- Routine work and absent pairings remain silent.

Helix receives first-class placement on the README, wiki homepage, sidebar,
workflow recipes, architecture explanation, glossary, and a dedicated
`Helix: Central Passage` guide.

## Wiki information architecture

The homepage opens with two equal paths and a prominent Helix crossing between
them.

### Use the skills

- `Start Here`
- `Helix: Central Passage`
- `Choosing a Skill`
- `Routine Work and Proportionality`
- `The Epistemic Arc`
- `Workflow Recipes`
- `Installation and Harness Compatibility`
- `Skill Catalog`
- one practical guide for each released skill:
  - `using-epistemic-skills`
  - `helix`
  - `blindspot-pass`
  - `applying-formal-rigor`
  - `evidence-research`
  - `write-goal`
  - `continuity-verify`
  - `decision-ledger`
  - `outsource`
  - `gauntlet`
  - `evidence-locked-uat`

### Develop and maintain

- `Architecture and Contracts`
- `Cross-Harness Packaging`
- `Testing and Evaluations`
- `Evidence, Status, and Known Limitations`
- `Contributing`
- `Release Process and Versioning`
- `Security, Provenance, and DCO`
- `Design History and Audits`

### Shared reference

- `Core Concepts`
- `Glossary`
- `FAQ and Troubleshooting`
- `Version History`

### Navigation files

- `_Sidebar.md` exposes every content page under the same three groups and
  places `Helix: Central Passage` near the top.
- `_Footer.md` identifies the current stable release, links to the canonical
  repository and release, and states that repository contracts control.
- No content page is allowed to be orphaned from `_Sidebar.md`.

## Homepage design

`Home.md` contains:

1. the one-paragraph value proposition;
2. current stable release and honest support boundary;
3. equal `Use the skills` and `Develop and maintain` entry tables;
4. the routine path as the default first decision;
5. Helix as the central passage for paired workflow/epistemic operation;
6. a compact map of the epistemic arc;
7. links to installation, the skill catalog, known limitations, and the release;
8. a clear source-of-truth statement.

The homepage must be useful without assuming prior knowledge of agent skills,
superpowers, formal methods, UAT, or multi-agent review.

## Standard skill-page template

Every skill page uses the same visible structure:

1. **What it does** — one concise behavioral description.
2. **Use it when** — positive triggers from released frontmatter and contract.
3. **Do not use it when** — routine and boundary cases.
4. **Inputs and prerequisites** — required state, tools, or prior artifacts.
5. **Normal workflow** — numbered method summary.
6. **Outputs and durable artifacts** — including record-free outcomes.
7. **Boundaries and failure modes** — fail-closed and degradation behavior.
8. **Example prompts** — realistic invocation examples, not magic phrases.
9. **Related skills and handoffs** — upstream/downstream relationships.
10. **Canonical sources and evidence** — immutable `v3.0.0` links.

The Helix page additionally explains the central-passage model, pairing rules,
silent absent triggers, the routine exit, ordering, and how Helix differs from
the router.

## README redesign

The estate-governance block remains byte-for-byte intact and retains its
position near the top of the file.

The rest of the README is reorganized into:

1. **Project identity** — concise value proposition, stable release, license,
   and harness-agnostic contract.
2. **Status badges** — release, license, stdlib checks, release-security, and
   CodeQL using durable GitHub workflow URLs.
3. **What this is and is not** — epistemic discipline beneath workflow skills,
   not a replacement for ordinary engineering or a mandate for ceremony.
4. **Choose your path** — equal user and maintainer links into the wiki.
5. **Five-minute start** — install one immutable copy, begin with the router or
   Helix as appropriate, and verify the expected skill inventory.
6. **Routine work first** — the four-part routine test and two-read micro-recon.
7. **Helix central passage** — a prominent diagram and boundary explanation.
8. **Task-to-skill decision table** — recognizable task shapes, entry point,
   and expected output.
9. **The epistemic arc** — a Mermaid flow showing routine exit, resumption,
   recon, decision, goal contract, gate, proof, persistence, and delegation.
10. **Skill catalog** — all eleven skills with trigger, purpose, and output.
11. **Installation and compatibility** — one-copy rule, harness matrix, pinned
    v3.0.0 commands, restart/reload requirements, and verification.
12. **Architecture and repository layout** — one canonical skill tree plus thin
    harness manifests.
13. **Trust, evidence, and limits** — deterministic evidence, no-credit
    diagnostics, accepted limitations, and links to the machine-readable record.
14. **Developing and contributing** — tests, DCO, design history, release
    process, and wiki maintainer entry points.
15. **License and support coordinates**.

The README remains comprehensive, but repeated low-level details move behind
clear wiki links when duplication would create a maintenance hazard.

## Source and version policy

- Every stable user page begins with `Applies to v3.0.0` and links to tagged
  source paths.
- Maintainer pages label links to `main` as current development.
- The wiki never uses an unlabeled `main` link to define released behavior.
- Historical audits and evaluations retain their original dates and claims.
- The release risk record controls the wording of behavioral and provider
  limitations.
- The wiki identifies itself as unversioned navigation over versioned sources.

## Required honesty boundaries

Documentation must preserve these v3.0.0 limitations:

- no claim of universal behavioral superiority;
- no claim of cross-provider generality from the incomplete campaign;
- the two genuine P0 behavioral failures remain disclosed;
- AGY quota failures remain availability failures, not merit judgments;
- Cursor compatibility remains `BLOCKED_EXTERNAL` where recorded;
- the amended Gauntlet arbitrator-certification battery remains `NOT_RUN`;
- the post-hoc diagnostic remains `release_credit: none`;
- risk acceptance does not satisfy or waive deterministic, security,
  provenance, review, or publication gates.

## Publication architecture

README and design changes use a normal branch and reviewed pull request against
`main`.

GitHub Wiki content lives in GitHub's separate
`ZMS-Labs/epistemic-skills.wiki.git` repository. Because GitHub has not created
that repository yet, the first page is bootstrapped through the authenticated
GitHub Wiki interface. The wiki repository is then cloned under
`Y:\dev\epistemic-skills.wiki`, populated as one coherent commit, pushed, and
verified from the remote.

Wiki commits use the same authorship and DCO discipline as the main repository,
even though GitHub Wiki does not provide the same pull-request workflow.

## Verification

### Structural checks

- every planned content page exists;
- `_Sidebar.md` links every content page exactly once;
- every sidebar target resolves to a local wiki file;
- wiki-to-wiki links resolve and no content page is orphaned;
- all eleven released skills have exactly one skill guide;
- README local links resolve in the main repository;
- README and wiki contain no mutable stable-install coordinate;
- version text, skill count, and manifest compatibility agree with v3.0.0;
- JSON and Markdown source links point to existing tagged files.

### Content checks

- every skill guide's use boundary agrees with its released frontmatter and
  `SKILL.md`;
- Helix is consistently the central passage and never mislabeled as the
  epistemic router;
- routine work remains the first decision and absent triggers remain silent;
- current limitations match the release record and receive no accidental pass;
- no historical design or audit is described as current certification.

### Publication checks

- the README pull request passes repository CI and independent review;
- the merged README renders correctly on GitHub;
- the wiki remote contains the intended commit and the local clone is clean;
- GitHub renders `Home`, `Helix: Central Passage`, one additional skill page,
  `Installation and Harness Compatibility`, and `Architecture and Contracts`;
- sidebar and footer navigation render on those pages;
- public page URLs are reachable without relying on local state.

## Failure handling

- If Wiki bootstrap fails, do not publish a partial navigation set; correct the
  bootstrap and push the complete wiki from the local source clone.
- If a page or link check fails, fix it before the wiki push or README merge.
- If rendered GitHub output differs materially from local Markdown, correct the
  source and republish rather than documenting the mismatch as acceptable.
- If a released claim cannot be anchored, omit it or label it as uncertain; do
  not infer a guarantee from design intent.
- Git history is the recovery mechanism for both repositories. Published wiki
  corrections use new commits; stable release tags are never moved.

## Non-goals

- changing any skill's behavior, trigger, schema, test, or evaluation result;
- moving or recreating the immutable v3.0.0 release;
- duplicating every design document or evidence packet in the wiki;
- claiming marketplace availability that has not been verified;
- turning the wiki into a generated API reference or an independent contract;
- adding a hosted documentation platform beyond GitHub README and Wiki.

## Completion contract

The work is complete only when:

1. the approved README is merged to `main`;
2. the complete wiki is committed and pushed to the GitHub Wiki repository;
3. structural, content, link, version, and rendered-page checks pass;
4. Helix is visibly and accurately presented as the centralized passage;
5. the original authoritative checkout and unrelated user work remain intact;
6. durable GitHub URLs and commit identities are reported to the operator.
