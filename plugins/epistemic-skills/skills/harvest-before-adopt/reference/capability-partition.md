# The capability partition — the expensive path

Reached only when triage says the answer matters *and* the harvest could not
supply it: something genuinely requires adopting running software.

This is the most rigorous part of the skill and the part with the most
provenance behind it — a formal derivation record and an adversarial panel that
returned NO-GO on its first form. It is placed behind the harvest deliberately.
**Reaching for it first is the failure mode**, not a shortcut.

---

## Why the obvious rule shape is wrong

A tempting formulation: *"no decision unless fewer than N of M scored rows come
out identically for the top two options."* It is unsound in both directions, by
two finite witnesses:

- `identical = 2` of 11 — nine rows differ, maximal separation under any reading —
  the predicate `2 < 9` holds, so it declares **no decision on the most
  separating evidence possible**.
- `identical = 11` of 11 — nothing differs, zero discrimination — `11 < 9` is
  false, so it **permits a decision on no discrimination at all**.

Inverting the comparator does not repair it. Once the verdict shape is a
*partition* rather than a *selection*, there is no global "top two options", so
the predicate's domain is empty. **The rule has to be re-derived, not
corrected** — which is what the rest of this document is.

The general lesson is portable: a scoring rule that counts agreement across rows
is measuring the wrong thing. Discrimination is per-capability, and a global
count destroys exactly the information that makes the decision tractable.

---

## Step A — Disqualifiers

**Run first. Disqualifiers are not capability rows.**

Licence, security, kill-switch, provenance. A confirmed disqualifier forces every
`ADOPT-EXTERNAL` disposition to `UNDECIDED`; **it can never select a
disposition.** With no adopt row surviving, the candidate is
`NO-ADOPTABLE-SET` — a *derived* label meaning nothing is takeable, not a
thresholded verdict.

> Generalising an existing adoption gate is precisely where this veto gets
> silently dropped. In the live case it vanished without anyone noticing, and was
> found only by grepping the new document for the word. **Check for it by name.**
> Without it, a security defect has to enter as a capability row — where it can
> *select* a disposition instead of vetoing one.

## Step B — Enumerate capabilities; preregister what matters

Closed **before** candidate evidence is cited, in one dated commit.

- **Unit:** a thing the incumbent does *for an operator*, named so an external
  candidate could plausibly do it instead. Not a component, not a file.
- **Admission test:** a row is a capability only if all four dispositions are
  meaningfully assignable **or** it is a genuine incumbent gap (the incumbent
  serves it not at all, so `KEEP-BESPOKE` is vacuous but the others are live).
  *The all-four form alone excludes exactly the incumbent-gap rows the method
  exists to surface — this correction came from running it.*
- **Grain is frozen here**, with a written rule. Subjective-preference rows are
  excluded; rows bundling several independent things are decomposed. Later
  splitting or merging needs recorded cause and a date.
- **Record the serving component** for each capability, and its revision
  (path + SHA) — this is what makes the coexistence check and bilateral staleness
  mechanical later.
- **Mark what is load-bearing:** losing it or getting it wrong blocks the
  incumbent's accepted contract.

### Preregistration needs independence, not a date

A chronological rule — "written before evidence" — is satisfiable by an author
who already knows the answer. Worse, if the load-bearing subset can be chosen
*after* dispositions are observed, anyone can escape an unfavourable result by
reclassifying every `UNDECIDED` capability as not load-bearing. The guard becomes
vacuous.

**Establish the set by draft → interview → independent review:**

1. **Draft** — the evaluator drafts capabilities, marks, and serving components
   from the incumbent's surface.
2. **Interview** — the operator is asked, in structured questions, which
   capabilities actually matter and why, *before dispositions exist*. This is what
   makes the set operator-sourced. **Approval alone is not enough: approval cannot
   see what a draft silently omitted.** Record the questions and verbatim answers.
3. **Independent review** — a party that did not author the draft checks it for
   omissions and for marks shaped to an expected answer.

The commit embeds the evidence corpus SHA as it stood, and a named declaration of
every candidate artifact already read.

**Where preregistration was impossible** — the evidence predates the method, or
the evaluator is already contaminated — write `guard degraded` **on the face of
the verdict** and claim no protection from it. Do not quietly proceed as if
compliant. Preregistration binds forward.

## Step C — Discriminate, per capability

Ask only: *does the evidence separate the options for this capability?* Never
"which is better overall."

| Disposition | Requires |
|---|---|
| `ADOPT-EXTERNAL` | candidate serves it, incumbent materially worse or absent, coexistence permits, plus the floor and coordinate below |
| `KEEP-BESPOKE` | incumbent serves it and the candidate **structurally cannot express it**, plus the floor below |
| `BUILD-NEW` | neither serves it adequately; the gap is the finding |
| `UNDECIDED` | evidence does not separate — **the default** |

### Structural expressibility is the discriminator

"Less polished", "less mature", "fewer features" are **maturity** claims. They
decay on their own and do not license keeping yours.

**A `KEEP` is structural only if the change that would refute it lies outside the
candidate's own repository.** A purely additive, non-breaking change its
maintainer could merge is a maturity claim ⇒ `UNDECIDED` + a re-probe date.

Things that *are* structural: a scheduling model that cannot express residency; a
producer that sits in a different trust boundary, so its assertions can never be
authoritative for you without re-derivation; an identity your system owns that the
candidate's session model actively contradicts. Note these are properties of
*where and how it runs*, which its repo cannot change.

**Expect this floor to demote rows against your own inclination.** That is it
working.

### `UNDECIDED` triggers — a floor, not a ceiling

1. The evidence would read the same under either disposition.
2. The decisive evidence sits behind an execution boundary you are not authorised
   to cross. **An unrunnable candidate producing `UNDECIDED` rows is a correct
   output, not a failure of the method.**
3. The claim rests on a source that would move — a mutable tag, an unpinned
   branch, a marketing page.
4. **The evidence record declares its own coverage incomplete on the surface that
   would carry the disposition** — an admitted unread file, an `unverified` label,
   an open gap note. *Partial coverage of a decisive surface is not
   discrimination.* Every row cites both its evidence artifact **and that
   artifact's own completeness label.*

Trigger 4 is the one everyone violates, usually by restating a hedged source
claim as fact one document downstream. Watch for it in your own method text.

**Before reporting a row `UNDECIDED` under trigger 4, check whether closing the
gap is free.** Reading an unread file costs nothing and needs no authorisation.
Reporting an unknown you could have resolved is not rigour.

### Evidentiary floors

A `KEEP-BESPOKE` row: cite a pinned revision and the specific construct that
forecloses the capability · state the change that would refute it, and where it
would have to live · declare the read coverage it rests on.

An `ADOPT-EXTERNAL` row: cite a pinned-revision observation of the candidate
*actually serving* the capability · a named reversal path with its cost · the
coexistence observation from Step D.

### Adoption coordinate

Every adopt row names the **content-addressed identifier** a later install must
use, plus the delta between it and whatever the install mechanism natively
references when that is a tag or a branch. Where the mechanism cannot express a
content-addressed pin, the row says so. Otherwise a one-way door is approved
against a coordinate that can move between approval and install.

## Step D — Coexistence, and it runs first

Localising `UNDECIDED` to one capability is sound **only if the adopt set can
operate alongside everything else without displacing it.** Without this check a
partition can be internally incoherent while every row reads decided.

**Four predicates, recorded for every adopt row:**

1. **Displacement** — does the component serving the adopt set subsume the host of
   another row?
2. **Contract** — the named interface at the seam, which side owns it, and whether
   your required fields are expressible in it.
3. **Lifecycle** — the persistence, session, and deployment assumptions the
   candidate makes about its host, and whether your runtime satisfies them.
4. **Failure semantics** — what the caller observes when the external component is
   absent, slow, or erroring, and which non-adopted capabilities degrade.

**Domain is everything not adopted**, not just what you keep. For each such
capability, name its host today and after adoption; block as unrealizable if any
is subsumed. **Any of (2)(3)(4) unanswered from pinned evidence forces that row to
`UNDECIDED`.**

**Mixed-host detection, before the subsumption clause:** group rows by serving
component; any component whose rows carry more than one disposition is
`MIXED-HOST` and must be split into distinct serving components or have its adopt
rows dropped.

**Three outcomes — silence never falls through to proceed:**

- `SUBSUMES` → re-partition.
- `OBSERVED-COEXISTENT` → proceed, citing a **pinned observation artifact and a
  named observer**.
- `NOT-OBSERVED` → **every adopt row → `UNDECIDED`**, reason recorded.

**Bounded, directed, recorded remedy:** at most **one** re-partition attempt; a
second failure means nothing is adoptable. A coexistence failure is resolved
**only by moving capabilities out of adopt**, never by moving kept ones in. Every
partition submitted and its rejection reason is recorded.

## Step E — Assemble

### No whole-candidate verdict by default, and no threshold

A capability you cannot take is **a factor to weigh, not a determinative one.**
It does not void the capabilities you can take.

Selecting a numeric "too many unknowns" threshold requires a loss function over
(wrong-adopt, wrong-keep, no-decision) that you almost certainly do not have.
**Inventing a number is false precision**, and soliciting one *after* the count is
visible reproduces the same vacuity preregistration exists to close. If the
threshold is not knowable, say so and record the counts so it becomes answerable
later.

### Informed consent is what replaces it

- Every approval request is presented with the **full partition visible in the
  same decision** — which rows are adopt / keep / build / undecided, and how many
  **load-bearing** rows are undecided. Per-row approval without that view lets
  rows accumulate into an adoption nobody ever decided on.
- The record carries `load_bearing_undecided { count, of, rows[] }`, so an unknown
  that was never surfaced is **an artifact, not an absence**.

### Still absolute, and unaffected by the absence of a threshold

A confirmed disqualifier (Step A) · `NOT-OBSERVED` coexistence (Step D) · the four
`UNDECIDED` triggers (Step C). These are per-row and evidence-driven.

### Approval scope

Adopt on a load-bearing capability is operator-approved. So is `BUILD-NEW` on any
capability (it commits build capacity) and `KEEP-BESPOKE` on a load-bearing one
(it commits indefinite maintenance and forecloses the candidate). Because the
load-bearing mark is evaluator-set, either approve every adopt or have the mark
countersigned.

### Staleness is bilateral

Each row cites **(candidate revision, revision of the incumbent component it
compares against)**. Staleness fires when **either** moves. One candidate revision
is pinned for the whole evaluation; if it moves mid-run, *all* rows scored before
the move are stale, not only those textually citing it. Any row moving into or out
of adopt re-fires the coexistence check.

### No recommendation

The output is a partition and its evidence. Disposition of the whole belongs to
whoever owns the one-way door.

---

## Reading a finished partition

The rows are not the finding. **If most `UNDECIDED` rows share one cause, that
cause is the finding** — and it is usually far more actionable than the rows.
"Six rows undecided" is noise; "six rows undecided because the thing was never
run, and running it is an hour in a container" is a decision.

Then **re-run triage**. A partition frequently changes the spend picture it was
commissioned under.
