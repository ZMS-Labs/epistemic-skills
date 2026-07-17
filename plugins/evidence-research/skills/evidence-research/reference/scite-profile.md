# Scite MCP — observed profile (first contact + authenticated re-probe 2026-07-17)

> **Not permanent configuration — re-check live.** This records the surface
> observed on first contact via the Claude Code HTTP MCP registration
> (`mcp__scite__*`, server `https://api.scite.ai/mcp`). Live tool schema wins
> over this file. Capabilities drift; auth state changes per session.

## Headline findings

1. **The server surfaced 24 tools** — far richer than the documented surface
   in `scite-first-contact.md` (which listed only literature search, Smart
   Citations, tallies, DOI lookup, holdings). No `check_holdings` tool exists.
2. **The session ran UNAUTHENTICATED.** The `claude mcp add --transport http`
   registration connects at transport level without completing OAuth, and the
   server silently serves an anonymous free tier. This is the exact
   unknown≠absent failure mode the first-contact protocol predicted — see
   "Auth semantics" below.
3. **Anonymous tier returns slim records only**: every `search_literature`
   mode (bare-DOI fetch, DOI+term, plain term search, tally-filtered) returned
   only `{title, url, doi}` per result. No tally, no citations, no abstract,
   no fulltextExcerpts, no retraction_notices — despite the tool description
   promising all of them. Whether the authenticated tier delivers the rich
   fields is **UNVERIFIED** until OAuth is completed.

## Tool inventory (observed 2026-07-17)

Literature: `search_literature` (the only scholarly-literature tool; Smart
Citations/tallies/excerpts ride on it per its description — no separate
tally or citation tool exists).

Collections (require sign-in): `create_collection`, `get_collection`,
`search_collections`, `update_collection`, `delete_collection`,
`add_dois_to_collection`, `remove_dois_from_collection`.

Regulatory/adjacent datasets (undocumented in marketing; present live):
`search_clinical_trials`/`get_clinical_trial` (ClinicalTrials.gov),
`search_device510k`/`get_device510k`, `search_510k_summaries`/
`get_510k_summary` (FDA 510(k) metadata + OCR'd summary full text),
`search_drugs`/`get_drug` (SPL/Orange Book/Drugs@FDA),
`search_faers`/`get_faers_report`, `search_maude`/`get_maude_report`,
`search_mhra`/`get_mhra_alert`, `search_grants`/`get_grant` (NIH/NSF/
Wellcome/EU), `search_patents`.

## `search_literature` schema (verbatim highlights)

- Targeting: `dois[]` (preferred), `titles[]`, `term` (Boolean AND/OR/NOT,
  phrase, proximity `"a b"~5`; cross-field over title/abstract/full-text).
- `dois`/`titles` WITHOUT `term` = metadata fetch; WITH `term` = full-text
  excerpt extraction (documented: up to 5 excerpts ~500 chars per call — vary
  `term` to read a paper section by section).
- Reception filters exist as **parameters**: `supporting_from/to`,
  `contrasting_from/to`, `mentioning_from/to`, `citing_publications_from/to`,
  `has_tally`, `has_retraction`, `has_concern`, `has_correction`,
  `has_erratum`.
- Scoping: `author`, `affiliation`, `journal`, `publisher`, `topic`,
  `paper_type`, `year`/`date_from`/`date_to`, `collection_slug`.
- Pagination: `limit` (default 10, keep 10–50), `offset`.
- Documented response fields: metadata, `fulltextExcerpts`, `access` (resolved
  access link), `citations` (Smart Citation statements with
  supporting/contrasting/mentioning/unclassified), `tally`,
  `retraction_notices`, `isOa`/`oaStatus`/`license`.
  **Observed anonymous response fields: `title`, `url`, `doi` only.**

## Server-shipped instructions (bind on this connector)

The server ships usage instructions (visible in the MCP server-instructions
block). Key binding points, recorded verbatim in intent: never fabricate
citations — cite only papers retrieved through the tool; APA citations +
References section; ALWAYS check `editorialNotices` for retractions before
citing; construct links as `https://doi.org/{doi}`; token-efficient full-text
workflow = discover broadly, then `dois`+targeted `term` per section
("introduction background" / "methods methodology" / "results findings" /
"discussion conclusion"); plan 3–5 diverse specific queries; verify
bibliographic fields against retrieved records and flag discrepancies.

## Auth semantics (the critical part)

- Anonymous calls **succeed with HTTP-200-shaped slim results** for a small
  free quota. There is NO in-band indication of the degraded tier. A run that
  trusted these results would silently record "no contrasting citations /
  no retraction notices" — exactly the failure mode the reception pass exists
  to prevent.
- Quota exhaustion then produces a hard tool error:
  `"Sign in to scite.ai to use this tool. Start a free trial…"` /
  `"You've used your last free scite search."`
- Collections tools fail loudly when anonymous (same sign-in error) even
  before quota exhaustion.

### MANDATORY auth canary (every evidence-research run using Scite)

Before the reception pass, call `search_collections` (no args, read-only,
cheap). Signed-in → returns `{collections, total}`. Anonymous → errors with
the sign-in message. **If the canary fails, Scite is UNAUTHENTICATED: stamp
matrix rows `reception: UNVERIFIED (Scite unauthenticated)` and do NOT treat
slim search_literature results as reception evidence.**

## AUTHENTICATED re-probe (2026-07-17, OAuth completed via /mcp)

- Auth canary passes: `search_collections` → `{"collections": [], "total": 0}`.
- **Responses stay SLIM even authenticated**: every `search_literature` mode
  (bare-DOI, DOI+term, term search) still returns only `{title, url, doi}`.
  The rich fields in the tool description (`tally`, `citations`,
  `fulltextExcerpts`, `retraction_notices`, abstracts) are NOT delivered by
  this MCP transport at all — the description is aspirational/stale. Do not
  wait for them or claim them.
- Retracted papers carry a **`RETRACTED:` prefix in `title`** (observed on
  the Wakefield 1998 Lancet paper).

### Reception pass — the workable degraded method (filters DO work)

Server-side filters verifiably filter (falsification pair 2026-07-17:
NumPy DOI + `has_retraction:true` → 0 results; Wakefield
`10.1016/s0140-6736(97)11096-0` + `has_retraction:true` → returned):

- **Retraction check** (the skill's single worst failure): membership test
  `dois: [X], has_retraction: true` → returned = RETRACTED. Same pattern for
  `has_concern` / `has_correction` / `has_erratum`.
- **Reception signal**: threshold membership tests
  `dois: [X], contrasting_from: N` (verified: Wakefield passes
  `contrasting_from: 5`). Bisect N for a coarse tally when a magnitude
  matters; `supporting_from`/`mentioning_from` likewise.
- **⚠ Misleading error**: a DOI excluded BY A FILTER returns
  `"No indexed papers matched the provided DOI(s) … not present in Scite's
  index"` — it does NOT mean the paper is unindexed. Never read that message
  as absence-from-index when filters are present.
- Citation *contexts* (the quoted citing sentences) are NOT retrievable via
  this MCP — record `reception: filter-level (no contexts)` in the matrix;
  context-level interrogation needs the scite.ai web UI (operator).

## Remaining unobserved

- Rate-limit / 429 behavior.
- Whether the claude.ai Scite connector (if it surfaces as
  `mcp__claude_ai_Scite__*`) exposes a richer response shape than this
  Claude Code HTTP registration.

---

## First-contact protocol (retained for the next drift event)

1. `ToolSearch("+scite")` → load ALL scite tool schemas in one call.
2. Record verbatim: tool names, parameters, server-shipped instructions.
3. Probe each capability with a cheap known-answer call (e.g.
   10.1038/s41586-020-2649-2) and record: response shape, whether contexts
   are included or need a second call, rate limits, auth failures.
4. Rewrite this profile (dated, "re-check live" header retained).
5. Update `evidence-research/SKILL.md` ONLY if the observed surface
   contradicts its engine-role assumptions.
6. Commit + push (canonical skills live in git), redeploy the skill cache.
