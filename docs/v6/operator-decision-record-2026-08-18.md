# Operator decision record — v6 program interview, 2026-08-18

Provenance: live operator interview (open-questions skill, explicit
invocation: "ask me all open questions until none remain"), conducted in
the session that produced the independent Gauntlet run
`docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/` (verdict NO-GO
against `00e5146e43ff9011153452b83fedda706723c52b`). Docket mode with
cascade appends; 16 questions asked, 16 answered; zero parked, zero
struck; closing probe returned nothing further.

Status: **PENDING OPERATOR RATIFICATION ECHO.** Per D14, the operator
directed the agent to post this record under explicit authority and to
issue an exact SHA-bearing ratification string; the operator echoes that
string back and the agent certifies the echo verbatim. A certification
section is appended to this file (follow-up commit) once the echo is
received. Until certification, every decision below is recorded
operator-instructed-in-interview, agent-transcribed.

## Decisions

- **D1 (R3 discharge).** The three BUILD-window merges to main —
  PR #190 (required-job semantics), PR #156 (publication-authorization
  step), PR #192 (ES6-ZI-001 baseline; the NO-GO candidate's base) — are
  **ratified**: retroactively confirmed as operator-approved acts.
- **D2 (repair seat).** THIS seat (the gauntlet-adjudicating session's
  lineage) executes the BUILD repair ticket. Consequence accepted: the
  next independent Gauntlet must be a different, fresh seat.
- **D3 (#104).** The unimplemented v5 design commitments (ROUTING.md,
  intrinsic ledgers, sentinel corpora, structural membership — as defined
  by the v5 design spec) are to be **implemented, all of them**, in the
  v6 candidate, before successor GO.
- **D4 (act classifications).** Classified **BUILD-permitted**
  (agent-executable without further asking): (a) non-`v*` pin tags (the
  `pin/…` namespace governed by `check_pin_tags.py`); (b) scratch-branch
  push plus `workflow_dispatch` of the gating suites at candidate SHAs;
  (c) marking draft PRs ready-for-review. `v*` version tags remain
  PROMOTION.
- **D5 (boundary amendment, narrow).** Wiki **maintenance** edits are
  BUILD-permitted. The v6.0 release wiki packet and support-point
  declaration remain PROMOTION, exactly as issue #191 wrote them.
- **D6 (#186 tag-ruleset).** **Disarm-as-authorization** is confirmed as
  the regime for v6.0.0: `protect-version-tags` keeps zero bypass
  actors; the documented disarm → tag → re-arm-with-seeded-probe
  procedure (RELEASING.md step 7) IS the authorization act. The #186
  tag-ruleset item is decided.
- **D7 (run-record hygiene).** The gauntlet run's pinned evidence file
  `docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/evidence/dossier-challenge-2026-08-18.json`
  is dispositioned by **exact-file allowlist** in
  `check_public_content.py` with a rationale comment (review-trail file
  that must quote the scrub vocabulary). No scrub; the dossier pin and
  seat-binding hash chain stay intact.
- **D8 (Step 7b).** Cross-family adjudication is **skipped for the
  NO-GO** verdict. **Standing instruction:** run Step 7b (manual-handoff
  consult) at the next GO-posture verdict, before operator acceptance.
- **D9 (#40).** #40's cross-family requirement is **re-scoped** into the
  v6-and-future publication gauntlets' Step 7b (first exercised per D8).
  Closure of #40 itself remains the operator's act.
- **D10 (#84 item 3).** The recommended field-pair ownership split is
  **confirmed** (epistemic-calibration owns the outcome store and
  resolution loop; epistemic-skills owns emission — events per the
  pinned contract plus decision-ledger outcome reviews as the resolution
  feeder), **and the operator grants the outcome store operator-visible
  status** — the field-tier mint gate becomes reachable. Content-class
  scoping of the visibility grant is checked at implementation.
- **D11 (main repair).** A minimal **non-draft fix PR to main** is
  authorized now, carrying only the three exact-file allowlist entries
  (the two ES6-ZI-001 files plus D7's file). Merging it remains the
  operator's act.
- **D12 (re-cut home).** The repaired candidate is built on a **new
  `claude/*` branch**; a **new draft PR** becomes the freeze PR and
  **supersedes #194**; the agent is authorized to **close #194** after
  posting the supersession comment. **#193 stays open** as the isolated
  custody PR.
- **D13 (old packet).** No push to `cursor/v6-candidate-build-5c03`. The
  #194 supersession comment carries the NO-GO verdict pointer; the
  successor packet carries the full disposition. The dead branch keeps
  its historical `NOT_RUN` stamp.
- **D14 (consent protocol).** The agent posts this record and the #191
  decision comment **with the operator's explicit authority**, then
  issues the exact ratification string (naming this file's commit SHA
  and content sha256). The operator echoes the string; the agent
  verifies and **certifies the echo verbatim** in an appended section
  and a follow-up commit. The operator may additionally post the same
  string on #191 from their own account, which upgrades the record to
  fully operator-authored.
- **D15 (sequencing).** Execute now, in order: (a) this consent
  machinery; (b) the D11 main fix PR; (c) the re-cut BUILD (the 15
  gauntlet acceptance criteria plus D3's v5 commitments) carried as far
  as the session allows; (d) supersede-and-close #194 once the successor
  draft PR exists.

## Cross-references

- Gauntlet verdict of record:
  `docs/gauntlet-runs/es-v6-candidate-freeze-2026-08-18/arbitration.md`
  (NO-GO; ruling-set@1; seven open P1).
- Fix ticket: the 15 acceptance criteria in that ruling-set; owners as
  assigned there, with R3's criterion discharged by D1 upon
  certification of the ratification echo.
- Standing operator holds NOT decided here: none remaining — #104 (D3),
  #186 tag-ruleset (D6), #84 item 3 (D10), #40 (D9) are all
  dispositioned above. The operator holds ledger for v6 is, as of this
  record, empty pending execution.
