# Harness Engineering in ai-code-copilot

Harness Engineering 是 ai-code-copilot 对 “Context First, Code Follows” 的扩展：

> **Context First, Harness Enables, Code Follows.**

这里的 Harness 不是单个工具，而是一组让 Agent 能可靠工作的缰绳：规格、任务拆分、测试、日志、指标、review、规则、自检脚本和知识沉淀。工程师的价值不是被缩减为“写提示词”，而是设计一个 Agent 能看见、能验证、能自我修正的工作环境。

Loop Engineering 是 Harness 之上的动态控制模型：Harness 回答 Agent 能看见什么，Loop 回答 Agent 如何基于这些信号循环执行、调整、停止和沉淀。框架内定义见 [`docs/loop-engineering.md`](loop-engineering.md)，核心产物是轻量的 Goal Contract。

## Harness 随 Spec 档位增长

普通低风险工作由模型原生执行，不强制建立框架记录。需要生命周期编排或实质风险控制时，框架自动激活：Compact SDD 把 Goal Contract 写入 `quick-card.md`；Full SDD 写入 `spec.md` 并由 tasks/test-spec/log/summary 扩展。原生执行、Compact SDD、Full SDD 使用相同的安全与验证标准，区别是 Harness 的持久化深度。

Harness 信号必须从合同派生：Acceptance 和 Done Signal 决定成功验证，Guardrails 防止通过删测试或绕过检查“假完成”，Fallback 决定失败后的降级、停止或人工门禁。升级时复制已有命令和真实结果，不为补文档虚构或重复成功证据。

## 核心原则

1. **人类掌舵，Agent 执行**
   - 人类定义目标、边界、验收和风险。
   - Agent 负责 research、实现、验证、记录和修复。
   - Agent 失败时先定位缺失反馈，也检查既有 Harness 假设是否过时；不默认用更多规则或重试解决。

2. **AGENTS.md 是目录，不是百科全书**
   - `AGENTS.md` 只保留短索引和关键入口。
   - 详细架构、规则和流程放在 `docs/`、`rules/`、`changes/templates/` 和 `knowledge/`。
   - 结构正确性由 `scripts/check_framework.sh` 等机械检查维护。

3. **让 Agent 看见可验证证据**
   - 每个变更都要记录 Agent 可见证据：测试命令、构建命令、日志入口、指标入口、UI 验证方式或人工确认项。
   - 如果信息只存在于聊天、会议或人脑中，对 Agent 来说就等于不存在，应沉淀到 repo-local 文档。

4. **Agent 可读性优先**
   - 代码、错误信息、日志、文档和测试都应便于 Agent 定位和推理。
   - 偏好稳定、清晰、组合性好的 “boring tech”。
   - 重要边界用规则、lint、结构化测试或 reviewer 约束，而不是靠口头提醒。

5. **Review 是反馈循环**
   - Spec reviewer 检查“是否按合同实现”以及“验收是否 Agent 可验证”。
   - Code quality reviewer 检查安全、可维护性以及“代码和信号是否 Agent 可读”。
   - Review 发现的问题应尽量沉淀为模板、规则、脚本或 knowledge。

## 官方 Agent / Harness 原则对齐（核对于 2026-09-03）

以下是本次检索并打开核实的相关官方资料，不声称穷尽所有最新发布。日期为文章发布日期；无发布日期的文档按查阅日记录。**来源观点与本项目落地选择分开**，不把厂商示例架构变成通用强制流程。

| 官方依据 | 提炼的原则 | 本项目落点与不照搬的边界 |
|----------|------------|--------------------------|
| OpenAI，2026-08-19：[Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform) | 可复用的是带 context、tools、进度、恢复与审批的 agent loop，而非单次 prompt | 宿主提供运行循环/权限机制；本框架提供项目合同和验证入口，不再造一个 agent runtime |
| OpenAI，2026-08-25：[Automating repetitive work](https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex) | 将实际命令、结果、失败尝试与人类决策变成下次可复用的工作上下文 | 复用 log/summary/knowledge，保留失败原因与选择依据，不引入新的 notebook 服务或文档权威 |
| OpenAI，查阅 2026-09-03：[Evaluate agent workflows](https://developers.openai.com/api/docs/guides/agent-evals) | 先用 trace 定位工具选择、交接和护栏问题，再用数据集做可重复评测 | outcome 与 trace 分开审查；offline oracle、grader 自检、真实 Agent run 三种证据不能互相冒充 |
| Anthropic，2026-03-24：[Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 执行与评价分离，给出可验证交付；逐项消融并重审随模型变化而失效的支架 | 固定验收比较 baseline/removed/restored；模型升级后重测必要性。保留逻辑上的 maker/checker 分离，但不默认增加多 Agent 或强制 sprint |
| Anthropic，2026-04-08：[Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) | session、harness、sandbox 是不同职责；持久会话不等于当前 context，凭据不应暴露给生成代码 | 用现有 Git/log 保存可审计事实；控制面持有授权/凭据，执行环境只获最小工具能力。不为概念分层新增三个服务 |
| Anthropic，2025-09-29：[Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | context 是有限资源；按需检索高价值内容，避免重复工具与模糊接口 | 保留 router/索引/路径引用，重读会变化的事实；外部文本作为数据而非指令，按需加载不等于漏读适用规则 |

### 本框架的执行约束

- **Loop**：观察当前状态 → 在合同与权限内行动 → 对实际结果验证 → 继续、交接或停止。自然语言宣称成功、工具 exit 0 和任务完成是三件事；成功必须满足当前 Acceptance。
- **可恢复性**：恢复时核对分支/revision、dirty diff、最近验证和未决审批；summary 是检索线索，不是对实时状态的替代。保留已发生副作用，避免在中断恢复后重复外部操作。
- **控制面边界**：审批主体、完整动作快照、可信 policy 和执行隔离分别核验；prompt、regex、模型自报批准不能承担身份认证。受控 CI 不能执行待审分支自改的门禁来证明自身可信。
- **证据分级**：self-review 只能标 self-review；独立 evaluator 也需用失败样本及人工判例校准，检查实际 outcome，而不是奖励漂亮的解释。只保存必要、脱敏的动作与结果，不收集私有思维链。
- **消融与漂移**：每个新增支架写清要纠正的失败模式；固定 model/version、policy/revision、任务与验收，单因素比较质量、失败率、成本/时延。模型升级、工具协议变化或重复误报触发重测，不机械增加或删除步骤。安全/权限门禁不可在线消融，样本未失败不证明冗余。
- **能力事实**：分开记录平台支持、仓库实现、测试验证、本地启用；厂商文档更新不能直接推导本机已具备能力。当前 hook 差异见 `rules/security.md`，不把 Claude 与 Codex 的同名事件当作同一协议。

## 每个变更都要回答的问题

- Agent 能看见哪些证据？
- 必跑的验证命令是什么？
- 失败时 Agent 应先查哪里？
- 关键日志、指标、trace、截图或 CI 入口在哪里？
- 哪些信息不可见，需要人工补充？
- 当前 Spec 档位中的 Goal Contract 是什么：Goal、Done Signal、Guardrails、Fallback、Memory？Acceptance/Done Signal/Guardrails/Fallback 分别派生了哪些验证、反作弊和失败处理信号？
- 这次经验是否应写入 `knowledge/` 或升级为机械规则？

## 不照搬的部分

OpenAI 的实验包含“零行人工手写代码”等团队约束。ai-code-copilot 不把它设为通用硬规则。本框架关注的是：让人类的判断通过 Harness 复用，让 Agent 的执行通过证据闭环，而不是规定人类永远不能编辑代码。
