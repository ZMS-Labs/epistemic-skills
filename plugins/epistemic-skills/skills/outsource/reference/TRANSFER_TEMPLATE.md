# Outsource transfer: `<work-id>`

| Field | Value |
|---|---|
| Schema | `outsource-transfer@1` |
| Mode | `transfer` |
| State | `DRAFT`, `READY`, `GAPS`, `ACCEPTED`, or `TRANSFERRED` |
| Work ID | `<work-id>` |
| Subject ref | `<stable identifier for the handed-over work>` |
| Subject revision | `<scope revision>` |
| Valid while | `subject-revision-unchanged` |
| Coverage limits | `<explicit inventory gaps or NONE>` |
| Baseline parent | `<40-character commit inspected before packet publication>` |
| Packet commit | `supplied by the immutable prompt URL after publication` |
| Prepared UTC | `<ISO-8601 timestamp>` |
| Supersedes | `<prior packet commit/path or NONE>` |
| Relay head | `<latest relay file or NONE>` |

## Transfer intent

State the operator's handover instruction verbatim, why this receiver is taking the work, and
the moment ownership passes: acceptance plus completed divestiture — never dispatch, and never
prompt delivery.

## Responsibility inventory

The full set being handed over, not one bounded outcome. Every row names the durable record it
was swept from; a responsibility with no record outside this packet must say so explicitly.

### In-flight work

| Work | Current state | Next action | Source |
|---|---|---|---|
| `<item>` | `<verified state>` | `<authorized next step>` | `<path/record>` |

### Standing obligations

| Obligation | Cadence or trigger | Current status | Source |
|---|---|---|---|
| `<obligation>` | `<when it fires>` | `<healthy / due / degraded>` | `<path/record>` |

### Authority held

| Authority | Provenance (grant and where recorded) | Transfers | Limits |
|---|---|---|---|
| `<capability or grant>` | `<operator instruction, mission record, or NONE>` | `yes / re-grant / origin-retained` | `<boundary>` |

### Open loops

| Loop | Owner today | Affected action | Source |
|---|---|---|---|
| `<unresolved question>` | `<who resolves it>` | `<what it blocks>` | `<ledger/path>` |

### Escalation paths

- `<who is told what, and when>`

## Inventory sweep

| Source swept | Responsibilities found | Recorded at |
|---|---|---|
| decision ledger | `<items or NONE>` | `<path>` |
| custodied missions | `<mission ids or NONE>` | `missions/<id>/` |
| task/TODO records | `<items or NONE>` | `<path>` |
| watchers and standing ops | `<items or NONE>` | `<path>` |

A source that could not be swept is a named gap, never silence.

## Repository and source

- **Repository:** `https://github.com/<owner>/<repo>`
- **Canonical remote:** `<remote name and redacted URL>`
- **Baseline parent:** `<commit inspected before packet publication>`
- **Packet commit:** Use the 40-character commit embedded in the immutable prompt URL. It is not
  duplicated inside this file because a Git commit cannot contain its own hash.
- **Base branch:** `<branch>`
- **Target access:** `<verified | operator-asserted | blocked>`
- **Source rule:** Read linked files at the packet commit from the prompt URL. Later branch state is out of scope
  unless a newer committed handoff supersedes this one.

## Context map

| Priority | Repository path | Load-bearing context | Read scope |
|---|---|---|---|
| Required | `<path>` | `<fact, contract, or interface this establishes>` | `<whole file or anchors>` |
| Supporting | `<path>` | `<why it may help>` | `<anchors>` |

Every required path must exist at the packet commit. Do not rely on local absolute paths,
attachments, or the originating chat.

## Current state

### Verified

- `<fact with repository path, commit, command result, or live-state anchor>`

### Incomplete or contradicted

- `<fact and impact>`

### Unknowns

- `<unknown>` — impact: `<impact>`; owner: `<who resolves it>`; closure: `<hold, escalate, or probe>`

### Next permitted action

- **Action and owner:** `<the receiver's first action after acceptance, or the origin's next preparatory step>`
- **Authority:** `<resolvable instruction/grant; prior answers retained unless superseded>`
- **Origin retains until divestiture completes:** `only the divestiture checklist below`

## Decisions already made

| Decision | Authority/source | Consequence | Revisit when |
|---|---|---|---|
| `<decision>` | `<operator or artifact>` | `<constraint it creates>` | `<condition>` |

## Custody acceptance contract

### ACCEPTED

The receiver returns the acceptance envelope with `custody_accepted: yes`, restating the
inventory — obligations, frontier, authority and its limits — and naming its first action. The
origin verifies the read-back covers every inventoried row, then records `ACCEPTED` with the
acceptance coordinate (the verbatim relay file and its commit). Acceptance is explicit
agreement by the receiving executor; dispatch proves neither acceptance nor execution.

### GAPS

The read-back names responsibilities the packet omitted, or declines custody with reasons. The
origin verifies each named gap against live state, amends the inventory, republishes at a new
commit, and sends exactly one corrective pointer turn. A named gap is evidence the sweep and the
read-back are working, not a failed transfer.

### WITHDRAWN

The operator cancels before acceptance. The origin resumes full ownership, records the
withdrawal in the packet, and divests nothing.

### Anti-proxy checks

- `<an acceptance restated in the origin's words only, not the receiver's read-back>`
- `<a custody_accepted yes that leaves authority provenance or open loops unacknowledged>`
- `<divestiture marked complete while any checklist row lacks its evidence>`

## Authority and boundaries

### Allowed

- `<actions the receiver may take without another approval>`

### Ask first

- `<destructive, publishing, spend, external-message, security, or scope-changing actions>`

### Forbidden

- `<actions outside the handed-over responsibility set>`

### Preserve

- `<unrelated work, interfaces, data, history, or invariants that must not be changed>`

After `TRANSFERRED`, these boundaries re-anchor to the receiver's own authority chain; the
packet's grants are recorded provenance, not standing authority over the receiver.

## Origin divestiture checklist

The transfer completes when every row carries evidence, not when acceptance lands.

- [ ] watchers and scheduled observers stopped or handed over — evidence: `<command result or handover record>`
- [ ] credentials and keys handed over or revoked — evidence: `<record; never the secret itself>`
- [ ] removed from review, approval, and notification loops — evidence: `<observation>`
- [ ] steward change recorded in affected missions and ledgers — evidence: `<record path>`
- [ ] origin residual obligations: `NONE`

## Acceptance response contract

Return only this envelope, with no conversational preamble:

```markdown
schema: outsource-acceptance@1
work_id: <work-id>
based_on_commit: <40-character commit or explicit NONE>
custody_accepted: yes | no
understanding_readback: <the obligations, frontier, and authority now owned, restated>
authority_acknowledged: <grants accepted with provenance, and any needing operator re-grant, or NONE>
open_loops: <ids confirmed, amended, or newly surfaced, or NONE>
first_action: <the next action the receiver will take and why>
gaps_found: <responsibilities the packet omitted, or NONE>
```

## Context-erasure audit

- [ ] No originating-chat knowledge is required to accept custody.
- [ ] Repository, immutable packet commit from the prompt URL, and target access are explicit.
- [ ] Every required path exists at the packet commit.
- [ ] The receiver can determine the full responsibility set, each item's source, and the
      authority that transfers.
- [ ] Every authority grant carries provenance; grants that cannot transfer are named for
      operator re-grant.
- [ ] Divestiture rows are complete and individually evidenced.
- [ ] The acceptance envelope shape is unambiguous.
- [ ] Packet and canonical outbound prompt template are committed and pushed before state becomes `READY`.
- [ ] The emitted prompt substitutes the receipt's 40-character packet commit for `{packet_commit}`.
