# Consensus — discovery engine (first contact)

> **Not permanent configuration — re-check live.** This records the *epistemic
> role* of the discovery layer and the access modes agents may find. Live
> schema / LOCAL.md bindings win. Capabilities and auth state drift.

## Epistemic role (why Consensus is in the triad)

Consensus answers *"what does the literature say about X?"* — question-led
discovery with study-design filters and optional research-agent synthesis. The unit
of evidence is the **paper**, and retrieved content needs an explicit local
evidence record. Threads can persist in the provider account; that does not prove a local artifact or library deposit.

For current tool selection and Threads constraints, read
[`consensus-threads.md`](consensus-threads.md). The older ZCode profile is
historical host evidence, not the current cross-host inventory.

## Access modes (negotiate every run)

Prefer, in order:

1. **Consensus MCP** (if the harness registers one) — inspect the live tool
   schema every run; record what variants exist (search-only? fetch?
   filters?) and any server-shipped usage instructions (those bind on this
   connector as harness configuration, not tool output).
2. **Operator-mediated web UI** — the agent emits queries, the operator runs
   them and returns results. Label the run `operator-mediated`; record the
   loss of programmatic filters/counts as a coverage limit.

Never fabricate a capability (fetch, filters, full text) the live schema or
LOCAL.md does not show.

## Degradation labels (copy verbatim into the matrix / run record)

| Condition | Stamp |
|---|---|
| No MCP / connector available | `consensus: UNAVAILABLE` — run Scite-led discovery, labeled |
| Operator-mediated only | `consensus: operator-mediated` |
| Study-design filters absent from live schema | coverage limit in the synthesis — say so |

## First-contact protocol

On first contact, inspect the needed live schemas and record their date,
parameters and connector instructions. Only run a capacity-checked probe when
an actual research task requires and authorizes it. Record any observed
response shape, filters, auth and rate-limit behavior separately from schema
observations. Update `consensus-profile.md` through the canonical repository
workflow, preserving dated historical observations and the "re-check live"
header. Publication and deployment require separate authority.
