# finding-set@1 — network-effects-strategist@2

## NE-01 — P1: Central hosting is correctly deferred because it creates no verified continuity loop

**Mechanism:** Browser-local snapshots mean adding another device does not make prior canvas state available there. A common URL could reduce setup friction, but that is operational economy, not a network effect. [I <- V sources.md:8; V sources.md:9]

**Recommended fix:** Make shared-URL convenience and shared-canvas continuity separate metrics. Promote only the former through a wrapper; treat the latter as a distinct product capability.

**Falsifier:** Deferral is wrong if local startup or route configuration causes abandonment of at least 20% of otherwise viable sessions across two device classes. Method: session-level setup and abandonment log. Threshold: >=6 of 30 sessions. Timeframe: two-week pilot.

## NE-02 — P1: A pooled adoption score would hide device-class failure

**Mechanism:** Manta's demonstrated value path is as a graphics tablet for a desktop browser, while PenEcho coordinate mapping, palm rejection, and latency remain unverified. [V sources.md:30] [V sources.md:31] Browser-local snapshots also prevent assuming iPad, iPhone, and Manta are interchangeable continuity nodes. [I <- V sources.md:8]

**Recommended fix:** Score task success, latency, setup burden, and voluntary reuse separately for iPad, Manta/InkFlow, and iPhone. Promote only roles that clear their own threshold.

**Falsifier:** Segmentation is unnecessary if all three devices show task-success rates within five percentage points and the same dominant workflow mix. Method: stratified analysis. Threshold: >=10 representative sessions per device and <=5-point success spread. Timeframe: two weeks.

## NE-03 — P2: The wrapper tipping point should be operational, not more devices

**Mechanism:** A wrapper can standardize access but cannot synchronize browser-local state. [I <- V sources.md:8] Centralization also inherits an unresolved LiteLLM ownership split. [I <- V sources.md:21; V sources.md:22]

**Recommended fix:** Exercise Option 2 only when repeated use is proven and a matched hosted week materially reduces setup/configuration friction. Bind it to exactly one verified model-route owner.

**Falsifier:** Immediate wrapping is superior if a pinned hosted URL yields at least 25% more completed sessions and at least 50% less setup time than the workstation URL. Method: crossover test. Threshold: both across >=20 sessions. Timeframe: two weeks.

## NE-04 — P2: Synchronization is the only plausible compounding device effect, and it is absent

**Mechanism:** Durable synchronized canvases could create device complementarity. Current snapshots remain local and export only as PNG, so that loop does not exist. [I <- V sources.md:8; V sources.md:9]

**Recommended fix:** Keep synchronization outside the pilot and fork decision. Modify only when valuable workflows repeatedly fail specifically because state cannot follow the operator and a disposable adapter cannot solve it.

**Falsifier:** Waiting for three blockers is too conservative if one configuration-insoluble synchronization blocker prevents at least half of all high-value cross-device tasks. Method: reproduce against pinned upstream and a disposable adapter. Threshold: >=50% failure across >=10 tasks. Timeframe: first two weeks.

## NE-05 — P3: Central inference can create congestion before adoption value

**Mechanism:** More device sessions share inference capacity; latency varies by provider, canvas complexity, image size, and reasoning, while current local routes do not document vision. [I <- V sources.md:15; V sources.md:24]

**Recommended fix:** Before cluster promotion, run a bounded three-session concurrency probe against the single-session baseline.

**Falsifier:** Congestion is immaterial if concurrent p95 latency stays within 15% of baseline and errors remain below 1%. Method: identical workload at one and three concurrent sessions. Threshold: both across >=100 requests. Timeframe: one test day.

## Hypothesis vote

- Supported: value is task-specific and a local pilot dominates infrastructure.
- Killed: central hosting creates continuity or a genuine network effect. [V sources.md:8]
- Verdict: **CONDITIONAL**
- Confidence: **0.91**
