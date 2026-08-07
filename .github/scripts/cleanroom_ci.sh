#!/usr/bin/env bash
# Run this repo's CI suites in a clean-room Linux checkout, without GitHub Actions.
#
# WHY THIS EXISTS
# ---------------
# A local run on the developer's working tree is not the same evidence as CI:
#   - it is Windows/MSYS2, not Linux — CRLF, path separators, and case
#     sensitivity all differ, and every one of those has produced a real defect
#     in this repo;
#   - it runs against a dirty tree with untracked files and stale __pycache__,
#     so it can pass on artifacts that were never committed;
#   - it shares state with whatever the developer was just doing.
#
# This script removes all three: a fresh detached checkout of the exact
# locally available commit named by REF, or a fresh clone of a remote branch/tag
# when that commit is not local, running exactly the workflow-declared Python
# steps. It is not a replacement for CI's independence — it runs on the same
# operator's hardware — but it is a strictly better local signal, and it costs
# no Actions minutes.
#
# It parses the step list OUT OF the workflow rather than duplicating it, so it
# cannot drift from what CI actually runs. A hardcoded copy would be one more
# hand-maintained projection, which is the defect class this repo keeps finding.
#
# USAGE
#   bash .github/scripts/cleanroom_ci.sh [REF] [REMOTE_URL]
# Defaults: REF=main, REMOTE=https://github.com/ZMS-Labs/epistemic-skills.git
set -uo pipefail

REF="${1:-main}"
REMOTE="${2:-https://github.com/ZMS-Labs/epistemic-skills.git}"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "clean-room CI"
echo "  ref     : $REF"
echo "  os      : $(. /etc/os-release 2>/dev/null && echo "$PRETTY_NAME" || uname -s)"
echo "  python  : $(python3 --version 2>&1)"
echo "  workdir : $WORK"
echo

SOURCE_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || true)"
RESOLVED_REF=""
if [ -n "$SOURCE_ROOT" ]; then
  RESOLVED_REF="$(git -C "$SOURCE_ROOT" rev-parse --verify "${REF}^{commit}" 2>/dev/null || true)"
fi

if [ -n "$RESOLVED_REF" ]; then
  # Clone committed objects only. --no-local avoids shared-object shortcuts while
  # preserving otherwise hidden PR merge commits available in the tested checkout.
  git clone --quiet --no-local --no-checkout "$SOURCE_ROOT" "$WORK/repo" || {
    echo "FATAL: clean clone failed for local commit '$RESOLVED_REF'"; exit 2; }
  cd "$WORK/repo" || exit 2
  git checkout --quiet --detach "$RESOLVED_REF" || {
    echo "FATAL: checkout failed for local commit '$RESOLVED_REF'"; exit 2; }
else
  git clone --quiet --depth 50 --branch "$REF" "$REMOTE" "$WORK/repo" || {
    echo "FATAL: clone failed for remote ref '$REF'"; exit 2; }
  cd "$WORK/repo" || exit 2
fi
echo "  commit  : $(git rev-parse --short HEAD)"
echo

WF=".github/workflows/epistemic-flexibility.yml"
[ -f "$WF" ] || { echo "FATAL: workflow not found: $WF"; exit 2; }

# Steps are extracted from the workflow, never hardcoded here.
mapfile -t STEPS < <(grep -oE '^        run: python [^ ]+\.py.*$' "$WF" | sed 's/^        run: //')
echo "extracted ${#STEPS[@]} python steps from $WF"
echo

export PYTHONIOENCODING=utf-8

# The workflow invokes `python`, which GitHub's setup-python action provides.
# A bare Ubuntu image ships only `python3`. Without this shim every step fails
# 127 with an identical error — 31 failures, one cause, none of them real. A
# uniform result across unrelated subjects is a mechanism artifact, not a
# finding, and this harness should never be able to report it as one.
SHIM="$WORK/shim"; mkdir -p "$SHIM"
if ! command -v python >/dev/null 2>&1; then
  command -v python3 >/dev/null 2>&1 || { echo "FATAL: neither python nor python3"; exit 2; }
  ln -sf "$(command -v python3)" "$SHIM/python"
  export PATH="$SHIM:$PATH"
  echo "  shim    : python -> $(command -v python3)"
  echo
fi

pass=0; fail=0; usage=0
declare -a FAILED=()
for step in "${STEPS[@]}"; do
  out="$(eval "$step" 2>&1)"; rc=$?
  short="${step#python }"
  if [ "$rc" -eq 0 ]; then
    pass=$((pass+1)); printf '  PASS  %s\n' "$short"
  elif [ "$rc" -eq 2 ] && printf '%s' "$out" | grep -qi 'usage:'; then
    # argparse usage error: CI supplies arguments this harness does not.
    usage=$((usage+1)); printf '  SKIP  %s  (needs args)\n' "$short"
  else
    fail=$((fail+1)); FAILED+=("$short")
    printf '  FAIL(%s)  %s\n' "$rc" "$short"
    printf '%s\n' "$out" | tail -4 | sed 's/^/          /'
  fi
done

echo
echo "clean-room CI: $pass passed, $fail failed, $usage skipped (need args)"
if [ "$fail" -gt 0 ]; then
  echo "failing:"; printf '  %s\n' "${FAILED[@]}"
  exit 1
fi
exit 0
