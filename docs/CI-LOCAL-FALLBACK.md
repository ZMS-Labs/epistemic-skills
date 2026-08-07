# Local CI fallback (issue #95)

When GitHub-hosted Actions is unavailable (minutes limits, assignment timeouts, or
org policy), this repository supports **faithful local execution** of the same
Python gates CI runs, without maintaining a second copy of the step list.

## Default path (Linux or WSL)

```bash
bash .github/scripts/run_local_ci.sh [REF]
```

`REF` defaults to `HEAD`. The wrapper:

1. Records the exact commit SHA under `docs/evidence/local-ci/`.
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

After a local run, commit or attach the generated file under
`docs/evidence/local-ci/<sha>.md` when substituting for a failed Actions assignment,
and note the substitution in the PR body.
