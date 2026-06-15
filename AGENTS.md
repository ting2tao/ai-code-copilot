# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 项目简介

ai-code-copilot 是一个面向多技术栈软件项目的 AI 编码协作框架（Codex skill，兼容 Claude Code）。它不是一个可运行的应用，而是一套部署到 `~/.codex/ai_code_copilot/`（Codex）或 `~/.claude/ai_code_copilot/`（Claude Code）的提示词、规则、Agent 和安装脚本。核心理念：**Context First, Harness Enables, Code Follows.** AI 让代码更容易生成，ai-code-copilot 通过 Spec 驱动的流程（brainstorm → propose → apply → review → archive）和 Harness 反馈循环，让上下文变得明确、可审查、可复用，确保 AI 在正确的上下文里做正确的事。

## 架构：两层结构

**全局层**（安装后默认位于 `~/.codex/ai_code_copilot/`）— 框架运行主体：
- `skill/SKILL.md` — Codex skill 注册入口，定义触发条件
- `agents/copilot-prompt.md` — 主提示词，定义所有命令逻辑、流程控制、硬性门控
- `agents/spec-reviewer.md` / `agents/code-quality-reviewer.md` — 双阶段审查的 Sub-Agent
- `hooks/session-start` — 会话启动时通过 `hookSpecificOutput` 注入安全规则
- `hooks/hooks.json` — hook 注册配置
- `scripts/init_project.sh` — 脚本化 `/init` 和 `--sync`
- `scripts/check_framework.sh` — 框架完整性自检
- `tests/fixtures/` — Java/Go/Python/Frontend/Monorepo 的初始化检测样例
- `rules/` — 跨语言通用规则（协作、安全、领域、项目上下文占位）
- `knowledge/` — 知识库（由 `/archive` 沉淀积累）
- `docs/harness-engineering.md` — Harness Engineering 方法论在本框架中的定义
- `docs/loop-engineering.md` — Loop Engineering 方法论在本框架中的定义
- `changes/templates/` — 变更文档模板（spec、tasks、test-spec、log、design-brief、quick-card、roadmap）
- `packs/` — 技术栈规则包，`/init` 时自动检测加载；Java/Go/Python/Frontend 规则都放在各自 pack 中

**项目层**（`/init` 后在业务项目中生成 `<project>/.ai_code_copilot/`）：
- `rules/project-context.md` — 自动检测的技术栈、构建命令、分层架构
- `rules/coding-style.md` — 项目级编码规范（覆盖全局）
- `rules/commit-convention.md` — Issue、分支、commit message、PR 与自动化审查规范
- `rules/domain-rules.md` — 业务约束（用户手动填写）
- `changes/<变更名>/` — 活跃变更目录，含 design-brief/spec/tasks/test-spec/quick-card/roadmap/log

## 修改框架时的关键文件

- `agents/copilot-prompt.md` — 所有命令逻辑、流程控制、硬性门控
- `skill/SKILL.md` — 触发条件和 skill 描述
- `hooks/session-start` — 会话启动注入的安全规则
- `scripts/*.sh` — 初始化、同步和框架自检
- `tests/fixtures/**` — pack 检测与脚本自检样例
- `rules/*.md` — 跨语言 core 规则和占位模板
- `packs/*/pack.md`、`packs/*/rules/*.md` — 技术栈检测、命令和专用编码规则
- `changes/templates/*.md` — 变更文档模板

## README 维护

- `README.md` 是默认英文文档，`README-CN.md` 是中文文档；修改任一 README 内容时，必须同步更新另一份。

## 安装脚本

- `install.sh` — macOS/Linux：clone 到 `~/.codex/ai_code_copilot/`，创建 skill symlink，注册 SessionStart hook
- `install.ps1` — Windows PowerShell：使用目录 Junction 替代 symlink
- `install-wsl.sh` — WSL 变体

## 核心设计原则

- **No Spec/Quick Card, No Code** — Standard/Complex 没有 spec 不准写代码；Quick 没有 quick-card 不准写代码
- **渐进式复杂度** — Quick（≤1天，<5文件）/ Standard / Complex（>5天，跨3+模块）
- **Evidence Before Claims** — 每个 task 完成必须展示可验证的命令输出
- **Harness Enables** — 规格、测试、日志、review、规则和知识沉淀共同构成 Agent 可见反馈循环
- **Loop Engineering** — 每个变更都要声明简洁的 Goal Contract：Goal、Done Signal、Guardrails、Fallback、Memory
- **DDD-lite Domain Check** — 复杂业务才记录 Language、Boundary、Invariants、State Transitions、Owner，不强制完整 DDD 结构
- **双阶段审查** — Spec Compliance（是否按 spec 实现）+ Code Quality（代码质量）
- **知识飞轮** — `/archive` 将经验沉淀到 `knowledge/`，下次自动加载
- **安全红线** — 硬编码密钥、日志打印敏感信息、资金/权限变更必须人工确认

## 命令速查

所有命令定义在 `agents/copilot-prompt.md` 中：

| 命令 | 用途 |
|------|------|
| `/init` | 检测技术栈，创建项目级 `.ai_code_copilot/` |
| `/brainstorm` | 苏格拉底式设计探索，输出 `design-brief.md` |
| `/propose` | Standard/Complex：生成 `spec.md` + `tasks.md` + `test-spec.md` + `log.md`；Quick：生成 `quick-card.md` + `log.md` |
| `/apply` | 逐 task 执行编码，每步需证据验证 |
| `/fix` | review 后的增量修正 |
| `/review` | 双阶段审查：Standard/Complex 做完整 Spec Compliance + Code Quality；Quick 做轻量合规检查（对照 quick-card）+ Code Quality |
| `/test` | TDD Red/Green 循环，覆盖率门禁 ≥80% |
| `/archive` | 知识沉淀 + 变更归档 |

Codex 输入注意：在 Codex 中请说 `finish <变更名>`、`archive <变更名>` 或中文自然语言来触发流程；不要输入 `/archive`，它会被 Codex 客户端解释为“归档当前会话”。如果 `/finish` 无法触发，也改用 `finish <变更名>`。
