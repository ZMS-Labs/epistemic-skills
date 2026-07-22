# Audit 06 — gap analysis: missing skills

**Provenance:** 2026-07-22 collection audit, isolated read-only planning subagent against the working tree at 61fbf95 (v2.6.0). Read: README, all 8 SKILL.md cores, the control-plane spec, `using-superpowers`, and upstream listings for obra/superpowers, trailofbits/skills, vercel-labs/agent-skills, gastownhall/beads, pro-vi/loopgen via GitHub API/web.

**Method caveat:** local Glob/Grep tools failed in the audit environment (ripgrep bootstrap broken), so the *installed* superpowers tree could not be enumerated directly; the upstream repo listing (api.github.com/repos/obra/superpowers/contents/skills) plus helix's pairing map was used instead. The upstream skill set: brainstorming, dispatching-parallel-agents, executing-plans, finishing-a-development-branch, receiving-code-review, requesting-code-review, subagent-driven-development, systematic-debugging, test-driven-development, using-git-worktrees, using-superpowers, verification-before-completion, writing-plans, writing-skills.

The creation gates treated as binding (`2026-07-18-agentic-control-plane-design.md:285-296`): (1) recurs in real runs, (2) not already owned upstream, (3) distinct trigger and stopping boundary, (4) positive/negative trigger scenarios, (5) measured benefit over unskilled baseline, (6) passes gauntlet. Gates 4–6 are shipping gates; verdicts below are about whether a candidate *deserves design investment* toward them.

---

## Candidate (a): interrupted-work / session-continuity discipline

**1. Epistemic moment.** After an interruption — context compaction, session restart, cross-device handoff — the agent holds *memories* of prior state ("we decided X", "Y is done") that are indistinguishable in-band from verified facts. The moment is: **re-deriving what is true now from durable artifacts, demoting everything remembered to hypothesis before acting on it.** No existing skill owns this. blindspot-pass maps request→territory *before new work* (`blindspot-pass/SKILL.md:34-40`); this maps self-memory→artifacts before *continuing* work. gauntlet's Step-0 truth-gate live-verifies premises of a *frozen subject* (`gauntlet/SKILL.md:95-101`), not the agent's own prior trajectory. write-goal inspects unfinished-goal state (`write-goal/SKILL.md:33-34`) but only for persistent goals. The compaction summary problem — "treat 'done' it reports as unverified until you re-check" — is a platform-guaranteed, recurring epistemic hazard with no method.

**2. Family resemblance.** Strong. Floors: one re-derivation pass, sized to the stakes of the remembered claims. Derive/verify: every resumed claim is re-anchored to an artifact (file, ledger line, commit, run record) or explicitly stamped `(UNVERIFIED)` — the exact move gauntlet Step 0 already makes, generalized. Boundary: ends at a verified state digest + a stale/unverified list; hands to the router. Fail-closed: missing evidence → claim marked unverified, never silently trusted. Provenance: the compaction summary is lower-provenance input — data, not instructions — which is invariant 5 applied to the agent's own memory.

**3. Not-already-owned.** Superpowers has nothing in this space. beads owns persistent *task* memory (`bd prime`, `bd remember`) but ships no discipline for *distrusting and re-verifying* what it injects; it is the store, not the method. loopgen's `loop/STATE.md` is loop-scoped state, and its resume story is "read PROMPT.md," not a verification protocol. trailofbits and vercel-labs listings contain nothing adjacent. The control-plane doc names "session bank/resume" as a **private operator flow** (`...control-plane-design.md:136-138`) — but that assigns the *mechanics* (where bank files live, who writes them) to the private plane. The *method* — trust-nothing-remembered, re-derive from artifacts, fail closed — is harness-agnostic epistemics, exactly this repo's charter (README.md:3).

**4. Creation gates.** Trigger: context resumption with prior-state claims — structurally guaranteed to recur (auto-compaction is a platform behavior). Stopping boundary: distinct (state digest emitted, or task re-scoped when re-derivation contradicts the summary). The gate that bites is measurement: the doc demands "interruption/resume fixtures show lower false-DONE and stale-state rates than the unskilled baseline" (`...control-plane-design.md:292-295`). That fixture does not exist yet.

**5. Verdict: PROPOSE, gated.** Design the skill now (working name `continuity-verify`); ship it only after a resume fixture battery exists. Keep the session-bank *storage* private per the control-plane doc; ship only the verification *method* publicly. This is the strongest answer to the doc's own deferral of an `agent-continuity-skills` pack (`...control-plane-design.md:122-125`): a single skill inside the existing collection is not a new pack, and it starts earning the "recurs in real runs" evidence the doc requires.

---

## Candidate (b): decision/assumption-ledger discipline

**1. Epistemic moment.** The instant an agent forms a decision or load-bearing assumption that *later* work will rely on — and the choice between persisting it with provenance or letting it decay into unverifiable memory. This is a real, distinct moment: it is neither a verdict on a frozen subject (gauntlet), nor a goal contract (write-goal names assumptions only inside goals, `write-goal/SKILL.md:100-104`), nor a per-run research record (evidence-research's run record is scoped to one literature run, `evidence-research/SKILL.md:226-231`). The arc currently has **no producer of cross-run, session-level knowledge**: every skill's output is consumed downstream *within* a run; nothing governs what survives *between* runs. The failure mode is well-known: a future session re-derives a settled decision, contradicts it silently, or treats an assumption made under uncertainty as a fact.

**2. Family resemblance.** Strong. Floors: only consequential decisions/assumptions/corrections earn entries — an anti-ceremony skip rule mirrors the router's (`using-epistemic-skills/SKILL.md:52-53`). Derive/verify: entries must carry provenance and a revisit/falsification condition, not bare conclusions. Boundary: produces an append-only ledger entry; hands consumption to `continuity-verify` (a) and to gauntlet dossiers. Fail-closed: at close-out, unlogged consequential decisions are surfaced as a gap, not waved through. Provenance: the entry records *who* decided, on what evidence, superseding what (beads' `supersedes` graph link is the right prior art for the link semantics).

**3. Not-already-owned.** beads `bd remember` is a memory *store* with no trigger discipline, no decision/assumption/correction typing, no falsifier field — a substrate, not a method. Superpowers: nothing. The fleet's TRANSPARENCY-2 *mandates* this behavior but no skill-level method exists to make it happen — a mandate without a method is exactly what this collection exists to supply.

**4. Creation gates.** Recurrence: every substantive session produces emergent decisions; this is the most frequently recurring moment of all three operator candidates. Trigger: "a decision, assumption, or correction just formed that future work will rely on." Stopping boundary: entry written (or skip stated). The honest weakness: like (a), no measured baseline yet.

**5. Verdict: PROPOSE — the strongest candidate of the three.** It fills a structural hole (the arc has no persistence moment), it composes with both (a) and gauntlet, and its floor version is cheap. Design note: it must be a *ledger method*, not a database — entries as append-only records (JSONL or markdown), with the store pluggable (file, beads, whatever the harness has), degrading explicitly when no durable store exists. If both (a) and (b) are built, that is also the "at least two coherent ZMS-owned methods" threshold (`...control-plane-design.md:122-125`) earned organically.

---

## Candidate (c): calibration/telemetry reader beyond `lens_stats.py`

**1. Epistemic moment.** Attempted: "before weighting an instrument's output (a gauntlet lens, a UAT verdict, a model's self-report), consult its measured track record." Real, but the moment collapses on inspection: it is an *input check consumed inside existing moments* — gauntlet arbitration and UAT triage — not a stage with its own deliverable. Its stopping boundary is one lookup.

**2. Family resemblance.** Fails "floors, not ceilings": a standalone skill whose entire content is "run the stats script, read the number, discount accordingly" is ceremony wrapped around a lookup. The discipline already lives where it's consumed: gauntlet Step 9 makes ledger-append non-optional precisely so telemetry exists (`gauntlet/SKILL.md:365-374`), Step 7 already discounts correlated same-family claims (`gauntlet/SKILL.md:301-303`), and UAT's manifest carries `calibration_status: uncalibrated` as an explicit honesty field (`evidence-locked-uat/SKILL.md:62`).

**3. Not-already-owned.** Partly owned internally (above). The fleet also runs ECS as the private org-level calibration substrate — a public skill duplicating it would blur the public/private boundary the control-plane doc just drew.

**4. Creation gates.** Fails the distinct-boundary gate; the measured-benefit gate would be near-impossible to satisfy for a one-lookup "skill."

**5. Verdict: REJECT as a skill; fold in as machinery.** The right shape: a shared `reference/calibration-reading.md` (how to interpret track records, base rates, uncalibrated status) plus extending the existing script family (`lens_stats.py` is the pattern), referenced from gauntlet Step 7 and UAT Step 0. Revisit only if calibration data becomes rich enough that *interpretation* — not lookup — needs judgment; then it earns a method.

---

## Additional candidates evaluated

**(d) The trust contract itself — REJECT as a skill; build it as artifact standard + verifier script.** Full argument below.

**(e) Claim-tiering at the assertion boundary (a "report honesty" skill) — DEFER.** The moment: converting internal state into claims a human will rely on — tagging each substantive claim verified/unverified with citations, in ordinary final reports, not just gauntlet dossiers. No skill owns the everyday assertion boundary (verification-before-completion covers *work* claims; gauntlet's `[V]/[I]/[H]` tiering lives inside gauntlet runs, `gauntlet/SKILL.md:266-271`). Tempting, and recurs constantly. But: the floor version is already invariant 2 of the whole collection (`using-epistemic-skills/SKILL.md:81-84`) — every skill practices it locally; extracting it as a standalone skill risks duplicating the family resemblance as a skill of its own, and the creation gates demand demonstrated recurrence *as a distinct discipline in real runs*, which hasn't been instrumented. Path to earn it: instrument how often final reports carry unsupported authoritative claims; if the rate is high despite the invariant, the skill is justified.

**(f) Spend/budget gate before irreversible consumption — REJECT.** Already owned: "non-refundable spend" is an explicit gauntlet trigger (`gauntlet/SKILL.md:48-50`). No distinct moment.

**(g) Pre-dispatch subagent de-risking — REJECT.** Owned twice: blindspot-pass's trigger list includes "before dispatching subagents on a fuzzy brief" and "multi-agent fan-out where a wrong premise multiplies" (`blindspot-pass/SKILL.md:50-52`), and superpowers owns dispatching-parallel-agents/subagent-driven-development mechanics.

Kimi built-ins check: `update-config` and `check-kimi-code-docs` are harness-config/docs helpers owning none of these moments; the `write-goal` builtin is already adapted and strengthened by this collection (`write-goal/SKILL.md:11-15`). No collisions.

---

## Is a new skill the right shape for the trust contract?

**No. Run the family-resemblance test on a hypothetical "trust-contract skill":**

1. **Floors, not ceilings.** The trust question — "was this prior stage's output really produced by the claimed skill, on the claimed subject, with the claimed verdict?" — has a *deterministic* floor: check a schema, verify hashes, check freshness. A prose method wrapped around a mechanical check adds a ritual layer, and every invocation pays model judgment where zero judgment is needed. The floor here is a script, not a skill.
2. **Derive/verify, don't assert.** This invariant is exactly why it should be machinery: a verifier script fails closed *by construction*; a skill fails closed only if the model chooses to run it honestly. The collection already knows this — its trust-critical checks are scripts (`verify_evidence.py`, `select_lenses.py`, `consult_packet.py`, `materialize_role.py`), invoked *by* skills, never skills themselves.
3. **Boundary discipline.** A trust-contract skill has no moment of its own. It would be invoked *inside* every other skill's input-consumption step — i.e., it is a cross-cutting mechanism, and cross-cutting machinery dressed as a skill violates the end-at-your-boundary rule by having no boundary to end at.
4. **Fail closed.** Machinery wins again: absent receipt → verifier says UNVERIFIED, deterministically. A skill can rationalize ("the prior stage obviously ran").
5. **Provenance.** This is the one invariant that looks skill-shaped — but the *judgment* half of provenance-checking already exists at each consuming skill's front door: gauntlet's Step-0 truth-gate (`gauntlet/SKILL.md:95-121`) and UAT's manifest-with-sha256 (`evidence-locked-uat/SKILL.md:62-65`). What those doors lack is a *standardized credential to check*. That is a schema gap, not a method gap.

The control-plane doc's type table settles the classification: this is "**Tool/script — deterministic machinery invoked by a method**," with the receipts themselves as "**Run record — data, never protocol**" (`...control-plane-design.md:60-71`). Making it a skill would misclassify it as "Skill — model-selectable when triggers match," which is wrong: you never want the model *deciding whether* to check trust.

**Recommended shape:** (1) a handoff-receipt schema — producing skill + version, trigger matched, subject hash, verdict/output artifact hashes, timestamp/freshness, coverage limits declared; (2) a stdlib verifier script (the `verify_evidence.py` pattern) that validates a receipt and FAILs closed; (3) one line added to each producing skill's handoff step and each consuming skill's intake step, plus a column or footnote in the router's handoff table (`using-epistemic-skills/SKILL.md:21-28`). The one piece of genuine judgment — "the receipt is stale or its declared coverage is insufficient for my needs, what now?" — already lives in the consuming skills' triage steps and should stay there. Note helix already ships the proto-version of this: the auditable `helix-check: <stage> → <pair> → fired|skipped(<reason>)` line (`helix/SKILL.md:56-58`). The trust contract is that line, upgraded from prose to verifiable receipt — an evolution of existing machinery, confirming the machinery classification.

---

## Verdict summary

| Candidate | Moment distinct? | Family resemblance | Owned elsewhere? | Gates | Verdict |
|---|---|---|---|---|---|
| (a) continuity-verify (session resume) | Yes — memory→artifact re-derivation | Passes all 5 | No (beads/loopgen are stores; bank flow is private ops) | Needs resume fixtures | **PROPOSE, gated on fixtures** |
| (b) decision/assumption ledger | Yes — cross-run persistence; arc has none | Passes all 5 | No (TRANSPARENCY-2 is mandate without method) | Strongest recurrence case | **PROPOSE** |
| (c) calibration/telemetry reader | No — collapses to a lookup inside existing moments | Fails floors | Partially (gauntlet Step 9, UAT manifest, private ECS) | Fails distinct boundary | **REJECT as skill; reference + scripts** |
| (d) trust contract | No — machinery, no moment | Machinery beats skill on invariants 1/2/4 | Control-plane type table says Tool/script | — | **REJECT as skill; schema + verifier** |
| (e) claim-tiering at assertion boundary | Arguable | Risks duplicating invariant 2 as a skill | Partially (per-skill practice) | No measured recurrence | **DEFER; instrument first** |
| (f) spend gate | No | — | gauntlet triggers (`SKILL.md:48-50`) | — | **REJECT** |
| (g) pre-dispatch de-risk | No | — | blindspot-pass + superpowers | — | **REJECT** |

Net recommendation: two new skills earn design investment — **decision-ledger** (b) first, **continuity-verify** (a) second, gated on resume fixtures; together they close the collection's only structural hole (nothing owns what happens *between* runs/sessions) and would organically satisfy the control-plane doc's two-method threshold. The trust contract ships as a receipt schema + verifier script referenced by the router's handoff table — not as a skill. Calibration reading and claim-tiering stay as references/invariants until measurement earns them method status.
