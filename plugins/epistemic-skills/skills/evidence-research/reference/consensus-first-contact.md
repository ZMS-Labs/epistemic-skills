# Consensus — discovery engine (first contact)

> **Not permanent configuration — re-check live.** This records the *epistemic
> role* of the discovery layer and the access modes agents may find. Live
> schema / LOCAL.md bindings win. Capabilities and auth state drift.

## Epistemic role (why Consensus is in the triad)

Consensus answers *"what does the literature say about X?"* — question-led
discovery over 200M+ papers with study-design filters. The unit of evidence is
the **paper**, and the surface is **session-bound**: unlike the library layer,
nothing Consensus returns persists unless the run deposits it.

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

On the first session where Consensus tools appear: load the full live schema,
probe with a cheap known-answer query, record response shape, filters,
server-shipped instructions, and auth/rate-limit behavior — then rewrite this
file into `consensus-profile.md` (observed profile, dated, with the same
"not permanent configuration — re-check live" header `scite-profile.md`
uses). Keep this file's protocol section at the bottom for the next drift
event, and commit + push.
