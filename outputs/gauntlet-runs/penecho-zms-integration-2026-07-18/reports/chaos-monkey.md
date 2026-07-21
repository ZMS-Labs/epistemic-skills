# finding-set@1 — chaos-monkey@2

## CM-01 — P1: CLI exposure can cross the intended trust boundary

**Failure combination:** The default `0.0.0.0:3888` listener remains active; LAN access is opened; CLI mode is enabled. A reachable LAN client can submit valid requests that launch local processes. [I <- V sources.md:11; V sources.md:13]

**Recommended fix:** Bind CLI mode to loopback or an explicit test-client allowlist, isolate it from API mode, and prove firewall enforcement first.

**Falsifier:** Method: enumerate listeners/firewall rules, probe from every pilot VLAN and three unauthorized clients while monitoring process creation. Threshold: zero accepted requests and zero process launches outside the named client. Timeframe: before trial and daily for seven days.

## CM-02 — P1: Option 2 inherits gateway split-brain

**Failure combination:** LiteLLM has two replicas using mutable `main-latest`; ownership is unresolved between a secret-only GitOps base and Fleet Orchestrator. Tag change plus partial rollout/config drift can make one advertised route behave differently across replicas while health stays green. [I <- V sources.md:21; V sources.md:22; V sources.md:23; V sources.md:26]

**Recommended fix:** Block Option 2 until ownership is singular, images are digest-pinned, every replica reports identical config/model-identity hashes, and rollout checks reject mixed identities.

**Falsifier:** Method: staged rollout, direct replica requests, then load-balanced route-identity assertions. Threshold: identical digests/config hashes/served identities across 10,000 requests and zero mislabeled execution. Timeframe: before Option 2.

## CM-03 — P2: Local state loss can masquerade as poor device or model fit

**Failure combination:** Browser-local snapshots, confirmed-ink-only PNG export, and Manta mediated through desktop browser mean a profile reset or interruption can erase continuity independently of input/model quality. [I <- V sources.md:8; V sources.md:9; V sources.md:30; V sources.md:31]

**Recommended fix:** Score interaction, inference, and continuity separately; require exports and inject browser-state loss.

**Falsifier:** Method: 20 scripted handoffs with storage deletion/restart. Threshold: >=95% recovery within two minutes and zero device/model failures attributable solely to local state. Timeframe: week one.

## CM-04 — P2: Troubleshooting an inference outage can create the privacy incident

**Failure combination:** A route fails; tracing is enabled; repeated diagnostic requests retain canvas images and fallback details. [I <- V sources.md:14; V sources.md:50]

**Recommended fix:** Use image-free diagnostics or an ephemeral encrypted trace sink with explicit retention; test under induced failure before real material.

**Falsifier:** Method: induce primary-route failure, issue 100 synthetic requests, inspect all artifacts. Threshold: zero recoverable images/crops and deletion within <=24 hours. Timeframe: before personal material.

## Hypothesis vote

- Conditional GO for Option 1 only; NO-GO for Options 2-4.
- Killed: central hosting solves continuity. [V sources.md:8]
- Confidence: **0.88**
