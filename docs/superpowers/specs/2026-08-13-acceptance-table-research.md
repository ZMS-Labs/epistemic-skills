# The manifest acceptance table vs the literature — VERDICT: it is a sample

**Method:** five parallel literature lanes (complete mediation · declared-vs-enforced
policy · tamper-evident logging · capability delegation · separation-of-duty and
liveness), each asked what the field names that A1–A8 does not.

⚠ **Provenance and completeness of this memo.** The five lanes completed. The
adversary and synthesis agents **died on a spend limit** before running, so the
synthesis below is the controller's, assembled from the lanes' structured
`gaps_in_our_table` output. It has **not** had an adversarial pass, and the
per-claim citation numbers live in the lane records
(`subagents/workflows/wf_ac9aad7f-fd7/journal.jsonl`), not here. Treat named
concepts as pointers to look up, not as verified citations.

---

## The verdict

**Sample, not a space — and not even a well-chosen one.** A1–A8 cluster almost
entirely on one axis: *does a declared entry bind, and is the record honest?*
The lanes returned **~30 named failure modes** the table does not cover, several
of which are structurally upstream of everything in it. The single largest:

> **Permission is not authority.** A1–A8 are all statements about *entries* and
> *enforcement* — i.e. permissions. The literature's central point is that
> permissions do not bound authority, because an actor causes effects
> *indirectly* through other actors that hold them. A mission can honour every
> entry in its scope and still cause any effect it likes through a subagent, a
> tool, or a delegated capability.

That is the confused-deputy family, and the table has no statement about it at all.

---

## What the table is missing, grouped

### 1. The mechanism itself is unprotected (reference-monitor lane)

- **Tamperproofness of the gate.** A4 protects the *receipts*. Nothing says the
  gate, guard config, scope declaration, or acceptance record cannot be modified
  **by the mission it governs**. The reference-monitor concept makes tamperproofness
  co-equal with complete mediation; we have neither stated.
- **Fail-safe default for the gate's own absence.** Nothing says what happens when
  the hook is missing, errors, or is uninstalled mid-mission. Default-deny /
  fail-closed is the canonical answer. **This is the session's own
  "detection without notification" finding, in the field's language.**
- **Economy of mechanism / verifiability.** The third leg — small enough that
  analysis can be assured complete — has no analogue.

### 2. Mediation is asserted, never bounded (mediation + delegation lanes)

- **Uncircumventability.** A2 says scope binds at the runtime boundary; nothing
  says that boundary is **unbypassable**, nor names the effect classes it does and
  does not intercept. The broker literature states its guarantee *conditionally*
  and we have adopted the guarantee without the condition.
- **Enforceability of the policy itself.** Some entries **cannot be enforced by any
  runtime monitor** — this is a decidable property of the policy (Schneider/Basin),
  not a fact about our plumbing. A1/A2 treat "enforced" as if it were the latter.
- **Policy carriage / context eviction.** For a design whose enforcement is *"a
  steward reads it"*, the most on-point named failure is that the policy is **not
  present in the decision state at the moment of action** — eviction, weakening,
  over-budget continuation.

### 3. The record has no independent challenger (tamper-evidence lane)

- **The commit gap.** Nothing requires a receipt be minted **synchronously** with
  the effect. This exact window defeated every prior tamper-evident logging scheme.
- **Equivocation / split view.** Nothing says the steward and the acceptor see the
  **same** mission. A store presenting two histories defeats A7 entirely without
  touching the chain, and A4 reports clean on both.
- **No external witness.** A7 requires a distinct *acceptor* (a role). Nothing
  requires a distinct **witness** holding a prior commitment (a cryptographic
  fact). An acceptor reading the mission's own self-report is not a witness.
- **No detection-latency bound.** The table never says *when* verification happens.
- **No graceful degradation.** When a tamper is found, what happens to the intact
  receipts?

### 4. Acceptance is one bit where the field has five (SoD lane)

- **Global satisfiability** — is the declared constraint set jointly satisfiable
  *before* the mission runs? (the workflow-satisfiability problem)
- **Resiliency / acceptor availability** — nothing requires a distinct acceptor
  *exists* or is reachable.
- **Binding of duty** — the dual of separation; "the actor who opened this must
  close it" is inexpressible.
- **Cardinality** — A7 is binary; the field specifies k-of-n.
- **Acceptor effectiveness — flagged by its lane as the largest gap.** Nothing
  requires the acceptor *could have said no*, had the evidence to, or bore any
  consequence. The rubber-stamp failure.
- **Capability-acquisition closure** — nothing stops the actor acquiring,
  delegating, or being delegated the acceptor capability.

### 5. Two-sidedness, interaction, and drift (policy lane)

- **Inter-entry interaction.** A1 is per-entry. The entire firewall-anomaly field
  exists because entry *i* silently nullifies entry *j* (shadowing) or produces
  order-dependent outcomes. **We have already hit this and not recognised it** —
  #143's `elif` bug is exactly shadowing.
- **Under-enforcement is also a defect.** The table guards only over-permission;
  the literature scores policy quality as **two-sided**, because excessive friction
  produces shadow security.
- **The acknowledgement surface is an unaudited policy of its own.** A6 demands
  every refusal have a discharge — and the discharge *becomes the hole*.
  Suppression counts rise monotonically over a project's life.
- **Staleness after a clean open.** A5 covers *losing* the store; nothing covers
  the store persisting while the world moves via channels it cannot see.
- **Provenance of the mission record.** If lower-provenance content (tool output,
  a fetched file, another agent) can reach the fields the steward reads, then
  **reading the mission is an injection channel** and the steward is the deputy.

### 6. Revocation does not exist in the table at all

Open, resume, verify, accept, close — **there is no REVOKE.** Lingering authority
is a measured failure; revocation is called the missing link of delegation. Nor is
there attenuation or a sub-delegation depth limit: nothing requires a subagent
receive strictly less than the mission holds.

---

## What this means for the version question

The v6 bar was going to be "A1–A7 are true." **That bar is now known to be
wrong-shaped** — satisfying it would leave permission-vs-authority, revocation,
uncircumventability, equivocation and acceptor-effectiveness entirely unaddressed,
while the release notes claimed the skill "works as intended."

**Recommended next step:** re-derive the table from the failure taxonomy above
rather than extending it. A statement per named family, then check which of A1–A8
survive as instances. Several will — A4 and A8 are sound as far as they go — but
the *organising axis* should come from the field, not from our incident log.

**Do not treat this memo as the new table.** It has had no adversarial pass, and
the session that produced it has repeatedly found that the *correction* is where
the defect hides.
