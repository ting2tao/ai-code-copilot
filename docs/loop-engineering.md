# Loop Engineering in ai-code-copilot

Loop Engineering 是 ai-code-copilot 对 Agent 工作方式的动态建模：

> **Context defines the target. Harness exposes the signals. Loop Engineering runs the feedback cycle.**

这里的 loop 不是“让 Agent 无限重试”。它是一个有退出条件的反馈循环：给定目标和上下文，Agent 执行动作，读取可观察信号，调整下一步，并把可复用经验沉淀回规则、模板、测试或知识库。

## 与 Harness Engineering 的关系

- **Harness Engineering** 回答：Agent 能看见什么、能运行什么、失败时能查哪里。
- **Loop Engineering** 回答：Agent 如何基于这些信号反复推进、调参、停止和沉淀。

换句话说，Harness 是环境，Loop 是运行在环境上的控制回路。

## Goal Contract

每个变更都应能写出一份简短的 Goal Contract。它不是流程问卷，而是目标管理：

| 项 | 问题 |
|----|------|
| Goal | 这轮到底要达成什么？ |
| Done Signal | 什么机器可验证信号代表完成？ |
| Guardrails | 不能用什么方式“假完成”？ |
| Fallback | 失败几轮后怎么降级、停机或找人？ |
| Memory | 哪些东西要沉淀，避免下次重来？ |

`Done Signal` 不能孤立存在。只写“测试通过”会诱导 Agent 针对验证器投机，例如删除失败测试、降低断言或绕过 lint。`Guardrails` 要和完成标准一起定义，防止 Goodhart 风险。

Goal Contract 不创建独立的流程文档，而是嵌入当前 Spec 档位：Inline SDD 在会话中保存 Goal/Scope/Done Signal/Verify；Compact SDD 写入 `quick-card.md`；Full SDD 写入 `spec.md`。Acceptance 与 Done Signal 生成正向验证，Guardrails 生成不得绕过的反向检查，Fallback 生成失败后的退出或人工门禁，Memory 决定是否进入 knowledge。

活动变更只允许 `Inline -> Compact -> Full` 或 `Inline -> Full` 单向升级。升级前停止新增编辑，复制合同、diff 和已有证据；机械 Reverse Sync 可直接记录，Goal、Scope、Acceptance、Guardrails、风险或外部动作变化则必须重新确认。

## Loop Runtime（可选）

当变更需要更强的自主循环时，再启用 Runtime 五件套：

| 能力 | 作用 |
|------|------|
| Automation | 定时或事件触发，是 loop 的心跳 |
| Worktree isolation | 并行 Agent 隔离工作区，避免互相踩文件 |
| Skills / knowledge | 把项目知识写在会话外，避免每轮重新猜 |
| Plugins / connectors | 连接 issue、CI、数据库、Slack 等真实工具 |
| Maker-checker subagents | 执行者和检查者分离，避免自己给自己打分 |

普通 Quick/Standard 变更不需要逐项填写 Runtime。只有自动巡检、批量修 CI、跨 PR 处理、定时 triage 等长运行场景才需要显式设计。

## 在现有流程中的落点

1. 路由器先选择 Inline/Compact/Full Spec 档位；不确定或风险扩大时单向升级。
2. `/brainstorm` 在需要设计探索时明确目标、边界和风险，避免循环朝错方向优化。
3. `/propose` 在持久化档位生成嵌入式 Goal Contract，说明完成信号、护栏、失败降级和沉淀位置。
4. `/apply` 按 task 执行，每轮记录 Loop Evidence：命令输出、日志、截图、review 结果或人工确认项。
5. `/review` 检查实现是否符合 spec，也检查 loop 是否可验证、可读、可停止。
6. `/fix` 和 `/fix-ci` 是局部修正循环，必须先定位观察信号，再做最小调参。
7. `/archive` 把有效的调参经验沉淀成 knowledge、rules、templates 或脚本检查。

## 不照搬的部分

Loop Engineering 不要求 Agent 自主接管所有决策，也不要求人类永远不写代码。本框架关注的是：让人类把模糊意图翻译成可验证目标、边界和降级策略，让 Agent 的执行进入可观察循环，让失败后的改进能沉淀到下一次循环。
