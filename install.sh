#!/usr/bin/env bash
# ai-code-copilot 安装脚本
#
# 使用方式:
#   1. 远程一行安装(推荐):
#      curl -fsSL https://raw.githubusercontent.com/ting2tao/ai-code-copilot/main/install.sh | bash
#
#   2. 本地安装(已 git clone 后):
#      cd ~/.claude/ai_code_copilot && bash install.sh
#
#   3. 卸载:
#      bash install.sh --uninstall

set -euo pipefail

# ============ 配置 ============
REPO_URL="${CODE_COPILOT_REPO:-https://github.com/ting2tao/ai-code-copilot.git}"
INSTALL_DIR="$HOME/.claude/ai_code_copilot"
SKILLS_DIR="$HOME/.claude/skills"
SKILL_LINK="$SKILLS_DIR/ai-code-copilot"

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

# ============ 卸载 ============
uninstall() {
  echo "${BOLD}卸载 ai-code-copilot${RESET}"
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

if [ "${1:-}" = "--uninstall" ] || [ "${1:-}" = "-u" ]; then
  uninstall
fi

# ============ 环境检测 ============
echo "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}║   ai-code-copilot — 安装/更新              ║${RESET}"
echo "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""

# 检测 git
if ! command -v git >/dev/null 2>&1; then
  err "未找到 git，请先安装 git"
  exit 1
fi

# 检测 Claude Code(非阻塞，仅提示)
if ! command -v claude >/dev/null 2>&1; then
  warn "未检测到 claude 命令"
  warn "本脚本只负责框架安装，Claude Code 需另行安装(https://docs.claude.com/claude-code)"
  echo ""
fi

# ============ 安装或更新 ============
if [ -d "$INSTALL_DIR/.git" ]; then
  info "检测到已安装，执行更新..."
  cd "$INSTALL_DIR"
  BEFORE="$(git rev-parse --short HEAD)"
  if git pull --ff-only; then
    AFTER="$(git rev-parse --short HEAD)"
    if [ "$BEFORE" = "$AFTER" ]; then
      ok "已是最新版本 ($AFTER)"
    else
      ok "已更新: $BEFORE → $AFTER"
    fi
  else
    err "更新失败，请手动检查: cd $INSTALL_DIR && git status"
    exit 1
  fi
elif [ -d "$INSTALL_DIR" ]; then
  # 目录存在但不是 git 仓库 — 可能是用户手动放的文件
  info "检测到本地目录(非 git 仓库)，跳过 clone，仅创建 symlink"
else
  info "首次安装，从 $REPO_URL clone..."
  mkdir -p "$(dirname "$INSTALL_DIR")"
  if ! git clone "$REPO_URL" "$INSTALL_DIR"; then
    err "git clone 失败"
    err "请确认仓库地址正确，或先手动 clone 到 $INSTALL_DIR 后再跑本脚本"
    exit 1
  fi
  ok "已 clone 到 $INSTALL_DIR"
fi

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

SETTINGS_FILE="$HOME/.claude/settings.json"

if [ ! -f "$SETTINGS_FILE" ]; then
  echo '{}' > "$SETTINGS_FILE"
fi

if grep -q "ai-code-copilot" "$SETTINGS_FILE" 2>/dev/null; then
  ok "hook 已注册，跳过"
else
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "
import json, sys
settings_path = '$SETTINGS_FILE'
hook_cmd = 'bash $HOOK_SCRIPT'
with open(settings_path, 'r') as f:
    settings = json.load(f)
hooks = settings.setdefault('hooks', {})
session_hooks = hooks.setdefault('SessionStart', [])
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
" && ok "hook 已注册到 $SETTINGS_FILE"
  else
    warn "未找到 python3，请手动将以下 hook 配置添加到 $SETTINGS_FILE："
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

if [ -d "$INSTALL_DIR/.git" ]; then
  VERSION="$(cd "$INSTALL_DIR" && git rev-parse --short HEAD)"
  ok "当前版本: $VERSION"
fi

# ============ 完成提示 ============
echo ""
echo "${BOLD}${GREEN}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}${GREEN}║  ✅ ai-code-copilot 安装完成                ║${RESET}"
echo "${BOLD}${GREEN}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo "${BOLD}下一步:${RESET}"
echo "  1. 重启 Claude Code 会话(让 skill 生效)"
echo "  2. cd 到业务项目根目录"
echo "  3. 输入: ${BOLD}初始化项目${RESET}"
echo "  4. 之后输入: ${BOLD}帮我做 xxx 需求${RESET} 即可触发流程"
echo ""
echo "${BOLD}更新:${RESET}     bash $INSTALL_DIR/install.sh"
echo "${BOLD}卸载:${RESET}     bash $INSTALL_DIR/install.sh --uninstall"
echo ""
