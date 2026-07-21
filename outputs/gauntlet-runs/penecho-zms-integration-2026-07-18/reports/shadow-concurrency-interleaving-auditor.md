# finding-set@1 — SHADOW concurrency-interleaving-auditor@1

## SC-01 — P1: Cross-device edits create ungoverned split-brain state

**Evidence:** Snapshots are browser-local with no documented sync. [V sources.md:8] [V sources.md:9]

**Schedule:** iPad saves `C-i`; Manta/desktop cannot receive it; both edit independently; each saves/exports; no version lineage or conflict winner exists. [I <- V sources.md:8; V sources.md:9]

**Recommended fix:** Do not credit continuity. Use explicit versioned PNG handoff or single-writer operation until conflict-aware sync exists.

**Falsifier:** Method: 50 synchronized two-device edit pairs. Threshold: one monotonic lineage with explicit conflicts/deterministic merges in 50/50 and zero lost edits. Timeframe: 48 hours.

## SC-02 — P1: A delayed response can cross a new-canvas boundary

**Schedule:** `A@r7` submits request; operator starts new canvas `B`; old response returns; without canvas/revision validation it can target wrong canvas or stale geometry. [V sources.md:7] [V sources.md:8] [V sources.md:15]

**Recommended fix:** Bind every request/response to immutable canvas UUID and revision; reject stale results.

**Falsifier:** Method: force delayed responses across 200 new-canvas transitions. Threshold: zero wrong-canvas mutations and 100% apply-to-origin or visible rejection. Timeframe: 48 hours.

## SC-03 — P2: Retry ambiguity can duplicate inference and CLI execution

**Schedule:** operation reaches executor; response is lost; client/operator retries; second inference/process starts; both finish. [V sources.md:10] [V sources.md:11] [V sources.md:15] [V sources.md:16]

**Recommended fix:** Stable operation ID and server-side single-flight/idempotent caching.

**Falsifier:** Method: 200 response-loss trials. Threshold: exactly one invocation, draft, and billable inference per ID. Timeframe: 48 hours.

## SC-04 — P2: Trace consent has a time-of-check/time-of-write gap

**Schedule:** request admitted trace-off; tracing enabled before completion; completion-time policy may persist prior private input. [V sources.md:14] [V sources.md:50]

**Recommended fix:** Capture immutable request-scoped consent at admission.

**Falsifier:** Method: 500 delayed requests with tracing toggled at every boundary. Threshold: trace-off admissions leave zero image artifacts; all trace-on artifacts have consent and purge correctly. Timeframe: 24 hours.

## SC-05 — P2: Replica/version skew invalidates route comparisons

**Schedule:** two replicas use mutable image; one updates first; matched requests hit different builds under one route label. [V sources.md:22] [V sources.md:23]

**Recommended fix:** Pin image/config, freeze rollouts, and record replica/model provenance per request.

**Falsifier:** Method: staggered restart plus 100 paired requests. Threshold: identical provenance or automatic exclusion, zero misclassified samples. Timeframe: seven days.

## Nonbinding vote

- SHADOW: Option 0 pending concurrency gates; Option 1 only as a serialized constrained experiment.
- Confidence: **0.86**
