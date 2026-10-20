# Issue #162 validation-code archive

This WIP preservation snapshot stores the source of local diagnostic, regression,
fixture-adaptation and receipt/replay tools. It preserves code against local
drive loss; it does not make these tools a supported product interface.

The sealed candidate's 13 source/test/evidence files remain byte-identical.
Historical evidence documents describe their state before this WIP commit.
This preservation is neither a release nor approval to integrate the safeguard.
Native compatible-platform and hosted integration validation remain outstanding.

These tools were written for the local investigation layout and some depend on
local evidence files or sibling checkout directories. Some scripts mutate test
fixtures, produce records, or install exact pinned test packages. They are kept
for auditability; they are not automatically run. No completed tests were rerun
for preservation. One filesystem-inventory script has its hardcoded private
paths replaced with portable cwd/temp-directory expressions; that archival copy
was not rerun or newly qualified. The manifest records original/stored hashes.

The archive includes exact prior/sealed source patches in deterministic gzip
wrappers; decompress before reconstruction. Context whitespace is preserved. Apply
the separately recorded prior test patch before the validated safeguard delta;
the combined candidate patch applies directly to the recorded release base.
Do not apply both reconstruction routes to the same checkout. Local logs, raw
filesystem inventories, virtual environments and personal records are excluded.
