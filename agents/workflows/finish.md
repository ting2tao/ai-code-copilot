# Workflow Module: finish / commit / publish

读取项目 `.ai_code_copilot/config.json`。`issuePolicy` 必须存在且为 `always / on-commit / on-publish / manual` 之一；缺失或非法时停止，不做兼容推断。`finishMode` 只控制 PR handoff。

## Issue lifecycle

```text
always     -> resolve workIssue before implementation
on-commit  -> local edits allowed; resolve workIssue before first commit
on-publish -> local edits and commits allowed; resolve workIssue before push/PR
manual     -> never auto-create; validate supplied Issue when present
missing    -> invalid configuration; stop and report
```

Issue 创建成功后立即持久化。已有 open Issue 先校验再复用；parent 存在时建立 native sub-issue；无 parent 时 standalone。关联失败保留原 work Issue 并阻塞所需阶段，不得创建替代 Issue。任何已解析 Issue 都保持 `closeTarget=workIssue`。

`manual` 且未提供 Issue 时，在当前记录源写 `workIssue: none`、`issueRelationship: none`、`closeTarget: none`。这不是把 parent 升格为工作票；publish 时省略所有 closing keyword，parent 如存在仍只用 `Refs #<parentIssue>`。

## Commit gate

- 原生执行请求 commit 时先自动激活并执行 `Native -> Compact`。
- 分支遵循项目合同；commit 使用 `type(scope): description`。
- `on-commit`/`always` 必须在 commit 前解析 Issue；`on-publish` 可延后。
- 记录实际 hash 和完整 message。

## Publish gate

1. 工作区无无关变更，当前分支与合同一致。
2. Spec/Quick review PASS，有新鲜 final validation。
3. 除 `manual` 且未提供 Issue 外，work Issue 必须 open、可读、同仓库、关系已解决。
4. 有 work Issue 时，PR body 只用 `Closes #<workIssue>`；`manual`/no-Issue 时省略 closing keyword。parent 始终只用 `Refs #<parentIssue>`，永不关闭 parent。
5. `finishMode=ask` 等待确认；`auto-pr` 执行 push/PR；`manual` 只输出命令和 body。
6. 将 PR URL、base、remote、验证和 closing statement 写回当前记录源。
