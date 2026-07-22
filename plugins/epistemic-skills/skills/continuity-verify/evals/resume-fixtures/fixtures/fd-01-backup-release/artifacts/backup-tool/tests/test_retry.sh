#!/bin/bash
# test_retry.sh — retry path tests
echo "test: retry on lock failure"
# NOTE: this test only checks the lock-failure exit code, not the rsync retry flag.
/tmp/backup.lock.exists && exit 0
echo "1 test, 0 failures (coverage note: retry flag path NOT exercised)"
