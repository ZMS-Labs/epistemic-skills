---
name: harvest-before-adopt
description: 'Use when an external project overlaps something you already built or plan to build, and the question is "should we adopt it, replace ours with it, or ignore it" — a competitor or upstream that does your job, a library that duplicates an in-house component, a framework someone proposes swapping in. Fires on "should we use X instead", "does X make ours obsolete", "evaluate X". Do NOT fire for choosing between candidates none of which you already have an incumbent for (that is an ordinary selection, not an adopt-or-keep question), for a dependency upgrade within a tool you already use, or as a way to justify a migration already decided.'
---

# harvest-before-adopt — take the ideas first; the software is the expensive part

An external project appears that does what your thing does. The reflex is to ask
**"should we adopt it?"** — a question that is expensive to answer, often
unanswerable without running the software, and whose two outcomes are a one-way
door and a shrug.

That is the wrong first question. **The extractable unit is not the system, and
it is not a capability. It is whatever the smallest transferable thing is** — a
distinction, a design principle, a tuned constant, an interface shape. Those are
free, instant, fully reversible, and require no install, no execution, and no
trust. Take them first. Only then ask whether anything is left that requires
adoption.

The failure this skill prevents is **spending the expensive question's budget to
get the cheap question's answer** — and its twin, adopting badly to avoid
"wasting" an evaluation already paid for.

Provenance: derived 2026-08-03/04 from a live two-candidate evaluation, hardened
by an adversarial panel that returned NO-GO on the first form (12 P1 findings).
Three things were built, in reverse order of discovery: the **capability
partition** (`reference/capability-partition.md`) came first and is the most
rigorous; **triage** and the **harvest ladder** came from noticing the partition
answered a question nobody had asked. The ladder is the load-bearing addition —
but the partition is not a lesser artifact, only a later step.

## Order of operations (this order is the skill)

```
1. TRIAGE   → PROBE / PARK / DROP, per ladder level
2. HARVEST  → take levels 1-4; re-run triage afterwards
3. (only if the harvest could not supply the answer)
   DISQUALIFIERS → ENUMERATE → DISCRIMINATE → COEXISTENCE → partition
```

Most candidates should stop after step 2.

## 1 — Triage: is finding out worth the attention?

Five inputs. They are **not equally knowable**, and the frame must not pretend
otherwise:

1. **Cost to find out** — usually the *only* reliably knowable number, and
   usually small. **It should dominate.**
2. **The prize** — what you would gain, and what lacking it costs you today.
3. **The floor** — what you lose if it fails. Normally just the probe cost.
4. **Decay rate** — how long an answer stays true. Provenance and bus factor as
   a *half-life*, not a quality score. A verdict about a young single-maintainer
   project expires in months: probe cheaply now, re-probe, and build nothing
   durable on it.
5. **Alternative use of the same attention** — the input that decides most real
   questions and that formal methods routinely omit.

Estimates are **ranges with stated assumptions**, never numbers pretending to be
measurements. The discipline is not precision; it is that each estimate is cheap
to revise when evidence returns.

**Two rules carry most of the weight:**

- **Cheap-and-reversible short-circuits the analysis.** If the probe is cheap and
  fully reversible, **run it instead of analysing whether to run it.** Building a
  decision procedure to decide whether to spend an hour costs more than the hour.
- **A `DROP` is reachable on structure alone, with no evidence.** If the prize is
  realizable only by abandoning the thing you are building, that is a category
  answer, not a close call. State it in a paragraph and stop.

**The spend decision is per ladder level, not per candidate.** A project can be
`DROP` at levels 5-8 and simultaneously your richest harvest source at 1-4 —
that is the *normal* case for a mature competitor. Never let a `DROP` at the top
of the ladder suppress the read at the bottom.

## 2 — Harvest: the extraction ladder

Cost and risk rise monotonically; **reversibility falls.**

| L | Unit | Cost | Reversible |
|---|---|---|---|
| 0 | **Nothing transferable found** — a real and informative outcome | read only | n/a |
| 1 | **Vocabulary / taxonomy** — a distinction you had no name for | ~0 | fully |
| 2 | **Concept / design principle** — an architectural move | ~0 | fully |
| 3 | **Calibrated constant / bound / default** — someone else's tuning work | ~0 | fully |
| 4 | **Interface or contract shape** | low | fully |
| 5 | **Code fragment** (licence permitting; attribution) | low | mostly |
| 6 | **Vendored module / subsystem** | medium | costly |
| 7 | **Dependency** | medium | costly |
| 8 | **Adopt the running system** | high | **one-way door** |

**Levels 1-4 are learning, not adoption.** The candidate never runs, is never
installed, and is never trusted.

**Harvest negatives too.** An anti-pattern to avoid, or a hazard you can now
name, is transferable value at level 1-2. For a mature competitor this is
usually the **richest seam**: their gaps are empirical evidence for the rules you
hold on principle, observed in the wild rather than argued.

### Why the harvest is a usable proxy for the expensive question

- **A read yielding nothing at levels 1-4 is evidence the higher levels would not
  pay either.** A system with no transferable ideas is unlikely to be worth
  adopting.
- **A read yielding plenty has already captured the value** — which converts an
  adopt-or-don't gamble into a guaranteed-positive read, and defuses the pressure
  that makes people adopt badly.

### Where the proxy fails — disclose this every time

- **It cannot tell you whether the software works.** Quality, reliability,
  performance, and operational cost are invisible to reading. The harvest makes a
  trial *optional*, never *unnecessary*, on those questions.
- **It is biased toward well-documented code.** A brilliant but terse project
  harvests poorly and will be undervalued.
- **Confirmation risk:** a motivated reader finds ideas everywhere. **Floor:**
  every harvest names what it examined and could *not* use. A harvest with no
  level-0 entries anywhere is suspect.

### Output — the harvest record

Per item: level · the thing · where it came from **at a pinned revision** ·
what it would change on your side · taken / deferred / rejected. Plus the
explicit **not-harvestable list**. This is what makes a read auditable instead of
an impression.

**Then re-run triage.** A rich harvest usually *lowers* the marginal value of a
trial, because most realizable value is already taken. The spend decision
changes, and often flips `PROBE` → `PARK`.

## 3 — The expensive path: the capability partition

**Full procedure: `reference/capability-partition.md`.** Read it when you get
here; do not work from this summary.

Reached only when triage says the answer matters *and* the harvest could not
supply it — something genuinely requires adopting running software. It is the
most rigorous part of this skill and it is placed last deliberately: **reaching
for it first is the failure mode.**

Its shape, so you can recognise when you need it:

- **Disqualifiers first**, and they are not capability rows. A confirmed
  disqualifier forces every adopt disposition to `UNDECIDED`; it can never
  *select* one. Generalising an adoption gate is exactly where this veto gets
  silently dropped — check for it by name.
- **Enumerate and preregister before citing evidence**, and preregistration needs
  *independence*, not a date: draft → operator interview → independent review.
  Where that was impossible, write `guard degraded` on the face of the verdict
  rather than claiming protection you do not have.
- **Disposition per capability** — `ADOPT-EXTERNAL` / `KEEP-BESPOKE` /
  `BUILD-NEW` / `UNDECIDED` — asking only *does the evidence separate the options
  for this capability?*, never "which is better overall."
- **Structural expressibility is the discriminator.** A `KEEP` is structural only
  if the change that would refute it lies **outside the candidate's own
  repository**. Expect this floor to demote rows against your own inclination.
- **Coexistence runs first, and is three-valued.** Displacement, contract,
  lifecycle, failure semantics — over everything *not* adopted, not just what you
  keep. `NOT-OBSERVED` forces every adopt row to `UNDECIDED`. **Silence never
  falls through to proceed.**
- **No whole-candidate verdict and no threshold.** A capability you cannot take is
  a factor to weigh, not a determinative one. Informed consent — the full
  partition visible in the same approval decision — replaces the number you do not
  have a loss function to pick.

**The rows are not the finding.** If most `UNDECIDED` rows share one cause, that
cause is the finding, and it is usually far more actionable than the rows. Then
re-run triage: a partition frequently changes the spend picture it was
commissioned under.

## Anti-patterns

| Smell | What is actually happening |
|---|---|
| "We need to trial it to say anything" | The harvest was skipped. Levels 1-4 need no trial. |
| A long analysis of whether to spend an hour | Cheap-and-reversible was not checked. Run it. |
| `DROP`, therefore stop reading | The spend decision is per level. The read is still free. |
| Every row `UNDECIDED`, no action | Correct output, but check *why*: if it is one shared cause, that cause is the finding, not the rows. |
| "Ours is better" | Maturity dressed as structure. Name the refuting change and where it would have to live. |
| Harvest with no rejected items | Confirmation risk. What did you examine and not use? |
| A verdict with no pinned revisions | Not evidence — an impression with a date on it. |

## Resources

- **`reference/capability-partition.md`** — the full expensive path: disqualifiers,
  enumeration and preregistration, the discrimination test and its floors, the
  four-predicate coexistence check, and why the obvious scoring-rule shape is
  unsound. Read it before doing step 3, not from memory.

## Honest status

This skill ships with **graded doctrine and a worked two-candidate provenance,
and no behavioural-battery evidence of its own.** The first form of the method
was adversarially panelled and returned **NO-GO with 12 P1 findings**; those
conditions are applied here. The revised form has produced one capability
partition and two harvests in real use, but **has not itself been re-panelled**.
Treat the ladder and the triage rules as the tested-by-use parts, and the
expensive path as the part carrying an unrepaired independence gap.
