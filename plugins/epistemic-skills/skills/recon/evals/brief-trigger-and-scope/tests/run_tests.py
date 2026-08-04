#!/usr/bin/env python3
"""Polarity tests for blindspot-pass trigger discipline and recon scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing blindspot-pass trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("blindspot_pass_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-recon-request", "map-territory-contradiction", "hidden-coupling-discovered",
        "pre-fanout-multiplication", "ambiguous-brief-two-targets", "hard-neg-unfamiliar-repo-only",
        "hard-neg-bounded-dispatch", "hard-neg-review-subject-established",
        "hard-neg-plan-premises-verified", "factual-lookup-no-fire", "mechanical-edit-no-fire",
        "state-report-contract", "state-obvious-fix-not-implemented", "state-injection-guard",
    ], "blindspot-pass fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids must be unique")
    for fixture in fixtures:
        require(fixture["expected_action"] in scorer.ACTIONS, f"{fixture['id']}: unknown expected_action {fixture['expected_action']!r}")
        require(fixture["trigger"] in {"explicit", "auto", "implicit", "none", "state"}, f"{fixture['id']}: unknown trigger {fixture['trigger']!r}")
        require(isinstance(fixture["scenario"], str) and fixture["scenario"].strip(), f"{fixture['id']}: scenario must be nonempty")

    balanced_rows = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    balanced = scorer.score(fixtures, balanced_rows)
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"full-pass": 8, "no-fire": 6}, balanced["actions"])

    for name in ("overfiring", "underfiring"):
        report = scorer.score(fixtures, json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8")))
        require(not report["pass"], f"{name} parody unexpectedly passed")
    over = scorer.score(fixtures, json.loads((ROOT / "examples" / "overfiring.json").read_text(encoding="utf-8")))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 6, over["failures"])
    require(any("ends at understanding" in failure for failure in over["failures"]), over["failures"])
    require(any("captured in the rewritten request" in failure for failure in over["failures"]), over["failures"])
    under = scorer.score(fixtures, json.loads((ROOT / "examples" / "underfiring.json").read_text(encoding="utf-8")))
    require(sum("expected full-pass" in failure for failure in under["failures"]) == 6, under["failures"])
    require(any("no best-guess answer" in failure for failure in under["failures"]), under["failures"])
    require(any("recon floor" in failure for failure in under["failures"]), under["failures"])
    require(any("Landmines finding" in failure for failure in under["failures"]), under["failures"])

    unknown_action = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    unknown_action[0]["action"] = "recon-sprint"
    unknown_action[1]["action"] = ["full-pass"]
    report = scorer.score(fixtures, unknown_action)
    require(not report["pass"] and sum("unknown action" in failure for failure in report["failures"]) == 2, report["failures"])

    unhashable_id = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    unhashable_id[0]["id"] = ["explicit-recon-request"]
    report = scorer.score(fixtures, unhashable_id)
    require(not report["pass"], "off-contract id types must fail, never crash")
    require(any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])
    require(any("response missing" in failure for failure in report["failures"]), report["failures"])

    noisy_no_fire = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    noisy_no_fire[5]["implemented"] = False
    noisy_no_fire[6]["skip_record"] = False
    report = scorer.score(fixtures, noisy_no_fire)
    require(not report["pass"], "a no-fire carrying process-artifact fields, even falsy, is not silent")
    require(any("must be silent" in failure for failure in report["failures"]), report["failures"])
    require(any("without a skip record" in failure for failure in report["failures"]), report["failures"])

    duplicated = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    duplicated.append(dict(duplicated[0]))
    report = scorer.score(fixtures, duplicated)
    require(not report["pass"] and any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])

    shape_violation = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    shape_violation[0]["sections_present"] = "all four"
    shape_violation[1]["questions"] = {"q1": "answered"}
    shape_violation[2]["artifacts_read"] = True
    report = scorer.score(fixtures, shape_violation)
    require(not report["pass"], "shape violations must fail, never crash or coerce")
    require(any("must be an array of bare ids" in failure for failure in report["failures"]), report["failures"])
    require(any("must be an array of question records" in failure for failure in report["failures"]), report["failures"])
    require(any("must be an integer count" in failure for failure in report["failures"]), report["failures"])

    print("blindspot-pass trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
