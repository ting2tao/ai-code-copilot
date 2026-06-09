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
need_file config/project-config.json
need_file docs/harness-engineering.md
need_file hooks/session-start
need_dir rules
need_dir packs
need_dir changes/templates
need_dir tests/fixtures/monorepo

for f in rules/*.md; do
  case "$(basename "$f")" in
    coding-style.md|security.md|domain-rules.md|project-context.md|commit-convention.md|github-metrics.md) ;;
    *) fail "core rules must stay generic; unexpected file in rules/: $f" ;;
  esac
done

bash -n install.sh
bash -n install-wsl.sh
bash -n hooks/session-start
bash -n scripts/init_project.sh

python3 - "$ROOT" <<'PY'
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pack_root = root / "packs"
prompt_text = (root / "agents" / "copilot-prompt.md").read_text(encoding="utf-8")
hook_text = (root / "hooks" / "session-start").read_text(encoding="utf-8")
skill_text = (root / "skill" / "SKILL.md").read_text(encoding="utf-8")
agents_text = (root / "AGENTS.md").read_text(encoding="utf-8")
agents_lines = agents_text.splitlines()
if len(agents_lines) > 120:
    raise SystemExit(f"AGENTS.md must stay a short index; found {len(agents_lines)} lines")
if "docs/harness-engineering.md" not in agents_text:
    raise SystemExit("AGENTS.md must point to docs/harness-engineering.md")
if "Context First, Harness Enables, Code Follows" not in agents_text:
    raise SystemExit("AGENTS.md must use the Harness-enabled core slogan")

frontmatter = skill_text.split("---", 2)[1]
description_lines = []
capture_description = False
for line in frontmatter.splitlines():
    if line == "description: |":
        capture_description = True
        continue
    if capture_description:
        if line.startswith("  "):
            description_lines.append(line[2:])
        else:
            break
description = "\n".join(description_lines)
if len(description) > 500:
    raise SystemExit(f"skill description is too long for reliable discovery: {len(description)} characters")
if "初始化项目" not in description[:160]:
    raise SystemExit("skill description must surface 初始化项目 near the beginning")

def command_set(text, label):
    match = re.search(rf"{label}[:：]\s*([a-z0-9_ /\-]+)", text)
    if not match:
        raise SystemExit(f"missing command menu labeled {label!r}")
    return {part.strip().lstrip("/") for part in match.group(1).split("/") if part.strip()}

prompt_commands = command_set(prompt_text, "可用流程")
hook_commands = command_set(hook_text, "可用命令")
if prompt_commands != hook_commands:
    raise SystemExit(
        "command menus drifted: "
        f"prompt={sorted(prompt_commands)} hook={sorted(hook_commands)}"
    )
if "fix-ci" not in prompt_commands:
    raise SystemExit("command menus must include fix-ci")
if "finish" not in prompt_commands:
    raise SystemExit("command menus must include finish")
for rel in ["agents/copilot-prompt.md", "hooks/session-start", "README.md", "README-CN.md"]:
    text = (root / rel).read_text(encoding="utf-8")
    if "/archive" in text and "不要输入 /archive" not in text:
        raise SystemExit(f"{rel} must warn Codex users not to type /archive")

project_config = json.loads((root / "config" / "project-config.json").read_text(encoding="utf-8"))
github_workflow = project_config.get("githubWorkflow", {})
expected_config = {
    "finishMode": "ask",
    "issueWhenMissing": "ask",
    "createPrAfterReviewPass": False,
    "defaultBaseBranch": "main",
    "pushRemote": "origin",
    "prDraft": False,
}
for key, value in expected_config.items():
    if github_workflow.get(key) != value:
        raise SystemExit(f"project config githubWorkflow.{key} must default to {value!r}")

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
    signals = manifest.get("signals") or []
    verification_matrix = manifest.get("verificationMatrix") or []
    if not signals:
        raise SystemExit(f"pack manifest must define signals: {manifest_path}")
    if len(verification_matrix) < 4:
        raise SystemExit(f"pack manifest must define a verification matrix: {manifest_path}")
    if pack_id == "frontend-react":
        signal_ids = {signal.get("id") for signal in signals}
        for required_signal in ["vite", "next", "typescript", "playwright"]:
            if required_signal not in signal_ids:
                raise SystemExit(f"frontend-react manifest missing signal {required_signal!r}")

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

required_harness_markers = {
    "agents/copilot-prompt.md": ["Harness", "Agent 可见"],
    "agents/spec-reviewer.md": ["Harness", "Agent 可验证"],
    "agents/code-quality-reviewer.md": ["Harness", "Agent 可读"],
    "changes/templates/spec.md": ["Agent Harness", "Agent 可见证据"],
    "changes/templates/quick-card.md": ["Agent Harness", "Agent 可见证据"],
    "changes/templates/test-spec.md": ["Agent Harness", "可观测信号"],
}
for rel, markers in required_harness_markers.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing_markers = [marker for marker in markers if marker not in text]
    if missing_markers:
        raise SystemExit(
            f"{rel} missing Harness markers: " + ", ".join(missing_markers)
        )

test_spec = (root / "changes" / "templates" / "test-spec.md").read_text(encoding="utf-8")
java_only_terms = ["Mockito", "MockMvc", "mvn test", "jacoco", "XxxServiceImpl", "XxxMapper"]
found_java_terms = [term for term in java_only_terms if term in test_spec]
if found_java_terms:
    raise SystemExit(
        "core test-spec template must stay stack-neutral; found Java-only terms: "
        + ", ".join(found_java_terms)
    )
PY

if [ -d tests/fixtures ]; then
  for fixture in tests/fixtures/*; do
    [ -d "$fixture" ] || continue
    tmpdir="$(mktemp -d /tmp/ai-code-copilot-fixture.XXXXXX)"
    cp -R "$fixture"/. "$tmpdir"/
    AI_CODE_COPILOT_HOME="$ROOT" "$ROOT/scripts/init_project.sh" --project "$tmpdir" >/tmp/ai-code-copilot-fixture.out
    test -f "$tmpdir/.ai_code_copilot/.copilot-state.json" || fail "fixture missing state: $fixture"
    test -f "$tmpdir/.ai_code_copilot/config.json" || fail "fixture missing project config: $fixture"
    grep -q '"finishMode": "ask"' "$tmpdir/.ai_code_copilot/config.json" || fail "fixture config missing finishMode ask: $fixture"
    grep -q '"issueWhenMissing": "ask"' "$tmpdir/.ai_code_copilot/config.json" || fail "fixture config missing issueWhenMissing ask: $fixture"
    test -f "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "fixture missing project context: $fixture"
    test -f "$tmpdir/.ai_code_copilot/rules/commit-convention.md" || fail "fixture missing commit convention: $fixture"
    test -f "$tmpdir/.ai_code_copilot/rules/github-metrics.md" || fail "fixture missing github metrics rule: $fixture"
    case "$(basename "$fixture")" in
      java-spring)
        test -f "$tmpdir/.ai_code_copilot/rules/java-spring-coding-style.md" || fail "java fixture did not load java-spring pack"
        test -f "$tmpdir/.ai_code_copilot/rules/java-spring-verification.md" || fail "java fixture did not load java-spring verification rule"
        grep -q '| `java-spring` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "java fixture context missing java-spring command row"
        grep -q '| `java-spring` | Maven' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "java fixture context missing java-spring signal row"
        grep -q '| `java-spring` | Controller endpoints, request/response DTOs, or validation |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "java fixture context missing java-spring verification matrix"
        ;;
      go)
        test -f "$tmpdir/.ai_code_copilot/rules/go-coding-style.md" || fail "go fixture did not load go pack"
        test -f "$tmpdir/.ai_code_copilot/rules/go-verification.md" || fail "go fixture did not load go verification rule"
        grep -q '| `go` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "go fixture context missing go command row"
        grep -q '| `go` | Go module' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "go fixture context missing go signal row"
        grep -q '| `go` | Package API, exported types, or interfaces |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "go fixture context missing go verification matrix"
        ;;
      python)
        test -f "$tmpdir/.ai_code_copilot/rules/python-coding-style.md" || fail "python fixture did not load python pack"
        test -f "$tmpdir/.ai_code_copilot/rules/python-verification.md" || fail "python fixture did not load python verification rule"
        grep -q '| `python` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "python fixture context missing python command row"
        grep -q '| `python` | pyproject.toml' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "python fixture context missing python signal row"
        grep -q '| `python` | Public function signatures, schemas, or typed models |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "python fixture context missing python verification matrix"
        ;;
      frontend-react)
        test -f "$tmpdir/.ai_code_copilot/rules/frontend-react-coding-style.md" || fail "frontend fixture did not load frontend-react pack"
        test -f "$tmpdir/.ai_code_copilot/rules/frontend-react-verification.md" || fail "frontend fixture did not load frontend-react verification rule"
        grep -q '| `frontend-react` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "frontend fixture context missing frontend-react command row"
        grep -q '| `frontend-react` | Vite' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "frontend fixture context missing frontend-react signal row"
        grep -q '| `frontend-react` | TypeScript types or shared contracts |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "frontend fixture context missing frontend-react verification matrix"
        ;;
      monorepo)
        test -f "$tmpdir/.ai_code_copilot/rules/go-coding-style.md" || fail "monorepo fixture did not load go pack"
        test -f "$tmpdir/.ai_code_copilot/rules/go-verification.md" || fail "monorepo fixture did not load go verification rule"
        test -f "$tmpdir/.ai_code_copilot/rules/frontend-react-coding-style.md" || fail "monorepo fixture did not load frontend-react pack"
        test -f "$tmpdir/.ai_code_copilot/rules/frontend-react-verification.md" || fail "monorepo fixture did not load frontend-react verification rule"
        grep -q '| `go` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "monorepo fixture context missing go command row"
        grep -q '| `frontend-react` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "monorepo fixture context missing frontend-react command row"
        grep -q '| `services/api` | `go` | `services/api/go.mod` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "monorepo fixture context missing go module row"
        grep -q '| `apps/web` | `frontend-react` | `apps/web/package.json` |' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "monorepo fixture context missing frontend module row"
        ;;
    esac
    AI_CODE_COPILOT_HOME="$ROOT" "$ROOT/scripts/init_project.sh" --project "$tmpdir" --sync --dry-run >/tmp/ai-code-copilot-fixture-dry-run.out
    if find "$tmpdir/.ai_code_copilot" -name '*.new' -type f | grep -q .; then
      fail "dry-run wrote .new files for fixture: $fixture"
    fi
    printf 'custom project context\n' > "$tmpdir/.ai_code_copilot/rules/project-context.md"
    printf 'custom domain rules\n' > "$tmpdir/.ai_code_copilot/rules/domain-rules.md"
    printf '{"githubWorkflow":{"finishMode":"manual"}}\n' > "$tmpdir/.ai_code_copilot/config.json"
    printf 'old test template\n' > "$tmpdir/.ai_code_copilot/changes/templates/test-spec.md"
    AI_CODE_COPILOT_HOME="$ROOT" "$ROOT/scripts/init_project.sh" --project "$tmpdir" --sync >/tmp/ai-code-copilot-fixture-sync.out
    grep -q 'custom project context' "$tmpdir/.ai_code_copilot/rules/project-context.md" || fail "sync overwrote project-owned project-context: $fixture"
    grep -q 'custom domain rules' "$tmpdir/.ai_code_copilot/rules/domain-rules.md" || fail "sync overwrote project-owned domain-rules: $fixture"
    grep -q '"finishMode":"manual"' "$tmpdir/.ai_code_copilot/config.json" || fail "sync overwrote project-owned config: $fixture"
    test ! -f "$tmpdir/.ai_code_copilot/rules/project-context.md.new" || fail "sync generated project-context.md.new for project-owned rule: $fixture"
    test ! -f "$tmpdir/.ai_code_copilot/rules/domain-rules.md.new" || fail "sync generated domain-rules.md.new for project-owned rule: $fixture"
    test ! -f "$tmpdir/.ai_code_copilot/config.json.new" || fail "sync generated config.json.new for project-owned config: $fixture"
    cmp -s "$ROOT/changes/templates/test-spec.md" "$tmpdir/.ai_code_copilot/changes/templates/test-spec.md" || fail "sync did not update managed test-spec template: $fixture"
    test ! -f "$tmpdir/.ai_code_copilot/changes/templates/test-spec.md.new" || fail "sync generated test-spec.md.new instead of updating managed template: $fixture"
    rm -rf "$tmpdir"
  done
fi

echo "ai-code-copilot framework check passed"
