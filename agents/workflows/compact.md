# Workflow Module: Compact SDD

Compact SDD 使用现有 `quick-card.md`，`recordMode: compact`。它适用于小型但需要持久化、commit、PR、跨会话或审计证据的变更。

## Required record

`quick-card.md` 必须包含 Goal、文件、Non-goals、Acceptance、Agent Harness、Goal Contract、风险/回滚、GitHub lifecycle、Execution/Commit/Review/Finish records。

新建 Quick Card 在既有 front matter 中写入最小 Artifact Chain metadata：`artifactVersion / artifactId / artifactType=quick-card / artifactStatus / sourceOfTruth / sourceRef / sourceRevision / upstream=none / upstreamHash=none`。repository 工作区记录使用 `sourceRef: self / sourceRevision: working-tree`，提交后更新为 `git:<sha>`。Compact 不为满足链路额外创建 design-brief/spec/tasks；Native 不强制落盘。无 metadata 的历史 Quick Card 保持 legacy 可读。

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
5. 同步 `artifactStatus`；状态变化必须符合 `workflow-policy.json.artifacts.statusTransitions`。
6. 发现 promotion trigger 时立即停止并升级，不得先写 full-only log。

## Compact -> Full Runtime promotion

超过 compact 边界、material Reverse Sync、Important/Critical correction、durable knowledge、open/accepted risk 或多个 review unit 时：

```text
stop edits -> create log.md and summary.md -> copy existing evidence from quick-card.md -> set recordMode: full -> recompute confirmation hash -> request confirmation if material -> resume
```

Quick Card 保留原始合同和 Promotion record。活动变更不得自动降级。
升级生成的 Full artifacts 必须引用 Quick Card 或新建的已确认 Full Spec，并固定真实 upstream hash；升级后运行 artifact checker，失败时不得恢复编辑。
