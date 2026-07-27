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
    match = SEMVER.fullmatch(version)
    if not match:
        fail(f"invalid semantic version: {version!r}")
    prerelease = match.group(4)
    if prerelease and any(
        identifier.isdigit()
        and len(identifier) > 1
        and identifier.startswith("0")
        for identifier in prerelease.split(".")
    ):
        fail(f"invalid semantic version prerelease: {version!r}")
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
        ["diff", "--quiet", "origin/main", "--", *BEHAVIOR_PATHS],
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


def check_install_contract(root: Path) -> None:
    installer_markers = {
        "install.sh": ["validate_source_tree", "replace_install_tree", "VERSION"],
        "install-wsl.sh": ["validate_source_tree", "replace_install_tree", "VERSION"],
        "install.ps1": ["Test-SourceTree", "Replace-InstallTree", "VERSION"],
    }
    for relative, markers in installer_markers.items():
        content = read_text(root / relative)
        require_markers(content, relative, markers)
        if "git pull" in content:
            fail(f"{relative} must replace from a validated source, not git pull")
        if "git rev-parse --short HEAD" in content:
            fail(f"{relative} must report VERSION, not a commit as the release version")
        if "帮我做 xxx 需求" in content:
            fail(f"{relative} must not claim generic coding requests activate the framework")


def check_project_sync_contract(root: Path) -> None:
    init_project = read_text(root / "scripts/init_project.sh")
    require_markers(
        init_project,
        "scripts/init_project.sh",
        [
            "def framework_version():",
            "def validate_existing_config():",
            "def write_managed(",
            'data["frameworkVersion"]',
            'data["frameworkCommit"]',
            "existing config githubWorkflow.issuePolicy is required",
            "framework-managed core rules",
            "active changes",
            "archives",
        ],
    )
    for forbidden in [
        "write_if_missing_or_new",
        "copy_if_missing_or_new",
        "migration-note:",
        ".new candidates",
    ]:
        if forbidden in init_project:
            fail(f"scripts/init_project.sh retains obsolete sync behavior: {forbidden}")


def check_documentation_contract(root: Path) -> None:
    docs = {
        "README.md": [
            "Model-first",
            "native",
            "automatic activation",
            "VERSION",
            "0.1.0",
            "full replacement",
            "frameworkVersion",
            "frameworkCommit",
        ],
        "README-CN.md": [
            "模型优先",
            "原生处理",
            "自动激活",
            "VERSION",
            "0.1.0",
            "整包覆盖",
            "frameworkVersion",
            "frameworkCommit",
        ],
        "AGENTS.md": ["模型优先", "原生处理", "自动激活", "VERSION", "整包覆盖"],
        "docs/ai-code-copilot-overview.md": ["Native", "Compact", "Full", "模型判断"],
        "docs/ai-code-copilot-flow.md": ["Native", "Activate", "Compact", "Full"],
        "docs/harness-engineering.md": ["原生执行", "Compact SDD", "Full SDD"],
        "docs/loop-engineering.md": ["Native", "Compact SDD", "Full SDD"],
        "docs/ai-code-copilot-team-talk.html": ["Native", "Compact", "Full"],
        "agents/copilot-prompt.md": ["模型原生处理", "自动激活", "框架托管文件"],
    }
    stale_claims = [
        "Inline SDD",
        "Inline -> Compact",
        "Inline -> Full",
        "脚本会自动 `git pull`",
        "installer will run `git pull`",
        "其他规则文件若与新版本不同，生成 `<文件>.new`",
        "Other rule files with different content are written as `<filename>.new`",
    ]
    for relative, markers in docs.items():
        content = read_text(root / relative)
        require_markers(content, relative, markers)
        for claim in stale_claims:
            if claim in content:
                fail(f"{relative} contains stale current-runtime claim: {claim}")


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    version = read_version(root)
    if behavior_changed_from_base(root) and not version_changed_from_base(root, version):
        fail("framework behavior changed without a VERSION bump")
    check_activation_contract(root)
    check_install_contract(root)
    check_project_sync_contract(root)
    check_documentation_contract(root)
    print(f"model-first-versioning: version {version} checks passed")


if __name__ == "__main__":
    main()
