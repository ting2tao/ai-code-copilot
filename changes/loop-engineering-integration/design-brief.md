# 设计简报：loop-engineering-integration

> **状态**：[ ] 探索中 / [x] 已确定
> **复杂度预判**：[ ] Quick / [x] Standard / [ ] Complex
> **创建时间**：2026-06-15
> **关联 Issue**：https://github.com/ting2tao/ai-code-copilot/issues/28

---

## 1. 需求理解

用户提供微信公众号文章和 Addy Osmani 的 X 长文链接，希望读取材料后理解 Loop Engineering，并把这个概念结合到 ai-code-copilot，使框架不仅有 Spec/Harness 驱动，还显式具备“Goal -> Done Signal -> Guardrails -> Fallback -> Memory”的循环工程能力。

---

## 2. 现状分析

| 模块/文件 | 现状描述 | 文件路径 |
|-----------|---------|---------|
| 核心方法论 | 已定义 Harness Engineering：规格、测试、日志、指标、review、规则、自检脚本和知识沉淀共同构成 Agent 可见反馈循环，但没有把 loop 作为一等对象定义。 | `docs/harness-engineering.md` |
| 主提示词 | 已要求 Harness Enables、Evidence Before Claims、review/fix/archive 闭环；但没有要求每个变更声明 loop goal、observation、tuning levers、exit condition。 | `agents/copilot-prompt.md` |
| 模板 | `spec.md`、`quick-card.md`、`test-spec.md` 已有 Agent Harness 字段；缺少 Goal Contract 字段，无法强制记录完成信号、护栏、失败降级和沉淀位置。 | `changes/templates/*.md` |
| 领域规则 | 已有通用领域规则，但缺少轻量 DDD 入口，无法在复杂业务中显式记录领域语言、边界、不变量和状态流转。 | `rules/domain-rules.md` |
| 自检脚本 | 已检查 Harness markers，未检查 Loop Engineering markers，无法防止后续概念漂移。 | `scripts/check_framework.sh` |
| README | 已说明 feedback loops，但没有给 Loop Engineering 一个清晰入口。 | `README.md`, `README-CN.md` |

---

## 3. 方案选项

### 方案 A：把 Loop Engineering 嵌入现有 Harness（推荐）

- **思路**：新增 `docs/loop-engineering.md`，并在 prompt、模板、reviewer、自检和 README 中加入轻量 Goal Contract。
- **优点**：复用现有 workflow，不增加新命令；让 loop 变成可审查字段。
- **缺点**：需要同时更新多份模板和自检脚本。
- **工作量**：约 8-10 个文档/脚本文件。
- **风险**：模板字段变重；通过简短表格和 marker 自检控制。

### 方案 B：新增独立 `/loop` 命令

- **思路**：为 loop 设计单独命令，负责生成和执行循环配置。
- **优点**：概念边界清晰。
- **缺点**：现阶段会和 `/apply`、`/fix`、`/test`、`/archive` 重叠，增加学习成本。
- **工作量**：较大，需要完整命令流和模板。
- **风险**：过度设计。

### 方案 C：只更新 README/文档

- **思路**：解释 Loop Engineering，不改 prompt 和模板。
- **优点**：改动最小。
- **缺点**：不会真正改变 Agent 行为，无法证明“本项目具有 Loop Engineering”。
- **工作量**：小。
- **风险**：停留在概念层。

---

## 4. 推荐方案 & 决策理由

- 选定方案：A
- 决策理由：本项目已经有 Harness 作为 Agent 可见环境，Loop Engineering 应作为 Harness 的动态执行模型，而不是另起一套命令系统。把 Goal Contract 放入 spec/quick-card/test-spec/review，可以让每个变更都回答“目标是什么、怎么证明完成、如何防止假完成、失败怎么降级、经验沉淀到哪里”。
- DDD 取舍：加入 DDD-lite Domain Check，而不是完整 DDD 框架；只在复杂业务触发 Language、Boundary、Invariants、State Transitions、Owner 五项。
- 用户已确认：[x] 是（来自本线程持续目标）

---

## 5. 风险识别

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 外部材料不可完全读取 | 可能误引来源 | 明确记录可读证据；微信正文不可读，X 仅用可验证的公开摘要和元数据，不伪造全文内容 |
| 概念重叠 | Harness 和 Loop 边界不清 | 定义 Harness 是环境，Loop 是运行在 Harness 上的反馈循环 |
| 模板变重 | 用户填写负担上升 | 字段保持短表格，并允许无对应能力时填“无/人工确认” |
| DDD 过重 | 框架变成架构宗教 | 明确 Domain Check 是 DDD-lite，不强制 Entity/Aggregate/Repository |

---

## 6. YAGNI 裁剪

- [x] 不新增 `/loop` 命令 — 先把 loop contract 嵌入现有流程。
- [x] 不实现自动指标/日志 adapter — 本次只定义入口和自诊断字段。
- [x] 不要求“无人手写代码” — 本项目强调人类判断可复用，Agent 执行有证据。
- [x] 不引入完整 DDD 框架 — 只保留复杂业务需要的 Domain Check。

---

## 7. 进入 /propose 的前置结论

- **选定方案**：A
- **涉及模块**：docs、README、agents、reviewers、templates、check script、change docs
- **预计复杂度**：Standard
- **核心改动点**：定义 Loop Engineering；补 Goal Contract；更新 review 与 archive 规则；加入自检 marker；同步中英 README。
- **用户已确认**：[x] 是 → 可执行 `/propose loop-engineering-integration`
