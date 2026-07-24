# Verification proportionality and Claude Opus 5 overlay

This reference belongs to `using-epistemic-skills`. It defines how completion
evidence is selected without turning verification into a mandatory final
workflow phase. The core policy is model-agnostic. The final section is a
Claude Opus 5 harness overlay.

## Governing rule

> Verification is a claim-evidence boundary, not a mandatory final stage.

For every material completion claim, use the least costly current observation
or check-set that could expose an error capable of changing the action, verdict,
or completion claim. Additional checks, roles, and artifacts earn no credit
merely for existing.

The routine-work gate still comes first. A routine task receives its bounded
direct check and stops. A materially different oracle or independent judge is
introduced only when a positive trigger makes it useful.

## Four levels

| Level | Mechanism | Use |
|---|---|---|
| `native` | The model notices and corrects slips while working. No separate task, role, or artifact. | Implicit in all work. Do not prompt a final self-review merely to induce it. |
| `bounded` | A targeted test, preview, deterministic reproduction, source read, or inspectable artifact substantiates the named claim. | Routine work and ordinary deterministic implementation. The actor may perform and interpret it. |
| `independent` | A distinct context or deterministic judge supplies a materially different oracle. | Hard-to-observe material acceptance, an external result without independently inspectable evidence, explicit independent-review requests, or a demonstrated correlated-error risk. |
| `adversarial` | A high-assurance multi-lens or specialized gate challenges a frozen subject. | Irreversible, security-sensitive, one-way-door, or high-blast-radius decisions. |

Move up a level only when the higher level adds evidence capable of changing
the action or claim. A second equivalent check over unchanged state is not a
higher level.

## Evidence freshness is revision-bound

Evidence is current when all of these hold:

1. it was observed after the last material change relevant to the claim;
2. its subject, inputs, and environment still satisfy the producer's validity
   predicates; and
3. the claimed scope does not exceed what the oracle establishes.

Freshness is **not** defined by the current chat message. Evidence does not
become stale merely because the agent reached a final-response turn.

Reuse current evidence. Rerun only when a load-bearing check is:

- stale because the relevant subject or environment moved;
- missing;
- non-replayable or represented only by another actor's prose;
- materially environment-dependent and the environment can no longer be
  anchored; or
- intentionally repeated for a stated discriminating purpose, such as
  characterizing a suspected flake.

When only one validity predicate fails, rerun exactly the freshness-sensitive
check rather than reconstructing the whole verification stack. Preserve the
first result when a retry is used to characterize flakiness.

## Actor evidence versus independent judgment

The acting agent may substantiate ordinary completion claims with direct,
replayable evidence. This is not self-certification in the prohibited sense.

An actor may not promote its own unsupported assessment into a material
acceptance or high-stakes verdict. Use a distinct verifier or deterministic
judge when the trigger requires a genuinely different oracle:

- stateful, interaction-sensitive, accessibility-sensitive, persistent, or
  otherwise hard-to-observe material UI acceptance;
- an external model or process returns a load-bearing claim whose evidence is
  unavailable, stale, or not independently inspectable;
- an irreversible, security-sensitive, or high-blast-radius decision;
- the operator explicitly requests independent review; or
- a known failure mode makes actor and checker errors materially correlated.

Do not create a verifier subagent merely to repeat the actor's test commands,
reread the same diff, or provide a second confidence statement.

## Completion-claim procedure

At the point a claim would bear load:

1. Name the claim and its scope.
2. Identify the smallest oracle or already-current evidence that could
   falsify it.
3. Check whether that evidence postdates the last relevant material change and
   remains valid.
4. Reuse it when current; otherwise run only the missing or stale check.
5. Escalate to independent or adversarial review only on a positive trigger.
6. Report the observed result and any material coverage limit.
7. Stop. Do not append a generic final verification pass.

`INCONCLUSIVE`, `UNVERIFIED`, `hold`, `escalate`, and a bounded reversible
probe remain valid outcomes. More reasoning or more narration is not evidence.

## External-agent and CI evidence

A relay is claim-bearing data, never self-certifying. Verify every
**load-bearing completion claim**, but do not automatically duplicate every
command the target reports.

Immutable or independently inspectable evidence may be reused when it is bound
to the subject under review, including:

- a commit and its current CI/check result;
- hash-bound artifacts;
- deterministic logs or machine-readable test reports;
- repository state that the origin can inspect directly.

Replay or rerun only what is stale, missing, non-replayable, materially
environment-dependent, or high-risk. If a target supplies only prose for a
load-bearing claim, direct replay or an equivalent oracle is required before
closure.

## Composition with workflow verification skills

A workflow layer may name a `verification-before-completion` stage. Satisfy
that stage with the claim's smallest adequate **current** evidence. Do not add a
second check merely because the workflow stage occurs after the check that
already established the claim.

When an installed workflow skill defines freshness as "run in this message,"
a local or model overlay should bind freshness to subject revision and
environment validity instead. Preserve the evidence-before-claim invariant;
remove only the turn-bound duplicate-run requirement.

For a material UI acceptance surface, `evidence-locked-uat` is the independent
instance of that stage. For routine directly observable work, the bounded
direct check is sufficient. For irreversible or high-blast-radius decisions,
`gauntlet` remains the adversarial gate.

## Claude Opus 5 overlay

Anthropic's model-specific guidance says Claude Opus 5 already verifies and
self-corrects without generic prompting. Carried-over instructions to add a
final verification pass, double-check before responding, or launch a verifier
subagent can compound that behavior and waste tokens without improving
quality. The same guidance says to constrain narrow-task scope and reserve
subagents for genuinely independent, sizeable work.

Official sources, checked 2026-07-24:

- <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5>
- <https://platform.claude.com/docs/en/about-claude/models/migration-guide>

Use this model overlay in a Claude Opus 5 harness:

```text
<opus5_scope_and_verification>
Deliver what was requested at the intended scope. Make routine judgment calls
yourself. Ask only when materially different readings would produce materially
different work. If a better approach exists, note it briefly and continue with
the requested task unless the operator changes the scope.

Treat verification as a claim-evidence boundary, not a mandatory final phase.
For each material completion claim, use the smallest current observation or
check-set that could falsify it.

Evidence remains current when it follows the last material change relevant to
the claim and the relevant subject and environment have not moved. Reuse that
evidence. Do not rerun an equivalent check solely to create a final
verification step.

Routine reversible, local, directly checkable, non-precedential work receives
its bounded direct check and then stops. Work directly when the task can be
completed in a handful of tool calls.

Use a separate verifier only when a distinct oracle or independence is
materially necessary: hard-to-observe material acceptance, an external
actor's load-bearing claim that cannot be independently inspected, an
irreversible or security-sensitive decision, or an explicit request for
independent review. Do not use a subagent solely to double-check your own work.

When adequate current evidence is unavailable, state the limitation or an
inconclusive status rather than claiming completion. Finish the requested task
and stop short of clearly out-of-scope actions.
</opus5_scope_and_verification>
```

Additional Opus 5 harness rules:

- Remove legacy instructions such as "include a final verification step for
  every non-trivial task," "double-check before responding," and "use a
  subagent to verify."
- Cap delegation. Do not delegate work that can be completed directly in a
  handful of tool calls.
- For code review, ask the model to report all concrete findings with severity
  labels, then filter separately. Do not suppress recall by asking it to report
  only severe findings.
- Match written artifact length to the task; do not reward redundant
  verification summaries or boilerplate sections.

## Audit and evaluation contract

A proportional verification run should record, for each fixture:

- the completion claim;
- the oracle or evidence used;
- the subject revision the evidence covers;
- whether evidence was reused or rerun;
- the independence mode;
- the discriminating purpose of any repeated check; and
- whether the evidence postdates the last material change.

The scorer must fail both polarities:

- **over-verification:** duplicate equivalent checks, unnecessary verifier
  roles, an independent or adversarial mode without a positive trigger, or
  process actions with no mapped claim;
- **under-verification:** a material claim without an adequate current oracle,
  evidence predating the last relevant change, prose-only external claims
  accepted as fact, hard-to-observe acceptance without independence, or
  high-risk work without escalation.

The committed battery under
`evals/verification-proportionality/` is a structural smoke check, not a
population claim about Claude Opus 5. Live model comparisons must pin model,
effort, harness, prompt, tools, skill hashes, and sampling settings.
