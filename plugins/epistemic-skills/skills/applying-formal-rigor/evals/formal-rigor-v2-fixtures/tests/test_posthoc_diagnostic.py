#!/usr/bin/env python3
"""Deterministic safety tests for the V3 post-hoc diagnostic."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from collections import Counter
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "posthoc_diagnostic.py"
SPEC = importlib.util.spec_from_file_location("posthoc_diagnostic", MODULE_PATH)
assert SPEC and SPEC.loader
diagnostic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagnostic)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_raises(error: type[Exception], function, *args, **kwargs) -> None:
    try:
        function(*args, **kwargs)
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


def semantic_manifest() -> dict:
    rows = []
    for repetition, count in ((1, 22), (2, 21), (3, 22)):
        origin_harness = "agy" if repetition == 2 else "codex"
        for index in range(1, count + 1):
            fixture = f"fixture-{index:02d}"
            rows.append({
                "arm": "v2-candidate",
                "repetition": repetition,
                "fixture": fixture,
                "origin_harness": origin_harness,
                "origin_provider": diagnostic.run_live.HARNESS_PROVIDERS[origin_harness],
                "classification": "original_qualifying",
                "view": f"views/v2-candidate/run-{repetition}/{fixture}.response.json",
                "view_sha256": "d" * 64,
            })
    rows.append({
        "arm": "neutral", "repetition": 1, "fixture": "fixture-01",
        "origin_harness": "codex", "classification": "original_qualifying",
    })
    return {"schema": "formal-rigor-posthoc-arm-inventory@1", "rows": rows}


def test_semantic_seat_map_and_transport_contracts() -> None:
    tasks = diagnostic.semantic_tasks(semantic_manifest())
    counts = Counter(task["judge_harness"] for task in tasks)
    candidate_counts = Counter({
        repetition: len({
            task["fixture"] for task in tasks if task["repetition"] == repetition
        })
        for repetition in (1, 2, 3)
    })
    require(counts == {"codex": 42, "agy": 88}, f"seat map drifted: {counts}")
    require(candidate_counts == {1: 22, 2: 21, 3: 22},
            f"candidate availability drifted: {candidate_counts}")
    require(all(task["judge_harness"] != task["origin_harness"] for task in tasks),
            "cross-provider judge boundary failed")

    prompt = "SEALED SEMANTIC PROMPT"
    agy_argv = diagnostic.agy_semantic_command(
        agy="agy", model="gemini-3.1-pro-high", prompt=prompt, effort="high",
    )
    require(agy_argv == [
        "agy", "--sandbox", "--dangerously-skip-permissions", "--mode", "plan",
        "--add-dir", ".", "--model", "gemini-3.1-pro-high", "--effort", "high",
        "--output-format", "json", "--print-timeout", "10m", "--print", prompt,
    ], f"AGY semantic argv drifted: {agy_argv}")

    with tempfile.TemporaryDirectory() as temporary:
        packet = Path(temporary) / "packet"
        response = Path(temporary) / "response.json"
        schema = ROOT / "formal-rigor-semantic-adjudication.schema.json"
        codex_argv = diagnostic.run_live.codex_command(
            codex="codex.cmd", model="gpt-5.6-sol", packet_dir=packet,
            response_path=response, prompt="-", output_schema=schema, effort="high",
        )
        for required in (
            "--ephemeral", "--ignore-user-config", "--ignore-rules", "plugins", "apps",
            "--sandbox", "read-only", "--output-last-message", "--output-schema",
        ):
            require(required in codex_argv, f"Codex isolation flag missing: {required}")
        require(diagnostic.run_live.codex_prompt_transport(prompt) == ("-", prompt),
                "Codex prompt is not transported over stdin")

        fixture_dir = ROOT / "fixtures" / "tm-01-false-mvd"
        candidate = Path(temporary) / "candidate.json"
        candidate.write_bytes(transport_frame("tm-01-false-mvd"))
        truth = json.loads((fixture_dir / "ground-truth.json").read_text(encoding="utf-8"))
        diagnostic.run_live.build_adjudication_packet(packet, fixture_dir, candidate, truth)
        manifest = diagnostic.run_live.packet_manifest(packet)
        require(set(manifest) == {
            "scenario.md", "artifacts/facts.json", "candidate-response.json",
            "rubric.json", "formal-rigor-semantic-adjudication.schema.json",
        }, f"semantic packet file set drifted: {set(manifest)}")
        rubric = json.loads((packet / "rubric.json").read_text(encoding="utf-8"))
        require(set(rubric) == {"fixture", "claims"},
                f"semantic rubric leaked hidden metadata: {set(rubric)}")
        require(all(set(claim) == {"id", "proof_obligations", "forbidden_propositions"}
                    for claim in rubric["claims"]), "semantic rubric leaked claim metadata")
        manifest_text = "\n".join(manifest).lower()
        for forbidden in (
            "ground-truth.json", "threshold", "score.py", "posthoc_diagnostic.py",
            "seat-a", "seat-b", "other-response",
        ):
            require(forbidden not in manifest_text, f"semantic packet leaked {forbidden}")


def adjudication(*, verdict: str = "VALID") -> dict:
    return {
        "adjudication": "formal-rigor-semantic-adjudication@1",
        "fixture": "tm-01-false-mvd",
        "verdict": verdict,
        "obligations": [{
            "claim_id": "c1",
            "obligation": "paired attributes do not establish an independent-set MVD",
            "status": "SATISFIED" if verdict == "VALID" else "VIOLATED",
            "response_coordinates": ["$.claim_assessments[0]"],
            "reason": "The candidate addresses the required relation semantics.",
        }],
        "forbidden_propositions": [{
            "claim_id": "c1",
            "proposition": "fixed columns are inherently unindexable",
            "present": False,
            "response_coordinates": [],
            "reason": "The candidate does not make the forbidden claim.",
        }],
        "coverage_limits": [],
    }


def test_agy_aggregate_extraction_is_unambiguous_and_fail_closed() -> None:
    value = adjudication()
    direct = json.dumps(value, separators=(",", ":")).encode("utf-8")
    extracted, direct_meta = diagnostic.extract_agy_adjudication(
        direct, "tm-01-false-mvd",
    )
    require(json.loads(extracted) == value, "direct AGY adjudication changed value")
    require(direct_meta["json_coordinate"] == "$", "direct JSON coordinate drifted")
    require(direct_meta["extraction_method"] == "direct_json_object",
            "direct extraction method drifted")

    nested_value = {"result": [{"payload": value}], "timing_ms": 12}
    extracted, nested_meta = diagnostic.extract_agy_adjudication(
        json.dumps(nested_value).encode("utf-8"), "tm-01-false-mvd",
    )
    require(json.loads(extracted) == value, "nested AGY adjudication changed value")
    require(nested_meta["json_coordinate"] == "$.result[0].payload",
            f"nested JSON coordinate drifted: {nested_meta}")
    require(nested_meta["extraction_method"] == "recursively_contained_json_object",
            "nested extraction method drifted")

    encoded_value = {"result": {"message": json.dumps(value)}}
    extracted, encoded_meta = diagnostic.extract_agy_adjudication(
        json.dumps(encoded_value).encode("utf-8"), "tm-01-false-mvd",
    )
    require(json.loads(extracted) == value, "string-encoded AGY adjudication changed value")
    require(encoded_meta["json_coordinate"] == "$.result.message",
            f"string JSON coordinate drifted: {encoded_meta}")
    require(encoded_meta["extraction_method"] == "string_encoded_json_object",
            "string extraction method drifted")

    divergent = adjudication(verdict="INVALID")
    wrong_fixture = {**value, "fixture": "tm-02-fixed-columns-not-4nf"}
    wrong_marker = {**value, "adjudication": "wrong-marker"}
    schema_invalid = dict(value)
    schema_invalid.pop("coverage_limits")
    wrong_row_container = {**value, "obligations": "not-an-array"}
    duplicate_row = json.loads(json.dumps(value))
    duplicate_row["obligations"].append(dict(duplicate_row["obligations"][0]))
    contradictory_obligation = json.loads(json.dumps(value))
    contradictory_obligation["obligations"][0]["status"] = "VIOLATED"
    contradictory_forbidden = json.loads(json.dumps(value))
    contradictory_forbidden["forbidden_propositions"][0]["present"] = True

    try:
        diagnostic.extract_agy_adjudication(
            json.dumps(schema_invalid).encode("utf-8"), "tm-01-false-mvd",
        )
    except ValueError as exc:
        require(bool(getattr(exc, "schema_errors", [])),
                "AGY schema rejection did not retain schema errors")
    else:
        raise AssertionError("schema-invalid AGY adjudication was accepted")

    for rejected in (
        b'{"message":"no adjudication"}',
        json.dumps({"a": value, "b": value}).encode("utf-8"),
        json.dumps({"a": value, "b": divergent}).encode("utf-8"),
        json.dumps(wrong_fixture).encode("utf-8"),
        json.dumps(wrong_marker).encode("utf-8"),
        b"{not-json",
        json.dumps(schema_invalid).encode("utf-8"),
        json.dumps(wrong_row_container).encode("utf-8"),
        json.dumps(duplicate_row).encode("utf-8"),
        json.dumps(contradictory_obligation).encode("utf-8"),
        json.dumps(contradictory_forbidden).encode("utf-8"),
    ):
        require_raises(
            ValueError, diagnostic.extract_agy_adjudication,
            rejected, "tm-01-false-mvd",
        )


def write_semantic_output_root(output: Path) -> None:
    fixture_ids = sorted(diagnostic.score.load_inventory(diagnostic.FIXTURES_ROOT))
    rows = []
    for repetition in (1, 2, 3):
        for index, fixture in enumerate(fixture_ids):
            if repetition == 2 and index == len(fixture_ids) - 1:
                continue
            origin_harness = "agy" if repetition == 2 else "codex"
            view = f"views/v2-candidate/run-{repetition}/{fixture}.response.json"
            view_path = output / view
            view_path.parent.mkdir(parents=True, exist_ok=True)
            raw = transport_frame(fixture)
            view_path.write_bytes(raw)
            rows.append({
                "arm": "v2-candidate", "repetition": repetition, "fixture": fixture,
                "origin_harness": origin_harness,
                "origin_provider": diagnostic.run_live.HARNESS_PROVIDERS[origin_harness],
                "classification": "original_qualifying", "view": view,
                "view_sha256": sha256(raw),
            })
    diagnostic._write_json(output / "diagnostic-manifest.json", {
        "schema": "formal-rigor-posthoc-diagnostic-manifest@1",
        **diagnostic.NON_RELEASE_FIELDS,
        "source_coordinate": "C:/tmp/excluded-v3-source",
        "source_tree_sha256": "1" * 64,
        "source_commit": "2" * 40,
        "planned_arm_calls": 286,
    })
    diagnostic._write_json(output / "arm-inventory.json", {
        "schema": "formal-rigor-posthoc-arm-inventory@1",
        **diagnostic.NON_RELEASE_FIELDS,
        "rows": rows,
    })


def semantic_value_for_packet(packet: Path) -> dict:
    rubric = json.loads((packet / "rubric.json").read_text(encoding="utf-8"))
    return {
        "adjudication": "formal-rigor-semantic-adjudication@1",
        "fixture": rubric["fixture"],
        "verdict": "VALID",
        "obligations": [
            {
                "claim_id": claim["id"], "obligation": obligation,
                "status": "SATISFIED", "response_coordinates": ["$.record"],
                "reason": "The candidate response supplies the required proof.",
            }
            for claim in rubric["claims"]
            for obligation in claim["proof_obligations"]
        ],
        "forbidden_propositions": [
            {
                "claim_id": claim["id"], "proposition": proposition,
                "present": False, "response_coordinates": [],
                "reason": "The candidate response avoids the forbidden proposition.",
            }
            for claim in rubric["claims"]
            for proposition in claim["forbidden_propositions"]
        ],
        "coverage_limits": [],
    }


class FakeSemanticRunner:
    def __init__(self) -> None:
        self.calls: list[tuple[list[str], dict]] = []

    def __call__(self, argv: list[str], **kwargs):
        self.calls.append((argv, kwargs))
        require(kwargs["timeout"] == 720, "semantic subprocess timeout drifted")
        require(kwargs["check"] is False, "semantic subprocess enabled check=True")
        packet = Path(kwargs["cwd"])
        require(packet.is_dir(), "semantic subprocess cwd is not the isolated packet")
        value = semantic_value_for_packet(packet)
        if argv[0] == "codex.cmd":
            response_path = Path(argv[argv.index("--output-last-message") + 1])
            response_path.write_text(json.dumps(value), encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout=b'{"event":"complete"}\n', stderr=b"")
        require(argv[0] == "agy", f"unexpected fake executable: {argv[0]}")
        aggregate = {"result": {"message": json.dumps(value)}, "elapsed_ms": 1}
        return SimpleNamespace(
            returncode=0, stdout=json.dumps(aggregate).encode("utf-8"), stderr=b"",
        )


def test_semantic_preflight_freezes_exact_cli_versions_and_catalog() -> None:
    catalog = b"gemini-3.6-flash-medium\ngemini-3.1-pro-high\n"

    def fake_preflight(argv: list[str], **kwargs):
        require(kwargs["capture_output"] is True and kwargs["check"] is False,
                "semantic preflight subprocess policy drifted")
        outputs = {
            ("codex.cmd", "--version"): b"codex-cli 0.144.6\n",
            ("agy", "--version"): b"1.1.7\n",
            ("agy", "models"): catalog,
        }
        return SimpleNamespace(returncode=0, stdout=outputs[tuple(argv)], stderr=b"")

    receipt = diagnostic.semantic_preflight(
        {"codex": "codex.cmd", "agy": "agy"}, runner=fake_preflight,
    )
    require(receipt == {
        "codex": {"version": "codex-cli 0.144.6"},
        "agy": {
            "version": "1.1.7", "catalog_sha256": sha256(catalog),
            "selected_model": "gemini-3.1-pro-high",
        },
    }, f"semantic preflight receipt drifted: {receipt}")

    def wrong_codex(argv: list[str], **kwargs):
        result = fake_preflight(argv, **kwargs)
        if argv == ["codex.cmd", "--version"]:
            result.stdout = b"codex-cli 0.145.0\n"
        return result

    require_raises(
        ValueError, diagnostic.semantic_preflight,
        {"codex": "codex.cmd", "agy": "agy"}, runner=wrong_codex,
    )


def test_frozen_candidate_outcome_rule() -> None:
    require(diagnostic._semantic_outcome(["VALID", "VALID"], "P1") == "PASS",
            "unanimous VALID did not pass")
    require(diagnostic._semantic_outcome(["VALID", "INVALID"], "P1") == "FAIL",
            "INVALID did not fail")
    require(diagnostic._semantic_outcome(["VALID", "INCONCLUSIVE"], "P0") == "FAIL",
            "P0 inconclusive did not fail")
    require(diagnostic._semantic_outcome(
        ["VALID", "INCONCLUSIVE"], "P1",
    ) == "ARBITRATION_REQUIRED", "non-P0 disagreement invented an outcome")


def test_diagnostic_cli_exposes_three_bounded_commands() -> None:
    parser = diagnostic.build_parser()
    prepared = parser.parse_args([
        "prepare-structural", "--source-root", "source", "--output-root", "output",
        "--expected-pin", "a" * 64, "--source-commit", "b" * 40,
    ])
    require(prepared.command == "prepare-structural", "prepare command is unavailable")
    semantic = parser.parse_args([
        "run-semantic", "--output-root", "output", "--harness", "codex",
        "--implementation-commit", "c" * 40,
    ])
    require(semantic.command == "run-semantic", "semantic command is unavailable")
    summarized = parser.parse_args(["summarize", "--output-root", "output"])
    require(summarized.command == "summarize", "summary command is unavailable")


def test_semantic_plan_execution_and_summary_are_frozen_and_at_most_once() -> None:
    receipt = {
        "codex": {"version": "codex-cli 0.144.6"},
        "agy": {
            "version": "1.1.7", "catalog_sha256": "3" * 64,
            "selected_model": "gemini-3.1-pro-high",
        },
    }
    with tempfile.TemporaryDirectory() as temporary:
        output = Path(temporary) / "diagnostic"
        output.mkdir()
        write_semantic_output_root(output)
        fake = FakeSemanticRunner()
        common = {
            "output_root": output,
            "executables": {"codex": "codex.cmd", "agy": "agy"},
            "implementation_commit": "4" * 40,
            "preflight_receipt": receipt,
            "runner": fake,
            "source_verifier": lambda commit, **kwargs: None,
        }
        codex_result = diagnostic.run_semantic(harness="codex", **common)
        require(codex_result["executed"] == 42, f"Codex execution count drifted: {codex_result}")
        plan = json.loads((output / "semantic-plan.json").read_text(encoding="utf-8"))
        require(len(plan["tasks"]) == 130, "semantic plan did not freeze all 130 seats")
        require(plan["timeout_policy"] == {
            "subprocess_seconds": 720, "agy_print_timeout": "10m",
            "retry_policy": "at-most-once",
        }, "semantic timeout policy drifted")
        require(plan["implementation_commit"] == "4" * 40,
                "semantic plan lost implementation commit")
        require(plan["source_coordinate"] == "C:/tmp/excluded-v3-source",
                "semantic plan lost source coordinate")
        require(plan["view_manifest_sha256"] == sha256((output / "arm-inventory.json").read_bytes()),
                "semantic plan lost view-manifest hash")

        agy_result = diagnostic.run_semantic(harness="agy", **common)
        require(agy_result["executed"] == 88, f"AGY execution count drifted: {agy_result}")
        require(len(fake.calls) == 130, "semantic fake did not observe every planned seat")
        call_paths = list((output / "semantic-diagnostic").rglob("call.json"))
        require(len(call_paths) == 130, "terminal semantic seal count drifted")
        for call_path in call_paths:
            call = json.loads(call_path.read_text(encoding="utf-8"))
            require(call["retry_policy"] == "at-most-once", "call retry policy drifted")
            require(call["transport"] == "completed", "fake semantic call did not complete")
            require(call["schema_valid"] is True and call["adjudication_valid"] is True,
                    "valid fake response was not accepted")
            require(call["secret_screen"]["passed"] is True, "secret screen did not pass")
            require((call_path.parent / "stdout.bin").is_file(), "stdout was not retained")
            require((call_path.parent / "stderr.bin").is_file(), "stderr was not retained")
            require((call_path.parent / "response.json").is_file(), "response was not retained")
        packet_root = output.parent / f"{output.name}-packets" / "semantic-diagnostic"
        require(not packet_root.exists() or not any(packet_root.iterdir()),
                "temporary semantic packets were retained")

        no_retry = FakeSemanticRunner()
        repeated = diagnostic.run_semantic(harness="agy", **{**common, "runner": no_retry})
        require(repeated["executed"] == 0 and repeated["terminal"] == 88,
                f"terminal AGY calls were not treated at-most-once: {repeated}")
        require(not no_retry.calls, "at-most-once rerun invoked the provider")

        report = diagnostic.summarize_semantic_diagnostic(output)
        require(report["outcomes"] == {"PASS": 65}, f"semantic outcomes drifted: {report['outcomes']}")
        require(report["completion_coverage"] == {
            "planned_candidates": 66, "available_candidates": 65,
            "missing_candidates": 1, "planned_seats": 130,
            "terminal_seats": 130, "valid_seats": 130,
        }, f"semantic completion coverage drifted: {report['completion_coverage']}")
        require(len(report["missing_candidates"]) == 1,
                "missing 66th candidate was not reported separately")
        require(report["dissent"] == [], "unanimous fake verdicts created dissent")
        require(report["p0_findings"] == [], "unanimous fake verdicts created P0 findings")

        tampered_response = call_paths[0].parent / "response.json"
        original_response = tampered_response.read_bytes()
        changed_response = json.loads(original_response)
        changed_response["coverage_limits"] = ["tampered after terminal seal"]
        diagnostic._write_json(tampered_response, changed_response)
        tampered_report = diagnostic.summarize_semantic_diagnostic(output)
        require(any(
            error.get("error") == "response hash mismatch"
            for error in tampered_report["validation_errors"]
        ), "summary trusted a response changed after terminal sealing")
        tampered_response.write_bytes(original_response)

        forged_path = call_paths[0]
        forged = json.loads(forged_path.read_text(encoding="utf-8"))
        original_fixture = forged["fixture"]
        forged["fixture"] = "forged-coordinate"
        diagnostic._write_json(forged_path, forged)
        require_raises(ValueError, diagnostic.run_semantic, **{
            **common, "harness": forged["judge_harness"], "runner": FakeSemanticRunner(),
        })
        forged["fixture"] = original_fixture
        diagnostic._write_json(forged_path, forged)

        plan["timeout_policy"]["subprocess_seconds"] = 721
        diagnostic._write_json(output / "semantic-plan.json", plan)
        require_raises(ValueError, diagnostic.run_semantic, **{
            **common, "harness": "codex", "runner": FakeSemanticRunner(),
        })


def main() -> int:
    test_semantic_seat_map_and_transport_contracts()
    test_agy_aggregate_extraction_is_unambiguous_and_fail_closed()
    test_semantic_preflight_freezes_exact_cli_versions_and_catalog()
    test_frozen_candidate_outcome_rule()
    test_diagnostic_cli_exposes_three_bounded_commands()
    test_semantic_plan_execution_and_summary_are_frozen_and_at_most_once()
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
        require(report["manifest"]["source_coordinate"] == str(source.resolve()),
                "diagnostic manifest did not bind the source coordinate")

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
