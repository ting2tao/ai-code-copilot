#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_HOME="$(cd "$SCRIPT_DIR/.." && pwd)"
COPILOT_HOME="${AI_CODE_COPILOT_HOME:-$DEFAULT_HOME}"
PROJECT_DIR="$PWD"
MODE="init"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage: scripts/init_project.sh [--project <dir>] [--sync|--upgrade] [--dry-run]

Initializes or synchronizes .ai_code_copilot/ in a business project.

Default behavior:
  - Creates .ai_code_copilot/ if missing.
  - Creates .ai_code_copilot/config.json if missing.
  - Overwrites framework-managed core rules, detected tech-pack rules, templates, and state.
  - Preserves project-owned config, project context, domain rules, knowledge, active changes, and archives.
  - Rejects invalid existing config instead of migrating it.

Options:
  --project <dir>  Target project directory. Defaults to current directory.
  --sync           Re-run detection and add missing/new template files for an existing project.
  --upgrade        Alias for --sync, intended for framework upgrades.
  --dry-run        Show planned writes without creating or changing files.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --project)
      [ "${2:-}" ] || { usage >&2; exit 2; }
      PROJECT_DIR="$2"
      shift 2
      ;;
    --sync)
      MODE="sync"
      shift
      ;;
    --upgrade)
      MODE="upgrade"
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[ -d "$COPILOT_HOME" ] || { echo "COPILOT_HOME not found: $COPILOT_HOME" >&2; exit 1; }
[ -d "$PROJECT_DIR" ] || { echo "project directory not found: $PROJECT_DIR" >&2; exit 1; }

python3 - "$COPILOT_HOME" "$PROJECT_DIR" "$MODE" "$DRY_RUN" <<'PY'
import json
import os
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

copilot_home = Path(sys.argv[1]).resolve()
project_dir = Path(sys.argv[2]).resolve()
mode = sys.argv[3]
dry_run = sys.argv[4] == "1"

target = project_dir / ".ai_code_copilot"
rules_target = target / "rules"
changes_target = target / "changes"
knowledge_target = target / "knowledge"
state_path = target / ".copilot-state.json"
config_path = target / "config.json"

excluded_dirs = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "target",
    "ai_code_copilot",
    ".ai_code_copilot",
}


def framework_version():
    version_path = copilot_home / "VERSION"
    try:
        version = version_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"unable to read framework VERSION: {version_path}: {exc}")
    if not re.fullmatch(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
        r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\n",
        version,
    ):
        raise SystemExit(f"invalid framework VERSION: {version_path}")
    value = version.strip()
    prerelease = value.split("+", 1)[0].partition("-")[2]
    if prerelease and any(
        identifier.isdigit()
        and len(identifier) > 1
        and identifier.startswith("0")
        for identifier in prerelease.split(".")
    ):
        raise SystemExit(f"invalid framework VERSION prerelease: {version_path}")
    return value


current_framework_version = framework_version()


def iter_project_files(names):
    wanted = set(names)
    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for name in files:
            if name in wanted:
                yield Path(root) / name


def package_json_has_any(path, names):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    deps = {}
    for key in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
        value = data.get(key)
        if isinstance(value, dict):
            deps.update(value)
    return any(name in deps for name in names)


def package_json_dependency_names(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    deps = set()
    for key in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
        value = data.get(key)
        if isinstance(value, dict):
            deps.update(value.keys())
    return deps


def package_json_script_names(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    scripts = data.get("scripts")
    return set(scripts.keys()) if isinstance(scripts, dict) else set()


def detect_pack(pack_dir, manifest):
    detect = manifest.get("detect", {})
    files = detect.get("files", [])
    package_deps = detect.get("packageJsonDependenciesAny", [])
    matches = []
    for path in iter_project_files(files):
        if path.name == "package.json" and package_deps:
            if package_json_has_any(path, package_deps):
                matches.append(path)
        else:
            matches.append(path)
    return matches


def detect_signals(manifest, matches):
    signals = []
    for signal in manifest.get("signals", []):
        label = signal.get("label") or signal.get("id")
        if not label:
            continue
        package_deps = set(signal.get("packageJsonDependenciesAny", []))
        package_scripts = set(signal.get("packageJsonScriptsAny", []))
        files_any = signal.get("filesAny", [])
        matched = False
        for match in matches:
            module_dir = match.parent
            if package_deps and match.name == "package.json":
                matched = matched or bool(package_json_dependency_names(match) & package_deps)
            if package_scripts and match.name == "package.json":
                matched = matched or bool(package_json_script_names(match) & package_scripts)
            if files_any:
                matched = matched or any((module_dir / rel).exists() for rel in files_any)
            if matched:
                break
        if matched:
            signals.append(label)
    return signals


def read_manifests():
    manifests = []
    for pack_dir in sorted((copilot_home / "packs").iterdir()):
        if not pack_dir.is_dir():
            continue
        manifest_path = pack_dir / "pack.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifests.append((pack_dir, manifest))
    return manifests


def write_project_owned(dest, content):
    if not dest.exists():
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
        return "created", dest
    existing = dest.read_text(encoding="utf-8")
    if existing == content:
        return "unchanged", dest
    return "preserved-project-owned", dest


def write_managed(dest, content):
    if not dest.exists():
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
        return "created", dest
    existing = dest.read_text(encoding="utf-8")
    if existing == content:
        return "unchanged", dest
    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return "updated-managed", dest


def prefixed_rule_name(pack_id, rel):
    return f"{pack_id}-{Path(rel).name}"


def command_value(commands, key):
    value = commands.get(key, "")
    return value if value else "(not configured)"


def project_context(detected):
    lines = [
        "---",
        "alwaysApply: true",
        "---",
        "# 工程上下文",
        "",
        "> Generated by ai-code-copilot from current project detection.",
        "> Project edits are preserved on sync; framework changes do not overwrite this file.",
        "",
        "## 1. 应用概况",
        "",
        f"- 应用名：{project_dir.name}",
        "- 简介：（请补充一句话描述）",
        "- 技术栈：" + (", ".join(d['name'] for d in detected) if detected else "未识别"),
        "- 命中的技术栈规则包：" + (", ".join(d['id'] for d in detected) if detected else "无"),
        "- 主要中间件：（请补充：数据库、缓存、消息队列、三方服务等）",
        "",
        "## 2. 模块与规则包",
        "",
        "| 模块路径 | 规则包 | 命中依据 |",
        "|----------|--------|----------|",
    ]
    if detected:
        for item in detected:
            for match in item["matches"]:
                rel = os.path.relpath(match, project_dir)
                module = os.path.dirname(rel) or "."
                lines.append(f"| `{module}` | `{item['id']}` | `{rel}` |")
    else:
        lines.append("| （待补充） | （待补充） | （未自动识别） |")

    lines.extend([
        "",
        "## 3. 架构与边界",
        "",
        "- 入口层：（待补充）",
        "- 业务/领域层：（待补充）",
        "- 数据/基础设施层：（待补充）",
        "- 前端状态/组件边界（如适用）：（待补充）",
        "",
        "## 4. 关键依赖",
        "",
        "| 规则包 | 依赖读取/扫描命令 |",
        "|--------|------------------|",
    ])
    if detected:
        for item in detected:
            scan = item["manifest"].get("scan", {}).get("command", "")
            lines.append(f"| `{item['id']}` | `{scan}` |")
    else:
        lines.append("| （待补充） | （待补充） |")

    lines.extend([
        "",
        "## 5. 技术栈信号",
        "",
        "| 规则包 | 自动识别信号 |",
        "|--------|--------------|",
    ])
    if detected:
        for item in detected:
            signals = "、".join(item.get("signals", [])) or "未配置细分信号"
            lines.append(f"| `{item['id']}` | {signals} |")
    else:
        lines.append("| （待补充） | （待补充） |")

    lines.extend([
        "",
        "## 6. 构建与测试命令",
        "",
        "| 规则包 | 依赖安装 | 编译/类型检查 | 全量测试 | 单模块/单文件测试 | Lint/格式化 |",
        "|--------|----------|----------------|----------|------------------|-------------|",
    ])
    if detected:
        for item in detected:
            commands = item["manifest"].get("commands", {})
            lines.append(
                "| `{id}` | `{dep}` | `{build}` | `{test}` | `{single}` | `{lint}` |".format(
                    id=item["id"],
                    dep=command_value(commands, "dependencyInstall"),
                    build=command_value(commands, "build"),
                    test=command_value(commands, "test"),
                    single=command_value(commands, "testSingle"),
                    lint=command_value(commands, "lint"),
                )
            )
    else:
        lines.append("| （待补充） | （待补充） | （待补充） | （待补充） | （待补充） | （待补充） |")

    lines.extend([
        "",
        "## 7. 变更验证矩阵",
        "",
        "| 规则包 | 改动场景 | 建议验证 |",
        "|--------|----------|----------|",
    ])
    has_matrix = False
    for item in detected:
        for row in item["manifest"].get("verificationMatrix", []):
            change = row.get("change", "（待补充）")
            commands = row.get("commands", [])
            command_text = "；".join(commands) if commands else "参考项目现有验证命令"
            lines.append(f"| `{item['id']}` | {change} | `{command_text}` |")
            has_matrix = True
    if not has_matrix:
        lines.append("| （待补充） | （待补充） | （待补充） |")
    lines.append("")
    return "\n".join(lines)


def framework_commit():
    try:
        return subprocess.check_output(
            ["git", "-C", str(copilot_home), "rev-parse", "--short", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unknown"


def state_content(detected):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data = OrderedDict()
    data["frameworkVersion"] = current_framework_version
    data["frameworkCommit"] = framework_commit()
    data["mode"] = mode
    data["initializedAt"] = now
    data["lastSyncedAt"] = now
    data["projectContextSyncedAt"] = now_utc
    data["projectContextStaleAfterDays"] = 30
    data["packs"] = [item["id"] for item in detected]
    data["packMatches"] = {
        item["id"]: [os.path.relpath(match, project_dir) for match in item["matches"]]
        for item in detected
    }
    data["syncPolicy"] = "framework-managed core rules, detected pack rules, templates, and state are overwritten; config, project-context.md, domain-rules.md, knowledge, active changes, and archives are project-owned and preserved"
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


detected = []
for pack_dir, manifest in read_manifests():
    matches = detect_pack(pack_dir, manifest)
    if matches:
        detected.append(
            {
                "id": manifest["id"],
                "name": manifest.get("name", manifest["id"]),
                "manifest": manifest,
                "pack_dir": pack_dir,
                "matches": matches,
                "signals": detect_signals(manifest, matches),
            }
        )

events = []

def validate_existing_config():
    if not (config_path.exists() or config_path.is_symlink()):
        return None
    try:
        existing_config_text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"unable to read existing config: {exc}")
    try:
        existing_config = json.loads(existing_config_text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"existing config contains invalid JSON: {exc}")
    if not isinstance(existing_config, dict):
        raise SystemExit("existing config root must be a JSON object")
    github_workflow = existing_config.get("githubWorkflow")
    if not isinstance(github_workflow, dict):
        raise SystemExit("existing config githubWorkflow must be a JSON object")
    if "issuePolicy" not in github_workflow:
        raise SystemExit("existing config githubWorkflow.issuePolicy is required")
    if github_workflow["issuePolicy"] not in {"always", "on-commit", "on-publish", "manual"}:
        raise SystemExit("existing config githubWorkflow.issuePolicy is invalid")
    return existing_config_text


existing_config_text = validate_existing_config()
config_path_present = existing_config_text is not None

if not dry_run:
    for directory in [rules_target, changes_target / "templates", changes_target / "archives", knowledge_target]:
        directory.mkdir(parents=True, exist_ok=True)

framework_config_text = (copilot_home / "config" / "project-config.json").read_text(encoding="utf-8")
if config_path_present:
    config_status = "unchanged" if existing_config_text == framework_config_text else "preserved-project-owned"
    config_dest = config_path
else:
    config_status, config_dest = write_project_owned(config_path, framework_config_text)
events.append((config_status, config_dest))

for src in sorted((copilot_home / "rules").glob("*.md")):
    if src.name == "project-context.md":
        continue
    if src.name == "domain-rules.md":
        status, path = write_project_owned(rules_target / src.name, src.read_text(encoding="utf-8"))
    else:
        status, path = write_managed(rules_target / src.name, src.read_text(encoding="utf-8"))
    events.append((status, path))

for item in detected:
    pack_id = item["id"]
    pack_dir = item["pack_dir"]
    for rel in item["manifest"].get("rules", []):
        src = pack_dir / rel
        dest = rules_target / prefixed_rule_name(pack_id, rel)
        status, path = write_managed(dest, src.read_text(encoding="utf-8"))
        events.append((status, path))

for src in sorted((copilot_home / "changes" / "templates").glob("*.md")):
    status, path = write_managed(
        changes_target / "templates" / src.name,
        src.read_text(encoding="utf-8"),
    )
    events.append((status, path))

status, path = write_project_owned(rules_target / "project-context.md", project_context(detected))
events.append((status, path))

index_status, index_path = write_project_owned(
    knowledge_target / "index.md",
    "# Knowledge Index\n\n"
    "> Project-specific knowledge discovered by `/archive`. Read this index first; load only relevant knowledge files.\n\n"
    "| ID | Summary | Tags | Scope | Applies-To | Risk | Last-Verified | File |\n"
    "|----|---------|------|-------|------------|------|---------------|------|\n"
    "| K000 | 示例：删除本行后开始沉淀知识 | example | example | propose | low | 1970-01-01 | example.md |\n",
)
events.append((index_status, index_path))

state_status, state_dest = write_managed(state_path, state_content(detected))
events.append((state_status, state_dest))

verb = "dry-run" if dry_run else "complete"
print(f"ai-code-copilot {mode} {verb}")
print(f"project: {project_dir}")
print("detected packs: " + (", ".join(item["id"] for item in detected) if detected else "none"))
for status, path in events:
    if status != "unchanged":
        print(f"{status}: {path.relative_to(project_dir)}")
if dry_run:
    print("note: dry-run only; no files were written.")
PY
