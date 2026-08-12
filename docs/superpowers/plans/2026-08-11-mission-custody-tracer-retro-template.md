# Mission-custody tracer retro — template

Fill after the tracer mission closes (or aborts). This retro — not the build — decides Stage C (enforcement hooks) per `2026-08-11-mission-custody-contracts-design.md`.

## Mission

- **Mission id:**
- **Repo / workspace:**
- **Opened / closed dates:**
- **Final status (from last checkpoint, not memory):**

## Sessions

- **Count and dates:**
- **Actors (steward, other workers, acceptor):**

## Interruptions survived

- What died (session/process), at which revision, and what resumed:
- Did pathless resume find the mission without being told where it was?

## Drift events

- Drift detected? (resume exit 3 occurrences, artifacts named):
- Was every drift honest — recorded reopen before repair, no silent continue?

## Acceptance

- Tier used; acceptor identity; was the role separation real (different session, not a relabel)?
- Any refusals (exit 2) and were they correct?

## The adoption falsifier — answered plainly

**Did custody change the outcome?** (What would have been lost, redone, or wrongly claimed done without it? If the honest answer is "nothing," say so.)

## Stage C decision input

- [ ] Build teeth (PreToolUse enforcement boundary earned)
- [ ] Stay convention-held (custody useful, enforcement not yet justified)
- [ ] Park (custody did not change the outcome)

Rationale:

## Consumption — a ruling nobody can read did not happen

A retro decides something. That decision has to reach the place the NEXT
steward actually reads, which is never this file: the next steward loads
`skills/manifest/SKILL.md` and the contract, not the closed mission's record.

The first time this was skipped, the tracer's "build teeth" ruling sat on an
unpushed branch of a different repo while the shipped skill text still told
every successor that Stage C was "gated on the tracer retro" — the decision
existed and was invisible for a day, and the successor mission ran the exact
actuators the ruling named, unguarded.

Do not close this retro until each is true or explicitly N/A:

- [ ] The ruling is an issue or PR in the repo that owns the skill and the
      contract — not only a line in this file.
- [ ] Any claim in `SKILL.md` that this retro just made false is corrected in
      that same change (search it for the gate you were deciding).
- [ ] The mission record is pushed, not local-only. A record that lives on one
      box is one disk failure from never having existed (SAFETY-5).
- [ ] Anything the mission proved about the CONTRACT — a defect, a missing
      capability, a residue worth disclosing — is filed where the contract's
      maintainers look, with the evidence that established it.
- [ ] Scrub before publishing: mission records sweep up whatever sits beside
      them. Harness session data (`.host-context/`) has carried verbatim
      operator prompts from unrelated sessions.
