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
# CLEANROOM_TMPDIR: on Windows hosts the default temp dir lives inside the
# user profile, which test_live_runner's sensitive-path guard deliberately
# refuses (kimi ruling S10 — the guard working, not a defect). Set this to
# any non-profile scratch path there; unset elsewhere.
WORK="$(mktemp -d ${CLEANROOM_TMPDIR:+-p "$CLEANROOM_TMPDIR"})"
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

# Scope disclosure (R9): this harness replicates the python steps of ONE
# workflow. The other workflows are separate CI surfaces and are NOT
# replicated here — never read this script's green as covering them.
OTHER_WFS="$(ls .github/workflows/*.yml 2>/dev/null | grep -v "$WF" | tr '\n' ' ')"
[ -n "$OTHER_WFS" ] && { echo "out of scope (separate workflows, not replicated): $OTHER_WFS"; echo; }

# Steps are extracted from the workflow, never hardcoded here. Both forms are
# covered: single-line `run: python ...` steps AND python lines inside
# `run: |` blocks (the original grep saw only the single-line form and
# silently dropped every block line — including the public-content gate).
# Each row is "<flag>\t<command>"; flag is:
#   -      plain, executed;
#   ctx    references CI event context ($RUNNER_TEMP/$GITHUB_*/${{ }}/env
#          wired by the workflow) — named SKIP, cannot run standalone;
#   pyyaml its block pip-installs PyYAML — executed only if yaml imports.
mapfile -t ROWS < <(python3 - "$WF" <<'PYEOF'
import re, sys
lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
rows = []
i = 0
while i < len(lines):
    line = lines[i]
    single = re.match(r"^(\s*)run:\s+(python3? \S+\.py.*)$", line)
    block = re.match(r"^(\s*)run:\s*[|>]-?\s*$", line)
    if single:
        rows.append(("-", single.group(2).strip()))
    elif block:
        indent = len(block.group(1))
        body = []
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= indent:
                break
            body.append(nxt.strip())
            j += 1
        has_pyyaml = any(b.startswith("pip install") and "yaml" in b for b in body)
        for b in body:
            if re.match(r"^python3? \S+\.py", b):
                if re.search(r"\$RUNNER_TEMP|\$GITHUB_|\$\{\{|\$BASE_SHA", b):
                    rows.append(("ctx", b))
                elif has_pyyaml:
                    rows.append(("pyyaml", b))
                else:
                    rows.append(("-", b))
        i = j - 1
    i += 1
for flag, cmd in rows:
    print(f"{flag}\t{cmd}")
PYEOF
)

# Completeness assertion (R9): an INDEPENDENT broad net counts every
# python-invoking line in the workflow; extraction must account for all of
# them or this harness fails loudly instead of silently under-replicating.
BROAD_COUNT="$(grep -cE '^[[:space:]]*(run: )?python3? [^ ]*\.py' "$WF")"
if [ "${#ROWS[@]}" -ne "$BROAD_COUNT" ]; then
  echo "FATAL: extraction divergence — workflow has $BROAD_COUNT python lines, extracted ${#ROWS[@]}"
  echo "broad net:"
  grep -nE '^[[:space:]]*(run: )?python3? [^ ]*\.py' "$WF" | sed 's/^/  /'
  echo "extracted:"
  printf '  %s\n' "${ROWS[@]}"
  exit 2
fi
echo "extracted ${#ROWS[@]} python steps from $WF (completeness: ${#ROWS[@]}/$BROAD_COUNT lines accounted for)"
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

pass=0; fail=0; usage=0; ctx=0; dep=0
declare -a FAILED=()
for row in "${ROWS[@]}"; do
  flag="${row%%$'\t'*}"; step="${row#*$'\t'}"
  short="${step#python }"
  if [ "$flag" = "ctx" ]; then
    # Named exclusion, never a silent drop: the step reads CI event context
    # (merge-base SHA, runner temp dir) that does not exist standalone.
    ctx=$((ctx+1)); printf '  SKIP  %s  (ci-context: needs GitHub event env)\n' "$short"
    continue
  fi
  if [ "$flag" = "pyyaml" ] && ! python -c 'import yaml' >/dev/null 2>&1; then
    # CI pip-installs PyYAML for this block; installing on the operator's
    # machine is a side effect this harness refuses. Named exclusion.
    dep=$((dep+1)); printf '  SKIP  %s  (missing dep: PyYAML; CI installs it)\n' "$short"
    continue
  fi
  out="$(eval "$step" 2>&1)"; rc=$?
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
total=${#ROWS[@]}
echo "clean-room CI: replicated $pass of $total workflow python steps"
echo "  pass=$pass fail=$fail need-args=$usage ci-context=$ctx missing-dep=$dep"
if [ "$((pass + fail + usage + ctx + dep))" -ne "$total" ]; then
  echo "FATAL: step accounting does not sum to $total — harness defect"; exit 2
fi
if [ "$fail" -gt 0 ]; then
  echo "failing:"; printf '  %s\n' "${FAILED[@]}"
  exit 1
fi
exit 0
