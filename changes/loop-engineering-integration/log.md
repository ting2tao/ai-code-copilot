# 变更日志：loop-engineering-integration

## 变更信息

| 项 | 内容 |
|----|------|
| 变更名 | loop-engineering-integration |
| 档位 | Standard |
| Issue | https://github.com/ting2tao/ai-code-copilot/issues/28 |
| 开始时间 | 2026-06-15 |
| 完成时间 | 待完成 |
| 涉及文件数 | 20 |
| commit 列表 | 未提交 |

---

## 外部材料读取证据

- X：已读取用户提供的 `/Users/tsnowy/Downloads/tweet_2064127981161959567.json`。Addy Osmani 将 Loop Engineering 描述为由系统替代人工逐轮提示 Agent；核心构件包括 Automations、Worktrees、Skills、Plugins/connectors、Sub-agents，以及会话外 Memory；同时强调 token cost、verification、comprehension debt、cognitive surrender 等风险。
- 微信：已读取用户提供的 `/Users/tsnowy/Downloads/微信公众号文章.json`。文章强调 Loop Engineering 的核心不只是工具五件套，而是目标定义能力：机器可验证的完成标准、边界条件、失败降级方案、目标分层，并提醒 Goodhart 风险。

---

## 过程记录

- 2026-06-15：确认当前仓库无项目级 `.ai_code_copilot/`，框架自身使用根目录 `changes/` 管理变更。
- 2026-06-15：当前分支初始为 `main`，创建 `codex/loop-engineering-integration` 工作分支。
- 2026-06-15：确定本次采用 Standard 档，在 `changes/loop-engineering-integration/` 补齐 design/spec/tasks/test/log。
- 2026-06-15：新增 `docs/loop-engineering.md`，并将 Goal Contract / Loop Evidence 嵌入 prompt、reviewer、模板和自检脚本。
- 2026-06-15：读取用户提供的两个本地 JSON 原文，决定将设计从早期 7 项字段收敛为 5 项 Goal Contract：Goal、Done Signal、Guardrails、Fallback、Memory；Addy 的五件套作为可选 Loop Runtime。
- 2026-06-15：根据用户关于 DDD 的追问，采用 DDD-lite Domain Check：只在复杂业务触发，字段收敛为 Language、Boundary、Invariants、State Transitions、Owner，不强制完整 DDD 分层。

---

## Loop Evidence

| 项 | 内容 |
|----|------|
| Goal | 让 ai-code-copilot 显式具备简洁的 Loop Engineering |
| Done Signal | `bash scripts/check_framework.sh` PASS，Goal Contract markers 覆盖关键文件 |
| Guardrails | 不新增复杂 `/loop` 命令；Quick 不填 Runtime 五件套；不把无法验证内容当事实 |
| Fallback | 自检失败按缺失 marker 补齐；材料不可读时写入不可见信息 |
| Memory | `docs/loop-engineering.md`、模板字段、`scripts/check_framework.sh` |

---

## 知识发现

- Loop Engineering 与 Harness Engineering 的边界应明确：Harness 是 Agent 能看见和操作的环境，Loop 是在这个环境上运行的目标驱动反馈循环。
- Goal Contract 比早期 7 项字段更适合作为默认模板：Goal、Done Signal、Guardrails、Fallback、Memory 已覆盖目标定义、验证、防投机、降级和沉淀。
- Addy 的 Automations、Worktrees、Skills、Connectors、Sub-agents 应作为可选 Loop Runtime，而不是普通变更的默认填写项。
- DDD 适合以 Domain Check 进入框架，而不是作为默认架构范式；AI 最容易写错的是领域语言、业务边界、不变量和状态流转。

---

## Knowledge candidates

| Candidate | Scope | Suggested sink | Status |
|-----------|-------|----------------|--------|
| Goal Contract should include Goal, Done Signal, Guardrails, Fallback, Memory. | workflow templates | `changes/templates/*.md` | applied |
| Runtime five-piece should stay optional: Automation, Worktree, Skills/knowledge, Plugins/connectors, Maker-checker subagents. | advanced loop design | `docs/loop-engineering.md` | applied |
| Unreadable external sources must be recorded as invisible information. | research workflow | `knowledge/` or rules | pending |
| Domain Check should stay DDD-lite: Language, Boundary, Invariants, State Transitions, Owner. | complex business changes | `rules/domain-rules.md`, `changes/templates/spec.md` | applied |

---

## /review 结论

待执行。

---

## Verification log

### 2026-06-15 - framework self-check

```text
command: bash scripts/check_framework.sh
exit code: 0
output:
ai-code-copilot framework check passed
```

### 2026-06-15 - Loop marker search

```text
command: rg -n "Loop Engineering|Goal Contract|Loop Evidence" docs README.md README-CN.md AGENTS.md agents changes/templates scripts
exit code: 0
output:
输出覆盖 docs/loop-engineering.md、docs/harness-engineering.md、README.md、README-CN.md、AGENTS.md、agents/copilot-prompt.md、agents/spec-reviewer.md、agents/code-quality-reviewer.md、changes/templates/*.md、scripts/check_framework.sh。
```

### 2026-06-15 - Goal Contract refinement RED

```text
command: bash scripts/check_framework.sh
exit code: 1
output:
docs/loop-engineering.md missing Loop markers: Goal Contract, Done Signal, Guardrails, Fallback, Loop Runtime
```

### 2026-06-15 - Goal Contract refinement GREEN

```text
command: bash scripts/check_framework.sh
exit code: 0
output:
ai-code-copilot framework check passed
```

### 2026-06-15 - New marker coverage

```text
command: rg -n "Goal Contract|Done Signal|Guardrails|Fallback|Loop Runtime|Loop Evidence" docs README.md README-CN.md AGENTS.md agents changes/templates scripts
exit code: 0
output:
输出覆盖 AGENTS.md、README.md、README-CN.md、docs/loop-engineering.md、docs/harness-engineering.md、agents/copilot-prompt.md、agents/spec-reviewer.md、agents/code-quality-reviewer.md、changes/templates/*.md、scripts/check_framework.sh。
```

### 2026-06-15 - Old marker cleanup

```text
command: legacy 7-field marker cleanup search
exit code: 1
output:
无输出，核心入口已清理旧 7 项字段。
```

### 2026-06-15 - Domain Check RED

```text
command: bash scripts/check_framework.sh
exit code: 1
output:
rules/domain-rules.md missing Domain Check markers: Domain Check, Language, Boundary, Invariants, State Transitions, Owner
```

### 2026-06-15 - Domain Check marker coverage

```text
command: rg -n "Domain Check|Language|Boundary|Invariants|State Transitions|Owner|DDD-lite|领域复杂度" rules changes/templates agents scripts changes/loop-engineering-integration
exit code: 0
output:
输出覆盖 rules/domain-rules.md、changes/templates/spec.md、changes/templates/quick-card.md、agents/copilot-prompt.md、agents/spec-reviewer.md、agents/code-quality-reviewer.md、scripts/check_framework.sh 和本变更文档。
```

### 2026-06-15 - Domain Check GREEN

```text
command: bash scripts/check_framework.sh
exit code: 0
output:
ai-code-copilot framework check passed
```
