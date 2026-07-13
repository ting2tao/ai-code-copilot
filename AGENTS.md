# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 项目简介

ai-code-copilot 是一个面向多技术栈软件项目的 AI 编码协作框架（Codex skill，兼容 Claude Code）。它不是一个可运行的应用，而是一套部署到 `~/.codex/ai_code_copilot/`（Codex）或 `~/.claude/ai_code_copilot/`（Claude Code）的提示词、规则、Agent 和安装脚本。核心理念：**Context First, Harness Enables, Code Follows.** AI 让代码更容易生成，ai-code-copilot 通过 Spec 驱动的流程（brainstorm → propose → apply → review → archive）和 Harness 反馈循环，让上下文变得明确、可审查、可复用，确保 AI 在正确的上下文里做正确的事。

## 架构：两层结构

**全局层**（安装后默认位于 `~/.codex/ai_code_copilot/`）— 框架运行主体：
- `skill/SKILL.md` — Codex skill 注册入口，定义触发条件
- `agents/router.md` — 轻量运行时入口，选择 Inline/Compact/Full SDD 并按需加载模块
- `agents/workflows/` — init、inline、compact、full、debug、review、test、finish、archive 专项模块
- `agents/copilot-prompt.md` — 旧安装或模块缺失时的严格兼容回退，不是默认加载入口
- `config/workflow-policy.json` — 分层阈值、风险类别、升级触发器和 Issue 策略的机械合同
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
- `changes/<变更名>/` — 活跃变更目录；Quick Compact 仅含 `quick-card.md`，Quick Full 含 `quick-card.md` + `log.md` + `summary.md`，Standard/Complex 按流程使用 spec/tasks/test-spec 等文件

## 修改框架时的关键文件

- `agents/router.md` / `agents/workflows/*.md` — 默认运行时路由和各阶段流程
- `config/workflow-policy.json` — 可机械验证的分层与生命周期策略
- `agents/copilot-prompt.md` — 兼容回退；修改核心合同后需检查回退是否仍保持更严格的 legacy 行为
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

- **Progressive SDD** — Inline SDD 使用会话内 Goal/Scope/Done Signal/Verify，仅限具备可执行验证和直接回滚的低风险小改动；Compact SDD 使用 `quick-card.md`；Full SDD 使用完整 spec/tasks/test/log 记录。三档只改变持久化成本，不降低工程质量
- **No Contract, No Code** — Inline 必须先明确会话合同；Compact 没有 Quick Card 不写代码；Full 没有确认的 Spec 不写代码
- **单向升级** — `Inline -> Compact -> Full` 或 `Inline -> Full`；活动变更不自动降级，升级必须保留 previous contract、diff 和验证证据
- **Quick 兼容** — 原 Quick Compact 对应 Compact SDD，`quick-card.md` 是唯一记录源；Quick Full 使用 `quick-card.md` + `log.md` + `summary.md`，Standard/Complex 对应 Full SDD；旧记录无需迁移
- **Issue 自动化** — 开始时用 `parentIssue` 读取整体需求；`issuePolicy` 决定解析时机：新项目默认 `on-publish`，旧配置缺失时按 `always`；到达门禁后自动创建或校验复用 `workIssue`，可用时建立 native sub-issue
- **Git 硬合同** — 分支必须是 `type/scope`，commit 必须是 `type(scope): description`
- **安全收尾** — PR 只用 `Closes #<workIssue>` 关闭工作 Issue，父级只用 `Refs #<parentIssue>`；`finishMode` 只控制 PR handoff
- **配置迁移** — 项目配置不自动改写；缺少 `issuePolicy` 时保持 legacy `always`，旧 `issueWhenMissing` 已废弃并忽略
- **Evidence Before Claims** — 每个 task 完成必须展示可验证的命令输出
- **Harness Enables** — 规格、测试、日志、review、规则和知识沉淀共同构成 Agent 可见反馈循环
- **Loop Engineering** — 每个变更都要声明简洁的 Goal Contract：Goal、Done Signal、Guardrails、Fallback、Memory
- **DDD-lite Domain Check** — 复杂业务才记录 Language、Boundary、Invariants、State Transitions、Owner，不强制完整 DDD 结构
- **双阶段审查** — Spec Compliance（是否按 spec 实现）+ Code Quality（代码质量）
- **知识飞轮** — `/archive` 将经验沉淀到 `knowledge/`，下次自动加载
- **安全红线** — 硬编码密钥、日志打印敏感信息、资金/权限变更必须人工确认
- **Superpowers 边界** — ai-code-copilot 是唯一默认编排器；Superpowers 只作为显式专项检查表使用，不默认叠加第二套 brainstorm/TDD/plan 流程

## 命令速查

默认命令路由定义在 `agents/router.md` 和 `agents/workflows/`；`agents/copilot-prompt.md` 保留兼容回退：

| 命令 | 用途 |
|------|------|
| `/init` | 检测技术栈，创建项目级 `.ai_code_copilot/` |
| `/brainstorm` | 苏格拉底式设计探索，输出 `design-brief.md` |
| `/propose` | Standard/Complex：生成 spec/tasks/test-spec/log/summary；Quick Compact：仅 `quick-card.md`；Quick Full：`quick-card.md` + `log.md` + `summary.md` |
| `/apply` | 逐 task 执行编码，每步需证据验证 |
| `/fix` | review 后的增量修正 |
| `/review` | 双阶段审查：Standard/Complex 做完整 Spec Compliance + Code Quality；Quick 做轻量合规检查（对照 quick-card）+ Code Quality |
| `/test` | TDD Red/Green 循环，覆盖率门禁 ≥80% |
| `/archive` | 知识沉淀 + 变更归档 |

Codex 输入注意：在 Codex 中请说 `finish <变更名>`、`archive <变更名>` 或中文自然语言来触发流程；不要输入 `/archive`，它会被 Codex 客户端解释为“归档当前会话”。如果 `/finish` 无法触发，也改用 `finish <变更名>`。
