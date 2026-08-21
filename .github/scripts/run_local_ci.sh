#!/usr/bin/env bash
# Local CI wrapper — issue #95. See docs/CI-LOCAL-FALLBACK.md.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
REF="${1:-HEAD}"
SHA="$(git -C "$ROOT" rev-parse --verify "${REF}^{commit}")"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
# The receipt is named for a COMMIT but describes the WORKING TREE, so whenever
# the tree is dirty the filename asserts something false -- and writing it inside
# the repository meant that false artifact was one `git add -A` away from being
# committed. It happened twice during the v6.0.0 release and was caught by hand
# both times. The receipt now lands OUTSIDE the repository by default, and its
# name carries the tree hash it actually describes rather than only the commit.
TREE="$(git -C "$ROOT" write-tree 2>/dev/null || echo unknown)"
DIRTY=""
if ! git -C "$ROOT" diff --quiet HEAD 2>/dev/null; then DIRTY="-dirty"; fi
RECEIPT_DIR="${LOCAL_CI_RECEIPT_DIR:-${TMPDIR:-/tmp}/epistemic-skills-local-ci}"
RECEIPT="$RECEIPT_DIR/${SHA:0:12}-tree-${TREE:0:12}${DIRTY}.md"
mkdir -p "$RECEIPT_DIR"

log() { echo "$*" | tee -a "$RECEIPT"; }

: >"$RECEIPT"
log "# Local CI receipt"
log ""
log "- **commit:** \`${SHA}\`"
log "- **tree actually tested:** \`${TREE}\`${DIRTY:+ (working tree is DIRTY -- NOT the tree of that commit)}"
log "- **started:** ${STAMP}"
log "- **host:** $(uname -a 2>/dev/null || true)"
log ""

log "## cleanroom (epistemic-flexibility steps)"
if ! bash "$ROOT/.github/scripts/cleanroom_ci.sh" "$SHA" 2>&1 | tee -a "$RECEIPT"; then
  log ""
  log "**result:** FAIL (cleanroom)"
  exit 1
fi

log ""
log "## commission-watch-contract (when workflow exists)"
if [ -f "$ROOT/.github/workflows/commission-watch-contract.yml" ]; then
  (
    cd "$ROOT"
    python plugins/epistemic-skills/contracts/watch-commission/test_watch_commission.py
    python -m py_compile plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py
    mapfile -t examples < <(find plugins/epistemic-skills/contracts/watch-commission/examples -maxdepth 1 -name 'valid-*.json' -print | sort)
    python plugins/epistemic-skills/contracts/watch-commission/verify_watch_commission.py "${examples[@]}"
    python .github/scripts/score_sentinels.py --self-test
    python .github/scripts/score_sentinels.py
    python .github/scripts/check_description_budget.py --self-test
    python .github/scripts/check_description_budget.py
    python .github/scripts/check_json_artifacts.py
    python .github/scripts/check_no_phantom_skills.py
    python .github/scripts/check_skill_inventory.py
    python .github/scripts/sync_skill_surfaces.py --check
    git diff --check
  ) 2>&1 | tee -a "$RECEIPT"
else
  log "(skipped — workflow absent on this ref)"
fi

log ""
log "**result:** PASS"
log "- **finished:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
