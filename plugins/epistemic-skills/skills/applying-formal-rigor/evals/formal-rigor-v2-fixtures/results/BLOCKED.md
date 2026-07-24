# Live-arm capability block

Status: `BLOCKED_CAPABILITY` for behavioral execution only.

The fixture corpus, prompt arms, schemas, deterministic structural scorer, and semantic
adjudication protocol are runnable. This implementation context has no invocation primitive
that can create isolated, pinned model calls while withholding scorer truth, ground truth,
other-arm output, and thresholds from each run agent.

Consequently:

- neutral, current-v1, v2-candidate, and all parody arms remain `NOT_RUN`;
- no hand-authored output is credited as behavioral evidence;
- the required neutral/current-v1 RED baseline has not been established;
- production `applying-formal-rigor` files remain unchanged under the RED-before-production-edit
  gate.

Smallest unblock: provide an isolated model/agent invocation primitive that accepts a frozen
prompt plus the run-agent-visible fixture packet, returns raw output, records exact
model/provider/harness/settings, and prevents access to this repository's scorer-only files.
