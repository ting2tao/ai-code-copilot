<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:roadmap
artifactType: roadmap
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:design-brief
upstreamHash: sha256:844c5ccce171a10dcd21c36cd8c4cde4b770a7c83c21cbc6c39f8f5b3e65bfcb
-->

# Complex Roadmap：ai-native-sdlc-alignment

> **状态**：[ ] 草稿 / [x] 已确认 / [ ] 实施中 / [ ] 已完成
> **创建时间**：2026-08-24
> **确认时间**：2026-08-24
> **确认人**：用户

---

## 1. 总目标

把 ai-code-copilot 从 AI Coding 工作流推进为 Agent 可持续工作的研发运行环境：Context 和 Skills 提供工作记忆，Artifact Chain 负责阶段交接，Evals 保护 Agent 配置，Hooks/CI 执行确定性控制，Agent Review 与 Human Gates 分层判断，Git 保存审计轨迹，Maintain 信号重新进入循环。同时保持平台无关、渐进式成本和人工风险责任。

## 2. 子变更拆分

| ID | 子变更 | Session scope | 依赖 | Upstream summary | 是否可并行 |
|----|--------|---------------|------|------------------|------------|
| S1 | Artifact Chain + Agent Eval Baseline | artifact schema、模板 metadata、eval case schema/runner、contract fixtures | — | — | 否，基础阶段 |
| S2 | Deterministic Guardrail Layers | guardrail policy、deterministic checks、CI/hook adapter、review/finish 集成 | S1 | artifact ID、policy version、eval baseline | 部分可并行 |
| S3 | Maintain-to-Plan Loop + Lifecycle Metrics | triage workflow、event intake、draft design-brief、metrics schema/docs | S1、S2 | artifact/control contracts、eval/guardrail evidence | 否 |

## 3. Session isolation rules

每个子变更进入实现前生成独立的 spec/tasks/test-spec/log；只加载本 roadmap、当前子变更记录以及表中声明的上游 `log.summary.md`。跨子变更只传递 schema、公开合同、关键决策和验证快照，不传递完整过程日志。

开始下游子变更前：

- [ ] 上游 `log.summary.md` 已由 owner 审阅。
- [ ] schema/version/兼容策略明确。
- [ ] 下游依赖的命令和 fixtures 可独立运行。
- [ ] 未解决风险已显式进入下游 Guardrails 或人工门禁。

## 4. 集成顺序

1. S1 先建立 artifact/eval 的机器合同与兼容策略。
2. S2 使用 S1 eval 保护 guardrail 行为，接入静态检查、CI 和可用平台 hook。
3. S3 让事件触发的诊断输出沿 S1 artifact chain 回流，并由 S2 guardrail 限制权限。
4. 运行全量 framework check、离线 eval、adapter capability check 和文档一致性检查。
5. live eval 先以非阻塞模式收集基线，再决定是否成为 merge gate。

## 5. 总体验收

- [ ] 新 Full 变更能从 design-brief 追踪到 spec/tasks/test/review/finish/lesson，且上游 hash 漂移可被检测。
- [ ] 至少 15 个代表性 Agent eval case 覆盖路由、升级、安全门禁、No Contract No Code、验证证据和平台兼容。
- [ ] advisory、deterministic、human gate 三层控制有统一 policy，至少两个确定性检查可执行失败和通过。
- [ ] CI/事故/告警事件可以只读诊断并生成 draft design-brief，默认不能越过 publish/production gate。
- [ ] 生命周期指标包含阶段时延、first-pass CI、返工、eval、审批等待和事故复发，并有 Goodhart guardrail。
- [ ] 旧变更记录无需迁移，`bash scripts/check_framework.sh` 保持通过。

## 6. 跨子变更风险

| 风险 | 影响 | 缓解措施 | 回滚方案 |
|------|------|---------|----------|
| schema 提前冻结 | 后续 adapter 被迫兼容错误抽象 | S1 先做 version=1 和 unknown-field tolerance | 回滚 schema/check，旧读取路径继续工作 |
| live eval 不稳定 | 阻塞合并 | 首期非阻塞、固定样本、重复运行与预算上限 | 退回 validate-only/offline eval |
| hook 平台能力不一致 | 安全语义不一致 | policy 输出 `advisory/deterministic/human` 和 capability 状态 | 禁用 adapter，保留 CI gate |
| triage 噪声 | 产生大量低价值 draft | 确定性 trigger、阈值、去重键和人工 triage | 关闭 event adapter，不影响手动流程 |

## 7. log.summary.md format

每个子变更 `/finish` 生成不超过 30 行的摘要，至少包含：schema/policy version、公开字段、兼容决策、验证命令和结果、下游已知风险；不包含实现尝试和完整日志。

## 8. 监控与归档

- 监控指标：offline/live eval pass rate、first-pass CI、artifact drift、guardrail block/false-positive、triage conversion、repeat incident。
- 知识沉淀方向：Agent eval case 设计、跨平台 hook capability、artifact migration、低噪声事件触发。
