#!/usr/bin/env bash
# Local CI wrapper — issue #95. See docs/CI-LOCAL-FALLBACK.md.
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
REF="${1:-HEAD}"
SHA="$(git -C "$ROOT" rev-parse --verify "${REF}^{commit}")"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RECEIPT_DIR="$ROOT/docs/evidence/local-ci"
RECEIPT="$RECEIPT_DIR/${SHA}.md"
mkdir -p "$RECEIPT_DIR"

log() { echo "$*" | tee -a "$RECEIPT"; }

: >"$RECEIPT"
log "# Local CI receipt"
log ""
log "- **commit:** \`${SHA}\`"
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
