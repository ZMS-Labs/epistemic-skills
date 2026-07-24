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
- Aligns every live version-bearing package manifest on 2.9.2 and distinguishes
  tagged stable installs from rolling repository installs.

## Compatibility

This is the first formal immutable baseline for the already-advertised 2.9 lineage;
it does not claim an evidence-backed comparison with an earlier immutable
release. Relative to the immediately preceding `main` state, no skill name,
contract schema version, or installation entrypoint is removed.

## Verification contract

The tag is created only after the exact release commit passes the complete
stdlib suite, DCO, CodeQL, manifest parity, JSON parsing, receipt verification,
the UAT judge self-test, and the Gauntlet deterministic tests. Publication also
requires a redacted full-history secret scan and a final tag-to-commit identity
check.

## Harness verification matrix

"Source-verified" means manifests, inventories, paths, and deterministic package
contracts were checked. It does not mean that native install, discovery,
auto-trigger, or isolation was exercised in that harness.

| Harness | Documented channel for 2.9.2 | Verification tier |
|---|---|---|
| Claude Code | Tagged checkout for stable; bare marketplace repo is rolling | Source-verified |
| Codex | Direct immutable `--ref v2.9.2`; `--ref main` is rolling | Source-verified plus deterministic package tests |
| Cursor | Tagged checkout for stable; `main` checkout is rolling; public marketplace not listed | Source-verified |
| Gemini CLI | Tagged checkout plus local link for stable; bare repo URL is rolling | Source-verified |
| Antigravity | Tagged checkout plus local install for stable; bare repo URL is rolling | Source-verified |
| Kimi Code | Tagged checkout plus local install for stable; bare repo URL is rolling | Source-verified |
| Generic Agent Skills harness | Tagged checkout for stable; `tree/main` URL is rolling | Source-verified |

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
