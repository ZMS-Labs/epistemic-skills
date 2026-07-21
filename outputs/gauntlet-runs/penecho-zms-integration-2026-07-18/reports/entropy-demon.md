# finding-set@1 — entropy-demon@2

## ED-01 — P1: The pinned pilot has no reproducible last-known-good

**Decay mechanism:** Evidence identifies upstream as current `main`, not an immutable revision. Provider latency varies and nominal models do not prove workload conformance. Without application/model/settings/task/environment identities, results decay as dependencies change. [I <- V sources.md:5; V sources.md:15; V sources.md:34; V sources.md:47]

**Recommended fix:** Record immutable PenEcho commit/image digest, dependency lock, actual model identity, settings, browser/OS/InkFlow versions, hashed tasks, rubric, and results in one evidence pack.

**Falsifier:** Method: rebuild twice on a clean workstation from the pack. Threshold: 100% immutable resolution, >=95% identical pass/fail, no undocumented manual config. Timeframe: within seven days.

## ED-02 — P1: Browser-local canvas state makes continuity evidence self-erasing

**Decay mechanism:** Snapshots are local, new-canvas behavior can overwrite state, unconfirmed drafts are excluded, and durable handoff is PNG. [V sources.md:8] [V sources.md:9]

**Recommended fix:** Make continuity a separate gate; export/hash every scored canvas and record all loss.

**Falsifier:** Method: 30 save/close/reopen/device-switch cycles without manual PNG re-import. Threshold: zero lost confirmed canvases, >=95% recovery within 60 seconds. Timeframe: 14 days.

## ED-03 — P2: The likely gateway is mutable and ownerless

**Decay mechanism:** LiteLLM uses `main-latest`; central GitOps contains only its secret while deployable manifests live elsewhere. [V sources.md:21] [V sources.md:22] [V sources.md:26]

**Recommended fix:** Do not depend on it until live image is digest-pinned, one repo is authoritative, and owner plus rollback exists.

**Falsifier:** Method: map live pod digest/effective config to one reviewed commit and execute rollback. Threshold: 100% Git-to-live provenance, no mutable reference, restore in <=15 minutes. Timeframe: before a scored gateway run.

## ED-04 — P2: Remote-boundary credentials have no demonstrated lifecycle

**Decay mechanism:** HTTPS/auth/rate limiting/size controls create long-lived secrets/certificates/policies without demonstrated ownership or expiry testing. [V sources.md:12]

**Recommended fix:** Require owner, inventory, renewal, maximum age, revocation, and rotation drill before Option 2.

**Falsifier:** Method: inventory and rotate a provider credential and ingress certificate. Threshold: full coverage, zero unknown owners/expired artifacts, old credentials rejected, <5-minute interruption. Timeframe: before promotion.

## ED-05 — P2: Route drift can corrupt privacy and experiment results

**Decay mechanism:** Explicit paid routes and removed deceptive fallbacks are a valuable maintenance regime, but multiple executors without per-request attestation can make a local result cloud-backed. [V sources.md:10] [V sources.md:25] [V sources.md:48] [V sources.md:49]

**Recommended fix:** Record executor, endpoint class, actual model, and fallback status for every scored request; fail on missing/conflicting identity.

**Falsifier:** Method: make local endpoint unavailable. Threshold: zero cloud executions, zero success without route evidence, 100% explicit local failure. Timeframe: before and throughout pilot.

## ED-06 — P3: Debug tracing can become a durable private-data store

**Decay mechanism:** Tracing captures images and responses; no enforced retention/backup exclusion/drift detector is established. [V sources.md:14] [V sources.md:50]

**Recommended fix:** Lock off ordinary tracing; bounded diagnostics require expiry, purge, quota, backup exclusion, and zero-data check.

**Falsifier:** Method: trace synthetic canvases and inspect storage/backups after expiry. Threshold: 100% deletion <=24 hours, zero backup copies, alert within 5 minutes if left enabled.

## ED-07 — P3: Manta viability can decay with an unversioned bridge

**Decay mechanism:** InkFlow makes Manta input plausible but quality is unproven; updates can regress it. [V sources.md:30] [V sources.md:31]

**Recommended fix:** Capture bridge version matrix and rerun a Manta regression script after each update.

**Falsifier:** Method: repeat 20 gestures/tasks across baseline and next update. Threshold: zero mapping/unrecoverable palm failures and <=10% latency/success degradation. Timeframe: within 48 hours of update.

## Hypothesis vote

- Conditional GO only for a disposable, immutable, replayable Option 1 pilot.
- NO-GO for using it as promotion evidence until state loss and provenance are bounded.
- Confidence: **0.90**
