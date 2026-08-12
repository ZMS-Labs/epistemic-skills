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
   <kebab> --instruction <verbatim> --operator <ref> --steward <your actor>
   --scope-in ... --scope-out ... --permission ... --protected ...
   [--tier declared-role-separation] [--hold-if RULE ...] [--stop-if RULE ...]
   [--escalate-if RULE ...] [--cost COST ...]`. An empty authority field is
   unbounded, not safely defaulted — fill all four envelope flags or `note` why
   the operator left one empty. Then `approve` only after the operator confirms
   the whole envelope (scope in/out, permissions, protected state, stop rules).
2. **Resume** — `resume` (pathless = no mission id or path; `--workspace` is
   still required). Treat chat and memory as untrusted until it exits 0. It
   hash-checks ONLY receipted artifacts — with zero receipts a clean exit is
   vacuous (stderr says so): a statement about your custody, not the tool. On
   exit 3: reconcile each drifted artifact (re-verify against live state
   first); a RECEIPT-MISSING finding clears only via `acknowledge-loss` —
   lost provenance is recorded, never re-minted — then re-cover the artifact
   with a fresh effect. Then continue.
3. **Advance** — one bounded step inside authority. Durable workspace files go
   through `effect --path <ws-relative> --content-file <file> --request-id <id>`
   IN PLACE of Write/Edit — effect IS the write: it writes the file and mints
   the receipt that `resume` drift-checks; a file written any other way is
   invisible to resume. Non-file effects (API mutations, other repos, remote
   state) cannot be receipted: `note` them with their verification evidence.
   Update `frontier` whenever the true next action changes and before session
   end — it is the next resume's anchor.
4. **Verify / Close** — `verify`, then acceptance by a DIFFERENT actor: a
   distinct session runs `accept` as itself (`--actor` must equal
   `--acceptor`). Never accept work you performed; the core refuses it
   (AcceptanceRefused) — do not work around the refusal.

## Boundaries

- Decline routine, one-step, in-session-checkable work (say so; no mission).
- Never select or invoke other skills by name from this seat; when a
  load-bearing condition blocks progress (an unverified claim, an unmapped
  territory, an irreversible fork), STATE THE CONDITION and the return point
  (mission id + frontier) and let the surrounding stack answer it.
- Custody here is convention-held, not mechanically enforced — the tracer
  retro (2026-08-11) ruled Stage C teeth IN, tracked as epistemic-skills#117;
  until that PreToolUse hook ships, honestly label enforcement as
  convention-held if asked.
- Degraded modes: core unavailable -> author a markdown mission manifest,
  label it session-bounded; store unwritable -> surface immediately; operator
  revocation -> stop consequential work, surface AUTHORITY_REVOKED.
- Mission state commits to the working repo by default (gitignore escape
  hatch for noisy missions).
