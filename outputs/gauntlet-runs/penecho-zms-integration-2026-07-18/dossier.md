# Frozen dossier: PenEcho adoption path for ZMS Labs

**Frozen:** 2026-07-18
**Axis:** open-question exploration
**Depth:** standard
**Decision owner:** ZMS Labs operator
**Scope:** decide the adoption and integration path; do not implement it in this run.

## Rewritten decision request

Choose the least-regret, evidence-generating path by which ZMS Labs can test and, only if justified, adopt upstream PenEcho as a pen-first visual AI client across iPad Pro, iPhone, and Supernote Manta, using explicit cloud, subscription-CLI, or local multimodal inference routes, while preserving ZMS source-of-truth discipline, privacy, route honesty, reversibility, and upstream compatibility. Decide what should be tested locally, what belongs in k3s/GitOps later, whether a wrapper repository is warranted, and what measured evidence would ever justify a fork.

## Blindspot pass

### Landmines

- Calling a browser canvas “integrated” when its snapshots are still device-local and its durable handoff is only PNG. [V sources.md:8] [V sources.md:9]
- Deploying CLI mode behind public ingress even though each valid request launches a local process and upstream limits it to localhost/trusted LAN. [V sources.md:11]
- Creating a second LiteLLM source of truth while current deployable manifests already live under Fleet Orchestrator and the central GitOps base carries only a secret. [V sources.md:21] [V sources.md:22]
- Advertising nominally multimodal local models before the actual PenEcho structured-draft workload is tested. [V sources.md:33] [V sources.md:34]
- Enabling traces that retain private canvas images without an explicit retention and privacy choice. [V sources.md:14]
- Treating AGPL as a blocker or ignoring it; unmodified hosting is different from serving a modified network version. [V sources.md:17]

### Hidden context

- The desired value is interaction quality and continuity across devices, not simply “another AI web app.”
- Manta has an immediate official bridge through InkFlow to a Windows/macOS browser, but native on-device PenEcho compatibility remains unproven. [V sources.md:30] [V sources.md:31]
- Existing ZMS model-route honesty is a valuable invariant: explicit local and paid routes already replaced deceptive aliases. [V sources.md:23] [V sources.md:25]
- Scholarly evidence supports only plausibility: handwriting advantages are small/conditional, digital creativity research is fragmented, and edge inference has trade-offs. [V sources.md:38] [V sources.md:39] [V sources.md:41] [V sources.md:42]
- Scite full-text/reception validation is unavailable due quota, so the research layer must not carry the deployment decision. [V sources.md:43]

### What good looks like

- Within a short pilot, the operator can complete representative pen-first tasks from iPad and Manta with acceptable recognition, correct spatial responses, and tolerable latency.
- Local and cloud choices are visibly and truthfully named; no silent cloud fallback is possible.
- The pilot changes no existing production control plane, requires no application fork, and can be deleted cleanly.
- A deployment decision is based on measured task success, latency, cost, privacy boundary, and repeated-use value—not model reputation or a compelling demo.
- If promoted, the service is cluster-native, pinned, authenticated, reproducible, and owned by one ZMS repo with an explicit upstream-update policy.

### Questions you should be asking

1. **Does PenEcho materially improve real workflows over screenshots plus ordinary chat?** Best current guess: probably for some spatial/diagram tasks, not enough to assume broad value; measure task completion and reuse.
2. **Which device path is real?** Best current guess: iPad Safari is the main direct canvas; Manta InkFlow to a desktop browser is the strongest immediate Manta path; iPhone is likely review/emergency input rather than primary drawing.
3. **Which inference route works on PenEcho's actual output contract?** Best current guess: a cloud model is the quality baseline, while Qwen3.5 27B or another served local VLM is a candidate, not a conclusion.
4. **Who owns LiteLLM?** Best current guess: Fleet Orchestrator owns the current deployable manifests, but live-cluster ownership must be verified before any new client depends on it. [I <- V sources.md:21, sources.md:22]
5. **What observation would justify a fork?** Best current guess: only repeated high-value blockers uniquely requiring server-side canvas synchronization, device adapters, or model-selector changes after a hosted unmodified pilot.

## Fixed evidence and constraints

- Upstream PenEcho already supports API, Codex CLI, and Claude CLI executors. [V sources.md:10]
- API mode has a documented remote boundary: HTTPS, authentication, rate limiting, and request-size controls. [V sources.md:12]
- CLI modes are a distinct trusted-LAN boundary and must not be conflated with API deployment. [V sources.md:11]
- Browser snapshots are local; central hosting does not by itself create cross-device canvas state. [V sources.md:8]
- The default listener is broad (`0.0.0.0:3888`) and must be constrained by deployment policy. [V sources.md:13]
- The existing ZMS LiteLLM configuration has no documented local vision route. [V sources.md:24]
- The recommendation must obey the five decision invariants in `sources.md`. [V sources.md:47] [V sources.md:48] [V sources.md:49] [V sources.md:50] [V sources.md:51]

## Option set @1

### Option 0 — Steeled null: opportunistic upstream use only

Run PenEcho only in disposable/local sessions, export PNGs when valuable, and make no ZMS repository or service commitment. This preserves maximum optionality and is correct if recurring value is weak. Kill the null when at least three valuable weekly tasks across two devices repeatedly suffer material setup/handoff friction.

### Option 1 — Unmodified workstation/LAN pilot

Run a pinned, unmodified upstream instance on a controlled workstation. Test three separate lanes: cloud API baseline; OpenAI-compatible local endpoint; and subscription CLI only on localhost/trusted LAN. Use iPad/iPhone over the trusted LAN where appropriate and Manta through InkFlow to the desktop browser. No new ZMS repo, no cluster ingress, no fork. This is the cheapest direct test of device fit, model fit, and recurring value.

### Option 2 — Pinned cluster-hosted upstream wrapper

Only after Option 1 passes, create a minimal ZMS-owned deployment wrapper that pins an unmodified upstream revision/image, exposes API mode behind the existing ingress/auth/rate-limit controls, and consumes one truthfully owned model gateway. It standardizes delivery but explicitly does not promise cross-device canvas synchronization. CLI mode remains outside public ingress.

### Option 3 — Trusted-LAN CLI workbench as a specialized lane

If matched tests show meaningful value over API mode, preserve a tightly scoped workstation workbench for Codex/Claude CLI tasks, with read-only or task-scoped repository authority. This is an adjunct to Option 1/2, not the default public architecture.

### Option 4 — Purpose-built ZMS fork

Fork only to solve measured, recurring blockers that cannot be handled by deployment configuration or a disposable adapter: durable synchronized canvases, device-specific interaction/import/export, or a necessary model-capability UI. This has the lowest reversibility and highest maintenance/licensing/state-migration burden.

## Formal comparison

### Real-options and value-of-information result

Option 1 buys the most decision-relevant information at the lowest irreversible cost: device compatibility, user value, model conformance, latency, and route economics. Option 2 is exercised only if that information is favorable. Option 4 spends the option before learning. Therefore the dominant sequence is `1 -> conditional 2 -> exceptional 4`, with Option 0 remaining the correct outcome if the pilot does not clear thresholds.

### Architecture and SSOT result

The current LiteLLM fact is stored in two places with different completeness: secret-only central GitOps and deployable Fleet Orchestrator manifests. [V sources.md:21] [V sources.md:22] Duplicating routes for PenEcho would create a configuration **update anomaly**: one model alias or credential boundary could change while the other stays stale. The pilot must consume an existing verified endpoint directly; a later wrapper may reference exactly one model-routing owner, never copy its catalog.

### Distributed-state result

Browser snapshots are local replicas with no documented server synchronization. [V sources.md:8] A cross-device “open my current canvas” promise would require at least read-your-writes and monotonic-read session guarantees, conflict semantics, and an authenticated data plane. Neither hosting nor LiteLLM provides those. Treat synchronization as a separate product decision, not a hidden acceptance criterion for a deployment wrapper.

### Type/invariant result

The model route exposed to PenEcho should be representable as an explicit sum type—`Local(model)` or `Cloud(provider, model)`—with no implicit fallback. That makes “local label, cloud execution” an illegal state rather than a documentation convention, preserving the existing route-honesty invariant. [V sources.md:23] [V sources.md:25]

### Complexity result

Let `U` be upstream releases and `P` local application patches. A wrapper has update work approximately proportional to `U`; a divergent fork adds review/rebase/testing across the `U x P` interaction surface. The lower-complexity wrapper is therefore preferred until measured blockers make at least one patch essential. This is a maintenance trade-off, not a claim that a fork is never appropriate.

### Blast-radius result

Option 1 fails inside a disposable workstation/LAN boundary. Option 2 adds ingress, auth, model-gateway, and cluster dependencies but remains declaratively removable. Option 3 concentrates CLI and repository authority and therefore needs the narrowest trust boundary. Option 4 adds persistent state and migration obligations. The sequence follows increasing blast radius and decreasing reversibility.

## DeepReason docket

- **Mode:** manual-docket
- **Run root / docket path:** this dossier
- **Replay status:** not applicable
- **Why used or skipped:** no callable DeepReason runtime is available; this manually frozen docket preserves hypotheses and discriminators but does not claim DeepReason replay guarantees.

### Survivor theories

- **Pen-first value is task-specific, not universal.** Falsifier: a representative task set shows no improvement in completion, comprehension, or reuse versus ordinary chat/screenshot handoff.
- **A local pilot dominates immediate infrastructure.** Falsifier: central hosting is required merely to test more than one available device or inference lane safely.
- **Cloud establishes the quality ceiling; local earns promotion by measured parity.** Falsifier: an already-served local vision route passes the same command/structure/latency thresholds before a cloud baseline is needed.
- **A wrapper is enough until state/device blockers repeat.** Falsifier: three or more high-value recurring workflows fail uniquely because upstream lacks synchronization or device adaptation.

### Refuted theories

- **“Self-hosted” automatically means private.** Refuted because logs/traces, broad listeners, silent fallbacks, and remote endpoints can still move or retain canvas data. [V sources.md:12] [V sources.md:13] [V sources.md:14]
- **Central hosting solves continuity.** Refuted because snapshots remain browser-local. [V sources.md:8]
- **A nominal vision model proves local readiness.** Refuted because model availability does not establish PenEcho's task/structured-draft contract. [V sources.md:34]

### Discriminating tests

| Test | Decides between | Priority | Pass signal |
|---|---|---:|---|
| 20-task pen workflow matrix on iPad and Manta/InkFlow | 0 vs 1 | P1 | >=80% useful completion and repeated voluntary use |
| Matched cloud vs local-VLM commands | cloud baseline vs local promotion | P1 | local meets agreed accuracy/structure and p95 latency without silent cloud fallback |
| Direct/local URL vs pinned hosted URL for one week | 1 vs 2 | P2 | hosting materially reduces setup/config drift or increases completed sessions |
| API vs CLI matched read-only repo-context tasks | 2 vs 3 | P2 | CLI delivers >=20% utility/cost advantage without broad write authority |
| Two-week blocker log plus disposable adapter | 2 vs 4 | P2 | >=3 recurring high-value blockers uniquely require application modification |

### Docket limits

No device interaction test, live-cluster ownership check, local-model PenEcho test, cost measurement, or security review has yet been executed. The dossier decides the best experiment sequence, not production readiness.

## Provisional thesis for attack

**Conditional GO:** approve only Option 1, the unmodified workstation/LAN pilot. Do not yet create a ZMS fork, production ingress, or durable wrapper repo. Promotion to Option 2 requires measured repeated value, explicit device/model thresholds, and a verified single owner for the live LiteLLM/control-plane route. Option 4 is NO-GO absent recurring modification-only blockers.
