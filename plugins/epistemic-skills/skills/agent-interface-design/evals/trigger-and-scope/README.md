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

No live behavioral epoch has been run against this battery; see
`results/BLOCKED.md`.
