#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

need_file() {
  [ -f "$1" ] || fail "missing file: $1"
}

need_dir() {
  [ -d "$1" ] || fail "missing directory: $1"
}

need_file skill/SKILL.md
need_file agents/copilot-prompt.md
need_file agents/spec-reviewer.md
need_file agents/code-quality-reviewer.md
need_file hooks/session-start
need_dir rules
need_dir packs
need_dir changes/templates

for f in rules/*.md; do
  case "$(basename "$f")" in
    coding-style.md|security.md|domain-rules.md|project-context.md) ;;
    *) fail "core rules must stay generic; unexpected file in rules/: $f" ;;
  esac
done

bash -n install.sh
bash -n install-wsl.sh
bash -n hooks/session-start
bash -n scripts/init_project.sh

python3 - "$ROOT" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
pack_root = root / "packs"
expected = {"java-spring", "go", "python", "frontend-react"}
actual = {p.name for p in pack_root.iterdir() if p.is_dir()}
missing = expected - actual
if missing:
    raise SystemExit(f"missing pack directories: {sorted(missing)}")

for pack_dir in sorted(p for p in pack_root.iterdir() if p.is_dir()):
    manifest_path = pack_dir / "pack.json"
    pack_md = pack_dir / "pack.md"
    if not manifest_path.exists():
        raise SystemExit(f"missing manifest: {manifest_path}")
    if not pack_md.exists():
        raise SystemExit(f"missing pack.md: {pack_md}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pack_id = manifest.get("id")
    if pack_id != pack_dir.name:
        raise SystemExit(f"pack id mismatch in {manifest_path}: {pack_id!r}")
    rules = manifest.get("rules") or []
    if not rules:
        raise SystemExit(f"pack has no rules: {manifest_path}")
    for rel in rules:
        rule_path = pack_dir / rel
        if not rule_path.exists():
            raise SystemExit(f"manifest references missing rule: {rule_path}")
    commands = manifest.get("commands") or {}
    for key in ["build", "test", "testSingle", "lint"]:
        if key not in commands:
            raise SystemExit(f"manifest missing commands.{key}: {manifest_path}")

for rel in [
    "changes/templates/spec.md",
    "changes/templates/tasks.md",
    "changes/templates/test-spec.md",
    "changes/templates/log.md",
    "changes/templates/design-brief.md",
    "changes/templates/quick-card.md",
    "changes/templates/roadmap.md",
]:
    if not (root / rel).exists():
        raise SystemExit(f"missing template: {rel}")
PY

echo "ai-code-copilot framework check passed"
