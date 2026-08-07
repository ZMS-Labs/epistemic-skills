# Lens report — state-machine adversary

**Role:** adversarial evaluator  
**Subject:** frozen `review/pr110-commission-watch-candidate-v2`  
**Question:** Can a persuasive but false record still obtain a trusted watch state?

## Validation kernel

The candidate is correctly preserving an important need: operators require a
portable way to specify and prove monitoring without pretending that a prompt or
configuration file remains active. A fix that merely deletes the skill or reduces
it to prose would lose that value.

## Attack table

| Attack | Expected defense | Result |
|---|---|---|
| Claim that `SKILL.md` is the observer | closed substrate kind plus prompt-time mechanism rejection | defended |
| Relabel `SKILL.md` as `fixture` | inspect mechanism ref, not only substrate label | defended |
| Populate all proof booleans but omit external persistence | require permitted mechanism, persistence receipt, and current enablement | defended |
| Use a self-asserted persistence receipt | reject self-asserted/prompt/session evidence prefixes | defended |
| Report no alert as healthy | require alert receipt for `PROVEN`; sentinel rejects silence-as-success | defended |
| Deliver a direct test message that bypasses the real probe | require `production_path: true` and complete proof bundle | defended structurally; external truth still requires receipt resolution |
| Deploy disabled configuration and call it watching | only `PROVEN` permits current watching; disabled mechanism cannot be `PROVEN` | defended |
| Deploy disabled configuration and call it `INERT` before control is proven | require exercised and receipted kill switch; otherwise `BLOCKED: KILL_SWITCH_UNPROVEN` | defended |
| Record a successful proof, then disable the observer | permit complete proof history under current `INERT` | defended without erasing evidence |
| Store only attractive proof fragments under `INERT` | require proof wholly absent or complete | defended |
| Mark `SUSPECT` because a failure is merely possible | require observed failure kind, detail, time, and receipt | defended |
| Mark `BLOCKED` because the agent did not think of a substrate | require block detail, observation time, evidence ref, and reason-field consistency | defended structurally; truth still requires evidence resolution |
| Use a fixture and imply production transfer | require coverage limits to disclose fixture/test scope and missing production coverage | defended |
| Leave trusted proof fresh forever | require `reprove_after` for `PROVEN` and retained complete proof | defended |
| Hide a prepared mechanism inside `DECLARED` | forbid prepared mechanism fields in `DECLARED` | defended |

## Findings

### F-SA-1 — External receipt truth is outside the semantic verifier

**Severity:** P3 / explicit coverage limit  
**Status:** accepted and documented

The verifier establishes carrier consistency and rejects known self-referential
forms. It cannot establish that `fixture://receipt/alert-001`, an HTTPS URL, a
provider id, or another reference resolves to authentic evidence supporting the
claim. This is not solvable by string validation without embedding every external
provider into the contract.

**Falsifier:** This finding is wrong if the verifier dereferences and authenticates
every evidence reference against an independently trusted source. It does not.

**Required preservation:** Consumers must perform proposition-level evidence
resolution and degrade unresolved or contradictory references. The contract
README and security boundary now say so.

### F-SA-2 — Time strings are intentionally opaque

**Severity:** P3  
**Status:** open, non-blocking

`received_at`, `observed_at`, and `reprove_after` are structurally strings rather
than RFC 3339 timestamps. This supports condition-based expiry but moves temporal
comparison into consumers. A consumer that assumes every value is a date can
mis-handle a condition string.

**Falsifier:** The finding is wrong if every consumer treats the fields as an
explicit tagged union or opaque validity condition. That consumer contract is not
yet implemented because Practical Agency does not yet exist.

**Recommendation:** Practical Agency should represent expiry as a tagged
`timestamp | condition` value in its own normalized mission state or add a future
minor contract revision if cross-consumer ambiguity appears in real use.

### F-SA-3 — Prefix guards are deliberately incomplete

**Severity:** P3 / security coverage limit  
**Status:** accepted and documented

The verifier refuses known prompt/session/self-asserted prefixes and obvious skill
paths. It is not a universal URI, filesystem, content, or prompt-injection
scanner. A novel malicious identifier can still be syntactically accepted.

**Falsifier:** The finding is wrong if reference resolution occurs only through
trusted, allowlisted provider adapters and the record remains data. The security
contract requires exactly that, but no production adapter exists yet.

## Verdict from this lens

**PASS WITH RESIDUAL LIMITS.** No open P1 or P2 state-transition defect was found
in the frozen candidate. The remaining risks belong to downstream evidence and
time-resolution adapters and are explicitly outside the current verifier's claim.
