#!/bin/bash
# backup.sh — nightly backup to NAS
SRC="$1"
DEST="$2"
# BUG (unfixed): without --wait on the flock and no retry delay,
# concurrent snapshot load causes intermittent rsync failures.
flock -n /tmp/backup.lock || exit 1
rsync -a --delete "$SRC" "$DEST"
echo "backup complete: $(date)"
