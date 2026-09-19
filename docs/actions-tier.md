# Continuous integration

The repository defines its checks in `.github/workflows/`. Each workflow names
the contract it validates; the status of one does not establish the others.

The `main-ci-gate` ruleset (ID `23680011`), verified on **2026-09-18**, is active
on `main`. It requires a pull request, resolved review threads, and the three
strict status checks listed below, with no bypass actors. The existing
organization rules continue to prohibit deletion and non-fast-forward updates.
Repository settings can change independently of source; inspect current
settings before relying on this dated observation.

## Read the result at the right level

**Merge protection, release readiness, and diagnostics are different checks.**
The three protected-branch contexts below are the minimum GitHub enforces for
merge. [RELEASING.md](../RELEASING.md) requires broader evidence on the exact
release candidate, including package, contract, wiki, security, and CodeQL
outcomes. A green badge for one workflow does not establish that entire set.

The required mission-custody job is **`contract` on Ubuntu**. Its
**`contract-macos` job is a dispatch-only diagnostic**, outside the required
merge gate. At v7 publication it reproduced the known case-insensitive APFS
failure tracked in [issue #162](https://github.com/ZMS-Labs/epistemic-skills/issues/162).
Its later skipped steps are untested, not passes. Custody exclusion and
filename-distinctness guarantees are unsupported on case-insensitive POSIX
filesystems. See [host coverage](release/v7-host-coverage.md#publication-stage-custody-diagnostic)
and the [exact-release publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/publication-receipt.json)
for the recorded outcome. This known diagnostic does not excuse a new or
unrelated failure.

## Workflow coverage

| Workflow | Job(s) | Trigger | Timeout | What it proves |
| --- | --- | --- | --- | --- |
| `epistemic-flexibility.yml` | `stdlib-checks` | ready PRs + push to `main` + dispatch | 30 min | Python suites, package invariants, and evidence-format checks |
| `commission-watch-contract.yml` | `contract` | ready PRs + push to `main` + dispatch | 30 min | the commission-watch contract |
| `mission-custody-contract.yml` | `contract`; diagnostic `contract-macos` | ready PRs + push, path-filtered; dispatch runs both jobs | 30 min each | required Linux custody behavior; a separate macOS filesystem diagnostic with the limitation described above |
| `wiki-contract.yml` | `snapshot`, `live` | `snapshot` on ready PRs + push + dispatch; `live` on a daily cron and dispatch | 10 / 15 min | current handbook and historical snapshot consistency; separately, published wiki inventory, version labels, and repository links |
| `openai-bundles.yml` | `build` | ready PRs + push, path-filtered; plus published releases and **`workflow_dispatch`** | 15 min | the OpenAI packaging bundles build. The push trigger is path-filtered and will not fire for a docs-only release candidate, so the manual dispatch is how `RELEASING.md`'s exact-candidate bundle evidence gets recorded — do not assume the automatic triggers cover it |
| `release-security.yml` | `full-history-secret-scan` | ready PRs + push to `main` + dispatch | 15 min | no matches from the configured secret rules in scanned history |
| `dco.yml` | `dco` | ready PRs (`pull_request_target`) | 5 min | author-matching sign-offs, subject to the documented DCO exceptions |

The live wiki check does not compare every sentence or image with the recorded
editorial commit. The publication helper binds source identity when staging;
prose accuracy and visual quality still require review.

## Workflow behavior

- **Draft-gated.** Every workflow above lists `ready_for_review` in its
  pull-request event types. Jobs eligible to run on PRs skip drafts; scheduled
  and diagnostic jobs have their own event conditions. As
  `release-security.yml` records in place, the two halves are one mechanism:
  without `ready_for_review`, a PR marked ready would be mergeable having
  executed zero checks, because pressing merge needs no further `synchronize`.
  This was already true before tiering and is unchanged.
- **Cancellation.** Most workflows group pull-request runs on `github.ref`
  and supersede them, while giving each non-pull-request run a group keyed on
  `github.run_id`. DCO and the secret scan use the exceptions below. Both
  parts of the usual pattern matter:
  `cancel-in-progress: false` protects a *running* member of a group but **not a
  pending one** — GitHub replaces a queued run when a newer one joins its group.
  A shared group would therefore let a push to `main` silently discard a queued
  scheduled or dispatched run, with no record that it never happened. The two
  places that would have bitten:
  - `wiki-contract.yml`'s `live` job is a **daily cron alarm** — the only thing
    that would notice someone re-drifting the published wiki through the web UI.
  - `mission-custody-contract.yml`'s `contract-macos` job runs on
    `workflow_dispatch` **only**, so a cancelled dispatch cannot be replaced by
    the push that displaced it. It is the sole macOS diagnostic.
- **`dco.yml` is keyed on the pull request number, not the ref.** It runs on
  `pull_request_target`, which executes in the context of the *base* branch, so
  `github.ref` is `refs/heads/main` for every pull request alike. A ref-keyed
  group would make one PR's DCO run cancel an unrelated PR's.
- **`release-security.yml` has no concurrency group at all**, deliberately. It is
  the full-history secret scan. A secret is introduced by a *commit*, not by the
  tip of a branch, and a scan cancelled halfway is indistinguishable in the UI
  from a scan that found nothing.
- **Bounded.** Every job in every workflow declares `timeout-minutes`. This was
  already true before tiering.

## Required contexts

As verified on 2026-09-18, `main-ci-gate` requires these exact contexts from
GitHub Actions (integration ID `15368`):

- `stdlib-checks`
- `DCO`
- `full-history-secret-scan`

Strict checking requires the branch to be current with its base. Pull requests
must resolve review threads; the required approving-review count is zero, so
this is not a claim of mandatory independent approval. No bypass actors are
configured. These merge controls supplement the existing deletion and
non-fast-forward protections; release gates still require the broader evidence
set in `RELEASING.md`.

Check both rulesets and classic branch protection before renaming a required
job; classic protection is not fully described by a ruleset listing.
