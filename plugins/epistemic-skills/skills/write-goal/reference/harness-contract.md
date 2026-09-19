# Native harness contract

This is an adaptation procedure, not a goal runner or a product capability table.
Apply it only to explicitly requested goal authoring or authorized native activation.
A draft-only instruction prohibits activation even when a suitable tool is available.

## Discover the selected surface

Identify product, invocation path (tool, API, command, UI, or plugin), installed
version where exposed, and the exact schema/help consulted. Inspect current goal or
loop state before creating anything. Reuse or reconcile an existing authorized
objective; never silently replace it or start a duplicate. If state cannot be read,
report that uncertainty and do not retry a potentially successful submission blindly.

Use current exposed tool schema/capability responses or installed implementation/help
first; consult current official documentation only for unresolved facts. Record a
compact surface profile in the existing task record when needed for continuation:
source coordinate/version/date, each pertinent fact, and whether it is explicit,
documented, safely observed, or unknown. Schema silence does not prove unlimited
payloads. Revalidate on interface/version changes, contradictory results, or material
coverage gaps; a cached profile is only valid within its observed scope. No full
platform survey is required when the relevant scoped facts remain current.

Discover separately:

- Operations and required/optional fields, active/concurrent-objective restrictions.
- Goal storage, repeated execution, scheduling, and persistence across resume.
- Objective and separate completion fields; supported references/attachments and the
  executor's access now and on the claimed resume path.
- Field and whole-request limits, counting units, prefixes, escaping, serialized
  wrappers, and required transport representation.
- Native defaults and optional token/time/iteration budgets. Omit unrequested optional
  budgets rather than populating a default yourself. If a mandatory control forces a
  material tradeoff, surface it; do not invent a user budget.
- Pause, cancel, resume, block, and completion semantics; thresholds and who can invoke
  each transition. Preserve the user's interrupt authority. Do not map pause to
  complete, manufacture a blocked status, or assume a status setter resumes execution.
- Returned identity/status, readback, normalized storage, and acknowledgment limits.

## Encode without changing the goal

Preserve outcome, primary proof and integrity/provenance guards, scope, protected
state, authority/cost boundaries, inspect/act/verify loop, and stop conditions. Remove
repetition and formatting overhead first. Map proof into a separate completion field
only if supported; otherwise keep it in the objective. Unknown unsupported options
must not be invented. Validate required fields and applicable limits before submission.

Count the actual submitted representation using the surface's unit. Characters,
Unicode code points, UTF-16 code units, UTF-8 bytes, and tokens are not interchangeable.
This synthetic control demonstrates the distinction without asserting a host limit:

```python
payload = "A" + chr(0x1F680)
assert len(payload) == 2
assert len(payload.encode("utf-16-le")) // 2 == 3
assert len(payload.encode("utf-8")) == 5
```

If wrappers count, serialize with the actual escaping/separators and count that
serialization, including the command prefix if applicable. A tokenizer is required
for a token limit; do not substitute a character estimate. Unknown limits remain
unknown until a safe observation or authoritative source resolves them. Tests use
profile-specific synthetic limits, never purported product quotas.

A shorter objective may reference a fuller versioned contract only after verifying
that the actual executor can retrieve and consume it now and on the relevant resume
path. Keep essential constraints inline. A file on the author's machine or a URL
accessible only to the author is insufficient. If representation cannot preserve the
contract, retain the usable draft and name the precise limitation; resolve a material
change only when necessary. Never truncate essential terms to obtain acceptance.

## Submit and inspect

1. Confirm explicit start authority still applies and no intervening pause/cancel or
   changed instruction supersedes it. Draft approval without start intent is not a
   license to ignore a draft-only restriction.
2. Invoke the discovered native mechanism with the authorized representation. Let the
   native executor own repetition and lifecycle; do not build a second loop.
3. On definite validation rejection, correct syntax/representation within the existing
   scope and retry boundedly. A changed substantive outcome needs new authority.
4. On timeout or ambiguous submission, inspect active state before retrying. Match the
   returned identity and contract when possible; if inspection cannot resolve whether
   creation succeeded, hold the duplicate-prone action and report the uncertainty.
5. Read back identity, native status and stored fields when supported. Compare all
   essential terms and completion fields, accounting only for documented harmless
   normalization. Detect truncation or missing terms; do not describe a damaged stored
   contract as successfully activated. Use a supported authorized correction or hold
   the dependent claim; do not blindly create another goal or invent pause semantics.
6. With acknowledgment only, report acceptance acknowledged and stored-content/state
   verification unavailable. Do not upgrade acknowledgment into execution, persistence,
   or outcome evidence. Preserve native identity and state reference if exposed.

Return one honest state: drafted; native activation observed (with its evidence
level); ambiguous; rejected; or unavailable. Unsupported persistence must be visible
when the authorized contract requires it. A loop-only host may serve a loop-only
request, but cannot be presented as cross-session goal storage. Activation/termination
and substantive completion remain distinct; the agreed proof decides the latter.

## Local verification scope

`../evals/trigger-and-scope/adapter-fixtures.json` and the existing test runner exercise
synthetic profiles and response traces. They check counting, call ordering, stored
content and reporting boundaries; they do not call a native host, establish real
quotas, or measure behavioral improvement.
