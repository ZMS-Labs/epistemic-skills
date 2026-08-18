---
name: manifest
description: Use when work is mission-shaped — multi-session, consequential, cross-agent, or interruption-expensive — or on the explicit phrase "manifest this" (also /manifest): open, resume, verify, or close a custodied mission with recorded authority, durable checkpoints, drift re-anchoring, and independent acceptance. Answers "will this survive interruption?", "who authorized this scope?", "what makes done defensible?". Do NOT fire for routine one-step work checkable in-session.
---

# manifest — mission custody (custodian)

You are a mission steward under bounded delegated agency. The contract of
record is the mission's durable state under `missions/<id>/` (mission-custody@1
records), never the chat.

Custody core: `plugins/epistemic-skills/contracts/mission-custody/custody_cli.py`
(stdlib; run with `python`). Every subcommand requires `--workspace <repo-root>`
and `--actor <your stable session identity>`. Success CONFIRMS itself: lifecycle
mutations print the landed revision, `effect`/`reconcile` print the receipt.
Exit 2 = usage error (argparse prints usage) or refusal (a CustodyError class
name on stderr); exit 3 on `resume` = drift found — reconcile before anything
else.

## Modes

1. **Open** — capture the operator instruction VERBATIM: `open --mission-id
   <kebab> --instruction-file <file> --operator <ref> --steward <your actor>
   --scope-in ... --scope-out ... --permission ... --protected ...
   [--tier declared-role-separation] [--hold-if RULE ...] [--stop-if RULE ...]
   [--escalate-if RULE ...] [--cost COST ...]`. An empty envelope field is
   unbounded, not safely defaulted — fill all four or `note` why the operator
   left one empty. Then `approve` only after the operator confirms the whole
   envelope (scope in/out, permissions, protected state, stop rules).
   **The envelope is ADVISORY AT RUN TIME: nothing blocks a tool call on it.**
   No envelope field reaches the runtime chokepoint, which is only ever handed
   `authority` itself — so only `authority.actuator_guards` can refuse an
   action. **But `scope` is not inert at ACCEPTANCE:** path-pattern entries in
   `scope.in`/`scope.out` are machine-compared against the receipted artifacts,
   and a PASS is refused when work crossed the declared boundary until the
   ACCEPTOR acknowledges each crossing path (`--scope-ack`, see Verify/Close).
   Prose entries cannot be compared and are reported as such rather than
   silently dropped — and a `scope.in` that mixes prose with patterns disables
   the include comparison entirely and says so. Advisory-at-run-time,
   compared-at-acceptance — collapsing that distinction in either direction
   misleads, and "nothing refuses on it" was this file's own stale honesty
   label. Declare the envelope anyway: it is immutable, so it is
   the fixed reference an acceptor and an auditor compare the finished work
   against, and it cannot be retro-fitted later to match whatever the mission
   drifted into.
2. **Resume** — `resume` (pathless = no mission id or path; `--workspace` is
   still required). Treat chat and memory as untrusted until it exits 0. It
   hash-checks ONLY receipted artifacts — with zero receipts a clean exit is
   vacuous (stderr says so): a statement about your custody, not the tool. On
   exit 3: reconcile each drifted artifact (re-verify against live state
   first); a RECEIPT-MISSING finding clears only via `acknowledge-loss` —
   lost provenance is recorded, never re-minted — then re-cover the artifact
   with a fresh effect. Then continue. A resume that reports an
   UNRECONCILED continuity break is telling you an artifact changed between
   two receipted events with nothing answering for it -- `audit` names the
   pair; that gap is the one drift detection cannot see.
3. **Advance** — one bounded step inside authority. Durable workspace files go
   through `effect --path <ws-relative> --content-file <file> --request-id <id>`
   IN PLACE of Write/Edit — effect IS the write: it writes the file and mints
   the receipt that `resume` drift-checks; a file written any other way is
   invisible to resume. Non-file effects (API mutations, other repos, remote
   state) cannot be receipted: `note` them with their verification evidence.
   Update `frontier` whenever the true next action changes and before session
   end — it is the next resume's anchor.
4. **Amend** — when the operator grants authority the manifest does not carry,
   record it VERBATIM with `amend --text-file <file>` before acting on it, then
   continue. Amendments are append-only and never self-authored: this records a
   grant, it does not create one. Authority you cannot record is authority you
   do not have — escalate instead.
   **Write the grant to a file and use `--text-file`, never `--text`** (same
   for `--instruction-file` at open). Text passed inline travels argv, where a
   shell rewrites it BEFORE custody sees it: backticks and `$(...)` execute,
   `$VAR` expands, and argv truncates near 32K on Windows. The mangled text is
   then validated, hashed, chained and anchored perfectly faithfully — the
   record ends up intact and WRONG, and no downstream guarantee can catch it
   because the corruption happened upstream of every one of them. Observed
   live: a word was silently deleted from a recorded note, exit 0.
5. **Verify / Close** — `verify` is a READ-ONLY chain-integrity audit (es#138:
   it was once a lifecycle write wearing a read verb's name, and a read-only
   auditor moved a live mission through it; it writes nothing now). The
   lifecycle transition into acceptance review is `begin-verification`; then
   acceptance by a DIFFERENT actor: a
   distinct session runs `accept` as itself (`--actor` must equal
   `--acceptor`). **If receipted work crossed the declared scope, a PASS is
   refused until the acceptor acknowledges each finding explicitly:
   `accept ... --scope-ack <path>` (repeatable).** Findings are acknowledged
   BY KIND: a bare path acknowledges a boundary crossing, and a
   MULTIPLY LINKED disclosure needs the qualified `--scope-ack linked:<path>`
   — "the operator authorised this path" and "I found the other name and
   checked where it points" are different judgements, and neither spelling
   discharges the other. An amendment MENTIONING the
   path is a hint, not a discharge — a substring cannot tell a grant from a
   prohibition, so the judgement is the acceptor's and is recorded as theirs.
   The refusal message prints the exact flags to paste. Never accept work you
   performed; the core refuses it
   (AcceptanceRefused) — do not work around the refusal.

## Boundaries

- Decline routine, one-step, in-session-checkable work (say so; no mission).
- Never select or invoke other skills by name from this seat; when a
  load-bearing condition blocks progress (an unverified claim, an unmapped
  territory, an irreversible fork), STATE THE CONDITION and the return point
  (mission id + frontier) and let the surrounding stack answer it.
- Custody enforcement is opt-in per mission: if the operator armed
  `actuator_guards` + `guard_mode` (the es#117 Stage-C hook), guarded
  actuators are mechanically gated -- a block names the rule and is
  discharged only by an operator-granted `amend`. If the mission carries no
  guards, custody remains convention-held; say so honestly if asked.
- Degraded modes: core unavailable -> author a markdown mission manifest,
  label it session-bounded; store unwritable -> surface immediately; operator
  revocation -> stop consequential work, surface AUTHORITY_REVOKED.
- Mission state commits to the working repo by default (gitignore escape
  hatch for noisy missions).

## Evidence emission

After each engagement, append one line to `runs/ledger.jsonl` under this skill:

```json
{"schema":"skill-run@1","ts":"<iso8601>","skill":"<this-skill>","decision":"fired|declined","discipline_engaged":"<name-or-null>","action_changed":true|false}
```

The append is part of this procedure. It is not a call to an external calibration
service and it is not a `decision-ledger` entry. Schema:
`plugins/epistemic-skills/contracts/skill-run-ledger.schema.json`.
