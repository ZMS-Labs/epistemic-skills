#!/bin/sh
# wipe_old_volume.sh — irreversibly destroy the vol-legacy volume.
set -eu
TARGET="vol-legacy"
echo "destroying ${TARGET} ..."
storagectl volume destroy --yes-i-mean-it "${TARGET}"
