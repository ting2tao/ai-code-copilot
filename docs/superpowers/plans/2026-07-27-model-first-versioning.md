# Model-First Activation and Semantic Versioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make ordinary low-risk coding model-native, automatically activate ai-code-copilot only for explicit lifecycle or material-risk work, and release the framework as semantic version `0.1.0` with full-replacement updates.

**Architecture:** A compact activation contract in `skill/SKILL.md`, SessionStart, and `workflow-policy.json` lets the platform model decide whether to activate the framework before loading any router. Activated work uses only Compact or Full modules. Root `VERSION` is the release identity; installers validate and replace the managed installation tree, while explicit project sync overwrites framework-managed files and preserves project-owned assets.

**Tech Stack:** Bash, Python 3 standard library, PowerShell, JSON, Markdown, Git.

---

## File Structure

### New files

- `VERSION` — one-line SemVer release identity.
- `scripts/check_model_first_versioning.py` — deterministic version, activation, installer, state, and documentation contract checks.
- `scripts/test_install_overwrite.sh` — hermetic macOS/Linux installer replacement smoke test.
- `changes/model-first-versioning/design-brief.md` — pointer to the approved canonical design and recorded alternatives.
- `changes/model-first-versioning/spec.md` — confirmed Full SDD execution contract.
- `changes/model-first-versioning/tasks.md` — task status linked to this implementation plan.
- `changes/model-first-versioning/test-spec.md` — P0/P1/P2 verification contract.
- `changes/model-first-versioning/log.md` — implementation evidence and decisions.
- `changes/model-first-versioning/summary.md` — bounded active-change state.

### Runtime and policy files

- `skill/SKILL.md` — narrow discovery to explicit lifecycle and semantic escalation signals.
- `config/workflow-policy.json` — model-first activation policy and Compact/Full tier policy.
- `hooks/session-start` — inject compact model-first guidance without loading the skill.
- `agents/router.md` — route only after activation.
- Delete `agents/workflows/inline.md` — native work now occurs before framework activation.
- `agents/workflows/{compact,full,debug,review,test,finish,archive}.md` — replace Inline promotion language with native activation or Compact/Full promotion.
- `agents/{spec-reviewer,code-quality-reviewer}.md` — review the model-first boundary.
- `changes/templates/{quick-card,summary}.md` — record `promotedFrom: native` when native work escalates.

### Version, install, and project sync

- `install.sh` — validate and fully replace a Codex/Claude installation on macOS/Linux.
- `install-wsl.sh` — apply the same replacement contract from WSL.
- `install.ps1` — apply the same replacement contract on Windows.
- `scripts/init_project.sh` — read `VERSION`, overwrite managed project files, preserve project assets, and write version plus commit state.
- `scripts/check_framework.sh` — call focused checks and exercise sync/install fixtures.
- `scripts/check_progressive_sdd.py` — validate model-first activation and Compact/Full routing.

### Documentation

- `README.md` and `README-CN.md` — synchronized user-facing activation, version, install, and sync behavior.
- `AGENTS.md` — concise repository contract.
- `docs/ai-code-copilot-overview.md` — model-first runtime architecture.
- `docs/ai-code-copilot-flow.md` — native/activated flow diagram.
- `docs/ai-code-copilot-team-talk.html` — current presentation wording.
- `docs/harness-engineering.md` and `docs/loop-engineering.md` — native execution and escalation boundary.

Historical design documents and archives remain unchanged.

---

### Task 1: Establish the Full SDD execution record

**Files:**
- Create: `changes/model-first-versioning/design-brief.md`
- Create: `changes/model-first-versioning/spec.md`
- Create: `changes/model-first-versioning/tasks.md`
- Create: `changes/model-first-versioning/test-spec.md`
- Create: `changes/model-first-versioning/log.md`
- Create: `changes/model-first-versioning/summary.md`
- Reference: `docs/superpowers/specs/2026-07-27-model-first-versioning-design.md`
- Reference: `docs/superpowers/plans/2026-07-27-model-first-versioning.md`

- [ ] **Step 1: Create the bounded design brief**

Use this exact contract:

```markdown
# Model-First Versioning Design Brief

status: confirmed
design: docs/superpowers/specs/2026-07-27-model-first-versioning-design.md
confirmed-by: user
confirmed-at: 2026-07-27

## Decision

Use model-first adaptive activation, semantic version `0.1.0`, direct full replacement for the global framework installation, and direct overwrite for framework-managed project files.

## Alternatives rejected

- Always load a micro-router: still charges every coding request.
- Explicit activation only: cannot escalate hidden material risk.
- Compatibility migration and rollback: explicitly excluded by the user.
```

- [ ] **Step 2: Create the confirmed Spec**

The file must start with:

```markdown
# Model-First Activation and Semantic Versioning Spec

status: confirmed
design: docs/superpowers/specs/2026-07-27-model-first-versioning-design.md

## Goal Contract

- Goal: Make low-risk work model-native and publish versioned full-replacement framework updates.
- Done Signal: Acceptance criteria 1-10 in the approved design pass with fresh command output.
- Guardrails: Preserve project-owned assets; require framework activation and human confirmation for material risk; do not preserve global installation edits.
- Fallback: Fail before replacement when the source is invalid; after replacement failure require a clean reinstall.
- Memory: Record only stable version, activation, ownership, and verification lessons at finish/archive.

## Scope

Implement sections 6-13 of the approved design.

## Non-goals

Use section 4 of the approved design without adding compatibility, rollback, online update checks, or release automation.

## Acceptance

Use all ten acceptance criteria from section 15 of the approved design as mandatory.
```

- [ ] **Step 3: Create tasks, test spec, log, and summary**

`tasks.md` must list Tasks 1-7 from this plan. `test-spec.md` must classify activation/version/install/sync checks as P0, documentation drift and syntax checks as P1, and Windows runtime smoke as P2 when unavailable locally. Initialize `log.md` with the approved decisions and baseline command:

```text
bash scripts/check_framework.sh
exit: 0
summary: progressive-sdd policy and framework checks passed before implementation
```

Create `summary.md` with:

```text
change: model-first-versioning
status: in-apply
goal: model-first activation and semantic version 0.1.0 with full replacement updates
scope: runtime policy installers project sync checks docs
open-risks: model activation is semantic and Windows runtime smoke may be unavailable locally
loaded-knowledge: none
```

- [ ] **Step 4: Record the real Spec hash**

Run:

```bash
shasum -a 256 changes/model-first-versioning/spec.md
```

Use `apply_patch` to insert `spec-hash: sha256:<the exact command output hash>` immediately after `status: in-apply` in `summary.md`. Re-run `shasum` and verify the recorded value exactly matches; no `pending`, placeholder, or abbreviated hash is allowed.

- [ ] **Step 5: Verify record completeness**

Run:

```bash
for file in design-brief.md spec.md tasks.md test-spec.md log.md summary.md; do
  test -s "changes/model-first-versioning/$file"
done
```

Expected: exit `0`.

- [ ] **Step 6: Commit**

```bash
git add changes/model-first-versioning
git commit -m "docs(model-first-versioning): establish execution records"
```

---

### Task 2: Add the semantic version contract and RED checks

**Files:**
- Create: `VERSION`
- Create: `scripts/check_model_first_versioning.py`
- Modify: `scripts/check_framework.sh:20-52`

- [ ] **Step 1: Add failing framework entry checks**

Add before the current shell syntax checks:

```bash
need_file VERSION
need_file scripts/check_model_first_versioning.py
```

Add after `python3 scripts/check_progressive_sdd.py "$ROOT"`:

```bash
python3 scripts/check_model_first_versioning.py "$ROOT"
```

- [ ] **Step 2: Run the check to verify RED**

Run:

```bash
bash scripts/check_framework.sh
```

Expected: non-zero with `FAIL: missing file: VERSION`.

- [ ] **Step 3: Create the initial version**

Create `VERSION` with exactly:

```text
0.1.0
```

- [ ] **Step 4: Create the focused checker**

Implement these interfaces in `scripts/check_model_first_versioning.py`:

```python
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


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    version = read_version(root)
    if behavior_changed_from_base(root) and not version_changed_from_base(root, version):
        fail("framework behavior changed without a VERSION bump")
    print(f"model-first-versioning: version {version} checks passed")


if __name__ == "__main__":
    main()
```

Later tasks extend this checker without changing `read_version`.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
bash scripts/check_framework.sh
```

Expected:

```text
model-first-versioning: version 0.1.0 checks passed
ai-code-copilot framework check passed
```

- [ ] **Step 6: Commit**

```bash
git add VERSION scripts/check_model_first_versioning.py scripts/check_framework.sh
git commit -m "feat(version): add semantic version contract"
```

---

### Task 3: Make activation model-first

**Files:**
- Modify: `scripts/check_model_first_versioning.py`
- Modify: `scripts/check_progressive_sdd.py`
- Modify: `config/workflow-policy.json`
- Modify: `skill/SKILL.md`
- Modify: `hooks/session-start`
- Modify: `agents/router.md`
- Delete: `agents/workflows/inline.md`

- [ ] **Step 1: Extend the checker with failing activation assertions**

Add:

```python
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
    for forbidden in ["实现/开发/写代码/加功能", "优化/重构/refactor", "修 bug/debug"]:
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
```

Call `check_activation_contract(root)` from `main()`.

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
```

Expected: non-zero with `activation.defaultPath must be native`.

- [ ] **Step 3: Replace the workflow policy**

Set policy version `2` and use:

```json
{
  "version": 2,
  "activation": {
    "defaultPath": "native",
    "explicitIntents": [
      "init", "sync", "upgrade", "brainstorm", "propose", "apply",
      "fix-ci", "review", "finish", "publish", "test", "archive"
    ],
    "mustActivateSignals": [
      "security", "authentication", "permission", "sensitive-data",
      "money", "destructive-operation", "production", "deployment", "ci",
      "dependency", "database", "schema", "generated-artifact",
      "public-api", "state-machine", "cross-module-business-rule",
      "session-handoff", "durable-decision", "auditable-review",
      "commit", "publish", "repeated-investigation",
      "material-uncertainty"
    ],
    "lowRiskOverrideAllowed": true
  },
  "tiers": {
    "compact": {
      "maxFiles": 5
    },
    "full": {
      "riskCategories": [
        "public-api", "schema", "database", "dependency", "ci",
        "deployment", "generated-artifact", "security", "permission",
        "authentication", "sensitive-data", "money", "state-machine",
        "cross-module-business-rule", "accepted-residual-risk"
      ]
    }
  },
  "promotion": {
    "toFull": [
      "full-risk-discovered", "material-reverse-sync",
      "important-review-correction", "critical-review-correction",
      "durable-knowledge", "open-risk", "multiple-review-units"
    ]
  },
  "git": {
    "allowedTypes": [
      "feat", "fix", "docs", "refactor", "test",
      "chore", "perf", "ci", "build"
    ]
  },
  "github": {
    "issuePolicies": ["always", "on-commit", "on-publish", "manual"],
    "newProjectDefault": "on-publish",
    "legacyDefault": "always",
    "closeTarget": "workIssue",
    "manualNoIssueCloseTarget": "none"
  }
}
```

- [ ] **Step 4: Narrow the skill entry**

The frontmatter description must state:

```yaml
description: |
  Use for explicit ai-code-copilot lifecycle requests such as 初始化项目/init/sync/upgrade,
  brainstorm/propose/apply/fix-ci/review/finish/publish/test/archive, or when the model detects
  security, permission, money, production, deployment, database, public-contract, persistent,
  audit, or cross-session risk. Do not use for ordinary low-risk implementation, debugging,
  refactoring, tests, documentation, discussion, or read-only analysis; handle those natively
  unless material risk or uncertainty appears.
```

Replace the hard gate with only:

```text
Native path: ordinary bounded low-risk work does not activate this skill.
Compact SDD: persisted work requires a valid quick-card.md before editing.
Full SDD: material risk requires a confirmed Spec and human confirmation where required.
```

Missing router, policy, or selected module must now fail with an upgrade instruction; do not load the monolithic prompt as a compatibility fallback.

- [ ] **Step 5: Update SessionStart and router**

Replace the current “帮我实现” activation hint with:

```text
模型优先：普通、边界明确、低风险且可直接验证的任务由模型原生处理，不自动加载 ai-code-copilot。
当请求显式进入 init/propose/review/finish/archive 等生命周期，或模型判断涉及安全、权限、资金、生产、部署、数据库、公共契约、持久化、审计、跨会话或重大不确定性时，自动激活 ai-code-copilot。
用户可要求低风险任务直接处理；不得借此绕过破坏性操作、外部写入或安全/权限/资金/生产风险的人工确认。
```

In `agents/router.md`, state that the skill is already activated, remove the low-risk Inline row, and route persisted small work to Compact and material risk to Full. Delete `agents/workflows/inline.md`.

- [ ] **Step 6: Rewrite classifier fixtures**

Replace the Inline/Compact/Full classifier in `scripts/check_progressive_sdd.py` with:

```python
def should_activate(policy: dict, facts: dict) -> bool:
    activation = policy["activation"]
    if facts.get("explicitIntent") in activation["explicitIntents"]:
        return True
    signals = set(facts.get("signals", []))
    if signals & set(activation["mustActivateSignals"]):
        return True
    return False


def classify_activated(policy: dict, facts: dict) -> str:
    risks = set(facts.get("risks", []))
    full_risks = set(policy["tiers"]["full"]["riskCategories"])
    if (
        risks & full_risks
        or facts.get("acceptedResidualRisk", False)
        or facts.get("files", 0) > policy["tiers"]["compact"]["maxFiles"]
        or facts.get("multipleDeliverableGoals", False)
        or facts.get("multipleReviewUnits", False)
    ):
        return "full"
    return "compact"
```

Fixtures must prove a normal local bugfix stays native, security activates Full, `finish` activates, and persisted documentation work activates Compact.

- [ ] **Step 7: Verify GREEN**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
python3 scripts/check_progressive_sdd.py .
bash hooks/session-start | python3 -m json.tool >/dev/null
```

Expected: both Python checks pass and SessionStart emits valid JSON.

- [ ] **Step 8: Commit**

```bash
git add config/workflow-policy.json skill/SKILL.md hooks/session-start agents/router.md \
  agents/workflows/inline.md scripts/check_progressive_sdd.py scripts/check_model_first_versioning.py
git commit -m "feat(runtime): make framework activation model-first"
```

---

### Task 4: Align activated workflows, reviewers, and records

**Files:**
- Modify: `agents/workflows/{compact,full,debug,review,test,finish,archive}.md`
- Modify: `agents/{spec-reviewer,code-quality-reviewer}.md`
- Modify: `changes/templates/{quick-card,summary}.md`
- Modify: `scripts/check_progressive_sdd.py`
- Modify: `scripts/check_framework.sh`

- [ ] **Step 1: Add failing marker checks**

Require:

```python
native_escalation_records = {
    "agents/workflows/compact.md": ["Native -> Compact", "promotedFrom: native"],
    "agents/workflows/full.md": ["Native -> Full", "material confirmation"],
    "agents/spec-reviewer.md": ["Native -> Compact", "Native -> Full"],
    "changes/templates/quick-card.md": ["promotedFrom: native"],
}
```

Also fail if active runtime files outside historical specs contain `Inline SDD`, `Inline -> Compact`, or `Inline -> Full`.

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
```

Expected: non-zero naming the first stale Inline marker.

- [ ] **Step 3: Update workflow language**

Apply these exact semantics:

- Native work has no framework record.
- When native work needs persistence, stop and create Compact with `promotedFrom: native`, current diff, and actual evidence.
- When native work discovers material risk, stop and create Full, then obtain material confirmation.
- Activated Compact may promote only to Full.
- Review, finish, archive, and test modules never imply that ordinary coding had to activate the skill.
- `summary.md` is used only for Full; Compact continues to use `quick-card.md`.

Do not change Issue close-target semantics.

- [ ] **Step 4: Verify GREEN**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash scripts/check_framework.sh
```

Expected: both checks pass.

- [ ] **Step 5: Commit**

```bash
git add agents/workflows agents/spec-reviewer.md agents/code-quality-reviewer.md \
  changes/templates scripts/check_progressive_sdd.py scripts/check_framework.sh
git commit -m "refactor(workflow): align records with native activation"
```

---

### Task 5: Implement full-replacement installers

**Files:**
- Create: `scripts/test_install_overwrite.sh`
- Modify: `scripts/check_model_first_versioning.py`
- Modify: `scripts/check_framework.sh`
- Modify: `install.sh`
- Modify: `install-wsl.sh`
- Modify: `install.ps1`

- [ ] **Step 1: Add failing static and integration checks**

The Python checker must fail if any installer retains `git pull` or commit-as-version output. Require these markers:

```python
installer_markers = {
    "install.sh": ["validate_source_tree", "replace_install_tree", "VERSION"],
    "install-wsl.sh": ["validate_source_tree", "replace_install_tree", "VERSION"],
    "install.ps1": ["Test-SourceTree", "Replace-InstallTree", "VERSION"],
}
```

Create `scripts/test_install_overwrite.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP_ROOT="$(mktemp -d)"
trap 'rm -rf "$TMP_ROOT"' EXIT

export HOME="$TMP_ROOT/home"
mkdir -p "$HOME"

first_output="$TMP_ROOT/first.out"
second_output="$TMP_ROOT/second.out"
expected_version="$(tr -d '\r\n' < "$ROOT/VERSION")"

(
  cd "$ROOT"
  bash install.sh --codex
) >"$first_output"

install_dir="$HOME/.codex/ai_code_copilot"
test "$(cat "$install_dir/VERSION")" = "$expected_version"
printf '%s\n' stale >"$install_dir/obsolete-framework-file"
printf '%s\n' local-change >>"$install_dir/README.md"

(
  cd "$ROOT"
  bash install.sh --codex
) >"$second_output"

test ! -e "$install_dir/obsolete-framework-file"
cmp "$ROOT/README.md" "$install_dir/README.md"
grep -q "当前版本: $expected_version" "$second_output"
test -L "$HOME/.codex/skills/ai-code-copilot"

python3 - "$HOME/.codex/settings.json" "$install_dir/hooks/session-start" <<'PY'
import json
import sys

settings = json.load(open(sys.argv[1], encoding="utf-8"))
hook = sys.argv[2]
commands = [
    item["command"]
    for entry in settings["hooks"]["SessionStart"]
    for item in entry["hooks"]
]
raise SystemExit(0 if any(hook in command for command in commands) else 1)
PY

echo "install-overwrite: macOS/Linux smoke passed"
```

Add `bash scripts/test_install_overwrite.sh` to `check_framework.sh`.

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
bash scripts/test_install_overwrite.sh
```

Expected: static check fails on `git pull`; smoke test leaves the obsolete file or local README change.

- [ ] **Step 3: Implement Bash replacement primitives**

Both Bash installers must define:

```bash
validate_source_tree() {
  local source_dir="$1"
  [ -f "$source_dir/VERSION" ] || err "安装源缺少 VERSION"
  [ -f "$source_dir/skill/SKILL.md" ] || err "安装源缺少 skill/SKILL.md"
  [ -f "$source_dir/agents/router.md" ] || err "安装源缺少 agents/router.md"
  local version
  version="$(tr -d '\r\n' < "$source_dir/VERSION")"
  [[ "$version" =~ ^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)([-+][0-9A-Za-z.-]+)?$ ]] \
    || err "VERSION 不是有效 SemVer: $version"
}

replace_install_tree() {
  local source_dir="$1"
  local stage_dir="${INSTALL_DIR}.stage.$$"
  rm -rf "$stage_dir"
  mkdir -p "$stage_dir"
  rsync -a --delete --exclude='.git' --exclude='.DS_Store' "$source_dir/" "$stage_dir/"
  cd "$APP_HOME"
  rm -rf "$INSTALL_DIR"
  mv "$stage_dir" "$INSTALL_DIR"
}
```

For a Git source checkout, use it directly. Otherwise clone `REPO_URL` into a temporary source directory, validate it, replace the install tree, and delete the temporary clone. Do not use `git pull`.

- [ ] **Step 4: Implement PowerShell replacement primitives**

Use:

```powershell
function Test-SourceTree([string]$SourceDir) {
    $versionPath = Join-Path $SourceDir "VERSION"
    if (-not (Test-Path $versionPath)) { throw "安装源缺少 VERSION" }
    $version = (Get-Content $versionPath -Raw -Encoding UTF8).Trim()
    if ($version -notmatch '^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)([-+][0-9A-Za-z.-]+)?$') {
        throw "VERSION 不是有效 SemVer: $version"
    }
    foreach ($relative in @("skill\SKILL.md", "agents\router.md")) {
        if (-not (Test-Path (Join-Path $SourceDir $relative))) {
            throw "安装源缺少 $relative"
        }
    }
}

function Replace-InstallTree([string]$SourceDir) {
    $stageDir = "$InstallDir.stage.$PID"
    if (Test-Path $stageDir) { Remove-Item $stageDir -Recurse -Force }
    New-Item -ItemType Directory -Path $stageDir -Force | Out-Null
    Get-ChildItem $SourceDir -Force |
        Where-Object { $_.Name -notin @(".git", ".DS_Store") } |
        Copy-Item -Destination $stageDir -Recurse -Force
    if (Test-Path $InstallDir) { Remove-Item $InstallDir -Recurse -Force }
    Move-Item $stageDir $InstallDir
}
```

Use a temporary `git clone` when the invocation is not from a Git source checkout.

- [ ] **Step 5: Report semantic version**

All installers read `$INSTALL_DIR/VERSION` and print:

```text
当前版本: 0.1.0
```

Git commit may be printed separately when available. It must never replace the semantic version.

- [ ] **Step 6: Verify GREEN**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
bash scripts/test_install_overwrite.sh
bash -n install.sh install-wsl.sh
command -v pwsh >/dev/null && pwsh -NoProfile -Command '$null = [scriptblock]::Create((Get-Content ./install.ps1 -Raw))'
```

Expected: static and macOS/Linux smoke checks pass. PowerShell parse passes when `pwsh` exists; otherwise record that the runtime check was unavailable.

- [ ] **Step 7: Commit**

```bash
git add install.sh install-wsl.sh install.ps1 scripts/test_install_overwrite.sh \
  scripts/check_model_first_versioning.py scripts/check_framework.sh
git commit -m "feat(install): replace framework tree by version"
```

---

### Task 6: Overwrite managed project files and record framework version

**Files:**
- Modify: `scripts/init_project.sh`
- Modify: `scripts/check_framework.sh`
- Modify: `scripts/check_model_first_versioning.py`

- [ ] **Step 1: Add failing sync fixture assertions**

Extend every fixture verification to assert:

```python
state = json.loads((project / ".ai_code_copilot/.copilot-state.json").read_text())
assert state["frameworkVersion"] == "0.1.0"
assert state["frameworkCommit"]
```

Add one overwrite fixture that:

1. Initializes a project.
2. Replaces `.ai_code_copilot/rules/coding-style.md` with `local managed edit`.
3. Replaces `.ai_code_copilot/rules/domain-rules.md` with `project domain asset`.
4. Adds `.ai_code_copilot/knowledge/custom.md`.
5. Runs `--sync`.
6. Asserts coding style equals the framework source, domain rules and knowledge remain unchanged, and no `.new` file exists.

Add one invalid-config fixture that expects non-zero exit and unchanged config.

- [ ] **Step 2: Verify RED**

Run:

```bash
bash scripts/check_framework.sh
```

Expected: failure because `frameworkVersion` is absent or managed rules still create `.new`.

- [ ] **Step 3: Add strict version loading**

Inside the embedded Python program:

```python
def framework_version():
    version_path = copilot_home / "VERSION"
    version = version_path.read_text(encoding="utf-8")
    if not re.fullmatch(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\n",
        version,
    ):
        raise SystemExit(f"invalid framework VERSION: {version_path}")
    return version.strip()
```

Call it before any destination directories or files are created.

- [ ] **Step 4: Replace managed files directly**

Rename `write_managed_template` to `write_managed` and use it for:

- All generic core rules except `project-context.md` and `domain-rules.md`.
- All matched pack rules.
- All change templates.
- Managed state.

Use `write_project_owned` for config, project context, domain rules, knowledge, active changes, and archives. Remove `.new` candidate generation and migration messages.

Invalid JSON, a non-object config root, a non-object `githubWorkflow`, or missing required `issuePolicy` must exit non-zero without rewriting config.

- [ ] **Step 5: Write fresh versioned state**

The state builder must begin:

```python
data = OrderedDict()
data["frameworkVersion"] = framework_version()
data["frameworkCommit"] = framework_commit()
data["mode"] = mode
data["initializedAt"] = now
data["lastSyncedAt"] = now
data["projectContextSyncedAt"] = now_utc
```

Update `syncPolicy` to state that framework-managed rules, pack rules, templates, and state are overwritten, while config, project context, domain rules, knowledge, active changes, and archives are preserved.

- [ ] **Step 6: Verify GREEN**

Run:

```bash
bash scripts/check_framework.sh
bash scripts/init_project.sh --project tests/fixtures/go --upgrade --dry-run
```

Expected: framework check passes; dry-run lists managed updates without creating `.new` files or writing fixture files.

- [ ] **Step 7: Commit**

```bash
git add scripts/init_project.sh scripts/check_framework.sh scripts/check_model_first_versioning.py
git commit -m "feat(sync): overwrite managed files and record version"
```

---

### Task 7: Synchronize runtime and user documentation

**Files:**
- Modify: `README.md`
- Modify: `README-CN.md`
- Modify: `AGENTS.md`
- Modify: `docs/ai-code-copilot-overview.md`
- Modify: `docs/ai-code-copilot-flow.md`
- Modify: `docs/ai-code-copilot-team-talk.html`
- Modify: `docs/harness-engineering.md`
- Modify: `docs/loop-engineering.md`
- Modify: `scripts/check_model_first_versioning.py`
- Modify: `scripts/check_framework.sh`

- [ ] **Step 1: Add failing documentation markers**

Require the following concepts:

```python
docs = {
    "README.md": [
        "Model-first", "native", "automatic activation", "VERSION",
        "0.1.0", "full replacement", "frameworkVersion", "frameworkCommit"
    ],
    "README-CN.md": [
        "模型优先", "原生处理", "自动激活", "VERSION",
        "0.1.0", "整包覆盖", "frameworkVersion", "frameworkCommit"
    ],
    "AGENTS.md": ["模型优先", "原生处理", "自动激活", "VERSION", "整包覆盖"],
    "docs/ai-code-copilot-overview.md": ["Native", "Compact", "Full", "模型判断"],
}
```

Fail if current docs outside historical specs say installers use `git pull`, generic rule differences create `.new`, or Inline SDD is the default coding path.

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
```

Expected: non-zero naming the first missing README marker.

- [ ] **Step 3: Update English and Chinese README together**

Document:

- Native -> Compact -> Full, with native outside the skill.
- Explicit and semantic automatic activation.
- `VERSION` and `v${VERSION}` release tags.
- Full-replacement update and loss of installation-local edits.
- No compatibility migration or automatic rollback.
- Direct overwrite of framework-managed project files.
- Exact preserved project-owned assets.
- `frameworkVersion` plus `frameworkCommit`.

Remove statements that updates run `git pull` or changed generic rules become `.new`.

- [ ] **Step 4: Update repository and architecture docs**

Keep AGENTS under 120 lines. Update diagrams from `Inline -> Compact -> Full` to `Native -> Activate -> Compact/Full`. Historical approved specs remain unchanged. Update the team-talk HTML only where it describes the current runtime.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python3 scripts/check_model_first_versioning.py .
bash scripts/check_framework.sh
git diff --check
```

Expected: all pass.

- [ ] **Step 6: Commit**

```bash
git add README.md README-CN.md AGENTS.md docs scripts/check_model_first_versioning.py \
  scripts/check_framework.sh
git commit -m "docs(runtime): document model-first versioned updates"
```

---

### Task 8: Final verification and review readiness

**Files:**
- Modify: `changes/model-first-versioning/{tasks,test-spec,log,summary}.md`
- Verify: all changed runtime, installer, sync, test, and documentation files

- [ ] **Step 1: Run targeted checks**

```bash
python3 scripts/check_model_first_versioning.py .
python3 scripts/check_progressive_sdd.py .
bash scripts/test_install_overwrite.sh
```

Expected: all three report passed.

- [ ] **Step 2: Run the full framework gate**

```bash
bash scripts/check_framework.sh
```

Expected:

```text
progressive-sdd: policy and module checks passed
model-first-versioning: version 0.1.0 checks passed
ai-code-copilot framework check passed
```

- [ ] **Step 3: Run syntax and diff checks**

```bash
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh \
  scripts/test_install_overwrite.sh install.sh install-wsl.sh
git diff --check origin/main...HEAD
```

Expected: exit `0` with no output from `git diff --check`.

- [ ] **Step 4: Run PowerShell validation when available**

```bash
if command -v pwsh >/dev/null; then
  pwsh -NoProfile -Command '$null = [scriptblock]::Create((Get-Content ./install.ps1 -Raw))'
else
  printf '%s\n' "PowerShell runtime unavailable; static contract checks only"
fi
```

Expected: parse success, or the explicit limitation message.

- [ ] **Step 5: Inspect scope**

```bash
git status --short
git diff --stat origin/main...HEAD
git log --oneline origin/main..HEAD
```

Expected: only approved design, plan, change records, runtime/policy, installers, sync/check scripts, and synchronized documentation.

- [ ] **Step 6: Update execution evidence**

Mark Tasks 1-8 complete, record every command and exit code in `log.md`, update `test-spec.md` with actual evidence, replace `summary.md` status with `in-review`, and replace `spec-hash` with:

```bash
shasum -a 256 changes/model-first-versioning/spec.md
```

- [ ] **Step 7: Commit final evidence**

```bash
git add changes/model-first-versioning
git commit -m "docs(model-first-versioning): record verification evidence"
```

- [ ] **Step 8: Request review**

Run Spec Compliance against the approved design and Code Quality against the implementation. Do not tag `v0.1.0`, push, or create a PR until finish/publish is explicitly authorized and the work Issue policy is satisfied.
