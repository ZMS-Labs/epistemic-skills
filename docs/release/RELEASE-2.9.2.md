# epistemic-skills 2.9.2

Release date: 2026-07-23

This is the first formal GitHub Release for the repository. It establishes an
immutable stable snapshot for the package that had previously been distributed
from mutable `main` only.

## Highlights

- Adds the repo-backed `outsource` discipline and its router/Helix integration.
- Integrates the five epistemic-flexibility controls across the existing arc.
- Includes the self-reference-safe outsource publication contract introduced
  after 2.9.0.
- Corrects the Gemini and README package inventories to eleven skills and nine
  disciplines.
- Expands canonical CI to score the committed continuity fixture results and
  run the DCO policy unit tests.
- Aligns every live package manifest and installation example on 2.9.2.

## Compatibility

This is a backward-compatible patch over the already advertised 2.9 line. No
skill name, contract schema version, or installation entrypoint is removed.

## Verification contract

The tag is created only after the exact release commit passes the complete
stdlib suite, DCO, CodeQL, manifest parity, JSON parsing, receipt verification,
the UAT judge self-test, and the Gauntlet deterministic tests. Publication also
requires a redacted full-history secret scan and a final tag-to-commit identity
check.

## Known limitations

- The epistemic-flexibility behavioral results establish protocol conformance,
  not behavioral superiority; the full 24-by-4 measurement sweep remains unrun.
- Static trace checks validate declarations and consistency, not runtime tool
  enforcement.
- Cross-harness packaging is deterministic/source-verified, but native install,
  discovery, auto-trigger, and isolation were not exercised in every harness.
- Cursor packaging is ready but the plugin is not yet publicly listed in the
  Cursor Marketplace.
- Gauntlet selector fit scoring remains frozen because it has not demonstrated
  benefit over constrained random fill; constraint and diversity enforcement
  remain active.
