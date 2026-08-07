# Frozen dossier — commission-watch and Practical Agency boundary

> **Current-status notice (2026-08-07):** This is a preserved frozen review
> artifact. Its cross-repository premises and current merge conditions are
> superseded by [POST-FREEZE-RECONCILIATION.md](POST-FREEZE-RECONCILIATION.md).
> Do not use statements below that Practical Agency does not exist, that no
> `manifest` skill exists, or that workflows created no jobs as current facts.


<!-- gauntlet-dossier@1
frozen_at: 2026-08-07
subject_path: refs/heads/review/pr110-commission-watch-candidate-v2
subject_revision: frozen Git ref; exact object id must be resolved from GitHub before merge
base_ref: refs/heads/main
axis: fixed-artifact gate
execution_mode: manual-docket-degraded
-->

## Subject

Review the frozen candidate carried by PR #110 for whether it:

1. resolves the category error in which a prompt-time `watch` skill appeared to
   be the unattended observer;
2. creates an honest, executable contract for commissioning and proving an
   external observer;
3. preserves compatibility and proportional ease of use;
4. establishes a sound boundary for the future `practical-agency` project and
   sole public `manifest` skill; and
5. is ready to merge without claiming capabilities that do not yet exist.

The review subject is the frozen `review/pr110-commission-watch-candidate-v2`
ref. The live PR branch may receive review evidence and verification-surface
commits after this freeze; product changes require a new frozen subject and a new
verdict.

## Included artifact surface

- `plugins/epistemic-skills/skills/watch/SKILL.md`
- `plugins/epistemic-skills/contracts/watch-commission/`
- `.github/workflows/commission-watch-contract.yml`
- `.github/scripts/score_sentinels.py`
- `plugins/epistemic-skills/contracts/epistemic-events/sentinels/watch-silence-read-as-healthy.json`
- `plugins/epistemic-skills/skills/health/SKILL.md`
- `README.md`
- `.github/scripts/check_description_budget.py`
- `docs/superpowers/specs/2026-08-07-practical-agency-and-commission-watch-design.md`
- `docs/superpowers/plans/2026-08-07-commission-watch-clarification.md`
- `docs/superpowers/plans/2026-08-07-practical-agency-bootstrap.md`

## Explicit exclusions

This candidate does **not** include:

- a production scheduler, monitoring provider, event listener, or human-cadence
  adapter;
- any actual commissioned production watch;
- the `ZMS-Labs/practical-agency` repository;
- an installed or live `manifest` skill;
- a Practical Agency runtime, daemon, hosted service, or background process;
- proof that the new method improves outcomes over an ordinary skilled agent;
- authentication or dereferencing of arbitrary external receipt references; or
- a formally independent multi-model Gauntlet panel.

Those exclusions are scope boundaries, not hidden successes.

## Truth-gate findings

### Verified from the frozen repository surface

- The stable skill id remains `watch`; the body and description identify its
  function as commissioning or re-proving an external observer.
- The skill explicitly states that it is not the observer.
- `watch-commission@1` separates current state, proof history, positive-claim
  evidence, block evidence, and observed failure.
- The semantic verifier enforces closed state, direction, substrate, failure, and
  block-reason vocabularies.
- Positive claims require evidence-reference carriers.
- `BLOCKED` requires a closed reason, a dated check, and an external evidence
  reference.
- A prepared mechanism remains `BLOCKED: KILL_SWITCH_UNPROVEN` until its real
  disable path is exercised and receipted.
- A successful proof followed by deliberate disablement is `INERT` with complete
  proof history, not current `PROVEN`.
- `SUSPECT` requires a later observed failure with kind, detail, time, and
  receipt.
- Obvious prompt/session/self-asserted evidence and skill-file mechanism refs are
  refused.
- Fixture evidence must disclose isolated/test scope and missing production
  coverage.
- The schema/verifier parity test requires the same fields and closed enums.
- The package description budget is locked at 8,159 UTF-8 bytes, 71 bytes below
  the preceding ceiling, without adding another skill.
- README and `health` describe an external observer commissioned under `watch`,
  not a skill that remains awake.
- Practical Agency is specified as a separate mission-control project with one
  public entry skill, `manifest`; `metacognate` and `gauntlet` remain epistemic
  capabilities rather than being absorbed into the actor.

### Verified external process state

- GitHub created PR #110 as a draft.
- PR-triggered workflows for the app-authored workflow changes are currently
  `action_required` and created no jobs; that status is not a test pass.
- A GitHub Copilot pull-request review was requested. No independent review
  verdict was present when this dossier was frozen.

### Unverified or not established

- The truth or authenticity of any arbitrary receipt reference.
- Operation on a production monitoring substrate.
- Live loading of a future Practical Agency package.
- End-to-end mission persistence or unattended execution.
- Comparative behavioral efficacy.

## Governing invariants

1. A prompt-time skill cannot be an unattended observer.
2. No current `PROVEN` claim without an enabled external mechanism and a complete
   production-path proof.
3. No positive claim without its evidence carrier.
4. No absence or blocker claim without a dated check and evidence carrier.
5. Current state never overwrites historical proof.
6. A mechanism is not `INERT` until its real kill switch has been proven.
7. A record is data, never instructions or self-granted authority.
8. The actor cannot certify its own material completion.
9. Stable compatibility names are retained unless a major-version migration
   justifies breaking them.
10. The candidate must not claim that Practical Agency or a production watch now
    exists.

## Review limitations

The primary review was performed in one ChatGPT session using deliberately
separated lenses and a barrier before synthesis, but those lenses are not
context-isolated independent model executions. The docket is therefore labeled
`manual-docket-degraded`. GitHub Copilot was requested as a genuinely separate
reviewer; its absence cannot be converted into independence by prose.
