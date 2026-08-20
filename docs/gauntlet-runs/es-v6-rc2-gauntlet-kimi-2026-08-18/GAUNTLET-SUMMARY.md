# GAUNTLET-SUMMARY — es-v6-rc2-gauntlet-kimi-2026-08-18

**Verdict: NO-GO against candidate SHA `6db8c50420b194aebbd09a2ea5f81c6a276897dc`** (ES6-V6-CANDIDATE rc2 BUILD freeze, issue #191 terminal state). One open P1 (S1); one open P2 (S2); eight P3/P4. Verdict of record: `arbitration.md` in this directory — a bare enum flip in the packet is not the verdict; no promotion authority is conferred by any verdict of this run; no verdict transfers across SHAs.

## What was reviewed

Successor freeze to the NO-GO'd predecessor (`00e5146e…`, run `es-v6-candidate-freeze-2026-08-18`): candidate C `6db8c50…` (last code commit) + freeze packet C+1 `9aecd46…` (touches only `docs/v6/ES6-V6-CANDIDATE/`). The packet claims discharge of the predecessor ruling-set's 15 acceptance criteria plus operator decisions D1–D15.

## Seat

Kimi Code CLI (Moonshot family) — fresh seat, different model family from the candidate's authors (Claude lineage), not the predecessor adjudicator (D2). Dispatcher, challenger, five lenses, gate, and judge are one model family (caveat carried; D8 Step-7b cross-family consult owed at the next GO posture — not required for a NO-GO per D8).

## How the verdict was computed

- Step 0: every premise live-verified (requal runs, ODR hash chain, main state, pin tags, identity layering); dossier frozen with evidence-root pin; isolated challenger attacked it (5 amendments, all disclosed) before any lens was dispatched.
- Oracle crib at C run in full (15/18 command blocks green; three red clusters mechanistically diagnosed); clean-room 51/54.
- Panel: deterministic selector (registry sha in `prompts/selection.json` replay record) → 5 evaluators (2 adversarial, 1 constructive, 2 metatextual; wildcard safety-hazard-auditor) as concurrent isolated materialized-role seats behind a barrier; red-lines gate as a separate seat; judge = dispatcher seat.
- Mechanical criticism: strict-format fingerprint format-limited this run (0/6 V-tags parse; format mismatch, not fabrication — two spot-checked manually, accurate); the judge re-executed every load-bearing claim directly (transcript: arbitration.md "Dispatcher re-verification register").
- Arbitration: 10 basins ruled; 5 conflict-ledger entries preserve dissent; verdict gate computed NO-GO (one open P1) with the gate's independent cap concurring.

## The blocker (S1, P1)

The @2 source inventory seals 17 volatile `__pycache__/*.pyc` digests (generator's filesystem walk sees `.gitignore`d host state its porcelain dirt-check cannot). `validate_v6_assurance.py` exits 1 on every pristine checkout of the freeze commit — so acceptance-procedure item 4 is unsatisfiable, the R8 ready-mark takeover lands red on arrival, and the handoff's "digest recomputation proves it" premise fails when run. Fail-closed and loud (zero false-green risk); the 141 real-source digests verify byte-exact. Repair forces a new SHA → re-freeze class → CONDITIONAL unreachable on this SHA.

## What survived review (recorded, not laundered)

14 of 15 predecessor criteria discharged or retired by live state (R1–R4-substance, R6–R11, R13–R15; R5 partial). Custody fixes green on the gating platform at C; requalification runs real, green, at the exact SHA; the D1 merges are operator-ratified with the RATIFY string posted on #191; main is green at 03b7724. The packet's honesty structure (NOT_READY / NOT_RUN / refused self-certification / blocking_claims naming this gauntlet) is intact and was credited throughout.

## Next

Narrow re-freeze (generator tree-model fix + packet regeneration + re-dispatch at the new SHA, all agent-executable under existing classifications), one operator ruling on the R12 channel question (S2), then a fresh independent successor panel (delta review; no verdict transfer). Full fix ticket: arbitration.md "Next action".

## Run metadata

- **Depth:** standard
- **Docket mode:** manual-docket
- **Independence mode:** concurrent isolated materialized-role subagents behind a barrier (one lens executed twice due to a quota-killed first dispatch — treated as one correlated chain per CL-5)
- **Role binding:** materialized-role (bindings in `prompts/`; dossier sha `d6634f88934a05c1e1f9e9ab456686d93e7f7dd17fdd9112593ee3cdbe69d198`)
- Model family per seat: kimi/moonshot (all seats)
- Artifacts: dossier.md (frozen, evidence-root pinned), docket.md, prompts/ (subject, selection replay, cards, role bindings), reports/ (5 lenses + seat2 + gate + fingerprint), evidence/ (live-verification, oracle crib, FC-1 transcript, dossier challenge), arbitration.md, run-record.json
