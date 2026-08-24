<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:design-brief
artifactType: design-brief
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: none
upstreamHash: none
-->

# 设计简报：ai-native-sdlc-alignment

> **状态**：[ ] 探索中 / [x] 已确定
> **复杂度预判**：[ ] Quick / [ ] Standard / [x] Complex
> **创建时间**：2026-08-24
> **关联 Issue**：parentIssue=none；workIssue 按 `on-publish` 延后解析
> **参考来源**：Anthropic, “The AI-Native SDLC playbook”, 2026-08-21

---

## 1. 需求理解

吸收 AI-native SDLC 的产物驱动、持续评测、确定性治理和维护闭环思想，优化 ai-code-copilot。保留现有 Progressive SDD、Goal Contract、Harness/Loop Engineering 和人工风险门禁，不照搬 Claude 专属文件名、服务或企业配置。目标是让框架不仅能规范一次编码会话，还能机械验证阶段交接、回归测试 Agent 配置，并让 CI/事故信号重新进入规划流程。

### 战略主张

AI Coding 只是第一阶段。下一阶段的竞争，不是谁让工程师用 Claude/Codex 更快地产生代码，而是谁先把研发系统改造成 Agent 可以持续工作的系统。这个系统由 `Context Engineering + Skills + Artifact Chain + Evals + Hooks + Agent Review + Human Gates + Git Audit Trail` 共同构成；任何单点工具都不能独立替代完整系统。

---

## 2. 现状分析

| 模块/文件 | 现状描述 | 文件路径 |
|-----------|---------|---------|
| Full SDD 记录集 | 已有 design-brief、spec、tasks、test-spec、log、summary、roadmap，但产物间主要靠人读语义关联 | `agents/workflows/full.md`, `changes/templates/*.md` |
| Agent 反馈循环 | 已有 Harness、Goal Contract、Red/Green、双阶段 review 和真实验证证据 | `docs/harness-engineering.md`, `docs/loop-engineering.md`, `agents/workflows/*.md` |
| 框架回归检查 | 已有静态合同检查和多技术栈初始化 fixtures，但缺少真实任务级 Agent 配置 eval | `scripts/check_framework.sh`, `scripts/check_progressive_sdd.py`, `tests/fixtures/**` |
| 治理执行 | 安全、Git、Issue 和风险规则完整，但当前仓库 hook 仅处理 SessionStart，许多规则仍是 advisory control | `hooks/hooks.json`, `rules/security.md`, `rules/commit-convention.md` |
| Maintain 闭环 | `/fix-ci` 能处理已知失败，`/archive` 能沉淀知识；缺少事件/事故/告警到 draft intent 的正式入口 | `agents/workflows/debug.md`, `agents/workflows/archive.md` |
| 生命周期指标 | 已定义 Issue、PR、CI 自愈和 PR 结构信号；缺少阶段时延、首次通过率、返工、eval 和事故复发指标 | `rules/github-metrics.md` |

---

## 3. 方案选项

### 方案 A：AI-native 增量对齐（推荐）

- **思路**：沿用现有文档和命令，分阶段增加 Artifact Chain metadata、Agent eval、确定性 guardrail contract、triage/Maintain 回流和生命周期指标。
- **优点**：兼容现有变更记录；不引入第二套 SDD；每阶段可独立验证和回滚。
- **缺点**：需要同时维护平台无关合同和少量平台 adapter；完整收益要经过真实项目数据验证。
- **工作量**：Complex，拆成 3 个 Standard 子变更，预计修改 20+ 个框架文件并新增 eval/guardrail 脚本与 fixtures。
- **风险**：metadata 和门禁过多会增加上下文与维护成本；live eval 可能产生模型调用成本和非确定性。

### 方案 B：完全采用文章的文件链

- **思路**：新增并强制 `intent.md → spec.md → plan.md → diff → review → incident`。
- **优点**：概念与文章一一对应，外部理解成本低。
- **缺点**：与 design-brief、tasks、test-spec、Quick Card 重复，削弱 Progressive SDD。
- **工作量**：Complex，且需要迁移现有模板和记录。
- **风险**：文档膨胀、兼容性下降、为形式牺牲小变更效率。

### 方案 C：只更新方法论文档

- **思路**：在 README 和 Harness/Loop 文档中增加 AI-native SDLC 说明，不改变脚本和工作流。
- **优点**：成本最低。
- **缺点**：没有行为级改进，无法验证 Agent 配置是否回归，也不能闭合 Maintain 循环。
- **工作量**：Quick/Standard。
- **风险**：优化停留在口号层。

---

## 4. 推荐方案与决策理由

- 选定方案：方案 A
- 决策理由：项目已经具备文章的大部分核心概念，应把现有语义合同升级为机器可验证合同，而不是新增重复流程。
- 用户已确认：[x] 是（2026-08-24，确认采用前述三阶段优化方向）

---

## 5. 风险识别

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 产物 metadata 变重 | Quick/Inline 使用成本上升 | Inline 不落盘；Compact 仅保留最小字段；完整链只要求 Full |
| eval 非确定性与成本 | CI 偶发失败或费用失控 | 静态 schema/fixture eval 必跑；live eval 可配置、分层、带预算且先非阻塞 |
| 平台耦合 | Claude/Codex 能力差异污染核心合同 | 核心定义平台无关 control；adapter 单独实现并允许 capability=unsupported |
| 过度自动化 | Agent 越过生产、权限或外部写入门禁 | 自动化默认只诊断和产出 draft artifact；生产与高风险动作保持人工确认 |
| 指标 Goodhart | 团队为数值优化而非质量 | 指标成组解读；保留 Guardrails；不以单一指标排名或阻塞 |
| 兼容性 | 旧记录无法通过新检查 | 新字段只对新建/升级记录强制；旧记录维持 legacy 读取路径 |

---

## 6. YAGNI 裁剪

- [x] 不新增强制 `intent.md`；强化 `design-brief.md` 作为 intent-equivalent artifact。
- [x] 不新增强制 `plan.md`；继续使用 `tasks.md` + `test-spec.md`。
- [x] 不把 Claude Tag、Claude Code Review、managed settings 设为核心依赖。
- [x] 不默认允许 Agent 自动部署或回滚生产。
- [x] 不首期建设通用可观测平台；只定义事件、指标和 adapter 合同。
- [x] 不要求历史变更批量迁移。

---

## 7. 进入 /propose 的前置结论

- **选定方案**：方案 A
- **涉及模块**：workflow/policy、templates、evals、scripts、hooks/guardrails、metrics、docs、README
- **预计复杂度**：Complex，3 个可独立 review 的 Standard 子变更
- **核心改动点**：Artifact Chain；Agent eval；deterministic guardrails；Maintain→Plan；lifecycle metrics
- **用户已确认**：[x] 是
