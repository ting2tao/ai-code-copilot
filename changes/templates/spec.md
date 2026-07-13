# 变更 Spec：{变更名}

> **状态**：[ ] 草稿 / [ ] 已确认 / [ ] 实施中 / [ ] 已完成
> **复杂度档位**：[ ] Quick / [ ] Standard / [ ] Complex
> **创建时间**：{YYYY-MM-DD}
> **父 Issue（parentIssue）**：{none / #123 / URL；已有父需求时填写}
> **工作 Issue（workIssue）**：{pending / #456 / URL；manual 且未提供 Issue 时填 none}
> **Issue 关系（issueRelationship）**：{pending / sub-issue / standalone；manual/no-Issue 时填 none}
> **关闭目标（closeTarget）**：{workIssue；manual/no-Issue 时为 none，且省略 closing keyword}
> **分支（branch）**：{type/scope；例如 feat/issue-workflow}
> **确认时间**：{YYYY-MM-DD HH:mm 或"未确认"}
> **确认人**：{用户/姓名}
> **确认范围 Hash**：{spec.md + tasks.md + test-spec.md 内容摘要}

---

## 1. 背景与目标

### 1.1 背景

{描述为什么要做这个变更，当前存在什么问题或业务诉求}

### 1.2 目标

{本次变更要实现什么，用一句话说清楚}

### 1.3 非目标（Out of Scope）

{明确不做什么，防止范围蔓延}

---

## 2. 功能点

> 每个功能点对应 tasks.md 中的一个或多个 Task。

| # | 功能点 | 优先级 | 备注 |
|---|--------|--------|------|
| F1 | {功能描述} | P0/P1/P2 | |
| F2 | | | |

---

## 3. 变更范围

### 3.1 涉及模块

```
{模块路径}
├── controller/
│   └── {XxxController.java}     ← {说明改动}
├── service/
│   ├── {XxxService.java}        ← {说明改动}
│   └── {XxxServiceImpl.java}    ← {说明改动}
└── dao/
    └── {XxxMapper.java}         ← {说明改动}
```

### 3.2 数据库变更

```sql
-- {说明 DDL 变更，无变更填"无"}
```

### 3.3 接口变更

```
{接口路径} {HTTP方法}
Request:  {参数说明}
Response: {返回说明}
```

---

## 4. 技术决策

| 决策点 | 选择 | 原因 |
|--------|------|------|
| {如：并发控制} | {如：Redis 分布式锁} | {如：现有基础设施已有，TTL=30s} |

---

## 5. 风险与注意事项

- ⚠️ **{风险点}**：{说明风险和缓解措施}
- 涉及资金/状态流转/权限变更时必须标注 ⚠️ 并说明影响范围

### 5.1 上线与回滚

| 项 | 内容 |
|----|------|
| 兼容性影响 | {接口/数据/配置兼容性说明；无则填"无"} |
| 灰度方式 | {如何小流量/分批启用；无需灰度则说明原因} |
| 回滚方案 | {代码回滚、配置回滚、数据回滚步骤} |
| 数据修复 | {是否需要补偿/修复脚本；无则填"无"} |
| 监控指标 | {上线后观察的日志、指标、告警} |

---

## 6. Agent Harness

> 记录 Agent 能看见、能运行、能自诊断的反馈循环。没有对应能力时填"无"，并说明是否需要人工确认。

| 项 | 内容 |
|----|------|
| Agent 可见证据 | {测试结果、构建输出、日志、指标、trace、截图、CI/PR 链接等} |
| 必跑验证命令 | `{project-context.md 中记录的命令}` |
| 日志/指标/trace 入口 | {日志查询、指标名称、trace/span、无则说明} |
| UI/浏览器验证入口 | {页面/路由/操作路径；无 UI 则填"无"} |
| 失败自诊断入口 | {失败时先看哪些命令、日志、文件或 dashboard} |
| 不可见信息/人工确认 | {聊天、会议、人脑知识、外部系统限制等} |
| 可沉淀的规则/知识 | {应写入 rules、knowledge、模板或自检脚本的内容} |

---

## 7. Goal Contract

> 记录这个变更的 Agent 反馈循环。Loop 不是无限重试，必须有机器可验证的 Done Signal、边界 Guardrails 和失败 Fallback。

| 项 | 内容 |
|----|------|
| Goal | {这轮到底要达成什么} |
| Done Signal | {什么机器可验证信号代表完成，如测试/类型检查/lint/指标阈值} |
| Guardrails | {不能用什么方式假完成，如不得删除测试、降低断言、绕过权限、跳过 lint} |
| Fallback | {失败几轮后怎么降级、停机、Reverse Sync 或找人确认} |
| Memory | {哪些经验要沉淀到 knowledge、rules、templates、tests 或脚本} |

### 7.1 Loop Runtime（可选）

> 仅自动化、批量修复、跨 PR/Issue、定时巡检等长运行场景填写；普通变更填"不启用"。

| 能力 | 内容 |
|------|------|
| Automation | {定时/事件触发方式；不启用则填"不启用"} |
| Worktree isolation | {是否需要独立 worktree/分支；不需要则说明原因} |
| Skills / knowledge | {需要加载的 skill 或 knowledge；无则填"无"} |
| Plugins / connectors | {GitHub/Linear/Slack/DB/MCP 等连接器；无则填"无"} |
| Maker-checker subagents | {是否拆分执行者和检查者；无则说明原因} |

---

## 8. Domain Check（DDD-lite，仅复杂业务填写）

> 仅金额、库存、额度、权限、状态机、跨模块业务协作、强一致性或领域词混淆时填写；普通 CRUD、UI、脚本、基础设施变更填"不适用"。

| 字段 | 内容 |
|------|------|
| Language | {核心领域词及定义；不适用则填"不适用"} |
| Boundary | {所属业务边界、不会跨越的边界；不适用则填"不适用"} |
| Invariants | {必须永远成立的业务不变量；不适用则填"不适用"} |
| State Transitions | {合法状态/流转/禁止流转/失败处理；不适用则填"不适用"} |
| Owner | {领域规则负责人或需人工确认的角色；不适用则填"不适用"} |

---

## 9. 待澄清事项

> /apply 前此列表必须清空

- [ ] {待澄清问题 1}
- [ ] {待澄清问题 2}

---

## 10. 验收标准

> 对应 /test 的 P0 用例

- [ ] {验收条件 1}
- [ ] {验收条件 2}

---

## 11. 测试策略

> /propose 阶段生成草案，/test 阶段细化为 test-spec.md。

- P0：{核心业务逻辑/主链路用例}
- P1：{数据访问/边界条件}
- P2：{入口层/错误响应/兼容性}
- 不测试：{明确不覆盖的内容及原因}
- 验证命令：`{project-context.md 中记录的命令}`
