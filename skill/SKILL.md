---
name: ai-code-copilot
description: |
  Use when a user asks to 初始化项目/init/setup/分析工程结构, brainstorm/方案设计, 实现/开发/写代码/加功能, 优化/重构/refactor, 修 bug/debug, 修 CI/fix-ci, review/审查代码, finish/收尾/开PR, 写测试/TDD, archive/归档, or directly requests propose/apply/fix/fix-ci/review/finish/test/archive for a software project.
---

# ai-code-copilot

本 skill 激活后，先读取轻量 router：

> **REQUIRED:** 立即定位 ai-code-copilot 框架根目录并读取 `agents/router.md`，
> 再按 router 只读取当前意图和档位所需的 `agents/workflows/*.md`。读取前不要开始任务动作。
>
> 框架根目录定位顺序：
> 1. 当前 skill 目录的父目录（即 `skill/..`）
> 2. 环境变量 `AI_CODE_COPILOT_HOME`
> 3. Codex：`$CODEX_HOME/ai_code_copilot`、`~/.codex/ai_code_copilot`、`~/.Codex/ai_code_copilot`
> 4. Claude Code：`$CLAUDE_HOME/ai_code_copilot`、`~/.claude/ai_code_copilot`
>
> 找到后读取：`<框架根目录>/agents/router.md`。
>
> 若 `agents/router.md`、`config/workflow-policy.json` 或选中的 workflow module 缺失，回退读取
> `<框架根目录>/agents/copilot-prompt.md`，明确报告正在使用更严格的 legacy fallback，并建议升级框架；不得静默放宽门禁。

<HARD-GATE>
Inline SDD：仅当 policy 的全部低风险条件明确满足，且会话中已有 Goal/Scope/Done Signal/Verify 时允许编辑。
Compact SDD：必须先生成有效 quick-card.md；material contract change 必须确认后才执行。
Full SDD：必须有已确认 Spec；涉及资金/状态流转/权限/安全/生产风险时必须高亮提醒并等待人工确认。
不确定档位时使用 Compact；命中 full risk 时直接使用 Full。活动变更只允许 Inline -> Compact -> Full 或 Inline -> Full，不自动降级。
</HARD-GATE>
