> **Applies to:** epistemic-skills v3.4.0
>
> **Canonical source:** [released Throwaway Prototyping source](https://github.com/ZMS-Labs/epistemic-skills/blob/v3.4.0/plugins/epistemic-skills/skills/throwaway-prototyping/SKILL.md)
>
> **v4.0.0 consolidation:** throwaway-prototyping was consolidated into [resolve](Skill-Resolve) as its **probe instrument** at v4.0.0 (2026-08-04); the name survives as instrument vocabulary, and the full method moved verbatim to [`resolve/probe/METHOD.md`](https://github.com/ZMS-Labs/epistemic-skills/blob/v4.0.0/plugins/epistemic-skills/skills/resolve/probe/METHOD.md). This page is retained as a historical guide; the tagged v4.0.0 sources are the sole contract.

# Throwaway Prototyping

## What it does

Resolves a live design or feasibility decision by **building the thinnest disposable probe that makes the answer observable** — the concrete form of the "bounded reversible probe" closure control, and the constructive complement of Blindspot Pass (which only reads). The prototype is an instrument, not a first draft.

## The four-clause contract (all before building)

1. **One named question**, written first, with the observation that would answer it each way.
2. **Disposal declared at birth** — the build lives somewhere that cannot merge by accident.
3. **The answer outlives the build** — captured to decision-ledger/ADR/tracker before deletion.
4. **Never promote** — the real implementation is rebuilt under normal discipline; it copies ideas freely, lines only under deliberate review. "It already works" is the rationalization to refuse: it worked as an instrument, under no contract.

Variants: logic probe (terminal state-explorer), comparative variants (N thin builds differing only on the decision axis — cosmetically-different variants are ONE variant), integration probe (thinnest end-to-end path through a doubted seam).

## Falsifiable gate

Passed when the pre-registered question has a recorded answer with its observation, the throwaway location is gone (or archived read-only), and no line reached a mergeable branch. A prototype found on a mergeable branch is a finding.

## Use it when

- A decision is cheaper to resolve by a 20-minute build than by continued argument, derivation, or reading.
- A gauntlet option-set names "build the thin version" as the cheapest discriminator, or a wayfinding frontier decision resolves by prototype.

## Do not use it when

- The question is answerable by reading (Blindspot Pass), derivation (Applying Formal Rigor), or literature (Evidence Research).
- The build would touch shared or live infrastructure — that is not a throwaway.
- As a way to start implementation early under another name.

Provenance: distilled from prototype patterns in ConnorGriffin/skills (MIT) and the Pocock-framework community synthesis; the disposal contract is the load-bearing addition.
