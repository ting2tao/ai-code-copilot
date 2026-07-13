---
alwaysApply: true
---
# GitHub 指标统计口径

本规则定义项目侧如何留下 GitHub 可统计信号。最终统计由 GitHub、GitHub API、GraphQL 或 GitHub Actions 完成；AI 不手工编造指标。

## 1. 目标

- 让 Issue、PR、commit、CI run、review 和测试变更具备稳定、可查询、可归因的数据结构。
- 避免通过拆 commit、堆低质量测试、关闭低价值 Issue 或水对话来刷指标。
- 指标只作为研发质量和 AI 协作成熟度诊断，不作为单一排名依据。

## 2. Issue Labels

建议仓库维护以下 label 体系：

- `type:feature`
- `type:bug`
- `type:docs`
- `type:refactor`
- `type:test`
- `type:chore`
- `priority:p0`
- `priority:p1`
- `priority:p2`
- `size:xs`
- `size:s`
- `size:m`
- `size:l`
- `source:ai-assisted`
- `source:human-only`

关闭 Issue 数量统计时，应按 type、priority、size 分组或加权。取消、不做、重复、迁移类 Issue 不应计入有效完成量。

### Work closure 与 parent progress

- 统计必须记录 `issuePolicy`（`always`、`on-commit`、`on-publish`、`manual`）；缺失配置单列为 legacy `always`，避免把生命周期差异误判为流程失败。
- `workIssue` 是一个已确认变更的交付单元；其 closure/关闭由合并 PR 中的 `Closes #<workIssue>` 统计。
- `parentIssue` 是整体需求；work Issue closure/关闭与 parent requirement progress 必须分开统计，后者按 native sub-issue 的完成数/总数和 acceptance checklist 进度计算。
- 有 work Issue 的变更中，`closeTarget` 必须固定为 `workIssue`；manual/no-Issue 使用 `closeTarget: none`。`parentIssue` 只能用 `Refs #<parentIssue>` 关联，不能因单个变更合并而自动关闭。
- `issueRelationship: sub-issue` 必须由 GitHub native relationship 验证；`standalone` 单独统计，`pending` 不计为可开工或可完成样本。
- 同一 confirmed contract 重复创建的 Issue 不得计入产出；应标记 duplicate 并调查流程违规。
- `manual` 且未提供 Issue 的交付不得伪造 closure 数据；应单独统计为 explicit no-Issue，而不是计入重复票或流程失败。

## 3. PR Body 必填信号

PR body 应使用 `.github/PULL_REQUEST_TEMPLATE.md`，至少包含：

- `Closes #<workIssue>`
- parentIssue 非 none 时的 `Refs #<parentIssue>`
- Change Type
- Test Evidence
- Risk
- AI Collaboration
- CI / CodeQL 状态

PR body 缺失这些字段时，`/review` 的 GitHub Readiness 应标记为 `NEEDS_INFO`。

## 4. Test-to-Code Ratio 口径

统计公式：

```text
Test-to-Code Ratio = 新增或修改测试代码有效行数 / 新增或修改业务逻辑有效行数
```

测试文件识别：

- Go：`*_test.go`
- TypeScript / JavaScript：`*.test.ts`、`*.test.tsx`、`*.spec.ts`、`*.spec.tsx`、`*.test.js`、`*.spec.js`
- Java：`src/test/**`
- Python：`tests/**`、`test_*.py`、`*_test.py`

业务逻辑代码排除：

- 测试文件
- generated / vendor / dist / build 目录
- lock files
- snapshot
- fixture 大数据文件
- 纯格式化或 import 重排

缺陷修复 PR 必须新增或更新回归测试；若无需测试，PR body 必须说明原因。

## 5. PR Size 与 Churn 风险

建议 GitHub Action 对 PR size 给出 warning：

- 有效变更文件数 > 20
- 有效变更行数 > 500

warning 不自动阻塞，但 `/review` 应提示拆分风险。统计 Code Churn 时应排除：

- 产品需求变化导致的后续迭代
- 文件重命名
- 大规模格式化
- generated/vendor/lock/snapshot
- 依赖升级引发的机械修改

## 6. CI 自愈口径

CI 修复不依赖特殊前缀如 `[AI-Gen]`。推荐由 GitHub 统计：

- workflow run failed 时间
- 同一 PR 下一次 workflow success 时间
- 中间修复 commit
- 修复 commit 是否与失败 job 相关

当用户触发 `/fix-ci` 时，AI 必须在 `log.md` 记录失败类型、失败命令、根因、修复摘要、验证命令和 commit。commit message 使用：

- `fix(ci): <中文简述>`
- `fix(test): <中文简述>`
- `ci(<scope>): <中文简述>`

## 7. GitHub Readiness 检查

`/review` 完成 Spec Compliance 和 Code Quality 后，必须检查：

- [ ] `workIssue` ID/URL 已记录、`closeTarget: workIssue` 且 PR 使用 `Closes #<workIssue>`；或 manual/no-Issue 已记录三个 `none` 且无 closing keyword
- [ ] parentIssue 非 none 时只使用 `Refs #<parentIssue>`，parent progress 与 work closure 分开统计
- [ ] Issue 具备 type / priority / size labels，或 PR 中说明暂缺
- [ ] PR body 填写 Change Type
- [ ] PR body 填写 Test Evidence，包含验证命令和实际结果
- [ ] PR body 填写 Risk
- [ ] PR body 填写 AI Collaboration
- [ ] CI 和 CodeQL 已触发；若缺失，PR 已明示缺口
- [ ] 若 CI 曾失败，已有 `/fix-ci` 或等效修复记录
- [ ] PR size 未超过 warning 阈值，或已说明拆分/不拆分原因

结论写入 `log.md ## /review 结论`：

- `GitHub Readiness：READY`
- `GitHub Readiness：NEEDS_INFO`，并列出缺失字段
