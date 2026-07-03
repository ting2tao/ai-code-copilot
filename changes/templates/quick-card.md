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

# Quick 变更卡：{变更名}

> **状态**：[ ] 草稿 / [ ] 已确认 / [ ] 实施中 / [ ] 已完成
> **创建时间**：{YYYY-MM-DD}
> **父 Issue（parentIssue）**：{none / #123 / URL；已有父需求时填写}
> **工作 Issue（workIssue）**：{pending / #456 / URL；Quick Card 确认后必须创建或绑定}
> **Issue 关系（issueRelationship）**：{pending / sub-issue / standalone}
> **关闭目标（closeTarget）**：workIssue（PR closing keyword 只关闭 workIssue）
> **分支（branch）**：{type/scope；例如 feat/issue-workflow}
> **确认时间**：{YYYY-MM-DD HH:mm 或"未确认"}
> **确认人**：{用户/姓名}
> **确认范围 Hash**：{quick-card.md 内容摘要}

---

## 1. 目标

{用 1-3 句话说明这次 Quick 变更要解决什么问题}

## 2. 涉及文件

- 新建：`{路径}` — {原因}
- 修改：`{路径}` — {预期改动}

## 3. 非目标（Out of Scope）

- {明确不做什么，防止 Quick 变成 Standard}

## 4. 验收方式

- [ ] {可验证条件，例如：指定测试/编译命令通过}
- [ ] {人工检查项，如适用}

## 5. Agent Harness

| 项 | 内容 |
|----|------|
| Agent 可见证据 | {测试/构建输出、日志、截图、CI 链接等} |
| 必跑验证命令 | `{命令}` |
| 失败自诊断入口 | {失败时先看哪些命令、日志或文件} |
| 不可见信息/人工确认 | {无则填"无"} |

## 6. Goal Contract

| 项 | 内容 |
|----|------|
| Goal | {这次 Quick 循环要达成的目标} |
| Done Signal | {判断完成的命令输出、日志、截图或人工确认} |
| Guardrails | {不能用什么方式假完成；无则填"无"} |
| Fallback | {失败时如何降级、停机或找人确认} |
| Memory | {有经验沉淀时写入哪里；无则填"无"} |

## 7. Domain Check（DDD-lite，可选）

> 普通 Quick 变更填"不适用"；涉及金额、权限、状态机、跨模块业务规则时，至少写清 Language、Boundary、Invariants、State Transitions、Owner。

{不适用 / Language: ...; Boundary: ...; Invariants: ...; State Transitions: ...; Owner: ...}

## 8. 风险与回滚

- 风险：{风险点；无则填"无明显风险"}
- 人工确认项：{涉及资金/状态/权限/敏感信息则必须列出；无则填"无"}
- 回滚方案：{代码/配置/数据回滚方式}

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
