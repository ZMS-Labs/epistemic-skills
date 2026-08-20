# Publication-gate summary

## NO-GO

The exact v6.0.0 candidate
`d0165bd0cf1e79b94140d4493cc11bf7ba31a2a3` must not be tagged or published.

Open blockers:

| Ruling | Priority | Gates | Finding |
|---|---|---|---|
| OAI-P1-01 | P1 | RG-5 | Exact subject fails the repository's author-matching DCO policy. |
| OAI-P1-02 | P1 | RG-5 | `openai-bundles` and `mission-custody-contract` were not rerun on the exact subject. |
| OAI-P1-03 | P1 | RG-2, RG-8, RG-9 | The current committed authorization sequence changes and invalidates the SHA it must authorize. |
| OAI-P2-01 | P2 | RG-1, RG-6 | The immutable release note contains three reproducible state/count inaccuracies. |

The historical promotion packet remains honestly `NOT_READY`; it is not proof of
publication readiness and should not be cosmetically regenerated. The minimum
safe remedy is a prospectively corrected authority sequence, a properly signed
successor candidate with accurate notes, complete exact-SHA reruns, and a fresh
operator-dispatched independent gate.

No implementer-authored GO was accepted. This run performed no merge, tag,
Release, ruleset change, packet mutation, operator acceptance, or publication
authorization.

See `dossier.md` for evidence and limits, and `arbitration.md` for the complete
RG-1..RG-9 disposition and conforming `ruling-set@1` object.
