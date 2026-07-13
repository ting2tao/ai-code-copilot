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
    print("progressive-sdd: policy checks passed")


if __name__ == "__main__":
    main()
