# Audit 04 — gauntlet

**Provenance:** 2026-07-22 collection audit, isolated read-only subagent against the working tree at HEAD 61fbf95 (v2.6.0; registry sha256 8224ac4a…, 102 entries: 67 active / 5 probation / 24 candidate / 6 retired — computed, not asserted). Base: `plugins/epistemic-skills/skills/gauntlet/` (all paths below relative to it unless noted).

---

## 1. Boundary/handoff contract as it exists today

**Consumes** — a *frozen verified dossier* plus a locked subject. Step 0 (SKILL.md:95-121) live-verifies premises, freezes `dossier.md` with uncertainty labels; Step 1 (SKILL.md:132-139) locks subject path/revision/scope/exclusions and the evidence root, with the invalidation rule "If the subject moves, restart" (SKILL.md:138). The collection router's handoff table states the interface formally: gauntlet consumes "a **frozen** subject (a de-risked request, a derived verdict, or an evidence matrix)" (`using-epistemic-skills/SKILL.md:28`).

**Produces** — computed GO/CONDITIONAL/NO-GO from the P1/P2 gate (SKILL.md:347-348), a dissent-preserving Conflict Ledger (SKILL.md:302-303), a GO coverage statement (SKILL.md:352-356), and an append-only run directory + one `runs/ledger.jsonl` line (SKILL.md:365-374).

**Hands to** — "the commit / merge decision" (`using-epistemic-skills/SKILL.md:28`), with explicit downstream semantics: a CONDITIONAL's open P2s are *blocking follow-ups*, not resolved items (SKILL.md:357-358); external infra safety gates are reconciled, never satisfied, by this skill (SKILL.md:35, 349-352).

**Machine-readable artifacts already present (the trust-contract exemplars):**

| Artifact | Where defined | Attestation property |
|---|---|---|
| `option-set@1` / `finding-set@1` / `ruling-set@1` | `reference/lens-registry.md:42-49` | Structured falsifier `{statement, method, threshold, timeframe}` schema-enforced at the tool layer (`assets/gauntlet-workflow.template.js:36-70`) |
| `gauntlet-role-binding@1` | `reference/runtime-role-binding.md:12`; `scripts/materialize_role.py` | SHA-256 of role source, persona, dossier, and composed prompt — replayable proof of *what was dispatched* |
| Selector replay record | `scripts/select_lenses.py:372-380` | registry_version + sha256 + subject vector + scores + exclusions + `selected_ids@versions`; selector is deterministic stdlib ("Same input => same output", docstring line 4) → third-party re-runnable |
| `runs/ledger.jsonl` schema | `runs/README.md:14-55` | Per-run: depth, verdict, registry_sha256, eligible flag, per-lens upheld/dup/overruled/unsupported/false_high, `seat: core|exploration` |
| `runs/adjudications.jsonl` | `runs/README.md:58-65`; `scripts/consult_packet.py` | Deterministic `request_id`; DISSENT → `ESCALATE-TO-SOVEREIGN`, never a verdict rewrite |
| Sovereign Fingerprint JSON | `scripts/verify_evidence.py:242-248` (`--json`) | Per-report verified/hallucinated/accuracy + per-tag results |

The pattern these share — *content hash + deterministic regenerator + replay record* — is exactly what a cross-skill trust contract should generalize.

---

## 2. Findings vs the five invariants

**1. Floors, not ceilings**
- STRENGTH: triage-before-engine cost model (SKILL.md:57-63); triage skip with cited-evidence reason format (SKILL.md:143-148, 376-380).
- STRENGTH: P3/P4 findings need only a one-line falsifier — "full structured falsifiers on minor observations generate boilerplate, not testability" (SKILL.md:272-274).
- STRENGTH: the selector's fit-scoring layer is FROZEN with a comment recording that it showed *no benefit over random fill* and refusing added sophistication (`scripts/select_lenses.py:64-67`); panel sizes were *reduced* on saturation evidence (SKILL.md:69-71). This is the invariant self-applied, with receipts.
- STRENGTH: lifecycle thresholds are review triggers, never automatic actions (`reference/lens-registry.md:76-79`).

**2. Derive/verify, don't assert**
- STRENGTH: `[V]` certifies source anchoring, *not* proposition truth (SKILL.md:267-270); oracle-adequacy check with planted-positive control requirement (SKILL.md:277-292).
- STRENGTH: `verify_evidence.py` fails closed on binary files cited by line (`scripts/verify_evidence.py:101-115`), with a regression test that includes a *positive* control so the guard can't pass by rejecting everything (`tests/run_tests.py:234-265`).
- DEFECT: `reference/lens-registry.md:131` asserts "**30 core candidates**" — the registry contains 24 (generated `roster/INDEX.md:13`; computed count 24). A hand-maintained count in the very document that decrees "Counts live in one place: roster/INDEX.md" (lens-registry.md:6). Self-violating drift.
- DEFECT: `reference/lens-registry.md:94` and `tests/run_tests.py:10` both point to `evals/README.md` for the behavioral admission battery — **that file does not exist**; `evals/` ships only `arbitrator-certification/` (verified via `git ls-files`). The admission gate for all 24 candidates is specified in a missing document.
- DEFECT: `reference/roadmap.md:69` cites the design doc `docs/superpowers/specs/2026-07-07-gauntlet-staple-deepreason-integration-design.md` — absent from the repo (that specs dir holds four other files). "The operator's copy" is private; the pointer is dead for any public reader.
- GAP: SKILL.md:426 calls the behavioral battery "designed, NOT run" at `evals/` — but no battery design files ship at all, and the smoke-run notes are explicitly *not* in the package (SKILL.md:404-405; README.md:177). The non-inferiority claim is unverifiable from the artifact. Honestly hedged, but the pointer overstates what `evals/` contains.
- GAP: `[I]` inference anchors are "spot-checked by the arbitrator" (`scripts/verify_evidence.py:35`), not mechanically checked — a documented soft spot in the mechanical layer.

**3. Boundary discipline**
- STRENGTH: the relation table (SKILL.md:29-39) and DeepReason role boundary (`reference/deepreason-integration.md:16-22`) are crisp: DeepReason never sets GO/NO-GO, never satisfies the external red-team gate; Step 7b's external read "never mechanically overrides" the verdict (SKILL.md:340-343); the shadow lens never touches the decision (SKILL.md:201-205).
- STRENGTH: `reference/consensus-integration.md` is a fully-worked handoff contract (freeze semantics, no ad hoc re-search, controlled reopen procedure at lines 40-49) — the best in-repo model of a trust boundary.
- GAP: the CONDITIONAL handoff is prose-only. The P2 conditions that downstream stages must treat as blocking (SKILL.md:357-358) live in a free-text template field (`assets/synthesis-template.md:17`), not in any machine-readable artifact — a downstream skill cannot *mechanically* consume them.

**4. Fail closed; degrade explicitly**
- STRENGTH: "Oracles FAIL CLOSED (non-negotiable)" with the two mandatory guards — tool-existence check and oracle-medium matching (SKILL.md:283-292); selector constraint violations are hard errors (SKILL.md:186); abort when the subject isn't establishable in truth (SKILL.md:99-100); stop the panel if no role binding is possible (SKILL.md:248); `orchestration: manual-degraded` must be disclosed (SKILL.md:255).
- DEFECT: shadow-seat rotation **fails open on missing telemetry**. `ledger_seat_counts` returns `{}` on a missing/corrupt ledger (`scripts/select_lenses.py:230-235`, comment "Missing/bad ledger => {}"), and rotation then tie-breaks by lens id (`select_lenses.py:284`) — silently seating the alphabetically-first probation lens every run and starving the rest. Silent degrade, exactly the invariant-4 pattern. (Live right now: see §5.1 — the shipped ledger is empty.)
- GAP: `verify_evidence.py` exits 0 "regardless of accuracy" (docstring lines 18-20) and nothing mechanically gates arbitration on the fingerprint — enforcement of "accepted claims require [V]/[I]" (SKILL.md:270) is procedural except inside the Workflow template. Acceptable at the contract level, but worth naming.

**5. Provenance and independence**
- STRENGTH: Step 0(6) injection guard — subject text is data; evidence-tag mimicry and reviewer-addressed text are themselves findings (SKILL.md:117-118); the materializer appends an explicit injection boundary (`reference/runtime-role-binding.md:42-43`).
- STRENGTH: the independence barrier is the stated source of value, with the "never a team" rule and the single bounded-reinstatement exception (SKILL.md:251-253; `reference/execution-model.md:67-78`); shadow reports are withheld from the arbitrator (SKILL.md:230-232); correlated same-family claims count as ONE claim (SKILL.md:301-302); the external adjudicator is asked to *attack* the verdict, not restate it (SKILL.md:329-330).
- GAP: model-family separation between judge and lenses is "when configurable" (SKILL.md:215-216) and enforced by the arbitrator *self-reporting* family sharing (`reference/execution-model.md:60-61`) — the actor grading its own provenance. Weak but disclosed.

---

## 3. Duplicated checks across the collection

**(a) Step 0 truth-gate live-verification vs blindspot-pass recon.**
Gauntlet: "live-verify every premise via probe/API/file read — NOT session memory or prior summaries" (SKILL.md:97-98). Blindspot-pass: "Live-verify anything the brief *asserts* about the territory" (`blindspot-pass/SKILL.md:73-74`). The two even share a near-verbatim sentence — gauntlet Step 1 "If the environment is degraded (a mount down, a mirror stale), verify the source-of-truth" (SKILL.md:138-139) vs blindspot-pass step 1 (line 74-75).
**Classification: freshness-sensitive.** Blindspot-pass runs at task start; the gauntlet gates a later, possibly-moved subject. The "NOT session memory" clause is deliberate freshness design. A trust contract may let Step 0 *consume* the blindspot output as leads, but must never treat it as a substitute verification. Any proposal that lets an upstream recon "attest" Step 0 would silently defeat it — flag this as the single most dangerous trust-contract failure mode. The correct attestation unit is the *frozen dossier itself* (freeze timestamp + subject revision), not the verification act.

**(b) Step 0 scholarly-evidence gate vs evidence-research.**
Gauntlet delegates wholesale: use evidence-research, attach its claim-evidence matrix + run record, preserve verification levels, lenses "perform no ad hoc Consensus searches" afterward (SKILL.md:101-111; `reference/consensus-integration.md`). Evidence-research produces exactly that artifact as its boundary (`evidence-research/SKILL.md:39`).
**Classification: idempotent-with-provenance — safe to attest once.** This is already an informal trust contract and the best one in the collection. One freshness caveat: reception/retraction status drifts over time (evidence-research itself plans at-rest re-checks, `evidence-research/SKILL.md:22`), and gauntlet already handles it via the controlled dossier reopen (SKILL.md:109-111) — so the attestation must carry the run record's timestamp and remain reopenable, never sealed.

**(c) Step 6 oracle-adequacy vs verification-before-completion (superpowers) and evidence-locked-uat.**
Gauntlet Step 6(3) (SKILL.md:277-292) judges claims *about* verification (mocked oracle, can't-fail test, green-for-unrelated-reasons). Evidence-locked-uat judges work-done claims with a deterministic judge and a blinded verifier (`evidence-locked-uat/SKILL.md:11-12, 59-61, 71-72`).
**Classification: doctrinal overlap, not operational duplication.** Different subjects (lens reports vs finished UI work), different times (pre-commit gate vs post-work proof). The *doctrine* (fail-closed oracles, planted-positive controls, never-round-up verdicts) is genuinely duplicated and could be cited rather than restated — but the checks themselves should not be attested across. One mechanical piece *is* idempotent and attestable: a `verify_evidence.py` run is deterministic given (report content, evidence-root content) — safe to attest once **only if** the attestation binds an evidence-root content hash. Today Step 1 establishes the evidence root as a *path* (SKILL.md:135-136) with no content pin, so a `[V path:line]` verification silently invalidates if the file changes later. That pin is the missing piece, not a re-run.

---

## 4. Trust-contract readiness

**Already attestable today (hash-stamped, replayable):**
- Panel selection: registry sha256 + subject vector + deterministic selector → replay record is independently re-runnable (`select_lenses.py:372-380`, 442-461; self-test proves determinism at lines 412-417).
- Role dispatch: `gauntlet-role-binding@1` binds role/persona/dossier/prompt hashes — proof of exactly what each lens was told (`runtime-role-binding.md:12, 40-42`; regression-tested, `tests/run_tests.py:268-316`).
- External adjudication: deterministic `request_id` + append-only record with escalate-never-override semantics (SKILL.md:322, 336-343).
- Verdict *gate*: P1→NO-GO / P2-open→CONDITIONAL / else GO is mechanical (SKILL.md:347-348) — but only downstream of the arbitrator's ruling-set, which is judgment. Attest "verdict computed from ruling-set@1 X", not "verdict correct".

**What a run record needs to be a trusted downstream input (all small):**
1. A **run manifest** (one JSON): dossier sha256 + freeze timestamp, subject path/revision, evidence-root content pin, selection replay hash, per-lens report hashes, fingerprint JSON ref, ruling-set ref, verdict + conditions array, depth, `docket_mode`, `independence_mode`, `role_binding` mode. Today these are scattered files and prose fields; Step 8 requires recording the last three (SKILL.md:362-363) with no schema and no home in the synthesis template.
2. **Structured conditions** on CONDITIONAL verdicts (the blocking P2s as a JSON array, not template prose) so downstream stages can mechanically refuse to treat CONDITIONAL as GO.
3. **An explicit invalidation rule in the manifest**: valid only while subject revision and evidence-root pin match — codifying the existing prose rule "If the subject moves, restart" (SKILL.md:138).

**What must never be attested:**
- *Lens independence/blindness for a given run.* The barrier is procedural; `independence_mode` is self-reported by the orchestrator. Attesting "the lenses didn't see each other" as fact would make the actor the judge of its own work (invariant 5). The arbitrator-certification battery (10/10, `evals/arbitrator-certification/results-2026-07-17.md`) certifies the role *design*, not any run. Downstream may rely on "run conducted under contract C", never on "independence achieved".
- *Step 0 freshness as a durable fact.* A dossier attestation must expire with subject drift; a "premises verified" stamp that outlives its freeze timestamp is exactly the session-memory substitution SKILL.md:97-98 forbids.
- *Verdict authority across skills.* A gauntlet GO must remain advisory input to a human/external gate decision (SKILL.md:349-352 keeps the external gate separate); a trust contract that lets a downstream stage auto-execute on an upstream GO recreates the over-trust failure the boundary discipline exists to prevent. Likewise, shadow-seat findings must stay excluded from any attested verdict content (`reference/lens-registry.md:69-72`).

---

## 5. Unfinished-feeling items — beyond the roadmap's self-report

The self-report (Phases 1-3 unbuilt, smoke-only battery, arbitrator certified) is **accurate as far as it goes**. What it does not say:

1. **The telemetry system shipped empty, and its only real data was deleted.** `runs/ledger.jsonl` is 0 bytes and `runs/adjudications.jsonl` is 0 bytes. Git history shows commit `2807896` (2026-07-20) recorded two genuine runs (PenEcho CONDITIONAL, fo-standards NO-GO — schema-conformant, including probation exploration seats) and the full run directory; commit `1d22614` ("hygiene: remove/scrub fleet-internal topology references", 2026-07-21) zeroed the ledger and removed the run directory because the subjects were private infrastructure. Consequences: (a) the entire lens-lifecycle machinery — rotation-balanced shadow seating, the 20-run activation trigger, deprecation flags, `lens_stats.py` — has never operated on shipped data; (b) the two probation lenses that had earned real track records (`concurrency-interleaving-auditor`: 3 unique-upheld; `effective-configuration-auditor`: 0) lost them in the public package; (c) there is no mechanism separating public schema from private telemetry, so the next live run on a private subject recreates the same scrub-or-leak dilemma. This is the single largest contributor to the "unfinished" feeling: a non-optional Step 9 feeding a lifecycle that has zero observable life.
2. **The admission gate's defining document is missing.** `evals/README.md` is referenced as the spec for the only path by which any of the 24 candidates can ever be promoted (`reference/lens-registry.md:89-94`), and it does not exist. The candidates are permanently frozen until that doc ships.
3. **The behavioral battery is not even *designed* in the public package**, despite SKILL.md:426 labeling `evals/` as "Behavioral eval battery (designed, NOT run)". Only the arbitrator-certification battery ships. The roadmap's honest-status block (SKILL.md:401-406) admits the smoke-only status but not the absence of design files.
4. **Doc drift contradicting the registry** — "30 core candidates" vs actual 24 (`reference/lens-registry.md:131`).
5. **Dead provenance pointer** — the Phase-design doc cited at `reference/roadmap.md:69` is not in the repo.
6. **The synthesis template predates its own requirements.** `assets/synthesis-template.md` has no fields for the GO coverage statement mandated 2026-07-14 (SKILL.md:352-356: capability families exercised, known unknowns, evidence freshness, residual uncertainty), no `docket_mode`/`independence_mode`/`role_binding` fields though Step 8 requires recording them (SKILL.md:362-363), its depth enum omits `max` (line 10), and its "Consensus Result" field name (line 14) now collides confusingly with the Consensus scholarly-evidence integration. A required artifact with no home is a fail-open by omission.
7. **No worked example ships.** With the PenEcho run scrubbed, a new user has no sample dossier, `selection.json`, lens report, or summary to imitate — every artifact shape must be inferred from prose.
8. **Deep mode's engine dependency is unpinned.** `reference/deep-mode-mcp.md:7` installs DeepReason from a bare git URL with no commit/tag pin, and `config/operator.yaml` pins `gpt-4.1`-era endpoints — a mutable external reference at the root of the "replayable, meter==log" guarantee (SKILL.md:154-157). If the engine drifts, replay breaks silently.
9. Minor: `verify_evidence.py`'s `[I]`-anchor check is arbitrator-spot-checked, not mechanical (`scripts/verify_evidence.py:35`) — disclosed in code, not in SKILL.md.

(Non-finding, checked and cleared: `scripts/__pycache__/*.pyc` present in the working tree is gitignored and untracked — local noise, not shipped.)

---

## 6. Minimal improvement proposals (each one focused PR)

1. **Ship a synthetic example run.** Add `examples/example-run/` with a small fictional subject: dossier, subject.json, selection.json (generated by the actual selector), two lens reports, fingerprint output, arbitration, summary, and *one* schema-conformant ledger line marked `"example": true`. Fixes §5.1(c) partially, §5.7, and gives the trust contract a concrete exemplar — without touching private data. (Not maximal: one run, standard depth.)
2. **Separate telemetry from package.** Move the live ledger's canonical home out of the shipped skill tree (e.g. a user-state path), have `select_lenses.py` read an explicit `--ledger` path, and make a *missing* ledger print a one-line warning instead of silently returning `{}` (`select_lenses.py:230-235`). Two-line behavior change + doc edit; fixes the fail-open rotation (§2/inv-4) and the scrub recurrence (§5.1).
3. **Add the missing `evals/README.md`** — or, if the admission-gate design isn't ready, change the two references (`reference/lens-registry.md:94`, `tests/run_tests.py:10`) to point at the roadmap and say "unspecified" honestly. Either direction is one file; shipping a broken pointer is the only wrong option.
4. **Fix the three drift items in one hygiene commit**: candidate count 30→24 (`reference/lens-registry.md:131`), dead design-doc pointer (`reference/roadmap.md:69` → point to the private-repo location by name, marked private), and SKILL.md:426's "designed" wording → "battery design not yet shipped".
5. **Update `assets/synthesis-template.md`** to match Step 8 as it exists today: add the GO-coverage-statement block, `docket_mode` / `independence_mode` / `role_binding` Meta fields, `max` in the depth enum, rename "Consensus Result" → "Verdict". Pure template alignment with already-mandated content.
6. **Define `gauntlet-run-record@1`** (the §4 manifest): a JSON schema + a `scripts/finalize_run.py` that hashes the dossier, selection record, reports, and ruling-set into one content-addressed record with a `valid_while: {subject_rev, evidence_root_pin}` field. This is the trust-contract kernel — it generalizes the existing selector-replay/role-binding pattern and adds nothing beyond hashing files that already exist. Explicitly document in its README the three never-attest items (independence, durable freshness, verdict authority).
7. **Pin the DeepReason engine reference** in `reference/deep-mode-mcp.md` (commit SHA or tag in the install line) and note that `config/operator.yaml` model names are examples to verify against current provider offerings. One-line-each edits that protect the replay guarantee.

Nothing above adds ritual; items 1-5 are drift/hygiene repairs, item 6 reuses the hash-and-replay pattern the skill already invented three times, item 7 closes a freshness hole. The strongest evidence that this skill is *not* maximal-ritual cargo is already in its own comments (`select_lenses.py:64-67`) — the audit's job was to confirm the machinery matches the claims, and with the exceptions cited, it does.
