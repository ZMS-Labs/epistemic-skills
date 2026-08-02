"""Fail-closed validation and emission for portable epistemic records."""

import argparse
import datetime as datetime_module
import json
from pathlib import Path
from typing import Any


EVENT_RECORD = "epistemic-event@1"
OUTCOME_RECORD = "epistemic-outcome@1"
EVENT_KINDS = {
    "routing-decision", "pairing-decision", "landmine-prediction",
    "formal-prediction", "evidence-claim", "goal-proof",
    "handoff-verification", "review-forecast", "uat-verdict",
    "ledger-revisit", "continuity-reanchor",
}
OUTCOME_CLASSES = {
    "correct", "incorrect", "partial", "unresolved",
    "over-escalated", "under-escalated", "regressed",
}
RESOLUTION_RULES = {
    "deterministic-fixture", "independent-adjudication",
    "field-observation", "supersession-chain",
}
OBSERVATION_CLASSES = {
    "verified", "contradicted", "unverified", "superseded",
    "accepted", "rejected", "recurred", "avoided",
}
EVIDENCE_REF_KINDS = {
    "artifact-hash", "receipt-hash", "oracle-hash",
    "ledger-entry-hash", "run-record-hash",
}
SKILL_NAMES = {
    "using-epistemic-skills", "helix", "blindspot-pass",
    "applying-formal-rigor", "evidence-research", "write-goal",
    "outsource", "gauntlet", "evidence-locked-uat", "decision-ledger",
    "continuity-verify",
}
PROHIBITED_CONTENT_KEYS = {
    "prompt", "transcript", "user_prose", "raw_content", "secret",
    "private_path", "evidence_content", "session_id", "exact_model_id",
}
PROVENANCE_MODES = {"preregistered", "contemporaneous", "post_hoc"}
RESOLUTION_STATUSES = {"resolved", "partial", "unresolved", "superseded"}
VERIFICATION_METHODS = {
    "deterministic-oracle", "independent-human", "independent-model",
    "field-observation",
}
INDEPENDENCE_CLASSES = {
    "deterministic", "different-family", "same-family", "self-reported",
}
ELIGIBILITY_PREDICATES = {
    "evaluation-case", "sampled-field-incident", "preregistered-prediction",
    "independently-resolvable-verdict", "correction-or-supersession",
    "revisit-trigger-fired",
}
COLLECTION_MODES = {"calibratable", "observational", "conditional"}
SKILL_EVENT_MAP = {
    "using-epistemic-skills": {
        "event_kinds": ("routing-decision",),
        "eligible_when": ("evaluation-case", "sampled-field-incident"),
        "outcome_sources": ("independent-adjudication",),
        "collection_mode": "observational",
        "sentinel_fixture": "router-over-under.json",
    },
    "helix": {
        "event_kinds": ("pairing-decision",),
        "eligible_when": ("evaluation-case", "correction-or-supersession"),
        "outcome_sources": ("independent-adjudication",),
        "collection_mode": "observational",
        "sentinel_fixture": "helix-missed-pair.json",
    },
    "blindspot-pass": {
        "event_kinds": ("landmine-prediction",),
        "eligible_when": ("preregistered-prediction",),
        "outcome_sources": ("field-observation",),
        "collection_mode": "calibratable",
        "sentinel_fixture": "blindspot-landmine.json",
    },
    "applying-formal-rigor": {
        "event_kinds": ("formal-prediction",),
        "eligible_when": ("preregistered-prediction",),
        "outcome_sources": ("deterministic-fixture", "field-observation"),
        "collection_mode": "calibratable",
        "sentinel_fixture": "formal-prediction.json",
    },
    "evidence-research": {
        "event_kinds": ("evidence-claim",),
        "eligible_when": ("independently-resolvable-verdict",),
        "outcome_sources": ("independent-adjudication", "field-observation"),
        "collection_mode": "conditional",
        "sentinel_fixture": "evidence-correction.json",
    },
    "write-goal": {
        "event_kinds": ("goal-proof",),
        "eligible_when": ("independently-resolvable-verdict",),
        "outcome_sources": ("field-observation", "supersession-chain"),
        "collection_mode": "conditional",
        "sentinel_fixture": "goal-regression.json",
    },
    "outsource": {
        "event_kinds": ("handoff-verification",),
        "eligible_when": ("evaluation-case", "sampled-field-incident"),
        "outcome_sources": ("deterministic-fixture", "independent-adjudication"),
        "collection_mode": "observational",
        "sentinel_fixture": "outsource-relay.json",
    },
    "gauntlet": {
        "event_kinds": ("review-forecast",),
        "eligible_when": ("preregistered-prediction", "correction-or-supersession"),
        "outcome_sources": ("field-observation", "supersession-chain"),
        "collection_mode": "conditional",
        "sentinel_fixture": "gauntlet-dissent.json",
    },
    "evidence-locked-uat": {
        "event_kinds": ("uat-verdict",),
        "eligible_when": ("independently-resolvable-verdict",),
        "outcome_sources": ("deterministic-fixture", "field-observation"),
        "collection_mode": "calibratable",
        "sentinel_fixture": "uat-seeded-defect.json",
    },
    "decision-ledger": {
        "event_kinds": ("ledger-revisit",),
        "eligible_when": ("revisit-trigger-fired",),
        "outcome_sources": ("supersession-chain",),
        "collection_mode": "observational",
        "sentinel_fixture": "ledger-revisit.json",
    },
    "continuity-verify": {
        "event_kinds": ("continuity-reanchor",),
        "eligible_when": ("evaluation-case", "sampled-field-incident"),
        "outcome_sources": ("deterministic-fixture", "field-observation"),
        "collection_mode": "observational",
        "sentinel_fixture": "continuity-contradiction.json",
    },
}


class EventError(ValueError):
    """A named, safe-to-share rejection for an epistemic record."""

    def __init__(self, name: str, detail: str):
        self.name = name
        self.detail = detail
        super().__init__(f"{name}: {detail}")


def _schema_error(detail: str) -> None:
    raise EventError("SCHEMA_VIOLATION", detail)


def _is_hex(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(
        character in "0123456789abcdef" for character in value
    )


def _is_nonempty_string_or_none(value: Any) -> bool:
    return value is None or (isinstance(value, str) and bool(value))


def _is_date(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 10:
        return False
    try:
        return datetime_module.date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _require_mapping(record: Any, allowed_keys: set[str], required_keys: set[str], label: str) -> dict:
    if not isinstance(record, dict):
        _schema_error(f"{label} must be an object")
    unknown_keys = set(record) - allowed_keys
    missing_keys = required_keys - set(record)
    if unknown_keys:
        _schema_error(f"{label} contains unsupported keys")
    if missing_keys:
        _schema_error(f"{label} is missing required keys")
    return record


def _reject_prohibited_keys(value: Any) -> None:
    if isinstance(value, dict):
        prohibited = set(value) & PROHIBITED_CONTENT_KEYS
        if prohibited:
            raise EventError("PROHIBITED_CONTENT", "record contains a prohibited content key")
        for nested_value in value.values():
            _reject_prohibited_keys(nested_value)
    elif isinstance(value, list):
        for nested_value in value:
            _reject_prohibited_keys(nested_value)


def _verify_evidence_ref(value: Any, label: str, allow_none: bool = False) -> None:
    if value is None and allow_none:
        return
    evidence_ref = _require_mapping(value, {"kind", "sha256"}, {"kind", "sha256"}, label)
    if evidence_ref["kind"] not in EVIDENCE_REF_KINDS or not _is_hex(evidence_ref["sha256"]):
        _schema_error(f"{label} is invalid")


def load_skill_event_map(path: Path) -> dict:
    """Load and fail closed on the public skill-event eligibility map."""
    with path.open(encoding="utf-8") as handle:
        mapping = json.load(handle)
    verify_skill_event_map(mapping)
    return mapping


def verify_skill_event_map(mapping: dict) -> None:
    """Validate the closed eleven-surface collection eligibility map."""
    if not isinstance(mapping, dict) or set(mapping) != {"skills"}:
        _schema_error("skill event map must contain only skills")
    skills = mapping["skills"]
    if not isinstance(skills, list) or len(skills) != len(SKILL_EVENT_MAP):
        _schema_error("skill event map must contain every closed skill exactly once")
    seen_skills: set[str] = set()
    required_keys = {
        "skill", "event_kinds", "eligible_when", "outcome_sources",
        "collection_mode", "sentinel_fixture",
    }
    for entry in skills:
        if not isinstance(entry, dict) or set(entry) != required_keys:
            _schema_error("skill event map entry has unsupported keys")
        skill = entry["skill"]
        if skill not in SKILL_EVENT_MAP or skill in seen_skills:
            _schema_error("skill event map skill is not closed or is duplicated")
        seen_skills.add(skill)
        for field, vocabulary in (
            ("event_kinds", EVENT_KINDS),
            ("eligible_when", ELIGIBILITY_PREDICATES),
            ("outcome_sources", RESOLUTION_RULES),
        ):
            value = entry[field]
            if not isinstance(value, list) or not value or any(item not in vocabulary for item in value):
                _schema_error(f"skill event map {field} is invalid")
        if entry["collection_mode"] not in COLLECTION_MODES:
            _schema_error("skill event map collection mode is invalid")
        if not isinstance(entry["sentinel_fixture"], str) or not entry["sentinel_fixture"].endswith(".json"):
            _schema_error("skill event map sentinel fixture is invalid")
        expected = SKILL_EVENT_MAP[skill]
        if (
            tuple(entry["event_kinds"]) != expected["event_kinds"]
            or tuple(entry["eligible_when"]) != expected["eligible_when"]
            or tuple(entry["outcome_sources"]) != expected["outcome_sources"]
            or entry["collection_mode"] != expected["collection_mode"]
            or entry["sentinel_fixture"] != expected["sentinel_fixture"]
        ):
            _schema_error("skill event map entry does not match the closed eligibility contract")
    if seen_skills != set(SKILL_EVENT_MAP):
        _schema_error("skill event map does not cover every closed skill")


def _verify_event_producer(value: Any) -> None:
    producer = _require_mapping(
        value,
        {"skill", "skill_version", "producer_sha256"},
        {"skill", "skill_version", "producer_sha256"},
        "producer",
    )
    if producer["skill"] not in SKILL_NAMES:
        _schema_error("producer skill is not closed")
    if not isinstance(producer["skill_version"], str) or not producer["skill_version"]:
        _schema_error("producer skill_version is invalid")
    if not _is_hex(producer["producer_sha256"]):
        _schema_error("producer sha256 is invalid")


def verify_event(record: dict) -> None:
    """Validate a closed, content-minimized epistemic event in memory."""
    _reject_prohibited_keys(record)
    if not isinstance(record, dict):
        _schema_error("event must be an object")
    variant = record.get("variant")
    if variant == "observational" and (
        "forecast" in record
        or (isinstance(record.get("observation"), dict) and "probability" in record["observation"])
    ):
        raise EventError("ILLEGAL_EVENT_VARIANT", "observational events cannot carry probabilities")
    if variant == "calibratable" and "observation" in record:
        raise EventError("ILLEGAL_EVENT_VARIANT", "calibratable events cannot carry observations")
    common_keys = {
        "record", "variant", "event_id", "idempotency_key", "producer", "event_kind",
        "subject_ref", "correlation_ref", "occurred_on", "model_family", "harness_class",
        "provenance_mode", "privacy_class", "evidence_refs",
    }
    if variant == "calibratable":
        allowed_keys = common_keys | {"forecast"}
        required_keys = allowed_keys
    elif variant == "observational":
        allowed_keys = common_keys | {"observation"}
        required_keys = allowed_keys
    else:
        _schema_error("event variant is invalid")
    event = _require_mapping(record, allowed_keys, required_keys, "event")
    if event["record"] != EVENT_RECORD:
        _schema_error("event record discriminator is invalid")
    if not _is_hex(event["event_id"]) or not _is_hex(event["idempotency_key"]):
        _schema_error("event identifiers must be lowercase sha256 values")
    _verify_event_producer(event["producer"])
    if event["event_kind"] not in EVENT_KINDS:
        _schema_error("event kind is not closed")
    if not _is_hex(event["subject_ref"]) or not _is_hex(event["correlation_ref"]):
        _schema_error("event references must be lowercase sha256 values")
    if not _is_date(event["occurred_on"]):
        _schema_error("occurred_on must be an ISO calendar date")
    if not _is_nonempty_string_or_none(event["model_family"]):
        _schema_error("model_family must be a non-empty string or null")
    if not _is_nonempty_string_or_none(event["harness_class"]):
        _schema_error("harness_class must be a non-empty string or null")
    if event["provenance_mode"] not in PROVENANCE_MODES:
        _schema_error("provenance mode is invalid")
    if event["privacy_class"] != "portable-minimized":
        _schema_error("privacy class is invalid")
    if not isinstance(event["evidence_refs"], list):
        _schema_error("evidence_refs must be an array")
    for evidence_ref in event["evidence_refs"]:
        _verify_evidence_ref(evidence_ref, "evidence_ref")
    if variant == "calibratable":
        forecast = _require_mapping(
            event["forecast"],
            {"outcome_class", "probability", "resolution_rule"},
            {"outcome_class", "probability", "resolution_rule"},
            "forecast",
        )
        probability = forecast["probability"]
        if (
            forecast["outcome_class"] not in OUTCOME_CLASSES
            or isinstance(probability, bool)
            or not isinstance(probability, (int, float))
            or not 0.0 <= probability <= 1.0
            or forecast["resolution_rule"] not in RESOLUTION_RULES
        ):
            _schema_error("forecast is invalid")
    else:
        observation = _require_mapping(
            event["observation"], {"class"}, {"class"}, "observation"
        )
        if observation["class"] not in OBSERVATION_CLASSES:
            _schema_error("observation class is invalid")


def verify_outcome(record: dict) -> None:
    """Validate a closed append-only epistemic outcome in memory."""
    _reject_prohibited_keys(record)
    outcome = _require_mapping(
        record,
        {
            "record", "observation_id", "event_id", "outcome_class", "resolution_status",
            "verification_method", "independence_class", "evidence_ref", "observed_on",
            "producer", "supersedes",
        },
        {
            "record", "observation_id", "event_id", "outcome_class", "resolution_status",
            "verification_method", "independence_class", "evidence_ref", "observed_on",
            "producer", "supersedes",
        },
        "outcome",
    )
    if outcome["record"] != OUTCOME_RECORD:
        _schema_error("outcome record discriminator is invalid")
    if not _is_hex(outcome["observation_id"]) or not _is_hex(outcome["event_id"]):
        _schema_error("outcome identifiers must be lowercase sha256 values")
    if outcome["outcome_class"] not in OUTCOME_CLASSES:
        _schema_error("outcome class is not closed")
    if outcome["resolution_status"] not in RESOLUTION_STATUSES:
        _schema_error("resolution status is invalid")
    if outcome["verification_method"] not in VERIFICATION_METHODS:
        _schema_error("verification method is invalid")
    if outcome["independence_class"] not in INDEPENDENCE_CLASSES:
        _schema_error("independence class is invalid")
    _verify_evidence_ref(outcome["evidence_ref"], "evidence_ref", allow_none=True)
    if not _is_date(outcome["observed_on"]):
        _schema_error("observed_on must be an ISO calendar date")
    if not isinstance(outcome["producer"], str) or not outcome["producer"]:
        _schema_error("outcome producer must be non-empty")
    if outcome["supersedes"] is not None and not _is_hex(outcome["supersedes"]):
        _schema_error("supersedes must be a lowercase sha256 value or null")
    if outcome["resolution_status"] == "superseded" and outcome["supersedes"] is None:
        _schema_error("superseded outcomes require a predecessor")
    if outcome["supersedes"] is not None and outcome["supersedes"] == outcome["observation_id"]:
        _schema_error("an outcome cannot supersede itself")
    if outcome["resolution_status"] == "resolved" and (
        outcome["evidence_ref"] is None or outcome["independence_class"] == "self-reported"
    ):
        _schema_error("resolved outcomes require independent evidence")


def canonical_record_bytes(record: dict) -> bytes:
    """Produce the stable JSONL bytes used by append-only public logs."""
    return (
        json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("utf-8")


def append_validated_record(record: dict, output: Path) -> None:
    """Validate and append one canonical record to an explicitly named file."""
    if not isinstance(record, dict):
        raise EventError("UNKNOWN_RECORD", "record must be an object")
    if record.get("record") == EVENT_RECORD:
        verify_event(record)
    elif record.get("record") == OUTCOME_RECORD:
        verify_outcome(record)
    else:
        raise EventError("UNKNOWN_RECORD", "unsupported record discriminator")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("ab") as handle:
        handle.write(canonical_record_bytes(record))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and append one epistemic record")
    parser.add_argument("record", type=Path, help="JSON record to validate")
    parser.add_argument("--output", type=Path, required=True, help="JSONL output path")
    arguments = parser.parse_args(argv)
    try:
        with arguments.record.open(encoding="utf-8") as handle:
            record = json.load(handle)
        append_validated_record(record, arguments.output)
    except (EventError, OSError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
