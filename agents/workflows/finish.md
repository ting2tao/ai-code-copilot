# Workflow Module: finish / commit / publish

读取项目 `.ai_code_copilot/config.json`。`issuePolicy` 缺失时使用 legacy default `always`；允许 `always / on-commit / on-publish / manual`。`finishMode` 只控制 PR handoff。

## Issue lifecycle

```text
always:     implementation 前解析或复用 workIssue
on-commit:  可本地编辑；首次 commit 前解析或复用 workIssue
on-publish: 可本地编辑和 commit；push/PR 前解析或复用 workIssue
manual:     不自动创建；提供 Issue 时校验
```

Issue 创建成功后立即持久化。parent 存在时建立 native sub-issue；无 parent 时 standalone。关联失败保留原 work Issue 并阻塞所需阶段，不得创建替代 Issue。

## Commit gate

- Inline 请求 commit 时先 `Inline -> Compact`。
- 分支遵循项目合同；commit 使用 `type(scope): description`。
- `on-commit`/`always` 必须在 commit 前解析 Issue；`on-publish` 可延后。
- 记录实际 hash 和完整 message。

## Publish gate

1. 工作区无无关变更，当前分支与合同一致。
2. Spec/Quick review PASS，有新鲜 final validation。
3. 除 `manual` 且未提供 Issue 外，work Issue 必须 open、可读、同仓库、关系已解决。
4. PR body 只用 `Closes #<workIssue>`；parent 只用 `Refs #<parentIssue>`，永不关闭 parent。
5. `finishMode=ask` 等待确认；`auto-pr` 执行 push/PR；`manual` 只输出命令和 body。
6. 将 PR URL、base、remote、验证和 closing statement 写回当前记录源。
