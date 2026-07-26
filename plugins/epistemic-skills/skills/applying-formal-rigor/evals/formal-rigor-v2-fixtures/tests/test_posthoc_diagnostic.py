#!/usr/bin/env python3
"""Deterministic safety tests for the V3 post-hoc diagnostic."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
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
        "harness": "codex", "provider": diagnostic.run_live.HARNESS_PROVIDERS["codex"],
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


def write_semantic_output_root(
    output: Path, *, source_coordinate: str | None = None,
) -> None:
    if source_coordinate is None:
        source = output.parent / "excluded-v3-source"
        source.mkdir(exist_ok=True)
        source_coordinate = str(source.resolve())
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
        "source_coordinate": source_coordinate,
        "source_tree_sha256": diagnostic.tree_sha256(Path(source_coordinate)),
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


class MalformedOnceCodexRunner(FakeSemanticRunner):
    def __init__(self) -> None:
        super().__init__()
        self.malformed_written = False

    def __call__(self, argv: list[str], **kwargs):
        if argv[0] == "codex.cmd" and not self.malformed_written:
            self.calls.append((argv, kwargs))
            packet = Path(kwargs["cwd"])
            require(packet.is_dir(), "malformed Codex fake did not receive packet cwd")
            response_path = Path(argv[argv.index("--output-last-message") + 1])
            response_path.write_bytes(b"{malformed-codex-json")
            self.malformed_written = True
            return SimpleNamespace(returncode=0, stdout=b'{"event":"complete"}\n', stderr=b"")
        return super().__call__(argv, **kwargs)


class NonzeroOnceCodexRunner(FakeSemanticRunner):
    def __init__(self) -> None:
        super().__init__()
        self.nonzero_written = False

    def __call__(self, argv: list[str], **kwargs):
        if argv[0] == "codex.cmd" and not self.nonzero_written:
            self.calls.append((argv, kwargs))
            packet = Path(kwargs["cwd"])
            require(packet.is_dir(), "nonzero Codex fake did not receive packet cwd")
            response_path = Path(argv[argv.index("--output-last-message") + 1])
            response_path.write_bytes(json.dumps(
                semantic_value_for_packet(packet), separators=(",", ":"),
            ).encode("utf-8"))
            self.nonzero_written = True
            return SimpleNamespace(
                returncode=9, stdout=b'{"event":"failed"}\n', stderr=b"terminal failure",
            )
        return super().__call__(argv, **kwargs)


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
        require(plan["source_coordinate"] == str((output.parent / "excluded-v3-source").resolve()),
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

        sealed_call_path = call_paths[0]
        sealed_call = json.loads(sealed_call_path.read_text(encoding="utf-8"))
        for artifact_name in ("stdout.bin", "stderr.bin"):
            artifact_path = sealed_call_path.parent / artifact_name
            original_artifact = artifact_path.read_bytes()
            artifact_path.write_bytes(original_artifact + b"tampered")
            require_raises(ValueError, diagnostic.run_semantic, **{
                **common, "harness": sealed_call["judge_harness"],
                "runner": FakeSemanticRunner(),
            })
            require_raises(ValueError, diagnostic.summarize_semantic_diagnostic, output)
            artifact_path.write_bytes(original_artifact)

        for field in ("implementation_commit", "source_commit", "source_tree_sha256"):
            original_binding = sealed_call[field]
            sealed_call[field] = "f" * len(str(original_binding))
            diagnostic._write_json(sealed_call_path, sealed_call)
            require_raises(ValueError, diagnostic.run_semantic, **{
                **common, "harness": sealed_call["judge_harness"],
                "runner": FakeSemanticRunner(),
            })
            require_raises(ValueError, diagnostic.summarize_semantic_diagnostic, output)
            sealed_call[field] = original_binding
            diagnostic._write_json(sealed_call_path, sealed_call)

        tampered_response = call_paths[0].parent / "response.json"
        original_response = tampered_response.read_bytes()
        changed_response = json.loads(original_response)
        changed_response["coverage_limits"] = ["tampered after terminal seal"]
        diagnostic._write_json(tampered_response, changed_response)
        require_raises(ValueError, diagnostic.summarize_semantic_diagnostic, output)
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


def test_concurrent_semantic_contenders_have_one_exclusive_winner() -> None:
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
        tasks = diagnostic.semantic_tasks(json.loads(
            (output / "arm-inventory.json").read_text(encoding="utf-8")
        ))
        plan = diagnostic._semantic_plan(
            output_root=output, tasks=tasks,
            implementation_commit="4" * 40, preflight_receipt=receipt,
        )
        task = next(row for row in plan["tasks"] if row["judge_harness"] == "codex")
        plan_sha = sha256(json.dumps(
            plan, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8"))
        fake = FakeSemanticRunner()
        barrier = Barrier(2)
        original_exclusive_write = diagnostic._exclusive_write_json

        def synchronized_exclusive_write(path: Path, value: object) -> None:
            barrier.wait(timeout=5)
            original_exclusive_write(path, value)

        diagnostic._exclusive_write_json = synchronized_exclusive_write
        try:
            def contend():
                return diagnostic._execute_semantic_task(
                    output_root=output, task=task, plan=plan,
                    plan_sha256=plan_sha,
                    executables={"codex": "codex.cmd", "agy": "agy"},
                    runner=fake,
                    packet_root=Path(temporary) / "packets",
                )

            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(contend) for _ in range(2)]
                failures = []
                successes = []
                for future in futures:
                    try:
                        successes.append(future.result(timeout=10))
                    except Exception as exc:  # the losing reservation must fail closed
                        failures.append(exc)
        finally:
            diagnostic._exclusive_write_json = original_exclusive_write
        require(len(fake.calls) == 1, f"concurrent contenders invoked provider {len(fake.calls)} times")
        require(len(successes) == 1 and len(failures) == 1,
                f"concurrent reservation result drifted: successes={len(successes)} failures={failures}")
        call_path = diagnostic._task_call_path(output, task)
        require(call_path.is_file(), "winning contender did not seal call evidence")
        require((call_path.parent / "attempt.json").is_file(),
                "winning contender lost its exclusive reservation evidence")


def test_packet_root_rejects_every_source_overlap_before_writes() -> None:
    receipt = {
        "codex": {"version": "codex-cli 0.144.6"},
        "agy": {
            "version": "1.1.7", "catalog_sha256": "3" * 64,
            "selected_model": "gemini-3.1-pro-high",
        },
    }
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "excluded-source"
        source.mkdir()
        sentinel = source / "sentinel.bin"
        sentinel.write_bytes(b"immutable-source")
        source_before = diagnostic.tree_sha256(source)
        source_entries = sorted(path.relative_to(source).as_posix() for path in source.rglob("*"))
        overlapping_roots = (source, source / "packet-child", source.parent)
        for index, packet_root in enumerate(overlapping_roots):
            output = root / f"diagnostic-{index}"
            output.mkdir()
            write_semantic_output_root(output, source_coordinate=str(source.resolve()))
            fake = FakeSemanticRunner()
            require_raises(
                ValueError, diagnostic.run_semantic, output,
                harness="codex",
                executables={"codex": "codex.cmd", "agy": "agy"},
                implementation_commit="4" * 40,
                preflight_receipt=receipt,
                runner=fake,
                source_verifier=lambda commit, **kwargs: None,
                packet_root=packet_root,
            )
            require(not fake.calls, f"overlapping packet root reached provider: {packet_root}")
            require(diagnostic.tree_sha256(source) == source_before,
                    f"overlapping packet root changed source bytes: {packet_root}")
            require(sorted(path.relative_to(source).as_posix() for path in source.rglob("*"))
                    == source_entries, f"overlapping packet root changed source tree: {packet_root}")


def test_semantic_packet_cleanup_survives_provider_exception() -> None:
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
        tasks = diagnostic.semantic_tasks(json.loads(
            (output / "arm-inventory.json").read_text(encoding="utf-8")
        ))
        plan = diagnostic._semantic_plan(
            output_root=output, tasks=tasks,
            implementation_commit="4" * 40, preflight_receipt=receipt,
        )
        task = next(row for row in plan["tasks"] if row["judge_harness"] == "codex")
        plan_sha = sha256(json.dumps(
            plan, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        ).encode("utf-8"))
        packet_root = Path(temporary) / "exception-packets"
        observed_packets = []

        def failing_provider(argv: list[str], **kwargs):
            packet = Path(kwargs["cwd"])
            require(packet.is_dir(), "provider exception did not occur at real packet boundary")
            observed_packets.append(packet)
            raise RuntimeError("deterministic provider boundary failure")

        require_raises(
            RuntimeError, diagnostic._execute_semantic_task,
            output_root=output, task=task, plan=plan, plan_sha256=plan_sha,
            executables={"codex": "codex.cmd", "agy": "agy"},
            runner=failing_provider, packet_root=packet_root,
        )
        require(len(observed_packets) == 1, "failing provider boundary was not exercised")
        require(not observed_packets[0].exists(), "provider exception retained temporary packet")
        require(not packet_root.exists() or not any(packet_root.iterdir()),
                "provider exception left packet-root contents")


def test_malformed_codex_terminal_is_retained_and_summarized() -> None:
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
        runner = MalformedOnceCodexRunner()
        common = {
            "output_root": output,
            "executables": {"codex": "codex.cmd", "agy": "agy"},
            "implementation_commit": "4" * 40,
            "preflight_receipt": receipt,
            "source_verifier": lambda commit, **kwargs: None,
        }
        first = diagnostic.run_semantic(harness="codex", runner=runner, **common)
        require(first["executed"] == 42, "malformed Codex epoch did not terminally execute")
        call_paths = list((output / "semantic-diagnostic").rglob("call.json"))
        malformed_calls = [
            (path, json.loads(path.read_text(encoding="utf-8")))
            for path in call_paths
            if json.loads(path.read_text(encoding="utf-8")).get("parse_error")
        ]
        require(len(malformed_calls) == 1, "malformed Codex call was not retained exactly once")
        malformed_path, malformed_call = malformed_calls[0]
        require(malformed_call["transport"] == "completed",
                "malformed Codex terminal lost completed transport")
        require(malformed_call["json_parseable"] is False,
                "malformed Codex terminal was marked parseable")

        no_retry = FakeSemanticRunner()
        replay = diagnostic.run_semantic(harness="codex", runner=no_retry, **common)
        require(replay["executed"] == 0 and replay["terminal"] == 42,
                "malformed terminal call was not retained for at-most-once replay")
        require(not no_retry.calls, "malformed terminal call was retried")
        report = diagnostic.summarize_semantic_diagnostic(output)
        require(any(
            error["fixture"] == malformed_call["fixture"]
            and error["seat"] == malformed_call["seat"]
            and error["parse_error"]
            for error in report["validation_errors"]
        ), "summary did not classify malformed terminal validation errors")

        raw_path = malformed_path.parent / "raw-response.bin"
        require(raw_path.is_file(), "malformed Codex raw response was not retained")
        require(not (malformed_path.parent / "response.json").exists(),
                "malformed Codex response was promoted to parsed-valid response.json")
        original_raw = raw_path.read_bytes()
        raw_path.write_bytes(original_raw + b"tampered")
        require_raises(
            ValueError, diagnostic.run_semantic,
            harness="codex", runner=FakeSemanticRunner(), **common,
        )
        require_raises(ValueError, diagnostic.summarize_semantic_diagnostic, output)
        raw_path.write_bytes(original_raw)


def test_nonzero_codex_output_and_prompt_bytes_are_hash_bound() -> None:
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
        runner = NonzeroOnceCodexRunner()
        common = {
            "output_root": output,
            "executables": {"codex": "codex.cmd", "agy": "agy"},
            "implementation_commit": "4" * 40,
            "preflight_receipt": receipt,
            "source_verifier": lambda commit, **kwargs: None,
        }
        result = diagnostic.run_semantic(harness="codex", runner=runner, **common)
        require(result["executed"] == 42, "nonzero Codex epoch did not terminally execute")
        calls = [
            (path, json.loads(path.read_text(encoding="utf-8")))
            for path in (output / "semantic-diagnostic").rglob("call.json")
        ]
        nonzero = [(path, call) for path, call in calls if call.get("exit_code") == 9]
        require(len(nonzero) == 1, "nonzero Codex call was not retained exactly once")
        call_path, call = nonzero[0]
        raw_path = call_path.parent / "raw-response.bin"
        require(raw_path.is_file(), "nonzero Codex output-last-message bytes were discarded")
        require(call.get("raw_response_sha256") == sha256(raw_path.read_bytes()),
                "nonzero Codex output-last-message hash was not sealed")
        require(not (call_path.parent / "response.json").exists(),
                "nonzero Codex output was promoted to response.json")
        for sealed_path, sealed_call in calls:
            prompt_path = sealed_path.parent / "prompt.bin"
            require(prompt_path.is_file(),
                    f"semantic call did not retain raw prompt bytes: {sealed_path.parent}")
            require(sha256(prompt_path.read_bytes()) == sealed_call["prompt_sha256"],
                    f"semantic prompt bytes do not match the frozen hash: {sealed_path.parent}")

        original_prompt = call_path.parent.joinpath("prompt.bin").read_bytes()
        call_path.parent.joinpath("prompt.bin").write_bytes(original_prompt + b"tampered")
        require_raises(
            ValueError, diagnostic.run_semantic,
            harness="codex", runner=FakeSemanticRunner(), **common,
        )
        require_raises(ValueError, diagnostic.summarize_semantic_diagnostic, output)


def test_summary_and_replay_rederive_current_upstream_bindings() -> None:
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
        common = {
            "output_root": output,
            "executables": {"codex": "codex.cmd", "agy": "agy"},
            "implementation_commit": "4" * 40,
            "preflight_receipt": receipt,
            "source_verifier": lambda commit, **kwargs: None,
        }
        diagnostic.run_semantic(harness="codex", runner=FakeSemanticRunner(), **common)
        diagnostic.run_semantic(harness="agy", runner=FakeSemanticRunner(), **common)
        trusted_tampering = []
        tamper_cases = {
            "arm-inventory": output / "arm-inventory.json",
            "diagnostic-manifest": output / "diagnostic-manifest.json",
            "source-view": next((output / "views").rglob("*.response.json")),
        }
        for label, path in tamper_cases.items():
            original = path.read_bytes()
            if path.suffix == ".json" and path.name in {
                "arm-inventory.json", "diagnostic-manifest.json",
            }:
                changed = json.loads(original)
                changed["tampered_after_seal"] = True
                diagnostic._write_json(path, changed)
            else:
                path.write_bytes(original + b"\n")
            try:
                diagnostic.summarize_semantic_diagnostic(output)
            except ValueError:
                pass
            else:
                trusted_tampering.append(f"summary:{label}")
            try:
                diagnostic.run_semantic(
                    harness="codex", runner=FakeSemanticRunner(), **common,
                )
            except ValueError:
                pass
            else:
                trusted_tampering.append(f"replay:{label}")
            path.write_bytes(original)
        require(not trusted_tampering,
                f"summary/replay trusted tampered upstream bindings: {trusted_tampering}")


def test_inventory_rejects_provider_plan_and_origin_identity_contradictions() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        accepted = []
        for label in ("provider-plan", "task-call-harness", "harness-provider"):
            source = root / f"source-{label}"
            source.mkdir()
            write_source(source, transport_frame("tm-01-false-mvd"))
            campaign_path = source / "campaign-plan.json"
            campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
            call_path = next((source / "arms").rglob("call.json"))
            call = json.loads(call_path.read_text(encoding="utf-8"))
            if label == "provider-plan":
                campaign["provider_plan"] = "noncursor-degraded-v2"
                call["provider_plan"] = campaign["provider_plan"]
            elif label == "task-call-harness":
                call["harness"] = "agy"
                call["provider"] = diagnostic.run_live.HARNESS_PROVIDERS["agy"]
            else:
                call["provider"] = diagnostic.run_live.HARNESS_PROVIDERS["agy"]
            campaign_path.write_text(json.dumps(campaign), encoding="utf-8")
            call["campaign_plan_sha256"] = sha256(json.dumps(
                campaign, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            ).encode("utf-8"))
            call_path.write_text(json.dumps(call), encoding="utf-8")
            try:
                diagnostic.prepare_structural(
                    source, root / f"output-{label}",
                    diagnostic.tree_sha256(source), "a" * 40,
                )
            except ValueError:
                pass
            else:
                accepted.append(label)
        require(not accepted,
                f"inventory accepted contradictory provider identity: {accepted}")


def test_packet_source_and_output_roots_are_pairwise_disjoint_before_reservation() -> None:
    receipt = {
        "codex": {"version": "codex-cli 0.144.6"},
        "agy": {
            "version": "1.1.7", "catalog_sha256": "3" * 64,
            "selected_model": "gemini-3.1-pro-high",
        },
    }
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        accepted = []
        reserved = []
        cases = []
        for label in ("packet-output", "packet-output-child", "packet-output-ancestor"):
            output = root / label / "diagnostic" if label.endswith("ancestor") else root / label
            output.mkdir(parents=True)
            if label.endswith("ancestor"):
                external_source = root / "external-frozen-source"
                external_source.mkdir()
                write_semantic_output_root(
                    output, source_coordinate=str(external_source.resolve()),
                )
            else:
                write_semantic_output_root(output)
            packet_root = (
                output if label == "packet-output"
                else output / "packets" if label == "packet-output-child"
                else output.parent
            )
            cases.append((label, output, packet_root))

        output_child_source = root / "source-output-child"
        output_child_source.mkdir()
        source_child = output_child_source / "frozen-source"
        source_child.mkdir()
        write_semantic_output_root(
            output_child_source, source_coordinate=str(source_child.resolve()),
        )
        cases.append(("source-output-child", output_child_source, root / "packets-child"))

        source_ancestor = root / "source-output-ancestor"
        source_ancestor.mkdir()
        output_in_source = source_ancestor / "diagnostic"
        output_in_source.mkdir()
        write_semantic_output_root(
            output_in_source, source_coordinate=str(source_ancestor.resolve()),
        )
        cases.append(("source-output-ancestor", output_in_source, root / "packets-ancestor"))

        for label, output, packet_root in cases:
            fake = FakeSemanticRunner()
            try:
                diagnostic.run_semantic(
                    output, harness="codex",
                    executables={"codex": "codex.cmd", "agy": "agy"},
                    implementation_commit="4" * 40,
                    preflight_receipt=receipt, runner=fake,
                    source_verifier=lambda commit, **kwargs: None,
                    packet_root=packet_root,
                )
            except ValueError:
                pass
            else:
                accepted.append(label)
            if list((output / "semantic-diagnostic").rglob("attempt.json")):
                reserved.append(label)
        require(not accepted and not reserved,
                f"overlapping roots accepted={accepted}; reserved={reserved}")


def main() -> int:
    test_semantic_seat_map_and_transport_contracts()
    test_agy_aggregate_extraction_is_unambiguous_and_fail_closed()
    test_semantic_preflight_freezes_exact_cli_versions_and_catalog()
    test_frozen_candidate_outcome_rule()
    test_diagnostic_cli_exposes_three_bounded_commands()
    test_semantic_plan_execution_and_summary_are_frozen_and_at_most_once()
    test_concurrent_semantic_contenders_have_one_exclusive_winner()
    test_packet_root_rejects_every_source_overlap_before_writes()
    test_semantic_packet_cleanup_survives_provider_exception()
    test_malformed_codex_terminal_is_retained_and_summarized()
    test_nonzero_codex_output_and_prompt_bytes_are_hash_bound()
    test_summary_and_replay_rederive_current_upstream_bindings()
    test_inventory_rejects_provider_plan_and_origin_identity_contradictions()
    test_packet_source_and_output_roots_are_pairwise_disjoint_before_reservation()
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
