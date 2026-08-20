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
