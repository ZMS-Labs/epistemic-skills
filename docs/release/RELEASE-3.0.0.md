# epistemic-skills 3.0.0

Status: **HOLD — draft release contract; not published**

This will be the repository's first formal GitHub Release. It will establish
the first immutable, supported snapshot for a package previously distributed
from mutable branches and development-version manifests.

## Intended release meaning

The release will bind all of the following to one commit:

- semantic version `3.0.0` across every live package surface;
- annotated Git tag `v3.0.0`;
- a non-draft, non-prerelease GitHub Release;
- these committed notes and their known limitations;
- deterministic and behavioral evidence identified by the release gate.

Until all five bindings exist and resolve to the same commit, 3.0.0 has not
been released. A branch name, registry contract version, draft note, passing
local test, or mutable `main` checkout is not a substitute.

## Intended highlights

- Proportional routing with a routine-work fast path, two-read micro-recon,
  silent absent triggers, and no process-only artifacts for routine no-ops.
- A three-tier applying-formal-rigor v2 contract in which focused work is
  genuinely smaller in kind and standard is the first full decision-record
  tier.
- Subject-seeded Gauntlet selection with stance anchors, bounded wildcards,
  replayable seed provenance, and non-governing historical telemetry.
- Clear separation between ordinary presentation checks and independent,
  evidence-locked UAT.
- Decision Ledger reuse of adequate durable artifacts instead of duplicate
  persistence.
- Runnable blinded proportionality and formal-rigor evidence protocols with
  explicit BLOCKED/NOT_RUN states where live capability is absent.

## Publication blockers

- Applying-formal-rigor v2 production changes remain gated on a real isolated
  neutral/current-v1 RED result; the deterministic Phase B scaffold alone does
  not satisfy that requirement.
- The pinned blinded proportionality arms have not run in a qualifying isolated
  harness.
- The candidate is not merged to `main`, version surfaces are not aligned to
  3.0.0, and the final release-commit CI/security/publication gates have not
  run.
- No `v3.0.0` tag or GitHub Release may be created while this status is HOLD.

## Compatibility position

3.0.0 is intentionally the first formal support point, not a claim of proven
compatibility with an earlier immutable release. The major version is justified
by material trigger, output-contract, registry, and evaluation changes. The
final notes must identify any installation or contract migration required from
the last rolling pre-release state.

## Evidence required to remove HOLD

Use the gate in `RELEASING.md`. Replace this draft's blockers with immutable
commit, workflow, behavioral-run, independent-review, and secret-scan
coordinates. Do not turn NOT_RUN or BLOCKED scaffolds into release evidence by
renaming them.
