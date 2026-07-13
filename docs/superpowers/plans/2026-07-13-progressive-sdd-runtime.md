# Progressive SDD Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert ai-code-copilot from a monolithic always-persisted workflow into a modular progressive SDD runtime with Inline, Compact, and Full contracts plus monotonic risk-based promotion.

**Architecture:** `skill/SKILL.md` loads a small `agents/router.md`, which reads the canonical `config/workflow-policy.json` and selects focused files under `agents/workflows/`. Existing compact/full Markdown records remain compatible, while Inline work stays in the conversation until lifecycle or risk triggers promotion. A dedicated Python self-check validates deterministic policy and module contracts, and the existing shell self-check remains the single top-level verification entrypoint.

**Tech Stack:** Markdown skills/prompts, Bash hooks/install/sync scripts, Python 3 standard library, JSON policy, Git/GitHub CLI.

**Design:** `docs/superpowers/specs/2026-07-13-progressive-sdd-runtime-design.md`

**Work Issue:** `#32` (`https://github.com/ting2tao/ai-code-copilot/issues/32`)

**Branch:** `feat/progressive-sdd`

---

## File map

### New files

- `config/workflow-policy.json` — canonical deterministic thresholds, risk categories, promotion triggers, Git types, and Issue policy values.
- `scripts/check_progressive_sdd.py` — focused policy/router/module fixtures invoked by the main framework self-check.
- `agents/router.md` — small intent/tier router and module-loading contract.
- `agents/workflows/init.md` — project initialization and sync behavior.
- `agents/workflows/inline.md` — Inline SDD eligibility, execution, evidence, and promotion.
- `agents/workflows/compact.md` — persisted compact Quick lifecycle and Inline-to-Compact evidence transfer.
- `agents/workflows/full.md` — brainstorm/propose/apply behavior for Full SDD.
- `agents/workflows/debug.md` — `/fix`, `/fix-ci`, root-cause, and escalation behavior.
- `agents/workflows/review.md` — persisted review routing and Inline promotion before auditable review.
- `agents/workflows/test.md` — selective TDD and Red/Green behavior.
- `agents/workflows/finish.md` — commit/publish gates, Issue policy, push, and PR behavior.
- `agents/workflows/archive.md` — durable knowledge extraction for persisted changes.

### Modified runtime and policy files

- `skill/SKILL.md` — load router first; use the legacy prompt only when modular files are absent.
- `agents/copilot-prompt.md` — declare legacy compatibility status and point to the router without deleting its safe fallback content.
- `hooks/session-start` — advertise router path, Inline/Compact/Full hard gates, and bounded promotion metadata.
- `config/project-config.json` — default new projects to `githubWorkflow.issuePolicy=on-publish`.
- `scripts/init_project.sh` — preserve existing project config and explain legacy missing-policy behavior.
- `scripts/check_framework.sh` — invoke the focused self-check and extend fixture assertions.
- `agents/spec-reviewer.md` — understand Inline provenance and monotonic promotion evidence.
- `agents/code-quality-reviewer.md` — require persisted promotion before auditable review and respect Issue lifecycle policy.
- `changes/templates/quick-card.md` — record `promotedFrom` and promotion evidence.
- `changes/templates/summary.md` — record optional full-tier promotion provenance.

### Modified documentation

- `README.md` and `README-CN.md` — synchronized user-facing progressive SDD and token-loading behavior.
- `AGENTS.md` — new architecture index and rules.
- `docs/ai-code-copilot-overview.md` — tier and Issue policy overview.
- `docs/ai-code-copilot-flow.md` — Inline/Compact/Full routing and promotion flow.
- `docs/harness-engineering.md` — derive Harness fields from the Spec tier.
- `docs/loop-engineering.md` — make Goal Contract the leading Spec section rather than a separate artifact.

---

### Task 1: Add the canonical workflow policy and focused self-check

**Files:**
- Create: `config/workflow-policy.json`
- Create: `scripts/check_progressive_sdd.py`
- Modify: `scripts/check_framework.sh`

- [x] **Step 1: Add a failing top-level check for the new policy checker**

Add the following near the initial `need_file` declarations in `scripts/check_framework.sh`:

```bash
need_file config/workflow-policy.json
need_file scripts/check_progressive_sdd.py
```

Add this after the existing shell syntax checks:

```bash
python3 scripts/check_progressive_sdd.py "$ROOT"
```

- [x] **Step 2: Run the framework check and verify Red**

Run:

```bash
bash scripts/check_framework.sh
```

Expected: non-zero exit with `missing file: config/workflow-policy.json`.

- [x] **Step 3: Create the canonical policy**

Create `config/workflow-policy.json` with this complete structure:

```json
{
  "version": 1,
  "tiers": {
    "inline": {
      "maxFiles": 2,
      "maxPurposes": 1,
      "maxCommits": 1,
      "requiresExecutableVerification": true,
      "requiresDirectRollback": true
    },
    "compact": {
      "maxFiles": 5
    },
    "full": {
      "riskCategories": [
        "public-api",
        "schema",
        "database",
        "dependency",
        "ci",
        "deployment",
        "generated-artifact",
        "security",
        "permission",
        "authentication",
        "sensitive-data",
        "money",
        "state-machine",
        "cross-module-business-rule",
        "accepted-residual-risk"
      ]
    }
  },
  "promotion": {
    "inlineToCompact": [
      "file-count-exceeded",
      "second-purpose",
      "second-commit",
      "verification-missing",
      "bounded-debugging-exceeded",
      "contract-ambiguous",
      "session-handoff",
      "commit-requested",
      "publish-requested",
      "auditable-review-requested",
      "persistence-requested"
    ],
    "toFull": [
      "full-risk-discovered",
      "material-reverse-sync",
      "important-review-correction",
      "critical-review-correction",
      "durable-knowledge",
      "open-risk",
      "multiple-review-units"
    ]
  },
  "git": {
    "allowedTypes": [
      "feat",
      "fix",
      "docs",
      "refactor",
      "test",
      "chore",
      "perf",
      "ci",
      "build"
    ]
  },
  "github": {
    "issuePolicies": ["always", "on-commit", "on-publish", "manual"],
    "newProjectDefault": "on-publish",
    "legacyDefault": "always",
    "closeTarget": "workIssue"
  }
}
```

- [x] **Step 4: Create the policy checker**

Create `scripts/check_progressive_sdd.py` as a Python 3 standard-library script. It must:

```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    raise SystemExit(f"progressive-sdd: {message}")


def read_text(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def classify(policy: dict, facts: dict) -> str:
    risks = set(facts.get("risks", []))
    full_risks = set(policy["tiers"]["full"]["riskCategories"])
    if risks & full_risks or facts.get("acceptedResidualRisk", False):
        return "full"
    inline = policy["tiers"]["inline"]
    if (
        facts.get("files", 0) > inline["maxFiles"]
        or facts.get("purposes", 1) > inline["maxPurposes"]
        or facts.get("commits", 1) > inline["maxCommits"]
        or not facts.get("executableVerification", False)
        or not facts.get("directRollback", False)
        or facts.get("persistedLifecycle", False)
    ):
        return "compact"
    return "inline"


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    policy = json.loads(read_text(root / "config/workflow-policy.json"))
    if policy.get("version") != 1:
        fail("workflow policy version must be 1")
    if policy["github"]["newProjectDefault"] != "on-publish":
        fail("new projects must default issuePolicy to on-publish")
    if policy["github"]["legacyDefault"] != "always":
        fail("legacy projects without issuePolicy must default to always")
    fixtures = [
        ({"files": 2, "executableVerification": True, "directRollback": True}, "inline"),
        ({"files": 3, "executableVerification": True, "directRollback": True}, "compact"),
        ({"files": 1, "executableVerification": True, "directRollback": True, "risks": ["public-api"]}, "full"),
    ]
    for facts, expected in fixtures:
        actual = classify(policy, facts)
        if actual != expected:
            fail(f"classifier expected {expected}, got {actual}: {facts}")
    print("progressive-sdd: policy checks passed")


if __name__ == "__main__":
    main()
```

- [x] **Step 5: Run the focused checker and top-level framework check**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash scripts/check_framework.sh
```

Expected: focused checker prints `progressive-sdd: policy checks passed`; the full check reaches the existing suite without a new policy error.

- [x] **Step 6: Commit Task 1**

```bash
git add config/workflow-policy.json scripts/check_progressive_sdd.py scripts/check_framework.sh
git commit -m "test(progressive-sdd): 固化分层与升级策略"
```

---

### Task 2: Add the modular router, workflow modules, and lightweight skill entry

**Files:**
- Create: `agents/router.md`
- Create: `agents/workflows/init.md`
- Create: `agents/workflows/inline.md`
- Create: `agents/workflows/compact.md`
- Create: `agents/workflows/full.md`
- Create: `agents/workflows/debug.md`
- Create: `agents/workflows/review.md`
- Create: `agents/workflows/test.md`
- Create: `agents/workflows/finish.md`
- Create: `agents/workflows/archive.md`
- Modify: `skill/SKILL.md`
- Modify: `agents/copilot-prompt.md`
- Modify: `hooks/session-start`
- Modify: `scripts/check_progressive_sdd.py`

- [x] **Step 1: Extend the checker so the missing router fails**

Add to `main()` in `scripts/check_progressive_sdd.py`:

```python
    required_modules = [
        "init.md",
        "inline.md",
        "compact.md",
        "full.md",
        "debug.md",
        "review.md",
        "test.md",
        "finish.md",
        "archive.md",
    ]
    router = read_text(root / "agents/router.md")
    for name in required_modules:
        read_text(root / "agents/workflows" / name)
        if f"agents/workflows/{name}" not in router:
            fail(f"router missing module reference: {name}")
    skill = read_text(root / "skill/SKILL.md")
    if "agents/router.md" not in skill:
        fail("skill must load agents/router.md")
    required_skill_fallback = "agents/copilot-prompt.md"
    if required_skill_fallback not in skill:
        fail("skill must retain the legacy prompt fallback")
```

- [x] **Step 2: Run the focused checker and verify Red**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
```

Expected: non-zero exit with `missing file: .../agents/router.md`.

- [x] **Step 3: Create `agents/router.md`**

The complete router must define:

```markdown
# ai-code-copilot Router

Load `config/workflow-policy.json` first. Load only the selected workflow modules; do not load every module or the legacy prompt by default.

## Always-on rules

- Preserve unrelated and uncommitted user changes.
- Never expose secrets or sensitive information.
- Require explicit authority for destructive or external operations.
- Require fresh verification evidence before completion claims.
- High-risk money, permission, state-transition, security, or production changes require Full SDD and human confirmation.

## Intent routing

| Intent | Module |
|---|---|
| init/sync/upgrade | `agents/workflows/init.md` |
| clear low-risk local edit | `agents/workflows/inline.md` |
| persisted small change | `agents/workflows/compact.md` |
| brainstorm/propose/apply complex change | `agents/workflows/full.md` |
| fix/fix-ci/root-cause | `agents/workflows/debug.md` plus the current tier module |
| review | `agents/workflows/review.md` |
| test/TDD | `agents/workflows/test.md` |
| finish/commit/publish/PR | `agents/workflows/finish.md` plus the current tier module |
| archive | `agents/workflows/archive.md` |

## Tier routing

Use Inline only when every Inline policy condition is known true. If uncertain, use Compact. Any full-risk category routes directly to Full. Promotion is monotonic: Inline -> Compact -> Full or Inline -> Full. Never automatically downgrade an active change.

## Context loading

Read project rules and code relevant to the current task. Read only the active change record for persisted tiers. Read `knowledge/index.md` before selecting at most five relevant knowledge files. SessionStart metadata is a hint, not the source of truth.

## Compatibility

If a required modular file is absent, load `agents/copilot-prompt.md`, report that the installation is using the stricter legacy fallback, and recommend `init --sync` or framework upgrade. Do not silently weaken a missing policy or gate.
```

- [x] **Step 4: Create focused workflow modules**

Write each module as an independently readable contract. Required sections and exact behavioral markers:

```text
init.md: init_project.sh, --sync, --upgrade --dry-run, project-owned preservation
inline.md: Goal, Scope, Done Signal, Verify, no persisted artifact, Inline -> Compact, Inline -> Full
compact.md: quick-card.md, recordMode: compact, promotedFrom: inline, Runtime promotion, evidence transfer
full.md: design-brief.md, spec.md, tasks.md, test-spec.md, log.md, summary.md, Reverse Sync
debug.md: root cause before fix, one hypothesis, Red/Green for bug fixes, three-failure architecture stop, fix-ci evidence
review.md: Inline auditable review triggers Compact promotion, Spec Compliance, Code Quality, promotion audit
test.md: risk-proportional TDD, explicit Red/Green when selected, no fake coverage claims
finish.md: issuePolicy, commit/publish gates, Closes #<workIssue>, Refs #<parentIssue>, finishMode
archive.md: persisted tiers only, knowledge/index.md selection, no forced durable knowledge for Inline
```

Copy command-specific safety and evidence semantics from the corresponding legacy prompt sections, but remove unrelated commands from each module.

- [x] **Step 5: Change `skill/SKILL.md` to load the router**

Replace the current complete-prompt requirement with:

```markdown
> **REQUIRED:** Locate the ai-code-copilot framework root, then read `<root>/agents/router.md`.
> Read only the workflow modules selected by the router.
> If `agents/router.md` or a selected module is missing, fall back to `<root>/agents/copilot-prompt.md`, report the stricter legacy fallback, and recommend a framework upgrade.
```

Update the hard gate so Inline needs a visible Inline contract, Compact needs a valid Quick Card, and Full needs a confirmed Spec. Full-risk work can never remain Inline or Compact.

- [x] **Step 6: Mark `agents/copilot-prompt.md` as the legacy compatibility fallback**

Prepend:

```markdown
> Compatibility fallback: new runtime activation starts at `agents/router.md` and loads focused files under `agents/workflows/`. This file preserves the stricter monolithic behavior for older or partially upgraded installations. New behavior must be implemented in the router/modules first and mirrored here only where fallback safety requires it.
```

Do not delete the legacy body in this phase.

- [x] **Step 7: Update SessionStart L0 routing text**

In `hooks/session-start`, replace the complete-prompt pointer and old Quick-only hard gate with router/module pointers and Inline/Compact/Full gates. Keep the active-change parser bounded and do not inject module bodies.

- [x] **Step 8: Run focused and full checks**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash -n hooks/session-start
bash scripts/check_framework.sh
```

Expected: all exit 0; the focused checker validates every module reference.

- [ ] **Step 9: Commit Task 2**

```bash
git add agents skill/SKILL.md hooks/session-start scripts/check_progressive_sdd.py
git commit -m "feat(progressive-sdd): 增加模块化运行时路由"
```

---

### Task 3: Implement promotion provenance and review contracts

**Files:**
- Modify: `changes/templates/quick-card.md`
- Modify: `changes/templates/summary.md`
- Modify: `agents/workflows/compact.md`
- Modify: `agents/workflows/full.md`
- Modify: `agents/workflows/review.md`
- Modify: `agents/spec-reviewer.md`
- Modify: `agents/code-quality-reviewer.md`
- Modify: `hooks/session-start`
- Modify: `scripts/check_progressive_sdd.py`
- Modify: `scripts/check_framework.sh`

- [ ] **Step 1: Add failing promotion contract assertions**

Extend `scripts/check_progressive_sdd.py`:

```python
    quick_card = read_text(root / "changes/templates/quick-card.md")
    for marker in ["promotedFrom:", "Promotion record", "previous contract", "evidence copied", "material confirmation"]:
        if marker not in quick_card:
            fail(f"quick-card missing promotion marker: {marker}")
    spec_reviewer = read_text(root / "agents/spec-reviewer.md")
    for marker in ["Inline -> Compact", "Inline -> Full", "mechanical Reverse Sync", "material Reverse Sync"]:
        if marker not in spec_reviewer:
            fail(f"spec reviewer missing progressive SDD marker: {marker}")
```

- [ ] **Step 2: Run Red**

Run `python3 scripts/check_progressive_sdd.py .`.

Expected: non-zero exit naming the first missing promotion marker.

- [ ] **Step 3: Extend the Quick Card metadata and record**

Add to the front matter:

```yaml
promotedFrom: none # none | inline
```

Add:

```markdown
## Promotion record

| promoted at | from | trigger | previous contract | evidence copied | material confirmation |
|---|---|---|---|---|---|
```

Update `summary.md` with optional `promoted-from: none | inline | compact` documentation while retaining all existing required fields.

- [ ] **Step 4: Update promotion and review modules**

Require exact ordering:

```text
stop edits -> capture contract/diff/evidence -> create target record -> copy evidence -> update tier/recordMode -> recompute hash -> request confirmation only for material change -> resume
```

Define mechanical Reverse Sync as path/symbol/command/implementation-detail correction without behavior or risk change. Define material Reverse Sync as Goal/Scope/Acceptance/Guardrails/risk/external-action change.

- [ ] **Step 5: Update both reviewers**

The Spec reviewer must verify both promotion paths, provenance, evidence preservation, and material-confirmation decisions. The Code Quality reviewer must require Inline work to promote before an auditable persisted review and must not require nonexistent log files before promotion completes.

- [ ] **Step 6: Update bounded SessionStart metadata**

Allow `promotedFrom` in validated Quick front matter and include it only in the existing bounded metadata list. Do not include Promotion record bodies.

- [ ] **Step 7: Run checks and commit**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash scripts/check_framework.sh
```

Expected: exit 0.

Commit:

```bash
git add agents hooks/session-start changes/templates scripts
git commit -m "feat(progressive-sdd): 记录单向升级与审查证据"
```

---

### Task 4: Add lifecycle-aware Issue policy without weakening legacy projects

**Files:**
- Modify: `config/project-config.json`
- Modify: `agents/workflows/inline.md`
- Modify: `agents/workflows/compact.md`
- Modify: `agents/workflows/full.md`
- Modify: `agents/workflows/finish.md`
- Modify: `rules/commit-convention.md`
- Modify: `rules/github-metrics.md`
- Modify: `scripts/init_project.sh`
- Modify: `scripts/check_progressive_sdd.py`
- Modify: `scripts/check_framework.sh`

- [ ] **Step 1: Add failing policy-lifecycle assertions**

Add to `scripts/check_progressive_sdd.py`:

```python
    project_config = json.loads(read_text(root / "config/project-config.json"))
    if project_config.get("githubWorkflow", {}).get("issuePolicy") != "on-publish":
        fail("new project config must default issuePolicy to on-publish")
    finish = read_text(root / "agents/workflows/finish.md")
    for marker in ["always", "on-commit", "on-publish", "manual", "legacy default: always", "Closes #<workIssue>", "Refs #<parentIssue>"]:
        if marker not in finish:
            fail(f"finish module missing issue policy marker: {marker}")
```

- [ ] **Step 2: Run Red**

Run `python3 scripts/check_progressive_sdd.py .`.

Expected: non-zero exit stating that project config lacks `issuePolicy=on-publish`.

- [ ] **Step 3: Add the new-project default**

Update `config/project-config.json`:

```json
"githubWorkflow": {
  "issuePolicy": "on-publish",
  "finishMode": "ask",
  "createPrAfterReviewPass": false,
  "defaultBaseBranch": "main",
  "pushRemote": "origin",
  "prDraft": false
}
```

- [ ] **Step 4: Implement lifecycle gates in workflow modules and rules**

Use this exact table:

```text
always     -> resolve workIssue before implementation
on-commit  -> local edits allowed; resolve workIssue before first commit
on-publish -> local edits and commits allowed; resolve workIssue before push/PR
manual     -> never auto-create; validate supplied Issue when present
missing    -> legacy default always
```

Whenever an Issue exists, keep `closeTarget=workIssue`, reuse an existing open Issue, never create a replacement after partial success, and never close the parent Issue.

- [ ] **Step 5: Preserve old project configuration**

Keep `scripts/init_project.sh` byte-preserving behavior for existing `.ai_code_copilot/config.json`. Add a migration note for a missing `issuePolicy` explaining that runtime uses legacy `always`; do not rewrite or generate `.new` for the project-owned config.

- [ ] **Step 6: Extend fixture checks**

In `scripts/check_framework.sh`:

- Assert new fixture config contains `"issuePolicy": "on-publish"`.
- Preserve an existing custom config without `issuePolicy` byte-for-byte.
- Assert sync output contains the legacy-default migration note.
- Keep obsolete `issueWhenMissing` preservation and warning coverage.

- [ ] **Step 7: Run checks and commit**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash scripts/check_framework.sh
```

Expected: all policy modes and fixture migrations pass.

Commit:

```bash
git add config agents/workflows rules scripts
git commit -m "feat(issue-policy): 按交付阶段解析工作 Issue"
```

---

### Task 5: Synchronize English/Chinese docs and framework indexes

**Files:**
- Modify: `README.md`
- Modify: `README-CN.md`
- Modify: `AGENTS.md`
- Modify: `docs/ai-code-copilot-overview.md`
- Modify: `docs/ai-code-copilot-flow.md`
- Modify: `docs/harness-engineering.md`
- Modify: `docs/loop-engineering.md`
- Modify: `scripts/check_progressive_sdd.py`
- Modify: `scripts/check_framework.sh`

- [ ] **Step 1: Add failing documentation markers**

Extend the focused checker with synchronized markers:

```python
    docs = {
        "README.md": ["Inline SDD", "Compact SDD", "Full SDD", "issuePolicy", "agents/router.md"],
        "README-CN.md": ["Inline SDD", "Compact SDD", "Full SDD", "issuePolicy", "agents/router.md"],
        "AGENTS.md": ["agents/router.md", "agents/workflows/", "Inline SDD", "单向升级"],
        "docs/ai-code-copilot-overview.md": ["Inline SDD", "Compact SDD", "Full SDD"],
    }
    for relative, markers in docs.items():
        text = read_text(root / relative)
        for marker in markers:
            if marker not in text:
                fail(f"{relative} missing documentation marker: {marker}")
```

- [ ] **Step 2: Run Red**

Run `python3 scripts/check_progressive_sdd.py .`.

Expected: non-zero exit naming the first missing README marker.

- [ ] **Step 3: Update the public documentation**

Document the same behavior in both READMEs:

- Skills use a small router and load modules on demand.
- Inline/Compact/Full are Spec persistence tiers, not three different quality standards.
- Promotion is monotonic.
- Existing compact/full records remain compatible.
- New projects default `issuePolicy` to `on-publish`; missing legacy config means `always`.
- Superpowers is a specialist library, not the default orchestrator.

- [ ] **Step 4: Update architecture and methodology docs**

Update `AGENTS.md` to name the router/modules/policy as key files. Update the flow chart with Inline -> Compact -> Full. Update Harness and Loop docs so Goal Contract is embedded in the Spec tier and Harness derives validation signals from Acceptance/Done Signal/Guardrails/Fallback.

- [ ] **Step 5: Run checks and commit**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash scripts/check_framework.sh
git diff --check
```

Expected: exit 0.

Commit:

```bash
git add README.md README-CN.md AGENTS.md docs scripts
git commit -m "docs(progressive-sdd): 同步分层运行时说明"
```

---

### Task 6: Final compatibility, installation, and acceptance verification

**Files:**
- Modify only files required by failures found in this task.
- Update: `docs/superpowers/specs/2026-07-13-progressive-sdd-runtime-design.md` with final implementation evidence.
- Update: `docs/superpowers/plans/2026-07-13-progressive-sdd-runtime.md` checkboxes and commit evidence.

- [ ] **Step 1: Verify shell syntax**

Run:

```bash
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh install.sh install-wsl.sh
```

Expected: exit 0 with no output.

- [ ] **Step 2: Run focused and complete framework checks**

Run:

```bash
python3 scripts/check_progressive_sdd.py .
bash scripts/check_framework.sh
```

Expected: focused checker prints success and the complete suite exits 0.

- [ ] **Step 3: Verify formatting and changed-file scope**

Run:

```bash
git diff --check origin/main...HEAD
git status --short
git diff --stat origin/main...HEAD
```

Expected: no whitespace errors; only planned framework, policy, template, test, and documentation files appear.

- [ ] **Step 4: Verify installation and sync dry-runs**

Run against a disposable project fixture:

```bash
tmpdir="$(mktemp -d /tmp/progressive-sdd-verify.XXXXXX)"
cp -R tests/fixtures/python/. "$tmpdir/"
AI_CODE_COPILOT_HOME="$PWD" bash scripts/init_project.sh --project "$tmpdir" --upgrade --dry-run
AI_CODE_COPILOT_HOME="$PWD" bash scripts/init_project.sh --project "$tmpdir"
grep -q '"issuePolicy": "on-publish"' "$tmpdir/.ai_code_copilot/config.json"
```

Expected: dry-run performs no writes; initialization succeeds and new config contains the new-project default.

- [ ] **Step 5: Review against every acceptance criterion**

Read the design §16 and map each criterion to a changed file plus fresh command evidence. Record any remaining Phase 3 measurement work as follow-up, not as a failed Phase 1/2 criterion.

- [ ] **Step 6: Commit final evidence corrections**

```bash
git add docs/superpowers/specs/2026-07-13-progressive-sdd-runtime-design.md docs/superpowers/plans/2026-07-13-progressive-sdd-runtime.md
git commit -m "docs(progressive-sdd): 记录升级验证证据"
```

- [ ] **Step 7: Run the complete verification again after the final commit**

Run:

```bash
bash scripts/check_framework.sh
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh install.sh install-wsl.sh
git diff --check origin/main...HEAD
git status --short --branch
```

Expected: all commands exit 0 and the working tree is clean.

---

## Execution choice

This task will be executed inline in the current session because the user requested implementation and did not request subagents. Use `superpowers:executing-plans` with checkpoints after Tasks 2, 4, and 6. Do not dispatch subagents unless the user explicitly asks for delegation.
