
## AMENDMENT 2026-08-06 — step 5 has a precondition the design missed

**D3 stands. Its sequencing does not.**

The design says "delete `using-epistemic-skills` and `helix`" as though it removes
two seats. Measured before executing it:

```
plugins/epistemic-skills/skills/using-epistemic-skills : 254 tracked files, 250 under evals/
plugins/epistemic-skills/skills/helix                  :   6 tracked files,   4 under evals/
```

The router's directory holds the **`epistemic-flexibility`** corpus — including the
four-arm behavioral campaign whose null result (`p=0.875`) the README reports — and
the **`proportionality`** blinded runner. `helix/reference/composition-contract.json`
is likewise read by the generator and the outsource suite.

Deleting the seat by deleting the directory would destroy the package's entire
behavioral evidence corpus as a side effect of a routing decision. That evidence is
the most distinctive thing this package has: most skill collections assert benefit;
this one measured it, got a null, and published it.

### Revised step 5, in order

1. **Relocate the eval corpora first.** `epistemic-flexibility` and
   `proportionality` measure the *collection*, not the router seat. They belong at
   package level (e.g. `plugins/epistemic-skills/evals/`), moved with `git mv` so
   history follows. `helix`'s composition eval likewise.
2. **Re-point every consumer** — `sync_skill_surfaces.py` (`ROUTER_PATH`,
   `COMPOSITION_PATH`, `NON_DISCIPLINES`), `check_json_artifacts.py`,
   `check_skill_inventory.py`, the outsource suite's router and helix assertions,
   and the CI `Compile new Python` list, which names
   `using-epistemic-skills/evals/epistemic-flexibility/audit_enforcement_language.py`
   by path.
3. **Then and only then delete the two seats**, and change the discipline
   arithmetic from `skills - 2` (router + helix) to `skills - 1` (the entry point
   is not a discipline).

### The general rule this earns

**A seat and its directory are not the same object.** Removing a capability must
not remove evidence that merely happens to be stored under it. Before deleting any
skill directory, inventory what is under `evals/` and `results/` and relocate
anything whose subject is not that skill.

This is the same failure shape as everything else found today — a decision made
against a *name* rather than against the *thing the name is attached to* — and it
was caught by counting files before deleting them, not by reasoning about the plan.
