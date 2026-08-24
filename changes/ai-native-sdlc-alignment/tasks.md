<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:tasks
artifactType: tasks
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:spec
upstreamHash: sha256:a9dee5165c570806487c2e4ccf9ef1ecedef3e61b6df6e133e79c6bcb49a1f84
-->

# 任务列表：ai-native-sdlc-alignment

> **关联 Spec**：`spec.md`
> **关联 Test Spec**：`test-spec.md`
> **关联 Roadmap**：`roadmap.md`
> **状态**：已确认；按 S1 → S2 → S3 顺序执行
> **零偏差原则**：每个子变更进入实现前生成独立 Standard 记录；本文件只维护 Complex 总体执行顺序和集成门禁。

## Preflight

- [x] 用户已确认 spec/tasks/test-spec/roadmap，确认 hash 已记录。
- [ ] `workIssue` 已按当前 lifecycle 解析，或仍未到 `on-publish` 门禁。
- [x] 创建并切换到 `feat/ai-native-sdlc`。
- [x] `git status --short` 已检查，不覆盖用户无关改动。
- [ ] 每个子变更拥有独立 spec/tasks/test-spec/log 和清晰目标文件。
- [ ] live eval、CI/hook adapter、事件 connector 的成本/权限/外部写入边界已单独确认。

## 进度概览

| Task | 描述 | 状态 | commit hash |
|------|------|------|-------------|
| T1 | S1：Artifact Chain 合同与 checker | ✅ | pending commit |
| T2 | S1：Agent Eval baseline | ✅ | pending commit |
| T3 | S2：三层 Guardrail policy 与 deterministic checks | ⏳ | |
| T4 | S2：CI/platform adapter 与 review/finish 集成 | ⏳ | |
| T5 | S3：Maintain/triage 回流 | ⏳ | |
| T6 | S3：Lifecycle metrics 与文档同步 | ⏳ | |
| T7 | 总体 review、兼容性和验收 | ⏳ | |

---

## T1：S1 — Artifact Chain 合同与 checker

**功能点**：F1

**预计文件**：

- 新建：`scripts/check_artifact_chain.py`
- 修改：`changes/templates/{design-brief,spec,tasks,test-spec,log,summary,quick-card,roadmap}.md`
- 修改：`agents/workflows/{full,compact,review}.md`
- 修改：`scripts/check_framework.sh`

**完成标准**：

- [ ] schema/version、artifact ID/type/status、upstream/hash、source-of-truth 和 approval 字段有唯一合同。
- [ ] 新记录非法关系 RED；合法链 GREEN；legacy fixture 保持 GREEN。
- [ ] Compact 只使用最小 metadata，Inline 不受影响。

---

## T2：S1 — Agent Eval baseline

**功能点**：F2

**预计文件**：

- 新建：`evals/README.md`, `evals/schema.json`, `evals/cases/*.json`
- 新建：`scripts/run_agent_evals.py`
- 修改：`scripts/check_framework.sh`

**完成标准**：

- [ ] 至少 15 个案例覆盖 Inline/Compact/Full、promotion、security/permission/deploy、No Contract No Code、review、verification、unsupported capability。
- [ ] validate-only/offline 模式无网络、无模型密钥也能执行。
- [ ] live adapter 显式 opt-in、带预算/超时、首期不阻塞 merge。

---

## T3：S2 — 三层 Guardrail policy 与 deterministic checks

**功能点**：F3、F4

**预计文件**：

- 新建：`config/guardrail-policy.json`, `scripts/check_guardrails.py`
- 修改：`rules/security.md`, `config/workflow-policy.json`
- 修改：`agents/workflows/{full,debug,review,finish}.md`

**完成标准**：

- [ ] 每条控制声明 advisory/deterministic/human gate、owner、trigger、evidence、block reason 和 approval route。
- [ ] 至少实现 secret/sensitive diff 与 protected/test-path 两类确定性检查。
- [ ] false-positive 有明确 override/人工路径，override 被记录而不是静默绕过。

---

## T4：S2 — CI/platform adapter 与流程集成

**功能点**：F4、F7

**预计文件**：

- 修改：`hooks/hooks.json` 或新增平台 adapter（以可用能力为准）
- 修改：`agents/router.md`, `skill/SKILL.md`, `agents/copilot-prompt.md`
- 修改：`scripts/check_framework.sh`

**完成标准**：

- [ ] 核心 policy 不依赖 Claude/Codex 专属设置。
- [ ] adapter 输出 supported/unsupported/degraded，不得假报 enforcement。
- [ ] CI gate 始终可作为平台 hook 缺失时的确定性 fallback。

---

## T5：S3 — Maintain/triage 回流

**功能点**：F5

**预计文件**：

- 新建：`agents/workflows/triage.md`
- 修改：`agents/router.md`, `skill/SKILL.md`, `config/workflow-policy.json`
- 修改：`changes/templates/design-brief.md`, `agents/workflows/debug.md`
- 新增：事件 fixtures 和 triage contract test

**完成标准**：

- [ ] deterministic trigger/event 输入先只读诊断，再生成 `status: draft` design-brief。
- [ ] draft 包含 source event、evidence、dedupe key、affected systems、proposed outcome 和 open questions。
- [ ] 未经人类 triage 不得 apply/publish/deploy；创建外部 Issue/PR 仍遵循现有 policy。

---

## T6：S3 — Lifecycle metrics 与文档同步

**功能点**：F6、F7

**预计文件**：

- 修改：`rules/github-metrics.md`
- 新建：`docs/ai-native-sdlc.md`
- 修改：`docs/{harness-engineering,loop-engineering,ai-code-copilot-flow}.md`
- 修改：`README.md`, `README-CN.md`, `AGENTS.md`

**完成标准**：

- [ ] 指标包含 artifact latency、first-pass CI、rework、eval、guardrail wait/false-positive、triage conversion、repeat incident。
- [ ] Test-to-Code Ratio 明确为辅助诊断，不作为单一质量结论。
- [ ] 中英文 README 同步，术语与 router/workflows 一致。

---

## T7：总体 review、兼容性和验收

**功能点**：F1–F7

**完成标准**：

- [ ] 三个子变更均通过 Spec Compliance、Code Quality 和 GitHub Readiness。
- [ ] 运行 `bash scripts/check_framework.sh` 并记录新鲜输出。
- [ ] 运行全量 offline eval 和 legacy compatibility fixtures。
- [ ] 检查 legacy `agents/copilot-prompt.md` 仍保持更严格兼容行为。
- [ ] roadmap §5 全部验收，未启用能力明确报告而非默认为 PASS。
