# Field evidence — mission stores in the wild (2026-08-13)

Read-only survey of `Y:\dev\*/missions`, prompted by the operator's note that
other agents are already using mission custody. Four repos carry stores; five
missions total. Nothing was modified.

| store | checkpoints | receipts | kinds | tail status |
|---|---|---|---|---|
| `epistemic-skills/missions/custody-instrument` | 2 | 0 | `checkpoint@1` | active |
| `practical-agency/missions/climb-pa-0-1` | 48 | 3 | **pre-@1 generation** | — |
| `practical-agency/missions/e2e-proof-001` | 6 | 0 | pre-@1 generation | — |
| `zh-wt-mission/missions/media-library-rebuild` | 89 | 9 | `checkpoint@1` | verifying |
| `zms-homelab/missions/media-library-rebuild` | 90 | 9 | `checkpoint@1` | verifying |

## Findings that bear load

**F1 — every live chain is `checkpoint@1`.** Task 5's anchor gate
(presence-keyed verification; epoch-2-keyed minting) and read-path epoch
monotonicity engage on none of them. The design claim "a genuinely un-migrated
@1 mission has no anchor, mints none, and stays exactly as unbricked as
before" has a concrete population it now provably protects.

**F2 — the lagging twin exists in the field, one write from a fork.**
`zh-wt-mission` (a zms-homelab worktree) and `zms-homelab` both hold mission
`media-library-rebuild`. The 89 common checkpoints are **byte-identical**
(sha-compared); zms-homelab is one revision ahead (r90). No attacker, no
tampering — just a worktree copy that stopped receiving writes. An agent
resuming the stale copy would append r90 there and create a genuine split
view. This is the exact scenario the anchor design's path-keyed identity +
`mission_id` secondary scan refuses ("a mission dir present twice IS a fork"),
and it is also a live exemplar of the **equivocation / split-view** class the
acceptance-table research (`2026-08-13-acceptance-table-research.md`) lists as
uncovered by A1–A8. The re-derivation should use it: the hazard is real,
attacker-free, and produced by normal worktree hygiene.

**F3 — a pre-@1 format generation is live.** `practical-agency` stores use
`<mission-id>.r<NNNNNNNN>.json` with interleaved `.r<NNNNNNNN>.receipt.json`
files inside `checkpoints/` — the store's `r????????.json` glob does not even
enumerate them. Task 7 (`migrate`) and any manifest claim about resumability
have a second migration distance to speak to, or must explicitly scope these
out as a retired generation.

**F4 — other agents leave evidence through normal use.** The 89/9 and 90/9
chains were written by the media-library-rebuild effort, not by this program.
Mission custody is being exercised as a consumer product while contract@2 is
mid-build; changes to store semantics land under real users, and the honest
baseline measurements in the manifest mission proposal should be re-taken
against these chains, not only against fixtures.
