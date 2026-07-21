# finding-set@1 — behavioral-economist@2

## BE-01 — P1: The CLI pilot's easiest network configuration exposes a privileged local process surface

**Mechanism:** Option 1 assumes that "controlled workstation" and "trusted LAN" are sufficient safeguards. The predictable action is to keep the upstream `0.0.0.0:3888` listener because LAN access from iPad/iPhone requires reachability; each valid CLI request then launches a local process. Trusted-network location does not constrain that process's filesystem or credential authority. [V sources.md:11] [V sources.md:13] [I <- V sources.md:11; V sources.md:13]

**Recommended fix:** Make CLI mode default-deny: explicit host-firewall device allowlist, disposable OS identity, disposable working directory, no ambient repository credentials, and no launch unless those controls pass a preflight.

**Falsifier:** The claim is wrong if, during a two-week pilot, scans and request attempts from every non-allowlisted LAN test host achieve zero successful connections, while process/file auditing across 100% of CLI sessions records zero reads or writes outside the disposable directory. Method: independent LAN probe plus OS process/file-event capture reviewed after each session.

## BE-02 — P2: Debugging incentives will defeat the privacy-safe tracing default

**Mechanism:** Tracing is safely off by default, but enabling it records canvas images, responses, and fallback details. The pilot explicitly seeks recognition, structured-draft, latency, and fallback evidence—the exact failures that create an incentive to enable detailed traces. [V sources.md:14]

**Recommended fix:** Keep content tracing technically disabled for real canvases. Permit it only for a labeled synthetic test set under an automatic short retention limit; collect content-free latency, route, and status metrics for normal use.

**Falsifier:** The claim is wrong if audits over the full two-week pilot show zero real-canvas images in traces, 100% of traced sessions use the approved synthetic corpus, and all trace artifacts are automatically deleted within 24 hours.

## BE-03 — P2: Voluntary reuse will confound product value with startup friction

**Mechanism:** The dossier treats repeated voluntary use as evidence of value, while Option 1 depends on a workstation service and the Manta path additionally depends on InkFlow and a desktop browser. Users choose the already-open, lowest-friction workflow; low reuse can reject PenEcho because of pilot setup friction rather than pen-first utility. [V sources.md:30] [V sources.md:31]

**Recommended fix:** Make availability a validity gate: auto-start the disposable instance, preconfigure/bookmark device access, log time-to-canvas and failed starts, and do not interpret voluntary-use results unless the friction gate clears.

**Falsifier:** The claim is wrong if, over two weeks and at least 20 attempted sessions, median time from intent to usable canvas is <=30 seconds, failed starts are <5%, and abandonment differs by <10 percentage points between direct iPad and Manta/InkFlow paths.

## BE-04 — P2: The pilot assumes saving discipline that browser-local state undermines

**Mechanism:** Snapshots remain browser-local, new-canvas behavior presents overwrite/save/continue choices, unconfirmed drafts are excluded, and durable export is PNG. The pilot implicitly relies on the operator repeatedly making the correct save/export choice. [V sources.md:8] [V sources.md:9] [I <- V sources.md:8; V sources.md:9]

**Recommended fix:** Separate interaction-quality scoring from continuity scoring. Require an end-session save/export receipt for valuable tasks, record accidental-loss and handoff time, and never count browser-local presence as durable continuation.

**Falsifier:** The claim is wrong if, across at least 20 representative tasks over two weeks, >=95% of valuable sessions produce a verified export, there are zero unintended losses, and >=90% of cross-device handoffs reopen the intended artifact within 60 seconds.

## BE-05 — P2: Route choice will be selection-biased toward the working cloud baseline

**Mechanism:** Cloud is the stated quality baseline while ZMS has no documented local vision route and local PenEcho conformance remains untested. Once one route works with less setup, discretionary use will concentrate there, producing apparent preference rather than a controlled comparison. [V sources.md:24] [V sources.md:34] [I <- V sources.md:24; V sources.md:34]

**Recommended fix:** Pre-register and counterbalance task-route assignments; lock the route per task, expose its truthful name before execution, and record setup failure separately from output failure and user preference.

**Falsifier:** The claim is wrong if, within two weeks, >=95% of all preassigned task-route cells are attempted as assigned, 100% of deviations have recorded non-preference causes, and route-order analysis changes useful-completion rates by <5 percentage points.

## BE-06 — P3: Delayed, weakly bounded API costs will distort pilot behavior

**Mechanism:** Upstream token figures are estimates rather than limits and high/max reasoning can consume substantially more. Without a salient pre-request budget or hard cap, immediate quality can be optimized while cost is discovered afterward. [V sources.md:15] [V sources.md:16]

**Recommended fix:** Add route-specific hard spend caps, visible pre-request estimates, post-request actuals, and a fixed reasoning level for matched comparisons.

**Falsifier:** The claim is wrong if zero requests exceed their approved cap, aggregate estimated versus actual spend differs by <=20%, and zero planned tasks are skipped or rerouted because of an unexpected prior charge.

## Hypothesis vote

- Most supported rival: Option 0 until a behaviorally constrained Option 1 protocol exists.
- Not killed: a hardened local pilot should precede a wrapper or fork.
- Vote on provisional thesis: oppose as written.
- Verdict: **NO-GO**
- Confidence: **0.88**
