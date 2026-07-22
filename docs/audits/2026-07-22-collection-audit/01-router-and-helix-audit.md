# Audit 01 — using-epistemic-skills + helix

**Provenance:** 2026-07-22 collection audit, isolated read-only subagent against the working tree at 61fbf95 (v2.6.0). Yardstick: the collection's five shared invariants. Line citations are to `plugins/epistemic-skills/skills/<name>/SKILL.md` unless prefixed otherwise.

Scope note: the two target skills are routing/pairing layers, so sections 3–4 required reading all six discipline skills in full — done. Coverage is total, not sampled.

---

## Skill 1: `using-epistemic-skills` (the router)

### 1. Boundary/handoff contract as it exists today

- The router's own boundary is stated only as a prohibition: "It never does the work itself — always read the skill it points you to" (`using-epistemic-skills/SKILL.md:13-14`). There is no explicit Consumes/Produces/Hands-to row for the router itself; the table at `:21-28` defines the **members'** boundaries, not the router's.
- The member handoff table (`:21-28`) is a **prose markdown table**. Produces entries are noun phrases with no artifact shape: "a **rewritten, de-risked request**" (`:23`), "a **derived verdict**" (`:24`), "an **approved, evidence-bound completion contract**" (`:26`), "a **computed GO / CONDITIONAL / NO-GO** + Conflict Ledger" (`:27`). No file path, no schema, no required-field list for any of them.
- The router's own output is a routing decision expressed as chat prose: "skip any stage whose trigger is absent, **and say you skipped it**" (`:52-53`) and "pass each output to the next per the handoff table" (`:69-70`). No format, no grammar, no sink. Contrast: gauntlet mandates a skip format ("`gauntlet: skipped — <Q1|Q2> failed because <cited evidence, not adjective>`", `gauntlet/SKILL.md:147-148`) and helix mandates an emit line (`helix/SKILL.md:57`). The router — the chokepoint of the whole collection — has the **weakest** audit format of the three.

### 2. Findings vs the five invariants

- **Invariant 1 (floors) — strength.** "Most work fires zero or one of these" (`:37`); "Running a stage on work that doesn't need it is ceremony" (`:53`); "this router does not manufacture work" (`:68`).
- **Invariant 2 (derive/verify) — strength + gap.** Strength: "Match the trigger you can *observe*, not a vibe" (`:57`). Gap (minor **defect**): there is no requirement to *record* which triggers were observed — the skip statement is unaudited prose, asymmetric with gauntlet's and helix's mandated formats (citations above).
- **Invariant 3 (boundary) — strength.** `:30-32` ("these boundaries are the interfaces"), anti-pattern rows `:108-113` correctly police member-level overreach ("evidence-research says GO" → "It never renders a verdict", `:111`).
- **Invariant 4 (fail closed) — gap.** No degradation rule for a routed-to skill being absent/uninstalled in the harness. The router routes by name; nothing governs the miss. (`:55-73` specifies routing, never routing failure.)
- **Invariant 5 (provenance/independence) — strength.** Invariant 5 stated at `:90-92`; "The UAT actor never certifies its own work — that's the whole point" (`:113`).
- **Cross-file drift (minor defect):** README.md:31 sequences the arc as "recon → design → evidence → gate → **verify**"; the router uses "recon → **decide** → [evidence] → contract → gate → **prove**" (`:3`, arc diagram `:40-44`). Cosmetic noun drift between the two canonical descriptions of the same arc.

### 3. Duplicated checks (router ↔ collection)

| Check | Where duplicated | Classification |
|---|---|---|
| Trigger matching for each member (routing table `:59-66`) | Each member's own `description` frontmatter + auto-fire sections (`blindspot-pass:42-61`, `gauntlet:42-55`, formal-rigor description `:3`) evaluate the same trigger independently | **Idempotent-mechanical within a session** — the observation doesn't change; safe to attest once. But **freshness-sensitive across stages**: new triggers can appear mid-work (a scholarly premise surfacing in brainstorming), which helix's cross-cutting row exists to catch (`helix:39,46`). Attestation needs stage-boundary scoping. |
| "Pass each output to the next" (chain integrity, `:69-70`) | helix's co-fire checklist re-asks "did blindspot-pass run?" (`helix:62-63`) | **Idempotent-mechanical** — whether a skill ran and produced its artifact is checkable once and never changes. Prime trust-contract candidate. |
| "Epistemic fires first" ordering (`:96-102`) | Restated in `helix:24-31` and `docs/superpowers/specs/2026-07-20-helix-design.md:42-48` | Three prose copies of one axiom; consistent today, drift-prone. **Idempotent-mechanical** per boundary. |

### 4. Trust-contract readiness

- **Could emit:** a one-line routing record, e.g. `router: fired=[blindspot-pass→<artifact-ref>] skipped=[evidence-research(trigger-absent)]`. This is machine-checkable, and downstream consumers (helix's co-fire check, gauntlet Step 0) could then verify *that the chain ran* instead of re-interrogating the session.
- **Must never attest:** the *quality* of any member's output (the router is not a judge — attesting "the rewrite is good" would violate verdict independence); trigger-absence claims beyond the current stage boundary; anything about evidence freshness (that is evidence-research's "live this run" doctrine, `evidence-research:261-263`, and gauntlet's truth-gate, `gauntlet:96-101` — both intentionally freshness-maximal).

### 5. Unfinished-feeling items

1. No skip/say format — the only collection-layer decision point with no auditable emission (`:53`).
2. Handoff table Produces column has no artifact shape — downstream skills cannot mechanically verify they received a well-formed input (`:21-28`). **This is the single biggest blocker for the trust-contract goal.**
3. No missing-skill degradation rule (`:55-73`).
4. README arc-noun drift (README.md:31 vs `:3`).
5. The helix pointer is one buried sentence (`:96-98`); the frontmatter `description` (`:3`) doesn't mention helix, so description-triggering harnesses may never surface the tandem path from the router.

### 6. Minimal improvement proposals (one focused PR each)

- **PR R1:** Add a one-line routing-record format (mirroring `helix-check:` and gauntlet's skip format): `router: fired=[...] skipped=[skill(trigger-absent)]`. ~4 lines in SKILL.md.
- **PR R2:** Add one "Artifact shape" note under the handoff table pinning each member's output form (prose section in chat / named file / JSON). One table annotation, no new mechanism.
- **PR R3:** One line: if the routed-to skill is absent, say so and stop — never improvise the discipline inline.
- **PR R4:** Reconcile README arc nouns with the router's (one-line README edit).
- **PR R5:** Mention helix in the router's frontmatter `description` (one clause).

---

## Skill 2: `helix` (the pairing map)

### 1. Boundary/handoff contract as it exists today

- Own boundary, explicit and clean: "This skill tells you which member pairs with which stage, in what position — **and nothing else**. **It never routes within a collection**" (`helix/SKILL.md:20-22`); "It sits between them. Member-level routing stays in `using-superpowers` and `using-epistemic-skills`" (`:111`).
- **Consumes:** the observation that a workflow stage fired / task start with both layers present. **Produces:** a pairing decision plus the `helix-check:` audit line. **Hands to:** the paired skill via the routers.
- Artifact shape: the `helix-check: <stage> → <pair> → fired|skipped(<reason>)` line (`:56-57`) — specified in **one sentence**. No grammar (what's legal inside `<reason>`?), no reason floor, no persistence sink, no rule on where the line goes. It is the collection's only audit artifact at the routing layer, and it is **semi-machine-readable at best**.

### 2. Findings vs the five invariants

- **Invariant 1 (floors) — strength.** "clean implementation needs no ceremony" (`:42`); "Fire-nothing is a valid outcome. helix manufactures no work" (`:80-81`); ceremony anti-pattern (`:108`).
- **Invariant 2 (derive/verify) — strength + two gaps.** Strength: "Make the check auditable" (`:56`). Gap 1 (**defect**, small): `skipped(<reason>)` has no floor on reason quality — a bare `skipped(not needed)` satisfies the format; gauntlet's analogous rule demands "cited evidence, not an adjective" (`gauntlet:147-148`). Gap 2 (gap): the co-fire checklist questions (`:62-78`) are self-assessed ("Ask: does its epistemic pair's own trigger match right now?", `:59-60`) without the router's "trigger you can *observe*" discipline (`router:57`) carried in.
- **Invariant 3 (boundary) — strength + one real defect.** Strength: `:20-22`, `:111`. **Defect — trigger narrowing:** the design doc explicitly rejected duplicating trigger tables (`helix-design.md:28-33`), yet the map restates *narrowed* trigger conditions inline. Gauntlet's own triggers include "infra-class… security posture; governance or legal-charter; **non-refundable spend**; architecture commit; a high-stakes claim that is hard to verify" (`gauntlet:47-51`); helix's rows say only "irreversible or one-way-door" (`:40`) and "irreversible / high-blast-radius" (`:45`). An agent following helix alone could skip gauntlet on a reversible-but-security-posture change or a non-refundable spend. The router has the same narrowing in milder form (`router:65` parenthetically folds security under irreversibility).
- **Invariant 3, second defect — guard softening across a restatement:** the checklist entry "did blindspot-pass run, or was its trigger absent (**territory already fully held in context**)?" (`:62-63`) paraphrases blindspot-pass's skip gate, which is deliberately *harder*: "skip only if you can, right now, name ≥2 concrete landmines (file:line) and the pattern's canonical example… without opening anything new" (`blindspot-pass:56-59`). helix's softer wording lets an agent attest "territory held" without the skip-gate proof. This is exactly the failure mode a trust contract must not encode.
- **Invariant 4 (fail closed) — strength + gap.** Strength: "an unfired pair is a stated decision, not an omission" (`:60-61`); fire-nothing valid (`:80-81`). Gap: `helix-check` lines have no persistence requirement — a line designed to be "auditable" (`:56`) evaporates with the session. Also no rule for a paired epistemic member being missing from the install (the "Any harness, any layer" section `:84-102` covers absent *auto-trigger* and non-superpowers layers, not absent skills).
- **Invariant 5 (provenance/independence) — strength.** helix never evaluates member outputs: "helix only pairs. Read the paired skill; the discipline lives there" (`:110`); "I basically already did this informally" → "Informal ≠ the discipline" (`:113`) correctly blocks self-attestation of rigor.

### 3. Duplicated checks (helix ↔ collection)

| helix check | Duplicated at | Classification |
|---|---|---|
| "Did blindspot-pass run / was its trigger absent?" (`:62-63`) | blindspot-pass auto-fire + skip gate (`blindspot-pass:42-61`) | Run/no-run fact: **idempotent-mechanical** — attest once. Skip-gate proof: belongs to blindspot-pass, must be *referenced*, not re-run — and not softened. |
| "Is 'better/cleaner/faster' being asserted?" (`:64-65`) | formal-rigor trigger (`applying-formal-rigor:3,19`) | **Idempotent at the decision point; freshness-sensitive across a stage** — new assertions appear during brainstorming. Attestation needs decision-point scoping, not session scoping. |
| "Is anything in it irreversible?" (`:66-67,72-73`) | gauntlet triage Q1 (`gauntlet:143-148`) | **Idempotent-mechanical only against a frozen subject.** Gauntlet itself: "If the subject moves, restart" (`gauntlet:138`). Any attestation must bind to the subject's hash/revision — a plan that keeps evolving invalidates the triage. |
| "Only on explicit goal-authoring intent does write-goal fire" (`:68-69`) | write-goal consent gate (`write-goal:27-34`); router anti-pattern (`router:112`) | **Idempotent-mechanical** — consent is a fact of the conversation; attest "no intent observed as of <boundary>". New consent can arrive later; window-scoped. |
| "If UI-facing, the stage *is* evidence-locked-uat" (`:70-71`) | UAT Step 0 tier triage (`evidence-locked-uat:14-24`) | Surface classification: **idempotent-mechanical**. But UAT's `BLOCKED_ENVIRONMENT` check (`:23-24`) is **freshness-sensitive** (preview envs die) — must never be attested stale. |
| "Epistemic first at every boundary" (`:24-31`) | router `:96-102`; design doc `:42-48` | **Idempotent-mechanical** per boundary; three prose copies, drift-prone. |

The big one: **gauntlet Step 0 live-verifies every premise** (`gauntlet:96-101`: "NOT session memory or prior summaries") even when its subject arrives from blindspot-pass, which *already* live-verified the brief's assertions (`blindspot-pass:73-76`). This duplication is **freshness-sensitive by design** — the trust contract must **not** absorb it. What it *can* absorb is **subject identity/provenance**: an attestation that the dossier gauntlet froze is content-identical to the blindspot-pass rewrite (hash-bound), so gauntlet verifies freshness of *premises* without re-deriving *provenance*.

### 4. Trust-contract readiness

- **Could emit:** the existing `helix-check:` line upgraded minimally: `helix-check: <stage> → <pair> → fired(<artifact-ref>) | skipped(<reason-class>: <evidence>)`, with reason classes like `trigger-absent | already-ran(<ref>) | operator-override`. With the `fired(<artifact-ref>)` form, helix becomes the **chain-of-custody carrier**: gauntlet Step 0 or UAT Step 0 could verify "the arc ran in order, epistemic-first" by reading check lines instead of re-asking the session. The best existing model for the artifact-ref format is UAT's `manifest.json` with sha256 of `gate.json` (`evidence-locked-uat:63-64`) — content-addressed, machine-checkable, already in the collection.
- **Must never attest:** (a) content validity of any member output — helix is not a judge; (b) verdict independence — gauntlet's lens isolation (`gauntlet:251-253`) and UAT's actor/verifier separation (`evidence-locked-uat:9-12,88`) must be *executed*, never inherited; the contract may carry independence *metadata* (who judged, which context/model family) but never a judgment; (c) evidence freshness — evidence-research's "reception data is `[V]`-grade **only when pulled live this run**; remembered tallies are `[H]`" (`evidence-research:261-263`), gauntlet's truth-gate, and UAT's environment reachability must re-run per their own clocks; the contract should carry *what was checked, when, to what level* so downstream can assess adequacy rather than blindly re-run or blindly trust.

### 5. Unfinished-feeling items

1. `helix-check` is a seed, not a contract — one sentence (`:57`), no grammar, no reason floor, no sink.
2. Trigger narrowing vs gauntlet's own trigger list (`:40,45` vs `gauntlet:47-51`).
3. Skip-gate softening for blindspot-pass (`:62-63` vs `blindspot-pass:56-59`).
4. Missing pairing: the map pairs evidence-research only as brainstorming-cross-cutting (`:39`); the **gauntlet Step-0 pre-freeze evidence gate** (`gauntlet:102-111`, referenced by `router:25`) is a real tandem boundary with no helix row.
5. Missing pairing: write-goal hands to "independent verification (e.g. evidence-locked-uat…, gauntlet…)" (`write-goal:21`), but helix pairs write-goal only *before* execution (`:41`) — nothing covers the goal-end verification pair.
6. No missing-member degradation rule.
7. Reason-quality asymmetry with gauntlet's cited-evidence skip bar (`:57` vs `gauntlet:147-148`).

### 6. Minimal improvement proposals (one focused PR each)

- **PR H1:** Formalize `helix-check` minimally — one grammar line plus reason classes for skips plus one sentence naming a sink (run notes / plan artifact). ~3 lines.
- **PR H2:** Fix trigger narrowing by *pointing* instead of restating: rows at `:40` and `:45` should read "per gauntlet's own trigger list" rather than a subset. One-line edits; removes the drift surface instead of widening the copy.
- **PR H3:** `:62-63` — reference blindspot-pass's skip gate by name ("trigger absent *per blindspot-pass's skip gate*"). One clause.
- **PR H4:** Add one cross-cutting clause to the evidence-research row (`:39`): "also feeds gauntlet's Step-0 pre-freeze evidence gate when scholarly evidence is material."
- **PR H5:** One-line degradation rule: if the paired skill is absent, say so and proceed with the workflow stage, flagging the missing epistemic check.

---

## Collection-wide synthesis for the trust contract

- **Only two skills emit machine-checkable artifacts today:** gauntlet (run directory, `selection.json` replay records, `runs/ledger.jsonl` — `gauntlet:123-130,174-184,365-374`) and evidence-locked-uat (`gate.json` + `manifest.json` with sha256 — `evidence-locked-uat:56-64`). The four upstream skills emit prose. A trust contract therefore has to start by pinning artifact shapes at the router's handoff table (PR R2) — the table already exists and is the natural home.
- **Cleanly attestable (idempotent-mechanical):** whether a skill ran; run order (epistemic-first); subject identity via content hash (gauntlet's frozen dossier, UAT's pinned commit SHA at `evidence-locked-uat:64`); consent facts (write-goal); mechanical evidence re-verification against a *frozen* dossier (`verify_evidence.py`, `gauntlet:263-292`) — attestable when hash-bound to that dossier.
- **Never attestable (must re-run or carry validity windows):** premise freshness (gauntlet Step 0), reception freshness (evidence-research "live this run"), environment reachability (UAT `BLOCKED_ENVIRONMENT`), verdict independence (lens isolation, blinded verifier, actor ≠ judge). The contract's job for these is to carry *provenance metadata* — what was checked, when, by whom, to what level, against which subject hash — so downstream skills assess **adequacy** instead of either re-running everything or trusting everything.
- **Design rule the audit supports:** attest *identity, well-formedness, and provenance*; never attest *freshness or judgment*. Both defects found in helix (trigger narrowing, skip-gate softening) are instances of the same underlying hazard — a restated guard arriving weaker downstream than it was at the source. A trust contract that copies *verdicts* instead of *references to artifacts* would industrialize that hazard.
- **Guard against maximal ritual (invariant 1):** every proposal above is a one-to-five-line edit to an existing file. The trust contract itself should start as a line format (`helix-check` upgrade, PR H1) plus an artifact-shape note (PR R2) — not a new schema, file format, or service. The collection's own evidence (UAT's manifest, gauntlet's replay records) shows the minimal shape already works where it exists.

**One ambiguity flagged:** the router's prose says "These **six** disciplines" (`router:8`) — correct as written, but the README skill table (`README.md:29-38`) and arc diagram (`README.md:17-23`) omit helix from the arc entirely; arguably correct as-is since helix is not a discipline.
