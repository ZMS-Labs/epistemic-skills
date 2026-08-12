# LOCAL.md — ZMS fleet overlay for decision-ledger

Overlay binding per this skill's "Local overlay" contract: adds substrate bindings;
never overrides the method. Public-safe by design — this file ships in the public
epistemic-skills package, so it states the routing rule and store *roles* only.
The resolvable coordinates of the private substrate live in that store's own
README, which is the durable copy of this rule (see the fleet's private ops
repository, discoverable via fleet governance docs — not named here per this
repo's public-content gate).

## Substrate bindings (ZMS fleet)

- **Public store:** this repository's `.ledger/entries.jsonl` — scoped to this
  project's own design/coordination decisions (its existing adoption).
- **Private store:** the ZMS fleet's private ops repository, which has adopted
  `.ledger/entries.jsonl` as the default substrate for fleet/org/ops/tooling
  decisions. Its `.ledger/README.md` carries the full binding.
- Repo-local `.ledger/` in other fleet repos remains valid for decisions scoped to
  those repos; do not create parallel stores where an adequate artifact (ADR,
  plan, issue decision) already exists.

## Visibility routing rule

1. Entries inherit substrate visibility — a ledger in a public repo is public.
2. Entries touching internal topology (IPs, hostnames, service layout),
   unremediated vulnerabilities, or person-identifying corrections MUST target
   the private store.
3. Supersedes chains never cross substrates. A private correction to a public
   decision restates a minimal public-safe head in the public store; detail
   stays private. Cross-store ids dangle, and dangling ids fail closed.
