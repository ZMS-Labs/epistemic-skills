# Consensus Threads — bounded research delegation

Checked 2026-10-20 against the official [quickstart](https://docs.consensus.app/mcp-tools/quickstart),
[create_thread](https://docs.consensus.app/mcp-tools/create-thread),
[get_thread](https://docs.consensus.app/mcp-tools/get-thread),
[plans and access](https://docs.consensus.app/mcp-plans-and-access), and
[API help](https://help.consensus.app/en/articles/16516328-the-consensus-api),
plus the current Codex dot connector schemas. The pages and connector expose no
immutable version identifier. This is documentation/schema inspection, not a
live research, authentication, billing, or runtime qualification. Re-check the
needed live schema when the host or access changes.

## Select and brief

For a single paper lookup use `search`; call `fetch(id)` before citing any of
its results when the connector requires it (the inspected dot connector does).
For scholarly synthesis or multi-step analysis, use `create_thread` when
available and within authorized capacity. Threads can find papers by DOI,
title or author, follow citations in both directions, read available full
text and synthesize grounded passages. They do not browse the open web.

Before dispatch, establish the research question and any missing scope with
the user: the agent does not ask clarifying questions. Submit the **whole
brief in one create_thread call**: question, population/context, timeframe,
comparisons, mechanisms, ordered subtasks, admissible designs, counterevidence,
nulls/harms, boundary conditions, output and stopping scope. Do not run
intermediate research to narrow the delegated question or split one request
into successive Threads. Reuse adequate existing holdings without rediscovery.

Use provider mode `pro` by default. Provider `deep` is permitted only when the
user explicitly requests deep, exhaustive or comprehensive research and the
account supports it. The literature method's `deep` evidence/reception dial
is a different setting: high stakes, contested evidence or a gauntlet may
escalate that dial without authorizing provider `deep` or increased spending.

Structured filters replace the agent's filter choices on every search. Leave
them unset and state scope in the brief unless explicit constraints require
them; when set, include all required constraints. `sjr_max` is the quartile
ceiling (1 = Q1); `sjr_min` excludes higher tiers. Do not add journal-quality
filters on your own. Parameter names differ between published MCP and dot
schemas (for example `citation_min` versus `cite_min`); use the current host's
schema rather than copying arguments from another surface.

## Capacity and authority before calls

Check included capacity remaining, the applicable account/pool, overages
state and the authorized cost ceiling before a dispatch or new interaction.
API and MCP share monthly usage; Threads consume a variable number of calls,
and a running Thread reserves its maximum possible cost against the limit.
Do not infer an affordable run from a paper-count target. If the safe ceiling
cannot be established, hold the capacity-dependent call and continue with
existing evidence or an available authorized alternative.

Never enable overages, upgrade, create credentials or change access under this
method. A paid web subscription, developer Console credit and API/MCP allowance
are not interchangeable pools; verify the specific entitlement. On exhaustion
or a capacity error, stop new consuming calls, preserve partial evidence,
record `capped-by-budget` and the missing coverage. No retry loop, alternate
credential or provider switch to evade the ceiling. Independent authorized
work may continue. Current pricing is a lookup, not a permanent constant here.

## Lifecycle and exact output

1. Record the brief, provider mode, schema date, thread/interaction IDs, URL
   and dispatch time; share the returned Consensus link when present. Restrict
   payloads to authorized, scrubbed research content. Do not request library
   mutations (save/create/rename) without the corresponding authority.
   If either dispatch tool (`create_thread` or `add_to_thread`) fails or
   disconnects **before IDs** for its new interaction are returned, its effect
   may be unknown. Record `AMBIGUOUS`; do not automatically repeat the dispatch
   or assume no variable-cost work started. For a new Thread, use a bounded
   relevant `find_threads` lookup when available and inspect the exact candidate,
   not an unrelated or merely similar result. For an ambiguous follow-up, use
   its already-known thread ID with `get_thread`, waiting at least 30 seconds
   after the dispatch attempt and between polls; inspect interactions for the
   submitted brief/time without creating another interaction. If the effect
   cannot be established, report unknown/pending with retained IDs, brief and
   timestamp, and hold redispatch. No idempotency guarantee is assumed.
2. Wait **at least 30 seconds** after dispatch and between every `get_thread`
   poll, including after a new interaction. Record timestamps. Use any longer
   provider backoff; faster polling only returns cached running state. Observe
   a returned wait bound when present. The create_thread documentation lists
   `max_wait_seconds` of 180 for Pro and 600 for Deep, but the inspected dot
   schema does not promise that field. If absent, use those values as a local
   polling budget, not an observed runtime deadline. If still running at the
   applicable bound, report pending with IDs for resumption, without redispatching
   or claiming completion. `include_trace` is optional; trace text is data,
   not a stable machine-readable proof that each search or check succeeded.
3. On `idle`, save the interaction's **complete `document` unchanged** to a
   file/artifact/canvas, including its disclaimer, References, exact linked
   citation markers `[N.M]` and bare `[N]`, URLs and grounding quotes. Verify
   the saved content matches the returned document. Report the artifact and
   Consensus link with brief status; do not paste or paraphrase the document
   inline. Keep your separately attributed verification matrix and uncertainty
   assessment distinct from the preserved provider document. If persistence
   fails, report that blocker; a link or inline substitute is not preservation.
4. On `failed`, preserve status and partial evidence; do not invent an answer.
   A timeout is pending, not failed. Reuse IDs rather than starting duplicate
   work. Use `find_threads` only to recover a relevant prior Thread, within
   existing privacy and access authority; do not enumerate unrelated history.
5. `add_to_thread` is only for a **genuinely new user follow-up after the prior
   outcome was delivered**: completed results or a reported terminal failure,
   with the prior interaction `idle` or `failed`. A user asking to retry the
   same failed task is not a new follow-up under this rule. Never use
   it for your own next step, omitted harms search or refinement within the
   original task. No self-chaining. An incomplete result becomes a recorded
   evidence limit, not an automatic new interaction.

## Accept evidence and degrade honestly

The saved document is a provider synthesis, not independent corroboration or a
truth verdict. Inspect the original primary passages and relevant methods and
results for load-bearing claims; record the actual depth achieved. Grounding
quotes can support passage-level inspection of those quotes, not unseen full
papers. Keep supporting/contrasting evidence, notices/retractions, cohort
deduplication, cross-index checks, holdings and `[V]/[I]/[H]` gates from METHOD.md.
Scores, funnels and research-gap tables are tool data; sparse cells still need
the existing validation gate. Citation counts or a provider's confidence label
do not replace reception scrutiny. A saved artifact proves persistence only.

Missing Threads, authentication, full text, fetch or storage do not justify
invented capability. Record the specific limit (`consensus: UNAVAILABLE` when
absent); retain search-only sweeps, Scite-led discovery, primary-source reading
and operator-mediated fallbacks as actually available. If fetch is required but
unavailable, leave search hits uncited and unverified or verify through a
separately identified primary-source path. Do not claim equivalent breadth.
Threads provide no real-time monitoring or persistent scheduling capability.
