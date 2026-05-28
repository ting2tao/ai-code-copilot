#!/usr/bin/env bash
# ai-code-copilot WSL 安装脚本
#
# 在 WSL (Windows Subsystem for Linux) 内运行，为 Windows Codex/Claude Code 安装框架
#
# 使用方式:
#   1. 远程一行安装:
#      curl -fsSL https://raw.githubusercontent.com/ting2tao/ai-code-copilot/main/install-wsl.sh | bash
#
#   2. 指定平台:
#      bash install-wsl.sh --codex
#      bash install-wsl.sh --claude
#
#   3. 本地安装(已 git clone 后):
#      bash install-wsl.sh --codex
#
#   4. 卸载:
#      bash install-wsl.sh --codex --uninstall

set -euo pipefail

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
      echo "用法: bash install-wsl.sh [--codex|--claude] [--uninstall]" >&2
      exit 1
      ;;
  esac
done

# 判断是否从源码目录运行
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
    WIN_APP_HOME="$WIN_HOME_WSL/.codex"
    ;;
  claude)
    APP_NAME="Claude Code"
    WIN_APP_HOME="$WIN_HOME_WSL/.claude"
    ;;
  *)
    err "平台必须是 auto、codex 或 claude"
    exit 1
    ;;
esac

mkdir -p "$WIN_APP_HOME"

INSTALL_DIR="${AI_CODE_COPILOT_HOME:-$WIN_APP_HOME/ai_code_copilot}"
SKILLS_DIR="$WIN_APP_HOME/skills"
SKILL_LINK="$SKILLS_DIR/ai-code-copilot"
SKILL_TARGET="$INSTALL_DIR/skill"
HOOK_SCRIPT="$INSTALL_DIR/hooks/session-start"
SETTINGS_FILE="$WIN_APP_HOME/settings.json"

# ============ 卸载 ============
uninstall() {
  echo "${BOLD}卸载 ai-code-copilot ($APP_NAME)${RESET}"
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

if [ "$UNINSTALL" -eq 1 ]; then
  uninstall
fi

# ============ Banner ============
echo "${BOLD}╔══════════════════════════════════════════╗${RESET}"
echo "${BOLD}║   ai-code-copilot — WSL 安装/更新          ║${RESET}"
echo "${BOLD}╚══════════════════════════════════════════╝${RESET}"
echo ""
echo "  目标平台: $APP_NAME"
echo "  Windows 配置目录: $WIN_APP_HOME"
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
  if git pull --ff-only 2>/dev/null; then
    AFTER=$(git rev-parse --short HEAD)
    [ "$BEFORE" = "$AFTER" ] && ok "已是最新版本 ($AFTER)" || ok "已更新: $BEFORE → $AFTER"
  else
    if [ -n "$SCRIPT_DIR" ]; then
      warn "远程更新失败，从本地源码目录同步..."
      rsync -a --delete --exclude='.git' --exclude='.DS_Store' "$SCRIPT_DIR/" "$INSTALL_DIR/"
      ok "已从本地源码同步"
    else
      err "更新失败，请手动检查: cd $INSTALL_DIR && git status"
      exit 1
    fi
  fi
elif [ -d "$INSTALL_DIR" ]; then
  if [ -n "$SCRIPT_DIR" ]; then
    info "检测到本地目录(非 git 仓库)，从源码目录同步..."
    rsync -a --delete --exclude='.git' --exclude='.DS_Store' "$SCRIPT_DIR/" "$INSTALL_DIR/"
    ok "已从本地源码同步"
  else
    info "检测到本地目录(非 git 仓库)，重新 clone..."
    rm -rf "$INSTALL_DIR"
    mkdir -p "$SKILLS_DIR"
    git clone "$REPO_URL" "$INSTALL_DIR"
    ok "已 clone 到 $INSTALL_DIR"
  fi
else
  if [ -n "$SCRIPT_DIR" ]; then
    info "从本地源码目录安装..."
    mkdir -p "$SKILLS_DIR"
    cp -R "$SCRIPT_DIR" "$INSTALL_DIR"
    rm -rf "$INSTALL_DIR/.git" "$INSTALL_DIR/.DS_Store"
    ok "已复制到 $INSTALL_DIR"
  else
    info "首次安装，从 $REPO_URL clone..."
    mkdir -p "$SKILLS_DIR"
    if ! git clone "$REPO_URL" "$INSTALL_DIR"; then
      err "git clone 失败，请确认仓库地址或网络连接"
      exit 1
    fi
    ok "已 clone 到 $INSTALL_DIR"
  fi
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

# 优先创建 Windows Junction（Windows 上的 Codex/Claude Code 最兼容）
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

# hook 命令: Windows 上的 Codex/Claude Code 通过 wsl 调用 bash 执行脚本
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
echo "  1. 重启 Windows $APP_NAME 会话(让 skill 生效)"
echo "  2. cd 到业务项目根目录"
echo "  3. 输入: ${BOLD}初始化项目${RESET}"
echo "  4. 之后输入: ${BOLD}帮我做 xxx 需求${RESET} 即可触发流程"
echo ""
echo "${BOLD}更新:${RESET}  bash $INSTALL_DIR/install-wsl.sh --$PLATFORM"
echo "${BOLD}卸载:${RESET}  bash $INSTALL_DIR/install-wsl.sh --$PLATFORM --uninstall"
echo ""
