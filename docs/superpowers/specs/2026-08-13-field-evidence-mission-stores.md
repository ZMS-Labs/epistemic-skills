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

---

## Part 2 — what the deepest live chain actually says about manifest

Mined read-only from `zms-homelab/missions/media-library-rebuild` (90
checkpoints, 9 receipts, 61 notes). This is the estate's most-exercised
mission and therefore the best available evidence for the operator's bar,
which is not a feature list: **"manifest works as I intend it."**

### F5 — a schema-shape trap that produced a false finding in this very survey

`receipt_ids` is a **TOP-LEVEL** checkpoint field. It is NOT under `state`
(which holds only `frontier`, `notes`, `unresolved_verdicts`). My first reader
looked under `state`, got `None`, and was one step from recording "9 receipt
files on disk but receipts never registered in the chain" — a false integrity
finding about live data. A second read retracted it: the chain is consistent,
`receipt_ids` grows 0→9 across r44–r76 and the final list matches the nine
files exactly.

Recorded because the trap is structural, not personal: `state` is where a
reader expects mission state, and everything else mission-stateful IS there.
Any future auditor, doc, or migration reading this chain will make the same
guess. ⚠ **Direction- and absence-claims about the chain need two reads.**

### F6 — the lifecycle has no way back, and a live mission is wedged in it

At r87 a **read-only auditor** (`actor agent:audit-blind-recon`) ran
`custody_cli verify` to check chain integrity. `verify` is `begin_verification`
— a lifecycle **WRITE** wearing a read verb's name (es#138) — and it moved the
mission `active → verifying`. No operator grant, no amendment, no
authentication: an arbitrary `--actor` string moved lifecycle state. The
auditor disclosed it at r88, which is the only reason it is visible.

The steward could not undo it. From `verifying` the exits are PASS
(completed, terminal), FAIL (reopened, but that means recording a verdict that
never happened), INCONCLUSIVE (stays), or cancel. **There is no honest path
back to `active`.** So the mission sits in `verifying` — one `accept` away
from a PASS on work that was never performed — carrying a shouted frontier:

> `*** DO NOT ACCEPT THIS MISSION. Status 'verifying' is an ARTEFACT, not a
> claim that the work is done. ***`

Two things this is evidence for, both load-bearing on the manifest
re-derivation:

1. **Revocation is genuinely absent from the lifecycle**, exactly as
   `2026-08-13-acceptance-table-research.md` reports (no REVOKE anywhere).
   This is that gap with a live casualty, not a literature citation.
2. **A steward's only remaining control was prose.** The record's integrity was
   preserved by *refusing to falsify it* and writing a warning a human must
   read. Fabricating a verdict to fix a status would be worse — correct call —
   but a custody instrument whose last line of defence is a shouted note is
   the same shape as `scope`/`stop_rules` being decorative at run time.

### F7 — the envelope is entirely unset on the estate's biggest mission

```
scope.in = []   scope.out = []   permissions = []   protected_state = []
guard_mode = None    actuator_guards = 0    amendments = 1
```

Every machine-comparable declaration is empty. All the constraint the operator
actually cares about lives in prose `stop_rules`:

> escalate_if: *any action would delete or move existing .107 library content*
> · *any change to VPN/gluetun or download-client enabled state* · *any write
> into PrivateVault or other-category storage*
> hold_if: *queue exceeds the Phase-3 approved cap* · *free space below the
> 4TB / 1TB reserves*

**This is the efficacy question answered empirically.** PR #143 spent 33
review threads hardening `scope` — and `scope` is empty on the only serious
live mission, while the real boundaries sit in fields nothing reads at run
time. It is not that stewards decline to declare an envelope; it is that the
things worth declaring here (*don't delete library content*, *don't touch VPN
state*) are **conditions on effects, not path sets**, and the schema offers a
machine-checkable slot only for paths. Contrast the custody-instrument
mission, whose work IS file-shaped: its `scope.in`/`scope.out`/`permissions`/
`protected_state` are all richly populated. **The envelope is used exactly
when the work is file-shaped and abandoned when it is not.** Any manifest v6
claim about scope enforcement has to say which of those two worlds it is for.

### F8 — custody is used ~80% as a journal

Of 61 notes on the final record: **49 free text**, 7 `effect:`, 2
`drift detected:`, 2 `reconciled:`, 1 `authority amended:`. The
machine-readable verbs are 12 of 61. The instrument's dominant real use is
durable narrative that survives interruption — which is what the frontier and
notes deliver, and which needs no envelope at all.

### F9 — the verbatim-grant instruction is being followed, which validates the #30 ruling

The single amendment is the operator's own words, lowercase, unedited, typo
intact (*"the authority needs to be such taht it records the truth in all of
its complexity…"*). Stewards really do paste operator text verbatim into
`amend`. That is the concrete population that PR #143's reserved-note refusal
would have blocked with no stated exit had the operator's sentence begun
`effect: ` — the defect fixed at `8118130`. The ruling was not hypothetical.
