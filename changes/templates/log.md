# 变更日志：{变更名}

> 本文件记录变更过程中的关键决策、踩坑、知识发现和验证证据，供 /review、/finish、/archive 使用。
> 压缩 log 只能移动过程性细节，不能删除审计证据。

---

## Summary

| 字段 | 内容 |
|------|------|
| 变更名 | {变更名} |
| 档位 | Quick / Standard / Complex |
| 状态 | proposed / in-apply / in-review / done |
| 开始时间 | {YYYY-MM-DD} |
| 完成时间 | {YYYY-MM-DD 或"未完成"} |
| parentIssue | {none / #123 / URL} |
| workIssue | {pending / #456 / URL；manual/no-Issue 时 none} |
| issueRelationship | {pending / sub-issue / standalone；manual/no-Issue 时 none} |
| closeTarget | {workIssue；manual/no-Issue 时 none} |
| branch | {type/scope} |
| 确认时间 | {YYYY-MM-DD HH:mm 或"未确认"} |
| 确认人 | {用户/姓名} |
| 确认范围 Hash | {确认时 spec/tasks/test-spec 或 quick-card 的内容摘要} |
| 涉及文件数 | {N} |
| commit 列表 | {列出所有 commit hash + message} |
| Last compressed | — |
| Archived entries | 0 |
| Archive hash | — |

> Standard/full Quick 使用本文件和 summary.md 记录执行、审查与收尾；compact Quick 由 quick-card.md 的 Execution/Commit/Review/Finish record 承载这些记录。

---

## Active decisions

> 关键架构/设计/范围决策。压缩时必须保留。

### {YYYY-MM-DD} - {决策标题}

**内容**：{发生了什么}
**决策**：{做了什么选择，为什么}
**影响**：{对后续的影响}

---

## Known risks

> 已知风险、缓解措施、人工接受项。压缩时必须保留。

- [ ] {风险描述}；缓解：{措施}；接受人/日期：{如适用}

---

## Review outcomes

### Spec Compliance（spec-reviewer）

**结论**：PASS / FAIL
**问题列表**：
- {问题描述}

### Code Quality（code-quality-reviewer）

**结论**：PASS / FAIL
**Critical 问题**：
- {问题描述}

**Important 问题**：
- {问题描述}

### GitHub Readiness

**结论**：READY / NEEDS_INFO
**缺失字段**：
- {Issue / PR body / Test Evidence / CI / CodeQL / Risk / AI Collaboration / PR size 等缺失项}

### Harness Readiness

**结论**：READY / NEEDS_INFO
**Agent 可见能力缺口**：
- {测试/日志/指标/trace/截图/失败自诊断入口缺口}

### Loop Readiness

**结论**：READY / NEEDS_INFO
**Loop 缺口**：
- {缺少 Goal / Done Signal / Guardrails / Fallback / Memory；无则填"无"}

---

## Verification log

> 编译、测试、curl、截图、CI 复现等证据。必须包含命令、输出摘要和 exit code。压缩时必须保留。

### {YYYY-MM-DD} - {验证标题}

```text
command: {command}
exit code: {0/non-zero}
output:
{实际输出摘要}
```

---

## Loop Evidence

> 每轮执行后记录 Done Signal、Guardrails、Fallback 和 Memory。压缩时必须保留最终完成证据和任何人工接受风险。

### {YYYY-MM-DD} - {loop 标题}

| 项 | 内容 |
|----|------|
| Done Signal | {测试/日志/指标/review/截图/人工确认} |
| Guardrails checked | {不得删除测试/降低断言/绕过校验/跳过检查等} |
| Fallback | {未触发/已触发，说明降级、停机或人工确认} |
| Memory | {knowledge/rules/templates/tests/scripts；无则填"无"} |

---

## Knowledge candidates

> 工作过程中随手记录值得沉淀的发现。`/finish` 和 `/archive` 都会扫描本区块。
> 格式可以先粗略，但沉淀到 knowledge/index.md 时必须补齐 ID、Summary、Tags、Scope、Applies-To、Risk、Last-Verified、File。

### [待沉淀] {发现标题}

**类别**：业务知识 / 技术约定 / 踩坑记录 / 架构决策
**内容**：{具体内容}
**关键词**：{触发加载的关键词，用于 knowledge/index.md}
**建议 Scope**：{模块/路径/领域}
**建议 Applies-To**：propose / apply / review / fix-ci
**建议 Risk**：low / medium / high
**建议文件名**：`{knowledge-file-name.md}`

---

## 知识发现

> 兼容旧流程的知识记录区。`/finish` 和 `/archive` 都会扫描；新条目优先写入 `## Knowledge candidates`。

### [待沉淀] {发现标题}

**类别**：业务知识 / 技术约定 / 踩坑记录 / 架构决策
**内容**：{具体内容}
**关键词**：{触发加载的关键词，用于 knowledge/index.md}
**建议 Scope**：{模块/路径/领域}
**建议 Applies-To**：propose / apply / review / fix-ci
**建议 Risk**：low / medium / high
**建议文件名**：`{knowledge-file-name.md}`

---

## 遗留问题

> 本次未解决、留待后续处理的问题。人工接受风险必须保留在 log.md。

- [ ] {遗留问题描述}（预计：{YYYY-MM-DD} 或下个迭代；接受人/日期：{如适用}）

---

## /fix-ci 记录

> CI 失败后使用 `/fix-ci` 时填写。无 CI 失败可保留为空。

| 字段 | 内容 |
|------|------|
| CI run URL | {URL 或"未提供"} |
| Job 名称 | {job name} |
| 失败类型 | 编译 / 单测 / lint / 类型检查 / CodeQL / 依赖安装 / 环境配置 / 其他 |
| 失败命令 | `{command}` |
| 根因 | {基于日志和代码定位出的原因} |
| 修复摘要 | {改了什么，为什么是最小修复} |
| 验证命令 | `{command}` |
| 验证结果 | {实际输出摘要 + exit code} |
| commit | {commit hash + message} |

---

## /finish 记录

> `/finish` 用于 GitHub 收尾：验证、push、创建 PR；有 work Issue 时用 `Closes #<workIssue>`，manual/no-Issue 时省略 closing keyword；父 Issue 始终只用 `Refs #<parentIssue>` 引用。

| 字段 | 内容 |
|------|------|
| finish 模式 | ask / manual / auto-pr |
| parentIssue | {none / #123 / URL；仅引用，不用 closing keyword 关闭} |
| workIssue | {#456 / URL；manual/no-Issue 时 none} |
| issueRelationship | {sub-issue / standalone；manual/no-Issue 时 none} |
| closeTarget | {workIssue；manual/no-Issue 时 none} |
| branch | {type/scope} |
| 远端 | origin |
| PR | {PR URL 或"未创建"} |
| Base branch | main |
| closing statement | {Closes #<workIssue>；manual/no-Issue 时 none} |
| parent reference | {Refs #<parentIssue> 或"none"} |
| 验证命令 | `{command}` |
| 验证结果 | {实际输出摘要 + exit code} |

---

## Process notes

> 可压缩边界：中间尝试、调试细节、重复记录写在这里。触发 Log compression rule 后可移动到 log.archive.md。
> 不得在本节放置唯一的 commit hash、验证证据、review FAIL 原因或人工接受风险。

### {YYYY-MM-DD} - {事件标题}

**内容**：{过程性记录}
