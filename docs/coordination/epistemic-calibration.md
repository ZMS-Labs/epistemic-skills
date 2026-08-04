# Epistemic Skills × Epistemic Calibration coordination charter

> **Frozen baseline:** this charter's body describes the repository as of
> `2d66a27` (v3.0.0-era); update owner: ZMS-Labs epistemic-skills maintainers.
>
> **Amendment 2026-08-04 (operator-authorized):** Phase 2's pilot subjects
> are the **current reality** — the latest immutable release tag (today
> `v4.0.0`) and current development HEAD — not the v3.0.0-era pair the
> frozen body names. Standing rule going forward: **calibration always
> tests the current release + HEAD; past immutable subjects enter a design
> only when a specific claim (regression, transfer, longitudinal) requires
> them.** Phase 0 completed 2026-08-04
> (`2026-08-04-phase0-counterpart-reconnaissance.md`); Phase 1 map:
> `2026-08-04-phase1-inventory-and-map.md`. The body below is otherwise
> retained as written.

**Established:** 2026-07-29  
**Skills subject:** `ZMS-Labs/epistemic-skills` at `2d66a27`  
**Calibration coordinate:** `https://github.com/ZMS-Labs/epistemic-calibration.git`  
**Status:** executable consumer-side contract; calibration-side adoption is not yet verified

## Executive position

`epistemic-skills` is at **3.0.0**, its first immutable support point. The
current branch is post-release documentation/evidence work, not a 3.1 product
line: the package manifests and public installation contract remain 3.0.0.

The products should be coordinated as a producer/consumer pair without merging
their responsibilities:

- **epistemic-skills owns the intervention contract**: triggers, procedures,
  outputs, schemas, deterministic judges, packaging, and honest evidence
  boundaries.
- **epistemic-calibration owns measurement**: versioned corpora, trial
  orchestration, blinded scoring, longitudinal/provider slices, and estimates
  of how those interventions behave.
- Neither repository may silently change the other's contract. Shared work
  crosses through immutable coordinates and an explicit compatibility record.

This is a deliberately loose repository connection. There is no submodule or
runtime dependency: installing the skill package must not pull in evaluation
data or calibration infrastructure, and calibration must test immutable skill
revisions rather than a mutable working tree.

## Where epistemic-skills is now

### Shipped and supported

| Surface | Current state | Authority |
|---|---|---|
| Product version | 3.0.0, first stable immutable support point | `README.md`; `docs/release/RELEASE-3.0.0.md` |
| Package | Eleven skills: router, nine disciplines, and Helix | `README.md` |
| Core operating model | Routine fast path; positive triggers; silent non-events; proportional process | `README.md`; released skill contracts |
| Cross-workflow coordination | Helix pairs epistemic methods with workflow stages but does not replace either router | `plugins/epistemic-skills/skills/helix/SKILL.md` |
| Distribution | Multi-harness package surfaces pinned to v3.0.0 | `README.md`; package manifests |
| Deterministic evidence | Repository test suites cover contracts, proportionality, formal-rigor fixtures, UAT triage, receipts, DCO, JSON, and Gauntlet mechanics | `.github/workflows/epistemic-flexibility.yml` |

### Supported, with bounded claims

The 3.0.0 support promise is about immutable contracts and deterministic
repository checks. It is **not** proof of universal behavioral superiority,
cross-provider generality, human equivalence, or current behavior in every
harness. The release risk record names the accepted gaps.

The V3 formal-rigor post-hoc report says “3.0.0 remains HOLD,” but that sentence
is local to the diagnostic's no-release-credit boundary and predates the later
release authorization/publication sequence. It must not be used as the current
product status. The README and release record are the current public status;
the diagnostic remains evidence with its original limitation.

### Open measurement work that belongs in the relationship

1. Native trigger precision and timing across supported harnesses.
2. False-act and false-hold rates on clean controls and traps.
3. Cross-model/provider and repeated-run behavior without provider/repetition
   confounding.
4. Gauntlet lens and arbitrator calibration on broader seeded corpora.
5. Evidence-locked UAT's transition from `uncalibrated` to the existing
   `calibrated:<corpus-ref>@<date>` vocabulary.
6. Real-world catch rate, correction burden, latency, and token/tool cost.
7. Version-to-version regression and transfer, while retaining negative and
   parody controls.

These are calibration questions. A finding may motivate a skill change, but a
measurement gap alone must not cause evaluation machinery to leak into the
runtime package.

## Blindspot pass

### Landmines

- “Connect the repositories” could mean a Git submodule, a runtime dependency,
  shared source, a Git remote, or a governance relationship. Only the last two
  preserve the package/evidence boundary; a submodule would couple installs to
  a changing corpus.
- This checkout initially had no Git remotes, and network access could not
  verify the calibration repository. The coordinate above is therefore an
  operator-supplied naming inference, not an observed calibration-side fact.
- The word *calibration* already has several scopes here: UAT seeded-defect
  status, Gauntlet telemetry, fixture smoke checks, and broad behavioral
  measurement. Treating them as one score would erase their populations and
  validity limits.
- Green deterministic checks do not estimate behavioral effectiveness. The
  release documentation explicitly separates immutable support from universal
  behavior claims.
- The current README estate header says `maintenance` and portfolio role
  `none`. Cross-product coordination must not silently override that external
  lifecycle authority.

### Hidden context

- The collection audit already rejected “calibration reader” as another skill;
  calibration should be machinery consumed at existing decision points, not
  runtime ceremony (`docs/audits/2026-07-22-collection-audit/06-gap-analysis.md`).
- UAT already defines a closed calibration status and transition shape, but
  intentionally lacks the corpus that would authorize the transition
  (`plugins/epistemic-skills/skills/evidence-locked-uat/references/schemas.md`).
- Existing release evidence contains useful trials but also missingness,
  same-family correlation, and provider/repetition confounding. Calibration
  must preserve those limitations rather than normalize them away.
- Helix's core division is useful here: workflow executes work; epistemic
  skills define what warrants belief. Calibration is a third concern—measuring
  whether those epistemic interventions work in specified populations—not a
  replacement strand inside Helix.

### What good looks like

- The 3.0.0 risk-acceptance JSON gives every accepted gap an owner, scope,
  revisit trigger, and exit criterion rather than a blanket waiver.
- Formal-rigor evaluation artifacts pin subjects, prompts, judges, attempts,
  missingness, and no-retry boundaries, allowing later interpretation without
  rewriting the historical result.
- UAT's calibration vocabulary requires a corpus reference and date instead of
  permitting an ungrounded `calibrated` boolean.

### Questions you should be asking

1. **Is epistemic-calibration already public and canonical at the named URL?**
   Best guess: yes, but this environment could not verify it; adoption remains
   blocked on a calibration-side immutable reference.
2. **Which product owns shared schemas?** Best guess: the repository that
   produces the artifact owns its schema; the consumer pins and validates a
   version, avoiding a third shared-source package for now.
3. **Should calibration results gate skill releases immediately?** Best guess:
   no. Start in observational mode, preregister thresholds, then promote only
   stable metrics with adequate controls to release gates.
4. **What is the first joint slice?** Best guess: UAT seeded-defect calibration,
   because epistemic-skills already exposes an explicit status transition and
   missing-corpus blocker.
5. **Does coordination change the maintenance lifecycle?** Best guess: no; it
   establishes interfaces and evidence intake. Lifecycle changes require the
   estate authority named in `README.md`.

## Product boundary and compatibility contract

### Ownership

| Concern | epistemic-skills | epistemic-calibration |
|---|---|---|
| Runtime trigger/procedure semantics | **owns** | consumes immutable subject |
| Runtime schemas and judges | **owns** | validates and reports exact versions |
| Corpus cases, labels, sampling frames | supplies testable contract requirements | **owns** |
| Trial execution and raw run evidence | supplies adapters where necessary | **owns** |
| Behavioral estimates and uncertainty | receives; does not inflate | **owns** |
| Product change decision | **owns** | recommends with evidence |
| Calibration methodology change | consulted when product meaning is affected | **owns** |

### Immutable exchange unit

Every cross-repository result must validate against
`plugins/epistemic-skills/contracts/epistemic-product-calibration.schema.json`
and carry at least:

```json
{
  "protocol": "epistemic-product-calibration@1",
  "producer": {"repo": "ZMS-Labs/epistemic-calibration", "revision": "<full SHA>"},
  "subject": {
    "repo": "ZMS-Labs/epistemic-skills",
    "revision": "<full SHA>",
    "version": "<semver>",
    "skill_or_surface": "<stable-slug>"
  },
  "contract_revision": "<tested contract>",
  "corpus": {"ref": "<path>", "revision": "<full SHA>", "sha256": "<hash>"},
  "runner": {"ref": "<path>", "revision": "<full SHA>", "sha256": "<hash>"},
  "execution": {"models": ["<pin>"], "harnesses": ["<pin>"], "started_at": "<RFC3339>", "completed_at": "<RFC3339>"},
  "sampling_frame": {"population": "<scope>", "planned": 1, "observed": 1, "excluded": 0, "missing": 0},
  "preregistration": {"ref": "<path>", "revision": "<full SHA>", "sha256": "<hash>"},
  "result": {"ref": "<path>", "revision": "<full SHA>", "sha256": "<hash>"},
  "status": "observed",
  "limitations": ["<validity limit>"],
  "never_attests": ["behavioral-merit-by-envelope", "statistical-validity-by-envelope", "release-readiness-by-envelope"]
}
```

The receiving repository records a pointer, interpretation, and disposition;
it does not copy mutable “latest” results or claim more than the sampling frame
supports. Corrections append or supersede—they do not rewrite historical
evidence.

### Change protocol

1. **Propose:** open a paired issue or design record naming both repositories,
   exact affected contracts, owner, and desired decision.
2. **Freeze:** pin the skill subject, corpus, runner, preregistration, and
   scoring contract before empirical execution.
3. **Run:** calibration retains attempts, failures, missingness, environment,
   and raw/derived evidence under immutable coordinates.
4. **Receive:** epistemic-skills independently verifies hashes, schema, subject
   identity, and claim scope before accepting any conclusion.
5. **Decide:** classify the result as no change, docs/claim correction,
   contract change, behavioral candidate, or release-gate candidate.
6. **Land independently:** each repository merges its own change with reciprocal
   immutable links. Neither merge depends on an unmerged branch in the other.
7. **Recalibrate:** contract or behavior changes invalidate only the explicitly
   affected measurements; the compatibility record states what remains usable.

## Phased coordination plan

### Phase 0 — establish the link (now)

- Treat `ZMS-Labs/epistemic-calibration` as the named measurement counterpart.
- Add a local `calibration` Git remote when the repository is reachable:
  `git remote add calibration https://github.com/ZMS-Labs/epistemic-calibration.git`.
- Obtain and record its default branch, HEAD SHA, lifecycle owner, current
  schemas, corpora, runners, and claims. Until then, all calibration-side state
  is **unknown**, not absent.
- Ask that repository to adopt or counter-propose `epistemic-product-calibration@1`.
- Give it the schema, valid fixture, negative fixtures, and stdlib verifier in
  `plugins/epistemic-skills/contracts/`; its first producer record must pass the
  same verifier in both repositories.

**Exit:** reciprocal immutable references and named owners exist in both repos.

### Phase 1 — inventory and map

- Create a matrix of each skill/surface to available corpus, runner, judge,
  harness, metric, and validity status.
- Import no results yet; identify duplicates, gaps, incompatible vocabularies,
  and hidden shared dependencies.
- Reconcile the calibration repo's roadmap with the accepted 3.0.0 risks and
  open audit findings.

**Exit:** every claimed measurement has a subject revision and sampling frame;
every high-priority product gap has an owner or explicit hold.

### Phase 2 — one end-to-end pilot

- Pilot evidence-locked UAT seeded defects against the latest immutable
  release tag and current development HEAD as separate subjects
  *(amended 2026-08-04 from "immutable 3.0.0": test current reality — see
  the amendment banner)*.
- Preregister expected planted-defect catches, clean-control false holds,
  thresholds, exclusions, and what would *not* authorize `calibrated`.
- Return an exchange-unit record and independently verify it here.

**Exit:** reproducible cross-repo result, including at least one positive and
one negative control; no product claim exceeds the evidence.

### Phase 3 — broaden observational calibration

- Add trigger/skip proportionality, formal-rigor semantic validity, Gauntlet
  lens/arbitrator behavior, continuity recovery, and outsource receipt
  behavior.
- Cross providers, harnesses, repetitions, and judges where claims require it;
  report missingness and correlated seats.
- Maintain longitudinal results by immutable product version.

**Exit:** versioned dashboards/reports can distinguish structural conformance,
semantic merit, availability failure, and population uncertainty.

### Phase 4 — promote selected gates

- Promote only preregistered, stable, independently reproducible measures.
- Put the threshold, corpus class, validity window, exception authority, and
  rollback rule in both repositories.
- Keep exploratory metrics non-governing.

**Exit:** accepted gates fail closed without turning proxy improvement into the
product objective.

## Formal decision record

- **Question:** How should two separately versioned products coordinate while
  preserving runtime-package independence and measurement validity?
- **Tier:** standard; this is a persistent cross-repository interface with
  multiple viable coupling models.
- **Alternatives:** merge calibration into skills; Git submodule/runtime
  dependency; informal links; immutable protocol with independent repos
  (**selected**); status quo (no coordination).
- **Hard constraints:** 3.0.0 remains immutable; no runtime dependency on
  calibration; evidence remains revision-bound; claims retain population and
  uncertainty; each repository controls its own releases.
- **Authorized objective:** coordinate the products “as they ought to be” while
  starting from the user's belief that skills is at 3.0. The priority rule is
  constraint-satisfaction, then minimize coupling and maximize traceability.
- **Derivation:** merging or submodules violate independence and versioning;
  informal links/status quo do not give identity, compatibility, or correction
  custody; an immutable exchange protocol satisfies the constraints and leaves
  either repository free to evolve.
- **Outcome:** `conditional` selection of the independent-repository protocol.
  It becomes bilateral only when the calibration repository verifies its
  coordinate and adopts or revises the contract.
- **Concessions:** more coordination overhead and duplicated validation logic;
  recovery is a small shared schema package only after two real consumers prove
  duplication is costlier than another compatibility surface.
- **Property reconciliation:** P1 fired (exchange invariants); P2 not applicable
  (no shared mutable datastore); P3 not applicable (no concurrent shared writes);
  P4 not applicable (no replication protocol); P5 fired (supersession and
  recovery); P6 not applicable to this public-metadata design; P7 not
  applicable; P8 unmapped (calibration populations and statistical methods are
  unobserved); P9 fired (versioning, compatibility, lifecycle).

## Rewritten request and next handoff

> Verify the canonical `ZMS-Labs/epistemic-calibration` repository and freeze
> its current revision. Compare its actual ownership, schemas, corpora, runners,
> roadmap, and evidence claims with epistemic-skills 3.0.0's supported contract,
> accepted risks, and open measurement gaps. Counter-propose or adopt
> `epistemic-product-calibration@1`, land reciprocal immutable references, then
> plan one preregistered UAT seeded-defect pilot. Do not merge repositories,
> introduce a runtime/submodule dependency, change estate lifecycle, or promote
> a metric to a release gate during the pilot.

Next workflow stage: calibration-side reconnaissance, followed by bilateral
design review of a frozen revision. If that review changes this interface
materially, update this charter before implementation.
