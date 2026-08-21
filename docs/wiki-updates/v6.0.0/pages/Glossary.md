> **Applies to:** epistemic-skills v6.0.0
>
> **Canonical sources:** [`metacognate`](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/plugins/epistemic-skills/skills/metacognate/SKILL.md) and [RELEASE-5.0.0.md](https://github.com/ZMS-Labs/epistemic-skills/blob/v6.0.0/docs/release/RELEASE-5.0.0.md)

# Glossary

**Blinded verifier** — The separate reviewer in Evidence-Locked UAT who judges from evidence alone, rather than the actor's own account.

**Conflict Ledger** — The Gauntlet artifact that preserves material dissent, evidence references, and unresolved conflict for arbitrated disposition.

**Discipline** — One of the thirteen epistemic methods that fire on their own descriptions. `metacognate` is the entry point, not a discipline.

**Durable artifact** — A repository-backed record with resolvable provenance and an appropriate revisit/consumption boundary, such as an ADR, plan, issue, PR, goal, derivation, ledger entry, or published handoff packet.

**Epistemic arc** — The linked system for resumption, recon, decision, evidence, contract, gate, proof, persistence, delegation, and the operational loop (watch/health/triage/did-it-land). Tasks may use zero or one discipline; it is not mandatory ceremony.

**Fail-closed** — A load-bearing missing tool or insufficient evidence cannot silently become a pass. The allowable outcomes preserve uncertainty: hold, escalation, or bounded reversible probe.

**INERT (watch)** — A watcher mechanism prepared or deployed but deliberately disabled. It is **not** installed and not watching. The only state in which a new mechanism may arrive.

**Load-bearing claim** — A claim about state, evidence, decision, safety, or completion that later work relies on and therefore must be anchored, qualified, or rejected.

**metacognate** — The sole skill invoked by name. Decides how much process a moment deserves — usually none — and returns control. Carries a procedure, never an inventory.

**Micro-recon** — For unfamiliar routine-looking work, reading the target artifact and nearest test/example before editing. It becomes a full recon (brief) trigger only when those reads expose a positive material risk.

**No-credit** — A result, diagnostic, process artifact, or extra ceremony that cannot count as release/behavioral proof. It must not be promoted into a pass by proximity or narrative.

**Positive trigger** — The observable condition in a released skill description that invokes that skill. Its absence is silent; no skip inventory is required.

**PROVEN (watch)** — Enabled explicitly, then proof-fired with alert received. The only state in which a watcher may be called installed or watching.

**Provenance** — Resolvable origin and identity for a claim, evidence item, artifact, source version, or immutable Git reference, sufficient for a reader to re-anchor rather than trust a summary.

**Routine path** — The default exit for work that is reversible, local, directly checkable, and non-precedential: make the change and perform its bounded check with no process-only artifact.

**UNKNOWN / UNVERIFIED / NARROWED / SUSPECT** — Four-valued honesty vocabulary across health, did-it-land, triage, and watch. Absence of evidence never renders as success.

**Unresolved uncertainty** — A condition where evidence cannot support proceeding. It remains visible as a hold/escalation/probe choice rather than being explained away.

**v6.0.0 support boundary** — The current immutable support point (fifteen skills). Published as an **exception release**: four independent publication reviews returned NO-GO and the owner overrode the judgment gate under a recorded exception. The integrity gates were met on their own terms and were not waived. Does not claim universal behavioral superiority or gate-complete certification.

**Exception release** — A release published without a `GO` from the independent publication gate, under a recorded owner exception that must state, *before* the tag is created: that the gate did not reach GO, that no GO exists, the owner and date and scope, what evidence remains and what it cannot establish, and the successor condition. The exception reaches the judgment gate only; it never reaches the integrity gates. Contrast **conforming release**.

**Conforming release** — A release carrying a recorded `GO` from an independent publication gate on the exact tagged candidate, with no unresolved P1 or P2. v6.0.0 is *not* one.

**v5.0.0 support boundary** *(historical)* — The immutable support point before v5.1.0 (fourteen skills). Published with item 6 PARTIALLY MET and item 8 WAIVED; see errata and post-release review.
