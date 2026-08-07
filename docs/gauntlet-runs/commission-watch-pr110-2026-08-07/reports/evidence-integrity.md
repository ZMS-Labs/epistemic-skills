# Lens report — evidence and oracle integrity

**Role:** metatextual/evidence evaluator  
**Subject:** frozen `review/pr110-commission-watch-candidate-v2`  
**Question:** Do the tests and documentation prove the claims they are used to support?

## Validation kernel

The candidate correctly refuses to equate configuration presence, source reads,
formatter tests, or silence with an operating observer. Its strongest contribution
is not the number of checks but the alignment between each success claim and a
specific external evidence carrier.

## Evidence ladder

| Claim | Available evidence | Supported conclusion |
|---|---|---|
| The skill no longer claims to be the observer | skill description/body and live README/health language | supported at source level |
| The carrier has a closed structural shape | JSON Schema plus schema/verifier parity test | supported for checked-in schema and code |
| Cross-field states reject planted false assurances | semantic test corpus and accepted/rejected examples | supported for enumerated controls |
| The sentinel rejects a prompt-time skill as observer | planted in-memory control plus committed sentinel | supported for the encoded oracle |
| Positive booleans cannot stand without receipt refs | verifier rules and focused tests | supported structurally |
| Receipt refs are authentic external evidence | no dereferencing/authentication layer | not established |
| A production watch was commissioned | no production adapter or receipt | not established |
| Practical Agency can consume the carrier | design and implementation plan only | not established |
| Exact candidate passed GitHub PR CI | workflows are `action_required`, no jobs created | not established |
| Package description cost did not increase | exact budget gate records 8,159 bytes against same 14-skill inventory | supported when gate executes |

## Findings

### F-EI-1 — Schema/verifier drift was initially possible

**Severity:** P2  
**Status:** resolved in candidate

The first contract iteration could have allowed the public JSON Schema and the
stdlib semantic verifier to evolve separately. Example tests exercised the Python
oracle but did not establish field/enum identity between the two surfaces.

**Resolution:** `test_structural_schema_matches_semantic_verifier` derives the
canonical top-level fields, nested object fields, and closed enum sets from the
semantic implementation and requires the published schema to match exactly.

**Falsifier:** The resolution fails if a schema field or closed enum changes while
the parity test remains green. The test compares both required and properties sets
for every nested object plus all governing enums.

### F-EI-2 — Receipt references could be overread as verified facts

**Severity:** P2  
**Status:** resolved as an explicit contract boundary

Required evidence-reference presence is materially stronger than booleans alone,
but it is not authentication. Without explicit language, a consumer could report
that the semantic verifier “verified the alert receipt” when it only verified that
a non-forbidden reference was present.

**Resolution:** the contract README and security boundary now state that the
verifier does not dereference, authenticate, or establish the truth of external
receipts. Consumers must resolve each material reference against a trusted source
and verify the proposition it supports.

**Falsifier:** The resolution is inadequate if user-facing or adapter guidance
still describes a shape-valid record as verified real-world evidence. The skill
instead says structural validity is not automatic trust, and the future adapter
plan preserves upstream semantic authority plus external evidence resolution.

### F-EI-3 — GitHub workflow state is not a green oracle

**Severity:** P2 process blocker  
**Status:** open external condition

The PR's `epistemic-flexibility`, `commission-watch-contract`, and CodeQL workflows
are `action_required`; their runs created zero jobs. This is consistent with
GitHub withholding app-authored workflow changes pending approval. It is not
consistent with saying the tests passed.

**Falsifier:** This finding closes only when jobs execute on the exact candidate
and conclude successfully, or when an equivalent trusted exact-ref execution is
recorded with command output. A status label without jobs is insufficient.

### F-EI-4 — RED chronology is genuine, not reconstructed from green

**Severity:** positive observation  
**Status:** retained

The branch history preserves distinct failing revisions for:

- the absent verifier;
- the missing user-facing commission boundary;
- the prompt-time-skill sentinel;
- state versus proof-history separation; and
- evidence-bearing blocked states, prepared-mechanism control, fixture scope, and
  prompt/self-asserted evidence refusal.

The later implementations made those same focused checks pass. This does not
prove completeness, but it does establish that the controls detect the targeted
missing behavior rather than merely accepting all input.

## Verdict from this lens

**CONDITIONAL.** The artifact-level evidence is strong and its earlier P2 contract
ambiguities were fixed. Merge readiness still depends on executing trusted jobs
against the exact final candidate; `action_required` with no jobs is not a pass.
