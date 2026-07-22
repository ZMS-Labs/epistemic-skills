<!-- gauntlet-dossier@1
frozen_at: 2026-07-22T00:00:00Z
subject_path: evidence/handoff-receipt.schema.json
subject_revision: example-rev-1
evidence_root: evidence
evidence_root_sha256: f05efa3e24fa0c3465a367d24d4d9d23a15a443b04673205d9f3d4959a16b1c8
-->
# Frozen dossier — adopt a handoff-receipt schema for a skills repo

**SYNTHETIC EXAMPLE — not a real run.** Everything below is fictional, written to
give the run-record / ledger-v2 contract a concrete, scrub-free exemplar. The real
runs that motivated this machinery were private and were removed; this example is
the shipped sample of every artifact shape (audit 04 §5.7, proposal 1).

## Subject lock (Step 1)

- Path: `evidence/handoff-receipt.schema.json` · revision: `example-rev-1` · scope:
  the draft receipt schema only · exclusions: verifier implementation, per-skill
  emit edits.
- Evidence root: `evidence/` — pinned by content hash at freeze (see header);
  `[V path:line]` tags are valid only while the pin holds.

## Verified premises (Step 0, live-verified at freeze)

- The draft schema closes the `valid_while` vocabulary to three predicates
  (verified — file read at freeze).
- The draft's session field is specified as a keyed-hash token, not a raw id
  (verified — file read at freeze).
- The fictional repo's conventions require schema + verifier to land in one PR
  (source-supported — conventions excerpt).

## Uncertainty labels

- synthetic: every premise and artifact in this run is fictional.
- incomplete: no verifier exists in this fictional repo; out of scope for the panel.
