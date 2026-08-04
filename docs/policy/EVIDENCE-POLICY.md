# Evidence policy — tests bind to claims, and run only when a claim is newly at stake

Adopted 2026-08-04 (v4.0.0 arc, operator-approved). This policy governs when
each class of evidence is produced, so testing is neither skipped endlessly
nor re-run needlessly. It applies the repository's own `valid_while` idea to
its own evidence: **a test result is valid while its subject is unchanged; a
tier runs only when the claim it licenses is newly at stake.** Calendar time
gates nothing.

## The tiers

| Tier | What runs | When it runs | Claim it licenses | Cost |
|---|---|---|---|---|
| **0 — deterministic** | polarity harnesses, scorer self-tests, drift/inventory/surface-sync gates, append-only ledger gate | every commit (CI) | "the machinery is internally consistent" | ~free |
| **1 — trigger epochs** | one battery's live blinded epoch (N=1 per fixture, opaque keys, preregistered) | **only when that skill's trigger surface changes** — the SKILL.md content hash recorded in the battery's latest RESULTS.md no longer matches | "this skill fires and stays silent on the right moments, and reports in contract shape" | ~600k tokens per battery |
| **2 — suite sweeps** | all batteries' epochs | release candidates only | "the suite's trigger discipline holds at this release" | ~n × tier 1 |
| **3 — comparative campaigns** | the four-arm superiority design (or a successor comparative design) | **once per claim** — when a superiority/benefit claim is first made, or a restructuring decision needs the comparison; never re-run without a new claim at stake | "the disciplines outperform a baseline on this fixture set / this claim" | millions of tokens |
| **field — instrumented use** | ECS epistemic events + outcome records; decision-ledger outcome reviews | continuously, as a side effect of real use — never scheduled | calibration claims, gated by **evidence thresholds** (e.g. the ≥25-resolved-pairs mint gate), never by calendar | ~free |

## Binding rules

1. **Subject hashes make evidence durable.** Every epoch RESULTS.md records
   the content hash of the SKILL.md it tested. CI or a session may treat the
   epoch as valid evidence exactly while that hash matches. A changed hash
   does not fail CI — it downgrades the claim: the README/status line must
   say "epoch predates the current trigger surface" until a Tier-1 re-run.
2. **No scheduled re-runs.** An unchanged subject re-tested is spend without
   information. The only clocks in this policy are release candidates
   (Tier 2) and new claims (Tier 3).
3. **Failures are results.** Every tier commits its outcome as-is — FAILs
   included, preregistration before dispatch, shipped scorers unmodified.
   A partial or aborted run is committed as BLOCKED, never analyzed as
   evidence and never silently retried.
4. **Field data outranks synthetic data for calibration claims.** Synthetic
   epochs license trigger/shape claims only. Anything about real-world
   benefit routes through the field tier's thresholds or Tier 3's
   preregistered designs — a passing epoch is never quoted as behavioral
   proof (each battery README already says this; this policy makes it
   suite-law).
5. **Claims name their tier.** Any README, release note, or PR claim about
   skill behavior cites the tier and artifact that licenses it. A claim
   without a citable artifact is removed, not defended.
6. **Cost is stated before Tier-3 runs.** A comparative campaign states its
   trial count, token estimate, and the decision it informs, in a committed
   design doc, before any dispatch — and states at what design size its
   result is only exploratory (per the campaign design's power-honesty
   rule).

## Worked example (the rule that would have saved the most spend)

The 2026-08-04 first-epoch sweep ran ten batteries in one day — correct,
because every battery's subject had never been epoch-tested (claim newly at
stake). Re-running those same epochs at the next release with unchanged
SKILL.md hashes would be waste under rule 2; changing one skill's trigger
wording re-arms exactly that one battery under rule 1. The four-arm campaign
runs once against the pre-consolidation suite (the restructuring decision is
the claim at stake) and is not re-run after consolidation unless a new
superiority claim is asserted.
