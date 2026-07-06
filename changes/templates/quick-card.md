---
change: "{change-name}"
status: proposed
recordMode: compact # compact | full
specHash: "{sha256}"
parentIssue: none # none | "#123" | URL
workIssue: pending # pending | "#456" | URL
issueRelationship: pending # pending | sub-issue | standalone
closeTarget: workIssue
branch: "type/scope"
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

> compact 模式这些表是唯一证据源；full 模式证据写入 log.md 和 summary.md，Quick Card 只保留索引与摘要。
> 每次 `/apply` 或 `/fix` 都追加实际 command、exit code、output summary 与对应 Loop Evidence。

| command | exit code | output summary | Loop Evidence |
|---|---:|---|---|

## Commit record

> 每次提交后立即追加实际 hash 与完整的 `type(scope): description` message。

| hash | message |
|---|---|

## Review record

> `/review` 追加 Spec Compliance、Code Quality、GitHub Readiness 与未解决风险；compact 收尾要求前两项均为 PASS。

| Spec Compliance | Code Quality | GitHub Readiness | open risks |
|---|---|---|---|

## Finish record

> `/finish` 追加 PR、验证结果、分支/远端和 closing statement；只允许 `Closes #workIssue`，parentIssue 仅使用 `Refs`。

| PR URL | base | remote | Closes workIssue | Refs parentIssue | final validation |
|---|---|---|---|---|---|
