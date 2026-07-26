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
- Repeated fresh formal-rigor epochs established a provider-contract blocker
  for the frozen Cursor arm. The live CLI offers transport formats but no
  schema-constrained response mode. Terminal-boundary, concision, syntax-check,
  and bounded-control prompt changes closed individual failures, but at source
  `fb6c914` the `fc-02` control passed 9/9 before Cursor `candidate` run 3 for
  `mt-03` remained unparseable. The retained root is
  `C:\tmp\formal-rigor-final-fb6c914`, content pin
  `6395c596b66a545d604af2457e17a551664f485636880ed267a5926d5cf07cce`.
  This gate is `BLOCKED_EXTERNAL`. The operator-authorized prospective
  `noncursor-degraded-v1` protocol may change the Cursor item from release
  blocker to known limitation only after one complete, content-pinned new epoch
  passes every unchanged gate. It uses 286 fresh terminal arms and 132 fresh
  terminal isolated semantic seats, with no Cursor or Fleet Cursor call; a
  partial, repaired, resumed-after-terminal-failure, mixed-protocol,
  substituted, or historical root cannot qualify. Until that epoch exists, the
  formal gate remains blocking and this release stays HOLD. Its exact evidence
  claim boundary is two-provider blinded conformance only: it does not claim
  three-provider robustness or Cursor reliability.
- The first fresh `noncursor-degraded-v1` epoch at source
  `fb19e9e9d2ee97b23d8408f54652fe2d86eb6a02` is excluded. Its canonical root
  `C:\tmp\formal-rigor-noncursor-fb19e9e` is content-pinned as
  `2b28b75b18adcab2e41faa2b375641b8e0fee2737de52ed3c0a14adabdff9c13` using
  the repository's sorted path/file-SHA-256 manifest algorithm. It recorded
  286 terminal calls: 285 parseable, 281 transport-schema-valid, four
  parseable-but-schema-invalid (`empirical_closure.tests` objects where strings
  are required), and one nonparseable self-talk/multiple-envelope response.
  It has no scoring, semantic, or release credit and must not be retried,
  repaired, resumed, or reused. The frozen Cursor blocker and prospective
  protocol remain unchanged.
- The completed `noncursor-degraded-v1` epoch at source
  `a18e8ba41085c7d45b126e342b3222a19e497bc6` is also excluded. Its canonical
  root pin is
  `11eecc3d589a88ccb19dc5117a2a0cfdd5019252f4bc5c528a98581c61efbe5a`.
  Of 286 terminal calls, 281 qualify and five fail unchanged gates: two raw
  telemetry user-profile-path leaks (one agy and one Codex; final response
  objects were clean), two agy strict-schema violations (v1-style record shape
  and object `uncertainty_posture` where a string is required), and one agy
  self-talk/fenced multi-draft response with two identical schema-valid
  envelopes. It has no scoring, semantic, or release credit and may not be
  retried, repaired, resumed, or reused. `noncursor-degraded-v2` is a distinct
  prospective protocol; release remains HOLD until a complete v2 epoch passes
  every unchanged gate. Its campaign and call provenance must retain canonical
  packet root and execution policy; frozen and v1 identities are inspectable
  but non-runnable under current source and require pinned historical commits.
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
- The completed `noncursor-degraded-v2` epoch at source
  `54d3bae4fe51a69cd9cab7658d703d695073006b` is excluded. Its root
  `C:\tmp\formal-rigor-noncursor-v2-54d3bae` has canonical pin
  `ce8c7253c8bc2a18f93a2591a4566295b9d69468a4bc7911760bc182309397b0`.
  It recorded 286 terminal arms: 154 qualifying Codex calls and 132 failed agy
  calls. Every agy failure records `--model gemini-3.1-pro-high conflicts with
  --effort=medium`, a systemic provider configuration incompatibility before
  model execution. V2 has no structural score, semantic, or release credit and
  may not be retried, repaired, resumed, or reused.
  `noncursor-degraded-v3` is distinct and prospective: a fresh source/root plus
  AGY 1.1.7 version/catalog/suffix capability preflight and receipt are
  required before it runs. Its exact matrix is arms: Codex
  `gpt-5.6-sol`/high and agy `gemini-3.6-flash-medium`/medium; semantic: Codex
  `gpt-5.6-sol`/high and agy `gemini-3.1-pro-high`/high; Cursor is
  zero/unavailable. The AGY preflight is not a Codex catalog claim: Codex has
  the narrow V2 basis of 154/154 qualifying calls under the same
  `gpt-5.6-sol`/high binding, while V2 remains excluded. Release remains HOLD
  unless a complete v3 epoch passes every unchanged gate.

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

## Completed excluded `noncursor-degraded-v3` epoch

The `noncursor-degraded-v3` root at source
`693c0fb26fa4e0c4f54e63b52497783c4ce60131` is
`C:\tmp\formal-rigor-noncursor-v3-693c0fb`, with canonical evidence-root pin
`87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1`.
It has 286 terminal arms and only 204 qualifying calls: Codex is 154/154
qualifying and AGY is 50/132 qualifying. The 82 invalid AGY calls are eleven
completed nonparseable outputs, four AGY-internal timeouts at about 302 seconds,
and 67 quota failures. The eleven retained raw outputs are duplicate valid JSON
frames, not one final object: eight have two byte-identical frames, two have
three, and one has five; none has divergent frames. The frozen fail-closed
transport rule therefore rejects them.

This whole root is excluded: no structural score, semantic adjudication, or
release credit; no retry, repair, resume, or reuse. Release remains **HOLD**.
Cursor remains zero/unavailable and provides no qualifying result.

After quota reset, the only contemplated next step is a separately
preregistered, bounded AGY transport pilot using AGY 1.1.7, the exact v3 phase
models, `--output-format json`, `--print-timeout 10m`, and runner
`--timeout-seconds 720`. The 720-second outer timeout exceeds the 600-second
internal wait, avoiding an outer-kill race and preserving terminal evidence.
The pilot retains byte-preserving raw evidence and fail-closed one-final-object
criteria. Only a passing pilot may justify a fresh V4/full root; it does not
repair V3. Fleet bridge audit does not
provide a substitute: the Gemini bridge ignores selected model/effort and
likely shares quota, while Ollama `qwen2.5` 7B is exploratory only, not release
evidence.

## V3 post-hoc diagnostic remains non-release evidence

The separately preregistered diagnostic at implementation commit
`a7c72933d2dc60979a1607a47cfe7e5747c84cbe` examined retained content from the
excluded V3 root without modifying or promoting it. The source pin remained
`87e7a615927b4e4148ae5d79677d78166c2aeb8ded294d79ff4dfaf204af29b1`;
the final diagnostic-root pin is
`35283d05bc288271a7c963fecada9854f03336ff2985eed47cfb00f4c717f252`.

The diagnostic structurally scored 215/286 planned responses, including 11
byte-identical repeated-frame views, and found 100/215 structural passes.
Candidate structural passing was 49/65 available responses. Of 130 semantic
seats, 42 Codex seats were valid and 88 AGY seats terminated on quota before
model output. The 21 Google-origin candidates judged by Codex yielded 19
semantic passes and two genuine P0 failures. The 44 OpenAI-origin candidates
had no valid AGY judgment: 22 P1 cases remain arbitration-required and 22 P0
cases are availability-driven fail-closed outcomes, not semantic invalidity.
The aggregate report's verdict map counts only the 42 valid parsed
adjudications, and its 24 P0 findings combine two merit failures with 22 quota
outcomes; neither field establishes 24 semantic invalidities.

Observed structural controls do not establish broad polarity, three AGY parody
arms are absent, semantic controls were not judged, and the two seats per
candidate are correlated same-provider observations. These results are
diagnostic-only, award `release_credit: none`, do not qualify or repair V3, and
do not satisfy any 3.0.0 gate. Release status remains **HOLD**. The full
accounting also records the perfect confounding: repetitions 1 and 3 are
OpenAI-origin and AGY-judged, while repetition 2 is Google-origin and
Codex-judged. Independent review found no Critical issue and conditionally
approved the corrected,
non-promotional interpretation with these limitations retained. It is in
`docs/release/evidence/2026-07-26-formal-rigor-v3-posthoc-diagnostic.md`.
