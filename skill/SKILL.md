---
name: ai-code-copilot
description: |
  AI 编码协作助手，基于 Spec 驱动 + 渐进式复杂度框架。
  完全独立，无需外部依赖。
  
  触发场景——以下任何情况都应调用本 skill：
  - 先讨论一下/brainstorm/帮我分析方案/设计探索/方案对比 → /brainstorm 设计探索
  - 帮我实现/开发/写代码/做需求/加功能/加接口 → /brainstorm + /propose + /apply 流程
  - 优化/重构/refactor/改造/调整代码/分层/把逻辑移到/迁移到service → /brainstorm + /propose + /apply 流程
  - 代码不合理/controller太胖/service层缺失/逻辑放错地方了 → /brainstorm + /propose + /apply 流程
  - 帮我修 bug/排查问题/报错了/不工作了/调试/debug → 四阶段系统调试
  - 帮我 review/审查/检查代码/看一下代码 → /review 两阶段 Sub-Agent
  - 写测试/单测/补测试/跑测试/测覆盖率/TDD → /test 流程
  - 归档/archive/沉淀知识/整理变更 → /archive 知识飞轮
  - 初始化项目/分析工程结构/setup → init 流程
  - 直接说出流程名：「init」「brainstorm」「propose」「apply」「fix」「review」「test」「archive」
  - 给一个 Java 类名/方法名 + 操作描述（如 XxxController#method 优化/重构/调整）→ brainstorm + propose 流程
---

# ai-code-copilot

本 skill 激活后，读取完整提示词：

> **REQUIRED:** 立即定位 ai-code-copilot 框架根目录并读取 `agents/copilot-prompt.md`，
> 按其中的指令运作。读取前不要输出任何内容，不要开始任何任务。
>
> 框架根目录定位顺序：
> 1. 当前 skill 目录的父目录（即 `skill/..`）
> 2. 环境变量 `AI_CODE_COPILOT_HOME`
> 3. Codex：`$CODEX_HOME/ai_code_copilot`、`~/.codex/ai_code_copilot`、`~/.Codex/ai_code_copilot`
> 4. Claude Code：`$CLAUDE_HOME/ai_code_copilot`、`~/.claude/ai_code_copilot`
>
> 找到后读取：`<框架根目录>/agents/copilot-prompt.md`。

<HARD-GATE>
Standard/Complex 档：/propose 未完成且用户未确认前，禁止任何编码动作。
Quick 档：必须先生成 quick-card.md（目标/文件/非目标/验收/风险），用户确认后才执行。
任何档位：涉及资金/状态流转/权限变更，必须 ⚠️ 高亮提醒，等待人工确认后才能继续。
不确定档位时，默认走 Standard。
</HARD-GATE>
