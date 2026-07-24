schema: outsource-relay@1
work_id: routine-proportionality-full-implementation
based_on_commit: a4f2210fe3e955b77bb2593fa3c6c991304a4142
status: PARTIAL
summary: Deterministic proportionality, Gauntlet, UAT, ledger, formal-rigor Phase B, and held 3.0.0 release preparation are implemented and green; production formal-rigor v2 is blocked before its required live RED.
work_product: Draft PR #48 https://github.com/ZMS-Labs/epistemic-skills/pull/48 on branch codex/v3-rigor-gauntlet; commits 3574687, 7700a3c, 4dd2a83, 4e1945e, 03f0768, 11233c3, a2c794c; principal evidence in VERIFICATION.md, formal-rigor-v2-fixtures/, proportionality/blinded/, UAT triage, Decision Ledger proportionality, and Gauntlet selector/replay files.
evidence: Full local deterministic suite PASS; proportionality control 10/10 routine, 4/4 material, 4/4 high-risk, median 25 words; full-ceremony and always-routine parodies fail; UAT and ledger over/under parodies fail; 20 changed Python files compile, 73 changed JSON files parse, 60 changed Markdown relative-link checks pass; PR #48 stdlib run 30068667692, DCO run 30068665696, and CodeQL run 30068665105 pass.
requirements: OUT-001..OUT-006 and OUT-008..OUT-016 satisfied; OUT-007 open because its required live RED cannot be captured in this execution context.
decisions_and_assumptions: First formal immutable release is 3.0.0 and remains HOLD; registry_version 3.0.0 is a Gauntlet contract version, not release publication; no isolated live-model capability was assumed.
blockers_or_questions: OUT-007 requires a qualifying isolated neutral/current-v1 formal-rigor invocation to capture RED before production edits. Live proportionality arms require the pinned fresh-context repository-aware harness. No operator question is open.
recommended_next_action: Obtain the isolated invocation capability and resume OUT-007 from the committed formal-rigor BLOCKED protocol without bypassing RED ordering.
