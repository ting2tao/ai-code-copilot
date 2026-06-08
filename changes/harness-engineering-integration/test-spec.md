# 测试 Spec：harness-engineering-integration

> **关联 Spec**：`spec.md`
> **Red/Green 铁律**：自检脚本先因 Harness markers 缺失失败，再补齐字段使其通过。

---

## P0 核心逻辑测试（必测）

### TC-P0-01：Harness markers 自检

**模块**：`scripts`
**测试文件**：`scripts/check_framework.sh`
**测试目标**：框架自检能发现 prompt、reviewer、模板缺少 Harness 字段。
**前置条件**：先添加 marker 检查，但不修改目标文档。
**操作**：运行 `bash scripts/check_framework.sh`
**预期结果**：RED 阶段失败并指出缺失 Harness markers；GREEN 阶段通过。
**RED 证据**：`agents/copilot-prompt.md missing Harness markers: Harness, Agent 可见`
**GREEN 证据**：`bash scripts/check_framework.sh` 输出 `ai-code-copilot framework check passed`

---

## 不测试项

| 项目 | 原因 | 风险接受人/确认方式 |
|------|------|-------------------|
| LogQL/PromQL/CDP adapter | 本次只建立框架约束，不实现外部工具接入 | 用户确认 |

---

## 实际测试结果

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `bash scripts/check_framework.sh` | RED | `agents/copilot-prompt.md missing Harness markers: Harness, Agent 可见` |
| `bash scripts/check_framework.sh` | GREEN | `ai-code-copilot framework check passed` |
| `bash scripts/check_framework.sh` | GREEN | 目标达成审计补强后再次输出 `ai-code-copilot framework check passed` |
