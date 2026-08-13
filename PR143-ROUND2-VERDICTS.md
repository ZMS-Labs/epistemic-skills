# PR #143 round 2 — five case tables, adversarially refuted

**Method:** one derivation agent per defect (product-space case table, adopted
rule, rejected rules with the row that kills each, predicted mutants), then two
independent lenses per defect — *unenumerated-case* and *collateral*. 15 agents,
0 errors. Journal:
`subagents/workflows/wf_2afa299f-f4b/journal.jsonl`; digest
`<scratchpad>/wf-digest.md`.

**Headline: all five defects are real and all five adopted fixes are
IN-SCOPE for #143 — but every one came back `NEEDS_ROWS`, and TWO of them
would ship a NEW defect of the same class they fix.** Nothing here is
implemented yet. That is deliberate: implementing a fix whose hole is already
named is the failure this program keeps paying for.

⚠ A note on the evidence itself: my first extractor read the journal with
`str.splitlines()` and crashed — because `splitlines()` splits on U+2028, and
the journal *contains* U+2028 as finding data. **Defect A bit the reader of its
own evidence.** Split on `"\n"`.

---

## A — identity guard (`_refuse_unprintable_identity`, shipped `284b53c`)

**Adopted:** `len(value.splitlines()) > 1 or not value.isprintable()`, on the
RAW value (never NFKC first — NFKC maps NBSP to space and would launder the
confusable before the check).

29 rows, 27 executed. A full-range census found the splitlines boundary set is
exactly `{0A,0B,0C,0D,1C,1D,1E,85,2028,2029}` — 8 of 10 are Cc, which is why
the shipped Cc+Cf rule caught most of them and missed exactly the two Z ones.

Why the reported minimal patch (add Zl+Zp) is **rejected**: it is the same
failure shape as the defect — extending the author's enumeration by exactly
the two categories the last reviewer happened to find. `isprintable()` fails
**closed** on the unenumerated class, and the census shows it additionally
refuses lone surrogates (which persist to disk via `ensure_ascii` and then
crash any utf-8-strict display or hash surface — executed), private-use,
unassigned, and the 15 non-ASCII Zs spaces. Zero false refusals across the
realistic battery: ASCII, composed *and decomposed* accents, CJK, single-codepoint
emoji, spaced human names.

Both clauses are load-bearing and each looks redundant next to the other:
`'a\n'` (trailing) leaves `splitlines()` at length 1 and is caught only by
`isprintable`; `'a\tb'` and an ANSI escape do not split at all.

### ⚠ Refuter findings — must be resolved before implementing

1. **The adopting argument does not survive at its own boundary.** The
   `ZS-NBSP` row justifies the widening by saying a display-identical,
   byte-distinct pair defeats the casefolded `acceptor_id != worker_id`
   self-certification check. But `'agent:worker-1 '` — a **trailing ASCII
   space** — builds exactly that pair from pure ASCII, and the adopted rule
   **accepts it** (executed). So either the justification is scoped to
   non-ASCII (and must say so) or the rule needs a separate trailing/leading
   whitespace decision. *Scope the justifying principle to the axis you
   tested.*
2. **The rule is a predicate; the guard's contract is predicate PLUS message
   shape.** A shipped test pins that the refusal surfaces `​` — the
   `repr` of the offending character. An implementer transcribing the adopted
   predicate with any natural one-line message breaks it.

**Residual, cannot be closed at this guard:** invisible-but-printable
characters — CGJ (U+034F), variation selectors, Hangul fillers. `isprintable()`
is True and every candidate rule accepts them; the same category holds the
combining acute in `José`, so character-class granularity cannot separate them.
**The docstring must re-scope its claim** to "no line structure, no control
effects, no Cf-class invisibles" — never "display-unique" — and point at es#150,
exactly as the reserved-note guard already defers homoglyphs. → separate issue.

---

## B — `_glob_regex` anchors with `$` (silent PASS)

**Adopted:** one token at the single compile site, `"$"` → `r"\Z"`, keeping
`re.DOTALL` and `.match`. Fixes all four consumers at once. `re.fullmatch` at
every call site was measured **observably identical in every grid cell**, so it
buys nothing while moving the guarantee from one compiler to four call sites.
Normalising newlines away was rejected outright: it would make the false CLEAN
the *spec*.

### 🚨 Refuter finding — the fix creates an UNDISCHARGEABLE refusal

Executed: with the anchor fixed, `safe.txt\n` correctly stops satisfying
`scope.in` — and the resulting refusal tells the acceptor to type
`--scope-ack "safe.txt\n"`. Every shell delivers that as a literal backslash +
`n`; `_norm_path` then turns the backslash into `/`; the ack names `safe.txt/n`
and **discharges nothing.**

**That is defect #25 again, in the fix for a different defect** — a refusal
whose printed exit does not work. The `_display_path` JSON quoting shipped at
`ed66dfe` covers whitespace but not this. **B must not land until its discharge
recipe is proven to work on a control-character path.**

Two more, both real:

- **The narrative overclaims.** For guards on shell/MCP tools the verifier
  *forces* `command_regexes` and `path_globs` never fire — and the identical
  `$` one-newline tolerance survives there verbatim (executed). "Scope patterns
  no longer match one character too many" is false for that class.
- **The seven suites are provably blind to this change** — they pass
  byte-identically with and without the fix. The merge gate cannot tell
  shipping it from not shipping it. Any commit must bring its own pins.

---

## C — `_link_count` stats the raw spelling (POSIX)

**Adopted:** stat the target returned by the **same `_resolve_artifact_path`
the writer used** — not `_norm_path`, which case-folds on NT and would name a
nonexistent spelling on a case-sensitive directory (executed), and not a
both-spellings probe, which mints a *false* MULTIPLY LINKED claim about bytes
that are not the receipted artifact.

Bonus, measured: the shipped raw stat also probes paths **outside the
workspace** for absolute spellings supplied via a forged receipt — an
information-probe surface the adopted rule closes.

### 🚨 Refuter finding — the fix turns a silent None into an uncaught CRASH

Executed, as an unprivileged Windows user: replace `docs/` with half of a
`docs ↔ other` junction loop, then `record_verdict("PASS", ...)`. Shipped code
records the PASS. **The adopted rule raises an uncaught `RuntimeError: Symlink
loop`** — a crash on the acceptance path from attacker-influenceable
filesystem state, i.e. the denial-of-service class `_load_receipt`'s doctrine
already forbids.

`RuntimeError` must join the caught set, and the derivation's own
unenumerated case (a resolved path that is **not a regular file** — a forged
`artifact_path` of `'.'` resolves to the workspace root, whose `st_nlink >= 2`
on POSIX by construction, reporting the workspace root as MULTIPLY LINKED)
means the probe needs an `S_ISREG` gate. Neither is optional.

---

## D — terminal `/.` : lexical and resolver disagree

**Adopted:** collapse `.` **segments** to a fixed point in the one shared
normaliser (`_normalize_relpath`) — terminal `/.`, iterated, interior `/./`,
leading `./`, doubled `//` — and **only** `.` segments. `..` stays untouched
(refused at the resolver, disclosed on the pattern side); a trailing dot
*inside* a final segment name (`weird.`) stays untouched, because it is a legal
name character and NT-only filesystem semantics must not leak into a
cross-platform lexical normaliser.

**Why this is in scope, and it is not the reported reason.** Codex's row is a
false *flag* — the safe direction, and dischargeable. The priority flip comes
from the **mirror row the derivation was asked to hunt and found**: the same
disagreement on the **pattern** side is a false **CLEAN** — an operator's
`scope.out` can be silently disabled by one `/.` spelling, and
`uncompared_scope_entries` does not list it, so nothing discloses it. Refusing
the spelling at `record_effect` instead was rejected because scope entries
never pass through `record_effect`, and because chains are append-only: dotted
spellings already sealed would flag forever.

### ⚠ Refuter finding
`scope.in=['./']` is a natural way to declare "the whole workspace is in
scope" — the include-side twin of the exclusion row, and stronger against the
"no honest manifest contains that" objection. Add it.

---

## E — one ack discharges two obligations

**Adopted:** key obligations by `(violating_path, reason-kind)`. A bare
`--scope-ack PATH` discharges only boundary-kind obligations; a link-kind
obligation needs `--scope-ack linked:PATH`; unknown kinds are never
dischargeable by an existing token form (**fail closed**). Parsing stays
exact-path-first, per the tie-break `_acknowledged_paths` already settled.

The "this breaks a shipped CLI contract" objection **dissolves on
measurement**: the merge base `41ee58e` contains **zero** occurrences of
`scope_ack` / `--scope-ack`. The flag, the gate, the finding and every
asserting test are introduced *by this PR*. Changing them revises #143's own
unreleased surface.

A per-kind bespoke flag (`--link-ack`) was rejected as a noun list that cannot
terminate — each new reason kind ships without its flag and fails open through
the path key. Deriving the token from the finding's reason makes new kinds fail
closed automatically.

### ⚠ Refuter finding — the token shares a namespace with real filenames
A file named `linked:name` **is creatable on NTFS** (alternate-data-stream
syntax), so the note `scope-ack by X: linked:docs/a` is permanently ambiguous
between a qualifier and a literal path — **the same audit defect this rule
exists to fix**. The record half must be unambiguous by construction, which is
es#150's structured `{path, kind}` field, not a token syntax.

A second refuter argues the link ack is *categorical* ("I accept other names
exist and have checked"), so a count change 2→3 does not create a new
obligation. Worth settling explicitly rather than leaving implied.

---

## Disposition

| defect | verdict | blocker before implementing |
|---|---|---|
| A | FIX_HERE | resolve the trailing-ASCII-space boundary; preserve the `repr` message shape; re-scope the docstring claim + file the invisible-but-printable residual |
| B | FIX_HERE | **prove the discharge recipe works on a control-character path first**; disclose the `command_regexes` twin; bring its own pins (suites are blind) |
| C | FIX_HERE | catch `RuntimeError`; gate on `S_ISREG` |
| D | FIX_HERE | add the `scope.in=['./']` include-side row |
| E | FIX_HERE (semantics) → es#150 (record schema) | make the record half unambiguous by construction, not by token syntax |

**Not riding along, to be filed:** control-character rejection at
`record_effect` (a contract change, es#147 precedent) · the invisible-but-
printable identity residual · the `command_regexes` `$` twin · the
`PermissionError`/parent-mkdir adjacency · the NT pattern-side trailing-dot
seam.
