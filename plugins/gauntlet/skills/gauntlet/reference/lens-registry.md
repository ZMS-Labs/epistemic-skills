# Lens registry — model, lifecycle, selection, and expansion policy

The canonical roster is **`roster/registry.json`** (schema: `roster/lens.schema.json`).
Every human-readable roster file and every count is **generated** from it by
`scripts/render_roster.py`. Hand-editing a generated file is drift; the validator fails on it.
Counts live in one place: `roster/INDEX.md` (generated).

## What counts as a distinct lens

A lens is distinct only when it differs materially on **all** of:
object of scrutiny · evidence signature · causal/failure mechanism · output + observable
falsifier · selection conditions/exclusions. **Persona flavor is not novelty.** Domain
similarity is not automatically overlap, but a domain specialization must demonstrate a
distinct diagnostic mechanism. Opposing ideological presets (e.g. `cloud-native-purist` /
`local-first-survivalist`) are counter-modes: one `mutex_group`, one diversity unit,
co-selected only with a recorded intentional contrast.

## Workflow roles (the pipeline, replacing the old "five groups" mental model)

1. **generate_options** — pre-panel, open questions only. 1-2 generators produce 3-5
   materially distinct alternatives **always including the null/status-quo option**
   (`option-set@1`). Their output feeds the DeepReason docket/hypothesis set; evaluators
   then inspect the generated alternatives. **Generator runs never satisfy evaluator-panel
   diversity.**
2. **evaluate** — the panel seats. Only these count toward stance/capability diversity.
3. **gate** — categorical/process checks that can block regardless of weighing
   (`governance-lawyer` = panel-process conformance; `red-lines-arbitrator` = categorical
   pre-optimization bounds).
4. **adjudicate** — consumes the record. `pragmatic-judge` is the **default final judge**;
   `bayesian-adjudicator` is the alternate **only when defensible priors/likelihoods exist**;
   `dialectical-synthesizer` generates pre-judgment synthesis candidates and **never rules**;
   `sovereign-ruler` rules only on values **recorded in the frozen dossier** — otherwise it
   emits an operator-choice memo.

The old Group E is not a fifth evaluator stance; it is the option-generation phase.
The premortem protocol (independent participant narratives before cross-talk) is a panel
*methodology* — the gauntlet's independent-lens barrier implements it — not a lens
(see `premortem-facilitator`, retired).

## Output contracts (canonical, used by bases, agents, and the workflow schema)

- **option-set@1**: option · assumptions · evidence/hypothesis status · differentiators ·
  upside · risks · cheapest discriminator test · kill criterion.
- **finding-set@1**: stable finding id · claim · P1-P4 · evidence refs (tiered) · reasoning ·
  hypothesis impact · observable falsifier {statement, method, threshold, timeframe} ·
  impact · proposed action.
- **ruling-set@1**: conflict ledger · evidence weights · UPHELD / OVERRULED /
  UPHELD-WITH-QUALIFICATIONS / SPLIT · preserved dissent · P1-P4 decisions ·
  acceptance criteria · computed verdict · next action.

## Evidence tiers (replaces the old [V path:line]-only rule)

- **[V path:line]** — directly verified source/probe evidence (mechanically checked by
  `scripts/verify_evidence.py`).
- **[I <- Vref]** — inference derived from cited verified evidence (names its [V] anchors).
- **[H]** — unverified hypothesis; carries zero weight at arbitration.

Accepted factual claims require [V] or [I]-anchored evidence. A falsifier must be
structurally observable (method + threshold + timeframe), not merely a non-empty string —
enforced by the validator on cards and by the workflow schema on findings.

## Lifecycle

`candidate -> probation -> active -> deprecated -> retired`

- **candidate**: complete fingerprint, never selectable. Promotion requires the behavioral
  admission gate (below).
- **probation**: seated automatically in the dedicated SHADOW seat (one per run,
  additional to the panel, standard/deep/max, default ON, rotation-balanced by prior
  seatings in runs/ledger.jsonl — fewest-seated first, id tie-break). Never holds a core
  seat, and its findings are EXCLUDED from arbitration/verdict (shadow semantics —
  unvalidated lenses never touch decisions; telemetry unconfounded by panel-size).
  Track unique upheld yield, duplication, unsupported evidence, false-high strikes,
  falsifier quality, operator overrides, tokens — via the run ledger (SKILL.md Step 9).
  **Thresholds below are REVIEW TRIGGERS, never automatic actions** (external-review
  adjudication 2026-07-14): the review weighs sample-size uncertainty, case mix, domain
  opportunity counts, false-high rate, and corroboration value — a lens is not promoted
  for crossing an administratively convenient integer. Flag review after 20 eligible
  runs or quarterly (`scripts/lens_stats.py`).
- **deprecate/merge** review-trigger when duplicate rate > 70% and unique upheld yield
  < 0.1/run, unless rare-critical coverage is explicitly documented. **Duplication is
  not uniformly waste**: distinguish (a) correlated waste — same evidence, same fix,
  same reasoning; (b) independent corroboration — same conclusion via a different
  evidence chain (VALUABLE on P1/P2, do not penalize); (c) apparent duplication hiding
  mechanism disagreement (surface it, don't merge it). Only (a) counts against a lens.
- **retired**: ID and card preserved forever (historical runs replay by id+version);
  `superseded_by` mandatory. Never delete an ID.

## Admission gate for candidates (behavioral — NOT YET RUN for any candidate)

Static fingerprint completeness is necessary, not sufficient. Activation requires paired
blind evaluation vs the nearest neighbor on >= 8 eligible dossiers with: >= 1 unique upheld
P1/P2 absent from the neighbor on >= 2 dossiers; >= 15% unique upheld findings overall;
abstention on hard negatives; not a rephrase of the same risk basin. See `evals/README.md`.

## Collision policy

`scripts/validate_roster.py` flags active-evaluator pairs on: canonical-question
Jaccard >= 0.60; same primary capability + domain overlap >= 0.70; object-of-scrutiny
token similarity >= 0.84. Every flagged pair must be merged, mutexed, given an explicit
neighbor boundary, or waived in `COLLISION_WAIVERS` with a reason.

**Known limitation:** the similarity oracle is token-Jaccard (stdlib), not embeddings.
It caught the mechanically-divisible collisions; it will under-flag paraphrase collisions.
The behavioral battery is the real detector; until it runs, treat "0 flags" as
"no lexical collisions", not "no semantic collisions".

## Resolved 2026-07-10 (roster corrections)

Merges/retirements (IDs preserved as retired aliases):
- `first-principles-engineer` -> `first-principles-rederiver` (identical re-derivation mechanism, different tone)
- `constraint-relaxer` + `constraint-inverter` -> **`constraint-negotiator`** (new merged generator: prices constraint removal vs retention complexity)
- `meta-epistemic-auditor` -> `epistemic-auditor` v2 (claim/evidence/status matrix + uncertainty bounds + update thresholds = one job)
- `premortem-facilitator` -> retired; `inversion-thinker` retained; the premortem protocol is workflow methodology
- `protocol-archeologist` / `chesterton-gate` kept with a HARD boundary (history reconstruction with no deletion in scope vs adjudication of one specific proposed deletion)
- `cloud-native-purist` / `local-first-survivalist` -> mutex counter-mode pair `leverage-vs-sovereignty`

Partial-overlap clusters narrowed via exclusive `object_of_scrutiny` + `neighbors[].boundary`
on every member (chaos/fmea/resilience; entropy/century/tech-debt/bus-factor/explainability;
observability/on-call/forensicist; angry-customer/polisher/adoption/behavioral/wcag;
forecaster/game-theorist/logician/ecological/measurement; zen-master/scope-sentinel;
bias-auditor/sunk-cost; inquisitor/premise/rederiver/historian; ethicist vs privacy/justice/
dual-use/legal specialists).

Removed nonexistent pseudo-slugs from SKILL.md: `blast-radius`, `ethnographer`,
`total-cost`, `bikeshedding` (real ids: `fmea-analyst`, `adoption-realist`,
`unit-economics-adversary`/`opportunity-cost-accountant`, `scope-sentinel`).

## Expansion frontier bookkeeping

**30 core candidates** are in the registry with complete fingerprints (status=candidate,
provenance marks the admission gate unrun). See `roster/candidates.md` (generated).

**Audited-candidate QUEUE (named, neighbor-mapped, NOT yet fingerprinted — do not select,
do not treat as registry entries):**
add-on: hermetic-reproducibility-auditor, model-shift-auditor, physical-security-auditor,
organizational-readiness-auditor, institutional-power-auditor,
stakeholder-representation-auditor, forecast-calibration-auditor,
capital-structure-stress-auditor, portfolio-tail-dependence-auditor,
competition-law-auditor, trade-controls-sanctions-auditor,
procedural-rights-remedies-auditor, algorithmic-contestability-auditor,
evidence-synthesis-auditor, simulation-credibility-auditor,
geopolitical-chokepoint-auditor, climate-physical-risk-auditor,
decommissioning-exit-auditor ·
experimental: cultural-portability-auditor, classification-stigma-auditor,
cross-border-escalation-auditor, planetary-boundaries-auditor,
scenario-signpost-designer, intergenerational-stewardship-auditor ·
generators: morphological-option-space-generator, backcasting-transition-path-generator,
intervention-level-alternative-generator.

**REJECTED as duplicative (2026-07-10 review) — do NOT re-add without behavioral evidence
disproving the collision:** capacity-envelope-auditor, dependency-lifecycle-auditor,
supportability-auditor, slo-error-budget-auditor, consent-integrity-auditor,
manipulation-deception-auditor, network-diffusion-auditor, trust-legitimacy-auditor,
pricing-elasticity-auditor, counterparty-credit-auditor, regulatory-horizon-scanner,
experimental-design-auditor, general-model-sensitivity-auditor, rebound-effect-auditor,
environmental-justice-auditor, real-options-stager.

## Selector

`scripts/select_lenses.py` — deterministic constrained selection with replay record
(registry version + sha256, subject vector, eligibility, scores, exclusions, selected
ids@versions). Panel constraints are in the script docstring and enforced post-selection
as hard errors; `--self-test` runs 1000 seeded fixtures (all must satisfy every
constraint, deterministically). Fit scoring is **lexical** (domain/capability/signal
matching) — a documented v1 limitation; a lens is gated by role/status/axis first, so a
keyword match can mis-rank but never seat a candidate, a retired ID, or a wrong-role card.
Runtime loads full card text only for selected ids: panel prompt tokens scale with panel
size, not registry size.
