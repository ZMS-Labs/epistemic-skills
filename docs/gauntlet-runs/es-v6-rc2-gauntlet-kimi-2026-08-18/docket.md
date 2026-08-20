# Deep-mode docket — manual-docket (no DeepReason engine in this environment)

Mode: `manual-docket` per SKILL.md Step 3 — conjecture a distribution of rival
failure modes, each self-naming its falsifier. Survivors seeded the panel as
finding candidates FC-1..FC-5 in the frozen dossier; they are hypotheses, not
findings. The docket was executed by the dispatcher seat during Step-0 live
verification (the crib + generator reads WERE the conjecture-refutation loop)
and is recorded here post-hoc with honest labels.

Subject: ES6-V6-CANDIDATE rc2 BUILD freeze at `6db8c50…` — does the frozen
candidate plus its C+1 packet truthfully discharge the predecessor's 15
acceptance criteria and honestly support operator acceptance?

## Null hypothesis

**H0 — the candidate truthfully discharges all 15 criteria, and the packet is
what it claims.** *Falsifier:* one acceptance criterion shown undischarged
against its own falsifier, or one material undisclosed gap.
**Outcome: KILLED** — S1 (R5(b) limb fails on every clean checkout), S2 (R12
recurrence on the criterion's own letter). Note for calibration: H0 survived
14 of 15 criteria — the kill is narrow.

## Rival failure modes conjectured

**FC-1 — the @2 digest seal does not verify anywhere off the generating
host.** *Falsifier:* fresh checkout of C+1 + `validate_v6_assurance.py` exits
0. **SURVIVES → S1 (P1).** (Conjectured by running the handoff's own
verification crib one step further than it asked — at C+1, not only at C.)

**FC-2 — the R15 characterization pin misbehaves on privileged NT.**
*Falsifier:* pin skips loudly or passes on this host. **SURVIVES as
platform-semantics defect → S7 (P3)**; the POSIX-only reading of the residual
(safety-hazard-auditor) was conjectured by the panel and verified.

**FC-3 — sync_skill_surfaces self-test crashes on privileged NT.**
*Falsifier:* self-test exits 0. **SURVIVES → S8 (P3).**

**FC-4 — handoff/packet prose overclaims the verifier experience.**
*Falsifier:* every prose claim about running the oracles survives execution.
**SURVIVES → S6 (P3).**

**FC-5 — the PINS deferral leaves R5(a)'s falsifier unsatisfied.**
*Falsifier:* a recorded operator ruling or PINS entry exists. **SURVIVES in
letter, substance discharged → S5 (P3, CL-3 split).**

**H-steering (carried from the predecessor's R18 doctrine) — the handoff's
crib anchors the seat at named-green oracles and away from the packet's own
verification channel.** *Falsifier:* the crib's named expectations are
complete and accurate. **SURVIVES weakly:** the crib never asked for the
validator at C+1 (where the one P1 lived), and two of its named expectations
were wrong for this host class. Mitigation executed: budgeted out-of-set
search ran BEFORE panel dispatch and found FC-1.

## Killed conjectures (progress, not damage)

- "The requalification runs are stamped prose" — KILLED: all five resolve
  live, workflow_dispatch, head_sha == C, per-job conclusions as recorded.
- "The R3 operator limb is still agent-asserted" — KILLED: echo-certified ODR
  hash chain verifies AND the operator posted the RATIFY string on #191.
- "The C+1 diff smuggles code changes" — KILLED: 13 files, all packet dir;
  zero inventoried files touched C..tip.
- "The ready-mark takeover is still undrilled" — KILLED: drill transcript
  in-tree and live-verified (PR #196, six fresh runs at an unchanged head).
- "The custody fixes broke the gate" — KILLED: custody suites green at C on
  the gating platform (run 32190028540, contract job success).
