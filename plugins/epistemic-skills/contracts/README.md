# Handoff receipts — `handoff-receipt@1`

A **handoff receipt** is a small JSON document a skill emits alongside its
output so a downstream skill can mechanically verify it received a well-formed
input — instead of re-interrogating the session or re-running checks.

A receipt is a producer **self-issued declaration** of **identity,
well-formedness, provenance, and a validity window**. It is not signed and not
counter-attested: the verifier (`verify_receipt.py`) certifies the **envelope
only** — binding and well-formedness — **not origin, and not the truth of
self-reported fields**. **"Trust" in this contract means exactly that envelope
and nothing more.** No field and no rule raises a consumer's confidence in a
judgment it did not make or re-verify.

## What a receipt never attests

Every receipt carries a non-empty `never_attests` array. The standard entries:

- `verdict-truth` — the receipt says nothing about whether the judgment in an
  artifact is right.
- `independence-achieved` — procedural properties (lens isolation, blinded
  verifier) are recorded as metadata, never certified.
- `freshness-beyond-window` — validity ends where `valid_while` ends.

The schema has no field capable of carrying a verdict, an approval, a
confidence score, or an independence claim; those words may appear only inside
`never_attests`.

## Validity windows and staleness

`valid_while` is a **closed predicate vocabulary**, evaluated by the
*consumer*, cheaply and mechanically:

| Predicate | Holder | True iff |
|---|---|---|
| `subject-revision-unchanged` | any receipt | recorded `subject.revision` equals the subject's current revision at consume time |
| `session-continuous` | any receipt | the receipt's `session` keyed hash equals the consumer's current-session keyed hash (equality only; the raw session id is never persisted) |
| `freeze-window-open` | gauntlet receipts | the dossier identified by `subject.sha256` has had no controlled reopen recorded since the freeze timestamp |
| `environment-reachable` | UAT receipts | the target environment answers at consume time |

A receipt whose predicates fail is not wrong — it is **stale**, and the
consumer re-runs exactly the freshness-sensitive check, nothing else.

- **Null subjects fail closed.** Null `subject.revision` MUST NOT be combined
  with `subject-revision-unchanged` (the verifier rejects it, nonzero exit,
  named reason). Any predicate that is unevaluable for a subject defaults to
  **stale** — stale-by-default, never silently valid.
- **Bounded downgrade.** A stale receipt is not discarded: its **envelope
  fields** (identity, well-formedness, provenance — run-order facts, hash
  equality, consent facts) downgrade one evidence tier (verified → dated
  inference). **Judgment-carrying kinds do not downgrade**: stale
  `derived-verdict`, dossier, and gate/verdict artifacts are ENVELOPE-ONLY —
  their judgment content is re-verified or void. Only envelope fields survive
  staleness.
- **Regime precedence.** Predicate failure outranks downgrade: a failed or
  unevaluable predicate means stale → re-run the freshness-sensitive check.
  The downgrade applies only when predicates are unevaluable or the only
  change is the session boundary.
- **Supersession (locality-bound).** For the same producer+subject, a later
  receipt supersedes earlier ones *within the artifact set presented to a
  single consumer at one consume point* (the `run.id` sequence gives the total
  order). A superseded receipt is not consumed at all. Supersession is not a
  global registry query; the verifier does not check it; stamps are outside
  it. It sits below predicate-failure: a superseded-but-valid head is
  displaced, but a stale head is still stale.

## Carrier split

- **JSON receipts** for file-producing skills (gauntlet, UAT,
  evidence-research matrix, file-written goal contracts) — verified by
  `verify_receipt.py`.
- **4-field stamps** for prose-producing skills (blindspot-pass,
  formal-rigor, write-goal, router): `subject.ref`, `subject.revision`,
  `valid_while` (same closed vocabulary), `coverage_limits`. The producer is
  the emitting skill by construction. **The verifier never parses prose.**

## Committed-artifact boundary

- **Committed (this repo):** the schema, verifier, this README, and the
  synthetic example receipts under `examples/`. They carry no operator data by
  construction.
- **Local-only (never committed):** run directories, dossiers, live receipts
  over real subjects, and screenshot-class captures. The repo-root
  `.gitignore` covers the run output roots (`outputs/`,
  `artifacts/uat/**/screenshots/`). Live run records may keep exact
  timestamps and per-seat model identity because they never leave the
  operator's machine.

## Privacy necessity pass

Every field in the schema has a named mechanical consumer:

- `run.session` is an **equality token**: a session-scoped key exists only in
  memory for the session's lifetime; the token is recomputed per run under
  that key. Two receipts carry equal tokens iff produced in the same session.
  The key and the raw harness session id are never persisted.
- `run.at` is **day-granularity** — every `valid_while` predicate consumes
  date precision and none consumes finer.
- `trigger.matched` is a **closed trigger-class** vocabulary and `subject.ref`
  is **hash-or-class** — no verbatim user prose is hash-bound into permanent
  artifacts.
- The `run.id` slug segment is the same subject-class-or-hash as
  `subject.ref`, never free text.
- `producer.sha256` is the **content pin** of the producer SKILL.md — a hash
  is an immutable coordinate; a version tag drifts.

## Verifying

```bash
python verify_receipt.py RECEIPT.json --artifact-root DIR
python verify_receipt.py --self-test
```

Exit 0 with a one-line OK summary on pass; nonzero exit with a named reason
(`SCHEMA_VIOLATION`, `BAD_PRODUCER_SHA256`, `MISSING_NEVER_ATTESTS`,
`UNKNOWN_PREDICATE`, `NULL_REVISION_PREDICATE`, `ARTIFACT_MISSING`,
`ARTIFACT_HASH_MISMATCH`) on any miss. Stdlib-only; the verifier never
evaluates judgment content.

## Extending the vocabularies

A new predicate, trigger-class, or artifact kind is added only by
**schema-version bump + verifier update in the same PR** — unknown values fail
closed by design, so a misfit blocks loudly and is never silently absorbed.
