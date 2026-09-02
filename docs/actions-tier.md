# GitHub Actions tier

**Tier: C** — in-repo checks (shared template does not apply)
**Reviewed: 2026-09-02** · **Next review due: 2026-12-01**

2026-12-01 is when this posture must be re-checked, not a date on which
anything was verified. Everything below was established on 2026-09-02.

**These checks are advisory, not a merge gate.** Neither the ruleset nor classic
branch protection requires any status-check context on the default branch, so a
pull request can be merged while the jobs below are failing or have not run at
all. They are worth reading before merging; nothing enforces that anyone did.

## Why the shared template does not apply

The org's Tier C gate templates (`tier-c-gate-python`, `-node`, `-mixed`) live in
the **private** `ZMS-Labs/zms-homelab` repository. `epistemic-skills` is
**public**, and GitHub does not permit a public repository to call a reusable
workflow that lives in a private one. The template cannot be referenced from
here at all, so the Tier C shape is implemented directly in this repo's own
workflows.

There is a second reason it would not fit even if it could be called: this
repo's gates are not one build. They are seven independent contract oracles,
several of which are the only thing standing between a claim and its evidence.
A single consolidated job would hide which oracle failed.

## What the gate runs

| Workflow | Job(s) | Trigger | Timeout | What it proves |
| --- | --- | --- | --- | --- |
| `epistemic-flexibility.yml` | `stdlib-checks` | ready PRs + push to `main` + dispatch | 30 min | the standard-library checks over the skill packs |
| `commission-watch-contract.yml` | `contract` | ready PRs + push to `main` + dispatch | 30 min | the commission-watch contract |
| `mission-custody-contract.yml` | `contract`, `contract-macos` | ready PRs + push, path-filtered to the mission-custody contracts and their specs; the macOS job on dispatch only | 30 min each | the mission-custody contract, on Linux always and on macOS on demand |
| `wiki-contract.yml` | `snapshot`, `live` | `snapshot` on ready PRs + push; `live` on a daily cron and dispatch | 10 / 15 min | that the committed handbook snapshot matches the package, and (daily) that the *published* wiki still does |
| `openai-bundles.yml` | `build` | ready PRs + push, path-filtered; plus published releases | 15 min | the OpenAI packaging bundles build |
| `release-security.yml` | `full-history-secret-scan` | ready PRs + push to `main` + dispatch | 15 min | no secret anywhere in the history |
| `dco.yml` | `dco` | ready PRs (`pull_request_target`) | 5 min | every commit carries a real `Signed-off-by` name and email |

## Tier C properties

- **Draft-gated.** Every workflow above lists `ready_for_review` in its
  `pull_request` types, and every job carries a `draft == false` condition. As
  `release-security.yml` records in place, the two halves are one mechanism:
  without `ready_for_review`, a PR marked ready would be mergeable having
  executed zero checks, because pressing merge needs no further `synchronize`.
  This was already true before tiering and is unchanged.
- **Cancellation, with two deliberate exceptions.** Every PR-triggered workflow
  now declares a `concurrency` group on `github.ref`. Two do not simply cancel:
  - **`release-security.yml` has no group at all.** It is the full-history
    secret scan. A secret is introduced by a *commit*, not by the tip of a
    branch, and a scan cancelled halfway is indistinguishable in the UI from a
    scan that found nothing.
  - **`wiki-contract.yml` cancels only on pull requests.** Its `live` job is a
    daily cron alarm — the only thing that would notice someone re-drifting the
    published wiki through GitHub's web UI. A scheduled run cancelled by a push
    to `main` is an alarm that silently did not fire, which is precisely the
    failure the workflow exists to prevent.
- **Bounded.** Every job in every workflow declares `timeout-minutes`. This was
  already true before tiering.

## Required contexts

The `main` ruleset enforces deletion and non-fast-forward protection only. It
requires **no status check contexts**, and classic branch protection is not
configured (the endpoint returns 404). Check *both* endpoints before changing a
job name here: classic protection is invisible to `/rules/branches`.
