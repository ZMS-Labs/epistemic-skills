#!/usr/bin/env python3
"""Deterministic safety tests for the V3 post-hoc diagnostic."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "posthoc_diagnostic.py"
SPEC = importlib.util.spec_from_file_location("posthoc_diagnostic", MODULE_PATH)
assert SPEC and SPEC.loader
diagnostic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagnostic)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_raises(error: type[Exception], function, *args) -> None:
    try:
        function(*args)
    except error:
        return
    raise AssertionError(f"{function.__name__} did not raise {error.__name__}")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def transport_frame(fixture: str, *, marker: str = "formal-rigor-fixture-response@1") -> bytes:
    return json.dumps({
        "response": marker,
        "fixture": fixture,
        "invocation": "focused",
        "skip_reason": None,
        "claim_assessments": [],
        "focused_output": ["A bounded focused response."],
        "record": None,
    }, separators=(",", ":")).encode("utf-8")


def write_source(source: Path, raw: bytes, *, mutate_call=None) -> dict:
    fixture, arm, repetition = "tm-01-false-mvd", "neutral", 1
    campaign = {
        "schema": "formal-rigor-live-campaign-plan@2",
        "provider_plan": "noncursor-degraded-v3",
        "source_commit": "a" * 40,
        "preflight_sha256": "b" * 64,
        "arm_tasks": [{
            "arm": arm, "repetition": repetition, "fixture": fixture,
            "harness": "codex", "model": "gpt-5.6-sol", "effort": "medium",
        }],
    }
    (source / "campaign-plan.json").write_text(json.dumps(campaign), encoding="utf-8")
    call_dir = source / "arms" / arm / f"run-{repetition}" / "calls" / fixture
    call_dir.mkdir(parents=True)
    (call_dir / "response.json").write_bytes(raw)
    call = {
        "schema": "formal-rigor-live-call@1", "kind": "arm",
        "provider_plan": campaign["provider_plan"], "source_commit": campaign["source_commit"],
        "arm": arm, "repetition": repetition, "fixture": fixture,
        "phase": "arms", "model": "gpt-5.6-sol", "reasoning_effort": "medium",
        "preflight_sha256": campaign["preflight_sha256"],
        "campaign_plan_sha256": sha256(json.dumps(
            campaign, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8")),
        "transport": "completed", "json_parseable": True, "schema_valid": True,
        "secret_screen": {"passed": True, "markers": []},
        "response_sha256": sha256(raw),
    }
    if mutate_call:
        mutate_call(call)
    (call_dir / "call.json").write_text(json.dumps(call), encoding="utf-8")
    return campaign


def assert_prepare_rejects(source: Path, output: Path) -> None:
    require_raises(ValueError, diagnostic.prepare_structural, source, output,
                   diagnostic.tree_sha256(source), "a" * 40)
    require(not (output / "views").exists(), "rejection wrote a response view")


def main() -> int:
    transport_schema = json.loads((ROOT / "formal-rigor-fixture-transport.schema.json").read_text(encoding="utf-8"))
    canonical_frame = transport_frame("tm-01-false-mvd")
    semantically_equal_different_bytes = json.dumps(
        json.loads(canonical_frame), indent=2, sort_keys=True,
    ).encode("utf-8")
    divergent_value = json.loads(canonical_frame)
    divergent_value["focused_output"] = ["A different focused response."]
    divergent_frame = json.dumps(divergent_value, separators=(",", ":")).encode("utf-8")
    wrong_fixture_frame = transport_frame("tm-02-fixed-columns-not-4nf")
    wrong_marker_frame = transport_frame(
        "tm-01-false-mvd", marker="formal-rigor-semantic-adjudication@1",
    )

    view, meta = diagnostic.extract_identical_frames(
        canonical_frame + b"\n" + canonical_frame,
        "tm-01-false-mvd", transport_schema,
    )
    require(view == canonical_frame, "two identical frames changed bytes")
    require(meta["frame_count"] == 2, "frame count was not retained")
    require(meta["normalization"] == "normalized_identical_repeated_frames",
            "normalization identity drifted")

    for rejected in (
        canonical_frame + b" " + semantically_equal_different_bytes,
        canonical_frame + b"\n" + divergent_frame,
        b"prefix" + canonical_frame,
        canonical_frame + b"suffix",
        wrong_fixture_frame + b"\n" + wrong_fixture_frame,
        wrong_marker_frame + b"\n" + wrong_marker_frame,
    ):
        require_raises(ValueError, diagnostic.extract_identical_frames,
                       rejected, "tm-01-false-mvd", transport_schema)

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "source"
        source.mkdir()
        write_source(source, canonical_frame)

        assert_prepare_rejects(source, source / "nested-output")

        occupied = root / "occupied-output"
        occupied.mkdir()
        (occupied / "already-here").write_text("no", encoding="utf-8")
        assert_prepare_rejects(source, occupied)

        bad_hash = root / "bad-hash"
        bad_hash.mkdir()
        write_source(bad_hash, canonical_frame,
                     mutate_call=lambda call: call.update(response_sha256="0" * 64))
        assert_prepare_rejects(bad_hash, root / "bad-hash-output")

        bad_secret = root / "bad-secret"
        bad_secret.mkdir()
        write_source(bad_secret, canonical_frame,
                     mutate_call=lambda call: call.update(secret_screen={"passed": False, "markers": ["token"]}))
        assert_prepare_rejects(bad_secret, root / "bad-secret-output")

        bad_identity = root / "bad-identity"
        bad_identity.mkdir()
        write_source(bad_identity, canonical_frame,
                     mutate_call=lambda call: call.update(fixture="copied-fixture"))
        assert_prepare_rejects(bad_identity, root / "bad-identity-output")

        output = root / "output"
        report = diagnostic.prepare_structural(
            source, output, diagnostic.tree_sha256(source), "a" * 40,
        )
        view_path = output / "views" / "neutral" / "run-1" / "tm-01-false-mvd.response.json"
        require(view_path.read_bytes() == canonical_frame, "qualifying view changed source bytes")
        require(report["inventory"][0]["classification"] == "original_qualifying",
                "qualifying source classification drifted")

        repeated_source = root / "repeated-source"
        repeated_source.mkdir()
        write_source(
            repeated_source, canonical_frame + b"\n" + canonical_frame,
            mutate_call=lambda call: call.update(
                json_parseable=False, schema_valid=False,
                schema_errors=["$: response is not parseable JSON"],
            ),
        )
        repeated_report = diagnostic.prepare_structural(
            repeated_source, root / "repeated-output",
            diagnostic.tree_sha256(repeated_source), "a" * 40,
        )
        repeated_view = root / "repeated-output" / "views" / "neutral" / "run-1" / "tm-01-false-mvd.response.json"
        require(repeated_view.read_bytes() == canonical_frame,
                "repeated-frame source did not materialize a single preserved frame")
        require(repeated_report["inventory"][0]["classification"] == "normalized_identical_repeated_frames",
                "repeated-frame source did not receive the normalized classification")

        failed_repeated_source = root / "failed-repeated-source"
        failed_repeated_source.mkdir()
        write_source(
            failed_repeated_source, canonical_frame + b"\n" + canonical_frame,
            mutate_call=lambda call: call.update(
                transport="failed", json_parseable=False, schema_valid=False,
                schema_errors=["$: response is not parseable JSON"],
            ),
        )
        assert_prepare_rejects(failed_repeated_source, root / "failed-repeated-output")

        parody_report = diagnostic._structural_report([
            {
                "arm": "parody-always-cautious", "repetition": 1,
                "fixture": "tm-01-false-mvd", "origin_provider": "codex",
                "classification": "original_qualifying",
                "structural_score": {"structural_pass": False, "dimensions_failed": ["S1"]},
            },
            *[
                {
                    "arm": arm, "repetition": 1, "fixture": "tm-01-false-mvd",
                    "origin_provider": None, "classification": "missing_no_content",
                }
                for arm in diagnostic.UNAVAILABLE_PARODY_ARMS
            ],
        ], "d" * 64, "a" * 40)
        require(set(parody_report["observed_parody_failure_evidence"]) == {"parody-always-cautious"},
                "unavailable parody arms were reported as observed")
        require(parody_report["unavailable_parody_arms"] == list(diagnostic.UNAVAILABLE_PARODY_ARMS),
                "unavailable parody accounting drifted")

    print("formal-rigor post-hoc diagnostic: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
