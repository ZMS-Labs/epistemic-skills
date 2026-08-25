# Consensus MCP — observed profile (first contact 2026-08-15, ZCode harness)

> **Not permanent configuration — re-check live.** Recorded on first live-tool
> session via ZCode HTTP MCP registration (`mcp__consensus__*`, server
> `https://mcp.consensus.app/mcp`, API-key Bearer header). Live tool schema wins
> over this file. Capabilities drift; auth state changes per session.

## Headline findings

1. **Single-tool surface**: `mcp__consensus__search` is the only tool.
2. **Auth = static API-key Bearer** (ZCode config `headers.Authorization`).
   OAuth also exists but tokens expire in hours (official docs) — do not pin those.
3. **Response is markdown, not JSON**: numbered references `[N]`, one block per
   paper — title (hyperlinked to `consensus.app/papers/details/<32-hex-id>`,
   `utm_source=claude_desktop` suffix), authors, year, citation count, journal,
   then the full abstract. Default 20 papers ("Found 20 papers, showing top 20").
4. **Consensus detail IDs are the join key** for Zotero deposits (deposited as
   `webpage` items with `consensus-id` in Extra per zms-homelab zotero_tools).

## `search` parameters (live schema 2026-08-15)

`query` (required) · `year_min`/`year_max` · `month_min`/`month_max` ·
`study_types[]` (rct, meta-analysis, systematic review, cohort, case-control,
etc.) · `sample_size_min` · `human` (bool) · `medical_mode` (bool) ·
`exclude_preprints` (bool) · `domain` (med,bio,cs,chem,phys,… comma codes) ·
`sjr_max` (1–4) · `duration_min`/`duration_max` (days) · `journal_name` ·
`publisher_name` · `page` · `include_full_text_chunks` (Enterprise).

## Server-shipped instructions (bind on this connector)

Results MUST be cited inline by their numbered references, e.g. `[1]`, `[2]`;
hyperlink paper titles with the exact returned URLs; attribute findings to
specific papers ("X improves Y [1]").

## Known-answer probe (2026-08-15)

Query: "what does the evidence say about metformin for longevity" → 20 papers,
mixed reception surface as expected for a contested question: favorable
meta-analysis (Campbell 2017, HR 0.93 all-cause mortality vs non-diabetics)
alongside critical review (Mohammed 2021, "remains controversial"), emerging
uncertainty (Keys 2025), null model-organism meta-analysis (Parish 2022), and
late-life harm (Espada 2020). Good spread of designs, years 2013–2026.

## Remaining unobserved

Rate-limit/429 behavior; quota semantics of the basic paid plan; full-text
chunks (Enterprise-only).

---

## First-contact protocol (retained for the next drift event)

1. Load the full live tool schema; record tool names, parameters, server-shipped
   instructions verbatim in intent.
2. Probe with a cheap known-answer query; record response shape, filters,
   auth/rate-limit behavior.
3. Rewrite this profile (dated, "re-check live" header retained).
4. Commit + push (canonical skills repo), redeploy the skill cache.
