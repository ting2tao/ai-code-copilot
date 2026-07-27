#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"progressive-sdd: {message}")


def read_text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def should_activate(policy: dict, facts: dict) -> bool:
    activation = policy["activation"]
    if facts.get("explicitIntent") in activation["explicitIntents"]:
        return True
    signals = set(facts.get("signals", []))
    if signals & set(activation["mustActivateSignals"]):
        return True
    return False


def classify_activated(policy: dict, facts: dict) -> str:
    risks = set(facts.get("risks", []))
    full_risks = set(policy["tiers"]["full"]["riskCategories"])
    if (
        risks & full_risks
        or facts.get("acceptedResidualRisk", False)
        or facts.get("files", 0) > policy["tiers"]["compact"]["maxFiles"]
        or facts.get("multipleDeliverableGoals", False)
        or facts.get("multipleReviewUnits", False)
    ):
        return "full"
    return "compact"


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    policy = json.loads(read_text(root / "config/workflow-policy.json"))
    if policy.get("version") != 2:
        fail("workflow policy version must be 2")
    if policy["github"]["newProjectDefault"] != "on-publish":
        fail("new projects must default issuePolicy to on-publish")
    if policy["github"]["legacyDefault"] != "always":
        fail("legacy projects without issuePolicy must default to always")
    if policy["github"].get("manualNoIssueCloseTarget") != "none":
        fail("manual projects without an Issue must use closeTarget none")
    activation_fixtures = [
        (
            {
                "signals": [],
            },
            False,
        ),
        (
            {
                "signals": ["security"],
            },
            True,
        ),
        (
            {
                "explicitIntent": "finish",
            },
            True,
        ),
        (
            {
                "signals": ["session-handoff"],
            },
            True,
        ),
    ]
    for facts, expected in activation_fixtures:
        actual = should_activate(policy, facts)
        if actual != expected:
            fail(f"activation expected {expected}, got {actual}: {facts}")

    tier_fixtures = [
        (
            {
                "files": 2,
            },
            "compact",
        ),
        (
            {
                "files": 6,
            },
            "full",
        ),
        (
            {
                "files": 1,
                "risks": ["public-api"],
            },
            "full",
        ),
    ]
    for facts, expected in tier_fixtures:
        actual = classify_activated(policy, facts)
        if actual != expected:
            fail(f"classifier expected {expected}, got {actual}: {facts}")
    for risk in policy["tiers"]["full"]["riskCategories"]:
        actual = classify_activated(
            policy,
            {
                "files": 1,
                "risks": [risk],
            },
        )
        if actual != "full":
            fail(f"full risk must classify as full: {risk}")

    required_modules = [
        "init.md",
        "compact.md",
        "full.md",
        "debug.md",
        "review.md",
        "test.md",
        "finish.md",
        "archive.md",
    ]
    router = read_text(root / "agents/router.md")
    for name in required_modules:
        read_text(root / "agents/workflows" / name)
        if f"agents/workflows/{name}" not in router:
            fail(f"router missing module reference: {name}")
    skill = read_text(root / "skill/SKILL.md")
    if "agents/router.md" not in skill:
        fail("skill must load agents/router.md")
    if "回退加载单体提示词" not in skill:
        fail("skill must reject monolithic prompt fallback")

    quick_card = read_text(root / "changes/templates/quick-card.md")
    for marker in [
        "promotedFrom:",
        "promotedFrom: native",
        "Promotion record",
        "previous contract",
        "evidence copied",
        "material confirmation",
    ]:
        if marker not in quick_card:
            fail(f"quick-card missing promotion marker: {marker}")
    spec_reviewer = read_text(root / "agents/spec-reviewer.md")
    for marker in [
        "Native -> Compact",
        "Native -> Full",
        "mechanical Reverse Sync",
        "material Reverse Sync",
    ]:
        if marker not in spec_reviewer:
            fail(f"spec reviewer missing progressive SDD marker: {marker}")

    native_escalation_records = {
        "agents/workflows/compact.md": [
            "Native -> Compact",
            "promotedFrom: native",
        ],
        "agents/workflows/full.md": [
            "Native -> Full",
            "material confirmation",
        ],
        "agents/code-quality-reviewer.md": ["Native -> Compact"],
    }
    for relative, markers in native_escalation_records.items():
        content = read_text(root / relative)
        for marker in markers:
            if marker not in content:
                fail(f"{relative} missing native escalation marker: {marker}")

    active_runtime_files = [
        "agents/workflows/compact.md",
        "agents/workflows/full.md",
        "agents/workflows/debug.md",
        "agents/workflows/review.md",
        "agents/workflows/finish.md",
        "agents/workflows/archive.md",
        "agents/spec-reviewer.md",
        "agents/code-quality-reviewer.md",
        "changes/templates/quick-card.md",
        "changes/templates/summary.md",
    ]
    stale_inline_markers = [
        "Inline SDD",
        "Inline -> Compact",
        "Inline -> Full",
        "promotedFrom: inline",
        "promoted-from: none | inline",
    ]
    for relative in active_runtime_files:
        content = read_text(root / relative)
        for marker in stale_inline_markers:
            if marker in content:
                fail(f"{relative} contains stale Inline marker: {marker}")

    project_config = json.loads(read_text(root / "config/project-config.json"))
    if project_config.get("githubWorkflow", {}).get("issuePolicy") != "on-publish":
        fail("new project config must default issuePolicy to on-publish")
    finish = read_text(root / "agents/workflows/finish.md")
    for marker in [
        "always",
        "on-commit",
        "on-publish",
        "manual",
        "legacy default: always",
        "Closes #<workIssue>",
        "Refs #<parentIssue>",
        "workIssue: none",
        "issueRelationship: none",
        "closeTarget: none",
        "省略所有 closing keyword",
    ]:
        if marker not in finish:
            fail(f"finish module missing issue policy marker: {marker}")

    manual_no_issue_records = {
        "changes/templates/quick-card.md": ["none (manual only)", "manual/no-Issue"],
        "changes/templates/spec.md": ["manual/no-Issue", "none"],
        "changes/templates/summary.md": ["none (manual only)"],
        "changes/templates/tasks.md": ["manual/no-Issue", "closeTarget 为 none"],
        "changes/templates/log.md": ["manual/no-Issue", "closing keyword"],
        "rules/commit-convention.md": ["workIssue: none", "closeTarget: none"],
    }
    for relative, markers in manual_no_issue_records.items():
        content = read_text(root / relative)
        for marker in markers:
            if marker not in content:
                fail(f"{relative} missing manual/no-Issue marker: {marker}")

    docs = {
        "README.md": [
            "Inline SDD",
            "Compact SDD",
            "Full SDD",
            "issuePolicy",
            "agents/router.md",
        ],
        "README-CN.md": [
            "Inline SDD",
            "Compact SDD",
            "Full SDD",
            "issuePolicy",
            "agents/router.md",
        ],
        "AGENTS.md": ["agents/router.md", "agents/workflows/", "Inline SDD", "单向升级"],
        "docs/ai-code-copilot-overview.md": [
            "Inline SDD",
            "Compact SDD",
            "Full SDD",
        ],
    }
    for relative, markers in docs.items():
        content = read_text(root / relative)
        for marker in markers:
            if marker not in content:
                fail(f"{relative} missing documentation marker: {marker}")
    print("progressive-sdd: policy and module checks passed")


if __name__ == "__main__":
    main()
