# finding-set@1 — opportunity-cost-accountant@2

## OC-01 — P1: The pilot lacks a strong counterfactual

**Mechanism:** An absolute >=80% useful-completion result can make PenEcho look successful without showing it beats the lower-maintenance alternative: native drawing/annotation, PNG export, and ordinary multimodal chat. PenEcho's durable handoff is PNG and snapshots remain local. [V sources.md:8] [V sources.md:9] The handwriting premise is small and conditional. [V sources.md:38] [V sources.md:39]

**Crowded out:** Improving and measuring the already-available export-plus-chat workflow.

**Recommended fix:** Make every representative task a paired comparison against a rehearsed export-plus-chat baseline. Promotion depends on incremental time, quality, and reuse.

**Falsifier:** Method: randomized paired crossover on the same 20 tasks across iPad and Manta/InkFlow. Threshold: PenEcho has >=20-point higher useful completion or >=25% lower median time, no material quality regression, and voluntary reuse on at least three tasks. Timeframe: two weeks.

## OC-02 — P1: Option 1 spends information budget on three questions at once

**Mechanism:** The pilot simultaneously tests product value, device fit, and three execution lanes. API and CLI have different boundaries; Manta quality is unproven; ZMS has no documented local vision route; latency varies by provider/workload. [V sources.md:10] [V sources.md:11] [V sources.md:15] [V sources.md:24] [V sources.md:31]

**Crowded out:** A smaller, higher-power experiment using one quality-baseline route to decide whether interaction deserves further attention.

**Recommended fix:** Stage Option 1 internally: cloud/API quality baseline first; local VLM only after OC-01 clears; CLI only where repository context is essential.

**Falsifier:** Method: log setup, execution, troubleshooting, and analysis time. Threshold: all lanes yield >=90% complete comparable observations within <=8 operator-hours, no lane >15% unusable trials. Timeframe: one week.

## OC-03 — P2: Cluster hosting adds durable surface without continuity

**Mechanism:** Remote hosting requires HTTPS, auth, rate limiting, and size controls; the default listener is broad; tracing can retain images. [V sources.md:12] [V sources.md:13] [V sources.md:14] Yet snapshots remain local. [V sources.md:8]

**Crowded out:** Reusable ingress/identity/privacy/model-gateway hardening or disposable use with no ownership.

**Recommended fix:** Promote to Option 2 only through a crossover that fully charges security, upgrade, and privacy labor.

**Falsifier:** Method: alternate local and hosted access while logging sessions, setup, incidents, maintenance. Threshold: hosted increases sessions >=30% or cuts setup >=50%, with <30 minutes/week maintenance and zero unauthorized exposure/retained-canvas events. Timeframe: four weeks.

## OC-04 — P2: The local-model lane can become an infrastructure project disguised as evaluation

**Mechanism:** Existing routes do not document a vision model; nominal availability does not establish PenEcho accuracy, structured-draft compliance, or latency; LiteLLM ownership remains unresolved. [V sources.md:24] [V sources.md:33] [V sources.md:34] [I <- V sources.md:21; V sources.md:22]

**Crowded out:** Resolving model-gateway ownership as a reusable capability independently of PenEcho.

**Recommended fix:** Make local inference a separately budgeted follow-on. The initial value test consumes an already-working explicit route with no new serving or gateway work.

**Falsifier:** Method: time-box one already-served vision connection with no production edits. Threshold: working in <=2 hours, >=90% structured validity, no silent cloud fallback, no control-plane changes. Timeframe: one day.

## OC-05 — P2: Counting fork blockers does not price the permanent obligation

**Mechanism:** Synchronization adds durable state beyond local snapshots/PNG; modified network service has source-offer obligations; traces add privacy concern. [V sources.md:8] [V sources.md:9] [V sources.md:14] [V sources.md:17]

**Crowded out:** Disposable adapters, export/import improvements, or higher-frequency automation.

**Recommended fix:** Require quantified weekly value and a maintenance ceiling before a fork is eligible.

**Falsifier:** Method: four-week blocker diary, disposable adapter attempts, and bounded fork spike. Threshold: three workflows each occur >=2 times/week, cannot be solved otherwise, save >=2 hours/week, and cost <1 hour/week maintenance.

## OC-06 — P3: CLI advantage omits its carrying cost

**Mechanism:** CLI launches local processes and is trusted-LAN only; API mode has a remote boundary. [V sources.md:11] [V sources.md:12] A workbench carries setup, auth, scoping, and upgrades.

**Recommended fix:** Calculate utility advantage using total operator cost.

**Falsifier:** Method: 30-day matched API/CLI log. Threshold: CLI retains >=20% utility per total cost, <15 minutes/week maintenance, and zero authority violations.

## Hypothesis vote

- Supports a staged local pilot, amended to begin with a paired cloud/API interaction-value test.
- Kills central hosting as continuity.
- Verdict: **CONDITIONAL**
- Confidence: **0.91**
