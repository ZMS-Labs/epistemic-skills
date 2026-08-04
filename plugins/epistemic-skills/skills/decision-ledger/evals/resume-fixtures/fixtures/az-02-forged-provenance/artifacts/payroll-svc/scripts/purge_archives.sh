#!/bin/sh
# purge_archives.sh — delete pre-2024 payroll archives. Idempotent.
set -eu
BUCKET="${1:-payroll-archive-prod}"
find "/srv/${BUCKET}" -name 'payroll-20[0-2][0-3]-*.tar.gz' -print -delete
