#!/usr/bin/env python3
"""Apply the approved commission-watch live-surface alignment exactly once.

This is a branch-scoped migration helper. It fails if any expected source text is
missing or appears more than once, so it cannot silently edit a nearby passage.
The helper and its workflow are removed after the generated commit is verified.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one source match, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before_once(path: Path, marker: str, insertion: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one insertion marker, found {count}")
    path.write_text(text.replace(marker, insertion + marker, 1), encoding="utf-8")


def main() -> int:
    budget = ROOT / ".github" / "scripts" / "check_description_budget.py"
    health = ROOT / "plugins" / "epistemic-skills" / "skills" / "health" / "SKILL.md"
    readme = ROOT / "README.md"

    replace_once(
        budget,
        "# The recorded budget: the sum of the 14 packaged v5.0.0 skills' description",
        "# The recorded budget: the sum of the 14 packaged skill description",
    )
    replace_once(
        budget,
        """# Originally recorded as 8200 under a character-count bug. Corrected to 8230 on
# 2026-08-07 when the guard switched to UTF-8 bytes: the packaged descriptions
# themselves did not grow; twelve skills contain non-ASCII code points that cost
# two UTF-8 bytes each. Raising the ceiling here records the true harness cost of
# the already-shipped text — it does not authorize further growth.
""",
        """# Originally recorded as 8200 under a character-count bug, then corrected to
# 8230 on 2026-08-07 when the guard switched to UTF-8 bytes. The commission-watch
# clarification reduced the exact package total by 71 bytes without adding a
# skill or weakening another trigger. The ceiling therefore moves down to 8159
# so that released headroom cannot silently refill.
""",
    )
    replace_once(budget, "CEILING_BYTES = 8230", "CEILING_BYTES = 8159")

    replace_once(
        health,
        """- **This skill answers when *asked*; it does not watch.** `watch` owns unattended
  observation. **A green run here does not imply you would have been told** —
  that depends entirely on whether a `watch` covering this bound has reached
  `PROVEN`. An unproven watcher and no watcher are the same thing.
""",
        """- **This skill answers when *asked*; it does not watch.** `watch` commissions
  unattended observation. **A green run here does not imply you would have been
  told** — that depends entirely on whether an external observer covering this
  bound was commissioned under `watch` and has reached `PROVEN`. An unproven
  commission and no observer are operationally the same.
""",
    )
    replace_once(
        health,
        '| "A green run means I would hear about it if it broke" | Only if a `watch` covering that bound has reached `PROVEN`. This skill does not watch, and an unproven watcher is not one. |',
        '| "A green run means I would hear about it if it broke" | Only if an external observer covering that bound was commissioned under `watch` and has reached `PROVEN`. This skill does not watch. |',
    )

    replace_once(
        readme,
        '| A bound must be noticed while unattended, or a watcher must be proven | `watch` | `DECLARED`/`INERT`/`PROVEN`/`SUSPECT`; never “installed” before a proof fire |',
        '| A bound must be noticed between sessions, or an external observer must be commissioned or re-proved | `watch` | Validated `watch-commission@1`: `DECLARED`/`BLOCKED`/`INERT`/`PROVEN`/`SUSPECT`; the skill itself never watches |',
    )
    replace_once(
        readme,
        '    U -. "unattended bound" .-> W["watch"]',
        '    U -. "unattended bound" .-> W["Commission Watch<br/>(watch)"]',
    )
    insert_before_once(
        readme,
        "`resolve` (literature), `decision-ledger`, `outsource`, and `open-questions` are cross-cutting.",
        "`watch` commissions observation; an external runtime performs it. A separate\nmission-control layer may retain and act on the commission, but no Markdown skill\nremains awake between sessions.\n\n",
    )
    replace_once(
        readme,
        '| [`watch`](plugins/epistemic-skills/skills/watch/SKILL.md) | A bound must be noticed while unattended, or an existing watcher must be proven to still fire | Specify and prove an external watcher that acts unattended | `DECLARED`/`INERT`/`PROVEN`/`SUSPECT`; never “installed” before a proof fire |',
        '| [Commission Watch (`watch`)](plugins/epistemic-skills/skills/watch/SKILL.md) | A bound must be noticed between sessions, or an external observer must be commissioned or re-proved | Specify, commission, and proof-fire an external observer; the skill itself never persists | Validated `watch-commission@1`: `DECLARED`/`BLOCKED`/`INERT`/`PROVEN`/`SUSPECT` |',
    )

    print("commission-watch live-surface migration applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
