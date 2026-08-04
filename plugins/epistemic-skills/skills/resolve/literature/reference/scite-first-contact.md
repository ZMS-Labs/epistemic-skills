# Scite MCP — first-contact protocol (SUPERSEDED — see scite-profile.md)

**First contact happened 2026-07-17: the live surface is
recorded in `scite-profile.md`, which supersedes this file.** Retained for
provenance: the pre-contact documented surface below turned out materially
wrong (24 tools, no `check_holdings`, anonymous-tier silent degradation).

Status as of 2026-07-17 (pre-contact): the Scite MCP server
(`https://api.scite.ai/mcp`, OAuth via `api.scite.ai/mcp/oauth/*`, scope
`mcp`) is registered in Claude Code user config, transport-level Connected.
Everything below is from public documentation and marketing material.

## Documented capabilities (unverified)

- Literature search over ~250M articles/chapters/preprints/datasets.
- Smart Citation retrieval: citing statements classified
  **supporting / contrasting / mentioning**, with the citation *context*
  (the excerpt around the citation) and DOI/metadata.
- Citation tallies/metrics per paper.
- DOI lookup / related-work discovery.
- `check_holdings` — institutional/personal full-text availability.

Sources: mcpservers.org/servers/www-scite-ai-mcp; Research Solutions launch
PR (2026); scite.ai; api.scite.ai/docs.

## First-contact protocol (do this on the first session where scite tools appear)

1. `ToolSearch("+scite")` → load ALL scite tool schemas in one call.
2. Record verbatim: tool names, parameters, server-shipped instructions (if
   the server ships usage instructions, they bind on this connector the same
   way Consensus's do — note them here).
3. Probe each capability with a cheap known-answer call (e.g. tallies for a
   famous DOI like 10.1038/s41586-020-2649-2) and record: response shape,
   whether contexts are included or need a second call, rate-limit headers,
   auth failures.
4. Rewrite this file into `scite-profile.md` (observed profile, dated, with
   the same "not permanent configuration — re-check live" header the
   Consensus profile uses). Keep this first-contact file's protocol section
   at the bottom for the next drift event.
5. Update `evidence-research/SKILL.md` ONLY if the observed surface
   contradicts its engine-role assumptions (e.g. no tallies exposed → the
   reception pass degrades to citation-context sampling; say so in §4).
6. Commit + push (canonical skills live in git), redeploy the skill cache.

## Known constraints to check at first contact

- Is search query-only or structured? (Mirrors the Consensus capability
  negotiation.)
- Are tallies returned with search results or only per-DOI?
- Is there a retraction/notice field, or is retraction inferred from
  editorial-notice citation types?
- Subscription gating: which calls require the paid plan; what does an
  entitlement failure look like (401 vs empty result) — an empty result that
  is actually an auth failure would silently fake "no contrasting citations",
  which is exactly the failure mode the unknown≠absent rule exists for.
  **If an engine call's failure is distinguishable from a true empty result,
  the run record must distinguish them.**
