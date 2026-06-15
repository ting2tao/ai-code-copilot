# 变更 Spec：loop-engineering-integration

> **状态**：[x] 已确认
> **复杂度档位**：[ ] Quick / [x] Standard / [ ] Complex
> **创建时间**：2026-06-15
> **关联 Issue**：https://github.com/ting2tao/ai-code-copilot/issues/28
> **确认时间**：2026-06-15
> **确认人**：用户
> **确认范围 Hash**：待提交后补录

---

## 1. 背景与目标

### 1.1 背景

用户提供两篇外部材料，希望 ai-code-copilot 具备 Loop Engineering。当前读取状态：

- 已读取用户提供的 `tweet_2064127981161959567.json`。Addy Osmani 将 Loop Engineering 描述为由系统替代人工逐轮提示 Agent；运行构件包括 Automations、Worktrees、Skills、Plugins/connectors、Sub-agents，以及外部 Memory。
- 已读取用户提供的 `微信公众号文章.json`。文章强调 Loop Engineering 的核心不只是工具五件套，而是目标定义能力：机器可验证的完成标准、边界条件、失败降级、目标分层，并提醒 Goodhart 风险。

本仓库已有 Harness Engineering，但还没有把 loop 作为一等工程对象写入主流程、模板和自检脚本。

### 1.2 目标

将 Loop Engineering 融入 ai-code-copilot，使每个变更都能声明并验证一个简洁的 Agent 反馈循环：Goal、Done Signal、Guardrails、Fallback、Memory。

### 1.3 非目标（Out of Scope）

- 不新增独立 `/loop` 命令。
- 不实现自动浏览器登录、微信验证或 X 长文抓取器。
- 不新增日志/指标/trace adapter。
- 不把无法读取的外部全文写成已验证事实。

---

## 2. 功能点

| # | 功能点 | 优先级 | 备注 |
|---|--------|--------|------|
| F1 | 新增 Loop Engineering 框架定义 | P0 | 说明 Harness 与 Loop 的边界 |
| F2 | 在主提示词核心法则和 propose/apply/review/archive 中加入 Goal Contract 要求 | P0 | 让 loop 进入实际工作流 |
| F3 | 在 spec、quick-card、test-spec、log 模板加入 Goal Contract/Loop Evidence 字段 | P0 | 让变更文档可审查 |
| F4 | 在 spec-reviewer 与 code-quality-reviewer 中检查 loop 可验证性和可读性 | P0 | 失败时回到 fix/reverse sync |
| F5 | 在 README/README-CN 中同步说明 Loop Engineering | P1 | 中英文档保持一致 |
| F6 | 在 `scripts/check_framework.sh` 加 Loop markers 自检 | P0 | 防止后续漂移 |
| F7 | 加入 DDD-lite Domain Check | P1 | 只在复杂业务场景记录领域语言、边界、不变量、状态流转和负责人 |

---

## 3. 变更范围

### 3.1 涉及模块

```
docs/
├── harness-engineering.md
└── loop-engineering.md
README.md
README-CN.md
AGENTS.md
agents/
├── copilot-prompt.md
├── spec-reviewer.md
└── code-quality-reviewer.md
rules/
└── domain-rules.md
changes/templates/
├── spec.md
├── quick-card.md
├── test-spec.md
└── log.md
scripts/
└── check_framework.sh
changes/loop-engineering-integration/
```

### 3.2 数据库变更

无。

### 3.3 接口变更

无。

---

## 4. 技术决策

| 决策点 | 选择 | 原因 |
|--------|------|------|
| Loop 定位 | Harness 之上的动态反馈模型 | Harness 提供可见环境，Loop 定义如何反复执行和调整 |
| 文档入口 | 新增 `docs/loop-engineering.md` | 避免把 `docs/harness-engineering.md` 写成过长混合概念 |
| 流程承载 | 嵌入现有命令 | 不增加用户心智负担 |
| 机械检查 | marker 检查 | 简单稳定，符合现有自检风格 |
| DDD 取舍 | DDD-lite Domain Check | 只保留会影响 Agent 正确性的领域语言、边界、不变量、状态流转和负责人，不强制完整 DDD 结构 |

---

## 5. 风险与注意事项

- ⚠️ **外部来源边界**：已读取用户提供的本地 JSON；外部平台实时页面仍可能受登录、验证或页面结构变化影响。
- ⚠️ **模板负担**：Goal Contract 应简短，可填“无/人工确认”，不得变成长问卷。
- ⚠️ **概念漂移**：Loop Engineering 不是“让 Agent 无限重试”，必须有 Done Signal、Guardrails、Fallback 和 Memory。
- ⚠️ **DDD 过度设计**：Domain Check 只在复杂业务触发，不强制 Entity/Aggregate/Repository 等结构名。

### 5.1 上线与回滚

| 项 | 内容 |
|----|------|
| 兼容性影响 | 仅文档、prompt、模板、reviewer 和自检脚本变更 |
| 灰度方式 | 不需要灰度 |
| 回滚方案 | 回滚本次文件变更 |
| 数据修复 | 无 |
| 监控指标 | `bash scripts/check_framework.sh` 通过 |

---

## 6. Agent Harness

| 项 | 内容 |
|----|------|
| Agent 可见证据 | `rg` 搜索 Loop markers；`bash scripts/check_framework.sh` 输出 |
| 必跑验证命令 | `bash scripts/check_framework.sh` |
| 日志/指标/trace 入口 | 无运行时日志；以变更文档和自检脚本作为 Agent 可见信号 |
| UI/浏览器验证入口 | 无 |
| 失败自诊断入口 | `scripts/check_framework.sh` marker 报错；`rg -n "Goal Contract|Loop Engineering|Loop Evidence"` |
| 不可见信息/人工确认 | 外部平台实时页面仍可能受登录或验证限制；本次以用户提供的本地 JSON 为已读证据 |
| 可沉淀的规则/知识 | Goal Contract 字段和自检 marker 可沉淀到模板/脚本 |

---

## 7. Goal Contract

| 项 | 内容 |
|----|------|
| Goal | 让每个 ai-code-copilot 变更都能声明可复用的 Agent 反馈循环 |
| Done Signal | `bash scripts/check_framework.sh` 通过，marker 搜索覆盖 docs/prompt/reviewer/templates/scripts |
| Guardrails | 不新增复杂 `/loop` 命令；不要求每个 Quick 填 Runtime 五件套；不把无法读取的外部全文当作事实 |
| Fallback | 自检失败时根据缺失 marker 补字段；外部材料不可读时写入不可见信息/人工确认 |
| Memory | `docs/loop-engineering.md`、`changes/templates/`、`scripts/check_framework.sh` |

### 7.1 Loop Runtime（可选）

| 能力 | 内容 |
|------|------|
| Automation | 本次不启用；仅在定时 triage、批量修 CI、跨 PR 处理等场景设计 |
| Worktree isolation | 使用当前分支；未来并行 Agent 场景启用 worktree |
| Skills / knowledge | 使用 ai-code-copilot skill 和本次外部材料作为知识输入 |
| Plugins / connectors | 本次不接入外部 connector |
| Maker-checker subagents | 通过现有 spec-reviewer / code-quality-reviewer 保持 maker-checker 分离 |

---

## 8. Domain Check（DDD-lite，仅复杂业务填写）

| 字段 | 内容 |
|------|------|
| Language | Loop Engineering、Harness Engineering、Goal Contract、Loop Runtime、Domain Check 的含义需在 docs/prompt/templates 中保持一致 |
| Boundary | 本次只修改框架方法论、prompt、模板、reviewer 和自检；不改变任何业务项目运行时代码 |
| Invariants | 不新增强制 `/loop` 命令；Quick 不强制 Runtime 五件套；Domain Check 不强制完整 DDD 分层；已读证据必须和文档一致 |
| State Transitions | 文档流程保持 brainstorm → propose → apply → review → archive；Domain Check 仅在领域复杂度触发时从“不适用”转为必填 |
| Owner | 框架维护者；涉及业务领域规则时由具体项目 owner 人工确认 |

---

## 9. 待澄清事项

无。

---

## 10. 验收标准

- [x] `docs/loop-engineering.md` 定义 Loop Engineering，并说明与 Harness Engineering 的关系。
- [x] `agents/copilot-prompt.md` 要求 propose/apply/review/archive 记录和使用 Goal Contract。
- [x] `changes/templates/spec.md`、`quick-card.md`、`test-spec.md`、`log.md` 包含 Goal Contract/Loop Evidence 字段。
- [x] `agents/spec-reviewer.md` 与 `agents/code-quality-reviewer.md` 检查 loop 可验证性/可读性和 Goodhart 风险。
- [x] `README.md` 与 `README-CN.md` 同步说明 Loop Engineering。
- [x] `scripts/check_framework.sh` 检查 Loop markers，且 `bash scripts/check_framework.sh` 通过。
- [x] `rules/domain-rules.md`、`changes/templates/spec.md`、`changes/templates/quick-card.md`、主 prompt 和 reviewer 包含 Domain Check / DDD-lite 规则。

---

## 11. 测试策略

- P0：运行 `bash scripts/check_framework.sh`。
- P1：运行 `rg -n "Goal Contract|Done Signal|Guardrails|Fallback|Loop Runtime|Loop Evidence|Domain Check|Invariants|State Transitions" docs README.md README-CN.md AGENTS.md agents rules changes/templates scripts`。
- P2：人工检查 README 中英内容一致。
- 不测试：外部平台全文抓取与登录态读取，因为本次不实现 adapter。
- 验证命令：`bash scripts/check_framework.sh`
