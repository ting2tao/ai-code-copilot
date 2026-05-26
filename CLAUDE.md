# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目简介

ai-code-copilot 是一个面向后端项目的 AI 编码协作框架（Claude Code skill）。它不是一个可运行的应用，而是一套部署到 `~/.claude/ai_code_copilot/` 的提示词、规则、Agent 和安装脚本。核心理念：**Code is Cheap, Context is Expensive**，通过 Spec 驱动的流程（brainstorm → propose → apply → review → archive）确保 AI 在正确的上下文里做正确的事。

## 架构：两层结构

**全局层**（安装后位于 `~/.claude/ai_code_copilot/`）— 框架运行主体：
- `skill/SKILL.md` — Claude Code skill 注册入口，定义触发条件
- `agents/copilot-prompt.md` — 主提示词，定义所有命令逻辑、流程控制、硬性门控
- `agents/spec-reviewer.md` / `agents/code-quality-reviewer.md` — 双阶段审查的 Sub-Agent
- `hooks/session-start` — 会话启动时通过 `hookSpecificOutput` 注入安全规则
- `hooks/hooks.json` — hook 注册配置
- `rules/` — 全局编码规范（Java P3C、Spring 约定、安全红线等）
- `knowledge/` — 知识库（由 `/archive` 沉淀积累）
- `changes/templates/` — 变更文档模板（spec、tasks、log、design-brief）
- `packs/java-spring/pack.md` — 技术栈规则包，`/init` 时自动检测加载

**项目层**（`/init` 后在业务项目中生成 `<project>/ai_code_copilot/`）：
- `rules/project-context.md` — 自动检测的技术栈、构建命令、分层架构
- `rules/coding-style.md` — 项目级编码规范（覆盖全局）
- `rules/domain-rules.md` — 业务约束（用户手动填写）
- `changes/<变更名>/` — 活跃变更目录，含 spec/tasks/log

## 修改框架时的关键文件

- `agents/copilot-prompt.md` — 所有命令逻辑、流程控制、硬性门控
- `skill/SKILL.md` — 触发条件和 skill 描述
- `hooks/session-start` — 会话启动注入的安全规则
- `rules/*.md` — 编码规范和约定
- `changes/templates/*.md` — 变更文档模板

## 安装脚本

- `install.sh` — macOS/Linux：clone 到 `~/.claude/ai_code_copilot/`，创建 skill symlink，注册 SessionStart hook
- `install.ps1` — Windows PowerShell：使用目录 Junction 替代 symlink
- `install-wsl.sh` — WSL 变体

## 核心设计原则

- **No Spec, No Code** — Standard/Complex 档必须先有确认的 spec 才能编码
- **渐进式复杂度** — Quick（≤1天，<5文件）/ Standard / Complex（>5天，跨3+模块）
- **Evidence Before Claims** — 每个 task 完成必须展示可验证的命令输出
- **双阶段审查** — Spec Compliance（是否按 spec 实现）+ Code Quality（代码质量）
- **知识飞轮** — `/archive` 将经验沉淀到 `knowledge/`，下次自动加载
- **安全红线** — 硬编码密钥、日志打印敏感信息、资金/权限变更必须人工确认

## 命令速查

所有命令定义在 `agents/copilot-prompt.md` 中：

| 命令 | 用途 |
|------|------|
| `/init` | 检测技术栈，创建项目级 `ai_code_copilot/` |
| `/brainstorm` | 苏格拉底式设计探索，输出 `design-brief.md` |
| `/propose` | 生成 `spec.md` + `tasks.md` + `log.md` |
| `/apply` | 逐 task 执行编码，每步需证据验证 |
| `/fix` | review 后的增量修正 |
| `/review` | 双阶段 Sub-Agent 审查（spec 合规 + 代码质量） |
| `/test` | TDD Red/Green 循环，覆盖率门禁 ≥80% |
| `/archive` | 知识沉淀 + 变更归档 |
