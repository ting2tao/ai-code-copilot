#!/usr/bin/env bash
# ai-code-copilot 安装脚本
#
# 使用方式:
#   1. 远程一行安装(推荐):
#      curl -fsSL https://raw.githubusercontent.com/ting2tao/ai-code-copilot/main/install.sh | bash
#
#   2. 指定平台:
#      bash install.sh --codex
#      bash install.sh --claude
#
#   3. 本地安装(已 git clone 后):
#      bash install.sh --codex
#
#   4. 卸载:
#      bash install.sh --codex --uninstall

set -euo pipefail

# ============ 配置 ============
REPO_URL="${CODE_COPILOT_REPO:-https://github.com/ting2tao/ai-code-copilot.git}"
PLATFORM="${CODE_COPILOT_PLATFORM:-auto}"
UNINSTALL=0

for arg in "$@"; do
  case "$arg" in
    --codex) PLATFORM="codex" ;;
    --claude) PLATFORM="claude" ;;
    --uninstall|-u) UNINSTALL=1 ;;
    *)
      echo "未知参数: $arg" >&2
      echo "用法: bash install.sh [--codex|--claude] [--uninstall]" >&2
      exit 1
      ;;
  esac
done

# 判断是否从源码目录运行（被 curl pipe 时 SCRIPT_DIR 为空）
SCRIPT_DIR=""
if [ -f "$PWD/skill/SKILL.md" ] && [ -f "$PWD/agents/copilot-prompt.md" ]; then
  SCRIPT_DIR="$PWD"
fi

# ============ 颜色 ============
if [ -t 1 ]; then
  RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; BLUE=$'\033[34m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; BLUE=''; BOLD=''; RESET=''
fi

info()  { echo "${BLUE}ℹ${RESET}  $*"; }
ok()    { echo "${GREEN}✓${RESET}  $*"; }
warn()  { echo "${YELLOW}⚠${RESET}  $*"; }
err()   { echo "${RED}✗${RESET}  $*" >&2; }

validate_source_tree() {
  local source_tree="$1"
  local source_version
  for required in VERSION skill/SKILL.md agents/copilot-prompt.md hooks/session-start; do
    if [ ! -f "$source_tree/$required" ]; then
      err "来源目录不完整，缺少: $required"
      return 1
    fi
  done
  if [ "$(wc -l < "$source_tree/VERSION" | tr -d ' ')" -ne 1 ] || grep -q $'\r' "$source_tree/VERSION"; then
    err "来源 VERSION 必须是单行 LF 结尾的 SemVer"
    return 1
  fi
  source_version="$(tr -d '\n' < "$source_tree/VERSION")"
  if [[ ! "$source_version" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$ ]]; then
    err "来源 VERSION 不是合法 SemVer: $source_version"
    return 1
  fi
  local version_without_build="${source_version%%+*}"
  if [[ "$version_without_build" == *-* ]]; then
    local prerelease="${version_without_build#*-}"
    local identifier
    local -a prerelease_identifiers
    IFS='.' read -r -a prerelease_identifiers <<< "$prerelease"
    for identifier in "${prerelease_identifiers[@]}"; do
      if [[ "$identifier" =~ ^0[0-9]+$ ]]; then
        err "来源 VERSION 的数字预发布标识不能有前导零: $source_version"
        return 1
      fi
    done
  fi
}

SOURCE_TMP=""
STAGE_DIR=""
cleanup_install_temps() {
  [ -z "$SOURCE_TMP" ] || rm -rf "$SOURCE_TMP"
  [ -z "$STAGE_DIR" ] || rm -rf "$STAGE_DIR"
}
trap cleanup_install_temps EXIT

replace_install_tree() {
  local source_tree="$1"
  local install_parent
  install_parent="$(dirname "$INSTALL_DIR")"
  mkdir -p "$install_parent"
  STAGE_DIR="$(mktemp -d "$install_parent/.ai-code-copilot-stage.XXXXXX")"
  cp -R "$source_tree/." "$STAGE_DIR/"
  rm -rf "$STAGE_DIR/.git" "$STAGE_DIR/.DS_Store"
  validate_source_tree "$STAGE_DIR"
  rm -rf "$INSTALL_DIR"
  mv "$STAGE_DIR" "$INSTALL_DIR"
  STAGE_DIR=""
}

resolve_platform() {
  if [ "$PLATFORM" = "auto" ]; then
    if [ -n "${CODEX_HOME:-}" ] || command -v codex >/dev/null 2>&1; then
      PLATFORM="codex"
    else
      PLATFORM="claude"
    fi
  fi

  case "$PLATFORM" in
    codex)
      APP_NAME="Codex"
      APP_HOME="${CODEX_HOME:-$HOME/.codex}"
      ;;
    claude)
      APP_NAME="Claude Code"
      APP_HOME="${CLAUDE_HOME:-$HOME/.claude}"
      ;;
    *)
      err "平台必须是 auto、codex 或 claude"
      exit 1
      ;;
  esac

  INSTALL_DIR="${AI_CODE_COPILOT_HOME:-$APP_HOME/ai_code_copilot}"
  SKILLS_DIR="$APP_HOME/skills"
  SKILL_LINK="$SKILLS_DIR/ai-code-copilot"
  SETTINGS_FILE="$APP_HOME/settings.json"
}

resolve_platform

# ============ 卸载 ============
uninstall() {
  echo "${BOLD}卸载 ai-code-copilot ($APP_NAME)${RESET}"
  echo ""
  if [ -L "$SKILL_LINK" ]; then
    rm "$SKILL_LINK"
    ok "已移除 skill symlink: $SKILL_LINK"
  else
    info "skill symlink 不存在，跳过"
  fi
  if [ -d "$INSTALL_DIR" ]; then
    warn "保留框架目录: $INSTALL_DIR"
    warn "如需彻底删除: rm -rf $INSTALL_DIR"
  fi
  ok "卸载完成"
  exit 0
}

if [ "$UNINSTALL" -eq 1 ]; then
  uninstall
fi

# ============ 环境检测 ============
echo "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}║   ai-code-copilot — 安装/更新              ║${RESET}"
echo "${BOLD}╚══════════════════════════════════════════╝"
echo ""

if ! command -v git >/dev/null 2>&1; then
  err "未找到 git，请先安装 git"
  exit 1
fi

if [ "$PLATFORM" = "codex" ] && ! command -v codex >/dev/null 2>&1; then
  warn "未检测到 codex 命令"
  warn "本脚本只负责框架安装，Codex 需另行安装"
  echo ""
elif [ "$PLATFORM" = "claude" ] && ! command -v claude >/dev/null 2>&1; then
  warn "未检测到 claude 命令"
  warn "本脚本只负责框架安装，Claude Code 需另行安装(https://docs.claude.com/claude-code)"
  echo ""
fi

info "目标平台: $APP_NAME"
info "安装目录: $INSTALL_DIR"

# ============ 安装或更新 ============
if [ -n "$SCRIPT_DIR" ]; then
  SOURCE_TREE="$SCRIPT_DIR"
  info "使用本地源码作为版本来源"
else
  SOURCE_TMP="$(mktemp -d)"
  SOURCE_TREE="$SOURCE_TMP/source"
  info "从 $REPO_URL 获取最新版本..."
  if ! git clone --depth 1 "$REPO_URL" "$SOURCE_TREE"; then
    err "git clone 失败"
    err "请确认仓库地址正确，或在源码根目录运行本脚本"
    exit 1
  fi
fi

validate_source_tree "$SOURCE_TREE"
SOURCE_VERSION="$(tr -d '\r\n' < "$SOURCE_TREE/VERSION")"
if [ -f "$INSTALL_DIR/VERSION" ]; then
  INSTALLED_VERSION="$(tr -d '\r\n' < "$INSTALL_DIR/VERSION")"
  info "直接覆盖更新: $INSTALLED_VERSION → $SOURCE_VERSION"
else
  info "安装版本: $SOURCE_VERSION"
fi
replace_install_tree "$SOURCE_TREE"
ok "框架托管目录已完整替换"

# ============ 创建 symlink ============
echo ""
info "注册 skill..."

mkdir -p "$SKILLS_DIR"

SKILL_TARGET="$INSTALL_DIR/skill"
if [ ! -d "$SKILL_TARGET" ]; then
  err "未找到 skill 源目录: $SKILL_TARGET"
  err "仓库结构可能异常"
  exit 1
fi

# 已存在的 link 或目录都先清理
if [ -L "$SKILL_LINK" ] || [ -e "$SKILL_LINK" ]; then
  rm -rf "$SKILL_LINK"
fi

ln -s "$SKILL_TARGET" "$SKILL_LINK"
ok "skill symlink: $SKILL_LINK → $SKILL_TARGET"

# ============ 注册 SessionStart Hook ============
echo ""
info "注册 session-start hook..."

HOOK_SCRIPT="$INSTALL_DIR/hooks/session-start"
chmod +x "$HOOK_SCRIPT" 2>/dev/null || true

if ! command -v python3 >/dev/null 2>&1; then
  warn "未找到 python3；hook 仍会注入 L0 安全规则，但 context freshness 与 active change 摘要会被跳过。"
  warn "建议安装 python3，以启用完整上下文管理能力。"
fi

if [ ! -f "$SETTINGS_FILE" ]; then
  mkdir -p "$(dirname "$SETTINGS_FILE")"
  echo '{}' > "$SETTINGS_FILE"
fi

if command -v python3 >/dev/null 2>&1; then
    python3 - "$SETTINGS_FILE" "$HOOK_SCRIPT" <<'PY'
import json
import sys

settings_path = sys.argv[1]
hook_script = sys.argv[2]
hook_cmd = f'bash {hook_script}'
with open(settings_path, 'r') as f:
    settings = json.load(f)
hooks = settings.setdefault('hooks', {})
session_hooks = hooks.setdefault('SessionStart', [])
session_hooks[:] = [
    entry for entry in session_hooks
    if not any(hook_script in hook.get('command', '') for hook in entry.get('hooks', []))
]
session_hooks.append({
    'matcher': '',
    'hooks': [{
        'type': 'command',
        'command': hook_cmd,
        'async': False
    }]
})
with open(settings_path, 'w') as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
PY
    ok "hook 已注册到 $SETTINGS_FILE"
else
  if grep -q "$HOOK_SCRIPT" "$SETTINGS_FILE" 2>/dev/null; then
    ok "hook 已注册，跳过"
  else
    warn "未找到 python3，安装脚本无法自动编辑 settings.json；请手动将以下 hook 配置添加到 $SETTINGS_FILE："
    echo ""
    echo "  \"hooks\": {"
    echo "    \"SessionStart\": [{"
    echo "      \"matcher\": \"\","
    echo "      \"hooks\": [{"
    echo "        \"type\": \"command\","
    echo "        \"command\": \"bash $HOOK_SCRIPT\","
    echo "        \"async\": false"
    echo "      }]"
    echo "    }]"
    echo "  }"
    echo ""
  fi
fi

# ============ 自检 ============
echo ""
info "自检..."

if [ ! -L "$SKILL_LINK" ]; then
  err "symlink 创建失败"; exit 1
fi
if [ ! -f "$SKILL_LINK/SKILL.md" ]; then
  err "SKILL.md 不可读: $SKILL_LINK/SKILL.md"; exit 1
fi
ok "symlink 与 SKILL.md 正常"

INSTALLED_VERSION="$(tr -d '\r\n' < "$INSTALL_DIR/VERSION")"
ok "当前版本: $INSTALLED_VERSION"

# ============ 完成提示 ============
echo ""
echo "${BOLD}${GREEN}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}${GREEN}║  ✅ ai-code-copilot 安装完成                ║${RESET}"
echo "${BOLD}${GREEN}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo "${BOLD}下一步:${RESET}"
echo "  1. 重启 $APP_NAME 会话(让 skill 生效)"
echo "  2. cd 到业务项目根目录"
echo "  3. 输入: ${BOLD}初始化项目${RESET}"
echo "  4. 之后输入: ${BOLD}帮我做 xxx 需求${RESET} 即可触发流程"
echo ""
echo "${BOLD}更新:${RESET}     bash $INSTALL_DIR/install.sh --$PLATFORM"
echo "${BOLD}卸载:${RESET}     bash $INSTALL_DIR/install.sh --$PLATFORM --uninstall"
echo ""
