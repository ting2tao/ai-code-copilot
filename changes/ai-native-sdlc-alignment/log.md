<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:log
artifactType: log
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:spec
upstreamHash: sha256:a9dee5165c570806487c2e4ccf9ef1ecedef3e61b6df6e133e79c6bcb49a1f84
-->

# 变更日志：ai-native-sdlc-alignment

## Summary

| 字段 | 内容 |
|------|------|
| 变更名 | ai-native-sdlc-alignment |
| 档位 | Complex |
| 状态 | in-apply（S1） |
| 开始时间 | 2026-08-24 |
| 完成时间 | 未完成 |
| parentIssue | none |
| workIssue | pending（on-publish） |
| issueRelationship | pending；预计 standalone |
| closeTarget | workIssue |
| branch | feat/ai-native-sdlc |
| 确认时间 | 2026-08-24 |
| 确认人 | 用户 |
| 确认范围 Hash | `sha256:e095b8f47bb69d4ecd7366cdbbd69b841c32c21bcd7e1a82139a17d0ae905a07`（动态 Artifact 字段归一化） |
| 涉及文件数 | 总范围 20+；按 S1/S2/S3 拆分 |
| commit 列表 | 无 |

## Active decisions

### 2026-08-24 - 产品定位从 AI Coding 提升到 Agent-operable SDLC

**内容**：用户明确提出，下一阶段竞争是把整个研发系统改造成 Agent 可以持续工作的系统，而非只提升 AI 写代码速度。
**决策**：采用八项能力模型：Context Engineering、Skills、Artifact Chain、Evals、Hooks、Agent Review、Human Gates、Git Audit Trail。
**影响**：作为总 Spec 和后续 README/docs 的战略主张；S1 范围不扩大，仍只实现 Artifact Chain、Evals 和审计地基。

### 2026-08-24 - Complex Spec 已确认

**内容**：用户明确回复“确认 Spec”。
**决策**：按 S1 → S2 → S3 实施；live model eval 首期非阻塞；triage 首期不接真实生产监控。
**影响**：本轮进入 S1，只修改 Artifact Chain 和 Agent Eval baseline；S2/S3 保持未开始。

### 2026-08-24 - 采用增量 AI-native 对齐

**内容**：用户同意基于 Anthropic AI-Native SDLC playbook 优化项目。
**决策**：保留现有 Progressive SDD 和产物命名，强化 Artifact Chain、Agent eval、三层 Guardrail、Maintain 回流和 lifecycle metrics。
**影响**：变更按 Complex 管理，拆成三个 Standard 子变更；本轮只建立提案，不实施行为变更。

### 2026-08-24 - 平台无关核心

**内容**：参考文章包含 Claude Code、Claude Tag、managed settings 等专属能力。
**决策**：核心合同使用平台无关 schema/policy；Claude/Codex/CI 只作为 adapter，unsupported 必须显式报告。
**影响**：不会因为单个平台缺失 hook 就削弱核心 CI/human gate。

## Known risks

- [ ] live eval 的成本、抖动和 merge 策略需在 S1 收集基线后再决定。
- [ ] guardrail adapter 启用会改变 CI/hook 行为，进入 S2 前需确认具体控制与批准路径。
- [ ] triage 真实外部连接器和生产监控不在首期范围。

## Review outcomes

尚未 review；Spec 仍为草稿。

## Verification log

### 2026-08-24 - 提案基线自检

```text
command: bash scripts/check_framework.sh
exit code: 0
output:
progressive-sdd: policy and module checks passed
ai-code-copilot framework check passed
```

### 2026-08-24 - S1 Artifact/Eval implementation

```text
command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --change-dir changes/ai-native-sdlc-alignment --require-chain
exit code: 0
output: PASS 12 artifacts

command: bash scripts/check_framework.sh
exit code: 0
output: artifact fixtures/templates/transition PASS; 18 offline evals and external scorer self-check PASS; framework check passed
```

## Loop Evidence

### 2026-08-24 - 提案建立

| 项 | 内容 |
|----|------|
| Done Signal | design-brief/roadmap/spec/tasks/test-spec/log/summary 完整且 framework check 通过 |
| Guardrails checked | 未改运行时；未创建分支/commit/Issue；未执行外部写入；Spec 未确认前不实施 |
| Fallback | 用户不接受任一关键边界时 Reverse Sync 对应 Spec/roadmap |
| Memory | 将文章映射为平台无关 Artifact/Eval/Guardrail/Triage 模型 |

## Knowledge candidates

### [待沉淀] AI-native SDLC 应优先复用现有 artifact

**类别**：架构决策
**内容**：引入外部 SDLC 方法时，应映射到现有 design-brief/spec/tasks/test/log，而不是机械新增同义文件；真正需要补的是机器关系、回归评测和闭环触发。
**关键词**：AI-native SDLC, artifact chain, intent, plan
**建议 Scope**：framework architecture
**建议 Applies-To**：brainstorm / propose / review
**建议 Risk**：medium
**建议文件名**：`ai-native-artifact-mapping.md`

## 遗留问题

- [ ] S1 完成后独立 review，再决定是否进入 S2。
