schema: outsource-relay@1
work_id: epistemic-skills-suite-stress-test
based_on_commit: 04f16380ac3588bba299068184eb7078e478892b
status: BLOCKED
summary: Target capability preflight failed; no execution prompt was emitted and no outsourced work began.
work_product: NONE
evidence: The supplied packet explicitly states that a writable checkout, test shell, authenticated GitHub mutation, and isolated-role execution are required and unavailable for the selected target.
requirements: OUT-001 open; OUT-002 open; OUT-003 open; OUT-004 open; OUT-005 open; OUT-006 open; OUT-007 open; OUT-008 open; OUT-009 open; OUT-010 open; OUT-011 open; OUT-012 satisfied
decisions_and_assumptions: Decision: do not begin or simulate execution without the required target capabilities. Assumptions: NONE.
blockers_or_questions: No selected target currently satisfies the capability preflight.
recommended_next_action: Select and dispatch the handoff to a target with a writable repository checkout, runnable test shell, authenticated GitHub write access, and isolated-role execution.
