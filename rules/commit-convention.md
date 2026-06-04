---
alwaysApply: true
---
# Git 提交与开发标准流

本规则约束 Issue、分支、commit 和 PR。任何代码变更都必须能从 Issue 追踪到分支、提交、PR 和验证结果。

## 1. Issue 依赖

- 严禁无票开发；所有代码变更必须关联一个 Issue。
- Standard/Complex 变更必须在 `spec.md` 写明 Issue ID 或 URL。
- Quick 变更必须在 `quick-card.md` 写明 Issue ID 或 URL。
- 没有关联 Issue 时，必须先停止并提示用户补充 Issue；不要继续编码。

## 2. 分支管理

- 推荐一个 Issue 对应一个开发分支。
- 分支命名推荐：`<type>/<description>-<IssueID>`。
- 示例：`feature/login-123`、`fix/header-456`、`docs/workflow-789`。
- 禁止在 `master` 或 `main` 分支直接开发或提交。

## 3. Commit Message

- 使用 Conventional Commits：`<type>[optional scope]: <description>`。
- 常用 type：
  - `feat`：新功能
  - `fix`：缺陷修复
  - `docs`：文档变更
  - `refactor`：重构
  - `test`：测试
  - `chore`：杂项维护
  - `perf`：性能优化
  - `ci`：CI 配置
  - `build`：构建系统或依赖
- scope 使用模块或能力名，例如 `search`、`org-search`、`coupon`、`workflow`。
- 不要把 `[issue-xxx]` 放在 commit message 前缀；这不属于 Conventional Commits 标准，可能影响 changelog/release 工具识别。
- 关联 Issue 时，优先使用：
  - `fix(org-search): 支持按组织名称查询服务范围 (#7)`
  - 或在 commit body / PR body 写 `Refs #7`
- 每次 commit 后，必须把 commit hash 和完整 message 写入 `tasks.md` 或 `log.md`，作为 `/review` 的提交证据。

## 4. PR 与自动化审查

- PR 必须关联对应 Issue ID，并使用 `Closes #ID` 关键字。
- 提交 PR 时必须触发 CodeQL 静态审查与 CI 编译自动化审查。
- 若仓库未配置 CodeQL 或 CI，必须在 PR 中标明缺口，并在合并前补齐或获得人工确认。
- PR 描述必须列出验证命令和实际结果，不能只写"已测试"。

## 5. AI 辅助开发

- 鼓励使用云端 Copilot 或本地 AI 助手提升效率。
- AI 生成的代码仍必须遵守本规则中的 Issue、分支、commit、PR 和验证门禁。
- AI 不得绕过人工确认、CodeQL、CI 或项目已有 review 流程。
