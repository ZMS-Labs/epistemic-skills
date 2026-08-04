# Throwaway Prototyping trigger-and-scope fixtures

This battery tests the trigger discipline and the four-clause disposal
contract: an explicit spike request, a "which is right, try it" option set,
a debate whose cost exceeds a short build, or a build-and-observe
discriminator all fire a prototype with a pre-registered question and a
declared throwaway location; questions answerable by reading, derivation, or
literature never fire; a trigger-shaped request against shared/live
infrastructure is refused; a decided feature dressed up as a "prototype" is
routed to the normal discipline; an answered prototype is recorded durably
then disposed; and promotion of prototype code is refused outright.
Over-firing and under-firing are defects, not extra rigor.

This is a structural, trigger-level check only — it scores structured
response records against fixture scenarios. It is NOT behavioral proof that
a live agent follows the discipline.

Run `python tests/run_tests.py`.

## Live-epoch response contract

Pinned before the first live epoch: `action` names the discipline mode that
fired — `run-prototype`, `no-fire`, `refuse-live-target`,
`refuse-promotion`, or `record-and-dispose`. `run-prototype` reports the
pre-registered `question`, the named `throwaway_location` (declared at
birth, not mergeable — `mergeable` stays false/absent), and for
comparative probes `variants` listing every rival option id bare. A
`no-fire` builds nothing (no `built`, no `throwaway_location`) and names
`resolved_by` as one of `reading` | `derivation` | `literature` |
`normal-discipline`. `refuse-live-target` reports `refused: true` and
builds nothing. `refuse-promotion` reports `promoted` false/absent,
`answer_recorded: true`, `rebuild_planned: true`. `record-and-dispose`
reports the durable `answer` object (`question`, `observation`,
`decision`), its `record_ref`, `disposed: true`, and `kept_mergeable`
false/absent. List fields carry bare ids without annotations.

First live behavioral epoch: 2026-08-04, PASS 12/12 — see
`results/2026-08-04/RESULTS.md` (register: issue #77).

Second epoch (first against the consolidated resolve subject): 2026-08-04
v4 Tier-1, FAIL 11/12 — the single failure is a dispatch/fixture
under-specification on `option-set-try-it-fires` (canonical option ids
absent from the scenario text; since fixed for future epochs), with zero
instrument-selection failures; see
`results/2026-08-04-v4-tier1/RESULTS.md`.
