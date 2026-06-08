# 设计简报：harness-engineering-integration

> **状态**：[x] 已确定
> **复杂度预判**：[ ] Quick / [x] Standard / [ ] Complex
> **创建时间**：2026-06-08
> **关联 Issue**：本线程用户确认，待补 GitHub Issue

---

## 1. 需求理解

将 OpenAI Harness Engineering 的关键思想融入 ai-code-copilot，但不照搬“零人工手写代码”等实验约束。目标是把 Harness 变成框架中的可执行能力：Agent 可见证据、验证命令、日志/指标入口、review 维度、知识沉淀和自检脚本。

---

## 2. 现状分析

| 模块/文件 | 现状描述 | 文件路径 |
|-----------|---------|---------|
| 主提示词 | 已有 Spec 驱动、Evidence Before Claims、双阶段 review，但缺少 Harness 明确定义和 Agent 可见能力字段 | `agents/copilot-prompt.md` |
| 变更模板 | spec/test/quick-card 已包含验收、测试、监控字段，但没有统一的 Agent Harness section | `changes/templates/*.md` |
| reviewer | 已检查 spec 合规和代码质量，但没有显式检查 Agent 可验证性/可读性 | `agents/spec-reviewer.md`, `agents/code-quality-reviewer.md` |
| 自检脚本 | 已检查模板、pack、命令菜单漂移，但未检查 Harness 字段是否存在 | `scripts/check_framework.sh` |
| 知识入口 | AGENTS.md 是精简索引，适合只新增短索引，不适合扩成长文 | `AGENTS.md` |

---

## 3. 方案选项

### 方案 A：最小可执行融入（推荐）

- **思路**：新增一份 Harness 文档，主 prompt 和模板增加 Agent Harness 字段，reviewer 增加检查维度，自检脚本强制 marker。
- **优点**：上下文增量小，直接进入现有门禁。
- **缺点**：暂不实现真正的 doc-gardening agent 或 observability adapter。
- **工作量**：1 天内，约 8-10 个框架文件。
- **风险**：字段过多可能让模板变重，需要保持短字段。

### 方案 B：完整 Harness 子系统

- **思路**：新增独立 Harness Readiness reviewer、doc-gardening 命令、日志/指标 adapter。
- **优点**：能力完整。
- **缺点**：超出当前框架成熟度，容易做成空壳。
- **工作量**：多天，跨脚本和工具链。
- **风险**：维护成本高。

---

## 4. 推荐方案 & 决策理由

- 选定方案：方案 A
- 决策理由：Harness Engineering 的第一步不是加复杂工具，而是把 Agent 所需的反馈回路写进 spec、review 和自检。
- 用户已确认：[x] 是

---

## 5. 风险识别

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 口号化 | README 变好看但流程不变 | 用模板、reviewer、自检脚本承载约束 |
| 上下文膨胀 | AGENTS.md 过长，挤占任务上下文 | AGENTS.md 只加短索引，长文放 docs |
| 过度照搬 | 把 OpenAI 实验约束误设为通用规则 | 明确不强制“零人工手写代码” |

---

## 6. YAGNI 裁剪

- [x] 不做独立 Harness reviewer — 先嵌入现有 Spec/Code/GitHub Readiness。
- [x] 不做 doc-gardening agent — 先用 check_framework.sh 做静态约束。
- [x] 不接 LogQL/PromQL/CDP adapter — 先记录 capability inventory。

---

## 7. 进入 /propose 的前置结论

- **选定方案**：方案 A
- **涉及模块**：docs、AGENTS、README、prompt、templates、reviewers、check script
- **预计复杂度**：Standard
- **核心改动点**：定义 Harness；模板新增 Agent Harness；reviewer 检查 Agent 可验证/可读；自检脚本强制 marker。
- **用户已确认**：[x] 是
