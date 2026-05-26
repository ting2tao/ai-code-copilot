#!/usr/bin/env bash
# ai-code-copilot WSL 安装脚本
#
# 在 WSL (Windows Subsystem for Linux) 内运行，为 Windows Claude Code 安装框架
#
# 使用方式:
#   1. 远程一行安装:
#      curl -fsSL https://git.eminxing.com/ai/ai-code-copilot/raw/master/install-wsl.sh | bash
#
#   2. 本地安装(已 git clone 后):
#      bash install-wsl.sh
#
#   3. 卸载:
#      bash install-wsl.sh --uninstall

set -euo pipefail

REPO_URL="${CODE_COPILOT_REPO:-https://git.eminxing.com/ai/ai-code-copilot.git}"

# ============ 颜色 ============
if [ -t 1 ]; then
  RED=$'\033[31m'; GREEN=$'\033[32m'; YELLOW=$'\033[33m'; BLUE=$'\033[34m'; BOLD=$'\033[1m'; RESET=$'\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; BLUE=''; BOLD=''; RESET=''
fi

info() { echo "${BLUE}ℹ${RESET}  $*"; }
ok()   { echo "${GREEN}✓${RESET}  $*"; }
warn() { echo "${YELLOW}⚠${RESET}  $*"; }
err()  { echo "${RED}✗${RESET}  $*" >&2; }

# ============ WSL 检测 ============
if ! grep -qiE "microsoft|wsl" /proc/version 2>/dev/null; then
  warn "未检测到 WSL 环境，此脚本专为 WSL 设计"
  warn "如果你在纯 Linux/Mac 上，请使用 install.sh"
  echo ""
fi

# ============ 获取 Windows 用户目录 ============
WIN_HOME=$(cmd.exe /C "echo %USERPROFILE%" 2>/dev/null | tr -d '\r\n')
if [ -z "$WIN_HOME" ]; then
  err "无法获取 Windows 用户目录"
  err "请确认 WSL interop 已启用: cat /proc/sys/fs/binfmt_misc/WSLInterop"
  exit 1
fi

WIN_HOME_WSL=$(wslpath "$WIN_HOME")
WIN_CLAUDE="$WIN_HOME_WSL/.claude"
mkdir -p "$WIN_CLAUDE"

INSTALL_DIR="$WIN_CLAUDE/ai_code_copilot"
SKILLS_DIR="$WIN_CLAUDE/skills"
SKILL_LINK="$SKILLS_DIR/ai-code-copilot"
SKILL_TARGET="$INSTALL_DIR/skill"
HOOK_SCRIPT="$INSTALL_DIR/hooks/session-start"
SETTINGS_FILE="$WIN_CLAUDE/settings.json"

# ============ 卸载 ============
uninstall() {
  echo "${BOLD}卸载 ai-code-copilot${RESET}"
  echo ""
  if [ -e "$SKILL_LINK" ]; then
    WIN_LINK=$(wslpath -w "$SKILL_LINK" 2>/dev/null || echo "")
    if [ -n "$WIN_LINK" ]; then
      cmd.exe /C "rmdir /S /Q \"$WIN_LINK\"" >/dev/null 2>&1 || rm -rf "$SKILL_LINK"
    else
      rm -rf "$SKILL_LINK"
    fi
    ok "已移除 skill junction: $SKILL_LINK"
  else
    info "skill junction 不存在，跳过"
  fi
  if [ -d "$INSTALL_DIR" ]; then
    warn "保留框架目录: $INSTALL_DIR"
    warn "如需彻底删除: rm -rf '$INSTALL_DIR'"
  fi
  ok "卸载完成"
  exit 0
}

[ "${1:-}" = "--uninstall" ] || [ "${1:-}" = "-u" ] && uninstall

# ============ Banner ============
echo "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}║   ai-code-copilot — WSL 安装/更新          ║${RESET}"
echo "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo "  Windows .claude 目录: $WIN_CLAUDE"
echo ""

# ============ 环境检测 ============
if ! command -v git >/dev/null 2>&1; then
  err "未找到 git，请先安装: sudo apt install git"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  warn "未找到 python3，settings.json 需手动配置 hook"
  warn "建议安装: sudo apt install python3"
fi

# ============ 安装或更新 ============
if [ -d "$INSTALL_DIR/.git" ]; then
  info "检测到已安装，执行更新..."
  cd "$INSTALL_DIR"
  BEFORE=$(git rev-parse --short HEAD)
  if git pull --ff-only; then
    AFTER=$(git rev-parse --short HEAD)
    [ "$BEFORE" = "$AFTER" ] && ok "已是最新版本 ($AFTER)" || ok "已更新: $BEFORE → $AFTER"
  else
    err "更新失败，请手动检查: cd $INSTALL_DIR && git status"
    exit 1
  fi
elif [ -d "$INSTALL_DIR" ]; then
  info "检测到本地目录(非 git 仓库)，跳过 clone，仅注册 skill"
else
  info "首次安装，从 $REPO_URL clone..."
  mkdir -p "$SKILLS_DIR"
  if ! git clone "$REPO_URL" "$INSTALL_DIR"; then
    err "git clone 失败，请确认仓库地址或网络连接"
    exit 1
  fi
  ok "已 clone 到 $INSTALL_DIR"
fi

# ============ 创建 Windows Junction ============
echo ""
info "注册 skill..."
mkdir -p "$SKILLS_DIR"

if [ ! -d "$SKILL_TARGET" ]; then
  err "未找到 skill 源目录: $SKILL_TARGET (仓库结构可能异常)"
  exit 1
fi

# 移除旧的 junction/symlink
if [ -e "$SKILL_LINK" ] || [ -L "$SKILL_LINK" ]; then
  WIN_OLD=$(wslpath -w "$SKILL_LINK" 2>/dev/null || echo "")
  if [ -n "$WIN_OLD" ]; then
    cmd.exe /C "rmdir /S /Q \"$WIN_OLD\"" >/dev/null 2>&1 || rm -rf "$SKILL_LINK"
  else
    rm -rf "$SKILL_LINK"
  fi
fi

# 优先创建 Windows Junction（Claude Code on Windows 最兼容）
WIN_LINK=$(wslpath -w "$SKILL_LINK")
WIN_TARGET=$(wslpath -w "$SKILL_TARGET")
if cmd.exe /C "mklink /J \"$WIN_LINK\" \"$WIN_TARGET\"" >/dev/null 2>&1; then
  ok "skill junction (Windows): $SKILL_LINK → $SKILL_TARGET"
else
  # 回退到 WSL symlink（需要 Windows 开发者模式）
  ln -s "$SKILL_TARGET" "$SKILL_LINK"
  ok "skill symlink (WSL): $SKILL_LINK → $SKILL_TARGET"
fi

# ============ 注册 SessionStart Hook ============
echo ""
info "注册 session-start hook..."
chmod +x "$HOOK_SCRIPT" 2>/dev/null || true

[ ! -f "$SETTINGS_FILE" ] && echo '{}' > "$SETTINGS_FILE"

# hook 命令: Windows Claude Code 通过 wsl 调用 bash 执行脚本
HOOK_CMD="wsl bash $HOOK_SCRIPT"

if grep -q "ai-code-copilot" "$SETTINGS_FILE" 2>/dev/null; then
  ok "hook 已注册，跳过"
elif command -v python3 >/dev/null 2>&1; then
  python3 -c "
import json
with open('$SETTINGS_FILE', 'r', encoding='utf-8') as f:
    s = json.load(f)
s.setdefault('hooks', {}).setdefault('SessionStart', []).append({
    'matcher': '',
    'hooks': [{'type': 'command', 'command': '$HOOK_CMD', 'async': False}]
})
with open('$SETTINGS_FILE', 'w', encoding='utf-8') as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
" && ok "hook 已注册: $HOOK_CMD"
else
  warn "请手动将以下内容合并到 $SETTINGS_FILE:"
  echo ""
  echo '  "hooks": {'
  echo '    "SessionStart": [{'
  echo '      "matcher": "",'
  echo '      "hooks": [{'
  echo '        "type": "command",'
  echo "        \"command\": \"$HOOK_CMD\","
  echo '        "async": false'
  echo '      }]'
  echo '    }]'
  echo '  }'
  echo ""
fi

# ============ 自检 ============
echo ""
info "自检..."

if [ ! -f "$SKILL_LINK/SKILL.md" ]; then
  err "SKILL.md 不可读: $SKILL_LINK/SKILL.md"
  err "junction 可能未生效，请检查 Windows 开发者模式是否已开启"
  err "开启方式: 设置 → 系统 → 开发者选项 → 开发者模式"
  exit 1
fi
ok "skill 目录与 SKILL.md 正常"

if [ -d "$INSTALL_DIR/.git" ]; then
  VERSION=$(cd "$INSTALL_DIR" && git rev-parse --short HEAD)
  ok "当前版本: $VERSION"
fi

# ============ 完成提示 ============
echo ""
echo "${BOLD}${GREEN}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}${GREEN}║  ✅ ai-code-copilot WSL 安装完成            ║${RESET}"
echo "${BOLD}${GREEN}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo "${BOLD}下一步:${RESET}"
echo "  1. 重启 Windows Claude Code 会话(让 skill 生效)"
echo "  2. cd 到业务项目根目录"
echo "  3. 输入: ${BOLD}初始化项目${RESET}"
echo "  4. 之后输入: ${BOLD}帮我做 xxx 需求${RESET} 即可触发流程"
echo ""
echo "${BOLD}更新:${RESET}  bash $INSTALL_DIR/install-wsl.sh"
echo "${BOLD}卸载:${RESET}  bash $INSTALL_DIR/install-wsl.sh --uninstall"
echo ""
