> **Applies to:** epistemic-skills v7.0.0.

# Install once, verify what your host actually loads

Use the [v7.0.0 installation instructions](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/README.md#installation-and-compatibility) for the immutable release and the [published release assets](https://github.com/ZMS-Labs/epistemic-skills/releases/tag/v7.0.0) for generated bundles. The [publication receipt](https://github.com/ZMS-Labs/epistemic-skills/releases/download/v7.0.0/publication-receipt.json) binds the tag, source, checks, and artifacts.

### What to verify

1. Choose one installation mechanism for the host. Preserve customized existing instructions or handlers.
2. Record the selected release and installed location. Use the host's documented trust and reload process.
3. Observe discovery or loading where the host exposes it. A correct manifest is insufficient to establish either.
4. Load `epistemic` explicitly if automatic entry delivery is unavailable or unverified.
5. Try a bounded real task and inspect the method's actual contribution. Installing does not by itself establish successful application.

### v7 coverage, honestly scoped

| Surface | What the v7 evidence establishes | What remains separate |
|---|---|---|
| Codex CLI | Live discovery of all 17 canonical entries in an isolated workspace; source and serialization checks for usage delivery | Native marketplace installation, model consumption, and task benefit |
| Claude Code | Hook adapter source and synthetic routing checks | Authenticated model application and live startup delivery |
| Gemini CLI | Version and source context configuration | Model delivery and native alias/goal behavior |
| Cursor, Kimi, Antigravity | Observed versions and relevant package or existing adapter checks | New automatic usage delivery and native goal support |
| ZCode and generic Agent Skills hosts | Documented discovery or explicit-load path | Unexercised runtime support |
| ChatGPT / OpenAI bundles | Built artifacts, indices, checksums, and published source identity | Upload, installation, loading, and application in a particular host |

The [dated v7 host record](https://github.com/ZMS-Labs/epistemic-skills/blob/v7.0.0/docs/release/v7-host-coverage.md) supplies the detailed versions and test scope. Its pre-publication status is historical; final publication is recorded separately. Host versions and interfaces may change after that observation.

Native goals and loops are inspected at use time. An upgrade does not silently activate or replace a goal. See [Write Goal](Skill-Write-Goal.md) and [troubleshooting](FAQ-and-Troubleshooting.md).
