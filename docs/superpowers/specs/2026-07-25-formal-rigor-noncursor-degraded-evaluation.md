# Formal-rigor non-Cursor degraded evaluation design

## Decision and authority

The operator authorized completion of the 3.0.0 release process without Cursor,
accepting a degraded evidence claim that is recorded honestly and may be
strengthened by a future targeted third-provider study. This amendment does not
repair, overwrite, relabel, or credit any failed Cursor epoch.

The selected design is a new, explicitly named two-provider protocol. The
original frozen three-provider protocol remains historically valid as a failed
and externally blocked protocol; it is not retroactively edited.

## Alternatives considered

1. **Remain blocked on Cursor.** Preserves the strongest preregistered provider
   diversity, but prevents release for a transport capability the product does
   not control. The operator rejected this option.
2. **Run a preregistered two-provider degraded protocol.** Preserves fresh
   replication, model-family diversity, candidate/judge separation, immutable
   raw evidence, and fail-closed scoring while narrowing the generalization
   claim. **Selected.**
3. **Introduce an unplanned third provider.** Restores a nominal third arm but
   adds a new harness, model, and transport contract during release closure.
   This moves rather than resolves the comparability problem and is deferred.

## Formal basis

- **Architecture and failure domains (P7):** Cursor is a single external
  transport failure domain. Making release liveness depend indefinitely on a
  schema capability absent from that surface couples publication to an
  uncontrollable dependency. A named degraded mode contains that failure domain
  without concealing it.
- **Type and contract integrity (P5):** `frozen-three-provider` and
  `noncursor-degraded-v1` are distinct protocol identities. Making the choice an
  explicit CLI value makes illegal silent substitution unrepresentable; every
  summary and call record carries the selected identity.
- **Experimental design:** a new preregistered epoch prevents post-hoc selection.
  Replication remains three candidate repetitions, while two independent,
  candidate-blinded semantic seats judge every candidate response. The loss is
  provider breadth, not within-protocol replication.
- **Information/provenance (P6/P7):** raw events, stderr, response bytes, packet
  hashes, source commit, harness, provider, model, and protocol identity remain
  retained. Failed historical roots stay content-pinned.

The concession is explicit: passing this protocol supports the candidate on
the tested OpenAI Codex and Google Gemini families. It does not establish a
three-provider result or Cursor output-contract reliability.

## Provider allocation

The protocol identity is `noncursor-degraded-v1`.

- Candidate and missing baseline repetitions: repetition 1 = Codex, repetition
  2 = agy/Gemini, repetition 3 = Codex.
- Parodies: three fixed arms use Codex and three fixed arms use agy/Gemini.
  The two former Cursor parodies are reassigned before the epoch begins.
- Semantic adjudication: both seats are separate, context-isolated calls on the
  provider other than the candidate response's provider. Seat reports remain
  immutable and cannot see one another. Same-provider seats are a disclosed
  diversity limitation, not a relaxation of isolation.
- The arm plan remains 286 calls and the semantic plan remains 132 calls. No
  call is retried once its `call.json` exists.

## Runner behavior

`run_live.py` gains an explicit `--provider-plan` choice for `plan`, `run-arms`,
and `run-semantic`:

- `frozen-three-provider` remains the default for historical replay.
- `noncursor-degraded-v1` selects only `codex` and `agy` and never invokes the
  Cursor executable or Fleet Cursor bridge.
- Allocation helpers require the plan identity rather than reading mutable
  environment state.
- Every call and run summary records `provider_plan`; conflicting reuse of an
  output root fails closed.

## Gates

A fresh pushed source commit and a new empty output root are mandatory.

The degraded campaign counts only if:

1. every planned arm and semantic call is terminal, parseable, schema-valid,
   secret-screen clean, identity matched, and provenance complete;
2. all three candidate repetitions pass all 22 structural fixtures;
3. the neutral/current-v1 and six parody controls exhibit their preregistered
   failure polarity;
4. both independent semantic seats return `VALID` for every candidate response,
   with existing disagreement and P0 rules unchanged;
5. the root is content-pinned and the exact results, limitations, and dissent
   are committed before release review.

Any terminal failure ends that epoch. A new correction requires a new source
commit and new output root.

## Release meaning and follow-up

If the degraded campaign passes, the formal-rigor release blocker is replaced
by a known limitation, not erased. Release notes must state that v3.0.0 has
two-provider behavioral evidence and no qualifying Cursor result. The original
Cursor roots and `BLOCKED_EXTERNAL` diagnosis remain linked.

Cursor becomes a non-blocking future evidence gap. Revisit when Cursor exposes
schema-constrained generation or when a separately designed targeted
third-provider conformance protocol is approved. Any future result supplements
v3.0.0 evidence; it cannot retroactively change what the release established.

## Test strategy

RED-first runner tests must prove:

- the new plan contains no Cursor tasks and retains 286 arm plus 132 semantic
  calls;
- candidate, baseline, parody, and semantic allocations match this document;
- every semantic seat differs from its candidate response provider;
- the historical default allocation is unchanged;
- call and summary provenance includes the provider-plan identity;
- output-root protocol conflicts fail closed.

After GREEN, run the complete deterministic suite before creating the fresh
live epoch.

## Completed v1 exclusion and prospective v2 identity

The completed `noncursor-degraded-v1` epoch at source
`a18e8ba41085c7d45b126e342b3222a19e497bc6`, canonical root pin
`11eecc3d589a88ccb19dc5117a2a0cfdd5019252f4bc5c528a98581c61efbe5a`, is
excluded. It recorded 286 terminal calls, of which 281 qualify and five fail:
two raw telemetry user-profile-path leaks (one agy and one Codex; final
responses clean), two agy strict-schema violations (v1-style record shape and
object `uncertainty_posture` rather than the required string), and one agy
self-talk/fenced two-identical-draft response. It has no scoring, semantic, or
release credit and cannot be retried, repaired, resumed, or reused.

The new `noncursor-degraded-v2` identity is prospective and distinct from v1.
It keeps the same two-provider map, 286 arm/132 semantic counts, unchanged
thresholds, terminal/no-retry behavior, and two-provider-only claim boundary.
Before execution, an output-adjacent neutral packet root is rejected if it is
profile-bound. Direct agy calls use `agy --add-dir .`; agy arms use medium
effort, agy semantic calls high effort, and Codex calls high effort. The exact
frozen transport schema is embedded in every non-native-schema arm prompt;
every non-native-schema semantic prompt embeds only the exact semantic
transport schema, never truth or scorer material. The campaign plan and every
call record the v2 identity, canonical packet root, and execution
policy/settings. Frozen and v1 identities remain inspectable but non-runnable
under current source; historical execution requires their pinned commits. A
complete v2 epoch uses active Codex and agy harnesses that reject Fleet-bridge
overrides; any bridge-backed evaluation requires its own preregistered protocol
identity. A complete v2 epoch passing every unchanged gate is required before
release can move beyond HOLD; historical Cursor blocking evidence remains intact.
