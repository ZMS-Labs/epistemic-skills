#!/usr/bin/env python3
"""Deterministic package-integration checks for the outsource skill."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve()
SKILL_ROOT = HERE.parents[1]
PACKAGE_ROOT = HERE.parents[3]
REPO_ROOT = HERE.parents[5]
EXPECTED_VERSION = "3.4.0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


WORDS = {11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
         16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}


def check_live_surface_counts(skill_count: int) -> None:
    """Issue #72 lint: every spelled count adjacent to skill/discipline wording on a
    LIVE surface must match the derived counts. Live surfaces = all JSON manifests
    (every string field, nested included), the README mermaid node, and GEMINI.md.
    README prose is excluded here (it legitimately carries per-tag historical counts)
    and is covered by the targeted assertions in main()."""
    import re
    disciplines = skill_count - 2  # router + helix are not disciplines
    ok_words = {WORDS[skill_count], WORDS[disciplines]}
    count_re = re.compile(
        r"\b(" + "|".join(WORDS.values()) + r")\b(?=[^.;]{0,60}(?:skill|discipline))",
        re.IGNORECASE)

    def strings_of(obj):
        if isinstance(obj, str):
            yield obj
        elif isinstance(obj, dict):
            for v in obj.values():
                yield from strings_of(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from strings_of(v)

    manifests = [
        REPO_ROOT / ".claude-plugin" / "marketplace.json",
        REPO_ROOT / ".cursor-plugin" / "marketplace.json",
        REPO_ROOT / ".cursor-plugin" / "plugin.json",
        REPO_ROOT / ".kimi-plugin" / "marketplace.json",
        REPO_ROOT / ".kimi-plugin" / "plugin.json",
        REPO_ROOT / "gemini-extension.json",
        REPO_ROOT / "plugin.json",
        PACKAGE_ROOT / ".claude-plugin" / "plugin.json",
        PACKAGE_ROOT / ".codex-plugin" / "plugin.json",
        PACKAGE_ROOT / ".cursor-plugin" / "plugin.json",
        PACKAGE_ROOT / ".kimi-plugin" / "plugin.json",
    ]
    for mp in manifests:
        data = json.loads(read(mp))
        for s in strings_of(data):
            for m in count_re.finditer(s):
                require(m.group(1).lower() in ok_words,
                        f"stale count word {m.group(1)!r} on live surface {mp.name}: ...{s[max(0,m.start()-30):m.end()+40]}...")
    readme = read(REPO_ROOT / "README.md")
    mermaid = [ln for ln in readme.splitlines() if "router and" in ln and "disciplines" in ln]
    for ln in mermaid:
        found = [w for w in WORDS.values() if w in ln.lower()]
        for w in found:
            require(w in ok_words, f"README mermaid node count stale: {ln.strip()}")
    gemini = read(REPO_ROOT / "GEMINI.md")
    for m in count_re.finditer(gemini):
        require(m.group(1).lower() in ok_words,
                f"stale count word {m.group(1)!r} in GEMINI.md")


def main() -> int:
    skill = read(SKILL_ROOT / "SKILL.md")
    require(skill.startswith("---\nname: outsource\n"), "invalid skill frontmatter/name")
    for phrase in (
        "docs/outsource/<work-id>/HANDOFF.md",
        "## Context-erasure test",
        "## Output contract",
        "## Workflow",
        "## Relay loop",
        "## Stop conditions",
        "https://github.com/<owner>/<repo>/blob/<commit>/docs/outsource/<work-id>/HANDOFF.md",
        "canonical outbound prompt template",
        "{packet_commit}",
    ):
        require(phrase in skill, f"SKILL.md missing contract phrase: {phrase}")
    require(
        "Store the exact outbound prompt" not in skill,
        "publication workflow still requires a commit to contain its own hash",
    )

    template = read(SKILL_ROOT / "reference" / "HANDOFF_TEMPLATE.md")
    for heading in (
        "# Outsource handoff:",
        "## Repository and source",
        "## Required outcome",
        "## Context map",
        "## Requirements",
        "## Completion contract",
        "## Authority and boundaries",
        "## Relay response contract",
    ):
        require(heading in template, f"handoff template missing heading: {heading}")
    require(
        "Packet commit | `supplied by the immutable prompt URL after publication`" in template,
        "handoff template does not use the prompt URL as the packet commit coordinate",
    )
    require(
        "Prepared commit | `<40-character Git commit>`" not in template,
        "handoff template still requires an impossible self-embedded commit",
    )

    router_root = PACKAGE_ROOT / "skills" / "using-epistemic-skills"
    router = read(router_root / "SKILL.md")
    require("These fifteen disciplines" in router, "router discipline count is stale")
    require("**outsource**" in router, "router does not route outsource")
    require("why these fifteen" in router, "router family-resemblance count is stale")
    require("Routine work leaves before the arc" in router, "router lacks routine-work exit")
    require("Absent triggers are silent" in router, "router still requires absent-trigger records")
    require(
        (router_root / "reference" / "routine-fast-path.md").is_file(),
        "routine fast-path reference is missing",
    )

    helix_root = PACKAGE_ROOT / "skills" / "helix"
    helix = read(helix_root / "SKILL.md")
    require("external delegation / model handoff" in helix, "helix lacks outsource pairing")
    require("Do **not** emit a line for an absent trigger" in helix, "helix still records non-events")
    require("continuity-verify → blindspot-pass" in helix, "helix lacks pre-arc resumption ordering")
    require("zero, one, or ordered set" in helix, "helix still implies single-pair selection")
    helix_contract = json.loads(read(helix_root / "reference" / "composition-contract.json"))
    require(
        helix_contract.get("schema") == "helix-composition-contract@1",
        "helix composition contract schema is missing or stale",
    )
    require(
        len(helix_contract.get("members", {})) == 15,
        "helix composition contract does not classify all fifteen disciplines",
    )
    helix_eval = helix_root / "evals" / "composition"
    for filename in (
        "README.md",
        "verify.py",
        "tests/run_tests.py",
        "results/BLOCKED.md",
    ):
        require((helix_eval / filename).is_file(), f"missing Helix composition artifact: {filename}")

    readme = read(REPO_ROOT / "README.md")
    require(f"**Version {EXPECTED_VERSION}.**" in readme, "README version is stale")
    require("**seventeen** skills" in readme, "README skill count is stale")
    require("**fifteen** disciplines" in readme, "README discipline count is stale")
    require("all seventeen skills" in readme, "README harness success check is stale")
    require("canonical skill cores (seventeen)" in readme, "README layout inventory count is stale")
    require("canonical skill cores (fourteen)" not in readme, "README still advertises twelve skill cores")
    require("**outsource**" in readme, "README skill table lacks outsource")
    require("## Routine work first" in readme, "README does not present the routine path first")

    contributing = read(REPO_ROOT / "CONTRIBUTING.md")
    require(
        "Ordinary contributions do not require the whole arc" in contributing,
        "contributor guidance does not explain the routine path",
    )

    gemini = read(REPO_ROOT / "GEMINI.md")
    require("seventeen skills" in gemini, "GEMINI context skill count is stale")
    require("fifteen disciplines" in gemini, "GEMINI context discipline count is stale")

    workflow = read(REPO_ROOT / ".github" / "workflows" / "epistemic-flexibility.yml")
    require(
        "continuity-verify/evals/resume-fixtures/score.py" in workflow,
        "CI omits continuity-verify committed-result scoring",
    )
    require(
        "helix/evals/composition/tests/run_tests.py" in workflow,
        "CI omits Helix composition contract tests",
    )
    require(
        "python .github/scripts/test_check_dco.py" in workflow,
        "CI omits DCO policy unit tests",
    )
    require(
        "evals/proportionality/run_tests.py" in workflow,
        "CI omits proportionality scorer polarity tests",
    )
    require(
        "evals/proportionality/blinded/tests/run_tests.py" in workflow,
        "CI omits blinded proportionality packet tests",
    )
    require(
        "applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/run_tests.py" in workflow,
        "CI omits formal-rigor v2 structural scorer tests",
    )
    require(
        "applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_focused.py" in workflow,
        "CI omits formal-rigor focused proportionality tests",
    )
    require(
        "applying-formal-rigor/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py" in workflow,
        "CI omits formal-rigor V3 post-hoc diagnostic tests",
    )
    require(
        "evidence-locked-uat/evals/triage/tests/run_tests.py" in workflow,
        "CI omits UAT proportionality triage tests",
    )
    require(
        "decision-ledger/evals/proportionality/tests/run_tests.py" in workflow,
        "CI omits Decision Ledger proportionality tests",
    )
    require(
        "open-questions/evals/trigger-and-scope/tests/run_tests.py" in workflow,
        "CI omits Open Questions trigger-and-scope tests",
    )
    for battery_skill in (
        "context-audit",
        "agent-interface-design",
        "wayfinding",
        "throwaway-prototyping",
        "intent-traced-merge",
    ):
        require(
            f"{battery_skill}/evals/trigger-and-scope/tests/run_tests.py" in workflow,
            f"CI omits {battery_skill} trigger-and-scope tests",
        )
        require(
            (PACKAGE_ROOT / "skills" / battery_skill / "evals" / "trigger-and-scope"
             / "tests" / "run_tests.py").is_file(),
            f"{battery_skill} trigger-and-scope battery is missing",
        )

    proportionality = router_root / "evals" / "proportionality"
    for filename in (
        "README.md",
        "fixtures.json",
        "score.py",
        "run_tests.py",
        "examples/balanced.json",
        "examples/full-ceremony.json",
        "examples/always-routine.json",
        "blinded/README.md",
        "blinded/arms.json",
        "blinded/scenarios.json",
        "blinded/runner.py",
        "blinded/results/BLOCKED.md",
        "blinded/tests/run_tests.py",
    ):
        require((proportionality / filename).is_file(), f"missing proportionality artifact: {filename}")

    formal_v2 = PACKAGE_ROOT / "skills" / "applying-formal-rigor" / "evals" / "formal-rigor-v2-fixtures"
    for filename in (
        "README.md",
        "formal-rigor-fixture-response.schema.json",
        "formal-rigor-record.schema.json",
        "score.py",
        "semantic-adjudication.md",
        "posthoc_diagnostic.py",
        "tests/run_tests.py",
        "tests/test_focused.py",
        "tests/test_posthoc_diagnostic.py",
        "results/BLOCKED.md",
    ):
        require((formal_v2 / filename).is_file(), f"missing formal-rigor v2 artifact: {filename}")

    proportionality_suites = (
        PACKAGE_ROOT / "skills" / "evidence-locked-uat" / "evals" / "triage",
        PACKAGE_ROOT / "skills" / "decision-ledger" / "evals" / "proportionality",
    )
    for suite in proportionality_suites:
        for filename in ("README.md", "fixtures.json", "score.py", "tests/run_tests.py"):
            require((suite / filename).is_file(), f"missing proportionality artifact: {suite.name}/{filename}")

    skill_dirs = [p for p in (PACKAGE_ROOT / "skills").iterdir() if p.is_dir()]
    require(len(skill_dirs) == 17, f"expected 17 skill directories, found {len(skill_dirs)}")
    check_live_surface_counts(len(skill_dirs))
    for directory in skill_dirs:
        require((directory / "SKILL.md").is_file(), f"missing SKILL.md: {directory.name}")

    manifests = (
        REPO_ROOT / "gemini-extension.json",
        REPO_ROOT / ".claude-plugin" / "marketplace.json",
        REPO_ROOT / ".cursor-plugin" / "plugin.json",
        REPO_ROOT / ".cursor-plugin" / "marketplace.json",
        REPO_ROOT / ".kimi-plugin" / "plugin.json",
        PACKAGE_ROOT / ".claude-plugin" / "plugin.json",
        PACKAGE_ROOT / ".codex-plugin" / "plugin.json",
        PACKAGE_ROOT / ".cursor-plugin" / "plugin.json",
        PACKAGE_ROOT / ".kimi-plugin" / "plugin.json",
    )
    for path in manifests:
        data = json.loads(read(path))
        version = data.get("version") or data.get("metadata", {}).get("version")
        require(version == EXPECTED_VERSION, f"stale version in {path}")
        text = json.dumps(data).lower()
        require("outsource" in text, f"manifest does not advertise outsource: {path}")

    require(
        "outsource" in json.loads(read(REPO_ROOT / "plugin.json"))["description"].lower(),
        "Antigravity manifest does not advertise outsource",
    )

    print("outsource integration: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
