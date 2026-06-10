# Test Spec：context-management-enhancement

> **覆盖率门禁**：框架脚本自检，不适用代码覆盖率。

## P0 验收

- `bash scripts/check_framework.sh` 通过
- `bash -n hooks/session-start` 通过
- `bash -n scripts/init_project.sh` 通过

## P1 验收

- fixture 初始化后的 `.copilot-state.json` 包含 `projectContextSyncedAt`
- fixture 初始化后的 knowledge index 包含结构化 schema
- sync 不覆盖 project-owned config/project-context/domain-rules

## 无需测试项

- 不测试真实 Codex/Claude 客户端 hook 运行时，因为本仓库自检覆盖 hook 脚本语法和输出菜单一致性。

