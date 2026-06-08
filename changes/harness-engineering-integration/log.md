# 变更日志：harness-engineering-integration

> 本文件记录变更过程中的关键决策、踩坑、和知识发现，供 /archive 时沉淀到 knowledge/。

---

## 变更信息

| 项 | 内容 |
|----|------|
| 变更名 | harness-engineering-integration |
| 档位 | Standard |
| 开始时间 | 2026-06-08 |
| 完成时间 | 2026-06-08 |
| 关联 Issue | 本线程用户确认，待补 GitHub Issue |
| commit 列表 | `edcfa3b docs(harness): integrate Harness Engineering workflow` |

---

## 过程记录

- 2026-06-08：用户确认按二审计划执行。
- 2026-06-08：先在 `scripts/check_framework.sh` 加 Harness marker 检查，运行后 RED，缺口为 `agents/copilot-prompt.md missing Harness markers: Harness, Agent 可见`。
- 2026-06-08：新增 `docs/harness-engineering.md`，并在 `AGENTS.md`、`README.md` 中只保留短入口，避免把索引文件扩成百科。
- 2026-06-08：更新 `agents/copilot-prompt.md`，将 Harness 纳入 /propose、/apply、/review、/archive。
- 2026-06-08：更新 spec、quick-card、test-spec 模板和两个 reviewer，将 Agent 可见证据、Agent 可验证性、Agent 可读性变成可审查字段。
- 2026-06-08：复跑 `bash scripts/check_framework.sh`，输出 `ai-code-copilot framework check passed`。
- 2026-06-08：目标达成审计发现 `AGENTS.md` 仍有旧口号，补充修正；同时给 `check_framework.sh` 增加 `AGENTS.md` 行数上限、Harness 文档索引和核心口号检查。
- 2026-06-08：再次运行 `bash scripts/check_framework.sh`，输出 `ai-code-copilot framework check passed`。
- 2026-06-08：本地提交 `edcfa3b docs(harness): integrate Harness Engineering workflow`。

---

## /finish 记录

| 项 | 内容 |
|----|------|
| 本地分支 | `codex/finish-workflow` |
| 验证命令 | `bash scripts/check_framework.sh` |
| 验证结果 | PASS，输出 `ai-code-copilot framework check passed` |
| 本地提交 | `edcfa3b docs(harness): integrate Harness Engineering workflow` |
| GitHub Issue | 未创建，`gh auth status` 显示 token invalid |
| Push | PASS，`git push -u origin codex/finish-workflow` 已推送远端分支 |
| PR | 未创建，`gh auth status` 仍显示 token invalid |

---

## 知识发现

- Harness Engineering 融入框架时，应优先落在模板、reviewer 和自检脚本中，避免停留在 README 概念说明。
- `AGENTS.md` 应继续作为知识地图，Harness 的细节放入 `docs/harness-engineering.md`，只在索引处短链。
- 对 Agent 友好的规则要尽量机械化，例如 marker 自检、模板字段和 reviewer 维度。

---

## /review 结论

### Spec Compliance（spec-reviewer）

**结论**：PASS

- F1 已实现：`docs/harness-engineering.md` 定义框架内 Harness Engineering，`AGENTS.md` 和 `README.md` 只保留短入口。
- F2 已实现：`agents/copilot-prompt.md` 将 Harness 纳入 /propose、/apply、/review、/archive。
- F3 已实现：`changes/templates/spec.md`、`quick-card.md`、`test-spec.md` 均包含 Agent Harness 字段。
- F4 已实现：`agents/spec-reviewer.md` 检查 Agent 可验证性，`agents/code-quality-reviewer.md` 检查 Agent 可读性。
- F5 已实现：`scripts/check_framework.sh` 检查 Harness markers、Harness 文档存在、AGENTS.md 短索引和核心口号。

### Code Quality（code-quality-reviewer）

**结论**：PASS

- 本次变更为 prompt、Markdown 模板、HTML 文案和 shell 自检脚本变更。
- `scripts/check_framework.sh` 使用既有 Python 自检块扩展 marker 检查，未引入新依赖。
- 未发现安全红线、状态流转、资金、权限或敏感日志风险。

### GitHub Readiness

**结论**：NEEDS_INFO

- 验证命令已记录：`bash scripts/check_framework.sh`。
- 缺口：当前变更记录为“本线程用户确认，待补 GitHub Issue”，尚无正式 GitHub Issue ID/URL。
- 处理方式：/finish 前需要创建或补录 Issue；若创建 PR，PR body 需包含 `Closes #ID`。

### Harness Readiness

**结论**：READY

- Agent 可见证据：`bash scripts/check_framework.sh` 输出 `ai-code-copilot framework check passed`。
- 失败自诊断入口：Harness markers 缺失会由 `scripts/check_framework.sh` 指向具体文件和缺失 marker。
- 不可见信息：OpenAI 内部真实 runtime 能力未实现，本次 spec 已明确列为非目标。
