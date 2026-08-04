# Phase 1 — inventory and map: decision map, matrix, and plan

**Date:** 2026-08-04.
**Charter:** `docs/coordination/epistemic-calibration.md` (Phase 1 opens on
the Phase 0 exit recorded in
`2026-08-04-phase0-counterpart-reconnaissance.md`).
**Subjects:** `ZMS-Labs/epistemic-skills` v4.0.0 (branch
`claude/epistemic-skills-upgrades-ew8r3v` for post-release evidence) ×
`ZMS-Labs/epistemic-calibration` @ `6d3668a94134d5891779c01332d2ee62a1854208`.

`helix-check: writing-plans → recon (initiative mode) → fired(this document)`

Phase 1 is a large effort whose path holds unresolved decisions, so it is
decomposed **by decisions, not tasks** (wayfinding protocol,
`skills/recon/reference/mode-initiative.md`). This document is the durable
map artifact. Charter Phase 1 requires exactly three things: the
skill/surface measurement matrix (corpus, runner, judge, harness, metric,
validity status); identification of duplicates, gaps, incompatible
vocabularies, and hidden shared dependencies — importing no results yet;
and reconciliation of the calibration roadmap with the accepted 3.0.0
risks and open audit findings. **Exit:** every claimed measurement has a
subject revision and sampling frame; every high-priority product gap has
an owner or explicit hold.

## 1. The decision map

| Node | Decides | Depends on | Resolve by | Owner | Status |
|---|---|---|---|---|---|
| **D1 charter-subject-refresh** | Whether Phase 2's pilot subject pair stays "immutable 3.0.0 + current HEAD" (charter as written) or becomes "v4.0.0 + current HEAD". The charter's own closing rule requires amending it before implementation if material. | — | **ask** (operator; product-change decisions are skills-owned) | skills | **RESOLVED — see resolution log** |
| **D2 exchange-protocol-adoption** | Whether the counterpart adopts `epistemic-product-calibration@1` or counter-proposes. Its event-contract lock is a de facto counter-proposal scoped to event collection only; the result-exchange protocol has no counterpart surface. | — (proposal can be made now; decision is theirs) | **ask** (paired proposal per change-protocol step 1) | calibration decides; skills proposes | **FRONTIER — open** |
| **D3 producer-vocabulary-bridge** | How v3-era producer names (counterpart's `ProducerSkill` enum + pinned map at `8d9b2f85`) coexist with the v4 eleven during Phase 1. | — | **derive** | skills (matrix convention); calibration (re-pin, later) | **RESOLVED below** |
| **D4 matrix-row-schema** | What one matrix row must carry to satisfy the exit criterion. | D3 | **derive** | skills | **RESOLVED below** |
| **D5 pilot-corpus-successor** | Design constraints and authorship of the Phase 2 corpus. The counterpart's existing pilot corpus is **ruled invalid by its own gauntlet** (baselines perfectly separable by outcome; a content-free 0.5 forecast beats the preregistered 15 % Brier bar — `docs/design/gauntlet/pilot-two-phase-verdict-2026-07-28.md` in the counterpart). | D1, D2 | ask + research (corpus is calibration-owned; skills supplies contract requirements) | calibration | non-frontier |
| **D6 advisory-instrument-repair** | Whether/when the counterpart repairs its advisory arm (hardcoded placeholder advisory string in `tools/run_pilot.py`; no renderer exists — its own gate-status record `docs/evidence/publication-gate-status-2026-07-27.md`, which files ledger `ecs-pilot-treatment-placeholder-20260727-09`, calls the usefulness claim "unproved, and currently unprovable by the existing harness"). Blocks usefulness claims only, not calibration measurement. | — (counterpart-internal) | prototype (theirs) | calibration | counterpart-owned; recorded gap |
| **D7 field-pair-supply** | Owner-or-hold for the field tier's supply problem: the ≥25-resolved-pairs mint gate (≥3 producers, ≥2 resolution rules) is unreachable by construction today — collection is fire-and-forget and operator-private, and in-repo resolved forecast→outcome pairs are ≈ zero (`docs/audits/2026-08-04-creation-gate-revisit.md`). | — | **ask** (operator resource decision) | operator | **DISPOSED — recommendation recorded, see resolution log** |
| **D8 reachability-guard** | Whether bilateral reachability obligations get a mechanical guard (nothing today stops deletion of `pin/ecs-contract-2026-07-27`, on which the counterpart's CI depends). | — | derive | skills | **RESOLVED: guard it — mint T2** |
| **D9 risk-reconciliation-disposition** | Owner-or-hold for each open FR3 risk against the counterpart's actual machinery. | matrix (T1) | derive | skills | **RESOLVED below (§5)** |

**Frontier as first charted: D1, D2, D7** — all three *ask* decisions,
with **D6 dependency-free and open — frontier by the resolution rule —
but counterpart-owned: it sits on their map, and is tracked here, not
worked.**

**Frontier after the 2026-08-04 operator answers (resolution log, §9):
D2 alone remains open on our side** — the paired proposal is filed
(issue #84) and the decision is the counterpart's. D5 stays non-frontier
until D2 answers (D1, its other ancestor, is resolved). D6 and the
counterpart-side items remain theirs.

## 2. Frontier decisions resolved in this pass (derivations, focused tier)

**D3 — producer-vocabulary bridge.** Derived directly from the contract's
own versioning rule (`docs/release/RELEASE-4.0.0.md`): retired producer
names in previously collected events validate against the pinned pre-4.0
contract revision; new collection under v4 names requires the counterpart
to re-pin — **counterpart-owned, not a Phase 1 blocker, never forced from
this side**. Consequence for the matrix: every validity claim carries an
explicit **contract-revision coordinate** (`8d9b2f85` = `pin/ecs-contract-2026-07-27`
for anything the counterpart consumes today; `v4.0.0` for post-consolidation
subjects) — in §3 the coordinate rides as the global branch-head default
with per-row pins wherever a row rests on pre-v4 evidence. Both
coordinates stay immutable in parallel.

**D4 — matrix row schema.** Derived from the charter's column list plus
the exit criterion plus D3: one row = *surface; corpus (+N); runner/scorer;
judge type (deterministic / blinded live-subject / oracle); harness +
model family; metric; latest committed result; validity status in the
evidence-policy's own tier vocabulary; subject revision; sampling frame*.
A row missing subject revision or sampling frame fails the exit criterion
by definition. The matrix in §3 instantiates this schema; its global
subject revision is branch head `fefe09f` (v4.0.0 + the resolution arc)
unless a row pins older evidence, and every N is stated per row.

## 3. The measurement matrix — skills side (T1, executed)

Validity labels below are the repository's own (Tier 0–3 + field, per
`docs/policy/EVIDENCE-POLICY.md`); none of them is a behavioral-superiority
claim. Sampling frames are the stated fixture counts at N=1 per fixture
(N=3 runs where noted); every 2026-08-04 live result is single-model-family
(claude-fable-5).

| Surface | Corpus (fixtures, N) | Runner / scorer | Judge type | Latest committed run + outcome | Validity label (repo's own) |
|---|---|---|---|---|---|
| using-epistemic-skills — router skill-selection/trigger surface | none — no routing battery exists (`skills/using-epistemic-skills/evals/` has only proportionality + epistemic-flexibility) | — | — | none | no surface; routing invariants covered only indirectly by helix composition structural checks |
| Router — proportionality battery (deterministic) | `evals/proportionality/fixtures.json`: 18 fixtures (10 routine / 4 material / 4 high-risk) + a five-field routine gate; 3 polarity example runs | `score.py` over `proportionality-run@1` records; `run_tests.py` (Tier 0, CI) | deterministic | CI-green polarity self-tests; no in-repo live run — live application is via blinded harness below | structural smoke check ("not a population measurement" — README); **fixtures still speak pre-v4 skill names** (`applying-formal-rigor`, `blindspot-pass` in `required_skills`; `evidence-research` in the routine gate's forbidden-fires list) |
| Router — blinded proportionality harness | `evals/proportionality/blinded/scenarios.json`: 18 scenarios; 3 repo arms + 2 parody prompts (`arms.json`, v3-era commit pins) | `runner.py` + shared `score.py`; packet tests in CI | blinded live-subject (gpt-5.6-sol, codex-isolated-turn) → deterministic scorer | `blinded/results/RESULTS.md` 2026-07-25: final product r1–r3 all PASS (162/162 terminal); main FAIL, PR46 3× FAIL; corrected parodies both FAIL | "conformance smoke checks, not population effect estimates"; **pre-v4 subject only, never re-run against v4.0.0** |
| Router — epistemic-flexibility protocol suite | 14 synthetic trace fixtures (9 invalid / 5 valid) + 15-paraphrase adversarial battery + enforcement-language audit | `validate_trace.py`, `run_tests.py`, `adversarial_paraphrase_battery.py`, `audit_enforcement_language.py` (Tier 0, CI) | deterministic | CI-green every commit (workflow steps in `epistemic-flexibility.yml`) | protocol-conformance smoke check — "not a behavioral effectiveness measurement" (README); validates authored traces, never live conduct |
| Router — epistemic-flexibility behavioral suite (four-arm campaign) | `behavioral/fixtures/`: 8 scenarios (gold/bad pairs); four-arm run used 01–06 × 3 reps × 4 arms = 72 trials | `score_behavior.py` (delegates to `validate_trace.py`); arms hash-pinned in `ARMS-MANIFEST.json`; `PREREG.md` | blinded live-subject (claude-fable-5, opaque keys) → deterministic scorer + paired exact permutation | `behavioral/results/2026-08-04-four-arm/RESULTS.md`: **no arm separation** — A=5/B=4/C=7/D=4 of 18; primary D>A p=0.875, directionally negative; trace-dialect defect found, uniform post-hoc adapter | Tier 3 comparative, **downgraded to EXPLORATORY** (size + post-hoc adapter); licenses no superiority claim in any direction |
| Router — ECS collection-hook pressure eval | 1 adapter-failure pressure scenario × 5 fresh-context reps × 2 arms | 5 fixed assertions per run | live-subject, assertion-scored | `behavioral/results/2026-07-27-ecs-collection-hook/RESULTS.md`: candidate 5/5 runs pass, old snapshot 0/5 | narrow live pressure probe; single scenario, pre-v4 |
| helix — composition contract | contract markers across all 11 skills + planted mutations for every high-risk omission | `evals/composition/verify.py` + mutation tests `tests/run_tests.py` (Tier 0, CI) | deterministic (structural + mutation-sensitivity) | CI-green; `results/BLOCKED.md`: **no live behavioral epoch ever** — "behavioral effectiveness is NOT_RUN, not inferred from the structural PASS" | structural only; live trigger recall / boundary loading explicitly out of scope |
| recon — brief mode battery | `evals/brief-trigger-and-scope/fixtures.json`: 14 (incl. 6 hard negatives, 1 injection fixture) | `score.py` + polarity tests (CI); live epochs per `LIVE-EPOCH-DISPATCH-CONTRACT.md` | live-subject (subject-blinded, opaque sha256 keys) → deterministic scorer | `results/2026-08-04-v4-tier1/RESULTS.md`: **FAIL 12/14** (2 question-count shape overruns over correct conduct); first epoch 2026-08-04: FAIL 13/14 | Tier-1 trigger-level, N=1, same-family; "passing it is NOT behavioral proof" |
| recon — candidate mode battery | `evals/candidate-trigger-and-scope/fixtures.json`: 14 (5 hard negatives) | same pattern | live-subject → deterministic scorer | `results/2026-08-04-v4-tier1/RESULTS.md`: **PASS 14/14**, first epoch, born-pinned contract | Tier-1 trigger-level, N=1, same-family |
| recon — initiative mode battery | `evals/initiative-trigger-and-scope/fixtures.json`: 13 (5 carry decision graphs) | same pattern; scorer crash fixed fail-closed same day | live-subject → deterministic scorer | corrected `results/2026-08-04-v4-tier1/`: **FAIL 11/13** — 1 reporting-vocabulary divergence + **the epoch program's only genuine hard-negative over-fire**; first attempt quarantined in `…-invalid-dispatch/` (defect record, not evidence); first epoch: 11/13 | Tier-1 trigger-level, N=1, same-family |
| resolve — derivation (formal-rigor v2 fixtures) | `derivation/evals/formal-rigor-v2-fixtures/fixtures/`: 22 fixture dirs; 6 parody arms designed | `run_live.py`, `score.py` (structural), `posthoc_diagnostic.py`; semantic adjudication doc + schema | blinded live-subject (Codex, 44 ephemeral sessions) → deterministic structural scorer; **LLM semantic adjudicator designed, never run** | `results/RESULTS.md`: RED established (neutral 4/22, v1 1/22, 2026-07-24); candidate diagnostic 18/22 = **structural gate FAIL** (2026-07-25); semantic NOT_RUN; parodies NOT_RUN fail-closed | "blinded conformance smoke check; not a population rate"; candidate GREEN never claimed; pre-v4 subject, raw roots local-only (C:\tmp) |
| resolve — literature trigger battery | `literature/evals/trigger-and-scope/fixtures.json`: 14 | `score.py` + polarity tests (CI); Tier-1 epochs | live-subject → deterministic scorer | `results/2026-08-04-v4-tier1/RESULTS.md`: **PASS 14/14 — second consecutive clean epoch** (first epoch also 14/14) | Tier-1 trigger-level, N=1, same-family |
| resolve — probe trigger battery | `probe/evals/trigger-and-scope/fixtures.json`: 12 | same pattern | live-subject → deterministic scorer | `results/2026-08-04-v4-tier1/RESULTS.md`: **FAIL 11/12** — single failure a fixture under-specification (canonical option ids absent from scenario text); first epoch: PASS 12/12 | Tier-1 trigger-level, N=1, same-family |
| decision-ledger — proportionality battery | `evals/proportionality/fixtures.json`: 4 (no-op / reuse / create / recurrent-correction) + polarity examples | `score.py`, `tests/run_tests.py` (Tier 0, CI) | deterministic | CI-green polarity tests; **no live epoch, no results/ directory** | structural smoke only |
| decision-ledger — resume-fixtures (continuity-verify) | `evals/resume-fixtures/fixtures/`: 10 artifact-corpus fixtures (8 planted traps, 2 clean controls) | `score.py` confusion-matrix gate (≥7/8 traps AND 0/2 false flags); CI re-scores all 13 committed run dirs | blinded live-subject arms (skilled / neutral baseline / parody) → deterministic scorer | `results/RESULTS-2026-08-04-v4.md`: **PASS — skilled-v4 gate met in all 3 runs (8/8, 0 false flags)**; baseline also 8/8 traps all runs (1 gate fail on a control flag); 2026-07-22 runs stand separately (different model family, comparison banned) | "deterministic smoke check, honestly labeled — not a measurement"; cannot attribute catches to the skill (named calibration question) |
| write-goal — trigger battery | `evals/trigger-and-scope/fixtures.json`: 14 | `score.py` + polarity tests (CI) | live-subject → deterministic scorer | `results/2026-08-04/RESULTS.md`: **PASS 14/14** (preregistered prediction was 11/14) | Tier-1 trigger-level, N=1, same-family; subject unchanged by v4 so epoch remains valid under the hash rule |
| outsource — trigger battery (+ packet/package integration tests) | `evals/trigger-and-scope/fixtures.json`: 14; plus deterministic `tests/run_tests.py` packet/package suite in CI | `score.py` + polarity tests | live-subject → deterministic scorer | `results/2026-08-04/RESULTS.md`: **FAIL 12/14** — both failures capability-id vocabulary drift (canonical ids live only in the README subjects can't read); issue-#77 class | Tier-1 trigger-level, N=1, same-family; failures diagnosed as reporting-contract, not conduct |
| open-questions — trigger battery | `evals/trigger-and-scope/fixtures.json`: 10 | `score.py` + polarity tests | live-subject → deterministic scorer | `results/2026-08-04/RESULTS.md`: **FAIL 8/10** — both failures "reporting-contract divergences over behaviorally-correct conduct"; preregistration predicted exactly this set | Tier-1 trigger-level, N=1, same-family |
| context-audit — trigger battery | `evals/trigger-and-scope/fixtures.json`: 14 (6 hard negatives) | `score.py` + polarity tests | live-subject → deterministic scorer | `results/2026-08-04/RESULTS.md`: **FAIL 8/14** — all 6 failures one diagnosed battery-design divergence (`full-audit` vs `report-only-audit` vocabulary; issue #77); trigger discipline itself clean (all hard negatives silent, every expected fire fired) | Tier-1 trigger-level, N=1, same-family; headline FAIL stands uncorrected pending battery redesign |
| gauntlet — arbitrator certification battery | `evals/arbitrator-certification/battery.json`: 10 planted-flaw cases (scorer-only truth); `inputs.json` arbitrator-facing | `score.py` (deterministic); certification threshold catch ≥9/10 | blind live-subject arbitrator dispatches (claude-fable-5, effort high) → deterministic scorer | `results-2026-08-04.md`: **CERTIFIED — 10/10 planted-flaw catch, 8/10 verdict-match** (both divergences more conservative); supersedes 2026-07-17 (valid only for retired shadow-seat protocol) | role-certification at standard rigor; N=1 per case, same-family |
| gauntlet — roster/selector + validate_ruling_set kernel gate | roster files + `select_lenses.py --self-test` 1000 deterministic constraint fixtures; 4 committed run sets under `docs/gauntlet-runs/` | `tests/run_tests.py`; `validate_ruling_set.py --self-test` + `--scan docs/gauntlet-runs` (Tier 0, CI) | deterministic | CI-green every commit | mechanical/structural only; **behavioral lens-admission battery named as an honest gap and absent** (`evals/README.md` referenced but nonexistent) |
| evidence-locked-uat — triage battery | `evals/triage/fixtures.json`: 4 routing fixtures (routine / stateful / explicit-request / blocked-environment) | `score.py`, `tests/run_tests.py` (Tier 0, CI); runtime `scripts/judge.py` deterministic judge | deterministic | CI-green polarity tests; **no live epoch, no results/ directory** | structural smoke only; entire UAT judge chain remains `calibration_status: uncalibrated` — the corpus that would authorize `calibrated:<ref>@<date>` does not exist (charter's named Phase-2 pilot) |

**Counterpart-side assets (from Phase 0/1 reconnaissance of
`6d3668a9…`):** a deterministic calibration kernel (Brier /
overconfidence report), integer-prior Beta-Binomial machinery with
clustered-correlation collapse, an advisory policy with Pareto frontier
over six cost dimensions, an event pipeline + append-only idempotent
in-memory store matching our event contract, a blinded paired-arm pilot
runner/scorer with model-family round-robin — and **no LLM judge anywhere**
(deterministic oracles only). Its two 10-case pilot corpora are
content-pinned but gauntlet-invalidated (D5); its advisory arm is
instrument-broken (D6); its `ProducerSkill` enum speaks the v3-era eleven
(D3).

## 4. Duplicates, gaps, incompatible vocabularies, hidden dependencies (charter bullet 2)

- **Incompatible vocabulary (live):** counterpart `ProducerSkill`/pinned
  map = v3-era names; our current map = v4 names. Bridged by D3; a real
  re-pin is counterpart-owned Phase 1 work under D2's proposal.
- **Vocabulary drift inside our own corpora:** the proportionality
  fixtures still speak pre-v4 skill names in their required-skill and
  routine-gate vocabularies; four
  trigger batteries carry diagnosed #77-class reporting-vocabulary defects
  (context-audit's battery-design divergence the largest). These are
  matrix rows, not hidden anymore.
- **Duplicates:** none found — the counterpart's kernel does not duplicate
  any skills-side scorer; the only overlap is the event contract, which is
  the intended interface.
- **Hidden shared dependencies, now named:** (1) the counterpart's CI
  fetches our repo **by SHA** and depends on `pin/ecs-contract-2026-07-27`
  for reachability — guarded by T2; (2) both sides' Phase 2 depend on the
  not-yet-adopted exchange protocol (D2); (3) the UAT judge chain's
  `calibrated:<corpus-ref>@<date>` transition depends on a corpus only the
  Phase 2 pilot can produce — and the pilot depends on D5's successor
  corpus, since the existing one is invalidated.
- **Coverage gaps (owner-or-hold assigned here; formal-rigor items also
  governed by §5):** all skills-owned, each under an **explicit hold**
  bound to the evidence policy's arming rules (a tier runs when its claim
  is newly at stake, never on a calendar): no router trigger-and-scope
  battery (hold — minting one is battery-design work that should follow
  D1's subject decision); helix has structural evidence only, no live
  epoch ever (hold per its own `results/BLOCKED.md` design note);
  evidence-locked-uat triage and decision-ledger proportionality have no
  live epochs (hold — deterministic Tier-0 coverage stands; a live epoch
  arms when a trigger-level claim is first made); gauntlet's behavioral
  lens-admission battery is named in its tests as an honest gap and does
  not exist (hold — charter Phase 3 scope); formal-rigor v2 semantic
  adjudication and parody arms are NOT_RUN with the candidate structural
  gate at FAIL (held under FR3-R1/-R2/-R5 in §5).

## 5. Roadmap × accepted-risk reconciliation (charter bullet 3; D9)

| Open risk (revisit trigger) | Counterpart machinery that bears on it | Phase 1 disposition |
|---|---|---|
| FR3-R1 formal-rigor behavioral confidence (next tag after v4.0.0 or 2026-10-31) | none directly; pilot design patterns reusable | **skills-owned, hold until deadline** — re-adjudicated 2026-08-04, unchanged |
| FR3-R2 cross-provider semantic coverage (same deadline, or when independent adjudication capacity exists) | pilot runner's **model-family round-robin** is the nearest reusable machinery — but it rotates execution families (subjects), not adjudicators, and the counterpart fields no model judge at all | **joint candidate** — name it in the D2 proposal as the second slice after the UAT pilot; the adjudication capacity itself must still be built; until adopted: hold |
| FR3-R3 causal confounding (when designing the next behavioral campaign) | paired within-subject crossover design in `run_pilot.py` separates arms properly | **skills-owned** — R3's trigger binds the next committed design, `contract-ablation-design-2026-08-04.md` (paired-by-fixture, declared single-model-family: provider held constant, not yet separated); it fires at that campaign's authorization; hold until then |
| FR3-R4 Cursor runtime compatibility (when a verifiable path appears) | none | **hold, unchanged** |
| FR3-R5 scorer discrimination vs superiority claims (before changing weights / claiming superiority) | their gauntlet's separability finding is the same defect class in corpus form | **skills-owned standing constraint** — inherited by D5's corpus requirements: successor corpora must be non-separable by construction |
| FR3-R6 diagnostic release-credit none (only if a fresh campaign supersedes) | — | **hold, unchanged** |

## 6. Fog-free tickets (minted; three-fact handoffs attached)

- **T1 — commit this matrix** *(executed by this document)*. Depends on:
  D3, D4 (resolved above). Observable behavior: every row carries subject
  revision + sampling frame; CI stays green. Invalidating decision: none.
- **T2 — mechanical reachability guard** *(executed 2026-08-04:
  `.github/scripts/check_pin_tags.py` + the "Pin-tag reachability guard"
  CI step — an absent or moved pin tag turns CI red; future pin tags
  register in its `PINS` map)*. Depends on: D8 (resolved). Observable
  behavior: deleting or moving the pin tag turns CI red. Invalidating
  decision: none.
- **T3 — the D2 paired proposal** *(executed 2026-08-04: issue #84 —
  change-protocol step 1 naming both repos, the exchange protocol, the
  v4 re-pin, the D7 ownership recommendation, and the successor-corpus
  requirements)*. Depends on: nothing (the *proposal*; the *decision* is
  D2, counterpart-owned). Observable behavior: an issue exists whose text
  a counterpart maintainer can act on without this session's context.
  Invalidating decision: D2 resolving as "counter-proposal" reshapes but
  does not invalidate the ask.

Nothing else is ticketable: every other region has an unresolved ancestor
(D1, D2, or D7) or a counterpart-side owner.

## 7. Exit-criterion adjudication and what remains

**Met by this document:** the matrix exists with subject revisions and
sampling frames on every row (first exit clause met), and every named gap
in §4/§5 carries an owner or an explicit hold — **except field-pair
supply, whose owner-or-hold is exactly what D7 asks the operator to
assign**. The exit criterion is therefore not yet fully met: its second
clause closes with D7, and Phase 1 is not claimed complete here.

**Remaining Phase 1 steps after the 2026-08-04 resolutions (§9):**

1. ~~**D1** — operator decides the Phase 2 subject pair~~ **RESOLVED**:
   test current reality (latest release tag + HEAD); charter amended.
2. **D2** — proposal filed (issue #84); the counterpart adopts,
   counter-proposes, or explicitly defers on its own schedule. *The only
   step Phase 1 still waits on.*
3. ~~**D7** — owner-or-hold for field-pair supply~~ **DISPOSED**:
   ownership recommendation recorded and carried in #84 (calibration owns
   store + resolution; skills owns emission; operator owns visibility);
   final confirmation rides the #84 answer.
4. ~~**T2** — reachability guard~~ **EXECUTED** (CI-enforced).
5. Counterpart-side, tracked not forced: D5 successor corpus (with the
   §5/FR3-R5 non-separability requirement, restated in #84), D6 advisory
   repair, and the PUBLICATION-HOLD ownership-review gate from Phase 0's
   "substantially met" owners criterion.

**Phase 1 closes** when 1–4 are done and the counterpart has either
adopted, counter-proposed, or explicitly deferred on D2 — at which point
**Phase 2 (one end-to-end pilot)** opens: evidence-locked-uat seeded
defects against the D1-chosen subject pair; preregistered expected
planted-defect catches, clean-control false holds, thresholds,
exclusions, and what would *not* authorize `calibrated` (charter Phase 2
verbatim, exit requiring at least one positive and one negative
control); one exchange-unit record produced by the counterpart and
independently verified here (hashes, schema, subject identity, claim
scope), with `outsource` governing the cross-repo packet and any
`accepted-gate` status inert until a skills-side ledger acceptance entry
exists. Phase 3 broadens observational calibration (and is where D7's
supply problem must actually be solved); Phase 4 promotes only
preregistered, stable, independently reproducible measures to gates.

## 8. Falsifiable gate (wayfinding self-check)

Walk upstream from each minted ticket: T1 → D3, D4 (both resolved above);
T2 → D8 (resolved); T3 → none (it is a proposal, not the decision). No
ticket has an unresolved ancestor. D5 is deliberately **not** ticketed —
its ancestors D1 (now resolved, §9) and D2 (open) leave one unresolved
ancestor standing — and no build ticket exists for the Phase 2 pilot for
the same reason. The map is honest.

## 9. Resolution log (recorded on the map with provenance)

- **D1 — RESOLVED 2026-08-04, provenance: operator interview** ("always
  be testing the current reality and not the past unless it's
  necessary"). Phase 2's subjects are the **latest immutable release tag
  (today v4.0.0) + current development HEAD**; past immutable subjects
  enter a design only when a specific claim (regression, transfer,
  longitudinal) requires them. The charter is amended accordingly
  (`epistemic-calibration.md`, amendment banner + Phase 2 bullet) —
  amendment-before-implementation honored. Revisit: if a regression or
  longitudinal claim later needs a past subject, that design names it
  explicitly.
- **D7 — DISPOSED 2026-08-04, provenance: operator asked "who should
  own?"; recommendation recorded and carried in issue #84.** Recommended
  split per the charter ownership table: **epistemic-calibration owns**
  the outcome store and resolution loop (trial evidence and estimates
  are charter-side calibration property, and its event store is already
  the right shape); **epistemic-skills owns** emission (events per the
  pinned contract; decision-ledger outcome reviews as the resolution
  feeder — already a first-class trigger); **the operator owns** the
  privacy boundary — granting the store operator-visible status is what
  makes the ≥25-pair mint gate *reachable*. Final confirmation rides the
  #84 answer; until then this stands as the skills-side recommendation,
  not a bilateral fact.
- **D8/T2 — EXECUTED 2026-08-04, provenance: operator "ok".**
  `.github/scripts/check_pin_tags.py` + the Tier-0 CI step; the pin-tag
  registry carries `pin/ecs-contract-2026-07-27 → 8d9b2f85…`.
- **T3 — EXECUTED 2026-08-04, provenance: operator authorization to act
  within the skills-side purview.** Issue #84 files the charter's
  change-protocol step 1 (exchange-protocol adoption; v4 event-contract
  re-pin; D7 ownership recommendation; successor-corpus requirements
  including the FR3-R5 non-separability constraint).
- Ledger: `calibration-phase1-frontier-resolved-20260804-15`.
