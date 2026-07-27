"""Behavioral tests for the public epistemic event contracts."""

import importlib.util
import json
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


def load(relative_path: str) -> dict:
    with (ROOT / "examples" / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


class EpistemicEventContractTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
