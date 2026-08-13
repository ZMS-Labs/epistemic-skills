# A mission for `manifest` — PROPOSAL, for the operator to correct

**Status:** draft by the steward, **not authority**. The intent below is inferred
from `SKILL.md`, the contract, and how the skill has been used. **Every inferred
line is marked ⓘ and is a guess until the operator overwrites it.** That is the
point of the exercise: the skill exists to make intent durable and defensible,
and its own intent has never been written down.

**Why this artifact:** the operator's stated bar is not a feature list — it is
*"manifest works as I intend it."* That is a better criterion than a version
number because it cannot be satisfied by careful wording. But it is unfalsifiable
while the intent lives in one person's head. This turns it into a small set of
statements that can be checked, and lets the version land when they are true
rather than being chosen.

---

## Instruction (ⓘ inferred — replace with your own words, verbatim)

> Make `manifest` a skill I can hand a piece of consequential, multi-session work
> to and trust that: the authority I granted is recorded and unforgeable, the
> boundary I declared either binds or tells me it doesn't, the work survives
> interruption without me re-explaining it, and "done" means something a second
> party checked rather than something the doer asserted.

## Scope

**In:**
- `contracts/mission-custody/` — the record contract, the store, the CLI, the gate
- `skills/manifest/SKILL.md` — the promise surface
- the Stage-C actuator hook and its harness wiring
- the mission store's durability (es#154)

**Out:**
- the other thirteen skills' content and triggers
- estate release governance (separate program)
- ECS / calibration
- ⓘ the *harnesses themselves* — we adapt to them, we do not fix them

**Protected state:**
- `Y:\dev\epistemic-skills\missions\` — a live chain, untracked, no recovery path
- any published `v*` tag
- the 14 packaged skill descriptions (a shared, rivalrous byte budget)

## Stop rules

1. **Stop if a change would make a sentence in `SKILL.md` untrue** — including by
   making it *more* true than the mechanism supports. Three releases running have
   overclaimed a gate; the next one is not this skill.
2. **Stop before making enforcement default-on without explicit authorization.**
   ⚠ This is a real risk and not a formality: arming guards by default would
   begin refusing actions on live missions that currently succeed. "Works as I
   intend" must not arrive as an outage.
3. Stop if closing a gap requires a breaking record change that cannot migrate a
   live mission — surface it instead.

## Acceptance criteria — the falsifiable statements

Each is a claim that is currently **false or unproven**, stated so a test can
kill it. This is the case table, applied to a release.

| # | statement | today | closes |
|---|---|---|---|
| **A1** | **Every scope entry an operator can write is either enforced or disclosed as unenforced. No entry is silently inert.** | **false** — three shapes found in one day: `docs/` matched only the bare dir, a `..` segment matched nothing real, a spaced Windows path dropped to prose | es#155, `96f1ad3`, thread #18 |
| **A2** | **`scope` binds at the runtime boundary, or `SKILL.md` and the envelope say plainly that it does not.** | **half** — the label is honest, but nothing at run time reads `scope`; `custody_gate.py` has **0** refusal points of its own and consults exactly `guard_mode` + `actuator_guards` | — |
| **A3** | **A mission with no guards says so, visibly, at open and at resume.** An unarmed mission is convention-held and must never be silently so. | **false** — unarmed is silent | — |
| **A4** | **No sequence of legal operations turns a recorded tamper into "coverage continues".** | **false** — an `@2` append re-attesting forged bytes launders it; verified end to end | es#118 Task 4+ |
| **A5** | **The mission store cannot be silently lost.** Its durability mode is recorded at open and surfaced at resume. | **false** — untracked and unignored, no `git checkout` restores it | es#154 |
| **A6** | **Every refusal names its discharge. There are no dead ends.** | **false** — a finding on a trailing-space path can never be acknowledged; the mission can never PASS by any operator action | #143 thread #25 |
| **A7** | **Acceptance is by a distinct actor and cannot be self-served.** | **partly** — the core refuses self-acceptance, but the acceptor can be the party that did the work | es#148 |
| **A8** | **A resume that exits clean means something.** With zero receipts it is vacuous, and says so. | **true** — already honest; listed so a later change cannot quietly break it | — |

**A2 is the one I would argue about.** Two honest answers exist — make `scope`
bind at run time, or state permanently that it is an acceptance-time boundary and
stop implying otherwise. ⓘ I have assumed you want the first. **If you want the
second, say so and A2 becomes a documentation task**, which changes the size of
this considerably.

## What this does to the version question

The number becomes derived. When A1–A7 are true, the skill's promise has changed
from *"I record what you did"* to *"I refuse what you may not do"* — and that is
what a major version is for. Whether it reads 6 or 7 will be obvious by then and
is not worth choosing now.

**5.1.0 is unaffected and should not wait for this.** It ships the convergence and
the custody hardening as they honestly stand, with A1–A7's open items **named in
known-limitations** rather than papered over.

## Tier and acceptance

⚠ **Not self-accepted.** Acceptance belongs to the operator or to an actor who did
none of the work. ⓘ Proposed tier: `declared-role-separation`.

## The obvious objection, stated rather than buried

Running this *as* a mission is dogfooding, and dogfooding is not proof. The first
thing this mission will hit is that its own `scope.out` does not bind at run
time — which is A2. **That is a feature of the exercise, not an embarrassment:**
the fastest way to find what manifest cannot yet express is to try to express
this with it.
