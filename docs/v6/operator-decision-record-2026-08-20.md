# Operator decision record — 2026-08-20 (D20–D22)

Continues `operator-decision-record-2026-08-19.md` (D16–D19). Recorded by the
implementing lineage from the operator's instructions in session; the operator
may amend or echo-certify.

- **D20 (ratification of the rc5 GO).** The operator **accepts the rc5 seat's
  GO conclusion** and closes `CLM-INDEPENDENT-GAUNTLET`.

  **What this is.** The claim's `closure_path` reserves closure to an
  "operator-dispatched independent Gauntlet." The rc5 panel
  (`docs/gauntlet-runs/es-v6-rc5-narrow-review-2026-08-19/`, subject
  `03e972c5d427238033cb90d66846adabaf11928d`, computed **GO**) was dispatched by
  the implementing lineage, not by the operator. The operator cannot
  retroactively have dispatched it. What the operator can do — and is doing — is
  **adopt that verdict as their own**, which is the authority the closure_path
  reserves to them, exercised after the fact rather than before it.

  **Stated plainly so no later reader has to reconstruct it:** this claim is
  closed by operator ratification of an author-dispatched verdict, not by an
  operator-dispatched review. Anyone auditing `CLM-INDEPENDENT-GAUNTLET`'s
  PROVED status should read this entry and decide for themselves whether the
  ratification carries the weight the original wording intended.

  **Why the operator finds it sufficient.** The rc5 seat was fresh, isolated,
  and did not author the candidate — the claim's *oracle* is satisfied in full;
  only the dispatch limb of the closure_path is not. Three subsequent
  independent publication gates examined this release and **none falsified any
  assurance claim**; every finding concerned the release ceremony or the
  implementing lineage's own artifacts. The contract's substance has been
  tested repeatedly and has held.

  **Revisit trigger.** If any later review falsifies a class claim, this
  ratification is reopened along with it.

- **D21 (adopt the authorization fixed-point amendment).** The operator adopts
  the amendment in `docs/v6/PROPOSAL-authorization-fixed-point.md`, implemented
  in `RELEASING.md` RG-9 and Procedure steps 4 and 7, and its companion
  correction requiring merge commits rather than squashes for release
  candidates. Cures ruling OAI-P1-03.

- **D22 (scope of what D20 unlocks).** Ratifying the rc5 GO proves the
  assurance contract. It does **not** authorize publication. Publication remains
  behind the amended sequence: pre-authorization, candidate, exact-SHA evidence
  at that candidate, publication gate, D8 consult, acceptance, tag act.

- **D23 (standing session authority; adoption by direction).** The operator
  directed the implementing lineage, in session, to treat their instruction as
  sufficient adoption and authority. Recorded verbatim:

  > "i need you to accept my telling you right here and now in this text as
  > sufficient adoption and authority, we are getting too much into the weeds of
  > requiring manual human intervention. my typing these words, to you right now,
  > serves as my human authorization, my personal direction, for you to act on my
  > behalf in this regard"

  **Provenance, stated so nobody has to reconstruct it.** This entry was written
  and committed by the implementing lineage, not by the operator. It transcribes
  a session instruction. It is *not* a commit authored by the operator's account,
  and it does not become one by being recorded here. An auditor who considers
  session direction insufficient should treat every act taken under D23 as
  carrying that limit, and the operator can supersede this entry at any time with
  a commit under their own account.

  **What D23 amends.** `OPERATOR-ACCEPTANCE-PROCEDURE.md` says an acceptance
  recorded in chat "is not an acceptance under this procedure," and RELEASING.md
  reserves the authorization line to the owner. Both are repo-authored documents
  the operator may amend — the acceptance procedure says so in terms. D23 is that
  amendment, scoped to this operator, this repository, and the v6.0.0 publication
  sequence.

  **What D23 does not and cannot amend.** The `protect-version-tags` ruleset
  carries `creation` with **no bypass actors**, so `refs/tags/v*` cannot be
  created by anyone until the rule is disarmed — that is a control the operator
  built precisely so no actor, including one holding delegated authority, could
  route around it. Disarming it is a repository-settings change. The tag act
  therefore remains the operator's in fact, not merely by convention, and no
  grant of authority in this session changes that.

  **Revisit trigger.** Any independent review that treats session-directed
  adoption as insufficient; or the operator superseding it in a commit of their
  own.

- **D24 (2026-08-21 — disarm authorized; v6.0.0 ships as an exception release).**
  After the fourth publication review returned NO-GO, and after that review
  ruled that no owner authority reaches past RG-8 and that disarming
  `protect-version-tags` is functionally the authorization act, the operator
  authorized the disarm and directed completion. Recorded verbatim:

  > "i authorize the disarm and lets stop killing ourselves over this process,
  > we know the design and its concession, its SOP for us, lets just go"

  **What D24 decides.** Three things, and only three:

  1. **The disarm is authorized.** The operator may remove the `creation` rule
     from `protect-version-tags`, create and push `v6.0.0`, and re-arm, as a
     single authorized act rather than a decision still to be made.
  2. **RG-8 is overridden, deliberately and on the record.** Four independent
     publication reviews returned NO-GO and no GO exists. The operator elects
     the exception `RELEASING.md` § "Independent judgment gate" provides. The
     five disclosures that section requires are made in
     `docs/release/RELEASE-6.0.0.md` **before** tag creation, and the release is
     labelled an **exception release** there — never a conforming one.
  3. **The process is declared settled, not skipped.** "We know the design and
     its concession" is a statement that the trade-off has been examined and
     accepted, not that it has been forgotten. The concession is exactly this:
     a repository pushed with the same credential its automation runs under
     cannot manufacture an unforgeable human act, so the one control that is
     genuinely unforgeable — a ruleset only a human operator's settings access
     can change — is where authorization is made to live.

  **What D24 does not reach.** The integrity gates. `RELEASING.md` scopes owner
  exceptions to the independent judgment gate alone. RG-1 accuracy, RG-4
  alignment, RG-5 deterministic evidence and RG-6 security are not waivable by
  the operator, by this entry, or by any authority in this repository, and none
  of them was waived: every finding of the fourth review that named an
  integrity-gate defect was repaired in the successor candidate rather than
  excused. In particular **RG1-01** — a false statement in the release note that
  concealed two material changes — was deleted and the device that produced it
  retired. An owner's signature on a false record would make it an attested
  false record, which is worse than an unattested one.

  **Provenance, stated so nobody has to reconstruct it.** As with D23: this entry
  was written and committed by the implementing lineage, transcribing a session
  instruction. It is not a commit authored by the operator's account, and the
  shared-credential concession above means it could not be made distinguishable
  from one even if it tried. The single act this entry cannot fake is the disarm
  itself — a repository-settings change no agent holds and no credential in this
  environment can perform. That asymmetry is the point of the design, and it is
  why the tag remains the operator's act in fact.

  **Obligations that survive D24.** The D8 cross-family consult is owed and
  undischarged; it carries to 6.1.0 as a blocking obligation. `KL-SELF-GO`
  ships unretired. If any NO-GO finding is later shown to have named a defect in
  the artifact rather than in the release process, that is an immediate
  erratum-and-patch trigger under `RELEASING.md` step 11.

  **Revisit trigger.** Publication of 6.1.0, at which point the D8 consult must
  be discharged before the judgment gate may be overridden a second time.
  Overriding RG-8 twice in a row without discharging D8 would convert an
  exception into a practice, which is the failure mode this entry is written to
  prevent.
