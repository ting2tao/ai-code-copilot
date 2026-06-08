# 变更 Spec：harness-engineering-integration

> **状态**：[x] 已完成
> **复杂度档位**：[ ] Quick / [x] Standard / [ ] Complex
> **创建时间**：2026-06-08
> **关联 Issue**：本线程用户确认，待补 GitHub Issue
> **确认时间**：2026-06-08
> **确认人**：用户
> **确认范围 Hash**：待提交后补录

---

## 1. 背景与目标

### 1.1 背景

用户希望将 OpenAI Harness Engineering 方法论融入 ai-code-copilot。当前框架已有 Spec 驱动、review 和 archive，但尚未把 Agent 的可见性、可验证性、可读性作为明确的一等约束。

### 1.2 目标

将 Harness Engineering 融入现有流程，使每个变更都能回答：Agent 能看见什么、如何验证、失败时如何自诊断、哪些经验要沉淀。

### 1.3 非目标（Out of Scope）

- 不强制“零人工手写代码”。
- 不新增独立 Harness reviewer。
- 不实现 LogQL/PromQL/Chrome DevTools adapter。
- 不扩写 AGENTS.md 成长篇百科。

---

## 2. 功能点

| # | 功能点 | 优先级 | 备注 |
|---|--------|--------|------|
| F1 | 在核心文档中定义 Harness Engineering 的框架内含义 | P0 | 以 docs 为主，AGENTS/README 只短引 |
| F2 | 在主提示词中加入 Harness 驱动的流程要求 | P0 | 覆盖 /propose、/apply、/review、/archive |
| F3 | 在 spec、quick-card、test-spec 模板中加入 Agent Harness section | P0 | 保持字段轻量 |
| F4 | 在 reviewer 中检查 Agent 可验证性和 Agent 可读性 | P0 | 嵌入现有 reviewer |
| F5 | 在 check_framework.sh 中机械检查 Harness markers | P0 | 防止后续漂移 |

---

## 3. 变更范围

### 3.1 涉及模块

```
docs/
└── harness-engineering.md
AGENTS.md
README.md
agents/
├── copilot-prompt.md
├── spec-reviewer.md
└── code-quality-reviewer.md
changes/templates/
├── spec.md
├── quick-card.md
└── test-spec.md
scripts/
└── check_framework.sh
```

### 3.2 数据库变更

无。

### 3.3 接口变更

无。

---

## 4. 技术决策

| 决策点 | 选择 | 原因 |
|--------|------|------|
| Harness 承载位置 | 嵌入现有流程 | 减少新概念和额外 reviewer |
| AGENTS.md | 只加短索引 | 保持目录属性 |
| 自检方式 | marker 检查 | 简单稳定，适合脚本化 |

---

## 5. 风险与注意事项

- ⚠️ **模板变重**：Agent Harness 字段应短而可填，不写成长问卷。
- ⚠️ **概念误用**：不得把 OpenAI 实验里的“无人手写代码”作为通用硬性规则。

### 5.1 上线与回滚

| 项 | 内容 |
|----|------|
| 兼容性影响 | 仅文档、prompt、模板和自检脚本变更 |
| 灰度方式 | 不需要灰度 |
| 回滚方案 | 回滚本次文件变更 |
| 数据修复 | 无 |
| 监控指标 | `bash scripts/check_framework.sh` 通过 |

---

## 6. 待澄清事项

无。

---

## 7. 验收标准

- [x] `scripts/check_framework.sh` 检查 Harness markers。
- [x] 核心 docs/prompt 清楚区分 Harness 方法论和 OpenAI 实验约束。
- [x] 模板包含 Agent 可见证据、验证命令、可观测信号、失败自诊断入口。
- [x] reviewer 输出维度包含 Agent 可验证性/可读性。

---

## 8. 测试策略

- P0：运行 `bash scripts/check_framework.sh`。
- P1：人工检查文档不重复扩写 AGENTS.md。
- P2：无端到端测试。
- 不测试：实际 LogQL/PromQL/CDP 集成，因为本次不实现 adapter。
- 验证命令：`bash scripts/check_framework.sh`
