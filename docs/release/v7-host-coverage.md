# v7 candidate host coverage

Status: retained pre-publication candidate evidence for the published v7.0.0 release.

Evidence date: 2026-09-18. This is candidate verification, not a published v7
release or a claim of automatic delivery across all supported hosts. The canonical usage body
is `plugins/epistemic-skills/skills/epistemic/SKILL.md`.

## Observed surfaces and support boundaries

| Product / surface | Observed version | Installation path class | Usage entry / context lifecycle | Native alias / goal evidence | Evidence tier |
|---|---|---|---|---|---|
| Codex CLI app-server | 0.149.0 | Isolated temporary home; workspace `.agents/skills` copy | Live `skills/list` discovers candidate descriptions. SessionStart adapter implements documented startup/resume/clear/compact context output; model consumption unexercised | Historical alias documentation-only. `goals` feature flag is stable/enabled; native representation/readback unexercised | **Live discovery**, source/serialization checks for injection |
| Codex desktop task | Version not collected | Existing plugin cache and user skill installations | Current task advertised older installed descriptions; canonical candidate read explicitly from source. No candidate startup claim | Current task exposes create/get/update_goal schemas; deliberately not activated in production task | Observed tool availability; no goal workflow proof |
| Claude Code CLI / plugin | 2.1.277 | Native plugin hook path using `CLAUDE_PLUGIN_ROOT` | SessionStart startup/resume/clear/compact/fork adapter follows current official contract; no authenticated model run | Alias documentation-only; goal support not inspected | Source and synthetic routing only |
| Cursor IDE | 3.19.7 | Tagged local plugin or team marketplace | Existing custody hooks retained. No new early usage-injection interface asserted. Explicit load after reload/context loss | Alias documentation-only; goal support unverified | Version observed; usage delivery unexercised |
| Cursor CLI | Not available as `agent` on PATH | Generated machine-local project/user hook config | Existing custody renderer unchanged; it must not acquire unverified usage commands. Explicit canonical load in fresh/resumed context | Alias documentation-only; goal support unverified | Existing custody tests only |
| Gemini CLI extension | 0.42.0 | Extension root context (`GEMINI.md`) and linked canonical tree | Root guidance supplies explicit load fallback after startup/resume/context loss; context file presence is not body delivery proof | Alias documentation-only; goal support unverified | Version and source configuration observed; model delivery unexercised |
| Antigravity native / Gemini bridge | 1.1.7 | Native plugin, extension link, or import: select one | Existing manifest only; use explicit canonical load. No Gemini hook behavior inferred for this host | Alias documentation-only; goal support unverified | Version observed; usage delivery unexercised |
| Kimi Code plugin | 0.28.1 | Repository plugin | Existing skillInstructions/tool mappings retained; reload/new session and explicitly load canonical body | Alias documentation-only; goal support unverified | Version observed; usage delivery unexercised |
| ZCode skill projection | Unavailable on PATH | User skill-directory projection | Existing install documentation only; new session and explicit canonical load | Alias documentation-only; goal support unverified | Unavailable in this verification |
| ChatGPT / OpenAI generated bundle | No host version observed | Generated upload snapshot | Bundle source does not establish runtime entry injection; load its canonical usage entry explicitly | Alias documentation-only; goal/loop availability host-dependent | Source packaging only |
| Generic Agent Skills hosts | Unspecified | Canonical skills-directory install | Discover/invoke `epistemic`, or read its SKILL.md; re-read if context lost | No native alias or native goal guarantee | Compatibility fallback, not exercised support |

## Live discovery receipt

The installed Codex app-server was launched with an empty temporary `CODEX_HOME`
and separate temporary workspace containing a copy of the candidate canonical
skill tree under `.agents/skills`. No authentication material was read or copied.
Its generated local protocol schema established the `initialize` and
`skills/list` calls. The response was filtered to entries whose source paths were
inside that isolated workspace; only actual `name` and `description` fields were
retained in [the sanitized capture](v7-host-evidence/codex-0.149.0-skills.json).
The capture contains 23 entries: all 17 canonical top-level skills plus six
nested method entries the host also discovered. It is not a package-generated
inventory and is not an assertion that only 17 skills appear in the host.

```text
python .github/scripts/check_loaded_descriptions.py --capture docs/release/v7-host-evidence/codex-0.149.0-skills.json
loaded-description ok: 17 packaged skills present in capture
```

This proves discovery through this CLI's workspace skill mechanism. It does not
prove native marketplace installation, full model context, method application,
remaining context headroom with other collections, or a comparative benefit.
No ordinary-prompt method application, startup model-consumption, or native-goal
readback receipt was obtained in this host validation. Those claims are explicitly
withdrawn for this packet.

## Early delivery and fallback

`hooks/usage_context.py` reads one canonical body from its own installation;
it does not keep a second method implementation. The Claude plugin registers
SessionStart in `hooks/hooks.json`. Codex's `hooks/codex-hooks.json` remains an
**install snippet**: merge its SessionStart handler into one trusted host hook
configuration, substitute the selected absolute plugin root, and approve the
hook using the host's normal trust interface. Preserve existing customized
handlers. Do not install the same handler into both user and project config.
The Codex handler disables host context summarization for this bounded body.
Python must be available to the host hook shell.

The loader emits the complete UTF-8 body in JSON additionalContext, with a
SHA-256 marker. It caps the canonical body at 64 KiB and refuses empty/missing
or invalid UTF-8 bodies and conflicting Claude/Codex manifest versions with a
visible fallback message. `--expected-sha256` optionally pins an operator's
selected body fingerprint. The fingerprint covers actual decoded source bytes,
including line endings. Comparing different checkouts can therefore expose a
line-ending difference as well as a content difference.

Delivery has **no persisted deduplication ledger**. Each matching lifecycle
call emits at most one bounded body, so resume/clear/compact cannot lose needed
instructions because of a stale delivery receipt. Repeated identical injections
have the same marker and instruct the model to reuse existing guidance without
repeated acknowledgment; host-level token deduplication is not claimed. Different
copies have different markers. Select one intended installation before relying
on conflicting guidance. Duplicate registration can still duplicate context;
remove the extra registration using the normal host configuration mechanism.

Errors never return a custody block or activate a goal. They return a visible
warning and instructions to explicitly load the selected installation's
`skills/epistemic/SKILL.md`. Unsupported hosts use that same fallback. Invoke
`epistemic` through the actual host interface; `using-epistemic-skills` remains a
documentation-only mapping until a native alias is verified for that surface.

## Verification and limits

- Six meaningful loader tests cover Unicode/escaping round-trip, all supported
  lifecycle sources, duplicate fingerprint/replay semantics, changed-source
  rejection, missing/empty/oversized bodies, manifest disagreement, and visible
  malformed-input fallback without custody blocking.
- Loaded-description checker self-tests pass, and the actual live capture passes.
- Description budget: 7,153 UTF-8 bytes across 17 canonical descriptions, below
  the package-local 8,636-byte ceiling. This is not estate headroom.
- Mission-custody suite passed (all green; POSIX-only symlink checks skipped on Windows); runtime-gate suite passed with zero failures. The unchanged
  custody registrations and Cursor renderer preserve their existing semantics.
- Synthetic payload tests establish serialization/routing; they do not establish
  startup/resume model consumption. No independent host's support is inferred
  from another, and no startup banner is counted as substantive method use.

Interface references inspected on the evidence date:
[Codex hooks](https://learn.chatgpt.com/docs/hooks) and
[Claude Code hooks](https://code.claude.com/docs/en/hooks).
Local `--help`, `--version`, feature listing, and generated app-server schemas
were used before filling unresolved contract details from official references.

## Publication-stage custody diagnostic

The v7 release-branch run [35422446331](https://github.com/ZMS-Labs/epistemic-skills/actions/runs/35422446331)
on `8854dd735b414997930e768bceead18f740e4868` passed the required Ubuntu
custody contract job. Its dispatch-only macOS diagnostic reproduced issue #162:
`distinct-real-file-untouched` and `distinct-both-files-tracked-separately`
failed in the lifecycle suite on case-insensitive APFS; later macOS steps were
skipped. This is observed unsupported behavior, not a successful platform tier.
Do not rely on custody exclusion or distinct-file guarantees on case-insensitive
POSIX filesystems. The final publication receipt binds the exact release rerun.
This contract diagnostic supplies no model/host skill-application evidence.
