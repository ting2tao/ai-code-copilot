# Harness Engineering in ai-code-copilot

Harness Engineering 是 ai-code-copilot 对 “Context First, Code Follows” 的扩展：

> **Context First, Harness Enables, Code Follows.**

这里的 Harness 不是单个工具，而是一组让 Agent 能可靠工作的缰绳：规格、任务拆分、测试、日志、指标、review、规则、自检脚本和知识沉淀。工程师的价值不是被缩减为“写提示词”，而是设计一个 Agent 能看见、能验证、能自我修正的工作环境。

## 核心原则

1. **人类掌舵，Agent 执行**
   - 人类定义目标、边界、验收和风险。
   - Agent 负责 research、实现、验证、记录和修复。
   - Agent 失败时，优先问“缺了什么 Harness”，而不是只让它重试。

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

## 每个变更都要回答的问题

- Agent 能看见哪些证据？
- 必跑的验证命令是什么？
- 失败时 Agent 应先查哪里？
- 关键日志、指标、trace、截图或 CI 入口在哪里？
- 哪些信息不可见，需要人工补充？
- 这次经验是否应写入 `knowledge/` 或升级为机械规则？

## 不照搬的部分

OpenAI 的实验包含“零行人工手写代码”等团队约束。ai-code-copilot 不把它设为通用硬规则。本框架关注的是：让人类的判断通过 Harness 复用，让 Agent 的执行通过证据闭环，而不是规定人类永远不能编辑代码。
