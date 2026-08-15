#!/usr/bin/env python3
"""Generate a deterministic, non-causal Stage-A portability decision record."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

from skill_artifact_lib import (
    ArtifactError,
    DuplicateJsonMember,
    canonical_json_bytes,
    load_json_strict,
    portable_tree_sha256,
    regular_files,
    sha256_bytes,
)


REQUIRED_ARTIFACTS = {
    "source", "ir", "generator", "transform", "projection", "profile",
    "host", "installer", "installed", "consumer", "planning_dag",
    "dependency_contract", "epoch", "contract_validator", "authoritative_root",
    "dynamic_dependencies", "artifact_library", "runner", "verifier",
    "generator_executor", "probe_tool", "enumerator", "code_authority",
}
REQUEST_FIELDS = {
    "record", "evidence_epoch", "purpose",
    "supersession_rule", "artifacts", "affected_dag_edges",
}
RECORD_FIELDS = {
    "record", "decision", "evidence_epoch", "input_digests", "input_kinds",
    "planning_dag_content_digest", "affected_dag_edges", "edge_dispositions",
    "outcome_criteria", "probe_observations", "supersession_rule",
    "evidence_class", "admissible_for", "not_evidence_for", "decision_digest",
    "content_digest",
}
HEX_DIGEST_LENGTH = 64
DECISIONS = {"proceed", "pivot", "narrow"}
CRITERION_STATUSES = {"passed", "failed", "unverified"}
PROBE_STATUSES = {"observed", "unverified", "failed"}
FORBIDDEN_PURPOSES = {"exact-conformance", "promotion", "usability", "tier-award"}
NOT_EVIDENCE_FOR = ["exact-conformance", "promotion", "tier-award", "usability"]
APPROVED_EXECUTION_AUTHORITY_DIGEST = "25e02a64335c707cafcdc261117f6d60530b5082f86c569fa5eea4960bb2a236"
CODE_TOOL_PATHS = {
    "generator": ".github/scripts/build_portable_skill_projection.py",
    "artifact_library": ".github/scripts/skill_artifact_lib.py",
    "contract_validator": ".github/scripts/validate_portability_contract.py",
    "generator_executor": ".github/scripts/execute_portability_generator.py",
    "probe_tool": ".github/scripts/probe_portability_surface.py",
    "enumerator": ".github/scripts/enumerate_dynamic_dependencies.py",
}


class SpikeError(ValueError):
    """A stable fail-closed Stage-A spike refusal."""


def refuse(code: str, detail: str = "") -> None:
    suffix = f": {detail}" if detail else ""
    raise SpikeError(code + suffix)


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == HEX_DIGEST_LENGTH
        and all(character in "0123456789abcdef" for character in value)
    )


def canonical_digest(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def record_digest(record: dict) -> str:
    return canonical_digest({key: value for key, value in record.items() if key != "content_digest"})


def strict_json(path: Path, label: str) -> object:
    try:
        return load_json_strict(path)
    except DuplicateJsonMember as error:
        refuse("SPIKE_DUPLICATE_JSON_MEMBER", f"{label}: {error}")
    except ArtifactError as error:
        refuse("SPIKE_JSON_UNREADABLE", f"{label}: {error}")


def resolve_artifact_path(root: Path, raw: object) -> Path:
    if not isinstance(raw, str):
        refuse("SPIKE_ARTIFACT_DESCRIPTOR_INVALID", "path must be a string")
    pure = PurePosixPath(raw)
    if (
        not raw or pure.is_absolute() or "\\" in raw
        or "." in pure.parts or ".." in pure.parts
    ):
        refuse("SPIKE_ARTIFACT_PATH_ESCAPE", repr(raw))
    candidate = root.joinpath(*pure.parts)
    try:
        candidate.resolve(strict=False).relative_to(root.resolve())
    except ValueError:
        refuse("SPIKE_ARTIFACT_PATH_ESCAPE", raw)
    return candidate


def is_reparse_point(path: Path) -> bool:
    try:
        junction = getattr(path, "is_junction", None)
        return bool((callable(junction) and junction()) or (getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0) & 0x400))
    except OSError:
        return True


def tree_contains_alias(root: Path) -> bool:
    if root.is_symlink() or is_reparse_point(root):return True
    try:
        for current, directories, files in os.walk(root, followlinks=False):
            for name in [*directories, *files]:
                path=Path(current)/name
                if path.is_symlink() or is_reparse_point(path):return True
    except OSError:return True
    return False


def artifact_digest(path: Path, kind: str) -> str:
    if kind == "file":
        if path.is_symlink() or is_reparse_point(path) or not path.is_file():
            refuse("SPIKE_ARTIFACT_TYPE_MISMATCH", str(path))
        try:
            return sha256_bytes(path.read_bytes())
        except OSError as error:
            refuse("SPIKE_ARTIFACT_UNREADABLE", str(error))
    if kind == "tree":
        if not path.is_dir():
            refuse("SPIKE_ARTIFACT_TYPE_MISMATCH", str(path))
        if tree_contains_alias(path):
            refuse("SPIKE_SOURCE_CHECKOUT_LEAKAGE", "tree contains a symlink, junction, or reparse point")
        try:
            return portable_tree_sha256(path)
        except ArtifactError as error:
            refuse("SPIKE_ARTIFACT_UNREADABLE", str(error))
    refuse("SPIKE_ARTIFACT_DESCRIPTOR_INVALID", f"unknown kind {kind!r}")


def validate_request_shape(request: object) -> dict:
    if not isinstance(request, dict):
        refuse("SPIKE_REQUEST_NOT_OBJECT")
    unknown = set(request) - REQUEST_FIELDS
    if unknown:
        refuse("SPIKE_UNKNOWN_FIELD", repr(sorted(unknown)))
    if set(request) != REQUEST_FIELDS:
        refuse("SPIKE_REQUIRED_FIELD_MISSING", repr(sorted(REQUEST_FIELDS - set(request))))
    if request.get("record") != "stage-a-portability-spike-input@1":
        refuse("SPIKE_RECORD_INVALID")
    if request.get("purpose") in FORBIDDEN_PURPOSES:
        refuse("SPIKE_PURPOSE_FORBIDDEN", str(request.get("purpose")))
    if request.get("purpose") != "architecture-decision":
        refuse("SPIKE_PURPOSE_INVALID")
    if not is_nonempty_string(request.get("evidence_epoch")):
        refuse("SPIKE_EVIDENCE_EPOCH_INVALID")
    if not is_nonempty_string(request.get("supersession_rule")):
        refuse("SPIKE_SUPERSESSION_RULE_INVALID")
    artifacts = request.get("artifacts")
    if not isinstance(artifacts, dict) or set(artifacts) != REQUIRED_ARTIFACTS:
        refuse("SPIKE_ARTIFACT_SET_INCOMPLETE")
    for name, descriptor in artifacts.items():
        if (
            not isinstance(descriptor, dict)
            or set(descriptor) != {"kind", "path", "sha256"}
            or descriptor.get("kind") not in {"file", "tree"}
            or not is_nonempty_string(descriptor.get("path"))
            or not is_digest(descriptor.get("sha256"))
        ):
            refuse("SPIKE_ARTIFACT_DESCRIPTOR_INVALID", name)
    affected = request.get("affected_dag_edges")
    if (
        not isinstance(affected, list) or not affected
        or not all(is_nonempty_string(edge) for edge in affected)
        or len(affected) != len(set(affected))
    ):
        refuse("SPIKE_DAG_EDGE_LIST_INVALID")
    return request


def bind_artifacts(root: Path, request: dict) -> tuple[dict[str, Path], dict[str, str]]:
    paths: dict[str, Path] = {}
    digests: dict[str, str] = {}
    for name, descriptor in sorted(request["artifacts"].items()):
        path = resolve_artifact_path(root, descriptor["path"])
        paths[name] = path
        actual = artifact_digest(path, descriptor["kind"])
        if actual != descriptor["sha256"]:
            refuse("SPIKE_DIGEST_MISMATCH", name)
        digests[name] = actual
    source = paths["source"].resolve()
    installed = paths["installed"].resolve()
    if source == installed or source in installed.parents or installed in source.parents:
        refuse("SPIKE_SOURCE_CHECKOUT_LEAKAGE", "source and installed trees overlap")
    source_bytes = str(source).encode("utf-8")
    try:
        if any(source_bytes in path.read_bytes() for path in regular_files(paths["installed"])):
            refuse("SPIKE_SOURCE_CHECKOUT_LEAKAGE", "installed bytes contain source checkout path")
    except ArtifactError as error:
        refuse("SPIKE_SOURCE_CHECKOUT_LEAKAGE", str(error))
    source_ids = set()
    for path in regular_files(paths["source"]):
        stat = path.stat()
        source_ids.add((stat.st_dev, stat.st_ino))
    for path in regular_files(paths["installed"]):
        stat = path.stat()
        if (stat.st_dev, stat.st_ino) in source_ids:
            refuse("SPIKE_SOURCE_CHECKOUT_ALIAS", path.relative_to(paths["installed"]).as_posix())
    return paths, digests


def validate_dependency_closure(source: Path, ir: object, contract: object) -> None:
    if not isinstance(ir, dict) or ir.get("schema") != "zms-skill-ir@1":
        refuse("SPIKE_IR_INVALID")
    if not isinstance(contract, dict) or contract.get("schema") != "zms-skill-dependencies@1":
        refuse("SPIKE_DEPENDENCY_CONTRACT_INVALID")
    skills = ir.get("skills")
    overrides = contract.get("skills")
    if not isinstance(skills, list) or not isinstance(overrides, dict):
        refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH")
    by_name = {entry.get("name"): entry for entry in skills if isinstance(entry, dict) and is_nonempty_string(entry.get("name"))}
    if len(by_name) != len(skills) or set(overrides) - set(by_name):
        refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH")
    for name, skill in by_name.items():
        override = overrides.get(name, {})
        roots = override.get("dependency_roots", []) if isinstance(override, dict) else None
        dependencies = skill.get("dependencies")
        if not isinstance(roots, list) or not all(is_nonempty_string(root) for root in roots) or not isinstance(dependencies, list):
            refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH", name)
        actual: dict[str, tuple[str, str]] = {}
        for dependency in dependencies:
            if (
                not isinstance(dependency, dict)
                or set(dependency) != {"path", "kind", "sha256"}
                or dependency.get("kind") not in {"file", "directory"}
                or not is_nonempty_string(dependency.get("path"))
                or not is_digest(dependency.get("sha256"))
            ):
                refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH", name)
            actual[dependency["path"]] = (dependency["kind"], dependency["sha256"])
        if set(actual) != set(roots) or len(actual) != len(dependencies):
            refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH", name)
        for relative in roots:
            target = resolve_artifact_path(source, relative)
            if target.is_file() and not target.is_symlink():
                expected = ("file", sha256_bytes(target.read_bytes()))
            elif target.is_dir() and not tree_contains_alias(target):
                expected = ("directory", portable_tree_sha256(target))
            else:
                refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH", relative)
            if actual[relative] != expected:
                refuse("SPIKE_DEPENDENCY_CLOSURE_MISMATCH", relative)


def validate_projection_bindings(ir: object, projection: object, profile: object, transform: object, installed: Path) -> None:
    if not all(isinstance(value, dict) for value in (ir, projection, profile, transform)):
        refuse("SPIKE_PROJECTION_BINDING_MISMATCH")
    expected = (
        projection.get("schema") == "zms-projection-result@1"
        and projection.get("source_sha256") == canonical_digest(ir.get("source"))
        and projection.get("profile_sha256") == canonical_digest(profile)
        and ir.get("profile_sha256") == canonical_digest(profile)
        and projection.get("ir_sha256") == canonical_digest(ir)
        and projection.get("generator_revision") == ir.get("generator_revision") == transform.get("generator_revision")
        and projection.get("transform") == profile.get("transform") == transform.get("identifier")
        and transform.get("record") == "projection-transform@1"
        and projection.get("served_tree_sha256") == portable_tree_sha256(installed)
        and projection.get("structural_only") is True
        and projection.get("non_release") is True
    )
    if not expected:
        refuse("SPIKE_PROJECTION_BINDING_MISMATCH")


def validate_bound_documents(documents: dict[str, object], request: dict) -> None:
    profile = documents["profile"]
    profile_fields = {"product", "surface", "release_or_channel", "profile_revision", "transform"}
    if (
        not isinstance(profile, dict) or set(profile) != profile_fields
        or not all(is_nonempty_string(profile.get(field)) for field in profile_fields)
    ):
        refuse("SPIKE_PROFILE_INVALID")
    transform = documents["transform"]
    if (
        not isinstance(transform, dict)
        or set(transform) != {"record", "identifier", "generator_revision"}
        or transform.get("record") != "projection-transform@1"
        or not is_nonempty_string(transform.get("identifier"))
        or not is_nonempty_string(transform.get("generator_revision"))
    ):
        refuse("SPIKE_TRANSFORM_INVALID")
    projection = documents["projection"]
    projection_fields = {
        "schema", "source_sha256", "profile_sha256", "ir_sha256",
        "generator_revision", "transform", "served_tree_sha256",
        "structural_only", "non_release", "never_attests",
    }
    if not isinstance(projection, dict) or set(projection) != projection_fields:
        refuse("SPIKE_PROJECTION_INVALID")
    ir = documents["ir"]
    ir_fields = {
        "schema", "generator_revision", "source", "canonical_package",
        "canonical_package_tree_sha256", "inventory_rule", "profile",
        "profile_sha256", "skill_count", "skills", "structural_only",
        "non_release", "never_attests",
    }
    if not isinstance(ir, dict) or set(ir) != ir_fields:
        refuse("SPIKE_IR_INVALID")
    epoch = documents["epoch"]
    if (
        not isinstance(epoch, dict)
        or set(epoch) != {"record", "current_epoch", "authority"}
        or epoch.get("record") != "evidence-epoch@1"
        or not is_nonempty_string(epoch.get("current_epoch"))
        or not is_nonempty_string(epoch.get("authority"))
    ):
        refuse("SPIKE_EVIDENCE_EPOCH_INVALID")
    host = documents["host"]
    if (
        not isinstance(host, dict)
        or set(host) != {"record", "transcripts"}
        or host.get("record") != "native-probe-transcript-set@1"
        or not isinstance(host.get("transcripts"), list) or not host["transcripts"]
    ):
        refuse("SPIKE_HOST_INVALID")
    consumer = documents["consumer"]
    consumers = consumer.get("consumers") if isinstance(consumer, dict) else None
    if (
        not isinstance(consumer, dict)
        or set(consumer) != {"record", "consumers"}
        or consumer.get("record") != "spike-consumer-set@1"
        or not isinstance(consumers, list)
        or len(consumers) != len(set(consumers))
        or not all(is_nonempty_string(item) for item in consumers)
    ):
        refuse("SPIKE_CONSUMER_INVALID")
    dag = documents["planning_dag"]
    if not isinstance(dag, dict) or set(dag) != {"record", "nodes", "edges", "content_digest", "bindings"}:
        refuse("SPIKE_DAG_INVALID")
    contract = documents["dependency_contract"]
    if (
        not isinstance(contract, dict)
        or set(contract) != {"schema", "defaults", "skills"}
        or not isinstance(contract.get("defaults"), dict)
        or not isinstance(contract.get("skills"), dict)
    ):
        refuse("SPIKE_DEPENDENCY_CONTRACT_INVALID")
    dynamic = documents["dynamic_dependencies"]
    if not isinstance(dynamic, dict) or dynamic.get("record") != "dynamic-dependency-enumeration@1":
        refuse("SPIKE_DYNAMIC_DEPENDENCY_INVENTORY_INVALID")


def validate_code_authority(paths: dict[str, Path], authority: object, request: dict) -> dict:
    fields={"record","authority_id","issuer_identity","probe_issuer_identity","probe_readback_identity","enumerator_issuer_identity","enumerator_readback_identity","platform_scope","tools","content_digest"}
    if not isinstance(authority,dict) or set(authority)!=fields or authority.get("record")!="stage-a-execution-authority@2" or authority.get("issuer_identity")!="operator-authority:ZMS-Labs/epistemic-skills:stage-a-execution-code" or authority.get("platform_scope")!=["linux"] or authority.get("content_digest")!=record_digest(authority) or canonical_digest(authority)!=APPROVED_EXECUTION_AUTHORITY_DIGEST:
        refuse("SPIKE_CODE_AUTHORITY_UNAPPROVED")
    if authority.get("probe_issuer_identity")==authority.get("probe_readback_identity") or authority.get("enumerator_issuer_identity")==authority.get("enumerator_readback_identity"):
        refuse("SPIKE_CODE_AUTHORITY_UNAPPROVED")
    tools=authority.get("tools")
    if not isinstance(tools,dict) or set(tools)!=set(CODE_TOOL_PATHS):refuse("SPIKE_CODE_AUTHORITY_UNAPPROVED")
    for name,relative in CODE_TOOL_PATHS.items():
        item=tools.get(name)
        if not isinstance(item,dict) or set(item)!={"path","sha256"} or item.get("path")!=relative or item.get("sha256")!=request["artifacts"][name]["sha256"] or item.get("sha256")!=sha256_bytes(paths[name].read_bytes()) or request["artifacts"][name]["path"]!=relative:refuse("SPIKE_CODE_NOT_APPROVED",name)
    if request["artifacts"]["code_authority"]["path"]!="authoritative-root/stage-a-execution-authority.json" or paths["code_authority"].read_bytes()!=(paths["authoritative_root"]/'stage-a-execution-authority.json').read_bytes():refuse("SPIKE_CODE_AUTHORITY_UNAPPROVED")
    if request["artifacts"]["runner"]["path"]!=".github/scripts/run_portability_spike.py" or sha256_bytes(Path(__file__).read_bytes())!=request["artifacts"]["runner"]["sha256"]:refuse("SPIKE_RUNNER_NOT_APPROVED")
    if request["artifacts"]["verifier"]["path"]!=".github/scripts/verify_portability_spike_bundle.py":refuse("SPIKE_VERIFIER_NOT_APPROVED")
    return authority


def run_bounded(command: list[str], code: str, timeout: int = 15) -> dict:
    try:
        completed=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=timeout,env={"PATH":os.environ.get("PATH", ""),"LANG":"C","LC_ALL":"C"})
    except BaseException as error:refuse(code,type(error).__name__)
    if completed.returncode!=0:refuse(code,(completed.stdout.strip() or completed.stderr.strip())[:240])
    try:value=json.loads(completed.stdout,object_pairs_hook=lambda pairs: duplicate_rejecting_object(pairs))
    except BaseException as error:refuse(code,type(error).__name__)
    if not isinstance(value,dict):refuse(code)
    return value


def duplicate_rejecting_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate')
        result[key]=value
    return result


def regenerate_derivation(paths: dict[str, Path], documents: dict[str, object], request: dict) -> None:
    with tempfile.TemporaryDirectory(prefix="zms-spike-regen-") as temporary:
        request_path=Path(temporary)/'request.json';request_path.write_bytes(canonical_json_bytes({"source":str(paths['source']),"source_record":documents['ir']['source'],"profile":documents['profile'],"expected_ir":str(paths['ir']),"expected_projection":str(paths['projection']),"expected_installed":str(paths['installed']),"generator":str(paths['generator']),"artifact_library":str(paths['artifact_library'])}))
        verdict=run_bounded([sys.executable,"-I",str(paths['generator_executor']),"--request",str(request_path)],"SPIKE_GENERATOR_EXECUTION_FAILED")
        if verdict.get('record')!='generator-execution-verdict@1' or verdict.get('status')!='passed':refuse("SPIKE_GENERATOR_EXECUTION_FAILED")


def resolve_probe_observations(root: Path, paths: dict[str, Path], authority: dict, epoch: str) -> list[dict]:
    verdict=run_bounded([sys.executable,"-I",str(paths['probe_tool']),"--root",str(root),"--transcripts",str(paths['host']),"--authority",str(paths['code_authority']),"--epoch",epoch],"SPIKE_PROBE_TRANSCRIPT_UNRESOLVED")
    observations=verdict.get('observations') if verdict.get('record')=='native-probe-verdict@1' else None
    if not isinstance(observations,list) or not observations:refuse("SPIKE_PROBE_TRANSCRIPT_UNRESOLVED")
    return observations


def resolve_dynamic_dependencies(paths: dict[str, Path], epoch: str) -> dict:
    verdict=run_bounded([sys.executable,"-I",str(paths['enumerator']),"--source",str(paths['source']),"--ir",str(paths['ir']),"--transcript",str(paths['dynamic_dependencies']),"--authority",str(paths['code_authority']),"--epoch",epoch],"SPIKE_DYNAMIC_ENUMERATION_UNRESOLVED")
    if verdict.get('record')!='dynamic-dependency-verdict@1' or not isinstance(verdict.get('skills'),list):refuse("SPIKE_DYNAMIC_ENUMERATION_UNRESOLVED")
    return verdict


def validate_authoritative_dag(paths: dict[str, Path], documents: dict[str, object], request: dict) -> None:
    if request["artifacts"]["contract_validator"]["path"] != ".github/scripts/validate_portability_contract.py":
        refuse("SPIKE_DAG_AUTHORITY_INVALID")
    authoritative_dag = paths["authoritative_root"] / "planning-dag.json"
    authoritative_epoch = paths["authoritative_root"] / "stage-a-evidence-epoch.json"
    if not authoritative_dag.is_file() or not authoritative_epoch.is_file():
        refuse("SPIKE_DAG_AUTHORITY_INVALID")
    if authoritative_dag.read_bytes() != paths["planning_dag"].read_bytes() or authoritative_epoch.read_bytes() != paths["epoch"].read_bytes():
        refuse("SPIKE_DAG_NOT_AUTHORITATIVE")
    dag = documents["planning_dag"]
    if dag.get("content_digest") != canonical_digest({key: value for key, value in dag.items() if key != "content_digest"}):
        refuse("SPIKE_DAG_CONTENT_DIGEST_MISMATCH")
    verdict=run_bounded([sys.executable,"-I",str(paths["contract_validator"]),"--planning-root",str(paths["authoritative_root"])],"SPIKE_DAG_AUTHORITY_INVALID")
    if verdict.get('valid') is not True or verdict.get('errors')!=[]:refuse("SPIKE_DAG_AUTHORITY_INVALID")


def affected_edges(dag: object) -> list[str]:
    if not isinstance(dag, dict) or dag.get("record") != "planning-dag@1":
        refuse("SPIKE_DAG_INVALID")
    nodes = dag.get("nodes")
    edges = dag.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        refuse("SPIKE_DAG_INVALID")
    node_ids = {node.get("id") for node in nodes if isinstance(node, dict) and is_nonempty_string(node.get("id"))}
    start = "stage-a-portability-spike"
    if len(node_ids) != len(nodes) or start not in node_ids:
        refuse("SPIKE_DAG_INVALID")
    graph = {node: [] for node in node_ids}
    normalized = []
    edge_ids = set()
    for edge in edges:
        if (
            not isinstance(edge, dict) or edge.get("from") not in node_ids or edge.get("to") not in node_ids
            or not is_nonempty_string(edge.get("transition_artifact"))
        ):
            refuse("SPIKE_DAG_INVALID")
        edge_id = edge["transition_artifact"]
        if edge_id in edge_ids:
            refuse("SPIKE_DAG_INVALID", "duplicate edge identifier")
        edge_ids.add(edge_id)
        graph[edge["from"]].append(edge["to"])
        normalized.append(edge)
    reachable = {start}
    todo = [start]
    while todo:
        current = todo.pop()
        for target in graph[current]:
            if target not in reachable:
                reachable.add(target)
                todo.append(target)
    return sorted(edge["transition_artifact"] for edge in normalized if edge["from"] in reachable)


def derive_decision(criteria: list[dict]) -> str:
    statuses = {criterion["status"] for criterion in criteria}
    if "failed" in statuses:
        return "pivot"
    if "unverified" in statuses:
        return "narrow"
    return "proceed"


def derive_criteria(observations: list[dict], dynamic: dict) -> list[dict]:
    criteria = [
        {"id": "exact-generator-regeneration", "status": "passed", "detail": "bound generator reproduced exact IR, projection result, and installed tree"},
        {"id": "source-checkout-isolation", "status": "passed", "detail": "installed tree has no source alias and remains unchanged after disposable source removal"},
        {"id": "platform-scope:linux", "status": "passed" if sys.platform.startswith("linux") else "unverified", "detail": "junction/reparse and mutation-independence evidence is currently scoped to Linux"},
    ]
    probe_status = {"observed": "passed", "unverified": "unverified", "failed": "failed"}
    for probe in observations:
        criteria.append({"id": f"native:{probe['product']}:{probe['surface']}", "status": probe_status[probe["status"]], "detail": probe["reason"]})
    unresolved = sorted(item["name"] for item in dynamic["skills"] if item["state"] == "unresolved")
    criteria.append({"id": "dynamic-dependency-inventory", "status": "unverified" if unresolved else "passed", "detail": "unresolved: " + ",".join(unresolved) if unresolved else "all dynamic dependency inventories explicitly resolved as none"})
    return sorted(criteria, key=lambda item: item["id"])


def decision_subject(record: dict) -> dict:
    return {
        "record": record.get("record"), "decision": record.get("decision"),
        "evidence_epoch": record.get("evidence_epoch"), "input_digests": record.get("input_digests"),
        "input_kinds": record.get("input_kinds"), "planning_dag_content_digest": record.get("planning_dag_content_digest"),
        "affected_dag_edges": record.get("affected_dag_edges"), "edge_dispositions": record.get("edge_dispositions"),
        "outcome_criteria": record.get("outcome_criteria"), "probe_observations": record.get("probe_observations"),
        "supersession_rule": record.get("supersession_rule"), "evidence_class": record.get("evidence_class"),
        "admissible_for": record.get("admissible_for"), "not_evidence_for": record.get("not_evidence_for"),
    }


def validate_spike_record(record: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return ["SPIKE_RECORD_NOT_OBJECT"]
    if set(record) != RECORD_FIELDS or record.get("record") != "stage-a-portability-spike@1":
        errors.append("SPIKE_RECORD_SHAPE_INVALID")
    criteria = record.get("outcome_criteria")
    expected_decision = derive_decision(criteria) if isinstance(criteria, list) and criteria and all(isinstance(item, dict) and item.get("status") in CRITERION_STATUSES for item in criteria) else None
    if record.get("decision") not in DECISIONS or record.get("decision") != expected_decision:
        errors.append("SPIKE_DECISION_MISMATCH")
    affected = record.get("affected_dag_edges")
    dispositions = record.get("edge_dispositions")
    expected_disposition = "eligible-for-next-gate" if expected_decision == "proceed" else "blocked"
    if (
        not isinstance(affected, list) or not isinstance(dispositions, list)
        or dispositions != [{"edge_id": edge, "disposition": expected_disposition} for edge in affected]
    ):
        errors.append("SPIKE_EDGE_DISPOSITION_MISMATCH")
    if record.get("evidence_class") != "non-causal-decision-support" or record.get("admissible_for") != ["architecture-decision"] or record.get("not_evidence_for") != NOT_EVIDENCE_FOR:
        errors.append("SPIKE_EVIDENCE_CLASS_INVALID")
    digests = record.get("input_digests")
    kinds = record.get("input_kinds")
    if not isinstance(digests, dict) or set(digests) != REQUIRED_ARTIFACTS or not all(is_digest(value) for value in digests.values()) or not isinstance(kinds, dict) or set(kinds) != REQUIRED_ARTIFACTS:
        errors.append("SPIKE_INPUT_BINDING_INVALID")
    if record.get("decision_digest") != canonical_digest(decision_subject(record)):
        errors.append("SPIKE_DECISION_DIGEST_MISMATCH")
    if record.get("content_digest") != record_digest(record):
        errors.append("SPIKE_CONTENT_DIGEST_MISMATCH")
    return sorted(set(errors))


def generate_record(root: Path, request: object) -> dict:
    request = validate_request_shape(request)
    paths, digests = bind_artifacts(root.resolve(), request)
    documents = {name: strict_json(paths[name], name) for name in ("ir", "transform", "projection", "profile", "host", "consumer", "planning_dag", "dependency_contract", "epoch", "dynamic_dependencies", "code_authority")}
    validate_bound_documents(documents, request)
    authority=validate_code_authority(paths,documents["code_authority"],request)
    epoch = documents["epoch"]
    if not isinstance(epoch, dict) or epoch.get("record") != "evidence-epoch@1" or epoch.get("current_epoch") != request["evidence_epoch"]:
        refuse("SPIKE_EVIDENCE_EPOCH_STALE")
    validate_dependency_closure(paths["source"], documents["ir"], documents["dependency_contract"])
    validate_authoritative_dag(paths, documents, request)
    regenerate_derivation(paths, documents, request)
    validate_projection_bindings(documents["ir"], documents["projection"], documents["profile"], documents["transform"], paths["installed"])
    required_edges = affected_edges(documents["planning_dag"])
    if sorted(request["affected_dag_edges"]) != required_edges:
        refuse("SPIKE_DAG_EDGE_CLOSURE_MISMATCH")
    observations=resolve_probe_observations(root.resolve(),paths,authority,request["evidence_epoch"])
    expected_consumers={f"{item['product']}|{item['surface']}" for item in observations}
    if set(documents['consumer']['consumers'])!=expected_consumers:refuse("SPIKE_CONSUMER_INVALID")
    dynamic=resolve_dynamic_dependencies(paths,request["evidence_epoch"])
    criteria = derive_criteria(observations, dynamic)
    decision = derive_decision(criteria)
    disposition = "eligible-for-next-gate" if decision == "proceed" else "blocked"
    dag_content = documents["planning_dag"].get("content_digest")
    if not is_nonempty_string(dag_content):
        refuse("SPIKE_DAG_INVALID", "missing content digest")
    record = {
        "record": "stage-a-portability-spike@1", "decision": decision,
        "evidence_epoch": request["evidence_epoch"], "input_digests": dict(sorted(digests.items())),
        "input_kinds": {name: request["artifacts"][name]["kind"] for name in sorted(REQUIRED_ARTIFACTS)},
        "planning_dag_content_digest": dag_content, "affected_dag_edges": required_edges,
        "edge_dispositions": [{"edge_id": edge, "disposition": disposition} for edge in required_edges],
        "outcome_criteria": criteria,
        "probe_observations": sorted(observations, key=lambda item: (item["product"], item["surface"])),
        "supersession_rule": request["supersession_rule"], "evidence_class": "non-causal-decision-support",
        "admissible_for": ["architecture-decision"], "not_evidence_for": NOT_EVIDENCE_FOR,
    }
    record["decision_digest"] = canonical_digest(decision_subject(record))
    record["content_digest"] = record_digest(record)
    errors = validate_spike_record(record)
    if errors:
        refuse(errors[0])
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.out.exists():
        refuse("SPIKE_OUTPUT_EXISTS", str(args.out))
    request = strict_json(args.request, "request")
    record = generate_record(args.root, request)
    try:
        args.out.write_bytes(canonical_json_bytes(record))
    except OSError as error:
        refuse("SPIKE_OUTPUT_WRITE_FAILED", str(error))
    print(record["decision"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SpikeError as error:
        print(f"REFUSED {error}")
        raise SystemExit(2) from None
