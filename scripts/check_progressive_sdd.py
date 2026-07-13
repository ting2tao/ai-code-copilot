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


def classify(policy: dict, facts: dict) -> str:
    risks = set(facts.get("risks", []))
    full_risks = set(policy["tiers"]["full"]["riskCategories"])
    if risks & full_risks or facts.get("acceptedResidualRisk", False):
        return "full"
    inline = policy["tiers"]["inline"]
    if (
        facts.get("files", 0) > inline["maxFiles"]
        or facts.get("purposes", 1) > inline["maxPurposes"]
        or facts.get("commits", 1) > inline["maxCommits"]
        or not facts.get("executableVerification", False)
        or not facts.get("directRollback", False)
        or facts.get("persistedLifecycle", False)
    ):
        return "compact"
    return "inline"


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    policy = json.loads(read_text(root / "config/workflow-policy.json"))
    if policy.get("version") != 1:
        fail("workflow policy version must be 1")
    if policy["github"]["newProjectDefault"] != "on-publish":
        fail("new projects must default issuePolicy to on-publish")
    if policy["github"]["legacyDefault"] != "always":
        fail("legacy projects without issuePolicy must default to always")
    fixtures = [
        (
            {
                "files": 2,
                "executableVerification": True,
                "directRollback": True,
            },
            "inline",
        ),
        (
            {
                "files": 3,
                "executableVerification": True,
                "directRollback": True,
            },
            "compact",
        ),
        (
            {
                "files": 1,
                "executableVerification": True,
                "directRollback": True,
                "risks": ["public-api"],
            },
            "full",
        ),
    ]
    for facts, expected in fixtures:
        actual = classify(policy, facts)
        if actual != expected:
            fail(f"classifier expected {expected}, got {actual}: {facts}")

    required_modules = [
        "init.md",
        "inline.md",
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
    if "agents/copilot-prompt.md" not in skill:
        fail("skill must retain the legacy prompt fallback")

    quick_card = read_text(root / "changes/templates/quick-card.md")
    for marker in [
        "promotedFrom:",
        "Promotion record",
        "previous contract",
        "evidence copied",
        "material confirmation",
    ]:
        if marker not in quick_card:
            fail(f"quick-card missing promotion marker: {marker}")
    spec_reviewer = read_text(root / "agents/spec-reviewer.md")
    for marker in [
        "Inline -> Compact",
        "Inline -> Full",
        "mechanical Reverse Sync",
        "material Reverse Sync",
    ]:
        if marker not in spec_reviewer:
            fail(f"spec reviewer missing progressive SDD marker: {marker}")

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
    ]:
        if marker not in finish:
            fail(f"finish module missing issue policy marker: {marker}")

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
