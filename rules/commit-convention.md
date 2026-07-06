---
alwaysApply: true
---
# GitHub 协作与 Commit 规范

本规则不照抄用户输入的提交格式。用户给出的 Issue 名或 commit 示例可能不规范，AI 必须先归一化为 GitHub 可识别、社区通用、自动化工具友好的格式。
GitHub 指标统计口径见 `github-metrics.md`；本文件只定义协作、commit 和 PR 的基础门禁。

## 0. 规范来源与边界

### GitHub 官方可识别

- closing keyword 只允许在 PR body 中用于当前合同的工作票，固定写作 `Closes #<workIssue>`；合并到默认分支时关闭该 work Issue。
- `parentIssue` 只能使用 `Refs #<parentIssue>` 引用，不得使用任何 closing keyword。
- 当前合同不使用 `Fixes` 或 `Resolves`，也不允许用数字示例替代已解析的 `workIssue` 占位符。

### 社区通用规范

- commit message 使用 Conventional Commits，但本项目强制 scope：`type(scope): description`。
- 该格式利于 changelog、release note、语义化版本和自动化工具识别。

### 项目约定，不冒充 GitHub 官方标准

- "严禁无票开发"是本项目协作策略，不是 GitHub 官方强制。
- CodeQL 和 CI 是本项目 PR 门禁；仓库未配置时必须明示缺口。

## 1. 开工前门禁

### 必须

- 严禁无票开发只认 `workIssue` confirmed/resolved；只有 `parentIssue` 不够，父需求不能代替当前变更的工作票。
- 所有代码、规则、配置、脚本、测试、文档变更都必须关联唯一 work Issue。
- Standard/Complex 变更必须在 `spec.md` 写明 `parentIssue`、`workIssue`、`issueRelationship`、`closeTarget` 和 branch。
- Quick 变更必须在 `quick-card.md` 写明同一组合同字段。
- `tasks.md` 的 Preflight 必须确认 `workIssue` 已解析、open、可读且属于当前仓库，`issueRelationship` 为 `sub-issue` 或 `standalone`，`closeTarget: workIssue`。
- 当前分支不得是 `master` 或 `main`。

### Issue 生命周期

- `parentIssue` 表示整体需求，可为 `none`；`workIssue` 表示本次已确认合同的唯一执行单元。
- 用户确认合同后，框架从合同自动创建并立即记录唯一 `workIssue`；已有 resolved workIssue 必须先验证后复用，不得重复创建。
- 有 parent 时，work Issue 必须成为 GitHub native sub-issue；无 parent 时记录 `issueRelationship: standalone`。
- native 关联失败时保留原 work Issue，记录 `issueRelationship: pending` 并阻塞开发；禁止为绕过关联错误新建替代 Issue。
- `workIssue` resolved 且关系验证成功后，才能由合同 derive `type/scope` 并创建或校验分支。
- 紧急修复也不能空缺 work Issue；可以自动创建故障/Hotfix work Issue，但必须先确认合同并持久化。

## 2. 分支管理

### 必须

- 禁止在 `master` 或 `main` 分支直接开发或提交。
- 分支名称必须使用 `type/scope`。
- type 仅允许：`feat`、`fix`、`docs`、`refactor`、`test`、`chore`、`perf`、`ci`、`build`。
- scope 必须是描述模块或能力的小写 kebab-case；Issue 编号不是 scope。
- 分支冲突时停止并询问复用或人工处理，禁止静默添加时间戳。
- 分支必须与当前 `workIssue` 的 confirmed contract 派生出的 `type/scope` 一致；`parentIssue` 不参与 branch scope，也不能作为开工凭据。

## 3. Commit Message

### 必须

- commit subject 必须使用 `type(scope): description`，scope 不可省略。
- type 仅允许：`feat`、`fix`、`docs`、`refactor`、`test`、`chore`、`perf`、`ci`、`build`。
- scope 必须是描述模块或能力的小写 kebab-case；Issue 编号不是 scope。
- description 必须说明实际变更，不添加 `[issue-123]` 等前缀。
- 不要使用用户随手输入的非标准前缀，例如 `[issue-7-org-keyword-search] fix: ...`。
- 不要把 Issue ID 当作 scope。
- 每个 task/fix 原则上一 task 一 commit。
- commit 归属于当前 `workIssue` 和已记录 branch 合同；`parentIssue` 只保留需求追踪语义，不作为 commit 的 close target。
- commit 前必须执行 `project-context.md` 中记录的编译/测试/检查命令。
- commit 后必须把 commit hash 和完整 message 写入 `tasks.md` 或 `log.md`，作为 `/review` 的提交证据。

### type

- `feat`：新功能
- `fix`：缺陷修复
- `docs`：文档、规则、提示词、模板
- `refactor`：重构
- `test`：测试
- `chore`：维护性改动
- `perf`：性能优化
- `ci`：CI 配置
- `build`：构建系统或依赖

### scope

- scope 使用模块、领域或能力名，例如 `search`、`org-search`、`coupon`、`workflow`、`git-contract`。
- scope 应保持短、稳定、可复用。
- scope 必须是小写 kebab-case，只允许小写字母、数字和连字符。

### Issue 关联

- 简单关联可放在 description 末尾，编号必须是 `workIssue`。
- 自动关闭语义只放在 PR body：`Closes #<workIssue>`。
- parentIssue 非 none 时，PR body 另加 `Refs #<parentIssue>`；parent 永远不用 `Closes`、`Fixes` 或 `Resolves`。
- commit body/footer 可使用 `Refs #<workIssue>` 表示关联但不自动关闭；不在 commit 中提前关闭 Issue。

### 推荐示例

- `feat(org-search): 支持按组织名称查询服务范围 (#7)`
- `fix(header): 修复移动端导航遮挡问题 (#456)`
- `docs(git): 补充 commit message 规范`
- `ci(codeql): 启用 CodeQL 静态扫描`

### 不推荐示例

- `[issue-7-org-keyword-search] fix: 支持按组织名称查询服务范围`
- `[add-coupon] 新增 issueCoupon 核心逻辑`
- `fix: issue-7-org-keyword-search`
- `feat: missing scope`
- `feat(Issue): bad scope`

## 4. PR 与自动化审查

### 必须

- PR 必须关联合同中已经 resolved 的 `workIssue`。
- PR body 必须使用 `Closes #<workIssue>`；`closeTarget` 必须为 workIssue。
- `parentIssue` 非 none 时必须添加 `Refs #<parentIssue>`，不得使用 closing keyword。
- PR 必须列出验证命令和实际结果，不能只写"已测试"。
- 提交 PR 时必须触发：
  - CodeQL 静态审查
  - CI 编译/测试自动化审查

### 例外处理

- 如果仓库未配置 CodeQL 或 CI，必须在 PR 中明确标明缺口。
- 自动化审查缺失时，不得静默合并；必须补齐配置或获得人工确认。
- 如果 PR 只包含非代码文档，也仍应关联 Issue，并说明不需要编译验证的原因。

## 5. 归一化示例

用户输入：

```text
[issue-7-org-keyword-search] fix: 按组织名称查询服务范围
```

应归一化为：

```text
fix(org-search): 支持按组织名称查询服务范围 (#7)
```

PR body 应包含：

```text
Closes #<workIssue>
Refs #<parentIssue>
```

## 6. 快速检查清单

- [ ] confirmed/resolved `workIssue` 与可选 `parentIssue` 已写入 `spec.md` 或 `quick-card.md`
- [ ] `issueRelationship` 已验证为 `sub-issue` 或 `standalone`，`closeTarget: workIssue`
- [ ] 当前分支不是 `master`/`main`，且符合 `type/scope`
- [ ] commit message 符合 `type(scope): description`
- [ ] commit hash 和 message 已写入 `tasks.md` 或 `log.md`
- [ ] PR body 使用 `Closes #<workIssue>`，parent 非 none 时只使用 `Refs #<parentIssue>`
- [ ] PR 触发 CodeQL 和 CI；若缺失，PR 已明示缺口
- [ ] PR 描述列出验证命令和实际结果
