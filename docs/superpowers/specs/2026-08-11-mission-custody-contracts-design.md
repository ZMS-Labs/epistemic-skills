# Mission custody, contracts-first ("custodian") — design

**Date:** 2026-08-11
**Status:** operator-approved in-session 2026-08-11 (brainstorming dialogue; approach and all eleven sections approved verbatim)
**Repo:** epistemic-skills (contract home)
**Provenance:** This design executes the FOLD cell of the pre-committed demand×vehicle decision rule from the practical-agency gauntlet run (`practical-agency-telos-2026-08-10`, verdict NO-GO on unconditional continuation, hypothesis ruling H-GATE-FIRST + H-FOLD; VEHICLE = fold-feasibility spike PASS; DEMAND = media/content tracer mission named by operator 2026-08-11). Run record: retained in the operator's private run archive (hash-chain verified). Lineage: helix (banked 2026-07-20) → practical-agency (custody pivot, 2026-08-07) → this design. Related: `2026-08-07-practical-agency-and-commission-watch-design.md`, `contracts/watch-commission/`.

## Purpose

Carry consequential, multi-session, interruption-expensive work as **custodied missions**: recorded authority, durable checkpoints, live-state re-anchoring on resume, and tiered independent acceptance. Ordinary requests are untouched.

Explicitly **not**: a router (no skill selection, ever — the adjudicated anti-helix boundary), a daemon or background actor, a second epistemic verifier, or a replacement for any existing discipline.

## Architecture

Three artifacts, one writable home each:

| Artifact | Home | Form |
|---|---|---|
| Contracts | epistemic-skills `contracts/mission-custody/` | `mission-custody@1` schema family + stdlib verifier + examples corpus + CI (the watch-commission@1 apparatus, exactly) |
| Custody core | epistemic-skills, beside the contracts | small stdlib reference implementation (fold-shim lineage), executable proof of the contracts |
| Harness bindings | per harness; Claude Code first | thin: one skill + the core CLI; later harnesses bind the same contracts |

practical-agency **parks**: prior-art reference implementation and proof corpus. An ADR (separate artifact, ordered by the gauntlet verdict) records the lineage and disposition. Its debt retirement (PR dispositions, main relabel, r42 reconciliation) is separate verdict-ordered work, not this design.

## Contracts — `mission-custody@1`

Four schemas, harvested and simplified from practical-agency's six:

1. **`mission-manifest`** — operator instruction (verbatim, append-only; amendments append, never rewrite), scope in/out, protected state, acceptable costs, required acceptance tier, stop/hold/escalate rules, steward and acceptor identities.
2. **`checkpoint`** — full-state snapshot per revision; `prev_checkpoint_sha256` over the prior checkpoint file's raw bytes (externally verifiable chain); mission status from a closed state list (`draft / active / reopened / verifying / completed / cancelled`).
3. **`receipt`** — binds an effect request to the observed artifact: request id, before/after content hashes, timestamp, actor.
4. **`acceptance-verdict`** — typed verdict (`PASS / FAIL / INCONCLUSIVE`), acceptor identity, assurance tier, bound mission revision + receipt refs.

Apparatus per schema: JSON Schema + stdlib verifier + valid/invalid examples corpus (every schema has failing examples that fail) + CI job — mirroring `contracts/watch-commission/` file-for-file in kind.

**Evolution rule** (locked from the mission-os gauntlet's P1-DEFER-SCHEMA-RULE lesson): additive optional fields only within `@1` (absent = default), anything else is a new schema epoch with documented migration.

## Custody core (reference implementation)

Stdlib-only, **~500–800 line cap**, fold-shim lineage (`fold-spike/shim.py` proved the size class on first attempt). Behaviors:

- **Pathless discovery**: find the single active mission from a workspace root; zero-or-multiple active missions is a named refusal, not a guess.
- **Atomic checkpoints**: mkstemp + fsync + `os.replace`; hash-chain verified on every resume.
- **Drift detection**: receipt/artifact hash mismatch → `ARTIFACT_HASH_MISMATCH` → recorded transition to `reopened`; silent continuation is structurally impossible.
- **Acceptance enforcement**: `acceptor_id == worker_id` → refusal; below-required-tier acceptance → refusal.
- **FAIL is clearable** (designed out of practical-agency's surviving branch defect, the reject dead-end): `FAIL` → remediation effect(s) with receipts → re-verification → acceptance is a legal, tested path. A test exists specifically proving a rejected mission can later complete.

Not a server, not a daemon: a CLI invoked per-operation by bindings. The core's test suite is the three-subprocess kill/resume/repair proof (per the spike runner pattern), plus the FAIL-clear path test, plus corpus round-trips.

## Claude Code binding — the custodian skill

One skill, three doors (operator-specified):

1. **Name-invocable**: `/manifest`.
2. **Description-fired**: mission-shaped work — multi-session, consequential, cross-agent, interruption-expensive — and the explicit phrase "manifest this".
3. **Metacognate-reachable**: the description speaks metacognate's condition vocabulary ("will this survive interruption?", "who authorized this scope?", "what makes done defensible?") so the gate's unanswerable condition names this discipline. No special wiring; no member inventory anywhere.

Hard **decline clause**: routine, one-step, in-session-checkable work is declined — presence in the ether must never become ceremony.

Mechanics: the skill drives the custody core CLI via Bash. Mission state lives at `missions/<id>/` **in the repo being worked, committed by default** (ADR-171 / TRANSPARENCY-1 alignment; resolves practical-agency's untracked-state collision), with a documented `.gitignore` escape hatch for noisy missions.

**Install gate**: the skill lands only with a description-byte-budget sign-off (measured 2026-08-06: installs can silently blank other skills' descriptions; the budget-owner item from the gauntlet verdict).

## Discipline integration — no-routing preserved

At bound moments (open / resume / verify / close) the custodian emits **conditions and return points** — e.g. "this claim needs a runtime-adequate oracle before checkpoint r7 closes" — never skill names. Selection remains where it lives today: skill descriptions + metacognate's judgment. This keeps P2-NO-PA-ROUTING intact.

## Acceptance — tiered, honest labels

`operator-accepted` (sovereign; always sufficient) > `agent-accepted` with `declared-role-separation` (distinct session/agent that did not do the work; enforced by the core) > self-certified (**refused**). Required tier is declared at mission open; for consequential missions the default **minimum** required tier is `declared-role-separation` (a distinct agent session suffices to close; the operator may always accept, override, or raise the requirement to operator-only at open). No `externally-proven` tier exists until evidence could actually support one — labels never overclaim.

## Enforcement staging

- **Stage A** — contracts + verifier + corpus + CI (this repo).
- **Stage B** — custody core + Claude Code custodian skill. Custody here is **convention-held and labeled so**: nothing yet prevents an agent bypassing the broker path. This is the deliberate experiment inherited from the fold spike's honest residual.
- **Stage C** (gated) — enforcement boundary: PreToolUse deny-hook (safety_gate-class) scoped to engaged missions, plus acceptance automation. Built **only if the tracer retro shows custody changed outcomes**. Teeth are earned, not presumed.

## Degraded modes

| Condition | Behavior |
|---|---|
| Custody core unavailable | Skill degrades to manifest-as-document: markdown mission manifest still authored, labeled session-bounded; no fabricated persistence |
| Checkpoint store unwritable | Visible degradation surfaced immediately |
| Contradiction on resume | Blocked until reconciled; no continuation over unresolved drift |
| Authority revoked | Consequential progress stops; surfaced immediately |

## Testing and success criterion

- Contracts: corpus CI — every schema has invalid examples that fail verification.
- Core: three-subprocess kill/resume/repair proof; FAIL-clear path test; corpus round-trips.
- Binding: evidence-locked UAT on the live skill.

**Success (the adoption falsifier, answered):** the media/content tracer mission (default candidate: the monitored-missing reconciliation arc; exact mission pinned in the implementation plan) custodied end-to-end across **≥3 real sessions**, including **≥1 genuine interruption** and **≥1 drift event**, closed at `declared-role-separation` or higher — followed by a short written retro answering: *did custody change the outcome?* The retro, not the build, decides Stage C.

## Non-goals (v1)

- No routing or stage-to-skill tables (anti-helix boundary holds)
- No daemon, scheduler, or background actor
- No ECS wiring (measurement consumers must exist first — gauntlet P4)
- No Codex port (the parked practical-agency alpha remains prior art)
- No receipt signing (P3-ordered follow-up if build continues past the tracer)
- No second public custody skill (open/resume/verify/close are modes of one skill)
