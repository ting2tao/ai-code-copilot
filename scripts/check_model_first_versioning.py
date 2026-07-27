#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path


SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)
BEHAVIOR_PATHS = [
    "skill",
    "hooks",
    "agents",
    "config",
    "rules",
    "packs",
    "changes/templates",
    "scripts",
    "install.sh",
    "install-wsl.sh",
    "install.ps1",
]


def fail(message: str) -> None:
    raise SystemExit(f"model-first-versioning: {message}")


def read_text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def read_version(root: Path) -> str:
    raw = read_text(root / "VERSION")
    if raw.count("\n") != 1 or not raw.endswith("\n"):
        fail("VERSION must contain one line with a trailing newline")
    version = raw[:-1]
    if not SEMVER.fullmatch(version):
        fail(f"invalid semantic version: {version!r}")
    return version


def git_result(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def version_changed_from_base(root: Path, version: str) -> bool:
    result = git_result(root, ["show", "origin/main:VERSION"])
    return result.returncode != 0 or result.stdout.strip() != version


def behavior_changed_from_base(root: Path) -> bool:
    result = git_result(
        root,
        ["diff", "--quiet", "origin/main...HEAD", "--", *BEHAVIOR_PATHS],
    )
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    return False


def require_markers(text: str, label: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        fail(f"{label} missing: {', '.join(missing)}")


def check_activation_contract(root: Path) -> None:
    policy = json.loads(read_text(root / "config/workflow-policy.json"))
    activation = policy.get("activation", {})
    if activation.get("defaultPath") != "native":
        fail("activation.defaultPath must be native")
    require_markers(
        " ".join(activation.get("mustActivateSignals", [])),
        "mustActivateSignals",
        ["security", "permission", "money", "production", "database", "deployment"],
    )
    require_markers(
        " ".join(activation.get("explicitIntents", [])),
        "explicitIntents",
        ["init", "propose", "review", "finish", "archive"],
    )
    skill = read_text(root / "skill/SKILL.md")
    description = skill.split("---", 2)[1]
    for forbidden in [
        "实现/开发/写代码/加功能",
        "优化/重构/refactor",
        "修 bug/debug",
    ]:
        if forbidden in description:
            fail(f"skill description retains unconditional coding trigger: {forbidden}")
    hook = read_text(root / "hooks/session-start")
    require_markers(
        hook,
        "SessionStart",
        ["模型原生处理", "自动激活 ai-code-copilot", "不得绕过人工确认"],
    )
    if (root / "agents/workflows/inline.md").exists():
        fail("framework-owned inline workflow must be removed")


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    version = read_version(root)
    if behavior_changed_from_base(root) and not version_changed_from_base(root, version):
        fail("framework behavior changed without a VERSION bump")
    check_activation_contract(root)
    print(f"model-first-versioning: version {version} checks passed")


if __name__ == "__main__":
    main()
