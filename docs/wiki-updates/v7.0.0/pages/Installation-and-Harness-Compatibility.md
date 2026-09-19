> **Applies to:** epistemic-skills v7.0.0.
> Source checks, loaded context, exercised workflows and comparative benefit are distinct.

# Installation and host coverage

Use the [v7.0.0 installation instructions](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/README.md#installation-and-compatibility)
from the immutable release. Before installing, verify that the
[v7.0.0 release](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.0.0)
is published and identifies the intended tag. Do not replace a customized
installation automatically.

Use one installation mechanism per host. Record the source revision, installed
path, loaded copy, reload boundary, discovery behavior and exercised workflow.
A source-level hook test is not an observed host startup. Alias support must be
verified per host. Existing native goals or loops are not restarted by upgrade.

| Surface | Evidence boundary |
|---|---|
| Claude Code and Codex hooks | Source adapters and focused checks; loaded-context and workflow claims require the current evidence packet |
| Gemini context | Explicit usage context and refresh guidance; actual startup loading requires host evidence |
| Cursor, Kimi, Antigravity | Package metadata; no inferred startup delivery or native-loop support |
| Generic Agent Skills and ZCode | Discovery/source delivery varies by host; explicit method loading is the fallback |
| OpenAI/ChatGPT bundles | Deterministic build and bundled index; upload/install execution is separate evidence |

See [current host evidence](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-evidence.md). Historical v6 harness
results remain evidence for v6 only.
