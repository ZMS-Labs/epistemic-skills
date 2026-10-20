# Issue #162 bounded local safeguard candidate

2026-10-20; based on released commit
`6f31811a173967568513d5deec316199c2df7669`. Local implementation and validation
only; issue #162 remains open. No commit, push, PR, merge, release or deployment.

## Implemented behavior

Managed approval, draft/active effects, reconcile and PASS refuse on a known
finite-witness mismatch or UNKNOWN. Effects check the existing actual parent
before fresh quarantine acknowledgements and again at the common write seam.
Root observations never authorize descendants. Missing target hierarchies are
not created. PASS also checks readable receipted-artifact parents. Checkpoint,
receipt, verdict and manifest schemas are unchanged.

The POSIX descriptor-relative probe creates an exclusive pending sidecar and
syncs its file and containing directory before creating scratch in the measured
directory. Only completed measurement, ownership-checked cleanup and a directory
sync permit removing the sidecar. Unexpected entries are preserved. Any pending
sidecar across the workspace mission union blocks managed operations regardless
of approval, readable chain, epoch or acknowledgement; unreadable discovery is
UNKNOWN. Status/resume retain diagnostics without manufacturing schema fields
or checkpoint obligations. No automatic orphan recovery/deletion/adoption is
provided.

Finite witnesses are ASCII case, sharp-s and NFC/NFD pairs. Agreement means
NO_MISMATCH_OBSERVED for those pairs/context only. No broad filesystem support,
complete Unicode identity, universal replacement-race or power-loss guarantee
is claimed. Filesystem persistence primitives must honor their contract.

## Validation and corrections

Tests were observed red before implementation. Later sibling-union, suppressed
discovery-error, diagnostic-probe and root-resolution regressions were each
observed red before correction. Independent review reproduced a material sibling
latch gap; workspace-union discovery now closes it. Review also corrected the
explicit declared-exclusion fixture.

The continuation found an actual PASS error-path defect: gathering receipt
parents could leak a symlink-loop RuntimeError on Python 3.12. A real symlink-loop
regression with explicitly simulated compatible measurement observed that red.
PASS now preserves AcceptanceRefused, mapping unavailable path resolution to
UNKNOWN; no exception becomes a successful verdict.

- Existing bundled CPython 3.12.14 on this Mac was used in a workspace-local venv;
  system Python/defaults were unchanged. Default Python remains 3.14.7.
- All 26 focused safeguard tests pass on Python 3.12. They cover actual Mac alias
  refusals, an explicit `secrets.env` exclusion, CLI exit contracts, pending state,
  interruption/corruption/replacement/permission/persistence failures, sibling
  union and unreadable discovery, unavailable primitives, missing parents,
  early refusal and retained late acknowledgement. Compatible measurements and
  injected failures are simulations. Independent review also ran all 26 on the
  default Mac Python and found no remaining material finding.
- Native diagnostic: filesystem folds case, comparator does not; managed
  operation reports SAFEGUARD REFUSED, with the comparison defect still open.
- Native Python 3.12 semantic/schema contract: 143 checks pass; store: 19 pass.
- JSON Schema parity passes: 8 fields x 33 cases plus compound control, on both
  Python 3.12 and 3.14. Exact repository dependency versions were installed from
  official PyPI into isolated workspace testenvs using binary wheels and required
  hashes. Only rpds-py's platform wheel hash differs from the Ubuntu lock; each
  Mac wheel digest was verified against official PyPI release metadata. The
  checked-in Ubuntu/Python 3.12 lock was not edited.
- All six legacy suites pass under explicitly simulated compatible measurement
  on Python 3.12: lifecycle 831, CLI 895, gate 183, es173 144, hook 200 and process
  proof 46 printed checks (2,299 total). The real managed gates, parent restriction
  and sidecar lifecycle remain in place; only pair measurement is simulated.
- Successful-write fixtures now explicitly prepare parents. Assertion ASTs are
  unchanged for 273 existing cases. Two old automatic-mkdir/unwind tests were
  deliberately replaced with missing/overlong-parent refusals, unchanged-chain
  and receipt controls, and existing-directory/write-error controls. The earlier
  manual test patch's added lines remain preserved; its gate file is unchanged.
- Native legacy results are **not green** on this aliasing Mac: per-case execution
  reports 208 failing cases out of 275. Of these, 188 directly raise the accepted
  KNOWN_MISMATCH refusal; 20 assertion cascades have captured subprocess evidence
  of that same refusal. Their exact names and traces are retained in local
  validation receipts. The simulated compatible matrix has no remaining failure.
- Compile, whitespace and assertion-preservation checks pass. No CLI security
  scan coverage is claimed; the previous external-egress denial was respected.

## Remaining integration gates

Local validation gaps available here are closed. Native compatible-filesystem,
Linux/NTFS/per-directory qualification and hosted CI remain absent. The locally
wired focused-test command covers the Ubuntu workflow job; it does not establish
hosted Mac coverage. Simulated success is not a substitute for these boundaries.

The candidate remains uncommitted and not integration-approved. Prior test-only
edits remain separately recorded; no integration/publication authority is implied
by the combined local working tree. No automatic recovery mechanism, identity
schema migration, broad Unicode support or issue closure is part of this lane.
