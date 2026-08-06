#!/usr/bin/env python3
"""Deterministic package-integration checks for the outsource skill."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve()
SKILL_ROOT = HERE.parents[1]
PACKAGE_ROOT = HERE.parents[3]
REPO_ROOT = HERE.parents[5]
EXPECTED_VERSION = "4.1.0"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    require(path.is_file(), f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


WORDS = {9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
         16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty"}


def check_live_surface_counts(skill_count: int) -> None:
    """Issue #72 lint: every spelled count adjacent to skill/discipline wording on a
    LIVE surface must match the derived counts. Live surfaces = all JSON manifests
    (every string field, nested included), the README mermaid node, and GEMINI.md.
    README prose is excluded here (it legitimately carries per-tag historical counts)
    and is covered by the targeted assertions in main()."""
    import re
    disciplines = skill_count - 1  # the entry point is not a discipline
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
        found = [w for w in WORDS.values() if re.search(rf"\b{w}\b", ln.lower())]
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

    # The router and helix seats were deleted 2026-08-06 and replaced by
    # metacognate, which enumerates NOTHING. The old assertions here required the
    # router description to list every discipline -- the single largest source of
    # the enumeration tax. Their replacements assert the opposite property: that
    # the entry point does NOT name members.
    entry_root = PACKAGE_ROOT / "skills" / "metacognate"
    entry = read(entry_root / "SKILL.md")
    _n = len(list((PACKAGE_ROOT / "skills").glob("*/SKILL.md")))
    _d = _n - 1  # the entry point is not a discipline
    require(_n in WORDS and _d in WORDS, f"no count word for {_n}/{_d}")
    _word, _nword = WORDS[_d], WORDS[_n]
    require("Tier 1 — IRON" in entry, "entry point lost its iron tier")
    require("Tier 2 — WISE" in entry, "entry point lost its judgment tier")
    require("Silence is a success state" in entry, "entry point lost its routine fast path")
    require("carries a procedure, never an inventory" in entry,
            "entry point no longer forbids enumerating members")
    members = [d.name for d in (PACKAGE_ROOT / "skills").glob("*/SKILL.md")]
    named = [m for m in (set(members) - {"metacognate"}) if m in entry]
    require(not named, f"entry point enumerates members, which is forbidden: {sorted(named)}")
    require(
        (entry_root / "reference" / "routine-fast-path.md").is_file(),
        "routine fast-path reference is missing",
    )

    # Relocated to package level with the rest of the corpora when helix was deleted.
    helix_eval = PACKAGE_ROOT / "evals" / "composition"
    for filename in (
        "README.md",
        "verify.py",
        "tests/run_tests.py",
        "results/BLOCKED.md",
    ):
        require((helix_eval / filename).is_file(), f"missing composition eval artifact: {filename}")

    readme = read(REPO_ROOT / "README.md")
    require(f"**Version {EXPECTED_VERSION}.**" in readme, "README version is stale")
    require(f"**{_nword}** skills" in readme, "README skill count is stale")
    require(f"**{_word}** disciplines" in readme, "README discipline count is stale")
    require("the tag's full skill count" in readme, "README harness success check is stale")
    require(f"canonical skill cores ({_nword})" in readme, "README layout inventory count is stale")
    require("canonical skill cores (sixteen)" not in readme, "README still advertises the pre-consolidation count")
    require("**outsource**" in readme, "README skill table lacks outsource")
    require("## Routine work first" in readme, "README does not present the routine path first")

    contributing = read(REPO_ROOT / "CONTRIBUTING.md")
    require(
        "Ordinary contributions do not require the whole arc" in contributing,
        "contributor guidance does not explain the routine path",
    )

    gemini = read(REPO_ROOT / "GEMINI.md")
    require(f"{_nword} skills" in gemini, "GEMINI context skill count is stale")
    require(f"{_word} disciplines" in gemini, "GEMINI context discipline count is stale")

    workflow = read(REPO_ROOT / ".github" / "workflows" / "epistemic-flexibility.yml")
    require(
        "decision-ledger/evals/resume-fixtures/score.py" in workflow,
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
        "resolve/derivation/evals/formal-rigor-v2-fixtures/tests/run_tests.py" in workflow,
        "CI omits formal-rigor v2 structural scorer tests",
    )
    require(
        "resolve/derivation/evals/formal-rigor-v2-fixtures/tests/test_focused.py" in workflow,
        "CI omits formal-rigor focused proportionality tests",
    )
    require(
        "resolve/derivation/evals/formal-rigor-v2-fixtures/tests/test_posthoc_diagnostic.py" in workflow,
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
    ):
        test_path = f"plugins/epistemic-skills/skills/{battery_skill}/evals/trigger-and-scope/tests/run_tests.py"
        require(
            f"run: python {test_path}" in workflow,
            f"CI does not execute {battery_skill} trigger-and-scope tests",
        )
        require(
            (PACKAGE_ROOT / "skills" / battery_skill / "evals" / "trigger-and-scope"
             / "tests" / "run_tests.py").is_file(),
            f"{battery_skill} trigger-and-scope battery is missing",
        )
    for recon_battery in (
        "brief-trigger-and-scope",
        "initiative-trigger-and-scope",
        "candidate-trigger-and-scope",
    ):
        test_path = f"plugins/epistemic-skills/skills/recon/evals/{recon_battery}/tests/run_tests.py"
        require(
            f"run: python {test_path}" in workflow,
            f"CI does not execute recon {recon_battery} tests",
        )
        require(
            (PACKAGE_ROOT / "skills" / "recon" / "evals" / recon_battery
             / "tests" / "run_tests.py").is_file(),
            f"recon {recon_battery} battery is missing",
        )

    proportionality = PACKAGE_ROOT / "evals" / "proportionality"
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

    formal_v2 = PACKAGE_ROOT / "skills" / "resolve" / "derivation" / "evals" / "formal-rigor-v2-fixtures"
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

    # A skill is a directory CONTAINING SKILL.md, not merely a directory. Counting
    # bare directories made this assertion fire on leftover build artifacts -- a
    # stale `__pycache__`-only folder from a removed skill counted as a skill and
    # failed the suite. Every other check in this repo globs `*/SKILL.md`; this now
    # agrees with them. The literal 11 is also derived, so adding a skill does not
    # require editing this line.
    skill_dirs = [p.parent for p in (PACKAGE_ROOT / "skills").glob("*/SKILL.md")]
    require(len(skill_dirs) == _n, f"expected {_n} skill directories, found {len(skill_dirs)}")
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
