# Local CI: useful checks, explicit limits

Use local checks for fast feedback or when GitHub Actions cannot run. The
clean-room harness extracts Python commands from `epistemic-flexibility.yml`
so its step list follows that workflow. It reports which commands ran, failed,
or were skipped. **Exit zero means the executed checks passed; it does not mean
all hosted gates were reproduced.**

For a small change, start with the targeted checks in the
[maintainer change map](MAINTAINING.md#change-map). The broader local wrapper is
useful before pushing a substantial change or diagnosing a CI failure.

## Run the wrapper on Linux or WSL

Use Git, Bash, and Python 3.12 to match the main hosted Python baseline. The
scripts use the available local interpreter; they do not install or pin it.

```bash
bash .github/scripts/run_local_ci.sh HEAD
```

`REF` is an optional first argument and defaults to `HEAD`. The wrapper has two
distinct inputs:

| Part | What it reads | What it does |
| --- | --- | --- |
| Clean-room checks | A fresh detached checkout of the resolved `REF` commit | Extracts the Python commands from that revision's `epistemic-flexibility.yml`, executes supported commands, and reports skips |
| Focused watch checks | The current working tree, when its watch workflow exists | Runs the watch contract tests and verifier, examples, sentinels, description budget, package structure checks, and `git diff --check` |

Use a clean checkout of `REF` so both parts describe the same revision. Changing
`REF` alone does **not** switch the wrapper's working-tree portion to that ref.
The watch portion is a selected set of commands, not an extraction of every step
in `commission-watch-contract.yml`.

## Read the skip counts

The clean-room summary accounts for every extracted Python command. It can
finish successfully while reporting these exclusions:

| Summary field | Why a command did not run |
| --- | --- |
| `ci-context` | It needs GitHub event or runner variables that the local process does not have. |
| `missing-dep` | Its workflow block installs PyYAML, but the local interpreter cannot import it. The harness does not install it automatically. |
| `need-args` | The command returned an argparse usage error because it requires arguments the harness did not supply. |

These are uncovered checks, not successful checks. Read the command named next
to each `SKIP`, and include any relevant gap when reporting the result. A failed
executed check returns nonzero. The clean-room harness replicates Python script
commands from one workflow; it does not reproduce action setup, every shell
command, or the complete GitHub environment.

## Clean-room checks only

```bash
bash .github/scripts/cleanroom_ci.sh "$(git rev-parse HEAD)"
```

The standalone script defaults to `main` when no ref is supplied. A locally
available commit is copied into a fresh detached checkout; otherwise the script
clones the named remote branch or tag. Its second argument can override the
remote URL. It also fetches remote `main` for checks that compare history, so
network access is required. See the
[script header](../.github/scripts/cleanroom_ci.sh) for temporary-directory
configuration and checkout behavior.

The optional [Kubernetes Job example](../.github/ci/cleanroom-job.yaml) runs the
harness on amd64 compute with cluster access, DNS, and outbound GitHub access.
Review its image, permissions, and resources before use. No particular cluster
or deployment environment is a project dependency.

## What hosted checks still add

The local wrapper does not cover all mission-custody checks, OpenAI bundle
packaging, wiki publication/link verification, full-history secret scanning,
CodeQL, or the live pull-request DCO API check. It also does not provide another
operator's environment or GitHub's fork isolation. Some individual checks can
be run locally; the wrapper's success does not claim they were.

When Actions is unavailable, attach the bounded local result to the PR and
identify the outstanding hosted checks. Local receipts do not automatically
satisfy branch protection or replace the exact-candidate evidence required by
[the release procedure](../RELEASING.md). The original fallback discussion is
[issue #95](https://github.com/ZMS-Labs/epistemic-skills/issues/95); self-hosted
runners on a public repository without fork-PR protections are not an approved
billing workaround.

## Receipts and privacy

The wrapper writes outside the checkout by default:

```text
${LOCAL_CI_RECEIPT_DIR:-${TMPDIR:-/tmp}/epistemic-skills-local-ci}/<sha12>-tree-<tree12>[-dirty].md
```

The receipt records the resolved commit, a working-tree hash, host information,
commands, and results. Remember that the clean-room portion tests the commit
while the watch portion tests the working tree. A `-dirty` receipt cannot
establish that the corresponding clean commit passed. Re-run in a clean
checkout when commit-bound evidence is needed.

Keep the original receipt local. When sharing it in a PR, remove hostnames,
home directories, and other personal identifiers; retain command outcomes and
skip counts. `docs/evidence/local-ci/` is ignored and is not a publication path.
`LOCAL_CI_RECEIPT_DIR` can select another receipt directory outside the checkout.
