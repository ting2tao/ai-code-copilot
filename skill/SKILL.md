---
name: ai-code-copilot
description: |
  Use when a user asks to 初始化项目/init/setup/分析工程结构, brainstorm/方案设计, 实现/开发/写代码/加功能, 优化/重构/refactor, 修 bug/debug, 修 CI/fix-ci, review/审查代码, 写测试/TDD, archive/归档, or directly requests propose/apply/fix/fix-ci/review/test/archive for a software project. Applies to Java, Go, Python, frontend, and monorepo projects.
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
