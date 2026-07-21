# Verified evidence snapshot — 2026-07-18

## Upstream PenEcho

- The live upstream repository is `erickong/penecho`, currently on the `main` branch and licensed AGPL-3.0. Source: https://github.com/erickong/penecho
- PenEcho describes itself as a browser canvas for handwriting, equations, diagrams, and spatial context. Source: https://github.com/erickong/penecho#readme
- The canvas is a sparse 20,000 x 20,000 logical surface, and the browser sends the relevant crop plus geometry to the server. Source: https://github.com/erickong/penecho#how-it-works
- The current README documents browser-local lightweight snapshots; new-canvas behavior can overwrite, save a copy, or continue, and unconfirmed drafts are excluded. Source: https://github.com/erickong/penecho#think-on-the-canvas
- Confirmed ink can be exported as a cropped high-resolution PNG. The documented surface does not claim repository integration or cross-device server-side canvas synchronization. Source: https://github.com/erickong/penecho#think-on-the-canvas
- Execution modes are OpenAI-compatible or Anthropic API, local Codex CLI, and local Claude CLI. Source: https://github.com/erickong/penecho#how-it-works
- CLI modes launch local processes and are restricted by upstream guidance to localhost or a trusted directly connected LAN. Source: https://github.com/erickong/penecho#safe-deployment
- API mode may be remotely exposed only behind HTTPS, authentication, rate limiting, and request-size controls; provider credentials stay server-side. Source: https://github.com/erickong/penecho#safe-deployment
- The default listener is `0.0.0.0:3888`, so an unreviewed cluster deployment would create a broad listener by default. Source: https://github.com/erickong/penecho#safe-deployment
- Request tracing is off by default; if enabled, traces include canvas images, redacted request bodies, raw/parsed responses, fallback details, and status. Source: https://github.com/erickong/penecho#safe-deployment
- The current README recommends provider-specific models based on hands-on canvas testing, but says actual latency varies with provider, canvas complexity, image size, and reasoning. Source: https://github.com/erickong/penecho#recommended-model-configurations
- Upstream says a typical low-effort request is roughly 10,000 input and 1,000 output tokens, while high/max reasoning can consume much more; these are estimates, not limits. Source: https://github.com/erickong/penecho#token-use-and-cost
- AGPL permits commercial use, but a modified network-served version must offer corresponding source to its users; a separate commercial license is available. Source: https://github.com/erickong/penecho#license-and-commercial-use

## ZMS Labs control-plane evidence

- `ZMS-Labs/zms-k3s-gitops/apps/base/litellm/kustomization.yaml` currently includes only `sealed-secrets/litellm-master-key.yaml`. Source: https://github.com/ZMS-Labs/zms-k3s-gitops/blob/main/apps/base/litellm/kustomization.yaml
- `ZMS-Labs/fleet-orchestrator/deploy/k8s/base/litellm/deployment.yaml` defines a two-replica LiteLLM deployment in the `fleet-orchestrator` namespace, using `ghcr.io/berriai/litellm:main-latest`. Source: https://github.com/ZMS-Labs/fleet-orchestrator/blob/main/deploy/k8s/base/litellm/deployment.yaml
- Fleet Orchestrator's LiteLLM configuration explicitly states an honesty invariant: a model name must truthfully name the served model. Source: https://github.com/ZMS-Labs/fleet-orchestrator/blob/main/deploy/k8s/base/litellm/config.yaml
- Its current local routes are `local/llama3.1-8b`, `local-ollama`, and `local/gpt-oss-120b`; none is documented there as a vision route. Source: https://github.com/ZMS-Labs/fleet-orchestrator/blob/main/deploy/k8s/base/litellm/config.yaml
- Its paid routes are explicit OpenAI, Anthropic, Gemini, DeepSeek, and Moonshot entries; silent premium-name-to-local fallbacks were removed. Source: https://github.com/ZMS-Labs/fleet-orchestrator/blob/main/deploy/k8s/base/litellm/config.yaml
- The split between the central GitOps secret-only base and Fleet Orchestrator's deployable LiteLLM manifests creates an unresolved ownership/source-of-truth question; that conclusion is an inference from the two verified files, not proof of live-cluster ownership.

## Devices and local inference

- Supernote's official InkFlow material says Manta and Nomad can act as pressure-sensitive graphics tablets for Windows and macOS, including PDF annotation in browsers. Source: https://supernote.com/blogs/supernote-blog/sticker-for-personalizing-journals-inkflow-turns-your-supernote-into-a-graphics-tablet
- This makes Manta-to-desktop-browser input technically plausible, but it does not prove that PenEcho's canvas interaction, coordinate mapping, palm rejection, or latency are acceptable; those remain direct-test questions.
- Ollama documents an OpenAI-compatible API surface. Source: https://docs.ollama.com/api/openai-compatibility
- Ollama's official Qwen3.5 library lists multimodal/vision variants including 9B, 27B, 35B, and 122B; the 27B Q4_K_M artifact is listed at 17 GB. Source: https://ollama.com/library/qwen3.5:27b
- Model availability and nominal vision capability do not establish PenEcho command accuracy, structured-draft compliance, or acceptable latency; those require the actual PenEcho workload.

## Scholarly evidence — capability-limited

- Lau's 2022 systematic review/meta-analysis identified 33 reports, 42 independent samples, and 88 effect sizes; it reported a small overall recall benefit for handwritten over typed lecture notes, `g = 0.144`, with note review potentially reducing the advantage. Consensus fetched record: https://consensus.app/papers/the-effect-of-typewriting-vs-handwriting-lecture-notes-on-lau/fe4f873ce58a5481981e46bd5aa90378/
- Bonneton-Botte et al. (2020) reported that a stylus-oriented tablet notebook's handwriting-learning benefit depended on children's initial skill level, cautioning against universal stylus-benefit claims. Consensus fetched record: https://consensus.app/papers/can-tablet-apps-support-the-learning-of-handwriting-an-bonneton-bott-fleury/99f34eaef04558b2a0f1cbf92b175880/
- Yang and Lee (2020) reported that VR sketching extended solution space and supported idea transformation in a pilot comparison with traditional sketching; the setting is not PenEcho and cannot establish product efficacy. Consensus fetched record: https://consensus.app/papers/cognitive-impact-of-virtual-reality-sketching-on-yang-lee/65d45ae9bd1f55a289f117ec3205b35b/
- Frich et al. (2019) reviewed 143 HCI creativity-support-tool papers and found the field fragmented, with many one-off prototypes and difficult cross-study comparison. Consensus fetched record: https://consensus.app/papers/mapping-the-landscape-of-creativity-support-tools-in-hci-frich-vermeulen/8b038bcaa3c0540c9f0dc19c855dfa43/
- Shi et al. (2020) surveyed edge AI and identified privacy/channel/traffic/energy motivations alongside communication overheads; it supports a trade-off, not an automatic local-first victory. Consensus fetched record: https://consensus.app/papers/communicationefficient-edge-ai-algorithms-and-systems-shi-yang/db6a083603ca5cef9003faee1f2ebd6d/
- Scite full-text and citation-reception validation was attempted but quota-blocked until 2026-07-24 UTC. Scholarly claims therefore remain discovery/fetched-record evidence, not Scite-validated full-text evidence.

## Decision invariants

- No fork is justified merely by deployment packaging; a wrapper can pin an unmodified upstream revision without creating a divergent application codebase.
- No local route may be labeled as a model it does not actually serve; this preserves ZMS's existing honesty invariant.
- No cloud fallback may occur silently from a route presented as local/private.
- Canvas content is personal working material and should not be placed in request traces, logs, or cloud routes without explicit operator-visible policy.
- A pilot must be reversible: deleting the test deployment/configuration should leave existing ZMS control planes and upstream source untouched.
