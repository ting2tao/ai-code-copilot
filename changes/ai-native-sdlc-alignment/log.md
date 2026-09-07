<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:log
artifactType: log
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:spec
upstreamHash: sha256:d54744ca078038516279986bef4fed50a17b7431a65373eca611789008833b25
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
| commit 列表 | `6be53b8 feat(sdlc): add artifact chain and agent eval baseline` |

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

### S1 Review

- Spec Compliance：PASS。
- Code Quality：PASS。
- GitHub Readiness：NEEDS_INFO，仅因 `on-publish` workIssue 尚未解析；不阻塞本地 commit。
- Harness/Loop Readiness：READY；live model eval 明确为未执行的 non-blocking capability。

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

- [x] S1 已完成本地 review，用户同意继续 S2。
- [ ] S2 最终人工/独立 review 与启用确认；当前无 commit/push/PR，S3 未实施。

### 2026-09-03 — S2 与消融增补

- 用户明确要求“继续，也加上消融原理，防止过度抽象和设计”；S2 子 Spec 增补确认来源，hash 同步，parent/S1 冻结合同未修改。
- 新增三层 Guardrail policy、event/Git checker、Claude Write/Edit adapter（仅仓库代码，未实际启用）；审批声明绑定 eventHash，不代替人类身份验证。
- 消融复用 YAGNI/Full/test/review/log；不创建新流程或独立报告，不在真实环境关闭安全门禁。
- 17 tests PASS，含 12 fixtures 与 4 组隔离消融；真实 diff 仍返回 protected-path/security ask，未伪造 approval。
- 详细失败/修复/证据与限制见 `s2-deterministic-guardrails/log.md`。

### 2026-09-03 — 官方原则更新与 S2 审查 FAIL

用户要求审查并加入最新 Claude/OpenAI Agent/Harness 原则。已核实官方文档，更新现有 harness/loop、Full/review、eval 和 capability 说明；未新增 runtime 或部署服务。本地审查复现 R1（不同删除 diff 共用审批 hash）与 R2（event 模式静默忽略风险/动作 flags），故 S2 当前审查 FAIL；19 tests GREEN 不代表缺陷已修复。安全协议修复待确认，不启用自动门禁。详细证据、来源和建议位于 S2 log，保留此前验证为历史记录。

### 2026-09-03 — 用户确认修复 R1 / R2

- 用户“修复”授权后，更新 S2 合同并实现最小修复：Git 快照摘要绑定完整 patch/base 与扫描文件字节/权限；event/hook 拒绝 Git-only flags（含显式默认值）。
- 永久回归首次 16 个断言失败，逐项修复后通过；补充边界后 23 tests OK，全量 framework、17 artifacts、18 offline eval/scorer 自检通过。具体命令与分阶段结果见 S2 log。
- 本地 R1/R2 修复复核通过，前轮未修复状态在此更新；不是独立 Agent Review。真实 diff 仍有 protected/fix/security ask，最终人工/独立审查与启用仍待确认。
- 未新增审批平台/快照引擎；未 commit/push/PR、未启用 hook/CI、未改个人配置；S3 未实施。

### 2026-09-07 — main 集成与最终独立重审完成

- S1/S2 已集成 `origin/main` ee028aa4，保留 model-first Native/Compact/Full 与 policy v2；VERSION 0.2.0。独立 Stage 1 PASS，最终 Stage 2 PASS（0 Critical / 0 Important / 0 Minor）。
- 相邻输入边界、policy selector typo 与纯文本 binary-marker 误拦截反例均已 RED → GREEN；37 tests、framework、17 artifacts、21 eval cases 通过。
- Issue #36 已解析。当前仅等待完成记录后的最终 review/commit/publish eventHash 人工批准；批准前不 commit/push/PR，不合并、不启用 hook/CI，S3 不在本次范围。

### 2026-09-03 — 独立审查 Stage 1 FAIL

用户明确要求独立审查。独立上下文 reviewer `/root/independent_spec_review` 亲自检查当前 S2 代码，复验 17 artifacts / 23 tests / framework PASS，但发现 R3(P1)：hook 以 cwd 代替仓库根，在 infra/tests 子目录漏掉路径审批；R4(P2)：旧 symlink 删除/替换未执行声明的类型阻断。主 Agent 已复验反例，完整证据和基线 hash 见 S2 log。R1/R2 原修复回归仍通过；当前整体审查 FAIL，按流程未启动 Stage 2。只更新审查记录，未修实现、未提交/发布或启用 hook/CI。

### 2026-09-03 — R3 / R4 修复

用户“修复”确认后，hook 改为从 Git 工作树根计算规则路径（cwd 只解析相对输入；根查询有界，未知根阻断）；Git 类型校验同时覆盖 base 旧模式与当前文件。原反例及扩展矩阵 RED → GREEN，27 tests / 17 artifacts / framework PASS。明确新增的 Git 工作树前提，不增加根配置协议或审批服务。详细证据见 S2 log；独立 Stage 1 重审和 Stage 2 尚未执行，不将本地通过写成独立 PASS。未提交、发布或启用 hook/CI，S3 未实施。

### 2026-09-03 — 独立重审发现 R5(P2)

独立 reviewer `/root/spec_rereview` 确认 R1–R4 功能修复验收通过，但 Stage 1 因单一 R5(P2) 诊断缺口 FAIL：Git 不可用时安全阻断正确（exit 2），却只报通用 invalid，未满足明确 degraded/恢复说明合同。主 Agent 已真实 PATH 隔离复验；27 tests、17 artifacts、framework 仍通过，不能覆盖该缺口。按流程未进入 Stage 2。本轮只记录审查结论，未修实现、未提交或启用 hook/CI；详见 S2 log。

### 2026-09-03 — 用户请求 Issue / PR 到 main：未创建，等待授权与门禁

- 用户请求“issue, 提交pr到main”。已只读确认 origin 为 ting2tao/ai-code-copilot，远端默认分支 main；无 open Issue、无 feat/ai-native-sdlc 的 open PR。
- 拟交付范围为本分支 S1/S2，不将未实施的 S3 计为完成。Issue 草稿位于 `/tmp/copilot-publish.h6JTfT/issue.md`，包含 R5、独立 Stage 1/2 和实际人工门禁的未完成项。
- 使用当前 GitHub CLI 身份创建工作 Issue，实际失败：`GraphQL: Unauthorized: As an Enterprise Managed User, you cannot access this content (createIssue)`。复查同名 open Issue 为空，故 workIssue 保持 pending，不虚构编号或重复创建。
- 只读 auth 核验：当前身份 shict01_onewo，仓库 viewerPermission=READ；已保存 ting2tao 账号但非活动账号。未切换账号、未读取/输出凭据，等待用户明确使用相应身份。
- 发布门禁也尚未满足：R5(P2) 导致独立 Spec review FAIL，Stage 2 尚未执行。没有将用户 PR 请求解释为风险豁免或代码修复授权。
- 本轮未 commit、push、创建 PR、合并或启用 hook/CI。待确认账号及 R5 修复/重审授权后继续。

### 2026-09-03 — 用户确认账号、修复与发布

用户明确答复“是的”，授权使用 ting2tao，修复 R5，完成独立审查后创建 Issue、提交并发起到 main 的 PR。已切换已登录 GitHub CLI 身份到 ting2tao，并验证 ADMIN 权限。已创建工作 Issue https://github.com/ting2tao/ai-code-copilot/issues/36，standalone，closeTarget=workIssue，仅覆盖本次 S1/S2 交付，S3 不随此票关闭。尚未提交/push/PR，不合并、不启用 hook/CI。
