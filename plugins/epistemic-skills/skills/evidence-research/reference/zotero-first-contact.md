# Zotero — durable library substrate (first contact)

> **Not permanent configuration — re-check live.** This records the *epistemic
> role* of the durable library layer and the access modes agents may find.
> Live schema / LOCAL.md bindings win. Capabilities and auth state drift.

## Epistemic role (why Zotero is in the triad)

| Layer | Question | Unit | Lifetime |
|---|---|---|---|
| Consensus | What does the literature say? | paper | session-bound discovery |
| Scite | How was this paper received? | citation statement | session-bound interrogation |
| **Zotero (library)** | What do *we* already hold, and what must this run leave behind? | library item (DOI-keyed) | **durable across sessions** |

Zotero is **not** a third discovery search engine competing with Consensus. It
is the substrate the other two feed: holdings check before rediscovery, deposit
after selection, and (when the Scite Zotero plugin is enabled) at-rest
reception columns that survive after MCP sessions expire.

## Access modes (negotiate every run)

Prefer, in order:

1. **Zotero Web API** (`api.zotero.org`) with a scoped API key + user/group
   library id — machine-readable holdings search and DOI deposit. Preferred
   for agents when credentials exist in the environment / secret store named
   by LOCAL.md.
2. **Library MCP** (if a harness registers one) — inspect live tool schema;
   same holdings/deposit contract.
3. **Operator-mediated GUI** — desktop or web-desktop Zotero behind SSO.
   Agents emit an **operator deposit checklist** (DOI list + collection name)
   and stamp `deposit: OPERATOR_PENDING`. Do not claim GUI automation unless
   LOCAL.md documents a working driver for that surface.

Never invent a silent GUI drive. A KasmVNC / remote-desktop canvas is often
**operator-only** (browser automation extensions frequently cannot inject into
an active VNC canvas).

## Holdings / deposit contract

**Holdings check (before Consensus rediscovery):**
- Search by DOI first; fall back to exact title.
- Record: item key, DOI, tags, notes, collection path, any at-rest Scite
  columns (Supporting / Contrasting / Mentioning / totals).
- Empty library → `holdings: empty` (real state, not a failure to search).

**Deposit (after matrix selection):**
- Add by DOI (preferred) into a run-scoped collection:
  `evidence-research/<claim-or-decision-id>/<YYYY-MM-DD>`.
- Tag with mode (`quick|standard|deep|formal-support`) and support relation.
- Record item keys in the run record.

**At-rest Scite plugin (optional, complementary to Scite MCP):**
- Plugin fetches public Smart Citation data **by DOI** — no Scite account
  required for the plugin (do not conflate with Scite *MCP* OAuth).
- Columns are often off by default; empty library ⇒ blank columns (not
  "zero contrasting").
- Label any plugin-sourced reception as
  `reception: zotero-plugin-at-rest (no MCP contexts)` — never as a live
  Scite MCP pass.

## Degradation labels (copy verbatim into the matrix)

| Condition | Stamp |
|---|---|
| No API / MCP / operator available | `holdings: UNVERIFIED (Zotero unavailable)` + `deposit: SKIPPED` |
| Operator must finish GUI deposit | `deposit: OPERATOR_PENDING` |
| Library reachable but has zero items for the claim | `holdings: empty` |
| Item already in library | `holdings: held` |
| Item added this run | `holdings: deposited-this-run` |

## Anti-patterns

| Thought | Reality |
|---|---|
| "I listed the DOIs in the chat — that's a deposit" | No. Deposit means a library item with a durable key. |
| "Zotero GUI loaded a 200 — library is usable" | Auth walls and empty sync states still count as unavailable / empty. |
| "Scite plugin columns are blank ⇒ no retractions" | Empty library or disabled columns look identical — verify DOI item + columns enabled. |
| "Skip Zotero; Consensus+Scite are enough" | The skill requires the triad in tandem; skip only with an explicit durability coverage limit. |

## Fleet binding

Concrete host, SSO, sync account status, and operator GUI steps live in
`LOCAL.md` — never hardcode a host into this file.
