#!/usr/bin/env python3
"""Polarity tests for did-it-land trigger discipline and landing-verdict scope."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def load(name: str) -> list:
    return json.loads((ROOT / "examples" / f"{name}.json").read_text(encoding="utf-8"))


def mutated(scorer, fixtures, balanced, fid, **changes):
    rows = copy.deepcopy(balanced)
    for row in rows:
        if row["id"] == fid:
            row.update(changes)
    return scorer.score(fixtures, rows)


def main() -> int:
    score_path = ROOT / "score.py"
    require(score_path.is_file(), f"missing did-it-land trigger-and-scope scorer: {score_path}")
    spec = importlib.util.spec_from_file_location("did_it_land_scope", score_path)
    scorer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scorer)
    fixtures = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))
    require([f["id"] for f in fixtures] == [
        "deploy-fix-called-done-landed", "merge-believed-applied-landed",
        "config-edit-runtime-loads-cache", "green-check-source-only-oracle",
        "artifact-distributed-to-consumer-landed", "guard-hook-installed-and-firing",
        "observed-effect-reverted-by-reconciler", "runtime-unreachable-unverified",
        "partial-coverage-one-of-three-consumers", "nofire-local-reversible-preview-edit",
        "nofire-nothing-depends-yet", "nofire-still-deciding-what-to-change",
        "nofire-health-state-question",
    ], "did-it-land fixture inventory drifted")
    require(len({f["id"] for f in fixtures}) == len(fixtures), "fixture ids not unique")
    require(all(f["expected_action"] in scorer.ACTIONS for f in fixtures), "fixture expected_action outside the action vocabulary")
    require(all("expected_verdict" in f for f in fixtures if f["expected_action"] == "verify-landing"),
            "every verify-landing fixture must carry expected_verdict")
    require([f["id"] for f in fixtures if f["holdout"]] == [
        "config-edit-runtime-loads-cache", "observed-effect-reverted-by-reconciler",
        "nofire-still-deciding-what-to-change",
    ], "did-it-land holdout set drifted — exactly 3 holdouts, spread across fire and no-fire")

    balanced = load("balanced")
    report = scorer.score(fixtures, balanced)
    require(report["pass"], report["failures"])
    require(report["actions"] == {"verify-landing": 9, "no-fire": 4}, report["actions"])

    for name in ("overfiring", "underfiring", "parody"):
        report = scorer.score(fixtures, load(name))
        require(not report["pass"], f"{name} example unexpectedly passed")
    over = scorer.score(fixtures, load("overfiring"))
    require(sum("expected no-fire" in failure for failure in over["failures"]) == 4, over["failures"])
    under = scorer.score(fixtures, load("underfiring"))
    require(sum("expected verify-landing, got no-fire" in failure for failure in under["failures"]) == 9, under["failures"])
    parody = scorer.score(fixtures, load("parody"))
    require(sum("expected no-fire" in failure for failure in parody["failures"]) == 4, parody["failures"])
    require(any("LANDED requires consumer_observation nonempty" in failure for failure in parody["failures"]), parody["failures"])
    require(any("source-only evidence requires verdict UNVERIFIED" in failure for failure in parody["failures"]), parody["failures"])
    require(any("expected verdict REVERTED, got LANDED" in failure for failure in parody["failures"]), parody["failures"])
    require(any("records of intent, not observations of effect" in failure for failure in parody["failures"]), parody["failures"])

    # Named verdict rules, exercised as mutations of the balanced example.
    source_only_landed = mutated(scorer, fixtures, balanced, "green-check-source-only-oracle",
                                 verdict="LANDED",
                                 consumer_observation="the running system was asked and answered")
    require(any("source-only evidence requires verdict UNVERIFIED" in failure for failure in source_only_landed["failures"]), source_only_landed["failures"])
    unreachable_landed = mutated(scorer, fixtures, balanced, "runtime-unreachable-unverified",
                                 verdict="LANDED",
                                 consumer_observation="the running system was asked and answered")
    require(any("runtime unreachable requires verdict UNVERIFIED" in failure for failure in unreachable_landed["failures"]), unreachable_landed["failures"])
    partial_landed = mutated(scorer, fixtures, balanced, "partial-coverage-one-of-three-consumers", verdict="LANDED")
    require(any("partial coverage requires verdict UNVERIFIED" in failure for failure in partial_landed["failures"]), partial_landed["failures"])
    # Regression (2026-10-25, Codex finding on PR #281): the verdict checks
    # above left consumer_observation unconstrained on the two fixtures
    # where no runtime observation exists - an UNVERIFIED row carrying an
    # invented observation passed. The README contract already required
    # null there; the scorer now enforces it.
    invented_unreachable = mutated(scorer, fixtures, balanced, "runtime-unreachable-unverified",
                                   consumer_observation="the gateway answered its alarm-status query and the new alarm behaviour is active")
    require(any("runtime unreachable requires consumer_observation null" in failure for failure in invented_unreachable["failures"]), invented_unreachable["failures"])
    invented_source_only = mutated(scorer, fixtures, balanced, "green-check-source-only-oracle",
                                   consumer_observation="the running service was queried and reports the new flag enabled")
    require(any("source-only evidence requires consumer_observation null" in failure for failure in invented_source_only["failures"]), invented_source_only["failures"])
    # Regression (2026-10-25, C16 tightening): the null rule is literal -
    # an empty or whitespace-only string is a present non-null value and
    # fails, and so does any non-string value (which additionally trips the
    # generic string-or-null type check). Only literal null or an absent
    # key satisfies the rule on these two fixtures.
    for bad_observation in ("", " ", 0, False, {}, []):
        for fid, needle in (
            ("runtime-unreachable-unverified", "runtime unreachable requires consumer_observation null"),
            ("green-check-source-only-oracle", "source-only evidence requires consumer_observation null"),
        ):
            tightened = mutated(scorer, fixtures, balanced, fid, consumer_observation=bad_observation)
            require(any(needle in failure for failure in tightened["failures"]),
                    (fid, bad_observation, tightened["failures"]))
    absent_key = copy.deepcopy(balanced)
    for row in absent_key:
        if row["id"] in ("runtime-unreachable-unverified", "green-check-source-only-oracle"):
            row.pop("consumer_observation", None)
    require(scorer.score(fixtures, absent_key)["pass"],
            "an absent consumer_observation key must satisfy the null rule")
    # Control: the null rule is flag-scoped, not a blanket UNVERIFIED rule -
    # partial coverage and the cache fixture legitimately name the
    # observation actually made (the balanced set already carries both and
    # must keep passing, asserted at the top of this suite).
    reverted_unobserved = mutated(scorer, fixtures, balanced, "observed-effect-reverted-by-reconciler", persistence="unverified")
    require(any("requires persistence observed" in failure for failure in reverted_unobserved["failures"]), reverted_unobserved["failures"])
    landed_no_observation = mutated(scorer, fixtures, balanced, "deploy-fix-called-done-landed", consumer_observation=None)
    require(any("LANDED requires consumer_observation nonempty" in failure for failure in landed_no_observation["failures"]), landed_no_observation["failures"])
    # Regression (2026-10-24, Codex P2): REVERTED is evidence-bearing like
    # LANDED - a null consumer_observation must fail it too.
    reverted_no_observation = mutated(scorer, fixtures, balanced, "observed-effect-reverted-by-reconciler", consumer_observation=None)
    require(any("REVERTED requires consumer_observation nonempty" in failure for failure in reverted_no_observation["failures"]), reverted_no_observation["failures"])
    # Regression (2026-10-24, Codex P2): a response whose id is outside the
    # fixture inventory must fail, never be silently ignored.
    extra_rows = copy.deepcopy(balanced) + [{"id": "nonexistent-trial", "action": "garbage"}]
    extra_report = scorer.score(fixtures, extra_rows)
    require(not extra_report["pass"], "an extra response with an unknown id unexpectedly passed")
    require(any("not in the fixture inventory" in failure for failure in extra_report["failures"]), extra_report["failures"])
    noisy_negative = mutated(scorer, fixtures, balanced, "nofire-nothing-depends-yet", verdict="LANDED")
    require(any("no-fire must be silent" in failure for failure in noisy_negative["failures"]), noisy_negative["failures"])

    # Malformed input fails closed with named failures, never a traceback.
    top_level = scorer.score(fixtures, True)
    require(not top_level["pass"], "non-list responses unexpectedly passed")
    require(any("responses must be an array" in failure for failure in top_level["failures"]), top_level["failures"])
    unknown = scorer.score(fixtures, [{"id": "deploy-fix-called-done-landed", "action": "certify-landed"}])
    require(any("unknown action 'certify-landed'" in failure for failure in unknown["failures"]), unknown["failures"])
    duplicated = scorer.score(fixtures, [
        {"id": "nofire-nothing-depends-yet", "action": "no-fire"},
        {"id": "nofire-nothing-depends-yet", "action": "no-fire"},
    ])
    require(any("response ids missing or duplicated" in failure for failure in duplicated["failures"]), duplicated["failures"])
    nonstring_action = scorer.score(fixtures, [{"id": "nofire-nothing-depends-yet", "action": ["no-fire"]}])
    require(any("action must be a string" in failure for failure in nonstring_action["failures"]), nonstring_action["failures"])
    nonstring_id = scorer.score(fixtures, [{"id": ["nofire-nothing-depends-yet"], "action": "no-fire"}])
    require(any("response ids missing or duplicated" in failure for failure in nonstring_id["failures"]), nonstring_id["failures"])
    bad_verdict = scorer.score(fixtures, [{
        "id": "deploy-fix-called-done-landed", "action": "verify-landing",
        "verdict": ["LANDED"], "artifact_resolved": "the deployed image",
        "consumer_observation": "observed at the runtime", "persistence": "observed",
    }])
    require(any("verdict must be one of" in failure for failure in bad_verdict["failures"]), bad_verdict["failures"])
    bad_observation = scorer.score(fixtures, [{
        "id": "deploy-fix-called-done-landed", "action": "verify-landing",
        "verdict": "LANDED", "artifact_resolved": "the deployed image",
        "consumer_observation": {"status": 200}, "persistence": "observed",
    }])
    require(any("consumer_observation must be a string or null" in failure for failure in bad_observation["failures"]), bad_observation["failures"])


    # Regression (2026-10-24, Codex P2): an "explanation" field on a no-fire
    # row is a silence breach - the scorer must reject any key beyond id and
    # action on no-fire rows, not only the battery's enumerated fields.
    explained = json.loads((ROOT / "examples" / "balanced.json").read_text(encoding="utf-8"))
    for row in explained:
        if isinstance(row, dict) and row.get("action") == "no-fire":
            row["explanation"] = "No applicable trigger; staying silent."
    explained_report = scorer.score(fixtures, explained)
    require(not explained_report["pass"], "no-fire rows carrying an explanation field unexpectedly passed")
    require(any("no-fire must be silent" in failure for failure in explained_report["failures"]), explained_report["failures"])

    print("did-it-land trigger-and-scope: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
