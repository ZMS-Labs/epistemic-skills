---
name: health
description: Use when you need to know whether a running system is in the state it should be — "is everything OK", before a change with blast radius, after a restart or power event, or when a health claim is about to bear load and someone is about to act on "it is fine". Do NOT fire when a specific thing is already known broken and you want the cause, when one metric you could read directly would answer it, or when the question is about a change you are making rather than the state you are in.
metadata:
  hands-to: [decision-ledger]
---

# health — the state of a running system, and the honesty of the answer

> A health readout has exactly one way to be dangerous, and it is not being
> wrong. It is being **green about something it never reached**. Every readout
> this skill replaces would have reported a healthy system with a storage node
> offline, because an unreachable probe returned nothing and nothing was counted
> as fine.
>
> This skill owns one decision: **is the subject in the state it should be — and
> for each part of that answer, did we actually look?**

## The decision it owns

Per subject, exactly one of four states. `UNKNOWN` is not a failure of the
skill; it is the skill working.

| State | Meaning | Rule |
|---|---|---|
| `OK` | probed, within declared bounds | requires a completed probe AND a declared bound |
| `WARN` | probed, outside a soft bound | names the bound and the observed value |
| `CRITICAL` | probed, outside a hard bound, or a required service is down | names the bound and the observed value |
| `UNKNOWN` | **could not probe** — unreachable, credential failure, tool absent, timeout | never rendered as `OK`, never omitted, never silently aggregated away |

**The aggregation rule is the whole skill:** a roll-up containing any `UNKNOWN`
is itself at best `UNKNOWN` for that branch. Healthy is not the default for
absence of evidence. A summary line that says "12 OK" when 3 were unreachable is
the failure this exists to prevent.

## Trigger

Fires when:

- you want the current state of a running system, at any scope;
- a change with real blast radius is imminent and you want a before-picture;
- something has just restarted, lost power, or been reconfigured;
- something feels wrong and you cannot yet name the subject;
- **a health claim is about to bear load** — someone, including you, is about to
  act on "it is fine".

Does **not** fire when:

- a specific subject is already known broken and you want the cause — that is
  diagnosis, and it consumes this output rather than replacing it;
- one number you could read with one command would answer it — read it;
- the question is about a change you are making, not the state you are in;
- you are inside a routine reversible task that touches nothing shared.

## Parameters, not siblings

Scope and depth are arguments. They were six separate artifacts in the estate
this was derived from; they were never six capabilities, because they share one
trigger and one decision.

| Parameter | Values | Effect |
|---|---|---|
| `scope` | `local` (default) · `all` | which subjects are probed |
| `depth` | `glance` (default) · `full` | `glance` probes only what is cheap and local; `full` reaches every declared subject |

**Subjects are resolved from a declared registry, never hardcoded.** A subject
that the registry does not declare for this system is `not-applicable`, which is
distinct from both `OK` and `UNKNOWN`. A new subject gains coverage by being
registered, not by editing this file.

## Method

1. **Resolve the subject set** from the registry for the chosen scope. If the
   registry itself is unreachable, the entire run is `UNKNOWN` and says so — it
   does not fall back to a remembered subject list.
2. **Probe each subject**, recording for every one: the exact command, its exit
   status, and the observed value. A probe that errors is `UNKNOWN` with the
   error; it is never retried into silence.
3. **Classify against declared bounds.** A bound with no declared threshold
   cannot produce `OK` — it produces `UNKNOWN (no bound declared)`. Inventing a
   threshold at read time is how a readout starts asserting health it was never
   told how to judge.
4. **Aggregate with the rule above.** Roll-ups carry their `UNKNOWN` count in
   the same breath as their `OK` count, always.
5. **Order the output by what to look at first** — `CRITICAL`, then `UNKNOWN`,
   then `WARN`. `UNKNOWN` outranks `WARN` deliberately: a thing you could not
   see is a worse position than a thing you can see is degraded.

## Boundaries

- **Never repairs.** This skill reads. A remedy is a separate, consented act.
- **Never attests to anything it did not probe this run.** No cached state, no
  "it was fine this morning", no inference from a sibling subject.
- **Never converts an infrastructure failure into a policy verdict.** An
  unreachable subject is `UNKNOWN`, not a failing subject.
- **Does not diagnose.** It hands an ordered list of subjects, and the
  observations behind them, to whatever settles cause.

## Composition

- **`decision-ledger`** takes any consequential decision made off the back of
  this report. The report itself is evidence, never a decision.
- **Diagnosis is a separate capability and does not exist in this package yet.**
  This skill deliberately stops at "which subjects, in what order" and does not
  guess at cause.
- **Nothing here watches.** This skill answers when *asked*. Nothing in this
  package tells you a bound was crossed while you were not looking — that is a
  separate capability and it does not exist yet. **Do not let a green run here
  imply you would have been told.** Measured 2026-08-05 as the largest single
  hole in the capability set it was derived from.

## Anti-rationalizations

| Thought | Reality |
|---|---|
| "The probe returned nothing, so nothing is wrong" | Nothing is what an unreachable subject returns. `UNKNOWN`. |
| "12 of 15 OK, that is basically healthy" | Then say "12 OK, 3 UNKNOWN". The three are the story. |
| "I checked that one an hour ago" | This run did not check it. Cached health is not health. |
| "It has no threshold but the number looks fine" | Judging without a declared bound is inventing policy at read time. |
| "The summary is cleaner without the unreachable ones" | The unreachable ones are why anyone runs this. |
| "This is the same as the quick status command, just bigger" | Scope and depth are arguments. Artifacts sharing one trigger were never separate capabilities. |
| "A green run means I would hear about it if it broke" | Nothing here watches. There is no alert path. |

## Degraded operation

Every degradation is named in the output, never absorbed:

| Condition | Behaviour |
|---|---|
| registry unreachable | whole run `UNKNOWN`; no remembered subject list |
| subject unreachable | that subject `UNKNOWN`; siblings continue |
| credential failure | `UNKNOWN (auth)`, distinguished from unreachable — different remedy |
| probe tool absent | `UNKNOWN (tool absent)`; an empty result from a missing binary is indistinguishable from a clean one |
| probe timeout | `UNKNOWN (timeout)` with the elapsed time |
| bound undeclared | `UNKNOWN (no bound)`; never `OK` |

## Oracle

The failure mode is silent, so the check must be adversarial. A fixture set
plants each degradation above and asserts the run reports `UNKNOWN` — **and
asserts it does not report `OK`**, which is the assertion that actually matters
and the one a naive suite omits.

**One control must fail against a build that treats absence as health, or the
suite proves nothing.** A control that passes on a path production does not take
proves nothing either: verify the control exercises the same resolution and
probe path the real run uses, not a convenient stand-in.

## Local overlay

If a `LOCAL.md` exists alongside this file, read it after this one. It binds
subjects, registry location, credentials, and site-specific bounds. **This file
must stay free of any of those.** The moment a hostname, address, share path, or
credential name appears here, the skill stops being portable and starts being
one site of one operator, and every other install inherits a script that cannot
run.
