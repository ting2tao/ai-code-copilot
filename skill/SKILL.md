---
name: ai-code-copilot
description: |
  Use for explicit ai-code-copilot lifecycle requests such as 初始化项目/init/sync/upgrade,
  brainstorm/propose/apply/fix-ci/review/finish/publish/test/archive, or when the model detects
  security, permission, money, production, deployment, database, public-contract, persistent,
  audit, or cross-session risk. Do not use for ordinary low-risk implementation, debugging,
  refactoring, tests, documentation, discussion, or read-only analysis; handle those natively
  unless material risk or uncertainty appears.
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
> 若 `agents/router.md`、`config/workflow-policy.json` 或选中的 workflow module 缺失，停止执行并建议升级框架；不得回退加载单体提示词或静默放宽门禁。

<HARD-GATE>
Native path：普通、边界明确、低风险且可直接验证的任务不激活本 skill。
Compact SDD：需要持久化的工作必须先生成有效 quick-card.md；material contract change 必须确认后才执行。
Full SDD：material risk 必须有已确认 Spec；涉及资金/状态流转/权限/安全/生产风险时必须高亮提醒并等待人工确认。
Native 工作需要持久化时进入 Compact，发现 material risk 时直接进入 Full；Compact 只允许升级到 Full，不自动降级。
</HARD-GATE>
