# Routine-work fast path — leave the arc before ceremony starts

This reference is part of `using-epistemic-skills`. It is **not another skill,
trigger, receipt, or workflow stage**. It defines the negative path: when no
special epistemic discipline is needed, ordinary work proceeds without
manufacturing a record that says nothing happened.

## Governing rule

> Use the least process that can still expose an error capable of changing the
> action or the completion claim.

The full arc exists for uncertainty, consequential decisions, external claims,
irreversibility, and difficult-to-observe completion. It is not the default
container for every edit.

## Routine gate

A task takes the routine path only when **all four** conditions are currently
true:

1. **Reversible** — one ordinary revert can undo the change without data repair,
   migration, external side effects, a compatibility break, or a second party's
   cooperation.
2. **Local** — the change does not cross security, privacy, authorization,
   tenancy, billing, legal, governance, infrastructure, network, public
   API/protocol, or cross-service consistency boundaries.
3. **Directly checkable** — an existing targeted test, local preview,
   deterministic reproduction, or comparably bounded observation makes both
   success and material failure easy to interpret.
4. **Non-precedential** — no unresolved design choice, scholarly premise,
   authorization, or cross-session judgment must be preserved for a later
   consumer.

The gate is evaluated against observed territory, not the request's adjectives.
"Small" and "simple" are not evidence; neither is unfamiliarity by itself a
reason to convene the full arc.

## Two-read micro-recon

When the territory is unfamiliar but the request appears routine, do **normal
work**, not a blindspot report:

1. open the artifact being changed; and
2. open the nearest test, canonical example, adjacent implementation, or local
   convention that determines what correct work looks like.

If those reads agree with the request and all four routine conditions remain
true, proceed directly. Do not rewrite the request, emit a stamp, list absent
triggers, or create a process artifact.

Leave the routine path when either read exposes any of:

- a premise in the request contradicted by the repository;
- hidden coupling outside the local surface;
- more than one material design option;
- an empirical or scholarly premise that will bear load;
- authorization, security, tenancy, billing, migration, public-contract, or
  other high-impact boundaries;
- fan-out to subagents or an external model where a wrong premise would
  multiply; or
- completion that cannot be established by the bounded direct check.

On exit, route from the **newly observed trigger**. Do not retroactively create a
routine-path record.

## Routine output contract

Routine work produces only:

- the requested change;
- the bounded direct check and its observed result; and
- any material limitation that affects the completion claim.

It produces **zero process-only durable artifacts**. In particular, routine work
must not create:

- a router record or inventory of absent triggers;
- `helix-check` skip lines;
- a blindspot report or rewritten request;
- a formal-rigor record;
- a decision-ledger entry or stated ledger skip;
- a UAT packet, manifest, or hash chain;
- a gauntlet run; or
- a handoff receipt whose only content is that no skill fired.

An existing product artifact may naturally record the work: the code change,
test, PR description, issue, or commit message. That is product provenance, not
a new epistemic-process artifact.

## Examples

### Routine

- Correct a documentation typo and run the link check.
- Change button copy, inspect the component and nearest rendered test/example,
  then verify the local preview.
- Rename a private helper with repository-wide references updated and the
  targeted unit test green.
- Add a local null guard whose intended behavior is already specified by a
  nearby test.

### Not routine

- Change button behavior in a stateful keyboard workflow whose completion claim
  requires acceptance evidence.
- Modify a tenant identifier path or authentication-token downgrade behavior.
- Choose a cache or schema strategy from multiple material alternatives.
- Make a destructive migration, DNS/firewall change, public protocol change, or
  other one-way/high-blast-radius decision.
- Delegate a fuzzy workload to several isolated agents.

## Escalation and missing capabilities

A missing optional skill does not block routine work. Continue through the
bounded direct check and name any material limitation.

A missing skill **does** block or rescope work when its own positive trigger is
present and the missing discipline protects a high-stakes boundary. Examples:
no gauntlet-capable independent review for an irreversible security change; no
reachable rendered surface for a material UI acceptance claim; no evidence
layer for a scholarly premise that determines a consequential decision.

## Audit rule

Absence is silent. Emit routing or pairing records only for:

- skills that actually fired; or
- a positive trigger that an authorized operator explicitly overrode.

The purpose of an audit trail is to preserve consequential action and judgment,
not to prove that every non-event was ceremonially considered.
