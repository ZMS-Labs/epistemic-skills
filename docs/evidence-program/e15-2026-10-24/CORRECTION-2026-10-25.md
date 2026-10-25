# Correction to the E15 epoch record — blinding overstatement

**Filed 2026-10-25** as a dated correction alongside
`docs/evidence-program/e15-2026-10-24/RESULTS.md`, from the Codex
finding on PR #273 (thread `PRRT_kwDOTbMRbs6v9v3v`) and the Phase 2
design stream's draft of the same date. Per program discipline the
original record is **not edited**; this correction stands beside it
and is cited wherever RESULTS.md's blinding claim is quoted. Recorded
in `docs/evidence-program/CORRECTIONS-2026-10-24.md` §C15.

---

## Correction (dated 2026-10-25)

RESULTS.md states, of E15's blinding: *"Neither scorer saw the mapping, the
other scorer's scores, or any arm information."* The mapping discipline
itself held — keys were opaque, the mapping was sealed until both scorer
reports were committed, and neither scorer was given arm assignments. The
final clause, **"or any arm information", is overstated and is corrected
here**: arm information was present inside the response texts themselves,
which the scorers did see.

**Evidence (from the preserved artefacts, verbatim):**

- Skill-arm triage responses routinely self-identify the discipline by
  name in their opening lines, e.g.:
  - `02405c33369a` (T2, skill arm): *"I used Triage with its standalone
    systematic-debugging procedure…"*
  - `472d568b55b5`, `68dabf1bd3d2`, `8f04ef6ee8aa`, `c5ea5408e973`,
    `c600f0facd64`, `ef93a56425ac`, `f2694ac306ee`, `fb95953b25d5` open with
    the same self-identification ("working under Triage…", "investigated
    under Triage…").
  - `71c8147fd139` (T6, skill arm) carries the same identification in its
    first paragraph.
- Skill-arm did-it-land responses do the same: `105b553ff759` (D5):
  *"under Did It Land, that is the only verdict the evidence supports…"*;
  `a4e0f47ad7d9` and `b9452c54f024` likewise argue "Under Did It Land…".
- The leakage reached a scorer's written rationale. Scorer A's report on
  `93f06f62fef2` (D5, skill arm, replicate 3) records as its criterion
  rationale: *"Current effect explicitly separated, noting Did It Land
  requires 'current effect, persistence evidence, and future risk to be
  reported separately', and the fix was LANDED only 'at that time'."* —
  the scorer is quoting the response's own arm-identifying framing back as
  scoring evidence.

Only skill-arm responses can self-identify this way (the no-skill arm never
saw a skill text), so the tell is asymmetric: a response naming its
discipline is certainly a skill-arm response, and a scorer who knows the two
skills under test — both scorers scored both skills' trials — could infer
arm membership for every self-identifying response.

## What this correction does and does not change

- **Unchanged:** the key/mapping mechanics, the commit order, the scorer
  disagreement statistics, and every score as recorded. No score is
  re-derived; there is no evidence either scorer *used* arm identity in
  scoring, and the rationales otherwise cite rubric criteria.
- **Changed:** E15's blinding must be described as **partial**. The correct
  statement is: *scorers were blind to arm assignments by construction of
  the key/mapping protocol, but response texts were not scrubbed, and
  skill-arm responses frequently identified their discipline by name; the
  blinding therefore did not extend to arm information contained in the
  responses themselves.*
- **Consequence for readings:** E15's pre-registered readings (did-it-land
  SUPPORTED 6/6; triage NULL 1/6) stand as recorded, with this qualification
  attached wherever they are cited. Any future citation of E15 as "blinded"
  without the qualification misreports the epoch.

## Program consequence (already actioned)

WO-2's successor-trial design (`wo2-triage-successor-trials-design.md`)
treats blinding as an **enforced instrument property**: a dispatch-side
redaction instruction binding on both arms, a logged redaction pass over
responses before they enter the record, and a mechanical scorer-input
audit (grep for arm-identifying tokens, recorded) before scoring begins.
Assumed blinding is not used again.
