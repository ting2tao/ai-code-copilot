# Workflow Module: Compact SDD

Compact SDD 使用现有 `quick-card.md`，`recordMode: compact`。它适用于小型但需要持久化、commit、PR、跨会话或审计证据的变更。

## Required record

`quick-card.md` 必须包含 Goal、文件、Non-goals、Acceptance、Agent Harness、Goal Contract、风险/回滚、GitHub lifecycle、Execution/Commit/Review/Finish records。

新提案写 `promotedFrom: none`；从原生执行升级写 `promotedFrom: native`。

## Issue lifecycle

```text
always     -> resolve workIssue before implementation
on-commit  -> local edits allowed; resolve workIssue before first commit
on-publish -> local edits and commits allowed; resolve workIssue before push/PR
manual     -> never auto-create; validate supplied Issue when present
missing    -> invalid configuration; stop and report
```

已有 open work Issue 必须校验后复用；创建或关联部分成功后不得另建替代 Issue。任何已解析 Issue 都保持 `closeTarget=workIssue`，parent 只追踪整体需求。

## Native -> Compact

严格顺序：

```text
stop edits -> capture Native contract/diff/evidence -> create quick-card.md -> copy evidence -> set promotedFrom: native and recordMode: compact -> recompute hash -> confirm material changes only -> resume
```

已有成功命令不为补文档而重复运行；复制时必须保留 command、exit code 和真实 output summary。若 Goal、Scope、Acceptance、Guardrails、风险或外部动作发生实质变化，等待确认；纯路径、符号、命令修正可机械 Reverse Sync 并记录。

## Apply

1. 完整读取 Quick Card 与相关项目规则。
2. 校验当前分支、Issue lifecycle policy、目标路径、验证命令和用户无关改动。
3. 单目的执行；每步把实际验证写入 Execution record。
4. 在 `issuePolicy` 要求的生命周期门禁前解析/校验 work Issue，并在 commit 后记录精确 hash/message。
5. 发现 promotion trigger 时立即停止并升级，不得先写 full-only log。

## Compact -> Full Runtime promotion

超过 compact 边界、material Reverse Sync、Important/Critical correction、durable knowledge、open/accepted risk 或多个 review unit 时：

```text
stop edits -> create log.md and summary.md -> copy existing evidence from quick-card.md -> set recordMode: full -> recompute confirmation hash -> request confirmation if material -> resume
```

Quick Card 保留原始合同和 Promotion record。活动变更不得自动降级。
