"""Behavioral tests for the public epistemic event contracts."""

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parent
MODULE_PATH = ROOT / "verify_epistemic_event.py"
SPEC = importlib.util.spec_from_file_location("verify_epistemic_event", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("unable to load verifier module")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

EventError = MODULE.EventError
append_validated_record = MODULE.append_validated_record
canonical_record_bytes = MODULE.canonical_record_bytes
verify_event = MODULE.verify_event
verify_outcome = MODULE.verify_outcome
load_skill_event_map = MODULE.load_skill_event_map
verify_skill_event_map = MODULE.verify_skill_event_map

MAP_PATH = ROOT / "skill-event-map.json"


def root_skills_reference() -> Path:
    """Resolve the tracked root skills alias on symlink-capable and Windows checkouts."""
    skills_alias = ROOT.parents[3] / "skills"
    if skills_alias.is_dir():
        skills_root = skills_alias
    else:
        skills_root = skills_alias.parent / skills_alias.read_text(encoding="utf-8").strip()
    return skills_root / "using-epistemic-skills" / "reference" / "epistemic-data-collection.md"


ROOT_REFERENCE = root_skills_reference()
PACKAGE_REFERENCE = (
    ROOT.parents[1]
    / "skills"
    / "using-epistemic-skills"
    / "reference"
    / "epistemic-data-collection.md"
)
EXPECTED_SKILLS = {
    "using-epistemic-skills", "helix", "blindspot-pass",
    "applying-formal-rigor", "evidence-research", "write-goal",
    "outsource", "gauntlet", "evidence-locked-uat",
    "decision-ledger", "continuity-verify",
}


def load(relative_path: str) -> dict:
    with (ROOT / "examples" / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def load_outcome_schema() -> dict:
    with (ROOT / "epistemic-outcome.schema.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def load_skill_event_map_schema() -> dict:
    with (ROOT / "skill-event-map.schema.json").open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_matches(instance: object, schema: dict) -> bool:
    """Evaluate the JSON Schema keywords exercised by public contracts."""
    if "const" in schema and instance != schema["const"]:
        return False
    if "enum" in schema and instance not in schema["enum"]:
        return False
    if "type" in schema:
        allowed_types = schema["type"]
        if not isinstance(allowed_types, list):
            allowed_types = [allowed_types]
        type_matches = {
            "object": isinstance(instance, dict),
            "array": isinstance(instance, list),
            "string": isinstance(instance, str),
            "number": isinstance(instance, (int, float)) and not isinstance(instance, bool),
            "null": instance is None,
        }
        if not any(type_matches.get(name, False) for name in allowed_types):
            return False
    if "required" in schema:
        if not isinstance(instance, dict) or not set(schema["required"]) <= set(instance):
            return False
    if schema.get("additionalProperties") is False and isinstance(instance, dict):
        if set(instance) - set(schema.get("properties", {})):
            return False
    if "properties" in schema and isinstance(instance, dict):
        for key, property_schema in schema["properties"].items():
            if key in instance and not schema_matches(instance[key], property_schema):
                return False
    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            return False
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            return False
        if "items" in schema and any(not schema_matches(item, schema["items"]) for item in instance):
            return False
    if "pattern" in schema and isinstance(instance, str) and not re.search(schema["pattern"], instance):
        return False
    if "not" in schema and schema_matches(instance, schema["not"]):
        return False
    for branch in schema.get("allOf", []):
        if not schema_matches(instance, branch):
            return False
    if "oneOf" in schema and sum(schema_matches(instance, branch) for branch in schema["oneOf"]) != 1:
        return False
    if "contains" in schema and isinstance(instance, list):
        matches = sum(schema_matches(item, schema["contains"]) for item in instance)
        if matches < schema.get("minContains", 1):
            return False
        if "maxContains" in schema and matches > schema["maxContains"]:
            return False
    if "if" in schema and schema_matches(instance, schema["if"]):
        if "then" in schema and not schema_matches(instance, schema["then"]):
            return False
    return True


class EpistemicEventContractTests(unittest.TestCase):
    def test_map_covers_every_packaged_skill_once(self):
        mapping = load_skill_event_map(MAP_PATH)
        verify_skill_event_map(mapping)
        names = [item["skill"] for item in mapping["skills"]]
        self.assertEqual(set(names), EXPECTED_SKILLS)
        self.assertEqual(len(names), len(set(names)))

    def test_every_skill_has_a_non_routine_eligibility_rule(self):
        mapping = load_skill_event_map(MAP_PATH)
        for item in mapping["skills"]:
            self.assertNotEqual(item["eligible_when"], "every invocation")
            self.assertTrue(item["sentinel_fixture"])

    def test_schema_and_verifier_reject_duplicate_skill_map_rows(self):
        mapping = load_skill_event_map(MAP_PATH)
        broken = json.loads(json.dumps(mapping))
        broken["skills"][1]["skill"] = "using-epistemic-skills"
        self.assertFalse(schema_matches(broken, load_skill_event_map_schema()))
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_skill_event_map(broken)

    def test_schema_and_verifier_reject_valid_field_wrong_cross_pairing(self):
        mapping = load_skill_event_map(MAP_PATH)
        broken = json.loads(json.dumps(mapping))
        broken["skills"][0]["event_kinds"] = ["pairing-decision"]
        self.assertFalse(schema_matches(broken, load_skill_event_map_schema()))
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_skill_event_map(broken)

    def test_schema_and_verifier_accept_the_closed_skill_event_map(self):
        mapping = load_skill_event_map(MAP_PATH)
        self.assertTrue(schema_matches(mapping, load_skill_event_map_schema()))
        verify_skill_event_map(mapping)

    def test_canonical_and_packaged_collection_references_match(self):
        self.assertEqual(
            ROOT_REFERENCE.read_bytes(),
            PACKAGE_REFERENCE.read_bytes(),
        )

    def test_calibratable_event_requires_probability_and_resolution_rule(self):
        record = load("valid/calibratable-event.json")
        verify_event(record)
        broken = {**record, "forecast": {**record["forecast"]}}
        del broken["forecast"]["probability"]
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_event(broken)

    def test_observational_event_rejects_probability(self):
        with self.assertRaisesRegex(EventError, "ILLEGAL_EVENT_VARIANT"):
            verify_event(load("invalid/observational-with-probability.json"))

    def test_raw_content_keys_fail_closed(self):
        with self.assertRaisesRegex(EventError, "PROHIBITED_CONTENT"):
            verify_event(load("invalid/raw-content.json"))

    def test_equal_canonical_records_have_equal_bytes(self):
        left = load("valid/calibratable-event.json")
        right = dict(reversed(list(left.items())))
        self.assertEqual(canonical_record_bytes(left), canonical_record_bytes(right))

    def test_unknown_event_kind_fails_closed(self):
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_event(load("invalid/unknown-event-kind.json"))

    def test_outcome_requires_independent_evidence_when_resolved(self):
        record = load("valid/outcome.json")
        verify_outcome(record)
        missing_evidence = {**record, "evidence_ref": None}
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_outcome(missing_evidence)
        self_reported = {**record, "independence_class": "self-reported"}
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_outcome(self_reported)

    def test_append_validated_record_requires_explicit_validated_record(self):
        record = load("valid/calibratable-event.json")
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "records" / "events.jsonl"
            append_validated_record(record, output)
            self.assertEqual(output.read_bytes(), canonical_record_bytes(record))

    def test_schema_and_verifier_reject_resolved_outcomes_without_independent_evidence(self):
        record = load("valid/outcome.json")
        for broken in (
            {**record, "evidence_ref": None},
            {**record, "independence_class": "self-reported"},
        ):
            self.assertFalse(schema_matches(broken, load_outcome_schema()))
            with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
                verify_outcome(broken)

    def test_schema_and_verifier_require_a_predecessor_for_superseded_outcomes(self):
        record = {**load("valid/outcome.json"), "resolution_status": "superseded", "supersedes": None}
        self.assertFalse(schema_matches(record, load_outcome_schema()))
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_outcome(record)

    def test_verifier_rejects_a_self_superseding_outcome(self):
        record = load("valid/outcome.json")
        broken = {
            **record,
            "resolution_status": "superseded",
            "supersedes": record["observation_id"],
        }
        with self.assertRaisesRegex(EventError, "SCHEMA_VIOLATION"):
            verify_outcome(broken)

    def test_append_invalid_scalar_raises_a_controlled_event_error(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "events.jsonl"
            with self.assertRaisesRegex(EventError, "UNKNOWN_RECORD"):
                append_validated_record([], output)


if __name__ == "__main__":
    unittest.main()
