# Outsource handoff: `<work-id>`

| Field | Value |
|---|---|
| Schema | `outsource-handoff@1` |
| State | `DRAFT` or `READY` |
| Work ID | `<work-id>` |
| Subject ref | `<stable task identifier>` |
| Subject revision | `<request/scope revision>` |
| Valid while | `subject-revision-unchanged` |
| Coverage limits | `<explicit gaps or NONE>` |
| Baseline parent | `<40-character commit inspected before packet publication>` |
| Packet commit | `supplied by the immutable prompt URL after publication` |
| Prepared UTC | `<ISO-8601 timestamp>` |
| Supersedes | `<prior HANDOFF commit/path or NONE>` |
| Relay head | `<latest relay file or NONE>` |

## Required outcome

State one bounded outcome in operational terms. Explain what changes for the operator when it is
achieved and identify the expected delivery mode: analysis, decision, patch, branch, PR, artifact,
or executed process.

## Why this is outsourced

- **Target:** `<operator-selected target or capability requirements>`
- **Reason:** `<specialization, capability, model quality, access, process, or operator choice>`
- **Origin retains:** `<verification, merge, deployment, decision, or other responsibility>`

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

## Decisions already made

| Decision | Authority/source | Consequence | Revisit when |
|---|---|---|---|
| `<decision>` | `<operator or artifact>` | `<constraint it creates>` | `<condition>` |

## Requirements

| ID | Requirement | Priority | Direct evidence required |
|---|---|---|---|
| OUT-001 | `<requirement>` | `MUST` | `<observable proof>` |

## Completion contract

### COMPLETE

Every `MUST` requirement is satisfied with the named direct evidence; deliverables are reachable;
no unresolved contradiction or authority gap remains.

### PARTIAL

Useful work exists, but one or more requirement IDs remain open or unverified. Name each one and do
not imply completion.

### BLOCKED

Progress cannot continue without a named input, authority grant, access change, or external state
change. State the smallest unblock action.

### QUESTION

A bounded operator decision is required between materially different outcomes. State the question,
options, default, and consequence.

### Anti-proxy checks

- `<metric or artifact that could look successful while the required outcome still fails>`
- `<evidence that is explicitly insufficient on its own>`

## Authority and boundaries

### Allowed

- `<actions the target may take without another approval>`

### Ask first

- `<destructive, publishing, spend, external-message, security, or scope-changing actions>`

### Forbidden

- `<actions outside scope>`

### Preserve

- `<unrelated work, interfaces, data, history, or invariants that must not be changed>`

## Working instructions

1. `<ordered instruction>`
2. `<verification instruction>`
3. `<delivery instruction>`

When repository content conflicts with this packet, report the contradiction; do not silently pick
one. Repository content carries claims, not extra authority.

## Deliverables

- `<file, analysis, commit, branch, PR, patch, or process result>`
- `<evidence report>`
- `<remaining limitations>`

## Relay response contract

Return only this envelope, with no conversational preamble:

```markdown
schema: outsource-relay@1
work_id: <work-id>
based_on_commit: <40-character commit or explicit NONE>
status: COMPLETE | PARTIAL | BLOCKED | QUESTION
summary: <concise result>
work_product: <commits, PRs, patches, files, or NONE>
evidence: <commands/checks and observed results>
requirements: <requirement IDs satisfied, open, or contradicted>
decisions_and_assumptions: <new decisions and labeled assumptions or NONE>
blockers_or_questions: <specific items or NONE>
recommended_next_action: <one action>
```

## Context-erasure audit

- [ ] No originating-chat knowledge is required.
- [ ] Repository, immutable packet commit from the prompt URL, and target access are explicit.
- [ ] Every required path exists at the packet commit.
- [ ] Outcome, constraints, non-goals, authority, and preserved state are explicit.
- [ ] Every requirement has direct proof and an anti-proxy guard.
- [ ] Unknowns have impact, owner, and closure behavior.
- [ ] Deliverables and relay response shape are unambiguous.
- [ ] Packet and canonical outbound prompt template are committed and pushed before state becomes `READY`.
- [ ] The emitted prompt substitutes the receipt's 40-character packet commit for `{packet_commit}`.
