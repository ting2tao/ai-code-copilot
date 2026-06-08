# 变更任务：harness-engineering-integration

> **关联 Spec**：`spec.md`
> **关联 Test Spec**：`test-spec.md`
> **零偏差原则**：Spec 是合同，tasks 是执行计划，不得擅自增删功能。

---

## Task 1：建立 Harness 自检红线

- [x] 修改 `scripts/check_framework.sh`，检查 prompt、reviewer、模板中的 Harness markers。
- [x] 运行 `bash scripts/check_framework.sh`，确认当前缺口可被检测。

## Task 2：补充 Harness 文档入口

- [x] 新增 `docs/harness-engineering.md`。
- [x] 更新 `AGENTS.md` 短索引。
- [x] 更新 `README.md` 简短介绍。

## Task 3：更新主提示词

- [x] 在核心法则中加入 `Context First, Harness Enables, Code Follows`。
- [x] 在 `/propose`、`/apply`、`/review`、`/archive` 中加入 Agent 可见能力、验证和沉淀要求。

## Task 4：更新模板与 reviewer

- [x] 更新 `changes/templates/spec.md`。
- [x] 更新 `changes/templates/quick-card.md`。
- [x] 更新 `changes/templates/test-spec.md`。
- [x] 更新 `agents/spec-reviewer.md`。
- [x] 更新 `agents/code-quality-reviewer.md`。

## Task 5：验证

- [x] 运行 `bash scripts/check_framework.sh`。
- [x] 记录最终验证输出。

## Task 6：目标达成审计补强

- [x] 修正 `AGENTS.md` 中残留的旧核心口号。
- [x] 在 `README.md` 增加 `docs/harness-engineering.md` 链接。
- [x] 在 `scripts/check_framework.sh` 增加 `AGENTS.md` 短索引和 Harness 文档索引检查。
- [x] 更新 `docs/ai-code-copilot-team-talk.html` 中的核心口号。
