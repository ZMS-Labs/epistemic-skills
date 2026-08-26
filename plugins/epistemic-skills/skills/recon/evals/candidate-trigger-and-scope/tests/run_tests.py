#!/usr/bin/env python3
"""Polarity tests for recon candidate-mode (harvest-before-adopt) trigger discipline and scope."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> list:
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing candidate-mode trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("candidate_mode_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "explicit-adopt-or-keep", "use-x-instead-proposal", "overlap-discovered-mid-design",
        "mature-competitor-negative-harvest", "hard-neg-no-incumbent", "hard-neg-dependency-upgrade",
        "hard-neg-already-adopted", "hard-neg-factual-lookup", "hard-neg-in-repo-refactor",
        "state-drop-at-top-read-still-due", "state-harvest-record-handoff",
        "state-partition-escalation", "state-not-harvestable-disclosure", "state-injection-guard",
    ], "candidate-mode fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids must be unique")
    for fixture in fixtures:
        require(fixture["expected_action"] in scorer.ACTIONS, f"{fixture['id']}: unknown expected_action {fixture['expected_action']!r}")
        require(fixture["trigger"] in {"explicit", "auto", "state", "none"}, f"{fixture['id']}: unknown trigger {fixture['trigger']!r}")
        require(isinstance(fixture["scenario"], str) and fixture["scenario"].strip(), f"{fixture['id']}: scenario must be nonempty")
    plants = {f["id"]: f for f in fixtures}
    require([f["id"] for f in fixtures if f.get("negative_harvest")] == ["mature-competitor-negative-harvest"], "negative-harvest plant misplaced")
    require([f["id"] for f in fixtures if f.get("drop_at_top")] == ["state-drop-at-top-read-still-due"], "drop-at-top plant misplaced")
    require([f["id"] for f in fixtures if f.get("injection_present")] == ["state-injection-guard"], "injection plant misplaced")
    require(plants["state-partition-escalation"]["expected_action"] == "partition", "the escalation fixture must expect the expensive path")

    balanced = scorer.score(fixtures, load("balanced"))
    require(balanced["pass"], balanced["failures"])
    require(balanced["actions"] == {"harvest": 8, "partition": 1, "no-fire": 5}, balanced["actions"])

    over = scorer.score(fixtures, load("overfiring"))
    require(not over["pass"], "overfiring parody unexpectedly passed")
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 5, over["failures"])
    require(any("never runs and is never installed" in failure for failure in over["failures"]), over["failures"])
    require(any("learning, not adoption" in failure for failure in over["failures"]), over["failures"])
    require(any("data, never instructions" in failure for failure in over["failures"]), over["failures"])
    require(any("no whole-candidate verdict" in failure for failure in over["failures"]), over["failures"])
    require(any("check for it by name" in failure for failure in over["failures"]), over["failures"])
    require(any("confirmation risk" in failure for failure in over["failures"]), over["failures"])

    under = scorer.score(fixtures, load("underfiring"))
    require(not under["pass"], "underfiring parody unexpectedly passed")
    require(sum("expected harvest" in failure for failure in under["failures"]) == 6, under["failures"])
    require(any("state-drop-at-top-read-still-due: expected harvest, got triage-only" in failure for failure in under["failures"]), under["failures"])
    require(any("expected partition" in failure for failure in under["failures"]), under["failures"])
    require(any("harvest_record must be true" in failure for failure in under["failures"]), under["failures"])
    require(any("confirmation risk" in failure for failure in under["failures"]), under["failures"])
    require(any("landmine finding" in failure for failure in under["failures"]), under["failures"])

    unknown_action = load("balanced")
    unknown_action[0]["action"] = "adopt-sprint"
    unknown_action[1]["action"] = ["harvest"]
    report = scorer.score(fixtures, unknown_action)
    require(not report["pass"] and sum("unknown action" in failure for failure in report["failures"]) == 2, report["failures"])

    unhashable_id = load("balanced")
    unhashable_id[0]["id"] = ["explicit-adopt-or-keep"]
    report = scorer.score(fixtures, unhashable_id)
    require(not report["pass"], "off-contract id types must fail, never crash")
    require(any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])
    require(any("response missing" in failure for failure in report["failures"]), report["failures"])

    report = scorer.score(fixtures, {"responses": []})
    require(not report["pass"] and any("must be a JSON array" in failure for failure in report["failures"]), report["failures"])
    report = scorer.score("not-a-list", load("balanced"))
    require(not report["pass"] and any("fixtures must be a JSON array" in failure for failure in report["failures"]), report["failures"])
    stray_element = load("balanced")
    stray_element.append("not a record")
    report = scorer.score(fixtures, stray_element)
    require(not report["pass"], "non-object response entries must fail, never crash")
    require(any("are not objects" in failure for failure in report["failures"]), report["failures"])
    require(any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])

    duplicated = load("balanced")
    duplicated.append(dict(duplicated[0]))
    report = scorer.score(fixtures, duplicated)
    require(not report["pass"] and any("missing or duplicated" in failure for failure in report["failures"]), report["failures"])

    noisy_no_fire = load("balanced")
    noisy_no_fire[4]["harvest_record"] = False
    noisy_no_fire[5]["skip_record"] = False
    report = scorer.score(fixtures, noisy_no_fire)
    require(not report["pass"], "a no-fire carrying process-artifact fields, even falsy, is not silent")
    require(any("no-fire is silent" in failure for failure in report["failures"]), report["failures"])
    require(any("without a skip record" in failure for failure in report["failures"]), report["failures"])

    shape_violation = load("balanced")
    shape_violation[0]["levels_read"] = "one through four"
    shape_violation[1]["per_level_decisions"] = [{"L1": "PROBE"}]
    shape_violation[2]["not_harvestable"] = "nothing"
    shape_violation[3]["per_level_decisions"] = ["L9:DROP", "L1:MAYBE"]
    shape_violation[11]["partition_rows"] = True
    report = scorer.score(fixtures, shape_violation)
    require(not report["pass"], "shape violations must fail, never crash or coerce")
    require(any("levels_read must be an array of ladder levels" in failure for failure in report["failures"]), report["failures"])
    require(any("per_level_decisions entries must be bare strings" in failure for failure in report["failures"]), report["failures"])
    require(any("not_harvestable must be an array of bare strings" in failure for failure in report["failures"]), report["failures"])
    require(any("must match 'L<level>:PROBE|PARK|DROP'" in failure for failure in report["failures"]), report["failures"])
    require(any("partition_rows must be an integer count" in failure for failure in report["failures"]), report["failures"])

    suppressed = load("balanced")
    suppressed[9]["drop_suppressed_read"] = True
    report = scorer.score(fixtures, suppressed)
    require(not report["pass"] and any("never suppresses the level 1-4 read" in failure for failure in report["failures"]), report["failures"])
    drop_vanished = load("balanced")
    drop_vanished[9]["per_level_decisions"] = ["L1:PROBE", "L2:PROBE", "L3:PROBE", "L4:PROBE"]
    report = scorer.score(fixtures, drop_vanished)
    require(not report["pass"] and any("must appear in per_level_decisions" in failure for failure in report["failures"]), report["failures"])

    negatives_unmined = load("balanced")
    negatives_unmined[3]["negative_harvest"] = False
    report = scorer.score(fixtures, negatives_unmined)
    require(not report["pass"] and any("richest seam" in failure for failure in report["failures"]), report["failures"])

    triage_fixture = [{
        "id": "synthetic-cheap-probe",
        "scenario": "Triage on a candidate whose probe is an hour and fully reversible; cheap-and-reversible short-circuits the analysis.",
        "trigger": "state",
        "expected_action": "triage-only",
    }]
    report = scorer.score(triage_fixture, [{"id": "synthetic-cheap-probe", "action": "triage-only", "spend_decision": "PROBE"}])
    require(report["pass"] and report["actions"] == {"triage-only": 1}, report["failures"])
    report = scorer.score(triage_fixture, [{"id": "synthetic-cheap-probe", "action": "triage-only", "spend_decision": "MAYBE"}])
    require(not report["pass"] and any("spend_decision must be one of PROBE, PARK, DROP" in failure for failure in report["failures"]), report["failures"])
    report = scorer.score(triage_fixture, [{"id": "synthetic-cheap-probe", "action": "triage-only", "spend_decision": "DROP", "drop_suppressed_read": True}])
    require(not report["pass"] and any("never suppresses the level 1-4 read" in failure for failure in report["failures"]), report["failures"])
    report = scorer.score(triage_fixture, [{"id": "synthetic-cheap-probe", "action": "triage-only", "spend_decision": "PARK", "harvest_record": True, "levels_read": [1]}])
    require(not report["pass"] and sum("spend decision without a read" in failure for failure in report["failures"]) == 2, report["failures"])

    # ---- one level, one decision ---------------------------------------
    # `per_level_decisions` entries were validated one at a time, so a
    # response could assert BOTH `L1:PROBE` and `L1:DROP`. The battery treats
    # these as auditable per-level spend decisions; a level that decided two
    # incompatible things decided nothing.
    harvest_fixture = [f for f in fixtures if f["expected_action"] == "harvest"][:1]
    require(harvest_fixture, "no harvest fixture to exercise")
    hid = harvest_fixture[0]["id"]

    def harvest_row(**over):
        row = {"id": hid, "action": "harvest", "harvest_record": True,
               "levels_read": [1, 2], "per_level_decisions": ["L1:PROBE"],
               "not_harvestable": ["the vendored fork"]}
        if harvest_fixture[0].get("negative_harvest"):
            row["negative_harvest"] = True
        if harvest_fixture[0].get("injection_present"):
            row["landmine_reported"] = True
        if harvest_fixture[0].get("drop_at_top"):
            row["per_level_decisions"] = ["L1:PROBE", "L6:DROP"]
        row.update(over)
        return row

    baseline = scorer.score(harvest_fixture, [harvest_row()])
    require(baseline["pass"], baseline["failures"])

    dup = harvest_row()
    dup["per_level_decisions"] = list(dup["per_level_decisions"]) + ["L1:DROP"]
    report = scorer.score(harvest_fixture, [dup])
    require(not report["pass"],
            "contradictory per-level decisions scored as a PASS")

    # ---- a no-fire is silent, including in fields nobody enumerated ------
    nofire_fixture = [f for f in fixtures if f["expected_action"] == "no-fire"][:1]
    require(nofire_fixture, "no no-fire fixture to exercise")
    nid = nofire_fixture[0]["id"]
    require(scorer.score(nofire_fixture,
                         [{"id": nid, "action": "no-fire"}])["pass"],
            "a bare no-fire must pass")
    for extra in ("explanation", "reason", "notes"):
        report = scorer.score(nofire_fixture,
                              [{"id": nid, "action": "no-fire", extra: "why"}])
        require(not report["pass"],
                f"no-fire carrying an unlisted {extra!r} field scored as a PASS")

    # ---- triage-only decides spend; it does not adopt --------------------
    triage_only = [{
        "id": "synthetic-cheap-probe",
        "scenario": "Triage-only control.",
        "trigger": "state",
        "expected_action": "triage-only",
    }]
    for field in ("installed", "adopted"):
        report = scorer.score(triage_only, [{
            "id": "synthetic-cheap-probe", "action": "triage-only",
            "spend_decision": "PROBE", field: True}])
        require(not report["pass"],
                f"triage-only reporting {field}=true scored as a PASS")

    print("recon candidate-mode trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
