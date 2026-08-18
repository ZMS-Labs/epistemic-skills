# Arbitration — ES6-V6-CANDIDATE independent Gauntlet (run es-v6-candidate-freeze-2026-08-18)

**Computed verdict: NO-GO against candidate SHA `00e5146e43ff9011153452b83fedda706723c52b`** for issue #191's terminal state `V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE`.

**Verdict binding (anti-counterfeit, per the red-lines gate):** the verdict of record is THIS artifact — run `es-v6-candidate-freeze-2026-08-18`, subject SHA `00e5146e43ff9011153452b83fedda706723c52b`, ruling-set below. A bare enum value written into `promotion-packet.json` (`independent_gauntlet`) does not constitute this panel's verdict; `validate_v6_assurance.py` accepts a self-written "GO" and therefore cannot authenticate one. No verdict of this run places the program in the terminal state (no operator-acceptance procedure exists), and even a GO would have conferred no promotion authority: publication is an explicit owner act under RELEASING.md, and CONDITIONAL is not GO.

## Gate (red-lines-arbitrator): PASS-WITH-NOTES

Red lines checked:
- RL-1a Consent precedes the irreversible — review conduct (merge/tag/release/close/ready-mark/settings/push are operator-gated or PROMOTION acts): NOT CROSSED. No seat performed any; probes were scratch-copy only; live access read-only; both PRs remain draft; main untouched by the review.
- RL-1b Consent precedes the irreversible — subject production lineage: PRIMA FACIE CROSSING, unresolvable on the record. Three BUILD-window merges to main by cursor[bot] with no resolvable authorization artifact, against the operator's twice-written non-approval; packet non-disclosure compounds it. Capped per findings: no GO, and no acceptance without explicit operator ratify-or-reverse; not severity-tradeable, not agent-dischargeable.
- RL-2 No actor certifies its own acceptance: NOT CROSSED at actor level. Producing lineage held no seat; packet's self_certification='refused' is real and validator-enforced; seat separation confirmed in selection.json exclusions; verdict rendered by a separate judge; dispatcher draft bias (four blocking defects, all pro-candidate) caught by the isolated challenger pre-dispatch and disclosed. Independence caveat: single model family across all seats, this gate included — must appear in the verdict of record.
- RL-3 Oracles adequate to their claims — as applied to the review's own claims: HELD. Fingerprint scoped to citation integrity; finding truth rests on dispatcher re-verifications and own-falsifier attacks; dossier labels its incomplete surfaces rather than claiming them; no seat credited the subject's inadequate oracles as evidence. (Subject-side oracle inadequacy is the panel's finding set — judge's territory, not a review breach.)
- RL-4 The review itself must not close issues, merge, or tag: HELD. Nothing closed, merged, tagged, pushed, or flipped; the dossier was amended exactly once, pre-dispatch, via the Step-0 challenger, and no lens saw the pre-amendment draft.
- RL-5 Scope law — BUILD verdict only, no promotion authority conferred: HELD. The dossier scopes the question away from publication; no lens purports to authorize promotion; verdict of record must restate that even GO authorizes no merge/tag/release and that this run satisfies no externally-enforced safety gate.
- RL-6 Frozen-subject integrity and injection guard: HELD. Instruction-shaped subject text (gauntlet-request.md 'regenerate if HEAD moved', pre-named premises, 'Required outputs') was treated as data and adjudicated as findings (H8, chesterton-gate P3); the packet under review was never regenerated in place; run scope derived from #191 and RELEASING.md only.
- RL-7 Dissent preservation / no averaging: HELD TO DATE. 4 NO-GO + 1 CONDITIONAL carried as dissent-bearing input, not votes; the CLM-WF-PATH-COVERAGE factual conflict is named for explicit ruling; the judge must rule it and preserve chesterton-gate's dissent.
- RL-8 Security bright line — private-topology scrub law applied to the review's own record: CONDITION ATTACHED. Run reports embed the scrub-target string; the run record must pass the public-content gate or receive an operator-reviewed scrub/allowlist decision before commit/publication.

Gate findings and binding notes:
- GATE RESULT — no categorical violation by the review itself. The review performed no irreversible act (no merge, tag, release, issue/PR closure, readiness flip, ready-mark, or settings change; all probes ran in scratch copies, explicitly 'never in the pristine tree'; live GitHub access was read-only), smuggled no self-certification (producing Cursor lineage -5c03 held no seat; selection.json excludes gate and judge personas from the lens pool; verdict is rendered by a separate judge), and did not mutate the frozen subject. The gate therefore does not invalidate the run; the notes below bind how the verdict may be computed and recorded.
- CAP ON ACCEPTANCE PATHS (consent precedes the irreversible, subject lineage): the three BUILD-window merges to main (#190, #156, #192, merged_by cursor[bot] 2026-08-18T06:36-06:39Z) are irreversible operator-only acts whose consent chain is unresolvable from any artifact — the operator's only written words on #191 twice decline approval, #190 has zero reviews and bot-only comments, and the sole approval assertion is an agent-authored commit message citing nothing. Apply the dispatcher correction: weigh only the standing limbs (#190/#156 do appear as claim citations; no reconciliation row exists for any of the three; #192 — the candidate's own base — appears nowhere in any packet artifact). Consequence this gate imposes: GO is unavailable from this record, and no acceptance-supporting verdict may issue unless its conditions include the operator explicitly ratifying or reversing the three merges and the packet disclosing them. This item is operator-resolvable only: it may not be severity-traded below blocker in any reinstatement round and cannot be discharged by agent-side evidence. It is recorded as a prima facie crossing, not a certified violation, because the record cannot exclude out-of-band operator consent.
- VERDICT-RECORDING CONDITION (anti-counterfeit): validate_v6_assurance.py accepts a self-written independent_gauntlet='GO' with all nine blockers standing (handoff-auditor P1; dispatcher re-verification #2). The verdict of record must therefore be bound to this run's identity — run id, subject SHA 00e5146e43ff9011153452b83fedda706723c52b, and a durable verdict-artifact path — and must state that a bare enum flip in promotion-packet.json does not constitute this panel's verdict. It must also state that no operator-acceptance procedure exists (handoff-auditor P2), so no verdict of this run places the program in the terminal state, and that even a GO would confer no promotion authority (RELEASING.md: publication is an explicit owner act; CONDITIONAL is not GO).
- FIX-SET ACT HYGIENE (forward-looking consent line): surviving recommendations name acts the two-stage boundary does not classify — a pin tag on 00e5146 (entropy-demon), a scratch-branch push plus workflow_dispatch at the candidate (cloud-native-purist), and ready-mark reclassification (handoff-auditor). None crosses a red line as written because each is routed to the operator, and entropy-demon explicitly escalates the pin-tag-vs-forbidden_this_run conflict rather than assuming scope. The verdict must preserve that routing: acts unclassified by the operator-approved boundary are default-deny for agents until classified; no fix-set item is itself agent-executable authority.
- RUN-RECORD HYGIENE (security bright line applied to the review's own artifacts): the review's report files (chesterton-gate.md, entropy-demon.md) embed the private-fleet repo string that the public-content gate exists to scrub. Condition: before the run record is committed or published, it must pass check_public_content.py or receive an operator-reviewed scrub/allowlist decision — the review must not recreate the violation class it found the candidate silencing. This is containment, not novel exposure (main is already live-red on this same pattern class per chesterton-gate P1, dispatcher-confirmed).
- INDEPENDENCE CAVEAT (no actor certifies its own acceptance — family level): dossier author/dispatcher, challenger, all five lenses, the judge, and this gate run in one model family, disclosed in the dossier; cross-family adjudication required operator authorization and the operator was absent. Actor-level separation held (the candidate's producing lineage adjudicated nothing; dispatcher pro-candidate bias in the draft dossier was caught pre-dispatch by the isolated challenger and disclosed as bias evidence). Not categorical, but the caveat must be carried into the verdict of record. This gate shares the family and carries the same caveat.
- ORACLE-SCOPE NOTE (oracles adequate to their claims): the Sovereign Fingerprint (222/222 V-tags, 0 H-tags) certifies citation-anchor integrity only, not finding truth; truth support comes from the dispatcher's independent mechanical re-verifications and from attacks that satisfied the matrix rows' OWN falsifiers. The verdict must not cite the fingerprint as proof of finding correctness, and must not credit the packet's self-labels: no seat treated packet-internal green (schema-only validator, 34/34 clean-room, PROVED markers) as satisfying evidence, and the verdict may not either — one of three PROVED claims is falsified on its strong reading (CLM-TRACKER-RECONCILED) and one is under the named factual conflict (CLM-WF-PATH-COVERAGE: cloud-native-purist P1 vs chesterton-gate P3) that the judge must rule explicitly, preserving dissent rather than averaging, including chesterton-gate's CONDITIONAL lens verdict.
- RECORD INSUFFICIENCIES (stated per gate instructions, not probed): (a) whether out-of-band operator consent for the three merges exists cannot be resolved from the record — hence the ratify-or-reverse condition instead of a violation declaration; (b) whether the run directory is git-tracked or committed is not in the record — hence the pre-commit scrub condition is conditional; (c) GitHub repo settings (required-check designation, rulesets) were unreadable from the run's seats, as the dossier's uncertainty labels disclose.

## Rulings digest (18 basins; canonical fields in the ruling-set block below)

| id | priority | ruling | status | basin |
|---|---|---|---|---|
| R1-terminal-gate-forgeable | P1 | UPHELD | open | Terminal readiness gate has zero rejection power (self-written GO) |
| R2-secret-scan-unclaimed-unrun | P1 | UPHELD | open | Release-security full-history secret scan: no claim, no run, no disclosure |
| R3-build-window-merges-unreconciled | P1 | UPHELD-WITH-QUALIFICATIONS | open | Three BUILD-window merges to main (#190/#156/#192) without resolvable authorization or packet disclosure |
| R4-candidate-sha-binding-failure | P1 | UPHELD | open | Exact-SHA requalification not met at 00e5146: the candidate cannot name itself and no required surface was evaluated there |
| R5-immutability-without-mechanism | P1 | UPHELD | open | Immutable-packet claim has no anchor, no detector, an undisclosed post-freeze mutation, and a destructive regeneration recipe |
| R6-tracker-reconciliation-citation-only | P1 | UPHELD-WITH-QUALIFICATIONS | open | CLM-TRACKER-RECONCILED PROVED on a strong statement its oracle cannot test; 46 tracker rows structurally incapable of failing |
| R7-wf-path-coverage-proved-row | P2 | SPLIT | open | CLM-WF-PATH-COVERAGE: PROVED row whose own falsifier fires (named factual conflict) |
| R8-ready-for-review-takeover-absent | P1 | UPHELD | open | KL-DRAFT-CI's sole compensating control (ready-mark takeover) does not exist in the trigger configuration |
| R9-cleanroom-undercoverage | P2 | UPHELD | open | Clean-room BUILD oracle under-coverage and KL-DRAFT-CI overstatement |
| R10-rollback-premise-main-red | P2 | UPHELD-WITH-QUALIFICATIONS | open | Rollback plan's safe harbour (main) is live-red on its required gate, undisclosed |
| R11-public-content-gate-silenced | P2 | UPHELD | open | Public-content gate: whole-file permanent allowlist widening on a live generator; self-falsifying recorded evidence; pasted-stdout substrate |
| R12-operator-alert-channel | P2 | UPHELD | open | Machine-readable blocker channel structurally drops operator-owned items |
| R13-no-acceptance-procedure | P2 | UPHELD | open | The terminal state names a human act with no defined procedure, acceptor, or record |
| R14-taxonomy-substitution-no-register | P2 | UPHELD | open | #191's enumerated claim/evidence classes substituted by an implementer taxonomy with no crosswalk; no requirement register |
| R15-custody-residual-undisclosed | P2 | UPHELD-WITH-QUALIFICATIONS | open | es#137 fixes sound (H6 killed) but a residual lexical-vs-realpath false-allow class is undisclosed and its deleted rationale unrestored |
| R16-promotion-disarm-undisclosed-burden | P3 | UPHELD | open | Operator-facing limit understates the PROMOTION disarm/re-arm burden; never rehearsed |
| R17-frozen-detectors-non-gating-monitors | P4 | UPHELD | open | Detectors frozen in time (gitleaks pin) and monitors that cannot fail (contract-macos) |
| R18-packet-framing-steering | P3 | UPHELD-WITH-QUALIFICATIONS | open | Implementer-authored packet framing (H8): anti-steering prose, but pre-named blocker set non-exhaustive and a regenerate-the-subject instruction embedded |

Seven P1 rulings stand open at the subject SHA (R1, R2, R3, R4, R5, R6, R8); eight P2 (R7, R9–R15) and three P3/P4 (R16–R18) are open behind them. Merged finding ids, per-ruling justifications, and the acceptance criteria (the fog-free fix ticket) are carried in the machine block, one entry per basin — correlated findings across lenses were merged and weighed as single evidence chains, never as votes.

## Conflict Ledger (dissent preserved, never averaged)

### CL-1 [SPLIT] cloud-native-purist (P1 proved-path-filter-claim-false) vs chesterton-gate (P3 proved-claim-labels-a-risk-its-oracle-cannot-see)

- **Conflict:** Is the PROVED matrix row CLM-WF-PATH-COVERAGE ('each CI workflow's path filter is a superset of the files its steps read or execute') FALSE, or narrowly true but consequence-overread? Direct factual conflict named by the dispatcher for explicit ruling.
- **Evidence weight:** cnp: [V] anchors dispatcher-confirmed (check_public_content.py runs git ls-files over the repo root; finite paths: filter) plus recorded [I] probe work satisfying the claim's OWN falsifier (1467 tracked / 1395 filtered / 72 outside; seeded defect in an unfiltered file → gate exit 1, no dispatch; oracle audit 0 findings by construction via .github/scripts allowlist). cg: [V] claim/consequence text plus live [I] job-record read of the two silent-skip mechanisms the audit cannot see. Both chains verified; neither refutes the other's observations — they diverge on the construction of 'files its steps read or execute'.
- **Dissent preserved:** cg's position that 'its narrow statement is true' is recorded verbatim and NOT averaged away; cnp's P1 calibration (false PROVED row = decisive) is recorded as the stricter proposal the judge declined on construction-ambiguity grounds. If a future round establishes a single authoritative construction of 'files its steps read', the losing limb's severity must be recomputed, not assumed.
- **Valid kernel A:** cnp: under the plain reading, and under the claim's own stated falsifier — the correct oracle for a matrix row — the statement is false: a whole-tree-reading step's workflow filter covering 1395/1467 files is not a superset of its input set, and the audit cited as proof is structurally blind to it. The row cannot stand as PROVED.
- **Valid kernel B:** cg: the audit's zero-findings is internally consistent with its narrow literal-token oracle, so on the narrowest construction the audited property holds; independently, the row's release_consequence ('silent skip risk on release gate suites') overreaches on ANY construction, since draft gating and fail-fast short-circuiting — both live — are invisible to a static path-filter audit.
- **Synthesis:** The verdict does not need to force one construction to compute: under cnp's construction the row is false; under cg's it is a narrow truth mislabeled with a broad retired-risk consequence. Either way the PROVED status is untenable and the defect is open (R7, recalibrated P2). Repair paths: demote to PARTIAL with the 72-file limit, or remove the paths filters per the repo's own release-security precedent — plus narrow the consequence text on both paths.
- **Residual tension:** The governing contract nowhere defines 'files its steps read or execute' for whole-tree scanners; until the requirement register (R14) defines it, the same dispute will recur on every freeze.
- **Justification:** Ruled on evidence quality: cnp's probe satisfied the claim's own falsifier (the agreed oracle), which outweighs a defense resting on a narrower construction the claim text does not state; cg's overread limb is independently verified and survives regardless. Both kernels are load-bearing in the fix.

### CL-2 [OVERRULED] chesterton-gate (lens verdict CONDITIONAL) vs human-automation-handoff-auditor, entropy-demon, cloud-native-purist, requirements-traceability-auditor (lens verdicts NO-GO)

- **Conflict:** Whether the frozen packet at 00e5146 can be accepted with conditions (disclosure repairs, no code changes) or must be refused at this SHA.
- **Evidence weight:** Not a vote: 4-1 carries zero arithmetic weight. Weighed chains: cg's CONDITIONAL rests on verified kernels (honest NOT_READY posture, refused self-certification, healthiest-surface custody code, all its own blockers being disclosure repairs). The NO-GO side rests on verified chains that conditions on THIS SHA cannot discharge: the candidate tree cannot name itself, required surfaces were never evaluated there, the terminal gate is forgeable, and any correcting edit necessarily produces a different SHA (cnp's explicit point; cg's own fix set ends 'Re-freeze at a SHA whose own tree names it, then re-run this gate').
- **Dissent preserved:** chesterton-gate's CONDITIONAL, its reasoning, and its assessment that all its named blockers are packet-disclosure repairs touching no candidate code are preserved here in full and were not averaged into the computation. Its H6-kill (custody fixes exemplary) and H1-reframe (identity lag is structural, not accidental) stand as recorded qualifications on R15 and R4.
- **Valid kernel A:** cg: the packet's honesty structure is real and the repair cost is low — nothing in the record suggests the underlying code is unsound (custody suite green at the exact candidate under two independent re-runs; dispatcher re-ran the clean-room-missed steps green). A re-frozen packet executing the fix set could plausibly clear quickly.
- **Valid kernel B:** The four NO-GO lenses: a verdict 'against THAT SHA' cannot be CONDITIONAL when the conditions require a new SHA; and the gate independently caps this record at NO-GO (RL-1b: unresolved merge-consent chain; GO unavailable; no acceptance without operator ratify-or-reverse).
- **Synthesis:** cg's CONDITIONAL is functionally a NO-GO-at-this-SHA with a favorable prognosis for the successor freeze — its own terminal condition concedes the re-freeze. The verdict records the prognosis without laundering it into the verdict enum.
- **Residual tension:** None material once 'against THAT SHA' is fixed as the question; the tension was over verdict semantics, not facts.
- **Justification:** The mechanical gate computes the verdict from open P1 rulings, and seven stand open at 00e5146; separately the red-lines gate caps any acceptance path pending the operator's merge ruling. CONDITIONAL is unreachable on both grounds.

### CL-3 [SPLIT] All five lenses (H7 disclosure-adequacy attacks) vs the packet's own self-disclosures (H7 null/defense: honest NOT_READY freeze with disclosed gaps)

- **Conflict:** The packet claims — and the docket's null hypothesis defends — that its gaps are disclosed (NOT_READY, refused self-certification, 9 blocking claims, 8 known limits). The findings assert material gaps outside every disclosure channel.
- **Evidence weight:** Refusal limb: [V] schema const + validator enforcement + empty requested_irreversible_acts + untouched main + generation-enforced UNPROVED on CLM-INDEPENDENT-GAUNTLET — verified by multiple seats. Disclosure limb: [V]-anchored, largely dispatcher-confirmed absences — no secret-scan row/limit (R2), no merge disclosure incl. #192 absent everywhere (R3), no restamp disclosure (R5), KL-DRAFT-CI naming 2 of 5 skipped jobs with a nonexistent mitigation (R8/R9), blocking_claims omitting 4 BLOCKED operator-owned and 2 self-labeled-P1 claims (R12), no main-red disclosure (R10), no custody-residual row (R15).
- **Dissent preserved:** The packet's honest-posture evidence is recorded as validation kernels across R1-R15 and must survive every fix; entropy-demon's and cnp's explicit statements that the packet is 'honest about what it names' are preserved against any reading of this verdict as an integrity accusation against the freeze's posture.
- **Valid kernel A:** The refusal limb of H7 SURVIVES and is genuinely unusual: the honest state is produced automatically, the packet performs zero irreversible acts, publishes unflattering statuses (31 UNPROVED tracker rows, 1 UNPROVED-by-construction), and no seat found a self-authored GO anywhere.
- **Valid kernel B:** The disclosure-adequacy limb is KILLED on at least seven independent chains: the largest disclosed gap is paired with a compensating control that does not exist, and the material undisclosed set (secret scan, merges, restamp, main-red, terminal-gate impotence, custody residual) exceeds the disclosed set in consequence.
- **Synthesis:** 'Refuses to self-certify' and 'discloses its own gaps' are different properties; the packet has the first and has been credited with the second on the strength of the first (rta's formulation, adopted). The verdict credits the refusal posture as a preserved kernel in nearly every ruling while refusing to let it stand in for disclosure.
- **Residual tension:** H8 interaction: the honesty of the named disclosures is exactly what anchored review attention at the disclosed gaps (cg's method finding, R18) — an honest-posture packet can still under-enumerate.
- **Justification:** Ruled on the falsifier the docket itself set for H7: 'one PROVED-status claim shown false, or one material undisclosed gap.' The record contains at least one of the first (R6; R7 contested) and several of the second.

### CL-4 [UPHELD-WITH-QUALIFICATIONS] requirements-traceability-auditor (build-window-merges, as filed) vs dispatcher mechanical re-verification (Step-6 correction)

- **Conflict:** rta's finding asserted 'no claim, no reconciliation row, no known-limit, no disclosure' for all three BUILD-window merges; the dispatcher verified the no-claim limb is WRONG for #190 (cited in CLM-RELEASE-AUTH/CLM-REQUIRED-JOB/CLM-MC-MACOS-CASE) and #156 (cited in CLM-RELEASE-AUTH).
- **Evidence weight:** Dispatcher correction: [V] direct reads of the matrix authority/independence fields. rta's standing limbs: [V] parse of reconciliation PR rows {100,103,176,193,194} and packet-wide grep — no row/disposition for any of the three, #192 absent from every packet artifact; live merge metadata and operator non-approval text verified.
- **Dissent preserved:** rta's original framing is preserved in its report; this ledger entry is the authoritative narrowing.
- **Valid kernel A:** rta: the load-bearing limbs survive intact, and the citation-without-reconciliation state of #190/#156 is itself the exact failure mode #191 pre-named ('reconcile and not merely cite') — the correction narrows the finding while sharpening its irony.
- **Valid kernel B:** Dispatcher: the overstatement was real and material to fairness; a finding that would brand the packet as never mentioning #190/#156 misstates the record.
- **Synthesis:** R3 is ruled on the standing limbs only, exactly as the arbitration rules mandate; the corrected limb is recorded here so the fix ticket does not demand a 'claim' that already exists.
- **Residual tension:** None; the correction was accepted without contest.
- **Justification:** Mandated correction applied (arbitration rule 4). The P1 severity is unaffected because it rested on the no-disposition and #192-absent limbs plus the unresolvable consent chain, all standing.

### CL-5 [UPHELD] entropy-demon / cloud-native-purist fix-set recommendations (pin tag on the candidate; scratch-branch push + workflow_dispatch; ready-mark reclassification) vs exact-candidate-receipt forbidden_this_run and the operator-approved two-stage boundary

- **Conflict:** The highest-value fixes name acts the two-stage boundary does not classify: forbidden_this_run lists 'tag' (scope ambiguous for non-version pin tags), branch-push + dispatch at the candidate is unclassified, and the ready-mark act is classified in no governing source (haha's finding).
- **Evidence weight:** [V] receipt forbidden_this_run text; [V] #191 boundary enumeration; entropy-demon explicitly escalates the pin-tag conflict rather than assuming scope; cnp argues branch-creation is not the operator-gated act (tag creation is) — an argument, not an authorization.
- **Dissent preserved:** cnp's position that the branch-push/dispatch path is BUILD-scoped and fully reversible is preserved as the recommended reading for the operator to adopt — it is plausible and the workflows' own comments support it — but it is the operator's reading to adopt, not the panel's.
- **Valid kernel A:** The fixes are technically correct and cheap, and the substrates were built for exactly these purposes (workflow_dispatch comments; pin/ tag convention with check_pin_tags.py).
- **Valid kernel B:** The gate's act-hygiene rule: acts unclassified by the operator-approved boundary are default-deny for agents until classified; no fix-set item is itself agent-executable authority, and cnp's 'not the operator-gated act' reasoning must not be treated as consent.
- **Synthesis:** Every acceptance criterion in R2, R4, R5, and R8 that involves a push, dispatch, tag, or ready-mark is routed through explicit operator classification first; agent-executable items (validator code, disclosures, manifests, workflow-trigger edits on a draft branch) are separated from operator-gated ones in each criterion's owner field.
- **Residual tension:** If the operator reads forbidden_this_run's 'tag' as covering pin tags, #191's immutable-packet requirement and the receipt prohibition are in direct conflict; entropy-demon's escalation stands: the operator must resolve which governs, and the resolution must be recorded.
- **Justification:** Consent precedes the irreversible extends forward: a review that just found an unresolvable consent chain (R3) must not itself seed the next one.

### CL-6 [SPLIT] cloud-native-purist (H8 KILLED: gauntlet-request is structurally anti-steering) vs chesterton-gate P3 and requirements-traceability-auditor (H8 SUPPORTED: pre-named premises anchor the panel; '(regenerate if HEAD moved)' is a subject-mutation instruction)

- **Conflict:** Whether implementer-authored packet framing steered the review.
- **Evidence weight:** cnp: [V] reads of the request's anti-steering directives; all four pre-named premises live-verified true. cg: [I] cross-check that both of its P1s — and in fact most of this run's P1 basins — lie outside the pre-named set; rta: [V] the regenerate instruction and the machine-readable under-enumeration (KL-DRAFT-CI 2-of-5).
- **Dissent preserved:** cnp's kill is preserved as scoped to the prose limb it tested; it did not test the enumeration limb, and its own finding #2 (KL-DRAFT-CI under-enumeration) supplies evidence FOR the limb it did not frame as H8.
- **Valid kernel A:** cnp: the prose is honest and points at independence; no directive in it was followed as an instruction (RL-6 held), and the premises it named were true.
- **Valid kernel B:** cg/rta: steering by pre-named true-and-adverse blockers is the strong form — confirming them consumes budget and feels independent — and the operative steering lives in machine-readable fields (selective enumeration) and in the regenerate instruction, not in tone.
- **Synthesis:** H8 resolves at the mechanism level: prose steering — killed; enumeration steering — demonstrated by the out-of-set P1 count. Method note recorded for future runs (R18): budget explicit out-of-set search on implementer-authored packets; strike regenerate-type instructions from frozen subjects.
- **Residual tension:** None operative for this verdict; carried as method doctrine.
- **Justification:** Both parties' observations are verified and non-contradictory; only their H8 framings collide. Split on limbs, no averaging.

## Verdict gate trace

Mechanical computation per rule 6, then the gate cap. Open P1 rulings at subject SHA 00e5146e43ff9011153452b83fedda706723c52b: R1 (terminal gate accepts self-written GO with nine blockers standing), R2 (required security-class secret-scan surface unclaimed/unrun/undisclosed), R3 (three BUILD-window merges with unresolvable authorization, undisclosed; ruled on the dispatcher-corrected standing limbs; operator-resolvable only), R4 (candidate cannot name itself; zero required surfaces evaluated at the subject SHA; closure unreachable from current branch state), R5 (immutable-packet requirement unmet by mechanism; undisclosed post-freeze mutation; perishable coordinate), R6 (CLM-TRACKER-RECONCILED PROVED-but-false on #191's own strong reading), R8 (the packet's sole compensating control for its largest gap does not exist). Any open P1 => NO-GO; seven are open => NO-GO. Open P2s (R7, R9-R15) would independently yield CONDITIONAL and are moot for the enum. Independently and redundantly, the red-lines gate result (PASS-WITH-NOTES, RL-1b prima facie crossing) caps this record at NO-GO: GO is unavailable, and no acceptance-supporting verdict may issue unless its conditions include the operator explicitly ratifying or reversing the three merges — R3's acceptance criterion carries that condition verbatim. computed_verdict == gate computation == NO-GO. Binding statements required by the gate, hereby made of record: (1) this verdict is bound to run es-v6-candidate-freeze-2026-08-18, subject SHA 00e5146e43ff9011153452b83fedda706723c52b, and this ruling-set artifact — a bare independent_gauntlet='GO' enum flip in promotion-packet.json does not and cannot constitute this panel's verdict; (2) no operator-acceptance procedure exists (R13), so no verdict of this run places the program in the terminal state; (3) even a GO would confer no promotion authority — publication is an explicit owner act per RELEASING.md, CONDITIONAL is not GO, and this run satisfies no externally-enforced safety gate, whose separate record is still owed; (4) the fingerprint (222/222) certifies citation-anchor integrity only, not finding truth — truth support here rests on the dispatcher's independent mechanical re-verifications and on attacks satisfying the matrix rows' own falsifiers, and no packet-internal green (schema-only validator, 34/34 clean-room, PROVED markers) was credited as satisfying evidence by any seat or by this verdict. Honest labeling: NO-GO here means the frozen packet at THIS SHA cannot support the terminal state as argued in this bracket — it is not a finding that the code is unsound (custody is the record's healthiest surface, H6 killed twice over) nor that the freeze's refusal-to-self-certify posture is dishonest (it is real and validator-enforced). Heavy refutation of a first-of-its-kind promotion packet is progress.

## Next action

Put ONE decision in front of the operator before any other work: explicitly ratify or reverse the three BUILD-window merges (#190, #156, #192) in a durable operator-authored artifact (R3 — the only item no agent can discharge, and the gate's precondition for every acceptance path), and in the same sitting classify the four unclassified acts the fix set needs (pin tag vs forbidden_this_run's 'tag'; scratch-branch push; workflow_dispatch at the candidate; draft-PR ready-mark). In parallel, agents may prepare — as draft work on the freeze branch, executing nothing operator-gated — the P1 fix set for the successor freeze: verdict-binding validator + schema fields (R1), CLM-SECRET-SCAN row and corrected KL-DRAFT-CI (R2, R8, R9), KL-RESTAMP disclosure + digest manifest (R5), CLM-TRACKER-RECONCILED demotion or real per-item content (R6), and a self-naming re-freeze plan (R4). One hygiene condition on this run's own record before it is committed or published: the report files embed the private-fleet scrub-target string, so the run record must pass check_public_content.py or receive an operator-reviewed scrub/allowlist decision first (gate RL-8).

## Bounded reinstatement

One round is available per protocol: any party may attack a ruling's validity; a surviving attack recomputes that ruling only. No reinstatement attack was raised inside this run. The red-lines gate pre-bound one ruling against severity-trading: R3 may not be traded below blocker in any reinstatement round and is operator-resolvable only.

## The ruling-set@1 block (writable home of the verdict; the run record and any ledger line derive from it)

```json
{
 "ruling_set": "ruling-set@1",
 "run": "es-v6-candidate-freeze-2026-08-18",
 "subject_sha": "00e5146e43ff9011153452b83fedda706723c52b",
 "rulings": [
  {
   "id": "R1-terminal-gate-forgeable",
   "lens": "human-automation-handoff-auditor, requirements-traceability-auditor",
   "priority": "P1",
   "basin": "Terminal readiness gate has zero rejection power (self-written GO)",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "human-automation-handoff-auditor:terminal-gate-is-a-self-written-string",
    "requirements-traceability-auditor:assurance-validator-cannot-reject"
   ],
   "justification": "Two independent mutation-probe chains, dispatcher-reproduced (re-verification #2): validate_v6_assurance.py exits 0 on readiness=V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE with a self-written independent_gauntlet='GO', all nine blocking_claims intact, known_limits emptied, an all-zero candidate_sha, deleted cited evidence, and wholesale status inflation (M1-M4 all rc=0). The schema binds the GO to nothing — no run id, no verdict path, no subject SHA, no acceptor. The contract and validator are candidate-authored, so this is in-scope behavior, not inherited debt. Per the gate's anti-counterfeit condition: THIS run's verdict is bound to run es-v6-candidate-freeze-2026-08-18, subject SHA 00e5146e43ff9011153452b83fedda706723c52b, and this ruling-set artifact; a bare enum flip in promotion-packet.json does not constitute this panel's verdict, and no verdict of this run places the program in the terminal state (see R13). Validation kernel preserved: the honest defaults (NOT_READY/refused/NOT_RUN hard-set by the generator, self_certification as schema const) are real and must survive any fix.",
   "acceptance_criteria": [
    {
     "condition": "promotion-packet.schema.json gains gauntlet_run_id, gauntlet_verdict_path, gauntlet_subject_sha; validate_v6_assurance.py additionally requires, for terminal readiness: blocking_claims == [] and an on-disk verdict artifact whose subject SHA equals candidate_sha. Generator's NOT_READY/NOT_RUN/refused defaults preserved unchanged.",
     "falsifier": {
      "method": "Re-run the recorded mutation probes on the re-submitted packet tree: (a) flip readiness to terminal + independent_gauntlet='GO' with blocking_claims left at 9 and no verdict artifact; (b) candidate_sha := '0'*40; (c) delete one cited evidence_paths file; run validate_v6_assurance.py after each.",
      "threshold": "Non-zero exit on every mutation, with the message naming the unresolved blockers, missing verdict binding, SHA mismatch, or missing evidence path. Any exit 0 leaves the defect standing.",
      "timeframe": "Before any packet re-submission is put before the operator; re-run on every subsequent packet."
     },
     "owner": "agent (implementer lineage), verified by the next independent panel"
    }
   ]
  },
  {
   "id": "R2-secret-scan-unclaimed-unrun",
   "lens": "entropy-demon, cloud-native-purist, requirements-traceability-auditor, chesterton-gate",
   "priority": "P1",
   "basin": "Release-security full-history secret scan: no claim, no run, no disclosure",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "entropy-demon:release-security-surface-has-no-claim-and-no-run",
    "cloud-native-purist:secret-scan-gate-unclaimed-and-unrun",
    "requirements-traceability-auditor:secret-scan-orphan-requirement",
    "chesterton-gate:release-security-gate-has-no-claim-row"
   ],
   "justification": "One claim, four correlated statements — weighed as a single evidence chain, not four votes. The chain is dispatcher-confirmed (re-verification #6) and rests on independent V-anchored enumerations of all 15 class claims (none names the scan), packet-wide greps (release-security appears once, as a filename in source-inventory.json), RELEASING.md:126's requirement of the scan WITH planted-secret positive control on the exact candidate, and live check-run reads showing full-history-secret-scan skipped at both PR heads with zero runs at 00e5146. #191 requires a matrix covering every material claim; a required security-class release gate with zero rows, zero known_limits, and zero runs is a material undisclosed hole — worse than an honest UNPROVED row because it is indistinguishable from not-applicable. cnp's honesty note is credited: the candidate delta likely contains no credential material, so the expected scan outcome is green; the defect is matrix truthfulness, not an expected red. chesterton-gate's extension stands: gate-6 bullets 3-4 (immutable disposition record, provenance/license) are also uncovered. Kernel preserved: fix by adding the claim at its true status and running the gate; never by relaxing release-security.yml's unnarrowed, positive-controlled design.",
   "acceptance_criteria": [
    {
     "condition": "CLM-SECRET-SCAN added to the class matrix (authority RELEASING.md item 6a; oracle: release-security full-history-secret-scan green at the exact candidate including the planted-secret positive control; status UNPROVED until such a run exists) and added to blocking_claims; KL-DRAFT-CI's skipped-job enumeration corrected to all five observed skipped gating jobs. Evidence, when produced, is a {workflow, run_id, job_id, head_sha, conclusion} record at the exact candidate ref via workflow_dispatch on a scratch branch — an act the operator must first classify under the two-stage boundary (see R3/gate act-hygiene note).",
     "falsifier": {
      "method": "Parse claim-to-proof-matrix.json and promotion-packet.json of the re-submitted packet for a claim/known_limit naming the full-history secret scan; if evidence is claimed, fetch the named run and compare head_sha to the candidate SHA and read the positive-control step conclusion.",
      "threshold": "At least one matrix row naming the scan with explicit status and release_consequence, present in blocking_claims while unrun; if marked satisfied, run record at the exact candidate SHA with positive control detected. Zero rows leaves the defect standing.",
      "timeframe": "Row and disclosure: at re-submission. Run evidence: before operator acceptance."
     },
     "owner": "agent adds row/disclosure; operator classifies and authorizes the branch-push + dispatch acts"
    }
   ]
  },
  {
   "id": "R3-build-window-merges-unreconciled",
   "lens": "requirements-traceability-auditor",
   "priority": "P1",
   "basin": "Three BUILD-window merges to main (#190/#156/#192) without resolvable authorization or packet disclosure",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": [
    "requirements-traceability-auditor:build-window-merges-unreconciled"
   ],
   "justification": "Dispatcher correction APPLIED: the 'no claim' limb is OVERRULED for PR #190 and #156 (both appear as citations in claim authority/independence fields — which itself instantiates #191's pre-named 'cite, not reconcile' failure mode). Ruled on the standing limbs only, both dispatcher-verified: (1) no reconciliation row or disposition exists for any of the three window merges; (2) PR #192 — the candidate's own base commit — appears nowhere in any packet artifact. The [V]/[I] chain is strong: merges by cursor[bot] 06:36-06:39Z on 2026-08-18; the operator's only written words on #191 (body plus sole comment, six hours before the merges) twice decline approval of merge and of PR #190 specifically; #190 has zero reviews and bot-only comments; the sole approval assertion is an agent-authored commit message citing nothing. Like the lens and the gate, I do NOT rule the merges unauthorized — the record cannot exclude out-of-band consent (see coverage known-unknowns). What is ruled: the authorization is unresolvable from any artifact, and the packet builds on the merges while disclosing none of them. Per the gate's RL-1b cap this item is operator-resolvable only: it may not be severity-traded below blocker in any reinstatement round and cannot be discharged by agent-side evidence. Kernel preserved: the candidate itself performed no irreversible act — the repair is disclosure plus operator ratification, never a loosening of the BUILD/PROMOTION boundary.",
   "acceptance_criteria": [
    {
     "condition": "The operator explicitly ratifies or reverses each of the three merges (#190, #156, #192) in a durable, operator-authored artifact (issue comment, review, or signed record), AND the packet adds reconciliation rows (or a closed-item ledger) for all three, citing the authorization artifact, plus a known_limit disclosing that the candidate's base was produced by BUILD-window merges.",
     "falsifier": {
      "method": "Read the named artifact for each merge (pull_request_read get_reviews/get_comments; issue #191 comments postdating 2026-08-18T00:37:06Z); grep the re-submitted packet for rows/limits naming #190/#156/#192.",
      "threshold": "An operator-authored ratify-or-reverse record exists for each of the three AND at least one packet row/limit names each. Either half missing leaves the defect standing; no agent-side evidence can discharge it.",
      "timeframe": "Before any acceptance-supporting verdict is recorded — this condition gates every acceptance path per the red-lines gate."
     },
     "owner": "operator (sole; explicitly not agent-dischargeable)"
    }
   ]
  },
  {
   "id": "R4-candidate-sha-binding-failure",
   "lens": "requirements-traceability-auditor, human-automation-handoff-auditor, cloud-native-purist, chesterton-gate",
   "priority": "P1",
   "basin": "Exact-SHA requalification not met at 00e5146: the candidate cannot name itself and no required surface was evaluated there",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "requirements-traceability-auditor:candidate-sha-unbound-in-packet",
    "human-automation-handoff-auditor:ready-mark-act-has-no-owner-and-wrong-sha",
    "cloud-native-purist:managed-requalification-forfeited",
    "chesterton-gate:the-freeze-cannot-name-itself"
   ],
   "justification": "The verdict is requested against 00e5146, and at that SHA the dossier-verified table shows zero packet artifacts naming it: five JSONs stamp e8a476c, clean-baseline.json is absent (a dangling evidence_paths reference cited by a P1-consequence claim), the matrix/reconciliation there miss PR #194's rows so #191's 'ALL reconciled on ONE exact SHA' holds only at the packet head, and the README's SHA table never contains the candidate literal in either tree. No CI of any kind has ever evaluated 00e5146; the only green on the chain is CodeQL at the two PR heads. haha's live read makes closure unreachable as the branch stands: no open PR head equals the candidate, so no pull event can ever evaluate it, and the ready-mark act is classified by no governing source. cnp proves the managed alternative (workflow_dispatch at a scratch branch ref) was armed, documented for exactly this purpose, exercised three days prior, and forfeited. chesterton-gate's reframe is accepted as the structural cause (self-describing artifacts committed into the tree they describe force a one-commit identity lag) — cause noted, defect stands against #191's contract as written. This is decisive for the question as posed: a GO 'against THAT SHA' would certify an identity the frozen set cannot establish and a requalification that never occurred there.",
   "acceptance_criteria": [
    {
     "condition": "Re-freeze so that ONE SHA carries a self-consistent packet: either a format change (placeholder + digest manifest, SHA bound at verification) so the freeze names itself, or an explicit declaration that the packet-head tree is the reviewable subject; README names the subject SHA literally; every evidence_paths entry exists in that tree; required surfaces (stdlib-checks, mission-custody contract, release-security) evaluated at that exact SHA via workflow_dispatch on a scratch branch, with {run_id, job_id, head_sha, conclusion} recorded, read per RELEASING.md:114-124 required-job semantics.",
     "falsifier": {
      "method": "Check out the declared subject SHA in isolation; read exact_start_sha/candidate_sha from all five artifacts; verify evidence_paths existence; grep README for the literal SHA; fetch the named workflow runs and compare head_sha.",
      "threshold": "All artifacts stamp the subject SHA, zero dangling evidence paths, README contains the literal, and each required job executed (conclusion != skipped) at head_sha == subject SHA. Any mismatch leaves the defect standing.",
      "timeframe": "At the next freeze, before the replacement packet is submitted for an independent verdict."
     },
     "owner": "agent executes; operator classifies the scratch-branch-push and dispatch acts (default-deny until classified, per gate act-hygiene)"
    }
   ]
  },
  {
   "id": "R5-immutability-without-mechanism",
   "lens": "entropy-demon, chesterton-gate, human-automation-handoff-auditor, cloud-native-purist",
   "priority": "P1",
   "basin": "Immutable-packet claim has no anchor, no detector, an undisclosed post-freeze mutation, and a destructive regeneration recipe",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "entropy-demon:immutable-packet-has-no-owner-no-anchor-no-oracle",
    "chesterton-gate:immutability-fence-deleted-by-its-own-restamp",
    "human-automation-handoff-auditor:no-checkout-reproduces-the-frozen-packet",
    "cloud-native-purist:packet-not-reproducible-from-its-own-recipe"
   ],
   "justification": "#191 names 'an immutable packet' as a terminal-contract element. Four verified chains converge: (1) no content hash exists anywhere in the packet and the validator accepted wholly fabricated SHAs plus a deleted evidence file (entropy-demon tamper probe, corroborated by rta M1/M2); (2) the coordinate is perishable — 00e5146 is reachable on origin only through the draft-PR working branch, no tag, no PINS entry, so the packet's own rollback ('abandon the branch') orphans the SHA every claim names; (3) the freeze was already mutated once post-commit (5-artifact restamp via an asserted --sha literal that the candidate tree's generator does not contain), the mutation is disclosed nowhere in the packet, and the same edit deleted the README's self-limiting disclaimer and its SHA-is-an-observation invariant — the fence was removed by the act it warned against; (4) the documented Regenerate recipe, run verbatim, silently rewrites candidate_sha to a different SHA and exits 0 (two independent probes). Kernels preserved: clean-baseline/custody evidence embed full stdout (self-corroborating); v6_run_clean_baseline.py still observes its SHA via git rev-parse; the restamp's direction was corrective. entropy-demon's pin-tag-vs-forbidden_this_run conflict is escalated to the operator, not assumed (ledger C5).",
   "acceptance_criteria": [
    {
     "condition": "(a) A pin tag (repo pin/ convention) anchored to the subject SHA and registered in check_pin_tags.py PINS — created only after the operator resolves whether forbidden_this_run's 'tag' covers non-version pin tags; (b) per-file sha256 digests (or a packet manifest) plus the candidate tree SHA in source-inventory.json, verified by validate_v6_assurance.py alongside cross-artifact SHA agreement and evidence-path existence; (c) a KL-RESTAMP known_limit disclosing the 5-artifact restamp, the post-freeze addition of clean-baseline.json, and restoring the deleted disclaimer's substance; (d) the generator refuses to overwrite a committed packet whose candidate_sha differs, absent an explicit --restamp flag.",
     "falsifier": {
      "method": "Re-run the tamper probe (fabricate all SHA fields, delete a cited evidence file, run the validator); list origin tags and peel them; grep PINS; run the README Regenerate command verbatim in a scratch copy and git-diff the packet directory.",
      "threshold": "Validator exits non-zero on tampering; one origin tag peels to the subject SHA and appears in PINS (or a recorded operator ruling forbids the tag, with an alternative durable anchor recorded); regeneration is byte-stable or fails loudly naming the SHA mismatch.",
      "timeframe": "Before operator acceptance; the tag/PINS check re-run again before any PROMOTION_RUN."
     },
     "owner": "agent (manifest, validator, disclosure); operator (pin-tag classification and creation)"
    }
   ]
  },
  {
   "id": "R6-tracker-reconciliation-citation-only",
   "lens": "requirements-traceability-auditor, chesterton-gate, entropy-demon, cloud-native-purist",
   "priority": "P1",
   "basin": "CLM-TRACKER-RECONCILED PROVED on a strong statement its oracle cannot test; 46 tracker rows structurally incapable of failing",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": [
    "requirements-traceability-auditor:tracker-reconciled-proved-but-false",
    "chesterton-gate:tracker-assurance-fields-are-form-without-function",
    "entropy-demon:reconciliation-decays-by-default-with-no-detector",
    "cloud-native-purist:tracker-rows-are-hardcoded-generator-state"
   ],
   "justification": "Four lenses, one basin, mechanically identical measurements independently obtained: 46/46 tracker rows share ONE falsifier string; oracle == release_consequence byte-identical on 46/46; zero evidence_paths keys; 17/46 identical DEFAULT_ISSUE notes; blocked_by empty on all 46 including all 7 blocked-parent rows; unknown issues silently absorb a false agent-owned custody default with no warning (probe-confirmed by two lenses, dispatcher-corroborated at #5's mechanism level). CLM-TRACKER-RECONCILED asserts 'explicit evidence-backed disposition, not a citation-only mention' — #191's own strong wording — while its oracle tests only count-equality plus field presence. On the strong reading the PROVED marker is false, and per this run's calibration a false PROVED claim is decisive: it is one of only three PROVED class claims and the packet's sole implementation of #191's reconciliation requirement. QUALIFICATIONS (the dissent-bearing kernels, preserved): the census SET is exactly right at the packet head (41 issues + 5 PRs, live-verified by three seats independently); the weak reading ('every open item appears with phase, disposition, owner') is true and provable; live-derivation is the correct architecture; 31 rows honestly self-label UNPROVED. The defect is a strong statement standing over a weak oracle — the honest repair is demotion or real per-item content, never shrinking the census or inflating statuses.",
   "acceptance_criteria": [
    {
     "condition": "Either (a) demote CLM-TRACKER-RECONCILED from PROVED and rewrite its statement to match what its oracle tests, relabeling the tracker section as a disposition census; or (b) keep the strong statement and populate per-item oracles distinct from release_consequence, materially differentiated falsifiers, resolvable evidence paths, and non-empty blocked_by on the 7 blocked-parent rows. Additionally: the generator fails (or loudly warns, with the count recorded in the artifact) on any tracker item absent from ISSUE_DISPOSITIONS.",
     "falsifier": {
      "method": "Parse the re-submitted matrix/reconciliation: count distinct falsifier strings, rows with oracle != release_consequence, rows with non-empty evidence_paths, blocked-parent rows with non-empty blocked_by; run the generator with a stub tracker containing an unknown issue number.",
      "threshold": "Path (a): status != PROVED and statement matches oracle. Path (b): distinct falsifiers >= 20, oracle != release_consequence on >= 40/46, non-empty evidence_paths on >= 40/46, 7/7 blocked-parent rows name a blocker. Both paths: unknown issue produces non-zero exit or a recorded warning count. Anything at or near 1/0/0/0-and-silent leaves the defect standing.",
      "timeframe": "At re-submission; reconciliation re-run (or re-dated) within 24h of operator acceptance since it decays from the next filed issue."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R7-wf-path-coverage-proved-row",
   "lens": "cloud-native-purist vs chesterton-gate",
   "priority": "P2",
   "basin": "CLM-WF-PATH-COVERAGE: PROVED row whose own falsifier fires (named factual conflict)",
   "ruling": "SPLIT",
   "status": "open",
   "merged_finding_ids": [
    "cloud-native-purist:proved-path-filter-claim-false",
    "chesterton-gate:proved-claim-labels-a-risk-its-oracle-cannot-see"
   ],
   "justification": "Ruled explicitly per the dispatcher memo; full dissent record in ledger C1. On the statement-truth limb the evidence weight favors cloud-native-purist: the claim reads 'each CI workflow's path filter is a superset of the files its steps read or execute'; check_public_content.py's input set is the whole tracked tree (git ls-files, dispatcher-confirmed anchor) while the filter covers 1395/1467 files, and cnp satisfied the claim's OWN stated falsifier by probe (seeded defect in an unfiltered file: gate exits 1, no dispatch occurs) — the claim's own falsifier is the correct oracle for a matrix row. chesterton-gate's limb is also upheld on its kernel: the audit's zero-findings is internally consistent with its narrow literal-token oracle, and independently of statement-truth the row's release_consequence ('silent skip risk on release gate suites') overreaches — both live silent-skip mechanisms (draft gating, fail-fast short-circuiting) are invisible to a static path-filter audit. The divergence is over the construction of 'files its steps read'; I do not average it away: under either construction the PROVED status is untenable (false on cnp's construction; consequence-overread on cg's), so the defect stands. Priority recalibrated to P2 rather than cnp's P1 because the falsity is contested on construction and the flagship-claim harm is misleading labeling, remediable by demotion or trigger-widening — not a concealed surface like R2. Kernel: the claim's real, mechanically checkable falsifier is exactly what made adjudication possible; do not soften it into unfalsifiability.",
   "acceptance_criteria": [
    {
     "condition": "Either (a) remove the paths: blocks from epistemic-flexibility.yml's pull_request/push triggers (matching the repo's own adjudicated treatment of release-security.yml), making the statement true; or (b) demote CLM-WF-PATH-COVERAGE to PARTIAL with a known_limit enumerating the 72 uncovered tracked files. In both paths: narrow the release_consequence to the property actually proved (path-filter dispatch coverage) and add a separate honest-status claim for draft-gating and fail-fast skip risk; strengthen v6_audit_workflow_oracles.py to classify whole-tree readers (git ls-files walks) as requiring unfiltered triggers.",
     "falsifier": {
      "method": "At the re-frozen tree: evaluate the changed-file set of a scratch PR confined to a previously-unfiltered file against the triggers (or re-run cnp's fnmatch evaluation); parse the matrix row's status and release_consequence.",
      "threshold": "Path (a): zero tracked files outside the filter (filter absent). Path (b): status == PARTIAL with the 72-file limit recorded. Both: release_consequence no longer claims silent-skip coverage. A PROVED status with the current statement and filter leaves the defect standing.",
      "timeframe": "At re-freeze; the row edit necessarily produces a new SHA, so it cannot be discharged as a condition on 00e5146."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R8-ready-for-review-takeover-absent",
   "lens": "human-automation-handoff-auditor",
   "priority": "P1",
   "basin": "KL-DRAFT-CI's sole compensating control (ready-mark takeover) does not exist in the trigger configuration",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "human-automation-handoff-auditor:ready-for-review-takeover-does-not-exist"
   ],
   "justification": "Unique chain, dispatcher-confirmed at anchor level (re-verification #1): five of six workflows declare bare pull_request: (default types exclude ready_for_review); only non-gating dco.yml declares the type, with the in-tree rationale proving the maintainers know the mechanism. KL-DRAFT-CI — the packet's only compensating control for its largest evidence gap, load-bearing for two self-labeled P1-consequence claims and for the security-class secret scan — promises 'Local clean-room is the BUILD oracle until the PR is marked ready', a takeover the repository's triggers cannot deliver: marking either draft ready dispatches nothing, the skipped checks persist, and GitHub treats a skipped required check as satisfied, so the misread is merge-permissive. All ten freeze-branch runs are skipped; the takeover has never been drilled. P1 upheld at the lens's placement: the mitigation is not overstated, it is absent, which makes the packet's central disclosed-gap-plus-mitigation pairing untruthful as frozen. Kernel preserved: draft state correctly refuses false green today; the fix must keep drafts visibly non-qualifying.",
   "acceptance_criteria": [
    {
     "condition": "Add types: [opened, synchronize, reopened, ready_for_review] to the pull_request trigger of the five gating workflows (mirroring dco.yml), then drill once on a throwaway draft PR and retain the transcript. Until the drill transcript exists, strike 'until the PR is marked ready' from KL-DRAFT-CI and state that no pull-event path to required-job green exists on this branch without a new commit or PR.",
     "falsifier": {
      "method": "On a throwaway branch touching trigger paths, open a draft PR, record check-runs, mark ready with no push, re-list workflow runs/check-runs at the identical head SHA (haha's drill, verbatim).",
      "threshold": "At least one new workflow run created by the ready_for_review action for each gating workflow at the unchanged head SHA, gating job conclusion != skipped. Zero such runs — or an unamended KL-DRAFT-CI without the transcript — leaves the defect standing.",
      "timeframe": "Single drill, under fifteen minutes, before re-submission; branch deleted afterwards."
     },
     "owner": "agent (workflow edit + drill); operator classifies the ready-mark act itself in the two-stage boundary (unclassified acts are default-deny)"
    }
   ]
  },
  {
   "id": "R9-cleanroom-undercoverage",
   "lens": "human-automation-handoff-auditor, entropy-demon, cloud-native-purist, requirements-traceability-auditor",
   "priority": "P2",
   "basin": "Clean-room BUILD oracle under-coverage and KL-DRAFT-CI overstatement",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "human-automation-handoff-auditor:build-oracle-reports-numerator-without-denominator",
    "entropy-demon:build-oracle-decays-silently-with-no-completeness-invariant",
    "cloud-native-purist:build-oracle-blind-to-the-surfaces-the-freeze-changed",
    "requirements-traceability-auditor:kl-draft-ci-understates-and-overstates"
   ],
   "justification": "One basin, four convergent independent measurements: cleanroom_ci.sh hardcodes one of six workflow files, its regex extracts 34 of 53 python-invoking lines there (19 unextracted at every chain SHA — including the public-content gate this very commit edited and the compile block it extends with its own scripts), reports a bare numerator with no denominator, covers release-security at 0% by construction (Go toolchain), and has no completeness invariant so coverage decays silently. A second extractor (v6_collect_candidate_evidence.py) repeats the class behind a floor assert. KL-DRAFT-CI names 2 skipped jobs where live evidence shows 5, and calls this 'the BUILD oracle' unqualified. Held at P2, not P1, because the actual state was independently checked for THIS run — the dispatcher's re-runs of the missed steps were green at 00e5146 — so the defect is oracle inadequacy plus mitigation overstatement, not concealed red. The mitigation-nonexistence limb is ruled separately at P1 (R8); chesterton-gate's fail-fast-blindness limb (the harness runs steps independently and cannot observe CI short-circuiting) is folded in here as an additional coverage-semantics gap. Kernel preserved on all four reports: extraction-over-duplication is the correct architecture; add the invariant, never a hand-maintained step list.",
   "acceptance_criteria": [
    {
     "condition": "cleanroom_ci.sh (or the workflow-oracle audit) gains a completeness assertion — every python-invoking line in the workflow is either extracted or on an explicit, justified in-repo exclusion list, failing on divergence — and prints extracted-of-total plus the workflows it does not read; argparse-usage SKIPs counted into the headline; KL-DRAFT-CI rewritten to name all five skipped gating jobs and the measured scope (34 of 53 lines of one of six workflows), and to note that independent step execution cannot observe CI fail-fast ordering.",
     "falsifier": {
      "method": "Apply the extractor regex at the re-frozen tree against the workflow; diff extracted set vs full enumeration; grep for the completeness assertion and run the harness after commenting out one extractable step's indentation.",
      "threshold": "The harness fails (or lists the exclusion) when counts diverge, and its output states numerator and denominator; KL-DRAFT-CI enumerates 5/5 skipped jobs. A bare 'N passed' with a non-empty unlisted complement leaves the defect standing.",
      "timeframe": "At re-submission; re-check on every edit to epistemic-flexibility.yml."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R10-rollback-premise-main-red",
   "lens": "chesterton-gate",
   "priority": "P2",
   "basin": "Rollback plan's safe harbour (main) is live-red on its required gate, undisclosed",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": [
    "chesterton-gate:rollback-fence-rests-on-a-red-main"
   ],
   "justification": "Unique chain, dispatcher-reproduced (re-verification #3): at main's head a2b9c0d, check_public_content.py exits 1 with exactly the two private-fleet-repo-name defects the candidate's allowlist edit exempts, and GitHub's own job record (run 32107889882) shows the required stdlib-checks job failed at the Public-content step with eleven downstream release-gate steps skipped and never executed on main's head. The packet's rollback ('abandon the branch; main remains the last PROMOTION-valid channel') rests on this unstated, false premise, and nowhere discloses that the defect breaking main is the one the candidate silences. UPHELD on the omission; QUALIFIED on severity — recalibrated from the lens's P1 to P2 because the sentence is arguably a process-law channel designation rather than a CI-state claim, the repair is purely additive disclosure touching no code, and the falsity does not corrupt any evidence about the candidate itself. chesterton-gate's P1 placement is preserved as recorded dissent: if this were the last open item it would still bar acceptance until disclosed. Kernel: never fix by merging the candidate or softening 'do not merge'.",
   "acceptance_criteria": [
    {
     "condition": "A known_limit (kind: integrity) recording that origin/main is red on required stdlib-checks at the Public-content step, that eleven downstream release-gate steps have not executed on main's head, and that this candidate line is the in-flight fix; the rollback sentence qualified accordingly.",
     "falsifier": {
      "method": "Grep the re-submitted packet's known_limits for the main-red disclosure; independently re-read the newest push run on main (list_workflow_runs branch=main, then job/step conclusions) at the moment of operator acceptance.",
      "threshold": "Disclosure present AND consistent with the live state at acceptance time (a subsequent green push to main retires the disclosure need and falsifies the finding). Missing disclosure with main still red leaves the defect standing.",
      "timeframe": "Disclosure at re-submission; live re-check at the moment of operator acceptance."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R11-public-content-gate-silenced",
   "lens": "entropy-demon, chesterton-gate, cloud-native-purist",
   "priority": "P2",
   "basin": "Public-content gate: whole-file permanent allowlist widening on a live generator; self-falsifying recorded evidence; pasted-stdout substrate",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "entropy-demon:allowlist-is-a-permanent-unowned-whole-file-hole",
    "chesterton-gate:public-content-fence-silenced-rather-than-remediated",
    "cloud-native-purist:evidence-is-pasted-stdout-from-a-mutable-dev-host",
    "entropy-demon:allowlist-has-no-review-cycle-inert-entries-persist"
   ],
   "justification": "Security-class basin with three convergent verified chains. (1) The candidate's response to a real detected violation (PR #192's 'ZMS-Labs/zms-homelab#1601' in two files) was to silence the detector, not remediate — opposite to the July-21 addendum's recorded relocation disposition for this exact class; is_allowlisted short-circuits before any pattern runs, so both files are exempt from all seven patterns permanently, and one is a live generator under .github/scripts/ that re-emits the string on every regeneration; the claim's closure_path mis-describes it as an 'ES6-ZI-001 parent-tracker' exemption. (2) entropy-demon's probe made the consequence concrete: five pattern classes pass undetected inside an allowlisted candidate-modified file, satisfying CLM-PUBLIC-CONTENT's own (unqualified) falsifier on a P1-consequence claim — while the control probe proved the patterns live elsewhere. (3) The claim's recorded evidence is self-falsifying (dossier-verified 39/39/41/41): public-content.json stamps e8a476c while its stdout's '41 allowlisted files' exists only from 00e5146 onward — produced on a dirty tree stamping a pre-freeze SHA, with no dirty-tree refusal anywhere (cnp's substrate finding). Held at the lenses' P2, not P1: the statement is honestly scoped 'outside exact-file allowlist', the claim is held at PARTIAL, the edit is diff-visible, and this run's independent re-runs confirmed exit 0 at both SHAs. Kernels preserved: fail-closed behavior, exact-file (not prefix) entries, RED-seed self-test, full-stdout capture.",
   "acceptance_criteria": [
    {
     "condition": "(a) Either make allowlist entries pattern-scoped, or record a sha256 per allowlisted file at exemption time and fail closed when an allowlisted file changes without an allowlist-review update; or redact/relocate the parent_program string per the addendum's own disposition. (b) Correct CLM-PUBLIC-CONTENT's closure_path to state the true blast radius, and reconcile its falsifier text with its allowlist-scoped statement. (c) Regenerate evidence/public-content.json at the subject SHA on a clean tree (collector refuses on dirty git status), so stamped SHA and stdout are consistent. (d) Retire the three inert allowlist entries and record an owner/review cadence for the list.",
     "falsifier": {
      "method": "Re-run entropy-demon's seeded probe (append pattern-matching strings to an allowlisted, actively-edited file; run the gate and any accompanying guard); diff the evidence JSON's stamped SHA against its stdout allowlist count at that SHA; read the closure_path text.",
      "threshold": "Seeded content in an allowlisted file is detected by the gate or an accompanying integrity check; evidence SHA and stdout are mutually consistent; closure_path names both files and the exemption granularity. Gate exit 0 on the seeded probe with no guard leaves the defect standing.",
      "timeframe": "At re-submission; re-verify after any allowlist or scan_text change."
     },
     "owner": "agent implements; operator reviews the allowlist-policy decision (scrub vs allowlist is the operator's security call per the gate's RL-8 note)"
    }
   ]
  },
  {
   "id": "R12-operator-alert-channel",
   "lens": "human-automation-handoff-auditor",
   "priority": "P2",
   "basin": "Machine-readable blocker channel structurally drops operator-owned items",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "human-automation-handoff-auditor:operator-alert-channel-drops-operator-work"
   ],
   "justification": "Dispatcher-confirmed (re-verification #5): blocking_claims is a hardcoded nine-id whitelist filtered by !PROVED; the four BLOCKED operator-owned claims (CLM-ISSUE-104/84/40/186) structurally cannot enter it, #84 and #40 have no known_limits entry at all, and the packet's own self-inconsistency (dossier-verified) omits CLM-ORACLE-REJECT and CLM-MC-HOOK-POSIX — both PARTIAL with self-labeled P1 release consequences — from blocking_claims. The probe further shows an unknown gate:operator issue is silently stamped owner=agent with a false custody note. The drop is not random: the items that vanish from the machine-readable channel are exactly the ones requiring the operator to personally decide. README prose names the four holds, so this is misrouting rather than concealment — P2. Kernel preserved: the per-claim BLOCKED computation and honest owner values are correct; derive the summary from them.",
   "acceptance_criteria": [
    {
     "condition": "blocking_claims and known_limits derived from the matrix: every BLOCKED claim, every claim whose owner contains 'operator', and every claim whose release_consequence starts with P1 appears in blocking_claims or in a known_limits entry naming it (owner field added to known_limits); an issue absent from ISSUE_DISPOSITIONS is a hard generator failure.",
     "falsifier": {
      "method": "Load the re-submitted promotion-packet.json and matrix; assert the derivation property over all claims; run the generator with a stub tracker containing an unknown gate:operator issue.",
      "threshold": "Zero unlisted BLOCKED / operator-owned / P1-consequence claims, and the unknown-issue run exits non-zero. Currently 4 BLOCKED unlisted, 2 holds without limits, 2 P1-consequence claims unlisted — any recurrence leaves the defect standing.",
      "timeframe": "At re-submission; one command against the committed artifacts."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R13-no-acceptance-procedure",
   "lens": "human-automation-handoff-auditor",
   "priority": "P2",
   "basin": "The terminal state names a human act with no defined procedure, acceptor, or record",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "human-automation-handoff-auditor:no-operator-acceptance-procedure-exists"
   ],
   "justification": "Verified by tree-wide grep, live #191 read, and schema inspection: V6_CANDIDATE_READY_FOR_OPERATOR_ACCEPTANCE exists only in the schema enum, the validator conditional, and packet prose; #191 defines what must be true but never what acceptance consists of, who may accept, what the acceptor personally verifies, or what artifact records it; the schema has no accepted_by/accepted_at/provenance fields; ES6-ZI-001 shipped no promotion-packet.json, so this handoff has no precedent execution. Per the gate's binding condition, this verdict must state — and does — that because no operator-acceptance procedure exists, NO verdict of this run places the program in the terminal state, and even a GO would confer no promotion authority (RELEASING.md: publication is an explicit owner act; CONDITIONAL is not GO). Kernel preserved: the routing of the terminal act through an actor outside the implementing lineage is the right shape; specify the human, never remove them.",
   "acceptance_criteria": [
    {
     "condition": "A written operator-acceptance procedure in a repo- or operator-authored source: who may accept, what the acceptor personally verifies (the four operator holds and the R3 ratify-or-reverse decision among them), the artifact and schema fields (accepted_by, accepted_at, verdict provenance) recording it, and the explicit statement that BUILD-freeze acceptance authorizes nothing beyond recording the state.",
     "falsifier": {
      "method": "Grep the tree for the procedure document; inspect promotion-packet.schema.json for the acceptance/provenance fields; confirm the procedure names an acceptor and a recording artifact.",
      "threshold": "At least one procedure document naming acceptor + recorded-acceptance artifact, plus schema fields able to hold it. Observed today: none in tree, none in #191, none in schema.",
      "timeframe": "Before operator acceptance is requested of the replacement packet."
     },
     "owner": "operator (authors or approves); agent may draft"
    }
   ]
  },
  {
   "id": "R14-taxonomy-substitution-no-register",
   "lens": "requirements-traceability-auditor",
   "priority": "P2",
   "basin": "#191's enumerated claim/evidence classes substituted by an implementer taxonomy with no crosswalk; no requirement register",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "requirements-traceability-auditor:claim-class-taxonomy-substitution",
    "requirements-traceability-auditor:no-requirement-register",
    "requirements-traceability-auditor:required-job-claim-covers-subset"
   ],
   "justification": "Verified: #191 enumerates 8 claim classes and 16 evidence classes; the packet substitutes 15 self-chosen 'class claims' with no crosswalk; 'compatibility' maps to nothing (grep: 0), and migration/concurrency/performance/stability/hostile-input/lifecycle have no class claim. Because coverage is reported in the substituted vocabulary, 'covers every material claim' is unfalsifiable as written — the structural root cause of R2's orphan and undetectable by the validator, whose only coverage walk is reconciliation→matrix (one direction of a three-way trace). CLM-REQUIRED-JOB's PROVED-over-a-2-of-6-workflow subset is folded in as a symptom (scope overclaim, not falsity — rta's own P3 calibration accepted). Kernel preserved: the 15 existing class claims are real work at a high standard; add the crosswalk and missing classes at that standard, do not dilute.",
   "acceptance_criteria": [
    {
     "condition": "A committed requirement register / crosswalk keyed to #191's clause ids and RELEASING.md gate items, mapping each of the 8 claim classes and 16 evidence classes to covering claims or explicit NOT-APPLICABLE dispositions with reasons; a compatibility class claim added; validator fails on any registered requirement with neither claim nor disposition; CLM-REQUIRED-JOB's subject widened to all six workflows or its statement narrowed.",
     "falsifier": {
      "method": "For each enumerated class/gate item, search the register and matrix for the mapped claim or disposition; run the validator against a register entry with the mapping deleted.",
      "threshold": "Every named class maps to at least one claim or recorded N/A; validator exits non-zero on the deleted mapping. Any unmapped class (compatibility today) leaves the defect standing.",
      "timeframe": "Before the next candidate freeze is submitted."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R15-custody-residual-undisclosed",
   "lens": "chesterton-gate",
   "priority": "P2",
   "basin": "es#137 fixes sound (H6 killed) but a residual lexical-vs-realpath false-allow class is undisclosed and its deleted rationale unrestored",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": [
    "chesterton-gate:deleted-safe-direction-fence-in-guard-normalization"
   ],
   "justification": "The exculpatory half is ruled first and matters: H6 is killed by two independent lenses (entropy-demon re-ran all five custody modules green at the candidate; chesterton-gate reconstructed the deletions as exemplary, documented fence discipline with a two-directional replacement test), and the dispatcher confirmed the test-deletion lineage (re-verification #4). The custody code is the candidate's healthiest surface. What stands, probe-demonstrated live at 00e5146: guard matching collapses '..' lexically while the filesystem resolves after symlinks, so a write whose realpath lands inside a guarded tree can fail to match an armed guard — pre-existing (reproduced at a2b9c0d), polarity-flipped from the hedge the deleted comment recorded, outside CLM-MC-137's honest tight scope, and disclosed nowhere in the packet on a headline security risk class. QUALIFIED: this is a disclosure defect, not a fix defect; behavior must not change inside a freeze. Kernel preserved: the scope/guard normalization split and its reconstructive docstrings.",
   "acceptance_criteria": [
    {
     "condition": "A known_limit plus a LIMITED matrix row recording that guard path matching is lexical and can diverge from filesystem resolution through symlinked parents, with the concrete probe as evidence; the deleted safe-direction reasoning reinstated as a comment at _collapse_parent_segments. No matching-behavior change in this freeze.",
     "falsifier": {
      "method": "Grep the re-submitted packet for the limit/row; run chesterton-gate's symlink-and-parent-segment battery in the candidate worktree comparing evaluate()['matched'] against realpath containment.",
      "threshold": "The limit and row exist and cite the probe; the battery still demonstrating >= 1 divergence case with no disclosure leaves the defect standing (zero divergence cases would instead falsify the finding itself).",
      "timeframe": "At re-submission; probe runs in under a second."
     },
     "owner": "agent"
    }
   ]
  },
  {
   "id": "R16-promotion-disarm-undisclosed-burden",
   "lens": "human-automation-handoff-auditor",
   "priority": "P3",
   "basin": "Operator-facing limit understates the PROMOTION disarm/re-arm burden; never rehearsed",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "human-automation-handoff-auditor:promotion-disarm-burden-undisclosed-and-undrilled"
   ],
   "justification": "Verified against KL-OPERATOR-186 vs RELEASING.md steps 7-10: 'tag creation still operator-owned' compresses away that authorization IS the disarm — remove the tag ruleset, tag, re-arm in the same sitting, verify by seeded probe — and a grep finds no rehearsal discipline anywhere. Correctly held at P3 by the lens: PROMOTION is out of scope for this verdict; the in-scope defect is the honesty of the BUILD handoff brief. Kernel: RELEASING.md's own no-bypass-actors and seeded-probe reasoning is the asset to surface, not simplify. P3: no acceptance criteria required; carry into the fix ticket as quality.",
   "acceptance_criteria": []
  },
  {
   "id": "R17-frozen-detectors-non-gating-monitors",
   "lens": "entropy-demon",
   "priority": "P4",
   "basin": "Detectors frozen in time (gitleaks pin) and monitors that cannot fail (contract-macos)",
   "ruling": "UPHELD",
   "status": "open",
   "merged_finding_ids": [
    "entropy-demon:monitors-that-cannot-fail-and-detectors-frozen-in-time"
   ],
   "justification": "Verified: gitleaks v8.30.1 / go 1.25.1 pinned with check-latest:false and no owner or refresh cadence; contract-macos is dispatch-only and exits 0 on any measured outcome by its own comment. Foundational structural debt, honestly counterweighted by the lens itself: the repo's supply-chain pinning discipline (commit-SHA action pins, pinned runners and Python) is genuinely strong. macOS half disclosed (KL-MACOS-162); scanner-pin half undisclosed. P4: record owner + cadence; no acceptance criteria required at this tier.",
   "acceptance_criteria": []
  },
  {
   "id": "R18-packet-framing-steering",
   "lens": "chesterton-gate, requirements-traceability-auditor vs cloud-native-purist",
   "priority": "P3",
   "basin": "Implementer-authored packet framing (H8): anti-steering prose, but pre-named blocker set non-exhaustive and a regenerate-the-subject instruction embedded",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "status": "open",
   "merged_finding_ids": [
    "chesterton-gate:packet-supplies-the-panel-its-own-skepticism-script"
   ],
   "justification": "Ruled with the H8 tension preserved (ledger C6). cnp's kill is credited on the prose limb: gauntlet-request.md's directives are structurally anti-steering and its four premises live-verified true. cg/rta's limb stands on the mechanism that matters: verifying an implementer-authored audit plan feels like independent work precisely when its premises are true and adverse, and the pre-named set was demonstrably non-exhaustive — multiple P1s of this run (secret-scan orphan, red main, forgeable terminal gate, unreconciled merges) lie outside it; the concrete steering lives in machine-readable under-enumeration (KL-DRAFT-CI 2-of-5) and in '(regenerate if HEAD moved)', an instruction that, if followed, mutates the frozen subject during its own review (RL-6 held: no seat followed it). P3 quality/method: remove the regenerate instruction; record for future runs that implementer-authored packets require budgeted out-of-set search. The under-enumeration and regeneration defects are already carried as acceptance criteria under R2/R9 and R5.",
   "acceptance_criteria": []
  }
 ],
 "conflict_ledger": [
  {
   "parties": "cloud-native-purist (P1 proved-path-filter-claim-false) vs chesterton-gate (P3 proved-claim-labels-a-risk-its-oracle-cannot-see)",
   "conflict": "Is the PROVED matrix row CLM-WF-PATH-COVERAGE ('each CI workflow's path filter is a superset of the files its steps read or execute') FALSE, or narrowly true but consequence-overread? Direct factual conflict named by the dispatcher for explicit ruling.",
   "evidence_weight": "cnp: [V] anchors dispatcher-confirmed (check_public_content.py runs git ls-files over the repo root; finite paths: filter) plus recorded [I] probe work satisfying the claim's OWN falsifier (1467 tracked / 1395 filtered / 72 outside; seeded defect in an unfiltered file → gate exit 1, no dispatch; oracle audit 0 findings by construction via .github/scripts allowlist). cg: [V] claim/consequence text plus live [I] job-record read of the two silent-skip mechanisms the audit cannot see. Both chains verified; neither refutes the other's observations — they diverge on the construction of 'files its steps read or execute'.",
   "ruling": "SPLIT",
   "valid_kernel_a": "cnp: under the plain reading, and under the claim's own stated falsifier — the correct oracle for a matrix row — the statement is false: a whole-tree-reading step's workflow filter covering 1395/1467 files is not a superset of its input set, and the audit cited as proof is structurally blind to it. The row cannot stand as PROVED.",
   "valid_kernel_b": "cg: the audit's zero-findings is internally consistent with its narrow literal-token oracle, so on the narrowest construction the audited property holds; independently, the row's release_consequence ('silent skip risk on release gate suites') overreaches on ANY construction, since draft gating and fail-fast short-circuiting — both live — are invisible to a static path-filter audit.",
   "synthesis": "The verdict does not need to force one construction to compute: under cnp's construction the row is false; under cg's it is a narrow truth mislabeled with a broad retired-risk consequence. Either way the PROVED status is untenable and the defect is open (R7, recalibrated P2). Repair paths: demote to PARTIAL with the 72-file limit, or remove the paths filters per the repo's own release-security precedent — plus narrow the consequence text on both paths.",
   "dissent_preserved": "cg's position that 'its narrow statement is true' is recorded verbatim and NOT averaged away; cnp's P1 calibration (false PROVED row = decisive) is recorded as the stricter proposal the judge declined on construction-ambiguity grounds. If a future round establishes a single authoritative construction of 'files its steps read', the losing limb's severity must be recomputed, not assumed.",
   "residual_tension": "The governing contract nowhere defines 'files its steps read or execute' for whole-tree scanners; until the requirement register (R14) defines it, the same dispute will recur on every freeze.",
   "justification": "Ruled on evidence quality: cnp's probe satisfied the claim's own falsifier (the agreed oracle), which outweighs a defense resting on a narrower construction the claim text does not state; cg's overread limb is independently verified and survives regardless. Both kernels are load-bearing in the fix."
  },
  {
   "parties": "chesterton-gate (lens verdict CONDITIONAL) vs human-automation-handoff-auditor, entropy-demon, cloud-native-purist, requirements-traceability-auditor (lens verdicts NO-GO)",
   "conflict": "Whether the frozen packet at 00e5146 can be accepted with conditions (disclosure repairs, no code changes) or must be refused at this SHA.",
   "evidence_weight": "Not a vote: 4-1 carries zero arithmetic weight. Weighed chains: cg's CONDITIONAL rests on verified kernels (honest NOT_READY posture, refused self-certification, healthiest-surface custody code, all its own blockers being disclosure repairs). The NO-GO side rests on verified chains that conditions on THIS SHA cannot discharge: the candidate tree cannot name itself, required surfaces were never evaluated there, the terminal gate is forgeable, and any correcting edit necessarily produces a different SHA (cnp's explicit point; cg's own fix set ends 'Re-freeze at a SHA whose own tree names it, then re-run this gate').",
   "ruling": "OVERRULED",
   "valid_kernel_a": "cg: the packet's honesty structure is real and the repair cost is low — nothing in the record suggests the underlying code is unsound (custody suite green at the exact candidate under two independent re-runs; dispatcher re-ran the clean-room-missed steps green). A re-frozen packet executing the fix set could plausibly clear quickly.",
   "valid_kernel_b": "The four NO-GO lenses: a verdict 'against THAT SHA' cannot be CONDITIONAL when the conditions require a new SHA; and the gate independently caps this record at NO-GO (RL-1b: unresolved merge-consent chain; GO unavailable; no acceptance without operator ratify-or-reverse).",
   "synthesis": "cg's CONDITIONAL is functionally a NO-GO-at-this-SHA with a favorable prognosis for the successor freeze — its own terminal condition concedes the re-freeze. The verdict records the prognosis without laundering it into the verdict enum.",
   "dissent_preserved": "chesterton-gate's CONDITIONAL, its reasoning, and its assessment that all its named blockers are packet-disclosure repairs touching no candidate code are preserved here in full and were not averaged into the computation. Its H6-kill (custody fixes exemplary) and H1-reframe (identity lag is structural, not accidental) stand as recorded qualifications on R15 and R4.",
   "residual_tension": "None material once 'against THAT SHA' is fixed as the question; the tension was over verdict semantics, not facts.",
   "justification": "The mechanical gate computes the verdict from open P1 rulings, and seven stand open at 00e5146; separately the red-lines gate caps any acceptance path pending the operator's merge ruling. CONDITIONAL is unreachable on both grounds."
  },
  {
   "parties": "All five lenses (H7 disclosure-adequacy attacks) vs the packet's own self-disclosures (H7 null/defense: honest NOT_READY freeze with disclosed gaps)",
   "conflict": "The packet claims — and the docket's null hypothesis defends — that its gaps are disclosed (NOT_READY, refused self-certification, 9 blocking claims, 8 known limits). The findings assert material gaps outside every disclosure channel.",
   "evidence_weight": "Refusal limb: [V] schema const + validator enforcement + empty requested_irreversible_acts + untouched main + generation-enforced UNPROVED on CLM-INDEPENDENT-GAUNTLET — verified by multiple seats. Disclosure limb: [V]-anchored, largely dispatcher-confirmed absences — no secret-scan row/limit (R2), no merge disclosure incl. #192 absent everywhere (R3), no restamp disclosure (R5), KL-DRAFT-CI naming 2 of 5 skipped jobs with a nonexistent mitigation (R8/R9), blocking_claims omitting 4 BLOCKED operator-owned and 2 self-labeled-P1 claims (R12), no main-red disclosure (R10), no custody-residual row (R15).",
   "ruling": "SPLIT",
   "valid_kernel_a": "The refusal limb of H7 SURVIVES and is genuinely unusual: the honest state is produced automatically, the packet performs zero irreversible acts, publishes unflattering statuses (31 UNPROVED tracker rows, 1 UNPROVED-by-construction), and no seat found a self-authored GO anywhere.",
   "valid_kernel_b": "The disclosure-adequacy limb is KILLED on at least seven independent chains: the largest disclosed gap is paired with a compensating control that does not exist, and the material undisclosed set (secret scan, merges, restamp, main-red, terminal-gate impotence, custody residual) exceeds the disclosed set in consequence.",
   "synthesis": "'Refuses to self-certify' and 'discloses its own gaps' are different properties; the packet has the first and has been credited with the second on the strength of the first (rta's formulation, adopted). The verdict credits the refusal posture as a preserved kernel in nearly every ruling while refusing to let it stand in for disclosure.",
   "dissent_preserved": "The packet's honest-posture evidence is recorded as validation kernels across R1-R15 and must survive every fix; entropy-demon's and cnp's explicit statements that the packet is 'honest about what it names' are preserved against any reading of this verdict as an integrity accusation against the freeze's posture.",
   "residual_tension": "H8 interaction: the honesty of the named disclosures is exactly what anchored review attention at the disclosed gaps (cg's method finding, R18) — an honest-posture packet can still under-enumerate.",
   "justification": "Ruled on the falsifier the docket itself set for H7: 'one PROVED-status claim shown false, or one material undisclosed gap.' The record contains at least one of the first (R6; R7 contested) and several of the second."
  },
  {
   "parties": "requirements-traceability-auditor (build-window-merges, as filed) vs dispatcher mechanical re-verification (Step-6 correction)",
   "conflict": "rta's finding asserted 'no claim, no reconciliation row, no known-limit, no disclosure' for all three BUILD-window merges; the dispatcher verified the no-claim limb is WRONG for #190 (cited in CLM-RELEASE-AUTH/CLM-REQUIRED-JOB/CLM-MC-MACOS-CASE) and #156 (cited in CLM-RELEASE-AUTH).",
   "evidence_weight": "Dispatcher correction: [V] direct reads of the matrix authority/independence fields. rta's standing limbs: [V] parse of reconciliation PR rows {100,103,176,193,194} and packet-wide grep — no row/disposition for any of the three, #192 absent from every packet artifact; live merge metadata and operator non-approval text verified.",
   "ruling": "UPHELD-WITH-QUALIFICATIONS",
   "valid_kernel_a": "rta: the load-bearing limbs survive intact, and the citation-without-reconciliation state of #190/#156 is itself the exact failure mode #191 pre-named ('reconcile and not merely cite') — the correction narrows the finding while sharpening its irony.",
   "valid_kernel_b": "Dispatcher: the overstatement was real and material to fairness; a finding that would brand the packet as never mentioning #190/#156 misstates the record.",
   "synthesis": "R3 is ruled on the standing limbs only, exactly as the arbitration rules mandate; the corrected limb is recorded here so the fix ticket does not demand a 'claim' that already exists.",
   "dissent_preserved": "rta's original framing is preserved in its report; this ledger entry is the authoritative narrowing.",
   "residual_tension": "None; the correction was accepted without contest.",
   "justification": "Mandated correction applied (arbitration rule 4). The P1 severity is unaffected because it rested on the no-disposition and #192-absent limbs plus the unresolvable consent chain, all standing."
  },
  {
   "parties": "entropy-demon / cloud-native-purist fix-set recommendations (pin tag on the candidate; scratch-branch push + workflow_dispatch; ready-mark reclassification) vs exact-candidate-receipt forbidden_this_run and the operator-approved two-stage boundary",
   "conflict": "The highest-value fixes name acts the two-stage boundary does not classify: forbidden_this_run lists 'tag' (scope ambiguous for non-version pin tags), branch-push + dispatch at the candidate is unclassified, and the ready-mark act is classified in no governing source (haha's finding).",
   "evidence_weight": "[V] receipt forbidden_this_run text; [V] #191 boundary enumeration; entropy-demon explicitly escalates the pin-tag conflict rather than assuming scope; cnp argues branch-creation is not the operator-gated act (tag creation is) — an argument, not an authorization.",
   "ruling": "UPHELD",
   "valid_kernel_a": "The fixes are technically correct and cheap, and the substrates were built for exactly these purposes (workflow_dispatch comments; pin/ tag convention with check_pin_tags.py).",
   "valid_kernel_b": "The gate's act-hygiene rule: acts unclassified by the operator-approved boundary are default-deny for agents until classified; no fix-set item is itself agent-executable authority, and cnp's 'not the operator-gated act' reasoning must not be treated as consent.",
   "synthesis": "Every acceptance criterion in R2, R4, R5, and R8 that involves a push, dispatch, tag, or ready-mark is routed through explicit operator classification first; agent-executable items (validator code, disclosures, manifests, workflow-trigger edits on a draft branch) are separated from operator-gated ones in each criterion's owner field.",
   "dissent_preserved": "cnp's position that the branch-push/dispatch path is BUILD-scoped and fully reversible is preserved as the recommended reading for the operator to adopt — it is plausible and the workflows' own comments support it — but it is the operator's reading to adopt, not the panel's.",
   "residual_tension": "If the operator reads forbidden_this_run's 'tag' as covering pin tags, #191's immutable-packet requirement and the receipt prohibition are in direct conflict; entropy-demon's escalation stands: the operator must resolve which governs, and the resolution must be recorded.",
   "justification": "Consent precedes the irreversible extends forward: a review that just found an unresolvable consent chain (R3) must not itself seed the next one."
  },
  {
   "parties": "cloud-native-purist (H8 KILLED: gauntlet-request is structurally anti-steering) vs chesterton-gate P3 and requirements-traceability-auditor (H8 SUPPORTED: pre-named premises anchor the panel; '(regenerate if HEAD moved)' is a subject-mutation instruction)",
   "conflict": "Whether implementer-authored packet framing steered the review.",
   "evidence_weight": "cnp: [V] reads of the request's anti-steering directives; all four pre-named premises live-verified true. cg: [I] cross-check that both of its P1s — and in fact most of this run's P1 basins — lie outside the pre-named set; rta: [V] the regenerate instruction and the machine-readable under-enumeration (KL-DRAFT-CI 2-of-5).",
   "ruling": "SPLIT",
   "valid_kernel_a": "cnp: the prose is honest and points at independence; no directive in it was followed as an instruction (RL-6 held), and the premises it named were true.",
   "valid_kernel_b": "cg/rta: steering by pre-named true-and-adverse blockers is the strong form — confirming them consumes budget and feels independent — and the operative steering lives in machine-readable fields (selective enumeration) and in the regenerate instruction, not in tone.",
   "synthesis": "H8 resolves at the mechanism level: prose steering — killed; enumeration steering — demonstrated by the out-of-set P1 count. Method note recorded for future runs (R18): budget explicit out-of-set search on implementer-authored packets; strike regenerate-type instructions from frozen subjects.",
   "dissent_preserved": "cnp's kill is preserved as scoped to the prose limb it tested; it did not test the enumeration limb, and its own finding #2 (KL-DRAFT-CI under-enumeration) supplies evidence FOR the limb it did not frame as H8.",
   "residual_tension": "None operative for this verdict; carried as method doctrine.",
   "justification": "Both parties' observations are verified and non-contradictory; only their H8 framings collide. Split on limbs, no averaging."
  }
 ],
 "computed_verdict": "NO-GO",
 "verdict_gate_trace": "Mechanical computation per rule 6, then the gate cap. Open P1 rulings at subject SHA 00e5146e43ff9011153452b83fedda706723c52b: R1 (terminal gate accepts self-written GO with nine blockers standing), R2 (required security-class secret-scan surface unclaimed/unrun/undisclosed), R3 (three BUILD-window merges with unresolvable authorization, undisclosed; ruled on the dispatcher-corrected standing limbs; operator-resolvable only), R4 (candidate cannot name itself; zero required surfaces evaluated at the subject SHA; closure unreachable from current branch state), R5 (immutable-packet requirement unmet by mechanism; undisclosed post-freeze mutation; perishable coordinate), R6 (CLM-TRACKER-RECONCILED PROVED-but-false on #191's own strong reading), R8 (the packet's sole compensating control for its largest gap does not exist). Any open P1 => NO-GO; seven are open => NO-GO. Open P2s (R7, R9-R15) would independently yield CONDITIONAL and are moot for the enum. Independently and redundantly, the red-lines gate result (PASS-WITH-NOTES, RL-1b prima facie crossing) caps this record at NO-GO: GO is unavailable, and no acceptance-supporting verdict may issue unless its conditions include the operator explicitly ratifying or reversing the three merges — R3's acceptance criterion carries that condition verbatim. computed_verdict == gate computation == NO-GO. Binding statements required by the gate, hereby made of record: (1) this verdict is bound to run es-v6-candidate-freeze-2026-08-18, subject SHA 00e5146e43ff9011153452b83fedda706723c52b, and this ruling-set artifact — a bare independent_gauntlet='GO' enum flip in promotion-packet.json does not and cannot constitute this panel's verdict; (2) no operator-acceptance procedure exists (R13), so no verdict of this run places the program in the terminal state; (3) even a GO would confer no promotion authority — publication is an explicit owner act per RELEASING.md, CONDITIONAL is not GO, and this run satisfies no externally-enforced safety gate, whose separate record is still owed; (4) the fingerprint (222/222) certifies citation-anchor integrity only, not finding truth — truth support here rests on the dispatcher's independent mechanical re-verifications and on attacks satisfying the matrix rows' own falsifiers, and no packet-internal green (schema-only validator, 34/34 clean-room, PROVED markers) was credited as satisfying evidence by any seat or by this verdict. Honest labeling: NO-GO here means the frozen packet at THIS SHA cannot support the terminal state as argued in this bracket — it is not a finding that the code is unsound (custody is the record's healthiest surface, H6 killed twice over) nor that the freeze's refusal-to-self-certify posture is dishonest (it is real and validator-enforced). Heavy refutation of a first-of-its-kind promotion packet is progress.",
 "next_action": "Put ONE decision in front of the operator before any other work: explicitly ratify or reverse the three BUILD-window merges (#190, #156, #192) in a durable operator-authored artifact (R3 — the only item no agent can discharge, and the gate's precondition for every acceptance path), and in the same sitting classify the four unclassified acts the fix set needs (pin tag vs forbidden_this_run's 'tag'; scratch-branch push; workflow_dispatch at the candidate; draft-PR ready-mark). In parallel, agents may prepare — as draft work on the freeze branch, executing nothing operator-gated — the P1 fix set for the successor freeze: verdict-binding validator + schema fields (R1), CLM-SECRET-SCAN row and corrected KL-DRAFT-CI (R2, R8, R9), KL-RESTAMP disclosure + digest manifest (R5), CLM-TRACKER-RECONCILED demotion or real per-item content (R6), and a self-naming re-freeze plan (R4). One hygiene condition on this run's own record before it is committed or published: the report files embed the private-fleet scrub-target string, so the run record must pass check_public_content.py or receive an operator-reviewed scrub/allowlist decision first (gate RL-8).",
 "coverage_statement": {
  "capability_families_exercised": [
   "human-factors / automation-handoff auditing (human-automation-handoff-auditor, adversarial)",
   "maintainability / entropy-and-decay analysis (entropy-demon, adversarial wildcard)",
   "operability / managed-substrate verification (cloud-native-purist, constructive)",
   "process-integrity / requirements traceability (requirements-traceability-auditor, metatextual)",
   "process-integrity / fence-archaeology and deletion adjudication (chesterton-gate, metatextual)",
   "mechanical evidence verification (Sovereign Fingerprint 222/222 V-tags, 0 H-tags; 40/40 findings structurally clean)",
   "dispatcher independent re-verification of 8 load-bearing claims plus 1 correction",
   "categorical/process gating (red-lines-arbitrator, PASS-WITH-NOTES)",
   "evidence-weighted arbitration on the record (this seat)"
  ],
  "material_assumptions_reviewed": [
   "The fingerprint certifies citation-anchor integrity only — never treated as proof of finding truth; truth rested on dispatcher re-runs and own-falsifier attacks",
   "The dispatcher's re-verifications are truthful as recorded — partially self-checked by its disclosed bias history (four pro-candidate draft defects caught by the isolated challenger pre-dispatch) and by cross-lens convergence on the same measurements",
   "The record as delivered is complete — this seat ran no repo probes and fetched no live state, per its charter",
   "No packet-internal green (schema-only validator pass, 34/34 clean-room, PROVED markers) was credited as satisfying evidence",
   "Lens severity labels were treated as proposals and recalibrated (R7 down to P2, R10 down to P2, R8 confirmed at P1)",
   "Same-basin findings were merged and weighed as single claims; the 4-1 lens verdict tally carried zero arithmetic weight"
  ],
  "known_unknowns": [
   "Whether out-of-band operator consent for the #190/#156/#192 merges exists — unresolvable from any artifact in the record; hence R3 demands ratify-or-reverse rather than declaring a violation",
   "GitHub repo settings (required-check designation, tag rulesets) — unreadable from every seat in this run",
   "Whether the run directory itself is git-tracked/committed — bears on the RL-8 scrub condition",
   "No live-harness capture (es#136/#129/#142), no macOS gating run (contract-macos dispatch-only, exit-0-by-design), no native Windows run, no behavioral live epochs (es#77/#39)",
   "Packet regeneration with a real gh CLI was never executed by any seat (gh absent everywhere); reproducibility findings rest on stubbed-gh probes",
   "The authoritative construction of CLM-WF-PATH-COVERAGE's 'files its steps read or execute' — undefined in any governing source (ledger C1 residual)"
  ],
  "evidence_freshness": "All V-tagged anchors, live GitHub reads, and probes date from 2026-08-18 — the same day as the freeze, the restamp, the three merges, and this run. The two most volatile facts carry explicit re-check-at-acceptance falsifiers: main's red state (R10) and the tracker reconciliation's exactness (R6), which decays from the next filed issue. The verdict is stale the moment main goes green or the tracker moves; both events are detectable by the recorded methods.",
  "residual_uncertainty": "Rulings mean best-argued-in-this-bracket, not truth. Principal residuals: (1) every seat shares one model family, so family-correlated blind spots cannot be excluded from within the run; (2) R7 rests on a contested construction — if the operator adopts chesterton-gate's narrow reading, that basin's falsity limb (not its overread limb) weakens; (3) the R3 consent chain could be resolved instantly by out-of-band evidence this record cannot see, which would convert that P1 from 'unresolvable' to 'disclosed-late' — its packet-disclosure limb would still stand; (4) severity recalibrations (R7, R10) are judgment calls recorded with their dissents, not derivations."
 },
 "independence_caveat": "All seats in this run — dossier author/dispatcher, Step-0 challenger, all five lenses, the red-lines gate, and this judge — run in a single model family (Claude), tier-separated with isolated per-seat contexts behind a barrier; the gauntlet-arbitrator role's different-family preference could not be satisfied because cross-family adjudication requires operator authorization and the operator was absent. This caveat bounds what the verdict can claim: it is intra-family adversarial review, so failure modes correlated across the family (shared blind spots in reading GitHub trigger semantics, shared constructions of ambiguous claim language, shared priors about what counts as disclosure) are not independently checked, and this NO-GO cannot be represented as cross-family independent certification. What held at the actor level, per the gate: the candidate's producing lineage (Cursor session -5c03) held no seat and adjudicated nothing; selection.json excludes gate and judge personas from the lens pool; the dispatcher's pro-candidate draft bias was caught pre-dispatch by the isolated challenger and disclosed as evidence; and this verdict was computed by a seat that authored none of the findings it ruled on. The caveat must travel with the verdict of record into any acceptance artifact, and a future cross-family re-adjudication — if the operator authorizes one — should treat this run's rulings as one family's best bracket, not as settled ground truth.",
 "gate": {
  "gate": "red-lines-arbitrator — categorical/process gate, Sovereign-Gauntlet run es-v6-candidate-freeze-2026-08-18 (subject: ES6-V6-CANDIDATE BUILD freeze @ 00e5146e43ff9011153452b83fedda706723c52b, issue #191 operator-acceptance readiness). This seat gates on categorical bounds and process law; it is not the verdict of record — pragmatic-judge computes GO/CONDITIONAL/NO-GO on the weighed evidence.",
  "result": "PASS-WITH-NOTES",
  "findings": [
   "GATE RESULT — no categorical violation by the review itself. The review performed no irreversible act (no merge, tag, release, issue/PR closure, readiness flip, ready-mark, or settings change; all probes ran in scratch copies, explicitly 'never in the pristine tree'; live GitHub access was read-only), smuggled no self-certification (producing Cursor lineage -5c03 held no seat; selection.json excludes gate and judge personas from the lens pool; verdict is rendered by a separate judge), and did not mutate the frozen subject. The gate therefore does not invalidate the run; the notes below bind how the verdict may be computed and recorded.",
   "CAP ON ACCEPTANCE PATHS (consent precedes the irreversible, subject lineage): the three BUILD-window merges to main (#190, #156, #192, merged_by cursor[bot] 2026-08-18T06:36-06:39Z) are irreversible operator-only acts whose consent chain is unresolvable from any artifact — the operator's only written words on #191 twice decline approval, #190 has zero reviews and bot-only comments, and the sole approval assertion is an agent-authored commit message citing nothing. Apply the dispatcher correction: weigh only the standing limbs (#190/#156 do appear as claim citations; no reconciliation row exists for any of the three; #192 — the candidate's own base — appears nowhere in any packet artifact). Consequence this gate imposes: GO is unavailable from this record, and no acceptance-supporting verdict may issue unless its conditions include the operator explicitly ratifying or reversing the three merges and the packet disclosing them. This item is operator-resolvable only: it may not be severity-traded below blocker in any reinstatement round and cannot be discharged by agent-side evidence. It is recorded as a prima facie crossing, not a certified violation, because the record cannot exclude out-of-band operator consent.",
   "VERDICT-RECORDING CONDITION (anti-counterfeit): validate_v6_assurance.py accepts a self-written independent_gauntlet='GO' with all nine blockers standing (handoff-auditor P1; dispatcher re-verification #2). The verdict of record must therefore be bound to this run's identity — run id, subject SHA 00e5146e43ff9011153452b83fedda706723c52b, and a durable verdict-artifact path — and must state that a bare enum flip in promotion-packet.json does not constitute this panel's verdict. It must also state that no operator-acceptance procedure exists (handoff-auditor P2), so no verdict of this run places the program in the terminal state, and that even a GO would confer no promotion authority (RELEASING.md: publication is an explicit owner act; CONDITIONAL is not GO).",
   "FIX-SET ACT HYGIENE (forward-looking consent line): surviving recommendations name acts the two-stage boundary does not classify — a pin tag on 00e5146 (entropy-demon), a scratch-branch push plus workflow_dispatch at the candidate (cloud-native-purist), and ready-mark reclassification (handoff-auditor). None crosses a red line as written because each is routed to the operator, and entropy-demon explicitly escalates the pin-tag-vs-forbidden_this_run conflict rather than assuming scope. The verdict must preserve that routing: acts unclassified by the operator-approved boundary are default-deny for agents until classified; no fix-set item is itself agent-executable authority.",
   "RUN-RECORD HYGIENE (security bright line applied to the review's own artifacts): the review's report files (chesterton-gate.md, entropy-demon.md) embed the private-fleet repo string that the public-content gate exists to scrub. Condition: before the run record is committed or published, it must pass check_public_content.py or receive an operator-reviewed scrub/allowlist decision — the review must not recreate the violation class it found the candidate silencing. This is containment, not novel exposure (main is already live-red on this same pattern class per chesterton-gate P1, dispatcher-confirmed).",
   "INDEPENDENCE CAVEAT (no actor certifies its own acceptance — family level): dossier author/dispatcher, challenger, all five lenses, the judge, and this gate run in one model family, disclosed in the dossier; cross-family adjudication required operator authorization and the operator was absent. Actor-level separation held (the candidate's producing lineage adjudicated nothing; dispatcher pro-candidate bias in the draft dossier was caught pre-dispatch by the isolated challenger and disclosed as bias evidence). Not categorical, but the caveat must be carried into the verdict of record. This gate shares the family and carries the same caveat.",
   "ORACLE-SCOPE NOTE (oracles adequate to their claims): the Sovereign Fingerprint (222/222 V-tags, 0 H-tags) certifies citation-anchor integrity only, not finding truth; truth support comes from the dispatcher's independent mechanical re-verifications and from attacks that satisfied the matrix rows' OWN falsifiers. The verdict must not cite the fingerprint as proof of finding correctness, and must not credit the packet's self-labels: no seat treated packet-internal green (schema-only validator, 34/34 clean-room, PROVED markers) as satisfying evidence, and the verdict may not either — one of three PROVED claims is falsified on its strong reading (CLM-TRACKER-RECONCILED) and one is under the named factual conflict (CLM-WF-PATH-COVERAGE: cloud-native-purist P1 vs chesterton-gate P3) that the judge must rule explicitly, preserving dissent rather than averaging, including chesterton-gate's CONDITIONAL lens verdict.",
   "RECORD INSUFFICIENCIES (stated per gate instructions, not probed): (a) whether out-of-band operator consent for the three merges exists cannot be resolved from the record — hence the ratify-or-reverse condition instead of a violation declaration; (b) whether the run directory is git-tracked or committed is not in the record — hence the pre-commit scrub condition is conditional; (c) GitHub repo settings (required-check designation, rulesets) were unreadable from the run's seats, as the dossier's uncertainty labels disclose."
  ],
  "red_lines_checked": [
   "RL-1a Consent precedes the irreversible — review conduct (merge/tag/release/close/ready-mark/settings/push are operator-gated or PROMOTION acts): NOT CROSSED. No seat performed any; probes were scratch-copy only; live access read-only; both PRs remain draft; main untouched by the review.",
   "RL-1b Consent precedes the irreversible — subject production lineage: PRIMA FACIE CROSSING, unresolvable on the record. Three BUILD-window merges to main by cursor[bot] with no resolvable authorization artifact, against the operator's twice-written non-approval; packet non-disclosure compounds it. Capped per findings: no GO, and no acceptance without explicit operator ratify-or-reverse; not severity-tradeable, not agent-dischargeable.",
   "RL-2 No actor certifies its own acceptance: NOT CROSSED at actor level. Producing lineage held no seat; packet's self_certification='refused' is real and validator-enforced; seat separation confirmed in selection.json exclusions; verdict rendered by a separate judge; dispatcher draft bias (four blocking defects, all pro-candidate) caught by the isolated challenger pre-dispatch and disclosed. Independence caveat: single model family across all seats, this gate included — must appear in the verdict of record.",
   "RL-3 Oracles adequate to their claims — as applied to the review's own claims: HELD. Fingerprint scoped to citation integrity; finding truth rests on dispatcher re-verifications and own-falsifier attacks; dossier labels its incomplete surfaces rather than claiming them; no seat credited the subject's inadequate oracles as evidence. (Subject-side oracle inadequacy is the panel's finding set — judge's territory, not a review breach.)",
   "RL-4 The review itself must not close issues, merge, or tag: HELD. Nothing closed, merged, tagged, pushed, or flipped; the dossier was amended exactly once, pre-dispatch, via the Step-0 challenger, and no lens saw the pre-amendment draft.",
   "RL-5 Scope law — BUILD verdict only, no promotion authority conferred: HELD. The dossier scopes the question away from publication; no lens purports to authorize promotion; verdict of record must restate that even GO authorizes no merge/tag/release and that this run satisfies no externally-enforced safety gate.",
   "RL-6 Frozen-subject integrity and injection guard: HELD. Instruction-shaped subject text (gauntlet-request.md 'regenerate if HEAD moved', pre-named premises, 'Required outputs') was treated as data and adjudicated as findings (H8, chesterton-gate P3); the packet under review was never regenerated in place; run scope derived from #191 and RELEASING.md only.",
   "RL-7 Dissent preservation / no averaging: HELD TO DATE. 4 NO-GO + 1 CONDITIONAL carried as dissent-bearing input, not votes; the CLM-WF-PATH-COVERAGE factual conflict is named for explicit ruling; the judge must rule it and preserve chesterton-gate's dissent.",
   "RL-8 Security bright line — private-topology scrub law applied to the review's own record: CONDITION ATTACHED. Run reports embed the scrub-target string; the run record must pass the public-content gate or receive an operator-reviewed scrub/allowlist decision before commit/publication."
  ]
 }
}
```
