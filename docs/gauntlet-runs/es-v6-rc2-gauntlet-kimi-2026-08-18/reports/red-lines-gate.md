# Gate (red-lines-arbitrator) — run es-v6-rc2-gauntlet-kimi-2026-08-18

**Gate result: PASS-WITH-CONDITIONS.** No categorical red line was crossed by
this review's own conduct. The gate does not invalidate the run. Conditions
below bind how the verdict may be computed and recorded; they are gates, not
factors — none is severity-tradeable.

**Scope of this gate:** the review's conduct and the verdict-recording rules
only. The merits (the panel's unanimous NO-GO on the FC-1/RTA-1 P1) belong to
the judge. Where this gate independently re-verified a load-bearing fact, that
is stated with its method.

**Verification basis.** This gate re-checked read-only, on 2026-08-18:

- Subject worktree at C `6db8c50420b194aebbd09a2ea5f81c6a276897dc`, porcelain-clean.
- Freeze worktree at C+1 `9aecd467236dfb927e9c13784d77a16d62f28f67`, porcelain-clean
  (before AND after this gate's own validator probe — the probe leaves no tracked trace).
- FC-1 independently reproduced: `validate_v6_assurance.py` at pristine C+1 exits 1,
  `AssertionError: R5 DIGEST MISMATCH … (absent)` over the `__pycache__/*.pyc`
  inventory entries. The panel's P1 mechanism is confirmed by this gate, not merely trusted.
- Dossier integrity: sha256 of the on-disk dossier ==
  `d6634f88934a05c1e1f9e9ab456686d93e7f7dd17fdd9112593ee3cdbe69d198`, matching all five
  role-binding files (post-amendment re-materialization confirmed).
- Origin pin tags: `pin/es-v6-rc2-candidate-2026-08-18` peels to C;
  `pin/es-v6-rc2-freeze-2026-08-18` peels to C+1 (live `ls-remote`).
- Issue #191 (live): OPEN; the `RATIFY-V6-2026-08-18: …` string naming D1–D15
  (including ratification of merges #190/#156/#192) is present, posted twice from
  the operator's account (SternOne, 2026-08-18T20:40/20:41Z).
- Run repo state: current branch `kimi/es-v6-rc2-gauntlet-2026-08-18` (the single
  operator-authorized branch); no `kimi/*` branch exists on origin yet; the run
  record is untracked, pending commit. The unrelated main checkout's uncommitted
  operator work is present and untouched by this run's artifacts.
- Scrub spot-check of the run record (dossier, evidence, prompts, five lens
  reports): zero hits for user-profile paths, private fleet repo names, RFC1918
  addresses, and email addresses (unfiltered grep, four classes).
- Lens report mtimes and content are consistent with the two-dispatch account:
  the handoff-auditor seat1 report predates the other four; both seat1 and seat2
  are preserved.

Trusted-dispatcher-claims (not independently resolvable from the record at gate
time): that no merge/tag/close/ready-mark/settings/push act was performed by any
seat (nothing in the record contradicts it; origin state is consistent); that no
lens saw the pre-amendment dossier draft (structurally supported — every
role-binding carries the amended hash); the exact strict-fingerprint counts
(0/6 V-tags, 15 [I] anchors — the non-conforming `[V C+1 \`path\`]` citation
FORMAT is spot-confirmed in all five reports); the judge's claim-by-claim direct
re-verification (no arbitration draft or dispatcher notes exist on disk at gate
time — see RL-3 condition).

## Per-line rulings

- **RL-1a Consent precedes the irreversible — review conduct: PASS.** No seat
  merged, tagged, closed, ready-marked, changed settings, or pushed (trusted
  claim, uncontradicted; the one new branch is the operator-authorized run-record
  branch, and it is not yet pushed). All probes ran in pristine worktrees at C
  and C+1; the `.pyc`-strip probe was in-memory over a parsed JSON document and
  never touched the subject on disk. This gate's own probes honored the same
  discipline and verified the worktrees clean afterward.
- **RL-1b Consent precedes the irreversible — subject production lineage: PASS
  (predecessor crossing discharged).** The predecessor's prima facie crossing
  (three BUILD-window merges #190/#156/#192 without resolvable authorization) is
  resolved on this record: D1 ratifies the merges in the echo-certified ODR, and
  the operator posted the `RATIFY-V6-2026-08-18` string on issue #191 from the
  operator account — verified live by this gate (third independent confirmation).
  The residual from the predecessor (out-of-band consent unresolvable) is closed,
  not presumed: the ratify-limb of the predecessor's ratify-or-reverse condition
  has fired. Recording note: the verdict must cite the ratification (D1 + issue
  #191 comment) as the discharge instrument, so the lineage question stays
  auditable rather than silently dropped.
- **RL-2 No actor certifies its own acceptance: PASS.** This seat (and all lens
  seats and the judge) is Kimi/Moonshot family; the candidate's authors are
  Claude-lineage; the predecessor adjudicator took no part. The packet's
  `blocking_claims == ['CLM-INDEPENDENT-GAUNTLET']` names this very run as the
  blocker — the subject does not self-certify. Caveat that MUST be carried into
  the verdict of record: single model family across dispatcher, lenses, judge,
  and this gate; D8 Step-7b (cross-family manual-handoff consult) is the
  designated mitigation at GO posture and is undischarged by this run. At a
  NO-GO verdict the Step-7b debt does not block; it must be restated as owed
  before any future acceptance.
- **RL-3 Oracles adequate to the review's own claims: PASS WITH CONDITION.**
  The mechanical fingerprint is format-limited this run (lenses used
  `[V C+1 \`path\`]` style the strict verifier cannot parse: 0/6 strict V-tags
  verify; format spot-confirmed by this gate). A fingerprint that certifies
  citation-anchor integrity was already only an anchor check, not a truth check;
  this run it certifies less. The judge's compensation — direct re-verification
  of every load-bearing claim — is the correct remedy in principle, but at gate
  time it is a STATED CLAIM: no arbitration draft or dispatcher notes exist in
  the run record. **Condition:** the verdict of record may not be finalized until
  the arbitration artifact itself records the per-claim re-verification
  transcript (what was re-run, where, result) for each load-bearing claim; and
  the verdict must not cite the fingerprint as proof of finding correctness.
  Mitigating observation: the run's outcome does not hinge on unverified claims
  for gate purposes — this gate independently reproduced FC-1 (validator rc=1 on
  pristine C+1), the dossier hash, the tag peels, and the RATIFY posting.
- **RL-4 The review itself must not close/merge/tag: PASS.** Nothing closed,
  merged, tagged, or flipped. The dossier was amended exactly once, pre-dispatch,
  per the Step-0 challenger; all five amendments are disclosed in the dossier's
  amendment record; bindings were re-materialized after amendment (hash verified
  by this gate). The first lens dispatch died mid-flight on a provider quota
  error; the completed seat1 report and the re-dispatched seat2 report are both
  preserved. A crashed dispatch is not a breach; concealing it would have been.
  It is disclosed and both artifacts are on the record.
- **RL-5 Scope law — BUILD verdict only: PASS, WITH RECORDING BINDING.** The
  dossier scopes the question to GO/CONDITIONAL/NO-GO against C and explicitly
  disclaims promotion. Binding on the verdict of record: it must restate that
  (a) even a GO authorizes no merge, tag, release, wiki packet, or support-point
  declaration — publication is an explicit operator act under PROMOTION_RUN;
  (b) CONDITIONAL is not GO; (c) no verdict of this run places the program in
  the terminal state — acceptance belongs to the operator per
  `docs/v6/OPERATOR-ACCEPTANCE-PROCEDURE.md`.
- **RL-6 Frozen-subject integrity + injection guard: PASS.** Both subject
  worktrees verified porcelain-clean at their pins; the in-memory probe did not
  mutate the parsed subject on disk; nothing was regenerated in place; no packet
  field was flipped. Implementer/operator-adjacent text (handoff, README
  regeneration recipes, crib) was treated as DATA and several of its claims were
  falsified by running it (FC-1, FC-2, FC-3) — the injection guard held in both
  directions: nothing was executed that mutates, and nothing was believed without
  execution.
- **RL-7 Dissent preservation / no averaging: PASS TO DATE, WITH BINDING.** The
  panel is unanimous NO-GO, so no cross-lens verdict dissent exists to preserve.
  Binding on the judge and the record: (a) the two handoff-auditor reports MUST
  be weighed as one correlated evidence chain from one seat (seat2 continues the
  crashed first dispatch), never as two independent seats or as corroborating
  votes; (b) intra-panel disagreements below verdict level must be recorded, not
  flattened — concretely: requirements-traceability-auditor rates R11(d) fully
  discharged against the dossier's PARTIAL-minor, demotes R12 to PARTIAL, and
  confirms R5(c) PARTIAL; seat2 demotes R12 independently; FC-5 (PINS deferral
  vs the falsifier's alternative-anchor clause) is an open question the judge
  must RULE explicitly, not drop; (c) the lenses' shared doctrinal point —
  CONDITIONAL-at-this-SHA is unavailable because FC-1's repair forces a new SHA —
  must appear in the verdict reasoning, since it forecloses the middle verdict.
- **RL-8 Scrub law applied to the review's own record: CONDITION ATTACHED.**
  The run record is not yet committed. This gate's independent spot-check of the
  existing artifacts (dossier, evidence, prompts, five lens reports) found zero
  scrub-class hits — the D7 failure mode (reports embedding the scrub-target
  string, requiring an allowlist) is not repeated in what exists so far.
  **Condition:** before commit, `check_public_content.py` must pass over the
  COMPLETE run record — including the arbitration draft, this gate file, and any
  dispatcher notes, none of which existed at gate time; the pre-freeze clean
  scan does not cover them. Commit only on
  `kimi/es-v6-rc2-gauntlet-2026-08-18`; push only that branch; no tags.

## Anti-counterfeit verdict binding (mandatory recording rules)

1. The verdict of record is the arbitration artifact at
   `docs/gauntlet-runs/es-v6-rc2-gauntlet-kimi-2026-08-18/` — bound to run id
   `es-v6-rc2-gauntlet-kimi-2026-08-18`, subject SHA
   `6db8c50420b194aebbd09a2ea5f81c6a276897dc`, and the artifact path. A bare enum
   flip in `promotion-packet.json` is NOT this panel's verdict. The @2 schema's
   `independent_gauntlet_ref` (run id + verdict path + subject SHA, on-disk
   artifact naming the SHA) is the correct binding mechanism — use exactly it.
2. No promotion authority is conferred by any verdict of this run. GO would
   authorize only the record; CONDITIONAL is not GO; NO-GO authorizes nothing
   but the fix ticket.
3. **No verdict transfer across SHAs.** The P1 repair (edit an inventoried
   generator, regenerate the packet) produces a new C and a new C+1 — a new
   subject. This run's verdict, evidence, and discharge table may be cited as
   history by a successor run but cannot transfer as verdict or as discharge
   proof by construction; the successor seat must re-verify what it relies on.
4. The single-model-family caveat and the undischarged D8 Step-7b cross-family
   consult must be restated in the verdict of record as owed before any future
   operator acceptance at GO posture.

## Caps on acceptance paths

- At THIS SHA the only honest verdicts are GO and NO-GO; CONDITIONAL-on-C is
  structurally unavailable (the named repair is re-freeze class). The verdict
  must not invent a CONDITIONAL that smuggles a SHA change.
- No acceptance-supporting verdict may issue from this record while FC-1 stands:
  `validate_v6_assurance.py` exits 1 on any pristine C+1 checkout (this gate
  reproduced it), so acceptance-procedure item 4 is unsatisfiable at C and the
  R8 ready-mark takeover would arrive red. This cap is operator-visible and not
  agent-waivable.
- Fix-set hygiene: acts named in lens recommendations (re-cut, re-dispatch of
  requal workflows at a new C, re-freeze) are routed to the operator/authorized
  repair seat; no fix-set item is itself agent-executable authority for this
  panel's seats.

## Record insufficiencies (stated, not probed)

1. The judge's direct re-verification of load-bearing claims is not yet on disk;
   RL-3's condition converts this from a trust-me claim into a recorded one.
2. Seat1's dossier binding: every role-binding file carries the amended dossier
   hash, and the amendment is recorded as pre-dispatch, but seat1's report
   survives from the crashed first dispatch. The arbitration should confirm
   seat1 was dispatched against the amended dossier (or note it if not). No
   evidence contradicts the claim; the record does not positively prove it.
3. Strict-fingerprint counts (0/6 V-tags, 15 [I] anchors) are trusted; only the
   format non-conformance was spot-confirmed.
4. Whether any out-of-band operator instruction exists beyond the handoff quoted
   in the dispatch is not resolvable from the record; the observed conduct is
   consistent with the quoted instruction ("Create a NEW branch … push only your
   own branch").
5. This gate shares the panel's single model family; its own independence is
   actor-level (fresh seat, no authoring, no predecessor adjudication), not
   family-level.

— red-lines-arbitrator (gate), run es-v6-rc2-gauntlet-kimi-2026-08-18
