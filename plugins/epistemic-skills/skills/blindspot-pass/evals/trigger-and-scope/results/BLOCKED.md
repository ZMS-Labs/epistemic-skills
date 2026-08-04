# Behavioral epoch status

No live behavioral epoch has been run against these fixtures. The committed
battery verifies scorer polarity and fixture schema only: the balanced
example passes, both parodies fail for their named polarity, and the harness
exits 0. None of that is evidence that a live agent under this skill fires
on the positive triggers, stays silent on the hard negatives, stops at
understanding instead of implementing a surfaced fix, or reports an embedded
instruction as a Landmines finding instead of following it.

A live epoch must pin model, harness, installed skill revision, and prompt
set; present each fixture scenario in isolation, withholding the scorer, the
other fixtures, and this results directory; retain the raw responses
unedited; and score them with `score.py` as committed. Failures are
committed as results, not retried away — recording BLOCKED rather than
claiming a pass is the house norm.
