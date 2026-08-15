# Dispatcher mechanical-criticism addendum (Step 6 record)

Dispatcher = the session that froze the dossier (bias disclosed in dossier).
Executed at the barrier, before arbitration. Each item: lens claim →
dispatcher re-execution → result.

1. **polymath F1a (repo description stale):** re-ran
   `gh api repos/ZMS-Labs/epistemic-skills --jq .description` → live string
   ends "…with a router that ties them together." **CONFIRMED** (the router
   seat was deleted in v5.0.0).
2. **polymath F1b (live wiki stale):** fetched
   github.com/ZMS-Labs/epistemic-skills/wiki/Installation-and-Harness-Compatibility →
   "Applies to: epistemic-skills v5.0.0", "Expect fourteen skills at
   v5.0.0", all install URLs `tree/v5.0.0`; zero v5.1.0/fifteen references.
   **CONFIRMED.**
3. **script-kiddie F1 (internal topology strings new since v5.0.0):**
   `git grep -l "10\.10\." HEAD` → **8 files** (lens said 11 — count
   corrected to 8; substance unchanged), vs **0 files at v5.0.0**; the 8 =
   custody example fixtures (4 invalid + 1 valid manifest-guard JSONs),
   test_custody_gate.py, and two stage-c custody-hook docs. Diff window
   `v5.0.0..8180554` = **266 files confirmed** (vs 19 reviewed). **CONFIRMED
   with count correction.**
4. **script-kiddie F3 (personal email spread):** `git grep -l
   zachstern@gmail` → 11 files at HEAD, 10 at v5.0.0; the delta file(s)
   (mission-custody-contracts plan/spec docs) are inside the release window.
   **CONFIRMED.**
5. **adjacent-possible F2 (budget script header says "14"):** read
   `.github/scripts/check_description_budget.py:59-61` → "the sum of the 14
   packaged skill description values" while CEILING_BYTES=8636 is the
   fifteen-skill total. **CONFIRMED** (zero-behavior comment).
6. **angry-customer F2 / adjacent-possible F1 / causal F1 (workflow_dispatch
   exists on both path-filtered suites):** dispatcher read both workflow
   files earlier this session — both carry `workflow_dispatch:` triggers.
   **CONFIRMED.**
7. **polymath F4 (phantom "inherit 5.0.0 tiers"):** dispatcher read
   RELEASE-5.0.0.md:154 earlier this session — item 7 was "**NOT TRACKED IN
   THIS TABLE**". **CONFIRMED** (no 5.0.0 tiers exist to inherit).
8. **FM-B sweep (self-graded run citations):** three independent lenses
   (script-kiddie, causal-identification, adjacent-possible) each re-ran
   the GitHub API checks — all ten cited run IDs resolve at the claimed
   SHAs with conclusion=success. Dispatcher re-verified the same earlier in
   session. **FM-B stays killed.**

Falsifier well-formedness: all P1/P2 findings above carry method +
threshold + timeframe. No P1/P2 struck for malformed falsifiers.

Oracle-adequacy spot check: the "green CI" claims were verified against
step-level job data (not run labels) by dispatcher and ≥1 lens
independently; the "wiki/description stale" claims were verified against
the LIVE surfaces (not caches). Adequate for their claims.
