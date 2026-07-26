#!/usr/bin/env python3
"""Fail-closed, non-promotable structural view of excluded V3 arm evidence."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
FIXTURES_ROOT = ROOT / "fixtures"
TRANSPORT_SCHEMA = ROOT / "formal-rigor-fixture-transport.schema.json"
NON_RELEASE_FIELDS = {
    "post_hoc": True,
    "source_epoch_excluded": True,
    "release_eligible": False,
    "release_credit": "none",
}
UNAVAILABLE_PARODY_ARMS = (
    "parody-always-decide",
    "parody-full-ceremony",
    "parody-jargon-only",
)


def _load_sibling(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


score = _load_sibling("score")
run_live = _load_sibling("run_live")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        file_hash = hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii")
        digest.update(relative + b"\0" + file_hash + b"\n")
    return digest.hexdigest()


def _byte_offset(text: str, character_offset: int) -> int:
    return len(text[:character_offset].encode("utf-8"))


def extract_identical_frames(raw: bytes, fixture: str, schema: dict) -> tuple[bytes, dict]:
    """Return one byte-identical frame only from an unambiguous repeated stream."""
    if not raw:
        raise ValueError("empty response cannot contain repeated frames")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("response is not UTF-8") from exc
    decoder = json.JSONDecoder()
    index = 0
    frames: list[bytes] = []
    while True:
        while index < len(text) and text[index].isspace():
            index += 1
        if index == len(text):
            break
        start = index
        try:
            value, index = decoder.raw_decode(text, index)
        except json.JSONDecodeError as exc:
            raise ValueError("response has a non-JSON prefix, suffix, or frame") from exc
        frame = raw[_byte_offset(text, start):_byte_offset(text, index)]
        if not frame:
            raise ValueError("response contains an empty frame")
        errors = run_live.validate_json_schema(value, schema)
        if errors:
            raise ValueError(f"frame violates transport schema: {errors}")
        if not isinstance(value, dict) or value.get("response") != "formal-rigor-fixture-response@1":
            raise ValueError("frame response marker does not match frozen transport")
        if value.get("fixture") != fixture:
            raise ValueError("frame fixture identity does not match coordinate")
        frames.append(frame)
    if len(frames) < 2:
        raise ValueError("repeated-frame normalization requires at least two frames")
    if any(frame != frames[0] for frame in frames[1:]):
        raise ValueError("repeated frames are not byte-identical")
    return frames[0], {
        "normalization": "normalized_identical_repeated_frames",
        "frame_count": len(frames),
        "raw_sha256": sha256_bytes(raw),
        "frame_sha256": sha256_bytes(frames[0]),
        "all_frames_byte_identical": True,
    }


def _read_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is unreadable: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return value


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _ensure_expected_identity(call: dict, task: dict, campaign: dict) -> None:
    expected = {
        "schema": "formal-rigor-live-call@1",
        "kind": "arm",
        "provider_plan": campaign.get("provider_plan"),
        "source_commit": campaign.get("source_commit"),
        "arm": task["arm"],
        "repetition": task["repetition"],
        "fixture": task["fixture"],
        "phase": "arms",
        "model": task.get("model"),
        "reasoning_effort": task.get("effort"),
    }
    if campaign.get("schema") == "formal-rigor-live-campaign-plan@2":
        expected.update({
            "preflight_sha256": campaign.get("preflight_sha256"),
            "campaign_plan_sha256": sha256_bytes(_canonical_json_bytes(campaign)),
        })
    for field, value in expected.items():
        if call.get(field) != value:
            raise ValueError(f"call identity {field!r} does not match campaign task")
    if call.get("secret_screen", {}).get("passed") is not True:
        raise ValueError("call secret screen did not pass")


def _ensure_qualifying_call(call: dict) -> None:
    if call.get("json_parseable") is not True or call.get("schema_valid") is not True:
        raise ValueError("single-frame call is not parseable and schema-valid")


def _ensure_completed_transport(call: dict) -> None:
    if call.get("transport") != "completed":
        raise ValueError("content-bearing call transport did not complete")


def _relative(source_root: Path, path: Path) -> str:
    return path.relative_to(source_root).as_posix()


def inventory_source_calls(source_root: Path, expected_pin: str) -> list[dict]:
    """Read every planned arm call without writing any derived artifact."""
    source_root = Path(source_root)
    if not source_root.is_dir():
        raise ValueError("source root is missing")
    if tree_sha256(source_root) != expected_pin:
        raise ValueError("source root content pin does not match")
    campaign = _read_json(source_root / "campaign-plan.json", "campaign plan")
    if campaign.get("schema") != "formal-rigor-live-campaign-plan@2":
        raise ValueError("diagnostic requires a V3 campaign plan")
    tasks = campaign.get("arm_tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("campaign arm_tasks is missing or empty")
    schema = _read_json(TRANSPORT_SCHEMA, "frozen transport schema")
    known_fixtures = score.load_inventory(FIXTURES_ROOT)
    rows: list[dict] = []
    coordinates: set[tuple[str, int, str]] = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("campaign arm task is not an object")
        arm, repetition, fixture = task.get("arm"), task.get("repetition"), task.get("fixture")
        if not isinstance(arm, str) or not isinstance(repetition, int) or not isinstance(fixture, str):
            raise ValueError("campaign arm task has invalid coordinate")
        if fixture not in known_fixtures:
            raise ValueError(f"campaign names an unknown fixture: {fixture}")
        coordinate = (arm, repetition, fixture)
        if coordinate in coordinates:
            raise ValueError("campaign arm task coordinate is duplicated")
        coordinates.add(coordinate)
        call_dir = source_root / "arms" / arm / f"run-{repetition}" / "calls" / fixture
        call_path = call_dir / "call.json"
        raw_path = call_dir / "response.json"
        row: dict[str, Any] = {
            "arm": arm,
            "repetition": repetition,
            "fixture": fixture,
            "origin_harness": task.get("harness"),
            "origin_provider": None,
            "source_call": _relative(source_root, call_path),
            "source_raw": _relative(source_root, raw_path),
            "view": f"views/{arm}/run-{repetition}/{fixture}.response.json",
            "call_sha256": None,
            "raw_sha256": None,
            "view_sha256": None,
            "normalization": None,
            "normalization_proof": None,
            "exclusion_reason": None,
        }
        if not call_path.is_file() and not raw_path.is_file():
            row.update(classification="missing_no_content", exclusion_reason="no terminal call or response artifact")
            rows.append(row)
            continue
        if not call_path.is_file():
            raise ValueError(f"response exists without call evidence: {raw_path}")
        call = _read_json(call_path, "call evidence")
        row["call_sha256"] = sha256_bytes(call_path.read_bytes())
        row["origin_harness"] = call.get("harness", row["origin_harness"])
        row["origin_provider"] = call.get("provider")
        _ensure_expected_identity(call, task, campaign)
        if not raw_path.is_file() or raw_path.read_bytes() == b"":
            row.update(classification="missing_no_content", exclusion_reason="terminal call retained no model content")
            rows.append(row)
            continue
        _ensure_completed_transport(call)
        raw = raw_path.read_bytes()
        row["raw_sha256"] = sha256_bytes(raw)
        if call.get("response_sha256") != row["raw_sha256"]:
            raise ValueError(f"response hash does not match terminal call: {raw_path}")
        try:
            response = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            response = None
        if response is not None:
            _ensure_qualifying_call(call)
            errors = run_live.validate_json_schema(response, schema)
            if errors or not isinstance(response, dict) or response.get("response") != "formal-rigor-fixture-response@1" or response.get("fixture") != fixture:
                raise ValueError(f"original response is not a valid matching transport frame: {raw_path}")
            row.update(
                classification="original_qualifying",
                normalization="original_qualifying",
                normalization_proof={"raw_sha256": row["raw_sha256"], "frame_count": 1},
            )
        else:
            frame, proof = extract_identical_frames(raw, fixture, schema)
            row.update(
                classification="normalized_identical_repeated_frames",
                normalization=proof["normalization"],
                normalization_proof=proof,
                _view_bytes=frame,
            )
        rows.append(row)
    return rows


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _counts(rows: list[dict]) -> dict[str, int]:
    content = [row for row in rows if row["classification"] != "missing_no_content"]
    scores = [row for row in content if isinstance(row.get("structural_score"), dict)]
    return {
        "planned": len(rows),
        "content_bearing": len(content),
        "normalized": sum(row["classification"] == "normalized_identical_repeated_frames" for row in rows),
        "structurally_scorable": len(scores),
        "structurally_passing": sum(score["structural_pass"] for score in (row["structural_score"] for row in scores)),
        "missing_no_content": sum(row["classification"] == "missing_no_content" for row in rows),
    }


def _group_counts(rows: list[dict], fields: tuple[str, ...]) -> dict[str, dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        label = "|".join(str(row.get(field)) for field in fields)
        groups[label].append(row)
    return {label: _counts(groups[label]) for label in sorted(groups)}


def _structural_report(rows: list[dict], source_pin: str, source_commit: str) -> dict:
    truth = score.load_inventory(FIXTURES_ROOT)
    enriched = []
    for row in rows:
        copied = dict(row)
        fixture_truth = truth.get(row["fixture"])
        copied["priority"] = fixture_truth.get("priority") if fixture_truth else None
        copied["fixture_kind"] = fixture_truth.get("kind") if fixture_truth else None
        enriched.append(copied)
    candidate = [row for row in enriched if row["arm"] == "v2-candidate"]
    candidate_available = [row for row in candidate if row["classification"] != "missing_no_content"]
    candidate_without_normalized = [row for row in candidate_available if row["classification"] == "original_qualifying"]
    parody_rows = [
        row for row in enriched
        if str(row["arm"]).startswith("parody-")
        and row["classification"] != "missing_no_content"
    ]
    observed_parodies = {}
    for arm in sorted({row["arm"] for row in parody_rows}):
        arm_rows = [row for row in parody_rows if row["arm"] == arm]
        observed_parodies[arm] = {
            **_counts(arm_rows),
            "intended_failure_evidence": [
                {"fixture": row["fixture"], "dimensions_failed": row["structural_score"].get("dimensions_failed", [])}
                for row in arm_rows if isinstance(row.get("structural_score"), dict)
                and not row["structural_score"].get("structural_pass")
            ],
        }
    candidate_gates = {}
    for label, selector in {
        "P0": lambda row: row.get("priority") == "P0",
        "trap": lambda row: row.get("fixture_kind") == "trap",
        "control": lambda row: row.get("fixture_kind") == "control",
    }.items():
        chosen = [row for row in candidate_available if selector(row)]
        candidate_gates[label] = _counts(chosen)
    return {
        "schema": "formal-rigor-posthoc-structural-report@1",
        **NON_RELEASE_FIELDS,
        "source_tree_sha256": source_pin,
        "source_commit": source_commit,
        "conditional_on_content": _counts([row for row in enriched if row["classification"] != "missing_no_content"]),
        "intent_to_test": _counts(enriched),
        "candidate_sensitivity_excluding_normalized": _counts(candidate_without_normalized),
        "candidate_available": _counts(candidate_available),
        "candidate_gate_components": candidate_gates,
        "by_arm": _group_counts(enriched, ("arm",)),
        "by_repetition": _group_counts(enriched, ("repetition",)),
        "by_fixture": _group_counts(enriched, ("fixture",)),
        "by_origin_provider": _group_counts(enriched, ("origin_provider",)),
        "by_priority": _group_counts(enriched, ("priority",)),
        "by_fixture_kind": _group_counts(enriched, ("fixture_kind",)),
        "observed_parody_failure_evidence": observed_parodies,
        "unavailable_parody_arms": list(UNAVAILABLE_PARODY_ARMS),
    }


def prepare_structural(source_root: Path, output_root: Path, expected_pin: str, source_commit: str) -> dict:
    """Create the diagnostic-only structural view after all source checks succeed."""
    source_root, output_root = Path(source_root), Path(output_root)
    if not source_root.is_dir():
        raise ValueError("source root is missing")
    source_resolved, output_resolved = source_root.resolve(), output_root.resolve()
    if output_resolved == source_resolved or output_resolved.is_relative_to(source_resolved):
        raise ValueError("diagnostic output must not be nested inside the source root")
    if output_root.exists() and any(output_root.iterdir()):
        raise ValueError("diagnostic output root must be new or empty")
    rows = inventory_source_calls(source_root, expected_pin)
    campaign = _read_json(source_root / "campaign-plan.json", "campaign plan")
    if campaign.get("source_commit") != source_commit:
        raise ValueError("requested source commit does not match campaign plan")
    if tree_sha256(source_root) != expected_pin:
        raise ValueError("source root changed during inventory")
    truth = score.load_inventory(FIXTURES_ROOT)
    output_root.mkdir(parents=True, exist_ok=True)
    for row in rows:
        if row["classification"] == "missing_no_content":
            continue
        raw_path = source_root / row["source_raw"]
        view_bytes = row.pop("_view_bytes", raw_path.read_bytes())
        view_path = output_root / row["view"]
        view_path.parent.mkdir(parents=True, exist_ok=True)
        view_path.write_bytes(view_bytes)
        row["view_sha256"] = sha256_bytes(view_bytes)
        response = json.loads(view_bytes.decode("utf-8"))
        if row["fixture"] not in truth:
            raise ValueError(f"unknown fixture in campaign: {row['fixture']}")
        row["structural_score"] = score.score_fixture(truth[row["fixture"]], response)
        score_path = output_root / "scores" / row["arm"] / f"run-{row['repetition']}" / f"{row['fixture']}.score.json"
        _write_json(score_path, {**NON_RELEASE_FIELDS, "source_coordinate": row["source_raw"], "score": row["structural_score"]})
    manifest = {
        "schema": "formal-rigor-posthoc-diagnostic-manifest@1",
        **NON_RELEASE_FIELDS,
        "source_tree_sha256": expected_pin,
        "source_commit": source_commit,
        "planned_arm_calls": len(rows),
    }
    inventory = {"schema": "formal-rigor-posthoc-arm-inventory@1", **NON_RELEASE_FIELDS, "rows": rows}
    report = _structural_report(rows, expected_pin, source_commit)
    _write_json(output_root / "diagnostic-manifest.json", manifest)
    _write_json(output_root / "arm-inventory.json", inventory)
    _write_json(output_root / "structural-report.json", report)
    return {"manifest": manifest, "inventory": rows, "report": report}
