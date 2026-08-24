<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:spec
artifactType: spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:roadmap
upstreamHash: sha256:9ac6664cf068b955e9529307b7951d439e95757d8f36a0a7ff6b94d8a7be6ae6
-->

# 变更 Spec：ai-native-sdlc-alignment

> **状态**：[ ] 草稿 / [x] 已确认 / [ ] 实施中 / [ ] 已完成
> **复杂度档位**：[ ] Quick / [ ] Standard / [x] Complex
> **创建时间**：2026-08-24
> **父 Issue（parentIssue）**：none
> **工作 Issue（workIssue）**：pending（`on-publish` 门禁解析）
> **Issue 关系（issueRelationship）**：pending；解析后应为 standalone
> **关闭目标（closeTarget）**：workIssue
> **分支（branch）**：feat/ai-native-sdlc
> **确认时间**：2026-08-24
> **确认人**：用户
> **确认范围 Hash**：`sha256:e095b8f47bb69d4ecd7366cdbbd69b841c32c21bcd7e1a82139a17d0ae905a07`（confirmationHash/sourceRevision/upstreamHash 归一化）

---

## 1. 背景与目标

### 1.1 背景

现有框架已经实现 Progressive SDD、Harness、Loop、双阶段 review、Evidence Before Claims 和知识飞轮。相比 AI-native SDLC 的完整闭环，当前主要差距是：产物之间缺少统一机器关系；Agent 配置没有真实任务级回归 eval；关键规则多为 advisory；维护信号不能正式回流到规划阶段；指标偏重 GitHub 结构而非循环质量。

### 1.2 目标

把 ai-code-copilot 从 AI Coding 工作流推进为 Agent 可持续工作的研发运行环境。通过 `Context Engineering + Skills + Artifact Chain + Evals + Hooks + Agent Review + Human Gates + Git Audit Trail` 建立平台无关、渐进式、可机械验证的 AI-native SDLC，使 artifact、Agent 配置、治理动作和维护反馈形成可审计闭环。

### 1.3 非目标（Out of Scope）

- 不替换 Inline/Compact/Full SDD，也不为 Inline 强制生成文件。
- 不新增强制 `intent.md` 或 `plan.md`。
- 不迁移历史 changes。
- 不绑定单一模型、Claude 服务、Codex 私有能力或外部 observability vendor。
- 不允许无人值守生产发布、权限变更、资金操作或破坏性数据库动作。
- 不在本变更中部署真实生产监控系统。

---

## 2. 功能点

| # | 功能点 | 优先级 | 备注 |
|---|--------|--------|------|
| F1 | 定义 versioned Artifact Chain metadata 和 source-of-truth/linkage 合同 | P0 | Full 强制，Compact 最小化，历史记录兼容 |
| F2 | 建立离线 Agent eval case schema、runner 和首批真实任务 fixtures | P0 | live adapter 首期可选且非阻塞 |
| F3 | 将控制分为 advisory、deterministic、human gate 三层 | P0 | 平台无关 policy 是事实源 |
| F4 | 提供可执行 guardrail checks 及 CI/平台 adapter capability 合同 | P0 | adapter 不支持时明确降级到 CI/human |
| F5 | 增加事件/事故/失败到 draft design-brief 的 triage workflow | P1 | 默认只读诊断，不自动越过外部门禁 |
| F6 | 扩展生命周期、eval、guardrail 和事故复发指标 | P1 | 成组解读，防 Goodhart |
| F7 | 同步 router、workflows、skill、文档和中英文 README | P0 | README 双语同步 |
| F8 | 明确 AI Coding → Agent-operable SDLC 的产品定位与能力模型 | P0 | 不新增平行流程，映射到现有 Context/Harness/Loop |

---

## 3. 变更范围

### 3.1 涉及模块

```text
config/
├── workflow-policy.json              # artifact/eval/guardrail/triage policy 入口
└── guardrail-policy.json              # 新增：三层控制与 capability 合同
agents/
├── router.md
└── workflows/
    ├── full.md
    ├── compact.md
    ├── review.md
    ├── finish.md
    ├── debug.md
    └── triage.md                      # 新增
changes/templates/
├── design-brief.md
├── spec.md
├── tasks.md
├── test-spec.md
├── log.md
├── summary.md
├── quick-card.md
└── roadmap.md
evals/
├── README.md
├── schema.json
└── cases/*.json                       # 新增：路由/风险/升级/验证案例
scripts/
├── check_artifact_chain.py            # 新增
├── check_guardrails.py                # 新增
├── run_agent_evals.py                 # 新增
└── check_framework.sh
rules/
├── security.md
└── github-metrics.md
docs/
├── ai-native-sdlc.md                  # 新增：平台无关方法与 adoption guide
├── harness-engineering.md
├── loop-engineering.md
└── ai-code-copilot-flow.md
README.md / README-CN.md / AGENTS.md / skill/SKILL.md
```

子变更实现时以 roadmap 的 session scope 为准；上述是总范围，不要求单个 PR 一次修改全部文件。

### 3.2 数据库变更

无。

### 3.3 公共合同变更

- 新增 artifact metadata schema、eval case schema 和 guardrail policy schema。
- 新建记录使用新 schema；旧记录保持可读，不要求迁移。
- 新增 `triage` 自然语言意图；是否公开为 slash command 由平台能力决定。

---

## 4. 技术决策

| 决策点 | 选择 | 原因 |
|--------|------|------|
| Intent artifact | 复用 `design-brief.md` | 避免与现有 brainstorm 产物重复 |
| Plan artifact | 复用 `tasks.md + test-spec.md` | 保留实现和验证的分离 |
| Metadata 形式 | Markdown 顶部有限字段 + JSON schema/checker | 人和 Agent 可读，同时可机械检查 |
| Source of truth | 每种 artifact 显式声明 repo/GitHub/external | 避免双向同步时权威不清 |
| Eval 分层 | validate-only/offline 必跑，live 可选非阻塞起步 | 控制成本与非确定性 |
| 治理事实源 | `guardrail-policy.json` | Skill/rules 只解释，脚本/CI/adapter执行 |
| Maintain 入口 | `triage` 生成 draft design-brief | 直接复用现有 Plan/Design 流程 |
| 自动化权限 | diagnose/draft 默认允许；publish/production 仍走现有人工门禁 | 保持人类对判断性和高风险动作负责 |

---

## 5. 风险与注意事项

- ⚠️ **CI/自动化合同变更**：本变更触及 CI/eval/guardrail 行为，必须保持 Full SDD，具体 adapter 启用前需人工确认。
- ⚠️ **安全控制误判**：guardrail false positive 可能阻塞安全内环；每个 block 必须给出原因、证据和批准路径。
- ⚠️ **外部写入边界**：triage 默认只读和 draft；创建 Issue/PR、回滚、部署仍受 issuePolicy、finishMode 和人工门禁约束。
- ⚠️ **兼容性**：新 checker 不得把历史记录当作失败样本；必须区分 legacy 和新 schema。

### 5.1 上线与回滚

| 项 | 内容 |
|----|------|
| 兼容性影响 | 新记录增加 metadata/schema；旧记录保持 legacy 读取 |
| 灰度方式 | S1/S2/S3 分 PR；live eval 和 event adapter 首期非阻塞/默认关闭 |
| 回滚方案 | 分阶段回滚 schema/checker/adapter；保留原 router 和 workflow fallback |
| 数据修复 | 无数据库数据；若生成错误 draft artifact，删除/关闭该 draft 并保留审计记录 |
| 监控指标 | eval pass/flakiness/cost、artifact drift、guardrail block/false-positive、triage conversion、repeat incident |

---

## 6. Agent Harness

| 项 | 内容 |
|----|------|
| Agent 可见证据 | schema 校验输出、fixture/eval 结果、guardrail allow/block、framework check、Git diff、PR checks |
| 必跑验证命令 | `bash scripts/check_framework.sh`；各阶段新增定向 Python checker |
| 日志/指标/trace 入口 | eval JSON result、CI check run、artifact verification log；live telemetry adapter 首期可选 |
| UI/浏览器验证入口 | 不适用 |
| 失败自诊断入口 | checker 返回具体 artifact/case/control ID、期望与实际、批准或降级路径 |
| 不可见信息/人工确认 | 模型供应商运行成本、企业平台设置、生产授权和真实告警系统 |
| 可沉淀的规则/知识 | eval case 编写、跨平台 capability、artifact migration、低噪声 triage |

---

## 7. Goal Contract

| 项 | 内容 |
|----|------|
| Goal | 将现有 SDD 建成 Agent 可持续工作的研发运行环境：上下文可获取、技能可复用、产物可交接、行为可评测、动作可治理、审查有人机分层、决策可追责 |
| Done Signal | roadmap §5 总体验收全部满足，framework check 与离线 eval 通过，live/event 能力未启用时明确报告 capability 状态 |
| Guardrails | 不增加 Inline 强制文档；不迁移历史记录；不删除/弱化现有测试与风险门禁；不把 unsupported adapter 伪装为已执行；不自动越过生产/权限/外部写入授权 |
| Fallback | schema/checker 不兼容则回退 legacy 读取；live eval 不稳定则保持非阻塞；hook 不可用则使用 CI gate；triage 噪声高则关闭 event adapter 保留手动入口 |
| Memory | 新事故进入 regression test/eval；重复误判进入 policy/fixture；跨平台差异进入 knowledge/docs |

### 7.1 Loop Runtime

| 能力 | 内容 |
|------|------|
| Automation | CI path trigger、schedule 和事件 adapter；默认只运行 validate/diagnose/draft |
| Worktree isolation | 子变更和 live eval sandbox 应隔离；普通文档验证不强制 |
| Skills / knowledge | ai-code-copilot skill、项目 rules/packs、归档 knowledge；记录实际版本 |
| Plugins / connectors | GitHub 可选；监控/Issue connector 通过 capability contract 接入 |
| Maker-checker subagents | live eval 与最终 review 可使用独立 checker；不将 subagent 设为所有任务默认要求 |

---

## 8. Domain Check

不适用业务 DDD；本变更的核心不变量是：artifact 上游关系可追踪、控制层级不降级、unsupported capability 不得宣称执行、生产和高风险动作必须由人类授权。

---

## 9. 待澄清事项

无。用户于 2026-08-24 确认：整个变更按 Complex 管理并拆成 S1/S2/S3；live model eval 首期可选、非阻塞；triage 首期只支持 CI/GitHub 事件样例，不接真实生产监控平台。

---

## 10. 验收标准

- [ ] Artifact chain 可以机械发现缺失上游、hash 漂移、非法状态和未知 source of truth。
- [ ] Agent eval 能稳定验证至少 15 个关键路由与治理场景。
- [ ] 至少两个确定性 guardrail 有 RED/GREEN fixture，且 block 输出包含批准路径。
- [ ] triage 能从 fixture event 生成合法 draft design-brief，且不能直接 publish/deploy。
- [ ] 指标定义覆盖 lifecycle/eval/guardrail/incident，并明确反 Goodhart 组合。
- [ ] README 中英文、docs、router、skill、legacy fallback 和自检保持一致。

---

## 11. 测试策略

- P0：schema、artifact chain、policy、guardrail 和 eval runner 的 deterministic contract tests。
- P1：router/skill/workflow 的真实提示 eval，至少覆盖安全、升级、无合同不编码、验证和外部动作。
- P2：用 fixture event 走 triage → draft design-brief → validate 的端到端测试。
- 不测试：真实生产告警、真实生产回滚、企业 managed settings；首期仅验证 adapter/capability 合同。
- 验证命令：`bash scripts/check_framework.sh`
