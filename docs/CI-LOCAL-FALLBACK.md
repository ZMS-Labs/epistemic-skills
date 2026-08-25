# Local CI fallback (issue #95)

When GitHub-hosted Actions is unavailable (minutes limits, assignment timeouts, or
org policy), this repository supports **faithful local execution** of the same
Python gates CI runs, without maintaining a second copy of the step list.

## Default path (Linux or WSL)

```bash
bash .github/scripts/run_local_ci.sh [REF]
```

`REF` defaults to `HEAD`. The wrapper:

1. Writes a receipt **outside the repository** —
   `${LOCAL_CI_RECEIPT_DIR:-${TMPDIR:-/tmp}/epistemic-skills-local-ci}/<sha12>-tree-<tree12>[-dirty].md`
   — naming both the commit and the tree it actually tested.
2. Runs `.github/scripts/cleanroom_ci.sh` for the `epistemic-flexibility` workflow
   (stdlib checks extracted from `.github/workflows/epistemic-flexibility.yml`).
3. Runs the focused `commission-watch-contract` steps when present on `REF`.

Use this **before** pushing when Actions is degraded. It is the standing substitute
for “green on GitHub” only when Actions cannot assign runners; prefer Actions when
available for CodeQL, DCO API checks, and fork isolation.

## Clean-room only

```bash
bash .github/scripts/cleanroom_ci.sh "$(git rev-parse HEAD)"
```

See the script header for remote URL override and detached-checkout behavior.

## Kubernetes Job (cluster path)

`.github/ci/cleanroom-job.yaml` schedules the same clean-room harness on amd64.
**Blocker (2026-08-06):** pods could not resolve `github.com` (cluster egress/DNS).
Fix cluster DNS/egress or clone from an in-cluster mirror before relying on this path.

## What local CI does not provide

- Cross-operator independence (same machine as the author).
- CodeQL or other GitHub-only integrations.
- **Self-hosted Actions runners on a public repo** without fork-PR protections —
  not approved as a billing workaround (see issue #95).

## Receipts

The receipt lands **outside the repository**, at
`${LOCAL_CI_RECEIPT_DIR:-${TMPDIR:-/tmp}/epistemic-skills-local-ci}/<sha12>-tree-<tree12>[-dirty].md`.
That is deliberate: the file describes a WORKING TREE, not a commit, so a copy
sitting inside the repo was one `git add -A` away from being committed as if it
described the commit it is named for (it happened twice during v6.0.0 and was
caught by hand both times). `docs/evidence/local-ci/` is `.gitignore`d for the
same reason and is **not** a publication path.

When substituting for a failed Actions assignment: paste the receipt body into
a PR comment (it is small, and a comment is timestamped and attributable), and
note the substitution in the PR body. A `-dirty` receipt is not a substitute for
green on a commit — re-run it on a clean tree first.

Override the destination with `LOCAL_CI_RECEIPT_DIR` if you want the file
somewhere durable outside the checkout.
