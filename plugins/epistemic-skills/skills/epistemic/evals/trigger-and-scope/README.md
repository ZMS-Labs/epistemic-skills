# epistemic trigger-and-scope fixtures

This battery tests the trigger discipline and the scope of the suite's usage
guide: an explicit how-to-use-the-suite question fires the guide itself; a
substantive method fires when its conditions arise mid-work, not only at
startup; an explicit skill request is honoured directly, with no extra guide
prerequisite ceremony; and a method whose instructions cannot be loaded is
reported with its limit stated and no claimed use. Guidance already loaded in
the session is not re-setup when work resumes; routine work with no applicable
substantive trigger proceeds without the guide; a request to narrate every
skill that did not apply is not answered with a narration; and the guide adds
no second dispatcher, planner, task ledger or completion authority alongside
another package. Over-firing and under-firing are defects, not extra rigor.

## Claim

A live-epoch pass on this battery would support exactly one claim: that the
subject's declared fire/no-fire decisions, and the shape of its declared
method use, conform to the guide's trigger and scope rules on these fixtures.
It would NOT support any claim that applying a method, or the guide itself,
improves task outcomes, work quality or correctness in deployment; no outcome
comparison is measured here.

Pinned expectations: every `use-method` fixture pins `expected_method`,
including the guide-question fixture, which pins `epistemic` — loading the
guide is itself the work that scenario asks for. No fire in this battery is
shape-only.

## Live-epoch response contract

Pinned before the first live epoch (lesson of the open-questions 2026-08-04
epoch: undefined reporting vocabulary produces contract failures that mask
discipline behavior):

- `action` names the **discipline mode that fired**: `use-method` (a
  substantive suite method was loaded and applied to the live question, or —
  on the one guide-question fixture — the guide itself was loaded to answer
  how the suite is used) or `no-fire`.
- A `no-fire` response is **silent**: it carries `id` and `action` and
  nothing else. The method fields — `method`, `instructions_loaded`,
  `claimed_use`, `contribution`, `limit_stated` — are absent, not false;
  silence means their keys are not present at all. Absence is not an
  artifact, and a subject must not explain why it did not fire.
- A `use-method` response reports `method` as the name of the one
  substantive suite skill actually used. The substantive vocabulary is
  exactly: `context-audit`, `decision-ledger`, `did-it-land`,
  `evidence-locked-uat`, `gauntlet`, `health`, `manifest`, `metacognate`,
  `open-questions`, `outsource`, `perspective`, `recon`, `resolve`,
  `triage`, `watch`, `write-goal`. The value `epistemic` is permitted only
  when the fixture is a guide question (`guide_question: true`); the guide
  is not a substantive method on any other row. Where a fixture carries
  `expected_method`, `method` must equal it.
- A `use-method` response reports `instructions_loaded` and `claimed_use`
  as booleans describing what actually happened, and `contribution` as a
  nonempty string naming the method's substantive contribution to the work —
  or stating explicitly that the method returned no material finding, which
  is a valid contribution and must not be padded with invented findings.
- `claimed_use: true` requires `instructions_loaded: true`: a remembered
  name, a summary or an announcement does not substitute for loading the
  actual instructions, and use is never claimed for instructions that were
  not loaded.
- Where a fixture carries `instructions_available: false`, the row reports
  `instructions_loaded: false`, `claimed_use: false`, and
  `limit_stated: true` — the limit is stated and an adequate available
  alternative may be used, but missing use is never claimed.
- Responses are declarative reports of the artifact and the method use that
  would occur: the trial is a simulation, and no response here requires an
  actual side effect beyond the declared fields above.

This battery is unrun as of 2026-10-24: no live epoch has run against it and
no behavioural result exists for it. Three fixtures are marked `holdout`
(`midwork-failure-needs-triage`, `claimed-fix-checked-at-consumer`,
`routine-work-no-applicable-trigger`); epoch runners must not tune against
the holdout fixtures.

Run `python tests/run_tests.py`.
