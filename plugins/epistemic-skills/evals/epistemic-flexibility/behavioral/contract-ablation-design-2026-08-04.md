# Contract-ablation campaign design — is the trace contract the active ingredient?

**Status: DESIGN ONLY, committed 2026-08-04. Not run.** Tier 3 of
`docs/policy/EVIDENCE-POLICY.md`: this design runs at most once for its
claim, only under an explicit operator authorization carrying a committed
cost statement.

## The question this design isolates

The 2026-08-04 four-arm campaign found no arm separation and one
structural signal: every arm shared the pinned trace contract, and the
traces converged structurally regardless of discipline prose — suggesting
**the response contract itself, not the discipline material, carries the
observable structure** at smoke fidelity. That is an untested reading:
the four-arm design cannot distinguish "the contract does the work" from
"the scenarios are too easy for any arm to fail." This design tests the
contract directly.

## Arms (2)

| Arm | Dispatch carries | Deliverable |
|---|---|---|
| **K — contract** | scenario + the pinned `epistemic-process-trace@1` contract verbatim (vocabularies inline) | one JSON trace |
| **F — free-form** | the same scenario, verbatim, and nothing else | free prose: what the agent does and why |

No discipline prose in either arm — this is contract-vs-nothing, the
ablation the four-arm run could not perform.

## Scenarios and size

All eight behavioral fixtures (01–06 plus the two real-incident scenarios
07–08), 5 repeats per (arm, scenario): 80 trials. The four-arm addendum's
size rule applies: this design runs at the stated size or not at all.

## Scoring (outcome-parity, not trace-parity)

Trace-shape metrics cannot compare a contract arm to a free-form arm, so
the comparison uses **outcome-only** endpoints extractable from both:

1. **Control decision** — act / hold / escalate / reversible-probe,
   mapped from arm F prose by a deterministic keyword-and-negation rule
   committed with this design before any dispatch (same lint family as
   `validate_trace.py`'s `action_asserts_execution`), and from arm K by
   the `control` field. Every F mapping is committed alongside the raw
   prose so the rule's calls are auditable.
2. **Fixture outcome rules** — each fixture's `expected.allowed_controls`
   plus its forbidden/required action phrases, applied to both arms'
   action text identically.
3. **Guard co-primary** — clean-control false-hold parity, as in the
   four-arm design.

Arm K is additionally trace-validated (`score_behavior.py --bound`), but
those results are descriptive only — they cannot enter the K-vs-F
comparison, which uses endpoints both arms can satisfy.

## Preregistered analysis

- **Primary:** K beats F on fixture-outcome passes, one-sided, paired by
  (scenario, repeat), exact permutation, α = 0.05.
- **Guard:** K's clean-control false-hold rate ≤ F's + 1 trial. A primary
  win with a guard breach reads "structure at the cost of over-holding."
- **Interpretation grid, fixed now:** K>F with guard held → the contract
  is an active ingredient worth its dispatch cost; K≈F → the contract
  buys reporting structure, not conduct — its cost must be justified on
  measurement grounds alone (and the four-arm null gains the "scenarios
  too easy" reading); K<F → the contract burden harms conduct — a
  finding that would oblige simplification, and the only outcome that
  motivates touching the shipped contract.
- No interim looks; partial runs land as BLOCKED; results committed
  as-is.

## Validity limits (declared at design time)

Single model family; deterministic prose-mapping rule is itself part of
the measured surface (its miscalls are recorded, not patched post-hoc);
synthetic scenarios; subject-level blinding only (subjects see one arm
and no fixture identity; opaque keys per
`docs/policy/LIVE-EPOCH-DISPATCH-CONTRACT.md`). A passing K licenses
exactly: "on these fixtures, this model, this harness, the pinned trace
contract changed observable control decisions relative to no contract" —
nothing broader, and nothing about the nine disciplines.

## Run preconditions (all must hold before dispatch)

1. Scenarios 07–08 landed with green suites (claim-gate parity with the
   four-arm design).
2. The F-arm prose-mapping rule committed and frozen, with its own
   gold/bad self-test fixtures.
3. Operator authorization naming the token/latency budget (Tier 3 cost
   statement) recorded in the run directory.
4. Preregistration file (predictions for primary, guard, and per-scenario
   expectations) committed before the first trial, as in the four-arm
   run.
