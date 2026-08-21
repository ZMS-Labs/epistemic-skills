# Redactions applied to `arbitration.md`

One class of change, mechanical, applied twice. No verdict, severity, ruling,
finding, or evidence conclusion was altered.

| Class | Occurrences | Original | Replacement |
|---|---|---|---|
| `email-address` | 2 (lines 38, 155) | the no-reply address in this repository's DCO sign-off identity, quoted by the judge when reading `git log` output and when stating its own authorship limit | `noreply-address-redacted` |

## Why, and the finding it produced

`check_public_content.py` flags any address-shaped string. The address in
question is a non-deliverable no-reply identity that already appears in every
commit trailer in this repository's history, so redacting it protects nothing —
but the gate is deliberately blunt, and the practice established this cycle is
to **remediate rather than allowlist**. Adding an allowlist entry to admit a
string the gate can live without would have widened the exemption surface to
save two characters of fidelity.

**The finding this produced is worth more than the redaction.** The gate did not
fail locally. It failed in CI, one commit later, on bytes that had not changed.
The cause: `tracked_files()` enumerated `git ls-files` only, so a **brand-new,
not-yet-staged file was invisible to it** — precisely the file class most likely
to carry a defect. A pre-commit run reported green; the file was staged
unchanged; CI, scanning a clean checkout where the file *is* tracked, failed on
it. The local gate had given false assurance at the one moment it was relied on.

`tracked_files()` now enumerates `--cached --others --exclude-standard`, so the
local answer matches the post-commit answer. In CI the checkout is clean and the
two enumerations are identical; nothing changes there. The window it closes is
entirely local, which is where it mattered.
