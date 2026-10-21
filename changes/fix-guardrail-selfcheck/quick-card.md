---
artifactVersion: 1
artifactId: "fix-guardrail-selfcheck:quick-card"
artifactType: quick-card
artifactStatus: confirmed
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: none
upstreamHash: none
change: "fix-guardrail-selfcheck"
status: in-progress
recordMode: compact
promotedFrom: none
specHash: "pending"
parentIssue: none
workIssue: none
issueRelationship: none
closeTarget: none
branch: "fix/guardrail-selfcheck"
---

# Quick 变更卡：fix-guardrail-selfcheck

> **状态**：[ ] 草稿 / [x] 已确认 / [x] 实施中 / [ ] 已完成
> **创建时间**：2026-10-21
> **父 Issue（parentIssue）**：none
> **工作 Issue（workIssue）**：none（manual）
> **Issue 关系（issueRelationship）**：none
> **关闭目标（closeTarget）**：none
> **分支（branch）**：fix/guardrail-selfcheck（基于 feat/ai-native-sdlc）
> **确认时间**：2026-10-21
> **确认人**：用户（会话中确认"可以"）
> **确认范围 Hash**：pending（完成时回填）

---

## 1. 目标

修复 `check_framework.sh` 在安装目录（无 `.git` 的托管树）运行时 `test_guardrails.py` 中 2 个 hook 测试必现失败的问题：这两个测试假设测试运行目录是 git 仓库，而新版 `install.sh` 的 staged 安装会删除 `.git`，导致 `hook_event` 的 `git rev-parse` 失败进入 degraded 拦截。

## 2. 涉及文件

- 修改：`tests/test_guardrails.py` — 两个失败测试改为在隔离的临时 git 仓库中执行（沿用文件内既有 temp-repo 写法）
- 修改：`VERSION` — 0.2.0 → 0.2.1（bug fix，patch bump）
- 修改：`README.md` / `README-CN.md` — 同步版本号引用
- 新建：`changes/fix-guardrail-selfcheck/quick-card.md`、`log.md`

## 3. 非目标（Out of Scope）

- 不修改 `scripts/check_guardrails.py` 的 hook 逻辑（degraded fail-closed 是正确行为）
- 不修改 `install.sh`（删除 `.git` 是 staged 安装的设计决策）
- 不处理 CI/发布流程

## 4. 验收方式

- [ ] `bash scripts/check_framework.sh`（源码仓库）通过
- [ ] 模拟安装环境（无 `.git` 的目录树）中运行 `tests/test_guardrails.py` 全部通过
- [ ] 重新执行 `install.sh` 后，在 `~/.claude/ai_code_copilot/` 中运行 `check_framework.sh` 通过

## 5. Agent Harness

| 项 | 内容 |
|----|------|
| Agent 可见证据 | unittest 输出、check_framework.sh 输出（含 exit code） |
| 必跑验证命令 | `bash scripts/check_framework.sh`；模拟安装目录中的 `python3 -m unittest` |
| 失败自诊断入口 | `tests/test_guardrails.py` 两个失败用例的 stderr（degraded 消息） |
| 不可见信息/人工确认 | 无 |

## 6. Goal Contract

| 项 | 内容 |
|----|------|
| Goal | 安装目录（非 git 仓库）中框架自检全部通过 |
| Done Signal | 三处验证命令 exit 0：源码仓库自检、模拟安装环境测试、安装后自检 |
| Guardrails | 不得通过跳过/删除测试来"修复"；不得改动 hook 的 fail-closed 语义 |
| Fallback | 若临时仓库方案有环境限制（如沙箱禁 git init），停下向用户确认 |
| Memory | 无 |

## 7. Domain Check（DDD-lite，可选）

不适用

## 8. 风险与回滚

- 风险：无明显风险（纯测试环境构造修正 + 版本号）
- 人工确认项：无
- 回滚方案：revert 提交即可，无数据/配置影响

## Execution record

| command | exit code | output summary | Loop Evidence |
|---|---:|---|---|
| bash scripts/check_framework.sh（修复前，安装目录） | 1 | 2 failures: test_hook_blocks_secrets…, test_hook_safe_pii_and_outside_root | log.md 基线 |

## Promotion record

| promoted at | from | trigger | previous contract | evidence copied | material confirmation |
|---|---|---|---|---|---|

## Commit record

| hash | message |
|---|---|

## Review record

| Spec Compliance | Code Quality | GitHub Readiness | open risks |
|---|---|---|---|

## Finish record

| PR URL | base | remote | Closes workIssue | Refs parentIssue | final validation |
|---|---|---|---|---|---|
