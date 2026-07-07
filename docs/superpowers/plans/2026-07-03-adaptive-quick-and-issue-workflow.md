# Adaptive Quick and Issue Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Quick changes choose a deterministic compact/full record mode, automatically create the correct work Issue after contract confirmation, and enforce `type/scope` branches plus `type(scope): description` commits.

**Architecture:** Keep the framework's three public complexity levels and treat compact Quick as a storage strategy inside Quick. Markdown templates remain the durable contract; `agents/copilot-prompt.md` orchestrates lifecycle transitions, `hooks/session-start` reads compact metadata when `summary.md` is absent, and `scripts/check_framework.sh` provides executable contract tests for prompts, templates, config migration, Git formats, and fixture behavior.

**Tech Stack:** Markdown prompt/rule/template files, Bash, embedded Python 3, GitHub CLI/API contracts, repository fixture tests.

**Source of truth:** `docs/superpowers/specs/2026-07-03-adaptive-quick-and-issue-workflow-design.md`, work Issue `#30`.

---

## File Map

| Responsibility | Files |
|---|---|
| Executable framework contracts | `scripts/check_framework.sh`, `tests/fixtures/**` |
| Quick classification and lifecycle orchestration | `agents/copilot-prompt.md` |
| Active compact-change discovery | `hooks/session-start` |
| Git, Issue, and PR policy | `rules/commit-convention.md`, `rules/github-metrics.md` |
| Independent review behavior | `agents/spec-reviewer.md`, `agents/code-quality-reviewer.md` |
| Durable change records | `changes/templates/quick-card.md`, `spec.md`, `tasks.md`, `summary.md`, `log.md` |
| Default config and preserved-config migration | `config/project-config.json`, `scripts/init_project.sh` |
| User-facing behavior | `README.md`, `README-CN.md`, `AGENTS.md`, `docs/ai-code-copilot-overview.md` |

### Task 1: Enforce the Git contract

**Files:**
- Modify: `scripts/check_framework.sh:109-131`
- Modify: `rules/commit-convention.md:19-101`
- Modify: `agents/copilot-prompt.md:318-330,653-666`

- [ ] **Step 1: Add failing Git-contract assertions**

Add this inside the existing embedded Python block in `scripts/check_framework.sh`, after config validation:

```python
allowed_types = "feat|fix|docs|refactor|test|chore|perf|ci|build"
branch_pattern = re.compile(rf"^({allowed_types})/[a-z0-9]+(?:-[a-z0-9]+)*$")
commit_pattern = re.compile(rf"^({allowed_types})\([a-z0-9]+(?:-[a-z0-9]+)*\): .+$")

for value in ["feat/issue-workflow", "docs/readme-sync"]:
    if not branch_pattern.fullmatch(value):
        raise SystemExit(f"valid branch rejected: {value}")
for value in ["codex/issue-workflow", "feat/Issue_Workflow", "feat/issue/workflow"]:
    if branch_pattern.fullmatch(value):
        raise SystemExit(f"invalid branch accepted: {value}")

for value in [
    "feat(issue-workflow): create work issue",
    "docs(readme-sync): 同步中英文说明",
]:
    if not commit_pattern.fullmatch(value):
        raise SystemExit(f"valid commit rejected: {value}")
for value in ["feat: missing scope", "[issue-7] fix: bad prefix", "feat(Issue): bad scope"]:
    if commit_pattern.fullmatch(value):
        raise SystemExit(f"invalid commit accepted: {value}")

git_contract_files = {
    "agents/copilot-prompt.md": ["type/scope", "type(scope): description"],
    "rules/commit-convention.md": ["type/scope", "type(scope): description"],
}
for rel, markers in git_contract_files.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit(f"{rel} missing Git contract markers: {missing}")
```

- [ ] **Step 2: Run the check and confirm the new contract fails**

Run:

```bash
bash scripts/check_framework.sh
```

Expected: FAIL with `agents/copilot-prompt.md missing Git contract markers` or `rules/commit-convention.md missing Git contract markers`.

- [ ] **Step 3: Replace optional-scope guidance with the mandatory contract**

In `rules/commit-convention.md`, define:

```markdown
## 2. 分支管理

- 分支名称必须使用 `type/scope`。
- type 仅允许：`feat`、`fix`、`docs`、`refactor`、`test`、`chore`、`perf`、`ci`、`build`。
- scope 必须是描述模块或能力的小写 kebab-case；Issue 编号不是 scope。
- 分支冲突时停止并询问复用或人工处理，禁止静默添加时间戳。

## 3. Commit Message

- commit subject 必须使用 `type(scope): description`，scope 不可省略。
- description 必须说明实际变更，不添加 `[issue-123]` 等前缀。
```

Update the `/apply` commit section and final Git summary in `agents/copilot-prompt.md` to use the same allowed types, branch validation, and mandatory scope. Add a preflight rule that a mismatched branch blocks edits and commits.

- [ ] **Step 4: Run the focused and full checks**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: `ai-code-copilot framework check passed`; `git diff --check` exits 0.

- [ ] **Step 5: Commit the Git contract**

```bash
git add scripts/check_framework.sh rules/commit-convention.md agents/copilot-prompt.md
git commit -m "docs(git-contract): 强制分支与提交格式"
```

### Task 2: Add the parent/work Issue data contract and compact Quick template

**Files:**
- Modify: `scripts/check_framework.sh:109-200,274-350`
- Modify: `changes/templates/quick-card.md:1-58`
- Modify: `changes/templates/spec.md:1-10`
- Modify: `changes/templates/tasks.md:12-19`
- Modify: `changes/templates/summary.md:1-10`
- Modify: `changes/templates/log.md:8-21,48-112,174-188`
- Modify: `config/project-config.json:7-14`
- Modify: `scripts/init_project.sh:439-501`

- [ ] **Step 1: Add failing template and config assertions**

Add these assertions to the embedded Python block in `scripts/check_framework.sh`:

```python
if "issueWhenMissing" in github_workflow:
    raise SystemExit("project config must not configure mandatory Issue creation")

quick_card = (root / "changes/templates/quick-card.md").read_text(encoding="utf-8")
for marker in [
    "recordMode:", "parentIssue:", "workIssue:", "issueRelationship:",
    "closeTarget:", "branch:", "## Execution record", "## Commit record",
    "## Review record", "## Finish record",
]:
    if marker not in quick_card:
        raise SystemExit(f"quick-card.md missing compact marker: {marker}")

for rel in ["changes/templates/spec.md", "changes/templates/summary.md", "changes/templates/log.md"]:
    text = (root / rel).read_text(encoding="utf-8")
    for marker in ["parentIssue", "workIssue", "closeTarget", "branch"]:
        if marker not in text:
            raise SystemExit(f"{rel} missing Issue contract marker: {marker}")
```

Change the fixture expectation at the bottom of `scripts/check_framework.sh` from requiring `issueWhenMissing` to rejecting it in newly initialized config.

- [ ] **Step 2: Run the check and verify RED**

Run:

```bash
bash scripts/check_framework.sh
```

Expected: FAIL with `project config must not configure mandatory Issue creation`.

- [ ] **Step 3: Remove Issue policy from default config**

Change `config/project-config.json` so `githubWorkflow` contains only PR handoff controls:

```json
"githubWorkflow": {
  "finishMode": "ask",
  "createPrAfterReviewPass": false,
  "defaultBaseBranch": "main",
  "pushRemote": "origin",
  "prDraft": false
}
```

Do not add a replacement Issue-creation setting.

- [ ] **Step 4: Turn `quick-card.md` into a compact/full-capable record**

Add machine-readable metadata at the top:

```yaml
---
change: {change-name}
status: proposed
recordMode: compact | full
specHash: {sha256}
parentIssue: none | #123 | URL
workIssue: pending | #456 | URL
issueRelationship: pending | sub-issue | standalone
closeTarget: workIssue
branch: type/scope
---
```

Keep the current requirement, Harness, Goal Contract, Domain Check, and rollback sections. Append exact compact record sections:

```markdown
## Execution record

| command | exit code | output summary | Loop Evidence |
|---|---:|---|---|

## Commit record

| hash | message |
|---|---|

## Review record

| Spec Compliance | Code Quality | GitHub Readiness | open risks |
|---|---|---|---|

## Finish record

| PR | base | remote | closing statement | parent reference | final validation |
|---|---|---|---|---|---|
```

- [ ] **Step 5: Align Standard/full templates**

Replace the single `关联 Issue` concept in `spec.md`, `summary.md`, and `log.md` with `parentIssue`, `workIssue`, `issueRelationship`, `closeTarget`, and `branch`. Update `tasks.md` preflight to require a resolved work Issue and a valid branch before implementation.

For full Quick and Standard/Complex, keep `log.md` and `summary.md`; for compact Quick, document that `quick-card.md` owns these records.

- [ ] **Step 6: Emit a migration note without rewriting project-owned config**

After `config_status` is calculated in `scripts/init_project.sh`, inspect an existing config:

```python
obsolete_issue_config = False
if config_path.exists():
    try:
        existing_config = json.loads(config_path.read_text(encoding="utf-8"))
        obsolete_issue_config = "issueWhenMissing" in existing_config.get("githubWorkflow", {})
    except Exception:
        pass
```

After event output, print:

```python
if obsolete_issue_config:
    print("migration-note: githubWorkflow.issueWhenMissing is obsolete and ignored; project-owned config was preserved.")
```

Update the sync fixture to preserve a config containing `issueWhenMissing` and assert both preservation and the migration-note output.

- [ ] **Step 7: Run checks and commit**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: framework check passes; fixture output confirms new configs omit the obsolete key and existing configs remain untouched.

Commit:

```bash
git add scripts/check_framework.sh scripts/init_project.sh config/project-config.json changes/templates
git commit -m "feat(change-record): 支持 compact Quick 与 Issue 合同"
```

### Task 3: Make SessionStart understand compact Quick metadata

**Files:**
- Modify: `scripts/check_framework.sh:274-352`
- Modify: `hooks/session-start:57-116`

- [ ] **Step 1: Add a failing compact SessionStart fixture**

In `scripts/check_framework.sh`, create a temporary initialized project with one active change containing only `quick-card.md`:

```bash
compact_project="$(mktemp -d /tmp/ai-code-copilot-compact.XXXXXX)"
mkdir -p "$compact_project/.ai_code_copilot/changes/tiny-doc-fix"
cat > "$compact_project/.ai_code_copilot/changes/tiny-doc-fix/quick-card.md" <<'EOF'
---
change: tiny-doc-fix
status: in-apply
recordMode: compact
specHash: sha256:test
parentIssue: none
workIssue: "#42"
issueRelationship: standalone
closeTarget: workIssue
branch: docs/tiny-doc-fix
---
EOF
compact_output="$(cd "$compact_project" && "$ROOT/hooks/session-start")"
grep -q 'recordMode: compact' <<<"$compact_output" || fail "SessionStart did not load compact Quick metadata"
grep -q 'workIssue: "#42"' <<<"$compact_output" || fail "SessionStart omitted compact workIssue"
rm -rf "$compact_project"
```

- [ ] **Step 2: Run the fixture and verify RED**

Run:

```bash
bash scripts/check_framework.sh
```

Expected: FAIL with `SessionStart did not load compact Quick metadata`.

- [ ] **Step 3: Add metadata fallback to the hook**

Replace `summary_status()` with helpers that prefer `summary.md` and fall back to Quick Card front matter:

```python
def field_value(path, key):
    if not path.exists():
        return None
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith(f"{key}:"):
                return line.split(":", 1)[1].strip().strip('"')
    except Exception:
        return None
    return None

def change_status(change):
    return field_value(change / "summary.md", "status") or field_value(change / "quick-card.md", "status")
```

When one active change has no `summary.md`, read only the Quick Card front-matter fields `change`, `status`, `recordMode`, `specHash`, `parentIssue`, `workIssue`, `issueRelationship`, and `branch`. Do not inject the requirement body or execution history.

- [ ] **Step 4: Verify compact and existing summary behavior**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: compact fixture passes; existing finished-summary and active-summary checks remain green.

- [ ] **Step 5: Commit**

```bash
git add hooks/session-start scripts/check_framework.sh
git commit -m "feat(session-context): 支持 compact Quick 摘要"
```

### Task 4: Implement deterministic Quick classification and promotion rules

**Files:**
- Modify: `scripts/check_framework.sh:173-263`
- Modify: `agents/copilot-prompt.md:46-56,208-268,270-337,405-464,596-620`
- Modify: `agents/spec-reviewer.md:8-34`
- Modify: `agents/code-quality-reviewer.md:23-34`

- [ ] **Step 1: Add failing workflow-marker assertions**

Add to `scripts/check_framework.sh`:

```python
adaptive_quick_markers = {
    "agents/copilot-prompt.md": [
        "Quick Compact", "recordMode: compact", "不超过 2 个文件",
        "Runtime promotion", "promote to full Quick",
    ],
    "agents/spec-reviewer.md": ["recordMode", "compact Quick", "quick-card.md"],
    "agents/code-quality-reviewer.md": ["recordMode", "compact Quick"],
}
for rel, markers in adaptive_quick_markers.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit(f"{rel} missing adaptive Quick markers: {missing}")
```

- [ ] **Step 2: Run and verify RED**

Run `bash scripts/check_framework.sh`.

Expected: FAIL with `missing adaptive Quick markers`.

- [ ] **Step 3: Add the deterministic classifier to the prompt**

Under progressive complexity, keep Quick / Standard / Complex and add:

```markdown
Quick 内部记录模式：
- Compact：预计 ≤2 文件、单一目的、单 commit、不改 API/DB/依赖/CI/部署/generated artifact，
  不涉及资金/权限/认证/安全/敏感信息/状态机/跨模块业务规则，并有可执行验证与直接回滚。
- Full：任一 Compact 条件不满足或无法确认时使用。
```

Update Quick `/propose` output rules:

```markdown
- Compact：只生成 quick-card.md，recordMode: compact。
- Full：生成 quick-card.md + log.md + summary.md，recordMode: full。
```

- [ ] **Step 4: Add runtime promotion before further implementation**

In `/apply` and `/fix`, add a named `Runtime promotion` gate. It promotes compact to full when file count exceeds two, a second purpose/commit appears, excluded risk is discovered, confirmation scope materially changes, review requires an Important/Critical correction, or durable knowledge/open risk appears.

Specify the exact order:

```text
stop edits -> create log.md and summary.md -> copy existing evidence from quick-card.md
-> set recordMode: full -> recompute confirmation hash -> request confirmation if hash changed
-> resume only after the full record is valid
```

- [ ] **Step 5: Align review and archive paths**

Update reviewers so compact Quick reads execution, commit, review, and Loop Evidence from `quick-card.md`; full Quick and Standard/Complex continue reading `log.md`. Update `/archive` so a compact change with no knowledge can archive directly, while discovered durable knowledge triggers promotion before archive.

- [ ] **Step 6: Run checks and commit**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: PASS.

Commit:

```bash
git add scripts/check_framework.sh agents/copilot-prompt.md agents/spec-reviewer.md agents/code-quality-reviewer.md
git commit -m "feat(quick-workflow): 增加自适应记录与升级规则"
```

### Task 5: Move automatic work-Issue creation after confirmation

**GitHub API reference:** [REST API endpoints for sub-issues](https://docs.github.com/en/rest/issues/sub-issues). The add-sub-issue endpoint requires the work Issue's REST database `id`, not its Issue number, and requires Issues write permission.

**Files:**
- Modify: `scripts/check_framework.sh:104-263`
- Modify: `agents/copilot-prompt.md:154-268,270-337,405-545,653-666`
- Modify: `rules/commit-convention.md:27-47,77-141`
- Modify: `rules/github-metrics.md:8-47,105-122`

- [ ] **Step 1: Add failing Issue-lifecycle assertions**

Add exact marker checks:

```python
issue_lifecycle_markers = {
    "agents/copilot-prompt.md": [
        "parentIssue", "workIssue", "issueRelationship", "closeTarget",
        "确认后自动创建", "不得重复创建", "Closes #<workIssue>", "Refs #<parentIssue>",
    ],
    "rules/commit-convention.md": [
        "parentIssue", "workIssue", "Closes #<workIssue>", "Refs #<parentIssue>",
    ],
    "rules/github-metrics.md": ["parentIssue", "workIssue", "closeTarget"],
}
for rel, markers in issue_lifecycle_markers.items():
    text = (root / rel).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit(f"{rel} missing Issue lifecycle markers: {missing}")
```

- [ ] **Step 2: Run and verify RED**

Run `bash scripts/check_framework.sh`.

Expected: FAIL with `missing Issue lifecycle markers`.

- [ ] **Step 3: Add parent requirement resolution before contract drafting**

In `/brainstorm` and `/propose`, require one parent-Issue question unless the input already supplies it. When supplied, read title, body, acceptance checklist, relationship metadata, and decision-bearing comments; summarize overall goal, this change's boundary, completed sibling work, and contradictions.

State explicitly that unreadable or contradictory parent context blocks confirmation-time Issue creation instead of being guessed.

- [ ] **Step 4: Add the confirmation-time Issue state transition**

After writing confirmation metadata, specify:

```text
if workIssue is resolved: validate and reuse it
else: build body from confirmed contract -> gh issue create -> persist workIssue immediately
if parentIssue exists: establish native sub-issue relation -> set issueRelationship: sub-issue
else: set issueRelationship: standalone
derive type/scope -> create or validate branch -> allow /apply
```

If linking fails after creation, persist the created work Issue, mark `issueRelationship: pending`, retry linking, and block `/apply`; never create a replacement Issue.

Specify the concrete GitHub CLI/API sequence. `owner`, `repo`, `parent_number`, and `work_number` come from the validated repository and recorded contract:

```bash
work_issue_id="$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "repos/${owner}/${repo}/issues/${work_number}" \
  --jq '.id')"

gh api --method POST \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "repos/${owner}/${repo}/issues/${parent_number}/sub_issues" \
  -F "sub_issue_id=${work_issue_id}"
```

Verify the relation before setting `issueRelationship: sub-issue`:

```bash
gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2026-03-10" \
  "repos/${owner}/${repo}/issues/${parent_number}/sub_issues" \
  --jq '.[].number'
```

Expected: output contains `work_number`. HTTP `403`, `404`, `410`, or `422` keeps the created work Issue, records the response, and leaves the relationship pending.

- [ ] **Step 5: Remove finish-time Issue guessing**

Delete `issueWhenMissing=ask/auto/manual` behavior from `/finish`. Make a missing, pending, closed, cross-repository, or unreadable `workIssue` a blocking error.

Build PR linkage only from the recorded contract:

```markdown
Closes #<workIssue>
Refs #<parentIssue>  <!-- only when parentIssue is not none -->
```

Never use a closing keyword for `parentIssue`.

- [ ] **Step 6: Align policy and metrics**

Update `commit-convention.md` so “no ticketless development” means a confirmed and resolved `workIssue`; a parent Issue alone is insufficient. Update `github-metrics.md` to measure work-Issue closure separately from parent requirement progress.

- [ ] **Step 7: Run checks and commit**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: PASS.

Commit:

```bash
git add scripts/check_framework.sh agents/copilot-prompt.md rules/commit-convention.md rules/github-metrics.md
git commit -m "feat(issue-workflow): 确认后自动创建工作 Issue"
```

### Task 6: Complete review and finish evidence routing

**Files:**
- Modify: `scripts/check_framework.sh:173-263`
- Modify: `agents/spec-reviewer.md:8-64`
- Modify: `agents/code-quality-reviewer.md:8-64`
- Modify: `agents/copilot-prompt.md:405-545`
- Modify: `changes/templates/quick-card.md`
- Modify: `changes/templates/log.md:48-112,174-188`

- [ ] **Step 1: Add failing evidence-routing assertions**

Add checks requiring these exact behaviors:

```python
review_text = (root / "agents/spec-reviewer.md").read_text(encoding="utf-8")
for marker in ["compact Quick", "Execution record", "Commit record", "Review record"]:
    if marker not in review_text:
        raise SystemExit(f"spec reviewer missing compact evidence marker: {marker}")

prompt_text = (root / "agents/copilot-prompt.md").read_text(encoding="utf-8")
for marker in ["closeTarget: workIssue", "parentIssue 永不自动关闭", "workIssue: pending"]:
    if marker not in prompt_text:
        raise SystemExit(f"prompt missing finish safety marker: {marker}")
```

- [ ] **Step 2: Run and verify RED**

Run `bash scripts/check_framework.sh`.

Expected: FAIL on the first missing compact evidence marker.

- [ ] **Step 3: Route compact evidence to the Quick Card**

Update `/apply`, `/fix`, `/review`, and `/finish` so `recordMode: compact` appends command, exit code, output, Loop Evidence, commit, review, and PR data to the corresponding Quick Card sections. Full Quick and Standard/Complex keep using `log.md` and `summary.md`.

- [ ] **Step 4: Update both reviewers**

Spec Compliance must validate compact evidence from `quick-card.md`. Code Quality must verify the active branch and recorded commits against the Git contract, reporting malformed Git evidence as Important and unresolved Issue/close-target state as `NEEDS_INFO`.

- [ ] **Step 5: Verify and commit**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: PASS.

Commit:

```bash
git add scripts/check_framework.sh agents/spec-reviewer.md agents/code-quality-reviewer.md agents/copilot-prompt.md changes/templates/quick-card.md changes/templates/log.md
git commit -m "feat(review-workflow): 路由 compact Quick 收尾证据"
```

### Task 7: Synchronize all user-facing documentation

**Files:**
- Modify: `scripts/check_framework.sh:207-263`
- Modify: `README.md:15-36,126-265,350-365`
- Modify: `README-CN.md:13-34,124-263,353-368`
- Modify: `AGENTS.md:57-78`
- Modify: `docs/ai-code-copilot-overview.md:55-70`

- [ ] **Step 1: Add failing documentation parity assertions**

Add:

```python
doc_markers = [
    "Quick Compact", "Quick Full", "type/scope", "type(scope): description",
    "parentIssue", "workIssue", "Closes #<workIssue>", "Refs #<parentIssue>",
]
for rel in ["README.md", "README-CN.md", "AGENTS.md", "docs/ai-code-copilot-overview.md"]:
    text = (root / rel).read_text(encoding="utf-8")
    missing = [marker for marker in doc_markers if marker not in text]
    if missing:
        raise SystemExit(f"{rel} missing workflow documentation markers: {missing}")
```

- [ ] **Step 2: Run and verify RED**

Run `bash scripts/check_framework.sh`.

Expected: FAIL with `README.md missing workflow documentation markers`.

- [ ] **Step 3: Update English and Chinese README together**

Document:

- Compact eligibility and promotion to full Quick.
- Compact single-file output versus full Quick's three files.
- Parent requirement reading before contract drafting.
- Mandatory work-Issue creation after confirmation.
- `Closes #<workIssue>` and optional `Refs #<parentIssue>`.
- Mandatory branch and commit formats.
- `finishMode` controls PR handoff only.
- Existing `issueWhenMissing` config is obsolete and ignored.

Update directory trees so compact Quick does not falsely show mandatory `log.md`/`summary.md`.

- [ ] **Step 4: Update contributor and overview docs**

Apply the same contracts to `AGENTS.md` and `docs/ai-code-copilot-overview.md`. Preserve the rule that README changes must always be bilingual.

- [ ] **Step 5: Verify and commit**

Run:

```bash
bash scripts/check_framework.sh
git diff --check
```

Expected: PASS.

Commit:

```bash
git add scripts/check_framework.sh README.md README-CN.md AGENTS.md docs/ai-code-copilot-overview.md
git commit -m "docs(workflow-automation): 同步 Quick 与 Issue 新流程"
```

### Task 8: Run final behavioral verification

**Files:**
- Verify: all files changed in Tasks 1-7
- Update only if evidence reveals a defect: the smallest owning file plus `scripts/check_framework.sh`

- [ ] **Step 1: Run the full framework suite**

```bash
bash scripts/check_framework.sh
```

Expected: `ai-code-copilot framework check passed`.

- [ ] **Step 2: Run repository hygiene checks**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intended workflow files are modified.

- [ ] **Step 3: Audit forbidden stale behavior**

```bash
rg -n "issueWhenMissing|<type>\[optional scope\]|Closes #ID|Quick.*quick-card.*log.*summary" agents rules config changes README.md README-CN.md AGENTS.md docs scripts
```

Expected: no active rule treats `issueWhenMissing` as configurable, allows an optional commit scope, closes an ambiguous Issue, or requires full records for every Quick. Migration documentation and negative assertions may still mention obsolete text explicitly.

- [ ] **Step 4: Audit required behavior**

```bash
rg -n "Quick Compact|recordMode: compact|parentIssue|workIssue|closeTarget|type/scope|type\(scope\): description|Closes #<workIssue>|Refs #<parentIssue>" agents rules changes config README.md README-CN.md AGENTS.md docs scripts
```

Expected: every contract appears in its owning prompt, rule, template, test, and documentation surfaces.

- [ ] **Step 5: Verify commit history and branch**

```bash
git branch --show-current
git log --oneline --decorate origin/main..HEAD
```

Expected: branch is `docs/workflow-automation` for the planning branch until implementation begins; implementation must move to or rename to a valid primary change branch such as `feat/workflow-automation` before code edits. Every new commit matches `type(scope): description`.

- [ ] **Step 6: Record final evidence**

Append the exact framework-check output, diff-check exit code, commit list, and any accepted risk to the active change record. Do not claim completion without this evidence.
