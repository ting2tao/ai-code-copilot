#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TMP_HOME="$(mktemp -d)"
trap 'rm -rf "$TMP_HOME"' EXIT

APP_HOME="$TMP_HOME/.codex"
INSTALL_DIR="$APP_HOME/ai_code_copilot"
export HOME="$TMP_HOME"
export CODEX_HOME="$APP_HOME"
export AI_CODE_COPILOT_HOME="$INSTALL_DIR"

cd "$ROOT"
bash install.sh --codex >"$TMP_HOME/install-first.out"

test -f "$INSTALL_DIR/VERSION"
cmp -s "$ROOT/VERSION" "$INSTALL_DIR/VERSION"
test -L "$APP_HOME/skills/ai-code-copilot"
test -f "$APP_HOME/skills/ai-code-copilot/SKILL.md"

printf 'obsolete\n' >"$INSTALL_DIR/obsolete-managed-file.txt"
printf 'locally modified\n' >"$INSTALL_DIR/README.md"

bash install.sh --codex >"$TMP_HOME/install-second.out"

test ! -e "$INSTALL_DIR/obsolete-managed-file.txt"
cmp -s "$ROOT/README.md" "$INSTALL_DIR/README.md"
cmp -s "$ROOT/VERSION" "$INSTALL_DIR/VERSION"
test -L "$APP_HOME/skills/ai-code-copilot"
test -f "$APP_HOME/skills/ai-code-copilot/SKILL.md"

python3 - "$APP_HOME/settings.json" "$INSTALL_DIR/hooks/session-start" <<'PY'
import json
import sys

settings_path, hook_script = sys.argv[1:]
with open(settings_path, encoding="utf-8") as handle:
    settings = json.load(handle)
commands = [
    hook["command"]
    for entry in settings.get("hooks", {}).get("SessionStart", [])
    for hook in entry.get("hooks", [])
    if hook_script in hook.get("command", "")
]
if len(commands) != 1:
    raise SystemExit(f"expected exactly one installed SessionStart hook, got {commands}")
PY

printf 'install-overwrite: repeated local install replaced the managed tree\n'
