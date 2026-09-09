#!/usr/bin/env python3
"""Copy the finished v6.0.0 handbook pages into a wiki clone, then verify.

The wiki is a separate repository that GitHub does not expose as an addressable
repo through its API, so an agent session scoped to `ZMS-Labs/epistemic-skills`
can clone it read-only but cannot push to it. The pages under `pages/` are the
finished, verified result; this script installs them and re-runs the oracle so
publishing is a checked act rather than a copy and a hope.

  git clone https://github.com/ZMS-Labs/epistemic-skills.wiki.git /tmp/es-wiki
  python publish_wiki.py /tmp/es-wiki            # dry run, reports the delta
  python publish_wiki.py /tmp/es-wiki --apply    # write, then verify
  cd /tmp/es-wiki && git add -A && git commit && git push

Refuses to write to anything that does not look like a wiki clone, reusing
`apply_v7_updates.check_paths` so the two cannot disagree about what a wiki is.
"""

from __future__ import annotations

import argparse
import filecmp
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAGES = HERE / "pages"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("wiki")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    root = Path(args.wiki)
    pages = sorted(PAGES.glob("*.md"))
    if not pages:
        print(f"no pages under {PAGES}")
        return 1

    reasons = _load("apply_v7_updates").check_paths(root)
    if reasons:
        print(f"refusing: {root} does not look like a wiki clone")
        for r in reasons:
            print(f"  - {r}")
        return 1

    added, changed, same = [], [], []
    for src in pages:
        dst = root / src.name
        if not dst.exists():
            added.append(src.name)
        elif not filecmp.cmp(src, dst, shallow=False):
            changed.append(src.name)
        else:
            same.append(src.name)
    stale = sorted(p.name for p in root.glob("*.md")
                   if not (PAGES / p.name).exists())

    print(f"{len(added)} new, {len(changed)} changed, {len(same)} identical")
    for n in added:
        print(f"  + {n}")
    for n in changed:
        print(f"  ~ {n}")
    for n in stale:
        print(f"  ! {n} exists in the wiki but not in pages/ -- left alone, review by hand")

    if not args.apply:
        print("\ndry run -- nothing written. Re-run with --apply.")
        return 0

    for src in pages:
        shutil.copy2(src, root / src.name)
    print(f"\nwrote {len(pages)} pages to {root}")

    print("verifying:")
    return subprocess.call([sys.executable, str(HERE / "check_wiki.py"), str(root)])


if __name__ == "__main__":
    sys.exit(main())
