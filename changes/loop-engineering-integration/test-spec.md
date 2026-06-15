# 测试 Spec：loop-engineering-integration

> **关联 Spec**：`spec.md`
> **Red/Green 铁律**：本次主要为文档和脚本自检变更，不新增业务测试；以自检脚本 marker 检查作为 P0 验收。
> **覆盖率门禁**：不适用。

---

## 0. 项目测试上下文

| 模块路径 | 技术栈/规则包 | 测试框架 | 全量测试命令 | 单测/定向测试命令 | 覆盖率命令/报告 |
|----------|---------------|----------|--------------|-------------------|----------------|
| `.` | shell + markdown | bash 自检 | `bash scripts/check_framework.sh` | 同全量 | 不适用 |

---

## 1. Agent Harness

| 项 | 内容 |
|----|------|
| Agent 可见证据 | `bash scripts/check_framework.sh` 输出；`rg` markers 输出 |
| 必跑验证命令 | `bash scripts/check_framework.sh` |
| 可观测信号 | 脚本失败时输出具体缺失 marker 和文件路径 |
| 失败自诊断入口 | `scripts/check_framework.sh` 中 Loop/Domain marker 检查；`rg -n "Goal Contract|Done Signal|Guardrails|Fallback|Loop Runtime|Loop Evidence|Domain Check|Invariants|State Transitions"` |
| 人工确认项 | 外部平台实时页面仍可能需要登录或验证；本次以用户提供的本地 JSON 为已读证据 |

---

## 2. Loop Evidence

| 项 | 内容 |
|----|------|
| Goal observed | 框架文档、prompt、模板、reviewer、自检脚本均能看到 Goal Contract |
| Done Signal | `bash scripts/check_framework.sh` PASS |
| Guardrail checks | 自检脚本要求 Guardrails / Goodhart markers，防止只留下“测试通过” |
| Fallback exercised | marker 缺失时自检 RED，按报错补文档/模板/脚本字段 |
| Memory update | `docs/loop-engineering.md`、模板字段、变更日志 |

---

## P0 核心逻辑测试（必测）

### TC-P0-01：Loop marker 自检

**模块**：`.`
**测试文件**：`scripts/check_framework.sh`
**测试目标**：框架关键文件包含 Loop Engineering markers。
**前置条件**：完成文档、prompt、模板、reviewer、自检脚本修改。
**操作**：运行 `bash scripts/check_framework.sh`
**预期结果**：命令退出码为 0。
**RED 证据**：本次未执行刻意 RED；原因是 marker 检查模式已在 Harness integration 中验证，本次复用同一机制。
**GREEN 证据**：`bash scripts/check_framework.sh` 输出 `ai-code-copilot framework check passed`，退出码 0。

### TC-P0-02：Goal Contract 可搜索

**模块**：`.`
**测试文件**：`docs/loop-engineering.md`, `agents/copilot-prompt.md`, `changes/templates/*.md`
**触发条件**：运行 `rg -n "Goal Contract|Done Signal|Guardrails|Fallback|Loop Runtime|Loop Evidence" docs README.md README-CN.md AGENTS.md agents changes/templates scripts`
**预期结果**：输出覆盖 docs、README、prompt、templates、reviewer、check script。
**RED 证据**：修改前 `bash scripts/check_framework.sh` 失败并提示 `docs/loop-engineering.md missing Loop markers: Goal Contract, Done Signal, Guardrails, Fallback, Loop Runtime`。
**GREEN 证据**：命令输出覆盖 `docs/loop-engineering.md`、`docs/harness-engineering.md`、`README.md`、`README-CN.md`、`AGENTS.md`、`agents/copilot-prompt.md`、reviewer、templates 和 `scripts/check_framework.sh`。

### TC-P0-03：Domain Check marker 自检

**模块**：`.`
**测试文件**：`rules/domain-rules.md`, `changes/templates/spec.md`, `agents/*.md`, `scripts/check_framework.sh`
**测试目标**：框架关键文件包含 DDD-lite Domain Check markers。
**前置条件**：已在自检脚本加入 Domain Check marker gate。
**操作**：运行 `bash scripts/check_framework.sh`
**预期结果**：命令退出码为 0。
**RED 证据**：加入 marker gate 后，补规则前自检失败：`rules/domain-rules.md missing Domain Check markers: Domain Check, Language, Boundary, Invariants, State Transitions, Owner`。
**GREEN 证据**：补齐规则、模板、prompt 和 reviewer 后，`bash scripts/check_framework.sh` 输出 `ai-code-copilot framework check passed`，退出码 0。

---

## P1 集成/数据/状态测试（应测）

### TC-P1-01：README 中英同步检查

**模块**：`.`
**测试文件**：`README.md`, `README-CN.md`
**依赖边界**：文档一致性
**操作**：人工比对核心特点、文档入口、workflow map 的 Loop Engineering 描述。
**预期结果**：中英文表达等价。

---

## P2 入口/端到端测试（选测）

无。此变更不涉及可运行应用入口。

---

## 不测试项

| 项目 | 原因 | 风险接受人/确认方式 |
|------|------|-------------------|
| 微信公众号正文抓取 | 当前返回验证页，不实现登录/验证绕过 | 记录为不可见信息 |
| X Article 全文抓取 | 公开页面仅能稳定读取摘要和元数据 | 记录为不可见信息 |
| 日志/指标 adapter | 本次只定义 Goal Contract，不实现集成 | spec 非目标 |

---

## 覆盖率目标

不适用。

---

## 实际测试结果

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `bash scripts/check_framework.sh` | PASS | `ai-code-copilot framework check passed` |
| `rg -n "Goal Contract|Done Signal|Guardrails|Fallback|Loop Runtime|Loop Evidence" docs README.md README-CN.md AGENTS.md agents changes/templates scripts` | PASS | 输出覆盖 AGENTS、README、docs、prompt、reviewer、templates、check script |
| legacy 7-field marker cleanup search | PASS | 退出码 1，无旧 7 项字段残留 |
| `rg -n "Domain Check|Language|Boundary|Invariants|State Transitions|Owner|DDD-lite|领域复杂度" rules changes/templates agents scripts changes/loop-engineering-integration` | PASS | 输出覆盖 domain rules、spec/quick-card template、prompt、reviewer、自检脚本和本变更文档 |
