> **Applies to:** epistemic-skills v4.0.0
>
> **Canonical source:** [released source](https://github.com/ZMS-Labs/epistemic-skills/tree/v4.0.0/plugins/epistemic-skills/skills)

# The Epistemic Arc

The arc is a handoff model, not a mandatory checklist. Most tasks take the routine exit or fire zero or one discipline. When several observable triggers are present, `using-epistemic-skills` orders the work so that each discipline's output is useful to the next one.

```text
routine -> change + bounded check

resume -> decision-ledger resume mode (continuity-verify) -> router
task -> recon -> decide -> contract -> workflow -> gate -> prove
         recon         resolve        goal        work      gauntlet  evidence-locked-uat
         (three modes) (three         when needed            when needed
                       instruments)

persist -> decision-ledger -> future re-anchoring
delegate -> outsource -> external execution -> origin verification
```

## The moments and their boundaries

- **Resumption:** `decision-ledger`'s resume mode (the former `continuity-verify`) fires before the arc when remembered state controls the next action. It re-anchors a state digest; it does not do the resumed work.
- **Recon:** `recon` makes the territory legible — brief mode (the blindspot pass) when micro-recon finds a material mismatch, hidden coupling, uncertainty, or fan-out risk; initiative mode (wayfinding) for a large foggy effort; candidate mode (harvest-before-adopt) for an overlapping external project. It ends at understanding.
- **Decision and evidence:** `resolve` settles the question with the cheapest sufficient instrument — derivation (the applying-formal-rigor method) derives a property claim; literature (the evidence-research method) assesses reception and holdings; probe (the throwaway-prototyping method) builds a disposable answer. No instrument renders a general ship/no-ship verdict.
- **Contract:** `write-goal` is for explicit persistent-goal intent, not ordinary plan execution.
- **Execution boundary:** `outsource` creates a committed, target-readable context packet before another model, agent, or process acts; the origin re-verifies returned claims.
- **Gate and proof:** `gauntlet` evaluates a frozen high-stakes subject; `evidence-locked-uat` supplies evidence and a blinded verdict for material UI-facing completion.
- **Persistence:** `decision-ledger` records qualifying consequential moments that lack an adequate durable artifact. It is retrospective and never a verdict.

## Ordering has a purpose

The router sequences multiple positive triggers roughly as recon, decision, contract, gate, and proof. A later consumer re-checks whether its input is still valid; if the subject changed materially, the relevant skill re-fires instead of patching stale output. A one-skill task relies on its own output, and a zero-skill task emits no router record.

## Helix across the arc

When workflow skills are present, [Helix: Central Passage](Helix-Central-Passage) positions a justified epistemic discipline relative to the workflow stage. It does not replace the router, and routine or absent pairs remain silent.

## Canonical references

- [Router source at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/SKILL.md)
- [Helix source at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/helix/SKILL.md)
- [Epistemic flexibility reference at v4.0.0](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/using-epistemic-skills/reference/epistemic-flexibility.md)
