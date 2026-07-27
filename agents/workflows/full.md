# Workflow Module: Full SDD

Full SDD 用于高风险、跨模块、超过五文件、多目标或需要完整审计的变更。

## Issue lifecycle

```text
always     -> resolve workIssue before implementation
on-commit  -> local edits allowed; resolve workIssue before first commit
on-publish -> local edits and commits allowed; resolve workIssue before push/PR
manual     -> never auto-create; validate supplied Issue when present
missing    -> invalid configuration; stop and report
```

全量记录从提案开始保存 Issue 状态，但只在策略门禁到达时执行创建。已存在的 open work Issue 必须复用；部分成功后不得创建替代票；有 work Issue 时 `closeTarget` 为 workIssue，manual/no-Issue 时为 none，parent 永不由子变更关闭。

## Record set

- `design-brief.md`: 需求理解、现状、2-3 方案、风险、YAGNI 和确认。
- `spec.md`: Goal Contract、行为、范围、Non-goals、Acceptance、Harness、Domain Check。
- `tasks.md`: 精确文件、符号、依赖顺序、验证和 commit 单元。
- `test-spec.md`: P0/P1/P2、无需测试项、命令和可见证据。
- `log.md`: 决策、失败、验证、review、knowledge candidates。
- `summary.md`: 不超过约定预算的 active change 摘要。
- `roadmap.md`: Complex 子变更依赖、集成顺序和上游 summary。

## brainstorm

读取项目现状和可用 Harness；一次只问一个问题；给 2-3 方案和推荐；逐段确认需求、方案、风险；生成 design brief。涉及父 Issue 时先读整体需求和已完成 sibling。

## propose

从已确认设计和真实代码生成完整记录。Goal Contract 是 Spec 首部：Goal、Done Signal、Guardrails、Fallback、Memory，不再创建独立文档。Harness 从 Acceptance/Done Signal/Guardrails/Fallback 派生。复杂领域补充 Language、Boundary、Invariants、State Transitions、Owner。

## apply

1. 校验 Spec 确认、hash、Issue policy、branch、dirty worktree 和所有目标路径。
2. 按 tasks 原子执行；行为变更采用 Red/Green。
3. 每个 task 运行验证并写 command、exit code、output summary。
4. 遇到 Spec 与现实不符先 Reverse Sync。
5. mechanical Reverse Sync 自动记录；material Reverse Sync 停止并重新确认。
6. commit message 使用 `type(scope): description`，并立即写入记录源。

## Native -> Full

原生调查直接发现 full risk 时跳过 Compact：停止编辑，生成完整记录，复制 Native contract/diff/evidence，标记 promotion provenance，等待 material confirmation 后继续。
