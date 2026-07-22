# Psychology and epistemic skills — research synthesis

**Date:** 2026-07-22  
**Repository:** `ZMS-Labs/epistemic-skills`  
**Repository base examined:** `e1f605461bc2665f98069ff049f6ef629bd849c9` (`main`, release 2.8.0)  
**Implementation:** draft PR [#35 — feat: integrate epistemic flexibility controls](https://github.com/ZMS-Labs/epistemic-skills/pull/35)  
**Epistemic status:** Consensus discovery completed; authenticated Scite reception and Zotero holdings/deposit unavailable, so reception, notice status, and durable holdings remain `UNVERIFIED`

## Research question

To what extent can the repository's agentic-coding, planning, fine-tuning, and epistemic disciplines be enhanced by—or derived from—Acceptance and Commitment Therapy (ACT), Dialectical Behavior Therapy (DBT), and Cognitive Behavioral Therapy (CBT)?

The investigation treated “derived from psychology” as a stronger claim than “can be described using psychological language.” A useful derivation must specify enough of a discipline's trigger, representation, operation, evidence source, stopping rule, and update behavior to distinguish it from plausible alternatives.

## Determination

| Hypothesis | Determination |
|---|---|
| The skills can be enhanced by ACT, DBT, CBT, and adjacent metacognition research. | **Strongly supported.** Several concrete controls can be integrated and tested. |
| The skills can be redescribed in psychological language. | **Largely true but weak evidence.** Many adaptive control systems permit such a redescription. |
| The complete repository can be uniquely derived from ACT, DBT, or CBT. | **Not supported under a meaningful derivation standard.** Psychology does not specify the repository's software-specific provenance, formal-method, independence, artifact-identity, and deterministic-verdict machinery. |
| The repository is a psychologically informed process architecture completed by formal epistemology and safety engineering. | **Best-supported formulation.** |

The compact synthesis is:

> ACT supplies a global control objective: epistemic flexibility. DBT supplies regulation under conflict, pressure, and recurrent failure. CBT supplies collaborative formulation and empirical belief testing. The repository supplies enforceable software artifacts, formal derivation, provenance, runtime independence, and deterministic verification.

## A derivation test

Represent a skill as:

```text
S = (trigger, state representation, operation, evidence source, stopping rule, memory update)
```

ACT, DBT, and CBT can often help derive:

- triggers such as fusion with fluent language, uncertainty, conflicting demands, avoidance, recurrent mistakes, and untested assumptions;
- representations such as thought versus fact, authorized priority versus proxy, prompting event versus chain link, and observation versus interpretation;
- operations such as defuse, formulate, validate, test, tolerate, synthesize, and recommit;
- updates such as revising a belief, recording a replacement response, or recommitting after a failed approach.

They do not derive at engineering specificity:

- which repository artifacts or Git state must be inspected;
- how hashes, receipts, manifests, and supersession graphs establish identity or freshness;
- how a frozen dossier becomes a closed evidence world;
- how reviewer isolation and cross-family independence are enforced;
- which formal theory decides a concurrency, normalization, complexity, or consistency claim;
- how a deterministic judge computes a verdict;
- how runtime observability distinguishes `PASS`, `FAIL`, `INCONCLUSIVE`, and `BLOCKED_ENVIRONMENT`.

Therefore, psychology can derive important process controls and some stage semantics, but not the complete implementation.

## Functional synthesis

### ACT: language control and epistemic flexibility

The useful translation is not that an agent experiences acceptance or mindfulness. It is that language should not receive control authority merely because it is fluent, familiar, or self-generated.

**Epistemic flexibility** is the capacity to:

1. contact current evidence rather than rely on remembered or summarized state;
2. treat generated and received language as claim-bearing data rather than truth or authorization;
3. preserve source, role, and session context;
4. retain unresolved uncertainty without manufacturing closure;
5. orient action to an explicitly operator-authorized priority;
6. choose a bounded action whose consequences can update the model.

Agent-safe translations of ACT processes:

| ACT process | Functional agent translation |
|---|---|
| Present-moment contact | Read the live repository, runtime, tool, or operator state. |
| Cognitive defusion | Separate the text of a claim from its truth, evidence, and authority. |
| Self-as-context | Preserve distinctions among agent, role, source, session, artifact, and claim. |
| Acceptance | Represent `UNVERIFIED`, `INCONCLUSIVE`, and `BLOCKED` without forcing a positive conclusion. |
| Values | Use explicitly operator-authorized priorities rather than presumed intrinsic values. |
| Committed action | Take bounded, reversible or authorized action with observable evidence. |

This maps strongly to Blindspot Pass, Continuity Verify, Write Goal, Evidence Research, and the repository-wide fail-closed rules.

A further ACT-derived check concerns **research as avoidance**. More investigation is not automatically more epistemic. Before escalating research, ask:

- What decision could another paper change?
- What observation would terminate the search?
- Is a reversible empirical probe now cheaper and more discriminating?
- Is the search gathering evidence or avoiding action under uncertainty?

### DBT: regulation under conflict and closure pressure

Agents do not experience human emotional distress. The functional analogue is regulation of action policy when contextual pressure would otherwise cause premature, rigid, or self-protective behavior.

Relevant pressures include:

- completion and closure pressure;
- urgency or instruction-following pressure;
- consistency with a previous answer;
- sunk-cost pressure after implementation;
- majority pressure from correlated reviewers;
- pressure to replace `BLOCKED` with plausible prose.

DBT contributes four strong process ideas.

#### Acceptance plus change

Before attacking or replacing a design, identify what genuine constraint or problem it correctly addresses. A reviewer should preserve the valid kernel of the current design even when recommending change.

#### Dialectical synthesis

For a material conflict, record:

- the valid kernel of position A;
- the valid kernel of position B;
- the synthesis or conditional integration;
- the residual tension the synthesis does not eliminate.

A forced synthesis is not required; some conflicts remain real trade-offs.

#### Behavioral chain analysis

For recurrent agent failures:

```text
prompting event
→ vulnerabilities
→ intermediate links
→ target failure
→ consequences
→ earliest interruptible link
→ replacement behavior
→ rehearsal fixture
```

Agent-relevant vulnerabilities include stale context, compaction, missing tools, ambiguous authority, high token pressure, leading prompts, correlated reviewers, and attractive but unverified canonical patterns.

#### Tolerating blocked states

The system should preserve `BLOCKED`, `UNVERIFIED`, `INCONCLUSIVE`, or “requires operator authorization” until evidence, authority, or a bounded reversible probe changes the state. Narrative confidence is not an escape route.

### CBT: collaborative empiricism and preregistered tests

CBT provides the closest analogue to the repository's empirical procedure:

1. expose the operative assumption;
2. operationalize it;
3. derive a prediction;
4. name a disconfirming observation;
5. construct a discriminating test;
6. run the test;
7. update the belief and plan.

The implementation pattern is:

```yaml
belief: what currently bears load
prediction: what should be observed if the belief is correct
disconfirming_observation: what would count against it
test: the bounded action or measurement
result: what was observed
update: how the belief, plan, or control state changes
```

The prediction and disconfirming observation must be recorded before the result is visible. This limits post-hoc reinterpretation.

The repository's strongest CBT correspondences are:

- Blindspot Pass as collaborative formulation and guided discovery;
- Applying Formal Rigor as operationalization and derivation;
- Evidence Research as external evidence gathering;
- Gauntlet as competing formulations and falsifiers;
- Evidence-Locked UAT as a behavioral experiment;
- Decision Ledger as an externalized decision/correction record;
- Continuity Verify as resumption and relapse-prevention discipline.

## Skill-by-skill mapping

| Repository member | Strongest psychological contribution | What psychology does not replace |
|---|---|---|
| `using-epistemic-skills` | Process-based target selection and sequencing | Router contracts, receipt semantics, tool orchestration |
| `helix` | Acceptance/change dialectic and staged treatment-like sequencing | Exact workflow-skill pairings |
| `blindspot-pass` | ACT defusion; CBT guided discovery; DBT vulnerability analysis | Repository-specific reconnaissance and artifact reads |
| `applying-formal-rigor` | Operationalization, metacognitive control, explicit falsification | Formal mathematics, lower bounds, type theory, database and distributed-systems theory |
| `evidence-research` | Collaborative empiricism, counterevidence search, uncertainty tolerance | Scholarly indexing, DOI identity, reception analysis, durable holdings |
| `write-goal` | ACT committed action; CBT action planning; DBT commitment and coping-ahead | Proof bundles, provenance, runtime goal adapters |
| `gauntlet` | Dialectics, competing formulations, validation before change | Frozen dossiers, isolation barriers, deterministic selection and verdict rules |
| `evidence-locked-uat` | Behavioral experiments and response prevention against self-certification | Runtime observability, manifests, blinded verification, deterministic judge |
| `decision-ledger` | Thought/belief records, diary-card-like monitoring, chain analysis | Append-only persistence, provenance coordinates, supersession graph |
| `continuity-verify` | Source monitoring, present-state reorientation, relapse prevention | Git/artifact re-anchoring and authorization verification |

## Implemented design decision

The psychology material was **not** added as separate `act`, `dbt`, or `cbt` skills. The relevant processes are cross-cutting controls inside existing epistemic moments, not distinct moments with unique triggers and stopping boundaries.

PR #35 therefore integrates:

1. claim/source separation;
2. operator-authorized priority versus success proxy;
3. preregistered discriminating tests;
4. recurrent-failure chains;
5. explicit closure control;
6. validation kernels and dialectical synthesis.

The design preserves the repository's existing family rules: floors rather than ceilings, derive or verify rather than assert, explicit boundaries, fail-closed degradation, provenance and independence, and re-fire rather than patch when the subject changes.

## Fine-tuning and evaluation implications

The psychological contribution is most testable as **process supervision**, not as therapy vocabulary in prompts.

A useful training unit is:

```text
context
→ trigger discrimination
→ structured epistemic artifact
→ bounded action
→ external feedback
→ revision
→ durable update
```

Negative contrastive examples should include:

- trusting a fluent handoff summary;
- treating a review or plan as authorization;
- changing a correct answer because a critique prompt presupposes error;
- treating correlated reviewers as independent evidence;
- optimizing a metric while violating the authorized objective;
- replacing a blocked state with narrative evidence;
- continuing research when a reversible probe is more discriminating;
- silently patching a stale output instead of re-firing the owning skill.

The committed behavioral program specifies four arms:

- **A:** baseline workflow;
- **B:** release 2.8.0;
- **C:** psychology-language reflection without artifact controls;
- **D:** the integrated epistemic-flexibility branch.

Primary outcomes should be deterministically scored where possible: false-act rate on traps, false-hold rate on clean controls, claim/source alignment, prediction preregistration, proxy separation, recurrence-chain quality, and closure choice. Secondary outcomes include token/tool cost, latency, calibration, and operator correction burden.

## Limits and non-transfer claims

1. Agents do not literally possess human distress, intrinsic values, therapeutic alliance, or clinical psychopathology. All translations are functional and non-anthropomorphic.
2. The same architecture can also be motivated by philosophy of science, control theory, cybernetics, high-reliability organizations, metacognition, and software safety engineering. Psychology is a generative basis, not a unique origin.
3. Psychotherapy mechanism research often identifies statistical or conceptual mediators without fully specified functional mechanisms. The repository should require executable triggers, operations, artifacts, and stopping rules rather than inherit vague process labels.
4. Evidence that a human therapeutic process works does not establish that the translated process improves language-agent behavior. The four-arm behavioral evaluation is required.
5. Consensus discovery was completed, but Scite reception and Zotero holdings/deposit were unavailable. No paper is represented as reception-verified or durably deposited by this run.

## Selected discovery anchors

The links below preserve the exact Consensus records consulted in the design session.

1. Jenna A. Macri & Ronald D. Rogge (2024), *Clinical Psychology Review*: [Examining domains of psychological flexibility and inflexibility as treatment mechanisms in acceptance and commitment therapy](https://consensus.app/papers/examining-domains-of-psychological-flexibility-and-macri-rogge/32da3a4e8f975aabb8d736defc0ddc1d/?utm_source=chatgpt). Meta-analysis/systematic review of ACT flexibility and inflexibility processes.
2. Shane J. McLoughlin & B. Roche (2023), *Behavior Therapy*: [ACT: A Process-Based Therapy in Search of a Process](https://consensus.app/papers/act-a-processbased-therapy-in-search-of-a-process-mcloughlin-roche/c20e24bd01e956719a363e2519d33c14/?utm_source=chatgpt). Critical examination of ACT mechanism and measurement claims.
3. L. Mehlum (2021), *Current Opinion in Psychology*: [Mechanisms of change in dialectical behaviour therapy for people with borderline personality disorder](https://consensus.app/papers/mechanisms-of-change-in-dialectical-behaviour-therapy-for-mehlum/89422e661918511c8850cdaa15d432fe/?utm_source=chatgpt). Review of regulation, skills, mindfulness, validation, and relational factors.
4. S. Rudge, J. Feigenbaum & P. Fonagy (2020), *Journal of Mental Health*: [Mechanisms of change in dialectical behaviour therapy and cognitive behaviour therapy for borderline personality disorder](https://consensus.app/papers/mechanisms-of-change-in-dialectical-behaviour-therapy-and-rudge-feigenbaum/2327c768cbfa53d5a85ff3f3d12240cd/?utm_source=chatgpt). Critical mechanism review.
5. Matthew W. Southward, Madeline L. Kushner, Doug R. Terrill & Shannon Sauer-Zavala (2024), *Psychiatric Clinics of North America*: [A Review of Transdiagnostic Mechanisms in Cognitive-Behavior Therapy](https://consensus.app/papers/a-review-of-transdiagnostic-mechanisms-in-southward-kushner/1bb54e2c40ad57acab08d26141718c0d/?utm_source=chatgpt). CBT-specific, transtheoretical, and psychopathological mechanisms.
6. Iony D. Ezawa & S. D. Hollon (2023), *Psychotherapy*: [Cognitive Restructuring and Psychotherapy Outcome: A Meta-Analytic Review](https://consensus.app/papers/cognitive-restructuring-and-psychotherapy-outcome-a-ezawa-hollon/978363ef09ee5e7db6b30e691d069dfc/?utm_source=chatgpt). Meta-analysis of within-session cognitive restructuring and outcome.
7. T. A. Carey, R. Griffiths, James E. Dixon & S. Hines (2020), *Frontiers in Psychiatry*: [Identifying Functional Mechanisms in Psychotherapy: A Scoping Systematic Review](https://consensus.app/papers/identifying-functional-mechanisms-in-psychotherapy-a-carey-griffiths/9b4d642e50d85cab8be16c330f74b75c/?utm_source=chatgpt). Critique of mechanism claims that are not functionally specified.
8. Stephen M. Fleming & Hakwan Lau (2014), *Frontiers in Human Neuroscience*: [How to measure metacognition](https://consensus.app/papers/how-to-measure-metacognition-fleming-lau/81100b9611d75cfe9133f25f0bdec526/?utm_source=chatgpt). Distinguishes metacognitive bias, sensitivity, and efficiency.
9. Jason Carpenter, Maxine T. Sherman, Rogier A. Kievit, Anil K. Seth, Hakwan Lau & Stephen M. Fleming (2019), *Journal of Experimental Psychology: General*: [Domain-General Enhancements of Metacognitive Ability Through Adaptive Training](https://consensus.app/papers/domaingeneral-enhancements-of-metacognitive-ability-carpenter-sherman/ba1e8f136bb359179a04e23472bf64dc/?utm_source=chatgpt). Experimental evidence on feedback-driven metacognitive calibration and transfer.

Additional discovery in the session covered ACT process mediation, workplace ACT subprocesses, DBT emotion-regulation and skills mechanisms, CBT collaborative empiricism, psychotherapy emotional-change mechanisms, and process-based therapy. Those results informed query expansion and boundary checking; the nine anchors above carried the final design argument.

## Durable continuation

The authoritative engineering continuation is:

- [`docs/handoffs/2026-07-22-epistemic-flexibility-v3.md`](../handoffs/2026-07-22-epistemic-flexibility-v3.md)
- [`docs/superpowers/specs/2026-07-22-epistemic-flexibility-integration.md`](../superpowers/specs/2026-07-22-epistemic-flexibility-integration.md)
- [`docs/superpowers/plans/2026-07-22-epistemic-flexibility-v3.md`](../superpowers/plans/2026-07-22-epistemic-flexibility-v3.md)
- [`plugins/epistemic-skills/skills/using-epistemic-skills/reference/epistemic-flexibility.md`](../../plugins/epistemic-skills/skills/using-epistemic-skills/reference/epistemic-flexibility.md)

This memo preserves the complete hypothesis evaluation and research rationale so that future work does not depend on the originating chat.