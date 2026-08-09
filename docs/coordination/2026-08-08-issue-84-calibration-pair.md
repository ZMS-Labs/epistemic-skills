# Issue #84 — skills-side status (2026-08-08)

Paired proposal: exchange-protocol adoption, v4 event-contract re-pin, field-pair
ownership (`docs/coordination/epistemic-calibration.md` step 1).

## Skills repository (this repo)

| Item | Status |
|---|---|
| `epistemic-product-calibration@1` contract at `plugins/epistemic-skills/contracts/` | **Published** on `main`; verifier + fixtures in tree |
| Pin-tag reachability guard | **CI** — `.github/scripts/check_pin_tags.py` |
| v4 producer names in event map / schema | **On `main`** at v5 support point |
| Mint `pin/` tag for counterpart-selected coordinate | **Ready** when calibration names a commit |

## Calibration repository (counterpart)

| Item | Owner | Status |
|---|---|---|
| Adopt or counter-propose `epistemic-product-calibration@1` | calibration | **Adopted** — `docs/coordination/2026-08-09-adopt-exchange-protocol.md` on calibration `main` (pending merge via PR) |
| Re-pin event contract at v4+ coordinate | calibration | **Done** — `epistemic-skills-event-contract@2` core lock; catalog decoupled |
| Field-pair supply for mint gate | joint | **Open** |

No forced merge from this issue. Next step: calibration maintainer records adopt/counter
on an issue or PR in `ZMS-Labs/epistemic-calibration`, then skills mints the agreed `pin/` tag.
