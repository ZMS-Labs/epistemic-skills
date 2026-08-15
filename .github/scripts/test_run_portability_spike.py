#!/usr/bin/env python3
"""Contract tests for the Stage-A portability spike runner."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / ".github/scripts/run_portability_spike.py"
VERIFIER = ROOT / ".github/scripts/verify_portability_spike_bundle.py"
VALIDATOR = ROOT / ".github/scripts/validate_portability_contract.py"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verifier_command(root: Path) -> list[str]:
    return [sys.executable, str(VERIFIER), "--root", str(root),
            "--approved-verifier-sha256", sha256_bytes(VERIFIER.read_bytes()),
            "--approved-validator-sha256", sha256_bytes(VALIDATOR.read_bytes())]


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256(b"zms-portable-tree-v1\0")
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode()
        mode = b"0755" if path.stat().st_mode & 0o111 else b"0644"
        digest.update(relative + b"\0" + mode + b"\0" + hashlib.sha256(path.read_bytes()).digest() + b"\n")
    return digest.hexdigest()


def load_runner():
    spec = importlib.util.spec_from_file_location("run_portability_spike", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


class SpikeFixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        source = root / "source"
        (source / "plugins/epistemic-skills/skills/manifest").mkdir(parents=True)
        (source / "plugins/epistemic-skills/contracts/mission-custody").mkdir(parents=True)
        (source / "plugins/epistemic-skills/skills/manifest/SKILL.md").write_text("---\nname: manifest\ndescription: fixture\n---\n", encoding="utf-8")
        (source / "plugins/epistemic-skills/contracts/mission-custody/custody.py").write_text("fixture custody\n", encoding="utf-8")
        dependency_contract = {
            "schema": "zms-skill-dependencies@1",
            "defaults": {"standalone": {"state": "unverified"}},
            "skills": {"manifest": {"dependency_roots": []}},
        }
        (source / "packaging/portability").mkdir(parents=True)
        (source / "packaging/portability/dependencies.json").write_bytes(canonical_bytes(dependency_contract))
        profile = {
            "product": "fixture-host", "surface": "fixture-surface",
            "release_or_channel": "fixture-1", "profile_revision": "profile@1",
            "transform": "preserve-canonical-package-layout@1",
        }
        self.write_json("profile.json", profile)
        (root / ".github/scripts").mkdir(parents=True)
        for filename in ("build_portable_skill_projection.py", "skill_artifact_lib.py", "validate_portability_contract.py", "run_portability_spike.py", "verify_portability_spike_bundle.py", "execute_portability_generator.py", "probe_portability_surface.py", "enumerate_dynamic_dependencies.py"):
            shutil.copy2(ROOT / ".github/scripts" / filename, root / ".github/scripts" / filename)
        builder = load_script("fixture_builder", root / ".github/scripts/build_portable_skill_projection.py")
        source_record = {"kind": "git-commit", "revision": "a" * 40, "dirty": False, "mutable": False}
        ir = builder.derive_ir(source, source_record, profile)
        self.write_json("ir.json", ir)
        self.write_json("transform.json", {"record": "projection-transform@1", "identifier": profile["transform"], "generator_revision": "phase1-v1"})
        built = builder.build_projection(source, root / "projection-output", source_record, profile)
        installed = built.projection_root
        shutil.copy2(built.result_path, root / "projection.json")
        self.write("installer.py", b"# bounded fixture installer\n")
        self.write_json("consumer.json", {"record": "spike-consumer-set@1", "consumers": ["fixture-host|fixture-surface"]})
        validator = load_script("fixture_validator", ROOT / ".github/scripts/validate_portability_contract.py")
        authoritative = root / "authoritative-root"; authoritative.mkdir()
        for filename in validator.PLANNING_ROOT_FILES.values():
            shutil.copy2(ROOT / "packaging/portability" / filename, authoritative / filename)
        shutil.copytree(ROOT / "packaging/portability/schemas", authoritative / "schemas")
        shutil.copy2(ROOT / "packaging/portability/stage-a-execution-authority.json", authoritative / "stage-a-execution-authority.json")
        authority = json.loads((authoritative / "stage-a-execution-authority.json").read_text())
        self.write_json("authoritative-root/stage-a-evidence-epoch.json", {"record": "evidence-epoch@1", "current_epoch": "task3-epoch@1", "authority": "task2-authoritative-root"})
        shutil.copy2(authoritative / "planning-dag.json", root / "planning-dag.json")
        payload={"version":"fixture 1","served_bytes_sha256":"b"*64,"readback_sha256":"b"*64,"positive_discovery":True,"neighboring_negative_rejected":True};stdout=canonical_bytes(payload)
        executable=root/"fixture-host";executable.write_bytes((f"#!{sys.executable}\nimport sys\nsys.stdout.buffer.write({stdout!r})\n").encode());executable.chmod(0o755)
        transcript={"record":"native-probe-transcript@1","product":"fixture-host","surface":"fixture-surface","evidence_epoch":"task3-epoch@1","authority_id":authority["authority_id"],"issuer_identity":authority["probe_issuer_identity"],"readback_identity":authority["probe_readback_identity"],"platform":"linux","tool_sha256":authority["tools"]["probe_tool"]["sha256"],"executable_name":"fixture-host","executable_path":"fixture-host","executable_sha256":sha256_bytes(executable.read_bytes()),"version":"fixture 1","command":["fixture-host"],"exit_code":0,"stdout_sha256":sha256_bytes(stdout),"stderr_sha256":sha256_bytes(b""),"served_bytes_sha256":"b"*64,"readback_sha256":"b"*64,"positive_discovery":True,"neighboring_negative_rejected":True,"status":"observed","reason":"non-production equivalence native boundary observed"}
        transcript["transcript_digest"]=sha256_bytes(canonical_bytes(transcript));self.write_json("host.json",{"record":"native-probe-transcript-set@1","transcripts":[transcript]})
        skill=ir["skills"][0];coverage=sha256_bytes(canonical_bytes({"members":skill["members"],"dependencies":skill["dependencies"]}));dynamic={"record":"dynamic-dependency-enumeration@1","evidence_epoch":"task3-epoch@1","authority_id":authority["authority_id"],"issuer_identity":authority["enumerator_issuer_identity"],"readback_identity":authority["enumerator_readback_identity"],"enumerator_sha256":authority["tools"]["enumerator"]["sha256"],"method":"complete-declared-root-and-member-enumeration@1","skills":[{"name":"manifest","state":"none","coverage_digest":coverage,"residuals":[]}]};dynamic["readback_digest"]=sha256_bytes(canonical_bytes(dynamic));self.write_json("dynamic-dependencies.json",dynamic)
        artifacts = {}
        for name, relative, kind in (
            ("source", "source", "tree"), ("ir", "ir.json", "file"), ("generator", ".github/scripts/build_portable_skill_projection.py", "file"),
            ("transform", "transform.json", "file"), ("projection", "projection.json", "file"), ("profile", "profile.json", "file"),
            ("host", "host.json", "file"), ("installer", "installer.py", "file"), ("installed", "projection-output/projection/plugins/epistemic-skills", "tree"),
            ("consumer", "consumer.json", "file"), ("planning_dag", "planning-dag.json", "file"),
            ("dependency_contract", "source/packaging/portability/dependencies.json", "file"), ("epoch", "authoritative-root/stage-a-evidence-epoch.json", "file"),
            ("contract_validator", ".github/scripts/validate_portability_contract.py", "file"),
            ("artifact_library", ".github/scripts/skill_artifact_lib.py", "file"),
            ("authoritative_root", "authoritative-root", "tree"),
            ("dynamic_dependencies", "dynamic-dependencies.json", "file"),
            ("runner", ".github/scripts/run_portability_spike.py", "file"),
            ("verifier", ".github/scripts/verify_portability_spike_bundle.py", "file"),
            ("generator_executor", ".github/scripts/execute_portability_generator.py", "file"),
            ("probe_tool", ".github/scripts/probe_portability_surface.py", "file"),
            ("enumerator", ".github/scripts/enumerate_dynamic_dependencies.py", "file"),
            ("code_authority", "authoritative-root/stage-a-execution-authority.json", "file"),
        ):
            artifacts[name] = self.descriptor(relative, kind)
        self.request = {
            "record": "stage-a-portability-spike-input@1", "evidence_epoch": "task3-epoch@1",
            "purpose": "architecture-decision",
            "supersession_rule": "any bound digest, evidence epoch, or affected edge change requires a fresh spike",
            "artifacts": artifacts,
            "affected_dag_edges": [],
        }
        self.request["affected_dag_edges"] = load_runner().affected_edges(json.loads((root / "planning-dag.json").read_text()))
        self.request_path = root / "request.json"; self.save_request()

    def write(self, relative: str, data: bytes) -> None: (self.root / relative).write_bytes(data)
    def write_json(self, relative: str, value: object) -> None: self.write(relative, canonical_bytes(value))
    def descriptor(self, relative: str, kind: str) -> dict[str, str]:
        path = self.root / relative; digest = tree_digest(path) if kind == "tree" else sha256_bytes(path.read_bytes())
        return {"kind": kind, "path": relative, "sha256": digest}
    def refresh(self, name: str) -> None:
        descriptor = self.request["artifacts"][name]; self.request["artifacts"][name] = self.descriptor(descriptor["path"], descriptor["kind"])
    def save_request(self) -> None: self.request_path.write_bytes(canonical_bytes(self.request))
    def run(self, output: str = "out.json") -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(RUNNER), "--root", str(self.root), "--request", str(self.request_path), "--out", str(self.root / output), "--approved-validator-sha256", sha256_bytes(VALIDATOR.read_bytes())], capture_output=True, text=True)


class StageAPortabilitySpikeTests(unittest.TestCase):
    def fixture(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        return SpikeFixture(Path(temporary.name))
    def assert_refused(self, fixture: SpikeFixture, code: str) -> None:
        fixture.save_request(); run = fixture.run()
        self.assertEqual(2, run.returncode, run.stdout + run.stderr); self.assertIn(code, run.stdout + run.stderr)
        self.assertFalse((fixture.root / "out.json").exists())

    def test_complete_bound_input_is_deterministic_and_non_causal(self) -> None:
        fixture = self.fixture(); first = fixture.run("first.json"); second = fixture.run("second.json")
        self.assertEqual(0, first.returncode, first.stdout + first.stderr)
        self.assertEqual((fixture.root / "first.json").read_bytes(), (fixture.root / "second.json").read_bytes())
        record = json.loads((fixture.root / "first.json").read_text())
        self.assertEqual("proceed", record["decision"]); self.assertEqual("non-causal-decision-support", record["evidence_class"])
        self.assertEqual(["architecture-decision"], record["admissible_for"])
        self.assertEqual({"exact-conformance", "promotion", "tier-award", "usability"}, set(record["not_evidence_for"]))
        self.assertNotIn(str(fixture.root.resolve()), (fixture.root / "first.json").read_text())
        self.assertEqual(set(fixture.request["artifacts"]), set(record["input_digests"]))

    def test_exact_input_digest_change_fails_closed(self) -> None:
        fixture = self.fixture(); (fixture.root / "host.json").write_text("changed\n", encoding="utf-8")
        self.assert_refused(fixture, "SPIKE_DIGEST_MISMATCH")
    def test_changed_generator_and_transform_each_fail_closed(self) -> None:
        for name in ("generator", "transform"):
            with self.subTest(name=name):
                fixture = self.fixture(); path = fixture.root / fixture.request["artifacts"][name]["path"]
                path.write_bytes(path.read_bytes() + b"changed\n"); self.assert_refused(fixture, "SPIKE_DIGEST_MISMATCH")
    def test_complete_dependent_edge_closure_is_required(self) -> None:
        fixture = self.fixture(); fixture.request["affected_dag_edges"].pop()
        self.assert_refused(fixture, "SPIKE_DAG_EDGE_CLOSURE_MISMATCH")
    def test_new_dependent_edge_invalidates_prior_edge_list(self) -> None:
        fixture = self.fixture(); dag = json.loads((fixture.root / "planning-dag.json").read_text())
        dag["nodes"].append({"id": "later-profile", "stage": "B", "kind": "contract", "terminal": True})
        dag["edges"].append({"from": "profile-work", "to": "later-profile", "kind": "implementation", "mode": "template", "transition_artifact": "edge-new-profile"})
        fixture.write_json("planning-dag.json", dag); fixture.refresh("planning_dag")
        self.assert_refused(fixture, "SPIKE_DAG_NOT_AUTHORITATIVE")
    def test_stale_evidence_epoch_is_rejected(self) -> None:
        fixture = self.fixture(); fixture.write_json("authoritative-root/stage-a-evidence-epoch.json", {"record": "evidence-epoch@1", "current_epoch": "task3-epoch@2", "authority": "task2-authoritative-root"}); fixture.refresh("epoch"); fixture.refresh("authoritative_root")
        self.assert_refused(fixture, "SPIKE_EVIDENCE_EPOCH_STALE")
    def test_source_checkout_symlink_or_path_leak_is_rejected(self) -> None:
        fixture = self.fixture(); installed_root = fixture.root / fixture.request["artifacts"]["installed"]["path"]; installed = installed_root / "skills/manifest/SKILL.md"; installed.unlink(); installed.symlink_to(fixture.root / "source/plugins/epistemic-skills/skills/manifest/SKILL.md")
        self.assert_refused(fixture, "SPIKE_SOURCE_CHECKOUT_LEAKAGE")
        fixture = self.fixture(); installed_root = fixture.root / fixture.request["artifacts"]["installed"]["path"]; (installed_root / "skills/manifest/SKILL.md").write_text(str((fixture.root / "source").resolve()), encoding="utf-8"); fixture.refresh("installed")
        self.assert_refused(fixture, "SPIKE_SOURCE_CHECKOUT_LEAKAGE")
    def test_undeclared_or_mismatched_dependency_is_rejected(self) -> None:
        fixture = self.fixture(); ir = json.loads((fixture.root / "ir.json").read_text())
        ir["skills"][0]["dependencies"].append({"path": "plugins/undeclared", "kind": "file", "sha256": "c" * 64}); fixture.write_json("ir.json", ir); fixture.refresh("ir")
        self.assert_refused(fixture, "SPIKE_DEPENDENCY_CLOSURE_MISMATCH")
    def test_exact_conformance_promotion_and_usability_purposes_are_rejected(self) -> None:
        for purpose in ("exact-conformance", "promotion", "usability", "tier-award"):
            with self.subTest(purpose=purpose):
                fixture = self.fixture(); fixture.request["purpose"] = purpose; self.assert_refused(fixture, "SPIKE_PURPOSE_FORBIDDEN")
    def test_decision_and_edge_disposition_tampering_is_detected(self) -> None:
        fixture = self.fixture(); self.assertEqual(0, fixture.run().returncode); module = load_runner()
        record = json.loads((fixture.root / "out.json").read_text()); record["decision"] = "pivot"
        self.assertIn("SPIKE_DECISION_MISMATCH", module.validate_spike_record(record))
        record = json.loads((fixture.root / "out.json").read_text()); record["edge_dispositions"][0]["disposition"] = "blocked"
        self.assertIn("SPIKE_EDGE_DISPOSITION_MISMATCH", module.validate_spike_record(record))
    def test_unknown_malformed_and_duplicate_json_inputs_fail_without_traceback(self) -> None:
        cases = []
        fixture = self.fixture(); fixture.request["surprise"] = True; fixture.save_request(); cases.append((fixture, "SPIKE_UNKNOWN_FIELD"))
        fixture = self.fixture(); fixture.request_path.write_text("{", encoding="utf-8"); cases.append((fixture, "SPIKE_JSON_UNREADABLE"))
        fixture = self.fixture(); fixture.request_path.write_text('{"record":"stage-a-portability-spike-input@1","record":"duplicate"}\n', encoding="utf-8"); cases.append((fixture, "SPIKE_DUPLICATE_JSON_MEMBER"))
        for fixture, code in cases:
            with self.subTest(code=code):
                run = fixture.run(); self.assertEqual(2, run.returncode, run.stdout + run.stderr); self.assertIn(code, run.stdout + run.stderr); self.assertNotIn("Traceback", run.stdout + run.stderr)
    def test_malformed_descriptors_paths_and_record_types_fail_closed(self) -> None:
        fixture = self.fixture(); fixture.request["artifacts"]["host"]["kind"] = "socket"; self.assert_refused(fixture, "SPIKE_ARTIFACT_DESCRIPTOR_INVALID")
        fixture = self.fixture(); fixture.request["artifacts"]["host"]["path"] = "../escape"; self.assert_refused(fixture, "SPIKE_ARTIFACT_PATH_ESCAPE")
        fixture = self.fixture(); fixture.request["record"] = "stage-c-exact-conformance@1"; self.assert_refused(fixture, "SPIKE_RECORD_INVALID")
    def test_criteria_derive_only_closed_decisions_and_edge_states(self) -> None:
        module=load_runner()
        for status, decision in (("passed", "proceed"), ("failed", "pivot"), ("unverified", "narrow")):
            with self.subTest(status=status):
                self.assertEqual(decision,module.derive_decision([{"status":status}]))
    def test_projection_semantic_bindings_reject_changed_ir_generator_or_transform(self) -> None:
        for field, value in (("generator_revision", "changed"), ("transform", "changed")):
            with self.subTest(field=field):
                fixture = self.fixture(); projection = json.loads((fixture.root / "projection.json").read_text()); projection[field] = value
                fixture.write_json("projection.json", projection); fixture.refresh("projection"); self.assert_refused(fixture, "SPIKE_GENERATOR_EXECUTION_FAILED")

    def test_unknown_or_malformed_bound_json_documents_fail_closed(self) -> None:
        cases = (
            ("host", "host.json", {"record": "native-probe-transcript-set@1", "transcripts": [], "extra": True}, "SPIKE_HOST_INVALID"),
            ("consumer", "consumer.json", {"record": "spike-consumer-set@1", "consumers": "fixture"}, "SPIKE_CONSUMER_INVALID"),
            ("epoch", "authoritative-root/stage-a-evidence-epoch.json", {"record": "evidence-epoch@1", "current_epoch": "task3-epoch@1", "authority": "task2-authoritative-root", "extra": True}, "SPIKE_EVIDENCE_EPOCH_INVALID"),
            ("profile", "profile.json", {"product": "fixture-host", "surface": "fixture-surface", "release_or_channel": "fixture-1", "profile_revision": "profile@1", "transform": "preserve-canonical-package-layout@1", "extra": True}, "SPIKE_PROFILE_INVALID"),
            ("transform", "transform.json", {"record": "projection-transform@1", "identifier": "preserve-canonical-package-layout@1", "generator_revision": "phase1-v1", "extra": True}, "SPIKE_TRANSFORM_INVALID"),
        )
        for artifact, relative, value, code in cases:
            with self.subTest(artifact=artifact):
                fixture = self.fixture(); fixture.write_json(relative, value); fixture.refresh(artifact)
                if artifact == "epoch": fixture.refresh("authoritative_root")
                self.assert_refused(fixture, code)

    def test_source_mutation_with_stale_ir_is_rejected(self) -> None:
        fixture = self.fixture(); source_skill = fixture.root / "source/plugins/epistemic-skills/skills/manifest/SKILL.md"
        source_skill.write_bytes(source_skill.read_bytes() + b"\nchanged\n"); fixture.refresh("source")
        self.assert_refused(fixture, "SPIKE_GENERATOR_EXECUTION_FAILED")

    def test_unrelated_generator_is_rejected_even_when_redigested(self) -> None:
        fixture = self.fixture(); generator = fixture.root / fixture.request["artifacts"]["generator"]["path"]
        generator.write_text("# unrelated generator\n", encoding="utf-8"); fixture.refresh("generator")
        self.assert_refused(fixture, "SPIKE_CODE_NOT_APPROVED")

    def test_installed_tree_must_be_generator_derived(self) -> None:
        fixture = self.fixture(); installed = fixture.root / fixture.request["artifacts"]["installed"]["path"] / "skills/manifest/SKILL.md"
        installed.write_bytes(installed.read_bytes() + b"\nnot generated\n"); fixture.refresh("installed")
        projection = json.loads((fixture.root / "projection.json").read_text()); projection["served_tree_sha256"] = tree_digest(installed.parents[2]); fixture.write_json("projection.json", projection); fixture.refresh("projection")
        self.assert_refused(fixture, "SPIKE_GENERATOR_EXECUTION_FAILED")

    def test_hardlinked_source_and_installed_member_is_rejected(self) -> None:
        fixture = self.fixture(); installed = fixture.root / fixture.request["artifacts"]["installed"]["path"] / "skills/manifest/SKILL.md"
        source = fixture.root / "source/plugins/epistemic-skills/skills/manifest/SKILL.md"; installed.unlink(); os.link(source, installed)
        fixture.refresh("installed"); projection = json.loads((fixture.root / "projection.json").read_text()); projection["served_tree_sha256"] = tree_digest(installed.parents[2]); fixture.write_json("projection.json", projection); fixture.refresh("projection")
        self.assert_refused(fixture, "SPIKE_SOURCE_CHECKOUT_ALIAS")

    def test_descendant_reparse_or_junction_is_rejected_before_traversal(self) -> None:
        fixture=self.fixture();module=load_runner();target=fixture.root/fixture.request['artifacts']['installed']['path']
        with mock.patch.object(module,'is_reparse_point',side_effect=lambda path:path.name=='SKILL.md'):
            with self.assertRaisesRegex(module.SpikeError,'SPIKE_SOURCE_CHECKOUT_LEAKAGE'):module.artifact_digest(target,'tree')

    def test_nonexistent_executable_cannot_forge_observed_status(self) -> None:
        fixture=self.fixture();host=json.loads((fixture.root/'host.json').read_text());item=host['transcripts'][0];item['executable_path']='missing-host';item['executable_sha256']='c'*64;item['transcript_digest']=sha256_bytes(canonical_bytes({key:value for key,value in item.items() if key!='transcript_digest'}));fixture.write_json('host.json',host);fixture.refresh('host')
        self.assert_refused(fixture,'SPIKE_PROBE_TRANSCRIPT_UNRESOLVED')

    def test_observed_fixture_executable_cannot_be_relabelled_as_codex(self) -> None:
        fixture=self.fixture();host=json.loads((fixture.root/'host.json').read_text());item=host['transcripts'][0]
        item['product']='openai-codex';item['surface']='codex-cli-project-user-discovery';item['executable_name']='codex';item['transcript_digest']=sha256_bytes(canonical_bytes({key:value for key,value in item.items() if key!='transcript_digest'}))
        fixture.write_json('host.json',host);fixture.write_json('consumer.json',{'record':'spike-consumer-set@1','consumers':['openai-codex|codex-cli-project-user-discovery']});fixture.refresh('host');fixture.refresh('consumer')
        self.assert_refused(fixture,'SPIKE_PROBE_TRANSCRIPT_UNRESOLVED')

    def test_self_asserted_dynamic_none_cannot_proceed(self) -> None:
        fixture=self.fixture();dynamic=json.loads((fixture.root/'dynamic-dependencies.json').read_text());dynamic['enumerator_sha256']='c'*64;dynamic['readback_digest']=sha256_bytes(canonical_bytes({key:value for key,value in dynamic.items() if key!='readback_digest'}));fixture.write_json('dynamic-dependencies.json',dynamic);fixture.refresh('dynamic_dependencies')
        self.assert_refused(fixture,'SPIKE_DYNAMIC_ENUMERATION_UNRESOLVED')

    def test_well_formed_dynamic_none_is_derived_unresolved_for_non_equivalence_source(self) -> None:
        fixture=self.fixture();ir=json.loads((fixture.root/'ir.json').read_text());ir['source']['revision']='b'*40;fixture.write_json('ir.json',ir)
        run=subprocess.run([sys.executable,'-I',str(fixture.root/'.github/scripts/enumerate_dynamic_dependencies.py'),'--source',str(fixture.root/'source'),'--ir',str(fixture.root/'ir.json'),'--transcript',str(fixture.root/'dynamic-dependencies.json'),'--authority',str(fixture.root/'authoritative-root/stage-a-execution-authority.json'),'--epoch','task3-epoch@1'],capture_output=True,text=True)
        self.assertEqual(0,run.returncode,run.stdout+run.stderr);verdict=json.loads(run.stdout);self.assertEqual('unresolved',verdict['skills'][0]['state'])

    def test_dynamic_dependency_residual_forces_narrow(self) -> None:
        fixture = self.fixture();dynamic=json.loads((fixture.root/'dynamic-dependencies.json').read_text());dynamic['skills'][0]['state']='unresolved';dynamic['skills'][0]['residuals']=['runtime import cannot be statically resolved'];dynamic['readback_digest']=sha256_bytes(canonical_bytes({key:value for key,value in dynamic.items() if key!='readback_digest'}));fixture.write_json('dynamic-dependencies.json',dynamic);fixture.refresh('dynamic_dependencies');fixture.save_request()
        run = fixture.run(); self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertEqual("narrow", json.loads((fixture.root / "out.json").read_text())["decision"])

    def test_api_compatible_generator_library_and_authority_tampering_never_executes(self) -> None:
        for name in ('generator','artifact_library'):
            with self.subTest(name=name):
                fixture=self.fixture();path=fixture.root/fixture.request['artifacts'][name]['path'];marker=fixture.root/'side-effect'
                path.write_bytes(path.read_bytes()+f"\nopen({str(marker)!r},'w').write('bad')\n".encode());fixture.refresh(name)
                self.assert_refused(fixture,'SPIKE_CODE_NOT_APPROVED');self.assertFalse(marker.exists())
        fixture=self.fixture();authority=json.loads((fixture.root/'authoritative-root/stage-a-execution-authority.json').read_text());authority['authority_id']='unapproved';authority['content_digest']=load_runner().record_digest(authority);fixture.write_json('authoritative-root/stage-a-execution-authority.json',authority);fixture.refresh('code_authority');fixture.refresh('authoritative_root')
        self.assert_refused(fixture,'SPIKE_CODE_AUTHORITY_UNAPPROVED')

    def test_generator_executor_top_level_runtime_error_is_stable_without_traceback(self) -> None:
        fixture=self.fixture();generator=fixture.root/'.github/scripts/build_portable_skill_projection.py';generator.write_text("raise RuntimeError('boom')\n")
        request={'source':str(fixture.root/'source'),'source_record':{'kind':'git-commit','revision':'a'*40,'dirty':False,'mutable':False},'profile':json.loads((fixture.root/'profile.json').read_text()),'expected_ir':str(fixture.root/'ir.json'),'expected_projection':str(fixture.root/'projection.json'),'expected_installed':str(fixture.root/'projection-output/projection/plugins/epistemic-skills'),'generator':str(generator),'artifact_library':str(fixture.root/'.github/scripts/skill_artifact_lib.py')}
        path=fixture.root/'executor-request.json';path.write_bytes(canonical_bytes(request));run=subprocess.run([sys.executable,'-I',str(ROOT/'.github/scripts/execute_portability_generator.py'),'--request',str(path)],capture_output=True,text=True)
        self.assertEqual(2,run.returncode);self.assertIn('REFUSED GENERATOR_EXECUTOR_FAILED',run.stdout);self.assertNotIn('Traceback',run.stderr)

    def test_bound_dag_requires_authoritative_shape_digest_transitions_and_gates(self) -> None:
        module = load_runner()
        mutations = ("reduced", "cycle", "stale-digest", "missing-transition", "gate-bypass")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                fixture = self.fixture(); dag = json.loads((fixture.root / "planning-dag.json").read_text())
                if mutation == "reduced":
                    dag["edges"] = dag["edges"][:-1]
                elif mutation == "cycle":
                    dag["edges"].append({"from": "n-active-bounded-exact-claim", "to": "reviewed-contract", "kind": "authority", "mode": "template", "transition_artifact": "missing-cycle-transition"})
                elif mutation == "missing-transition":
                    dag["edges"][0]["transition_artifact"] = "missing-transition"
                elif mutation == "gate-bypass":
                    dag["edges"].append({"from": "reviewed-contract", "to": "n-active-candidate", "kind": "authority", "mode": "template", "transition_artifact": "missing-bypass-transition"})
                else:
                    dag["edges"][0]["kind"] = "evidence"
                if mutation != "stale-digest":
                    dag["content_digest"] = module.canonical_digest({key: value for key, value in dag.items() if key != "content_digest"})
                fixture.write_json("planning-dag.json", dag); fixture.write_json("authoritative-root/planning-dag.json", dag)
                fixture.refresh("planning_dag"); fixture.refresh("authoritative_root")
                expected = "SPIKE_DAG_CONTENT_DIGEST_MISMATCH" if mutation == "stale-digest" else "SPIKE_DAG_AUTHORITY_INVALID"
                self.assert_refused(fixture, expected)

    def test_custodied_two_surface_result_is_current_non_causal_narrowing(self) -> None:
        module = load_runner()
        record = json.loads((ROOT / "packaging/portability/stage-a-portability-spike.json").read_text())
        dag = json.loads((ROOT / "packaging/portability/planning-dag.json").read_text())
        self.assertEqual([], module.validate_spike_record(record))
        self.assertEqual(module.affected_edges(dag), record["affected_dag_edges"])
        self.assertEqual("narrow", record["decision"])
        self.assertEqual(
            {("anthropic-claude-code", "claude-code-cli-plugin", "unverified"), ("openai-codex", "codex-cli-project-user-discovery", "unverified")},
            {(item["product"], item["surface"], item["status"]) for item in record["probe_observations"]},
        )

    def test_shipped_evidence_bundle_replays_byte_identically(self) -> None:
        run = subprocess.run(verifier_command(ROOT), capture_output=True, text=True)
        self.assertEqual(0, run.returncode, run.stdout + run.stderr)
        self.assertEqual("verified-byte-identical", run.stdout.strip())

    def test_isolated_bundle_request_object_revision_and_resolver_tampering_are_rejected(self) -> None:
        for mutation in ("request", "object", "code-revision", "root-member"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                isolated = Path(temporary); shutil.copytree(ROOT / "packaging/portability", isolated / "packaging/portability")
                if mutation == "request":
                    target = isolated / "packaging/portability/stage-a-evidence/request.json"
                    target.write_bytes(target.read_bytes() + b"tampered\n")
                elif mutation == "object":
                    bundle = json.loads((isolated / "packaging/portability/stage-a-portability-spike.bundle.json").read_text())
                    target = isolated / bundle["artifact_resolvers"]["source"]["path"]
                    target.write_bytes(target.read_bytes() + b"tampered\n")
                elif mutation == "code-revision":
                    target = isolated / "packaging/portability/stage-a-portability-spike.bundle.json"
                    bundle = json.loads(target.read_text()); bundle["code_revision"] = "0" * 40
                    bundle["content_digest"] = sha256_bytes(canonical_bytes({key: value for key, value in bundle.items() if key != "content_digest"}))
                    target.write_bytes(canonical_bytes(bundle))
                else:
                    target = isolated / "packaging/portability/stage-a-portability-spike.bundle.json"
                    bundle = json.loads(target.read_text()); bundle["artifact_resolvers"]["planning_dag"]["member"] = "not-the-authoritative-dag.json"
                    bundle["content_digest"] = sha256_bytes(canonical_bytes({key: value for key, value in bundle.items() if key != "content_digest"}))
                    target.write_bytes(canonical_bytes(bundle))
                run = subprocess.run(verifier_command(isolated), capture_output=True, text=True)
                self.assertEqual(2, run.returncode, run.stdout + run.stderr); self.assertIn("REFUSED", run.stdout); self.assertNotIn("Traceback", run.stdout + run.stderr)
                if mutation == "code-revision": self.assertIn("BUNDLE_CODE_REVISION_UNAPPROVED", run.stdout)
                if mutation == "root-member": self.assertIn("BUNDLE_RESOLVER_INVALID", run.stdout)

    def test_retained_bundle_replays_without_git_or_ancestor_objects(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            isolated=Path(temporary);shutil.copytree(ROOT/'packaging/portability',isolated/'packaging/portability')
            run=subprocess.run(verifier_command(isolated),capture_output=True,text=True,env={'PATH':''})
            self.assertEqual(0,run.returncode,run.stdout+run.stderr);self.assertEqual('verified-byte-identical',run.stdout.strip())

    def test_retained_absence_replay_is_independent_of_caller_path(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            isolated=Path(temporary);shutil.copytree(ROOT/'packaging/portability',isolated/'packaging/portability');binary=isolated/'bin';binary.mkdir()
            for name in ('claude','codex'):
                target=binary/name;target.write_text('#!/bin/sh\nexit 0\n');target.chmod(0o755)
            run=subprocess.run(verifier_command(isolated),capture_output=True,text=True,env={'PATH':str(binary)})
            self.assertEqual(0,run.returncode,run.stdout+run.stderr);self.assertEqual('verified-byte-identical',run.stdout.strip())

    def test_replay_refuses_coherently_redigested_executable_code_before_side_effect(self) -> None:
        for name in ('runner','generator_executor'):
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temporary:
                isolated=Path(temporary);shutil.copytree(ROOT/'packaging/portability',isolated/'packaging/portability');marker=isolated/'executed'
                bundle_path=isolated/'packaging/portability/stage-a-portability-spike.bundle.json';request_path=isolated/'packaging/portability/stage-a-evidence/request.json';bundle=json.loads(bundle_path.read_text());request=bundle['canonical_request'];resolver=bundle['artifact_resolvers'][name];target=isolated/resolver['path']
                data=(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n".encode()+target.read_bytes());digest=sha256_bytes(data);target.write_bytes(data)
                request['artifacts'][name]['sha256']=digest;resolver['sha256']=digest;resolver['object_sha256']=digest;request_path.write_bytes(canonical_bytes(request));bundle['request_digest']=sha256_bytes(canonical_bytes(request));bundle['content_digest']=sha256_bytes(canonical_bytes({key:value for key,value in bundle.items() if key!='content_digest'}));bundle_path.write_bytes(canonical_bytes(bundle))
                run=subprocess.run(verifier_command(isolated),capture_output=True,text=True)
                self.assertEqual(2,run.returncode,run.stdout+run.stderr);self.assertIn('BUNDLE_CODE_UNAPPROVED',run.stdout);self.assertFalse(marker.exists())

    def test_split_descriptor_and_object_digests_refuse_every_code_object_before_execution(self) -> None:
        names=('runner','verifier','generator_executor','generator','artifact_library','contract_validator','probe_tool','enumerator')
        for name in names:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temporary:
                isolated=Path(temporary);shutil.copytree(ROOT/'packaging/portability',isolated/'packaging/portability');marker=isolated/'executed'
                bundle_path=isolated/'packaging/portability/stage-a-portability-spike.bundle.json';bundle=json.loads(bundle_path.read_text());resolver=bundle['artifact_resolvers'][name];target=isolated/resolver['path']
                data=(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n".encode()+target.read_bytes());target.write_bytes(data);resolver['object_sha256']=sha256_bytes(data)
                bundle['content_digest']=sha256_bytes(canonical_bytes({key:value for key,value in bundle.items() if key!='content_digest'}));bundle_path.write_bytes(canonical_bytes(bundle))
                run=subprocess.run(verifier_command(isolated),capture_output=True,text=True)
                self.assertEqual(2,run.returncode,run.stdout+run.stderr);self.assertIn('BUNDLE_OBJECT_DESCRIPTOR_SPLIT',run.stdout);self.assertFalse(marker.exists())

    def test_source_and_authority_content_revision_identities_cannot_be_relabelled(self) -> None:
        for field in ('source_revision','authoritative_revision'):
            with self.subTest(field=field),tempfile.TemporaryDirectory() as temporary:
                isolated=Path(temporary);shutil.copytree(ROOT/'packaging/portability',isolated/'packaging/portability');path=isolated/'packaging/portability/stage-a-portability-spike.bundle.json';bundle=json.loads(path.read_text());bundle[field]='content-addressed-tree-sha256:'+'0'*64;bundle['content_digest']=sha256_bytes(canonical_bytes({key:value for key,value in bundle.items() if key!='content_digest'}));path.write_bytes(canonical_bytes(bundle))
                run=subprocess.run(verifier_command(isolated),capture_output=True,text=True)
                self.assertEqual(2,run.returncode,run.stdout+run.stderr);self.assertIn('BUNDLE_REVISION_IDENTITY_INVALID',run.stdout)


if __name__ == "__main__":
    unittest.main()
