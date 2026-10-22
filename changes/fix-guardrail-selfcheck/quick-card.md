---
artifactVersion: 1
artifactId: "fix-guardrail-selfcheck:quick-card"
artifactType: quick-card
artifactStatus: finished
sourceOfTruth: repository
sourceRef: self
sourceRevision: git:6728f5cb1a1277c039b2c9a90a5d341086e1b87f
upstream: none
upstreamHash: none
change: "fix-guardrail-selfcheck"
status: finished
recordMode: full
promotedFrom: none
specHash: "sha256:546e1f074934364af722333c8d94517a5b69cbfb18c0ecdfdf2a6ba5b02e74d3"
parentIssue: none
workIssue: none
issueRelationship: none
closeTarget: none
branch: "feat/ai-native-sdlc"
---

# Quick 变更卡：fix-guardrail-selfcheck

> **状态**：[ ] 草稿 / [x] 已确认 / [x] 实施中 / [x] 已完成
> **创建时间**：2026-10-21
> **父 Issue（parentIssue）**：none
> **工作 Issue（workIssue）**：none（manual）
> **Issue 关系（issueRelationship）**：none
> **关闭目标（closeTarget）**：none
> **分支（branch）**：feat/ai-native-sdlc（PR #38）；隔离修复工作区为 fix/pr38-conflicts
> **确认时间**：2026-10-21
> **确认人**：用户（会话中确认"可以"）
> **确认范围 Hash**：sha256:546e1f074934364af722333c8d94517a5b69cbfb18c0ecdfdf2a6ba5b02e74d3

---

## 1. 目标

修复 `check_framework.sh` 在安装目录（无 `.git` 的托管树）运行时 `test_guardrails.py` 中 2 个 hook 测试必现失败的问题：这两个测试假设测试运行目录是 git 仓库，而新版 `install.sh` 的 staged 安装会删除 `.git`，导致 `hook_event` 的 `git rev-parse` 失败进入 degraded 拦截。

## 2. 涉及文件

- 修改：`tests/test_guardrails.py` — 两个失败测试改为在隔离的临时 git 仓库中执行（沿用文件内既有 temp-repo 写法）
- 修改：`VERSION` — 原始 0.2.0 → 0.2.1；合入最新 main 后为 0.2.2 → 0.2.3（patch bump，不降级）
- 同步：`README.md` / `README-CN.md` — 保留最新 main 的 VERSION 单一来源说明，不重新写入版本常量
- 新建：`changes/fix-guardrail-selfcheck/quick-card.md`、`log.md`、`summary.md`

## 3. 非目标（Out of Scope）

- 不修改 `scripts/check_guardrails.py` 的 hook 逻辑（degraded fail-closed 是正确行为）
- 不修改 `install.sh`（删除 `.git` 是 staged 安装的设计决策）
- 不处理 CI/发布流程

## 4. 验收方式

- [x] `bash scripts/check_framework.sh`（源码仓库）通过
- [x] 实际临时安装环境（无 `.git`）中 `tests/test_guardrails.py` 全部通过
- [x] 临时 HOME 下执行 `install.sh --claude` 后，在实际无 `.git` 安装目录运行 `check_framework.sh` 通过（不改个人安装）

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
| bash scripts/check_framework.sh（修复后，源码仓库） | 0 | ai-code-copilot framework check passed | log.md |
| python3 -m unittest tests.test_guardrails（安装目录） | 0 | Ran 30 tests — OK | log.md |
| bash install.sh --claude（重新部署 0.2.1） | 0 | 直接覆盖更新 0.2.0 → 0.2.1，自检正常 | log.md |
| bash scripts/check_framework.sh（修复后，安装目录） | 0 | ai-code-copilot framework check passed | log.md |

## Promotion record

| promoted at | from | trigger | previous contract | evidence copied | material confirmation |
|---|---|---|---|---|---|

## Commit record

| hash | message |
|---|---|
| bf2bcad | fix(guardrails): run hook tests in isolated repos so installed self-check passes |

## Review record

| Spec Compliance | Code Quality | GitHub Readiness | open risks |
|---|---|---|---|
| PASS（详见 log.md Quick Review） | PASS（详见 log.md Quick Review） | PR #38 已存在；本轮重新验证 | 无 |

## Finish record

| PR URL | base | remote | Closes workIssue | Refs parentIssue | final validation |
|---|---|---|---|---|---|
| https://github.com/ting2tao/ai-code-copilot/pull/38 | main | origin | —（manual，无 Issue） | — | 原始 v0.2.1 验证；本轮 v0.2.3 验证见 log.md |

## 2026-10-22 冲突修复合同

用户请求：“PR #38，解决这些问题”。GitHub 审查评论/失败检查为空，实际问题是 mergeable=CONFLICTING；最新 main 已合入 PR #40（4bc4c72）。保留 main 的 README/能力声明/Codex 实现；保留本 PR 两处隔离 Git fixture 修复；VERSION 前进到 0.2.3。采用 merge 更新原 head，不改写已发布历史、不合并 PR 到 main。原工作区未提交的 Quick Card URL 改动保持原样，本工作区独立记录原 PR URL。

原记录已有 log.md，因此本轮将 recordMode 从 compact 单向提升为 full，补齐 summary.md 与有效产物 metadata；不新增业务功能或风险授权。分支名称同步为现有 PR head，旧分支描述仅为历史记录。

验收：无冲突标记/未解决 index entries；源码和真实临时安装目录（无 .git）完整自检通过；最终相对 main 的生产护栏/安装脚本无差异；原 PR 可合并。配置沿用原合同 manual/no-Issue，不新增工作票。

本轮验证：main 无 Git 副本 RED（2 failures）；源码和实际临时安装目录 GREEN（各 50 tests + 23 offline eval cases）；产物链 PASS 3；相对 main 的 runtime/README 字节一致；提交/发布 Guardrail PASS，无待审批项。审核方式为本地 self-review，未声称独立 Agent 审查。

Finish verified: PR #38 is OPEN / MERGEABLE / CLEAN, base main, ordinary fast-forward push; no main merge. Implementation merge commit: 6728f5c fix(guardrails): resolve PR conflicts and preserve installed self-check.
