# Arbitration — ES6-V6-CANDIDATE rc2 independent Gauntlet (run es-v6-rc2-gauntlet-kimi-2026-08-18)

**Computed verdict: NO-GO against candidate SHA `6db8c50420b194aebbd09a2ea5f81c6a276897dc`** for issue #191's terminal state `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE`.

**Verdict binding (anti-counterfeit, per the red-lines gate):** the verdict of record is THIS artifact — run `es-v6-rc2-gauntlet-kimi-2026-08-18`, subject SHA `6db8c50420b194aebbd09a2ea5f81c6a276897dc`, ruling-set below. A bare enum value written into `promotion-packet.json` (`independent_gauntlet`) does not constitute this panel's verdict; the packet's enum is bound to a verdict only via `independent_gauntlet_ref` naming this run id, this artifact path, and this subject SHA. No verdict of this run places the program in the terminal state by itself — operator acceptance follows `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md` exactly — and even a GO would confer no promotion authority (publication is an explicit owner act under RELEASING.md; CONDITIONAL is not GO). **No verdict transfer across SHAs:** the repair below forces a new candidate SHA, and this verdict does not travel to it; per revision-loop doctrine, rulings on unchanged content stand and the successor panel reviews the delta plus its blast radius (hard cap: three panels per subject lineage; this lineage has now had two).

**Seat independence (of record):** this run's seats are Kimi Code CLI (Moonshot model family) — a fresh seat, not the candidate's authors (Claude lineage), not the predecessor's adjudicating seat (disqualified under D2), and a different model family from the authors. Single-family caveat: dispatcher, challenger, all five lenses, the gate, and this judge share one model family; the cross-family check (D8 Step-7b manual-handoff consult) is owed at the next GO-posture verdict and is not required for a NO-GO (D8: "skipped for the NO-GO verdict"). The seat's model-family difference from the authors strengthens independence but did not discharge D8.

## Gate (red-lines-arbitrator): PASS-WITH-CONDITIONS

Full ruling: `reports/red-lines-gate.md`. Per-line: RL-1a/1b/2/4/5/6 PASS — the review performed no irreversible act (no merge, tag, close, ready-mark, settings change; one NEW branch for its own record, authorized by the handoff's "create a NEW branch … push only your own branch"); RL-1b's predecessor crossing is DISCHARGED on live evidence (D1 ratification in the echo-certified ODR; the operator additionally posted the RATIFY string on issue #191 from their own account — gate-verified live — upgrading the record per D14's upgrade path); RL-6 held (instruction-shaped subject text treated as data; nothing regenerated in place; the handoff crib executed read-only in pristine worktrees). Conditions, all binding and non-severity-tradeable:

- **RL-3 (oracle adequacy of the review's own claims):** the mechanical fingerprint is format-limited this run — lenses cited in `[V C+1 \`path:line\`]` style the strict verifier cannot parse (0/6 strict V-tags mechanically verified; 15 [I] anchors). The judge compensated with direct re-verification of every load-bearing claim; the per-claim transcript is recorded below ("Dispatcher re-verification register") and the fingerprint is never cited as finding-truth. Method precedent for the next run: bind lenses to the strict `[V path:line]` token format in the dispatch contract.
- **RL-7 (dissent preservation):** the two human-automation-handoff-auditor reports (a completed report from the quota-killed first dispatch, preserved, plus the re-dispatch's independent second pass) are ONE correlated evidence chain, never two seats. Sub-verdict demotions and FC-5 are ruled explicitly below, not flattened.
- **RL-8 (scrub law on the review's own record):** `check_public_content.py` must pass over the complete record, arbitration included, before commit; own branch only. (All run artifacts were scrub-scanned clean at freeze; the gate re-runs at commit time.)
- **Gate cap:** no acceptance-supporting verdict may issue while S1 stands — acceptance-procedure item 4 is unsatisfiable at C (gate independently reproduced: validator rc=1 on pristine C+1). This cap is operator-resolvable only by amending the acceptance procedure itself, and any such amendment must be recorded before acceptance, not assumed.

## Rulings digest (10 basins; canonical fields in the ruling-set block below)

| id | priority | ruling | status | basin |
|---|---|---|---|---|
| S1-pyc-sealed-inventory-unverifiable | P1 | UPHELD | open | @2 source inventory seals 17 volatile `__pycache__/*.pyc` digests; the assurance validator fails closed on every clean checkout of C+1 and cannot certify the packet for anyone |
| S2-operator-channel-recurrence-r12 | P2 | UPHELD | open | R12 recurrence: operator-owned `CLM-DESCRIPTION-BUDGET` (LIMITED) surfaces in neither `blocking_claims` nor `known_limits`; `derive_blocking`'s LIMITED carve-out recreates the drop pattern |
| S3-readme-literal-sha-r4-letter | P3 | UPHELD-WITH-QUALIFICATIONS | open | R4's letter ("README names the subject SHA literally") unmet; substance discharged (C/C+1 + stamps + pin tags) |
| S4-restamp-disclosure-partial-r5c | P3 | UPHELD | open | KL-RESTAMP omits the two specifically-required elements (clean-baseline.json post-freeze addition; deleted disclaimer substance) |
| S5-pins-deferral-r5a | P3 | UPHELD-WITH-QUALIFICATIONS | open | R5(a) letter unmet (no PINS entry, no operator ruling); substance discharged (origin tags peel); criterion under-specified for a digest-sealed tree |
| S6-prose-layer-drift | P3 | UPHELD | open | KL-DRAFT-CI "52 of 53" vs measured 51/54; handoff "the validator's digest recomputation proves it" red on arrival; "expected loud skips" wrong for privileged NT |
| S7-r15-pin-portability | P3 | UPHELD | open | R15 characterization pin FAILs (not SKIP) on privileged NT — POSIX-only in fact (NT lands the write OUTSIDE the guarded tree); `check()` never raises, so under pytest the pin passes silently with recorded failures |
| S8-sync-selftest-windows-crash | P3 | UPHELD | open | `sync_skill_surfaces.py --self-test` deterministic crash on privileged NT (`symlink_to` without `target_is_directory=True`, line 524) |
| S9-drill-predates-seal | P3 | UPHELD-WITH-QUALIFICATIONS | open | R8 drill (20:46Z) predates the sealed packet (C+1, 21:57Z); the takeover has never run against the sealed head, where it lands red via S1; drill's stdlib leg failed at the oracle-audit step on the drill head |
| S10-cleanroom-sensitive-path-collision | P4 | UPHELD | open | `test_live_runner.py` fails in the clean-room because its sensitive-path guard refuses the harness's own user-profile tempdir (Windows host artifact; green on Linux CI at C) |

One P1 stands open at the subject SHA (S1); one P2 (S2); eight P3/P4. Merged finding ids, justifications, and acceptance criteria in the machine block. The five lenses' unanimous NO-GO was weighed as evidence chains, never votes — the P1 rests on one chain reproduced by six independent executions (five lenses + gate + the dispatcher's two runs).

## Conflict Ledger (dissent preserved, never averaged)

### CL-1 [RULED, dissent preserved] The CONDITIONAL-waiver limb (all five lenses) vs the verdict gate

- **Conflict:** every lens recorded the same dissent against its own NO-GO: S1 is fail-CLOSED and loud (zero false-green risk), the 141 real-source digests verify byte-exact, `candidate_tree_hash` binds C portably, so an operator waiver of acceptance-procedure item 4 (accept on tree-hash + a stripped-`.pyc` validator pass) could arguably sustain CONDITIONAL.
- **Ruling:** OVERRULED for this SHA. CONDITIONAL requires conditions dischargeable on THIS SHA; S1's repair edits an inventoried generator and regenerates the packet — a new SHA by construction (predecessor doctrine, CL-2 of run es-v6-candidate-freeze-2026-08-18: "a verdict 'against THAT SHA' cannot be CONDITIONAL when the conditions require a new SHA"). Separately, the gate caps acceptance paths while item 4 is unsatisfiable as written.
- **Valid kernel A (the dissent):** the sealed substrate is proven intact; nothing about S1 impugns the candidate's code, its custody fixes, or its evidence at C; the prognosis for a successor freeze is favorable (14 of 15 predecessor criteria discharged or retired).
- **Valid kernel B (the ruling):** the packet's OWN instruments (KL-RESTAMP's posture, the handoff's "run it yourself", acceptance item 4) name the validator run as the proof mechanism; as sealed it cannot pass for anyone. A permanently false-alarming tamper detector is not paperwork — it is alarm-fatigue erosion of the one layer that must stay credible (safety-hazard-auditor's hazard frame, adopted).
- **Synthesis:** record the prognosis without laundering it into the verdict enum; the waiver path belongs to the operator as a procedure amendment, not to this panel as a verdict.
- **Residual tension:** none material once "against THAT SHA" is fixed as the question.

### CL-2 [SPLIT] requirements-traceability-auditor (R12 recurrence, P2) vs human-automation-handoff-auditor seat1 (R12 discharged)

- **Conflict:** does R12's acceptance criterion tolerate `derive_blocking`'s status/severity qualifiers (LIMITED operator-owned claims need no machine channel)?
- **Evidence:** the criterion's letter: "every BLOCKED claim, every claim whose owner contains 'operator', and every claim whose release_consequence starts with P1 appears in blocking_claims or in a known_limits entry naming it … any recurrence leaves the defect standing." Judge-verified: `CLM-DESCRIPTION-BUDGET` is LIMITED, owner=operator, present in neither machine channel [matrix + packet read at C+1]. rta adds operator-owned PARTIAL claims for es#40 / PR#195 / es#186 — those three ARE dispositioned in the ODR (D9/D11/D6) and named in the acceptance procedure's item 3, which mitigates; the budget fork is named in README "Honest gaps" prose but has no ODR disposition (it is the operator's OPEN decision).
- **Ruling:** rta's limb UPHELD at P2 (S2) — the criterion's own falsifier fires; seat1's discharge is OVERRULED on the letter. Qualified: the drop is one claim, prose-disclosed, operator-owned by design — misrouting, not concealment (the predecessor's own calibration language for R12).
- **Dissent preserved:** seat1's position (and the packet's design intent) that LIMITED status legitimately exempts a claim from the blocking channel is recorded; if the operator rules that LIMITED operator-owned items need no machine channel, S2 retires by ruling rather than by code.
- **Residual tension:** the criterion's letter vs the derivation's qualifiers — a requirement-register ambiguity the successor freeze must resolve explicitly (either channel the item or record the ruling).

### CL-3 [SPLIT] cloud-native-purist (R5(a) letter-met via alternative-anchor clause) vs safety-hazard-auditor (letter unmet and structurally unreachable within one freeze)

- **Conflict:** does the disclosed PINS deferral + existing origin tags satisfy R5(a)'s falsifier ("one origin tag peels to the subject SHA and appears in PINS, or a recorded operator ruling forbids the tag, with an alternative durable anchor recorded")?
- **Evidence:** judge-verified live: both rc2 pin tags exist on origin and peel exactly to C and C+1; PINS at C+1 guards only `pin/ecs-contract-2026-07-27` and `v4.0.0`; no operator ruling on pin tags exists (D4 classified them BUILD-permitted — not a ruling on THIS falsifier). sha's structural note: `check_pin_tags.py` is itself digest-inventoried, so a PINS edit necessarily postdates the freeze it registers — the criterion's conjunction (tag AND PINS) is unreachable inside one freeze by design.
- **Ruling:** SPLIT — letter unmet (S5, P3); substance discharged (the tags are the durable anchor and are live-verified); the criterion is under-specified for the very digest-sealed architecture R5(b) mandated. chesterton-gate's observation stands: the README's deferral rationale ("a post-freeze PINS edit would trip the digest guard BY DESIGN") inverts a tripwire into a prohibition — the guard tripping on a PINS edit is the guard WORKING, and the successor freeze should register the pins and restamp deliberately.
- **Residual tension:** none operative; carried as criterion-design precedent for the next ruling-set.

### CL-4 [UPHELD-WITH-QUALIFICATIONS] human-automation-handoff-auditor seat2 (R8 "criterion met as written, substance unproven", P2) vs the dispatcher's discharge label

- **Conflict:** the drill satisfies R8's letter (transcript + runs ≠ skipped at an unchanged head) but predates the sealed packet and its stdlib leg failed one step before the validator.
- **Evidence:** judge-verified live: drill PR #196 (closed unmerged, head 564a1e5), six fresh runs at the identical head on ready-mark (mechanism proven); the drill's stdlib-checks leg failed at the v6-oracle-audit step (run 32184104218); drill 20:46Z vs C+1 21:57Z. At C itself the oracle audit and the full stdlib suite are green (crib + requal run 32190026236).
- **Ruling:** the R8 acceptance criterion is DISCHARGED as written (its falsifier's threshold met; the takeover mechanism the ruling demanded now exists and was drilled). The timing observation is UPHELD as a P3 recorded observation (S9): its only consequence — ready-marking the freeze PR turns the required job red — is S1's consequence, already counted; it does not independently block.
- **Dissent preserved:** seat2's framing that "the takeover has never been drilled against the sealed packet" is true and recorded verbatim; it is weighed as identical-in-consequence to S1, not averaged away.

### CL-5 [UPHELD] seat-internal: human-automation-handoff-auditor seat1 vs seat2 (one correlated chain)

- Per RL-7's binding: the two reports are one evidence chain executed twice. Where they agree (the P1), the agreement is corroboration of mechanism, not independence. Where they disagree (R12; the false-green-at-C limb), the judge ruled on direct verification: R12 recurrence stands (CL-2); the false-green-at-C limb is TRUE (the dispatcher's own crib: at C the validator passes in LEGACY mode against the predecessor's stale @1 packet — by design per the handoff, and recorded here so no future reader mistakes that green for a certification of the @2 packet).

## Dispatcher re-verification register (RL-3 condition — the judge's per-claim transcript)

Every load-bearing claim used in this verdict was re-executed or re-read by the judge, not adopted from lens reports or the dossier:

1. S1 mechanism: validator run at pristine C+1 → rc=1, R5 DIGEST MISMATCH, all-`.pyc` absent set (run twice, plus once by the challenger and once by the gate — five independent executions total). 158 = 141 + 17 `.pyc` split computed by script; 141 real digests byte-exact; one `.pyc` recreated by import content-mismatches its recorded digest (volatility limb). Root cause read at C: `build_source_inventory` filesystem `rglob` (v6_generate_candidate_packet.py:851-887) vs `.gitignore`-aware `git status --porcelain` dirt check (:1202-1206). Strip-probe (in-memory, subject untouched): all validator stages pass with the 17 entries removed.
2. S2: packet + matrix read at C+1 — `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']`; nine known_limits, none naming CLM-DESCRIPTION-BUDGET; matrix row LIMITED/operator.
3. S3: `git grep` for the full and short candidate SHA against the packet README at C+1 → zero matches.
4. S7: isolated probe — this host creates symlinks without OSError (no skip); `os.path.realpath(link/../x.txt)` collapses lexically on NT, landing the write OUTSIDE the guarded tree (the POSIX divergence does not exist on NT); `_guard_norm_path` case-folds. `check()` appends to FAILURES and never raises (test_custody_gate.py:24-29).
5. S8: traceback read; `sync_skill_surfaces.py:524` `symlink_to` without `target_is_directory=True`; `--check` green.
6. Drill facts (S9): transcript read at C+1; PR #196 state + head verified via gh; run 32184104218 re-fetched (pull_request event, head 564a1e5, failed step = v6 workflow oracle audit).
7. Requalification: all five run URLs re-fetched live — workflow_dispatch, head_sha == C, per-job conclusions (custody contract success / contract-macos failure disclosed); release-security planted-secret positive-control step green.
8. R3 discharge: ODR file at d7c4178 sha256 == certification-section hash; RATIFY string present on #191 from the operator's account (live).
9. R7/R8 repairs: trigger types and paths-filter removal read at C's tree.
10. Main state: PR #195 merged 2026-08-18T22:03:42Z as 03b7724; main head green on both push runs; es#137 OPEN with fix commits confirmed non-ancestors of origin/main.
11. C/C+1 identity: diff C..C+1 confined to the packet dir (13 files); diff C..tip touches zero of 158 inventoried files (script-computed); pin tags peel to C/C+1 (live ls-remote).
12. Fingerprint: `verify_evidence.py` over the reports dir — 6 strict-format V-tags, 0 mechanically verified (format mismatch: lenses used `[V <tree> \`path\`]` style); the two spot-checked manually (cg's generator-lines and acceptance-procedure-item-4 citations) are accurate.

## Verdict gate trace

Mechanical computation: open P1 rulings at subject SHA `6db8c50420b194aebbd09a2ea5f81c6a276897dc`: S1 (the freeze's own verification instrument cannot pass on any clean checkout; acceptance-procedure item 4 unsatisfiable; the R8 takeover lands red on arrival; the handoff's digest-recomputation premise fails when run). Any open P1 ⇒ NO-GO; one is open ⇒ NO-GO. Open P2 (S2) would independently yield CONDITIONAL and is moot for the enum. Independently, the red-lines gate caps this record: no acceptance-supporting verdict while S1 stands. computed_verdict == gate computation == NO-GO.

**Prognosis (recorded, not laundered):** 14 of 15 predecessor acceptance criteria are discharged or retired by live state (R1, R2, R3, R4-substance, R6, R7, R8, R9, R10, R11, R13, R14, R15; R5 partial). The candidate's substantive guards are green and layered; the defect set is one tree-model line in a generator plus disclosure completeness. The successor freeze is expected to be cheap; the successor PANEL is still mandatory (no verdict transfer; fresh seat per D2's consequence).

## Next action

One decision for the operator, then a narrow re-freeze:

1. **Re-cut the candidate (agent-executable under existing classifications):** fix the generator's inventory tree model (`git ls-files` or an explicit `.gitignore`-respecting walk — never a relaxed validator), regenerate the packet at the new C, re-dispatch the five requalification workflows at the new SHA (D4b already classifies scratch-branch push + dispatch), register the rc3 pin tags in PINS AT the freeze (accept the digest-guard restamp deliberately, per CL-3), add the literal SHA to the README (S3), complete KL-RESTAMP's two omitted elements (S4), correct the KL-DRAFT-CI fraction (S6), and fold in the three one-line test-portability fixes (S7 skip-guard widening + `check()`-raises-under-pytest, S8 `target_is_directory=True`).
2. **One operator ruling (kills S2 either way):** rule whether LIMITED operator-owned claims must occupy a machine channel (blocking_claims / known_limits) or are legitimately prose-only — letter of R12's criterion vs the derivation's qualifiers (CL-2).
3. **Answer chesterton-gate's posed question:** whether this panel's evidence transfers to the post-fix SHA as a scoped continuation (delta review per revision-loop doctrine) or a fresh full panel is required — the protocol's answer is delta-plus-blast-radius with a fresh seat, but the operator may tighten it.
4. D8 stands: Step-7b cross-family consult at the successor's GO posture, before operator acceptance.

## Bounded reinstatement

One round is available per protocol: any party may attack a ruling's validity; a surviving attack recomputes that ruling only. No reinstatement attack was raised inside this run. The gate pre-bound one item against severity-trading: S1 caps every acceptance path while acceptance-procedure item 4 names the validator run as the proof instrument.

## The ruling-set@1 block (writable home of the verdict)

```json
{
 "ruling_set": "ruling-set@1",
 "run": "es-v6-rc2-gauntlet-kimi-2026-08-18",
 "subject_sha": "6db8c50420b194aebbd09a2ea5f81c6a276897dc",
 "seat": {
  "family": "kimi/moonshot",
  "independence": "fresh seat; not the author lineage (claude); not the predecessor adjudicator (D2); different model family from the authors; single-family panel caveat recorded; D8 Step-7b owed at next GO posture"
 },
 "rulings": [
  {
   "id": "S1-pyc-sealed-inventory-unverifiable",
   "lens": "all five lenses + dossier FC-1 + gate (one mechanism, six independent executions — weighed as one evidence chain)",
   "priority": "P1",
   "basin": "@2 source inventory seals 17 volatile __pycache__/*.pyc digests; validate_v6_assurance.py fails closed (R5 DIGEST MISMATCH, absent) on every clean checkout of C+1; a regenerated .pyc content-mismatches even on the generating host",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "dossier:FC-1",
    "human-automation-handoff-auditor:F1 (both passes)",
    "cloud-native-purist:CNP-1",
    "requirements-traceability-auditor:RTA-1",
    "safety-hazard-auditor:SHA-1",
    "chesterton-gate:CG-1"
   ],
   "justification": "Judge-reproduced (register item 1): the generator's filesystem rglob walk includes .gitignore'd host state that the porcelain dirt-check cannot see, sealing 17 volatile .pyc digests (158 = 141 + 17). The validator fails closed on any pristine checkout of C+1, so: acceptance-procedure item 4 ('the assurance validator passes on the exact packet bytes') is unsatisfiable by anyone including the operator; the R8 ready-mark takeover turns required stdlib-checks red on arrival (epistemic-flexibility.yml:268 runs the validator); KL-RESTAMP's posture prose and the handoff's 'the validator's digest recomputation proves it' do not survive execution. Fail-CLOSED polarity means zero false-green risk — weighed and recorded (CL-1) — but a permanently false-alarming tamper detector erodes the credibility of the freeze's one integrity layer. Repair edits an inventoried generator and regenerates the packet: a new SHA, hence not conditionally dischargeable on C. Kernels preserved: fail-closed digest direction (141 real sources byte-exact), the tamper self-test (18/18 at C), candidate_tree_hash portability, honest defaults (NOT_READY / NOT_RUN / refused self-certification / blocking_claims naming this gauntlet).",
   "acceptance_criteria": [
    {
     "condition": "The generator's inventory walk excludes .gitignore'd/untracked host state (git ls-files or an equivalent tracked-file enumeration), and validate_v6_assurance.py exits 0 on a pristine checkout of the new freeze commit while exiting non-zero on a planted one-byte mutation of an inventoried source. The successor packet's requalification evidence names the new candidate SHA with all five gating workflow_dispatch runs green (dispatch acts already classified under D4b).",
     "falsifier": {
      "method": "Fresh clone or worktree of the successor freeze commit on any OS; run validate_v6_assurance.py (expect exit 0); flip one byte in an inventoried source (expect exit != 0); re-fetch the five named runs and compare head_sha to the new candidate.",
      "threshold": "Exit 0 on the clean checkout AND exit != 0 on the tampered one AND five green dispatch runs at the new SHA. Today: first limb fails everywhere off the generating host.",
      "timeframe": "Before the successor packet is submitted for its independent verdict; re-run on every packet."
     },
     "owner": "agent (generator fix + regeneration + dispatch); operator (none beyond D4b's existing classification)"
    }
   ]
  },
  {
   "id": "S2-operator-channel-recurrence-r12",
   "lens": "requirements-traceability-auditor, human-automation-handoff-auditor seat2",
   "priority": "P2",
   "basin": "R12 recurrence: operator-owned CLM-DESCRIPTION-BUDGET (LIMITED) surfaces in neither blocking_claims nor known_limits; derive_blocking's LIMITED carve-out recreates the machine-channel drop pattern for the one live operator-open decision",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "requirements-traceability-auditor:RTA-3",
    "human-automation-handoff-auditor:F3 (seat2)"
   ],
   "justification": "Judge-verified against the criterion's own letter: every operator-owned claim must appear in blocking_claims or a known_limits entry naming it; CLM-DESCRIPTION-BUDGET (LIMITED, owner=operator) appears in neither (matrix + packet read at C+1). The criterion's falsifier fires on its own threshold ('any recurrence leaves the defect standing'). Qualified per CL-2: one claim, prose-disclosed in README 'Honest gaps', operator-owned by design — misrouting, not concealment; the es#40/PR#195/es#186 operator items rta names are ODR-dispositioned (D9/D11/D6) and covered by acceptance-procedure item 3, unlike the budget fork. Seat1's discharge is overruled on the letter, dissent preserved. Kernel: derive_blocking's single-home derivation and the validator's hand-edit rejection are correct and must survive.",
   "acceptance_criteria": [
    {
     "condition": "Either (a) every operator-owned claim regardless of status appears in blocking_claims or a known_limits entry naming it (owner field present), or (b) a recorded operator ruling exempts LIMITED-status operator-owned claims from the machine channels, with the criterion's letter amended in the same artifact so the register and the derivation agree.",
     "falsifier": {
      "method": "Parse the successor packet and matrix; assert the channel property over every claim whose owner contains 'operator'; grep for the operator ruling if (b).",
      "threshold": "Zero unlisted operator-owned claims, or the ruling artifact exists and the amended criterion text matches the derivation. Any unlisted operator-owned claim with no ruling leaves the defect standing.",
      "timeframe": "At successor submission; one command against the committed artifacts."
     },
     "owner": "operator rules (a) vs (b); agent implements"
    }
   ]
  },
  {
   "id": "S3-readme-literal-sha-r4-letter",
   "lens": "requirements-traceability-auditor",
   "priority": "P3",
   "basin": "R4's letter unmet: the packet README never names the subject SHA literally (grep: zero matches, full or short form); substance discharged via C/C+1 declaration, artifact stamps, and pin tags",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": ["requirements-traceability-auditor:RTA-2"],
   "justification": "Judge-verified (register item 3). The R4 basin (the freeze cannot name itself) is closed by construction and live-verified; the criterion's unconditional README-literal clause is simply unmet. P3: one-line repair at the successor freeze, which S1 already forces.",
   "acceptance_criteria": []
  },
  {
   "id": "S4-restamp-disclosure-partial-r5c",
   "lens": "dossier challenger, chesterton-gate, requirements-traceability-auditor, cloud-native-purist",
   "priority": "P3",
   "basin": "KL-RESTAMP discloses the restamp class generically but omits the two elements R5(c) specifically required: the post-freeze addition of clean-baseline.json and restoration of the deleted disclaimer's substance (the SHA-is-an-observation invariant)",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": ["dossier-challenger:D-2 (partial)", "chesterton-gate:CG-4", "requirements-traceability-auditor:RTA-4 (partial)"],
   "justification": "Seat-confirmed by direct read of KL-RESTAMP at C+1. chesterton-gate's framing adopted: the deleted fence was narrated, not re-erected. P3 disclosure-completeness; fold into the successor freeze.",
   "acceptance_criteria": []
  },
  {
   "id": "S5-pins-deferral-r5a",
   "lens": "cloud-native-purist, safety-hazard-auditor, chesterton-gate (CL-3 split)",
   "priority": "P3",
   "basin": "R5(a) letter unmet (rc2 pins absent from PINS; no operator ruling on the falsifier's alternative-anchor clause); substance discharged (origin tags peel to C/C+1, live-verified); criterion under-specified because check_pin_tags.py is digest-inventoried, so PINS registration necessarily postdates the freeze it registers",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": ["dossier:FC-5", "cloud-native-purist:CNP-3", "safety-hazard-auditor:SHA-3", "chesterton-gate:CG-3"],
   "justification": "CL-3 records the split and the structural note. The successor freeze should register the pins at freeze time and accept the deliberate digest-guard restamp (the guard tripping on the PINS edit is the guard working, not a reason to defer). Criterion-design precedent for the next ruling-set.",
   "acceptance_criteria": []
  },
  {
   "id": "S6-prose-layer-drift",
   "lens": "chesterton-gate, human-automation-handoff-auditor seat2, requirements-traceability-auditor, cloud-native-purist",
   "priority": "P3",
   "basin": "Prose layer unsealed and drifted: KL-DRAFT-CI '52 of 53' vs measured 51/54 at C; handoff 'the validator's digest recomputation proves it' red on arrival (S1); handoff 'expected loud skips' wrong for privileged NT (S7/S8); drill transcript's READY table transposes the custody/commission-watch run IDs (substance intact per live API)",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": ["chesterton-gate:CG-2", "human-automation-handoff-auditor:F4 (seat2)", "requirements-traceability-auditor:RTA-4 (partial)", "cloud-native-purist:CNP-4", "dossier-challenger:D-1 (minor limb), D-4"],
   "justification": "Each limb judge-verified (register items 4-6, 10; crib). Individually minor; collectively the prose layer promises a verifier experience the bytes do not deliver — the truthfulness surface this program exists to protect. P3; all repairs are one-line text fixes at the successor freeze.",
   "acceptance_criteria": []
  },
  {
   "id": "S7-r15-pin-portability",
   "lens": "safety-hazard-auditor (+ dossier FC-2)",
   "priority": "P3",
   "basin": "R15 characterization pin FAILs instead of SKIPping on privileged NT (skip guard keys only on OSError from symlink_to); the POSIX lexical-vs-realpath divergence does not exist on NT (the write lands OUTSIDE the guarded tree — guard and filesystem agree); check() never raises, so under pytest the pin passes silently with recorded failures",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": ["dossier:FC-2", "safety-hazard-auditor:SHA-2"],
   "justification": "Judge-reproduced (register item 4). KL-GUARD-LEXICAL's disclosure remains accurate for POSIX; the pin's NT behavior is a test-portability defect, not a custody-guard defect — the gating Linux surface is green at C. Latent oracle-adequacy note: the suite's exit-code discipline protects script execution (how CI runs it) but not pytest collection. P3; fixes are a skip-guard widening and a raise-on-failures under pytest.",
   "acceptance_criteria": []
  },
  {
   "id": "S8-sync-selftest-windows-crash",
   "lens": "safety-hazard-auditor (+ dossier FC-3)",
   "priority": "P3",
   "basin": "sync_skill_surfaces.py --self-test crashes deterministically on privileged NT: _selftest_copy creates the skills alias via symlink_to without target_is_directory=True (line 524); the gating --check operation is unaffected and green",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": ["dossier:FC-3", "safety-hazard-auditor:SHA-4 (half)"],
   "justification": "Judge-reproduced (register item 5). One-line fix class. Recorded within KL-WINDOWS's disclosed platform class; the handoff's crib expected it to pass, which is S6's prose gap.",
   "acceptance_criteria": []
  },
  {
   "id": "S9-drill-predates-seal",
   "lens": "human-automation-handoff-auditor seat2",
   "priority": "P3",
   "basin": "The R8 drill (2026-08-18T20:46Z) predates the sealed packet (C+1, 21:57Z); the takeover has never run against the sealed head, where it lands red via S1; the drill's stdlib leg failed at the v6-oracle-audit step on the drill head",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": ["human-automation-handoff-auditor:F2 (seat2)"],
   "justification": "CL-4: R8's criterion is discharged as written (mechanism drilled, transcript retained, runs != skipped at an unchanged head — judge-verified live); the timing observation's only consequence is S1's, already counted. Downgraded from the lens's P2 to P3 as identical-in-consequence, dissent preserved in CL-4.",
   "acceptance_criteria": []
  },
  {
   "id": "S10-cleanroom-sensitive-path-collision",
   "lens": "dispatcher (crib), uncontested",
   "priority": "P4",
   "basin": "test_live_runner.py fails inside cleanroom_ci.sh on this Windows host because its sensitive-path guard refuses the harness's own user-profile tempdir — fail-closed guard vs harness scratch placement; green on Linux CI at C",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": ["dossier:cleanroom-cluster"],
   "justification": "Observed in the seat's clean-room run (51/54); mechanism read at run_live.py:1274. P4 environment/portability note; the successor freeze may either place clean-room scratch outside the profile or exempt the fixture deliberately.",
   "acceptance_criteria": []
  }
 ],
 "discharged_predecessor_criteria": {
  "R1": "discharged — @2 verdict-binding fields; planted bare-enum-GO/wrong-SHA/missing-artifact all fail closed (validator self-test at C)",
  "R2": "discharged — CLM-SECRET-SCAN row; release-security dispatch run at C green with planted-secret positive control (live)",
  "R3": "discharged — D1 ratification (echo-certified ODR, hash-verified) upgraded to operator-posted RATIFY string on #191 (live); CLM-MERGE-190/156/192 matrix rows cite D1",
  "R4": "substance discharged (C/C+1, stamps, tags, requal at C); letter partial — see S3",
  "R5": "PARTIAL carrying the blocker — see S1 (b), S4 (c), S5 (a); (d) restamp refusal verified stricter-than-spec",
  "R6": "discharged via path (a) — CLM-DISPOSITION-CENSUS; statement matches oracle; generator fails closed on undispositioned items",
  "R7": "discharged via path (a) — paths filters removed from whole-tree readers; oracle audit strengthened (whole-tree-reader classification, self-test green)",
  "R8": "discharged as written — ready_for_review types on all five gating workflows; drill transcript retained and live-verified; see S9 for the timing observation",
  "R9": "discharged — completeness assertion, numerator/denominator print, named skips observed in the seat's own clean-room run; KL-DRAFT-CI names all five skipped jobs (fraction drift: S6)",
  "R10": "retired by live state — main green at 03b7724 (the falsifier's own retirement clause); KL-MAIN-RED carries the clause",
  "R11": "discharged — digest-bound exact-file allowlist green at C (37 files); owner/cadence recorded; four inert entries retired; one dormant entry digest-bound by design",
  "R12": "recurrence — see S2",
  "R13": "discharged — OPERATOR-ACCEPTANCE-PROCEDURE.md; @2 operator_acceptance schema fields; validator refuses terminal state without it (self-test)",
  "R14": "discharged — requirement register validates; crosswalk enforcement fails closed on planted defects (self-test); register recomputed 33/33 mapped (rta)",
  "R15": "discharged (disclosure limbs) — KL-GUARD-LEXICAL + CLM-MC-GUARD-LEXICAL LIMITED; safe-direction docstring reinstated; pin portability is S7"
 },
 "computed_verdict": "NO-GO",
 "verdict_binding": {
  "run_id": "es-v6-rc2-gauntlet-kimi-2026-08-18",
  "subject_sha": "6db8c50420b194aebbd09a2ea5f81c6a276897dc",
  "verdict_path": "docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/arbitration.md",
  "statements": [
   "This artifact is the verdict of record; a bare independent_gauntlet enum flip in promotion-packet.json is not this panel's verdict.",
   "No verdict of this run places the program in the terminal state by itself; operator acceptance follows docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md exactly.",
   "Even a GO would confer no promotion authority; CONDITIONAL is not GO; publication is an explicit owner act under RELEASING.md.",
   "No verdict transfer across SHAs: the S1 repair forces a new candidate SHA; rulings on unchanged content stand for the successor panel's delta review.",
   "This run satisfies no externally-enforced safety gate."
  ]
 }
}
```
