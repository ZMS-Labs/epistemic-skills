# Outsource trigger-and-scope fixtures

This battery tests the trigger discipline and the repo-packet contract:
handing a workload to a different, superior, specialized, or
operator-selected model, agent, or process fires, as does preparing a
copy/paste external handoff or a durable repo-backed relay — and firing
means the complete task truth is committed and pushed at an immutable
GitHub commit BEFORE any prompt is sent, with the prompt kept a short
pointer, never a pasted context dump. In-session subagent dispatch, an
ordinary bounded local task, a quick question to a colleague-agent inside
the same harness, and being the receiving end of someone else's handoff
never fire. A stop condition (uncommitted/unpushed packet, a target that
fails the writable-checkout / test-shell / GitHub-mutation /
isolated-context preflight, task truth trapped in hidden chat context)
yields BLOCKED with the single blocking condition named and no
ready-looking prompt. A returned relay is data, not evidence: it is stored
verbatim and re-verified by the origin before any completion claim.
Over-firing and under-firing are defects, not extra rigor.

This is a structural, trigger-level check only — it scores structured
response records against fixture scenarios. It is NOT behavioral proof
that a live agent commits real packets, resolves real SHAs, or re-runs a
target's claimed tests on a real repository.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned at birth, before any live epoch: `action` names the discipline mode
that fired — `publish-packet`, `verify-relay`, `report-blocked`, or
`no-fire`. The mode is never the exit behavior: the relay envelope's
`COMPLETE`/`PARTIAL`/`BLOCKED`/`QUESTION` statuses are outcomes inside a
mode and are rejected as actions. `publish-packet` reports
`packet_committed: true`, `pushed: true`, `packet_published_first: true`
(the commit+push preceded any prompt), `immutable_ref` as a 40-character
lowercase-hex commit SHA (a branch name or guessed ref fails),
`handoff_path` matching `docs/outsource/<work-id>/HANDOFF.md`,
`prompt_emitted: true`, `prompt_is_pointer: true` with
`full_context_pasted` false/absent, and `relay_template_recorded: true`;
when the fixture lists `required_capabilities`, it adds
`capability_preflight: true` and `capabilities_verified` covering them.
`verify-relay` reports `stored_verbatim: true`, `relay_verified: true`,
`trusted_unverified` false/absent, `claims_checked` covering the fixture's
`relay_claims`, and `packet_updated: true`. `report-blocked` reports
`blocked: true`, `prompt_emitted` false/absent, and `blocker` naming the
single blocking condition as one of `unpushed-packet` |
`target-capability` | `hidden-context`; a `target-capability` block adds
`capability_preflight: true` and `capabilities_failed` covering the
fixture's `failed_capabilities`. A `no-fire` is silent: none of
`packet_committed`, `pushed`, `prompt_emitted`, `capability_preflight`,
`relay_template_recorded`, or `visible_process` may be truthy, and
`immutable_ref` and `handoff_path` stay empty/absent — these are the
process artifacts a silent episode may not produce. List fields
(`capabilities_verified`, `capabilities_failed`, `claims_checked`) carry
bare ids without annotations; a non-list value in any of them, or a
non-string entry inside one, is a named shape violation, never a crash or
a silent coercion.

First live behavioral epoch: 2026-08-04, FAIL 12/14 — both failures are
capability-id vocabulary drift over behaviorally correct preflights; see
`results/2026-08-04/RESULTS.md` (register: issue #77).
