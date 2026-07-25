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

- The required pre-production applying-formal-rigor RED is established under
  `plugins/epistemic-skills/skills/applying-formal-rigor/evals/formal-rigor-v2-fixtures/results/2026-07-24-red-baseline/`:
  neutral passed 4/22 structurally and current-v1 passed 1/22 structurally.
  A later candidate diagnostic at source
  `0e3b0e203acbe3829032e702c047b35903d1c021` completed 22/22 parseable calls
  but failed structurally at 18/22. Its evidence root is
  `C:\tmp\formal-rigor-canonical2-0e3b0e2`, content pin
  `d787ff560e5908c72839842484878ed179ff4f6e09f56cee8d588c49ca6d94cd`.
  The retained misses were an over-escalated `cc-03` tier, a missing adequate
  P7 module for `mt-01`, a contract-disputed P7 classification for `um-01`,
  and missing P6 engineering coverage for `um-02`. Semantic adjudication was
  not run after structural failure. Candidate GREEN requires a qualifying new
  pinned campaign, not relabeling or repairing this epoch; all candidate
  repetitions, six parody arms, and independent semantic gates remain
  release-blocking.
- The pinned isolated proportionality protocol has completed. Final candidate
  `b73b04af46255bddf103a3f7e80e69b442ebddab` passed all three repetitions:
  routine `10/10`, material `4/4`, high-risk `4/4`, with routine narration
  medians `7`, `6.5`, and `6` words. The canonical evidence root is
  `C:\tmp\proportionality-final-7cdf6fc`, content pin
  `11168ef457764778be19c5ace54f3f263621f260377e4bbf9c87eb281b8d2e59`.
- The corrected parody epoch is
  `C:\tmp\proportionality-parody-correction-15cce7e`, content pin
  `cb5a8d7f64d7ec78321005a938bbf040d99af62e316a932522b8c37180c97d4c`;
  both `full-ceremony` and `always-routine` fail as required. Retained `main`
  and PR #46 failures remain comparative evidence. The uncorrected parody
  output and all canary, partial, source-exposed, or other diagnostic roots are
  excluded from release evidence.
- The release subject is not merged to `main`; live package/version surfaces
  still report `2.9.1`; and the complete deterministic, DCO, CodeQL,
  manifest-parity, committed-JSON, full-history secret-scan, and publication
  checks have not passed on the exact release commit.
- The final independent Helix/Gauntlet publication review remains incomplete.
  Release status therefore remains **HOLD**.
- No `v3.0.0` tag or GitHub Release may be created while this status is HOLD.

## Compatibility position

3.0.0 is intentionally the first formal support point, not a claim of proven
compatibility with an earlier immutable release. The major version is justified
by material trigger, output-contract, registry, and evaluation changes.

### Migration from the rolling pre-release

- Replace existing plugin or skill copies; do not layer a second installation
  mechanism over an existing one. Reload the harness or start a fresh task
  after upgrading.
- Codex users must rerun the Gauntlet role renderer after upgrading, using the
  `3.0.0` cache path.
- Routine work and absent triggers are now silent: integrations must not
  require router records, Helix skip inventories, role calls, or process-only
  artifacts for the routine path.
- Applying-formal-rigor output is tiered. Focused work is inline, limited to six
  bullets or 250 visible words, and emits no persistent record; standard and
  high-assurance work use `formal-rigor-record@2`. Consumers of the prior
  seven-lens or unstructured output must update.
- `theory-battery.md` remains as a compatibility index for existing links. No
  repository data migration is required; the breaking changes are installation,
  trigger, output-contract, and evaluation-contract changes.

## Evidence required to remove HOLD

Use the gate in `RELEASING.md`. Replace this draft's blockers with immutable
commit, workflow, behavioral-run, independent-review, and secret-scan
coordinates. Do not turn NOT_RUN or BLOCKED scaffolds into release evidence by
renaming them.
