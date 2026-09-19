# Standalone systematic debugging

Use this procedure when no adequate applicable debugging provider is available.
It supplies a complete investigation and repair loop within the user's existing
scope. It is not an imitation claim that another package was used.

1. **Establish the actual failure.** Recover the request, error, environment,
   revision, reproduction steps and expected behavior. Reproduce safely if useful;
   record when it is intermittent or cannot be reproduced. Read relevant recent
   changes and trace the failing input through the responsible boundary.
2. **Reuse and distinguish evidence.** Check the applicability of an existing
   diagnosis. Keep observed facts separate from hypotheses and record which
   observations were inherited. Compare a working case when one is available;
   identify the relevant difference rather than copying a fix blindly.
3. **Choose a discriminating test.** State the explanation and what would come
   out differently under its strongest live alternative. Prefer a low-cost safe
   test that resolves that difference. A controlled repair can be the test when
   authorized and reversible; explain what it can and cannot establish.
4. **Observe and update.** Execute one informative test, inspect its result and
   retain contrary observations. If it fails, revise the hypothesis rather than
   layering speculative changes. After repeated failed attempts, reassess the
   failing boundary and assumptions. Seek a missing capability or user-owned
   decision only when needed; do not turn a fixed retry count into a universal
   approval ceremony.
5. **Repair when authorized.** Make the smallest change supported by the causal
   evidence. Preserve unrelated work. For diagnosis-only requests, return the
   causal finding without implementing a repair. A confirmed existing diagnosis
   may proceed directly to the already-authorized repair.
6. **Verify the requested outcome.** Exercise the original failing path with the
   same relevant inputs, then a proportionate regression/control. Observe the
   consuming system when the claim concerns an installed or deployed effect.
   Distinguish fixed source, passing test, deployed state and observed outcome.
7. **Return and continue.** State CAUSE, NARROWED, UNKNOWN or NOT-BROKEN with its
   basis, the repair and verification result, and any material unresolved limit.
   Acknowledge Triage's standalone procedure and complete the remaining authorized
   work. Record only evidence useful to the task or an existing evidence contract.
