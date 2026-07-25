# applying-formal-rigor v2 blinded fixtures

This directory implements Phase B of the approved v2 design. It is a blinded conformance
smoke check, not a population measurement or truth oracle.

- `fixtures/<id>/scenario.md` and `artifacts/` are run-agent visible.
- `ground-truth.json`, `score.py`, thresholds, and other results are scorer-only.
- the public response and v2 record schemas close their persisted vocabularies;
- `formal-rigor-fixture-transport.schema.json` is the strict, inlined,
  OpenAI-compatible projection used to fail closed at model-output time;
- `semantic-adjudication.md` owns independent derivation judgment;
- `results/` records immutable identities, hashes, dissent, and coverage limits.

Run `python tests/run_tests.py` and `python score.py --inventory-only`.

The authorized full live battery is executed by `run_live.py` from a clean,
pushed candidate commit:

```text
python run_live.py plan
python run_live.py run-arms --output-root <durable-temp-root> --arm v2-candidate --repetition 1 --fixture tm-01-false-mvd --workers 1 --cursor <cursor-agent-path>
python run_live.py run-arms --output-root <durable-temp-root> --workers 4
python run_live.py run-semantic --output-root <durable-temp-root> --workers 4
python run_live.py summarize-semantic --output-root <durable-temp-root>
```

An authenticated Fleet Orchestrator surface bridge may be used explicitly when
the local harness is unavailable:

```text
python run_live.py run-arms --output-root <durable-temp-root> --cursor fleet-bridge://default/fleet-orchestrator/surface-bridge-v2-0 --cursor-model auto
```

This adapter sends a sealed, scorer-free virtual packet over `kubectl exec`
stdin to the bridge's full-output `/stream` endpoint. It never clones the
repository into the agent workspace, and the local command line contains no
fixture payload. The bridge currently does not forward a requested model to
its Cursor or Gemini streaming helpers, so the adapter rejects every model id
except the honest `auto` label and records `surface-default-auto` in each call.
Raw bridge NDJSON is always retained. If Cursor emits multiple complete
snapshots for the same recognized response envelope and fixture, only the
final snapshot is materialized and that normalization is recorded; distinct
envelopes fail closed. If one malformed snapshot is immediately followed by
one terminal complete snapshot, recovery is limited to matching recognized
envelope and fixture headers with no other marker or trailing content; every
ambiguous form remains unnormalized. Calls through one runner process are
serialized because the shared bridge pod can be terminated under concurrent
Cursor streams; local Codex and agy calls still use the requested worker
concurrency.
Use of this adapter is therefore a disclosed transport/model-plan variance,
not evidence for the pinned Cursor model below.

Local Codex arm calls receive the complete sealed packet on stdin rather than
the Windows command line. The prompt embeds the scenario, minimal artifacts,
applicable pinned-v1 files, candidate skill, theory battery, and module index;
material module bodies remain available in the sealed packet for selective
reading. The transport schema rejects readiness acknowledgements and other
non-response text before it can be mistaken for a scored answer.

Local plain-text harness stdout is retained unchanged in `events.jsonl`. When
that stdout contains prose or a Markdown fence around exactly one complete,
top-level `formal-rigor-fixture-response@1` or
`formal-rigor-semantic-adjudication@1` JSON envelope, the runner may extract
that envelope into `response.json` and records
`response_normalization: extracted-single-recognized-json-envelope` in
`call.json`. This is transport normalization only: it does not repair fields,
consult scorer truth, or imply schema or semantic validity. Zero recognized
envelopes, repeated or distinct envelopes, nested schema/prompt echoes, and
ambiguous or truncated recognized JSON remain unnormalized and fail closed at
the existing JSON-parseability gate. Fleet bridge snapshot normalization keeps
its separate, stricter provenance and distinct-envelope protections.

The plan contains 286 arm calls (the two missing repetitions for each baseline,
three candidate repetitions, and all six 22-fixture parodies) plus 132 isolated
semantic-seat calls. Calls are fresh and terminal: once a `call.json` exists,
the runner never retries it. Transport, parse, secret-screen, packet hashes,
raw response, events, and stderr are retained for adjudication and export.

The provider allocation is frozen rather than additive: candidate repetitions
1/2/3 use Codex OpenAI `gpt-5.6-sol`, agy Gemini `gemini-3.1-pro-high`, and
Cursor CLI `gpt-5.6-sol`, respectively. Missing baseline repetitions follow the
same mapping, two parody arms are assigned to each harness, and semantic seats
rotate across the two harnesses other than the candidate response's harness.
The preregistered 418-call plan remains the identity of the original epoch;
it is a plan size, not a continuing authorization ceiling. Any correction run
uses a new immutable output root and is reported as a separate epoch rather
than overwriting or retrying a recorded call. Including the 44 already-recorded
OpenAI RED baseline calls, each harness contributes 154 arm-plus-adjudication
calls in the original plan.

Absent or non-isolated model execution is `NOT_RUN`, never a RED result credited to an
arm. Neutral and current-v1 RED runs were durably recorded before production edits under
`results/2026-07-24-red-baseline/`; candidate, parody, and semantic arms remain separately
gated and `NOT_RUN` until executed.
