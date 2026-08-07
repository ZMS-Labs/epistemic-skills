# Dynamic OpenAI and ChatGPT Bundles Design

## Goal

Make `epistemic-skills` usable through an immediate ChatGPT Personal Skill
upload and ready for the durable OpenAI plugin/marketplace route without
creating a second, hand-maintained inventory or blocking concurrent repository
work.

## Constraints

- `plugins/epistemic-skills/` remains the only canonical package.
- Adding, renaming, or removing a skill must not require editing the builder,
  wrapper, workflow, or manifest inventory.
- Bundles must be revision-bound, deterministic, and fail closed on malformed
  frontmatter or a marketplace path that points away from the canonical tree.
- Pull-request artifacts must identify a durable source commit, not a temporary
  merge-ref SHA whose lifetime is coupled to the PR.
- The immediate upload path must remain honest: uploaded Personal Skills are
  snapshots, not live repository mounts.
- Public directory publication is outside GitHub and must not be represented as
  complete merely because a package builds.

## Architecture

A stdlib-only builder scans direct `skills/<name>/SKILL.md` children, validates
frontmatter, hashes each complete skill subtree, and generates a machine-readable
index. It produces two archives from the same bytes:

1. A single ChatGPT Skill wrapper containing the generated index and the full
   canonical package as supporting resources.
2. A repository-layout plugin bundle containing the existing `.agents`
   marketplace and canonical package paths.

A dedicated GitHub Actions workflow runs tests and builds both artifacts for
relevant PRs, every relevant `main` push, releases, and manual dispatch. On PRs,
the workflow checks out and records the durable PR head SHA; other events use
their event SHA. Checkout, index provenance, and artifact naming share that one
revision value.

## Data flow

```text
plugins/epistemic-skills/skills/*/SKILL.md
                 + package support files
                 + existing manifests
                           |
                           v
             build_openai_bundles.py
                 /                 \
                v                   v
  ChatGPT Personal Skill ZIP   OpenAI plugin ZIP
                \                   /
                 v                 v
                  SHA256SUMS + CI artifact
```

No generated archive is committed. A workflow artifact is always rebuilt from
the checked-out revision, preventing stale binary drift in Git history.

## Validation and failure behavior

The builder rejects an empty skill glob, missing or malformed frontmatter,
frontmatter/directory name mismatch, symlinks, malformed manifests, a marketplace
source other than `./plugins/epistemic-skills`, or a plugin skills path other
than `./skills/`. Archive members are sorted, timestamps fixed, permissions
normalized, and checksums emitted.

Unit tests plant inventory additions, source drift, and malformed frontmatter;
they also compare archive bytes from repeated builds. A separate workflow
contract test prevents PR artifacts from regressing to a temporary merge-ref SHA
or omitting their own test from workflow execution and path triggers.

## Concurrency and future evolution

The implementation lives on an isolated branch. Future work on `main` changes
the next generated artifact automatically because the workflow reads the
canonical package at that revision. If the branch falls behind during review,
normal branch updating resolves source conflicts; there is no copied skill tree
to reconcile.
