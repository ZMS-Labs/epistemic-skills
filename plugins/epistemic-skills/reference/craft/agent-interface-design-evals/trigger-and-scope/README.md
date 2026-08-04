# agent-interface-design trigger-and-scope fixtures

This battery tests the trigger discipline and the scope contract: the skill
engages when an interface another agent will consume is authored or modified
(a tool or function-call schema, an MCP server surface, a structured-output
contract, a subagent dispatch contract, an agent-caller CLI, or a review that
adds one) and stays silent on human-facing interfaces, throwaway single-caller
scripts, prose handoffs (routed to write-goal/outsource), and inbound
instruction audits (routed to context-audit). Two hard negatives — a
human-caller CLI and a prose subagent brief — discriminate trigger shape from
trigger substance. Two state fixtures exercise the cold-consumer gate (a gate
failure demands a structural fix or a *recorded* compatibility concession,
with the transcript kept) and the example-lint (every usage example is
justified by a named weaker-consumer audience or converted into a structural
fix and deleted). Over-firing and under-firing are defects, not extra rigor.

This is a structural, trigger-level battery: it scores structured response
sets against a deterministic scorer. It is NOT behavioral proof that a live
agent triggers correctly or designs good interfaces.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the 2026-08-04 open-questions
and context-audit epochs): `action` names the **discipline mode that
fired** — `engage` (the interface-design method runs), `no-fire` (silent:
no `schema_edits`, `consumer_test`, or `visible_process` fields at all;
an excluded crossing states `routed_to` with the owning skill),
`consumer-gate` (adjudicating a failed cold-consumer test: `remedy` is
`structural-fix` — naming `fixed_parameter` — or a `recorded`
`compatibility-concession`; `transcript_kept` states whether the test
transcript survives), or `example-lint` (`dispositions` maps every example
id to `{"outcome": "justified", "audience": …}` or
`{"outcome": "deleted", "structural_fix": …}`). For `engage`,
`encodes_in_structure` and `consumer_test` report whether the method's
structure-first rule and cold-consumer test actually ran; any
`examples_added` must carry matching `example_justifications`.

First live behavioral epoch: 2026-08-04, PASS 14/14 — see
`results/2026-08-04/RESULTS.md` (methodology and its disclosed batching
limitation included; register: issue #77).
