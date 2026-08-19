#!/usr/bin/env python3
"""Verify that every registered pin tag is reachable on origin at its pinned commit.

The counterpart repository (ZMS-Labs/epistemic-calibration) fetches this
repository BY SHA in its CI and relies on these tags only to keep those
SHAs reachable (its verify.yml says so explicitly). Deleting or moving a
pin tag would break the counterpart silently — this guard makes that a
red build here instead (charter obligation: bilateral reachability,
docs/coordination/2026-08-04-phase0-counterpart-reconnaissance.md).

Register every future pin tag in PINS with its PEELED commit hash (the
commit the tag must keep reachable — for an annotated tag, the target of
the tag object, shown by `git ls-remote` as the `^{}` line).

Stdlib only. Exit 0 = every pin present and correct; 1 = violation;
2 = origin unreachable (infrastructure, not a policy verdict).
"""
from __future__ import annotations

import subprocess
import sys

PINS = {
    # tag name -> peeled commit that must stay reachable at that name
    "pin/ecs-contract-2026-07-27": "8d9b2f85bd8e081a547e33f4bb9b5eb880a4c2b0",
    # v4.0.0 is the counterpart's v4 re-pin coordinate (issue #84): the
    # release tag itself is the reachability guarantee for the v4 event
    # contract, so it is guarded like a pin tag.
    "v4.0.0": "53ad6d523107d8c0d84f50945e22d6b744199446",
    # v6 rc2 freeze coordinates (operator-pushed 2026-08-18, live-verified).
    # Registration discipline for digest-sealed freezes (kimi ruling S5 /
    # CL-3): because this file is itself digest-inventoried, a freeze's OWN
    # pins are registered at the NEXT freeze — one-freeze lag, each
    # registration a deliberate reviewed edit; the guard tripping on a PINS
    # edit is the guard working. rc3's pins get registered at the freeze
    # after rc3.
    "pin/es-v6-rc2-candidate-2026-08-18": "6db8c50420b194aebbd09a2ea5f81c6a276897dc",
    "pin/es-v6-rc2-freeze-2026-08-18": "9aecd467236dfb927e9c13784d77a16d62f28f67",
}


def remote_tag_commit(tag: str) -> str | None:
    """Peeled commit for `tag` on origin, or None if the tag is absent."""
    ref = f"refs/tags/{tag}"
    proc = subprocess.run(
        ["git", "ls-remote", "origin", ref, ref + "^{}"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"git ls-remote failed: {proc.stderr.strip()}")
    direct = peeled = None
    for line in proc.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        sha, name = parts
        if name == ref + "^{}":
            peeled = sha
        elif name == ref:
            direct = sha
    # Annotated tags peel via the ^{} line; lightweight tags point straight
    # at the commit.
    return peeled or direct


def main() -> int:
    failures = []
    for tag, expected in PINS.items():
        try:
            actual = remote_tag_commit(tag)
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            print(f"ERROR: cannot query origin for {tag}: {exc}", file=sys.stderr)
            return 2
        if actual is None:
            failures.append(f"{tag}: ABSENT on origin (pinned {expected})")
        elif actual != expected:
            failures.append(f"{tag}: points at {actual}, pinned {expected}")
        else:
            print(f"ok pin tag {tag} -> {expected}")
    if failures:
        print("PIN TAG REACHABILITY VIOLATION:", file=sys.stderr)
        for failure in failures:
            print(f" - {failure}", file=sys.stderr)
        print(
            "Pin tags are the counterpart's reachability guarantee and are "
            "never deleted or moved; see the module docstring.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
