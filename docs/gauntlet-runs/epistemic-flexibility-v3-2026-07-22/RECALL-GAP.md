# Recall gap — control/action check is NOT fail-closed (2026-07-22 Step-7b DISSENT)

The cross-family Step-7b consult (GPT-5.6 Pro, request_id GX-CONSULT-6614769c2dbaf38d) returned
**DISSENT (high confidence)**; orchestrator verification confirmed it (`adjudications.jsonl`).

**Verified:** `action_asserts_execution` has a **100% false-negative rate** on 15 execution paraphrases
("roll this out", "make the change live", "advance it to production", "apply the migration now",
"promote the build", "send it", "cut the release", …) — see
`evals/epistemic-flexibility/adversarial_paraphrase_battery.py`. It catches only the two near-literal
planted phrases. A keyword matcher cannot achieve semantic recall.

**Consequence:** the earlier POST-FIX-VERDICT's "P1 CLOSED → CONDITIONAL" was **premature**. The check is
a shallow tripwire, not fail-closed enforcement. **The P1 (mechanical control/action enforcement) is
REOPENED.** The verdict on the fail-closed dimension reverts toward NO-GO until a *structured* fix exists.

**Sound fix (recommended, not yet built):** replace free-text parsing with a **structured action
declaration** — require the trace to carry an explicit `action_executes: boolean` the agent must set,
and enforce `control in {hold, escalate} => action_executes == false`. This moves the check from an
impossible parsing problem to a checkable declared field (residual: the agent could mis-declare, a
smaller and auditable surface). Escalated to the Sovereign for the path decision.

---
## Round 2 (2026-07-22): structured fix ALSO dissented — category limit accepted

The structured `action_executes` fix (commit edbf12b) was sent for a second cross-family read
(GX-CONSULT-b57b2d8b26dfc63d). **DISSENT (high confidence), ACCEPTED:** the check only compares two
*self-authored* fields; an agent acts-while-holding by declaring `action_executes: false` (lint 0/15 →
~100% adversary bypass). **A static trace validator cannot enforce runtime behavior — it sees only
declarations.** P1-as-validator-enforcement is UNACHIEVABLE at this layer; real enforcement needs a
runtime tool-call gate (absent here). The field is retained as discipline/consistency aid + future-gate
hook, relabelled NOT enforcement. Honest net: the integration is a set of discipline/documentation
scaffolds for cooperative agents + honest labels — not enforcement/security controls.
