# Consensus integration boundary

## Role separation

`consensus-research` establishes and verifies the scholarly record. Gauntlet
adversarially evaluates the decision against the frozen record and alone
computes GO/CONDITIONAL/NO-GO. Ordinary web search is not a literature review,
and a Consensus-only scan is not a complete systematic review.

Consensus claims do not bypass the Gauntlet evidence hierarchy. A claim enters
the dossier as `[V]` only to the level actually verified; an inference grounded
in that record is `[I]`; an unverified proposition remains `[H]`.

## Before dossier freeze

Invoke `consensus-research` only when peer-reviewed evidence is material. Add a
claim-evidence matrix with:

- claim and Gauntlet `[V]`/`[I]`/`[H]` mapping;
- source ID, title, exact URL/DOI, authors, and year;
- study design, population/context, and result direction;
- metadata-level, abstract-level, fetched, or full-text verification level;
- direct support, indirect support, contradiction, or no information;
- limitations, correction/retraction status, and cohort/version family.

Add the Consensus run record with queries, filters, result counts,
selected/fetched IDs, exclusions, limitations, warnings, timestamps, and
provenance. Preserve coverage limits and uncertainty when the dossier freezes.

## During the panel

All lenses receive the same frozen scholarly record. They perform no ad hoc
Consensus searches. A lens may identify a missing-evidence finding and
falsifier, but it may not privately expand the record or convert a search result
into a new verified premise.

## After adjudication

Use Consensus again only for a material scholarly-evidence gap that could change
a P1/P2 finding or verdict. Perform a controlled dossier reopen:

1. preserve the prior dossier revision and verdict;
2. record the reason for reopening and the new search provenance;
3. attach the updated claim-evidence matrix and run record;
4. freeze a new dossier revision;
5. recompute every affected criticism, arbitration, coverage statement, and
   verdict stage.

Never silently amend, overwrite, or backfill an existing verdict.
