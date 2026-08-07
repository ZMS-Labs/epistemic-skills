# Lens: chaos-monkey

**Verdict from this lens:** GO for merge; CONDITIONAL for release tag

## Findings

### F1 — absence-as-success controls now fail closed

Sentinel corpus executes oracles that reject UNKNOWN→OK, plausible→CAUSE,
source-read→LANDED, silence→PROVEN, and routine-overfire. Inventory fails if a
named sentinel file is missing. Planted self-tests cover empty and missing
cases. **Fixed.**

### F2 — public-content gate can still be allowlist-gamed

`check_public_content.py` allowlists historical review receipts. An insider could
smuggle a private path into an allowlisted prefix. Mitigation: allowlist is path
prefix to release-review docs only; keep it narrow. Residual: **P3 accepted** with
monitoring — do not broaden prefixes without review.

### F3 — description ceiling equals measured total

Ceiling 8230 == measured 8230. Any description growth fails CI. Estate-wide drops
remain invisible without `--capture`. **Release condition C1/C2.**

### F4 — generated inventory markers could be deleted

If someone removes GENERATED markers and hand-edits, sync `--check` must still
fail. Current `--check` re-renders and diffs. **Covered.**
