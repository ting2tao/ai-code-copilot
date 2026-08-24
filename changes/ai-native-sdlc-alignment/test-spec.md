<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:test-spec
artifactType: test-spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:spec
upstreamHash: sha256:a9dee5165c570806487c2e4ccf9ef1ecedef3e61b6df6e133e79c6bcb49a1f84
-->

# 测试 Spec：ai-native-sdlc-alignment

> **关联 Spec**：`spec.md`
> **关联 Roadmap**：`roadmap.md`
> **状态**：草稿；每个子变更实施前补充精确 RED/GREEN 命令和 fixture 路径
> **测试原则**：prompt、policy、schema、模板和 workflow 行为都必须先有失败合同，再修改实现转绿。

## 0. 项目测试上下文

| 模块路径 | 技术栈/规则包 | 测试框架 | 全量测试命令 | 定向测试命令 | 覆盖率命令/报告 |
|----------|---------------|----------|--------------|----------------|-----------------|
| repository root | Markdown/Bash/Python/JSON | framework self-check + fixtures | `bash scripts/check_framework.sh` | 各新增 Python checker | 不适用；按 case/contract coverage 统计 |

## 1. Agent Harness

| 项 | 内容 |
|----|------|
| Agent 可见证据 | checker exit code、case ID、expected/actual、artifact path、guardrail decision、framework output |
| 必跑验证命令 | `bash scripts/check_framework.sh` |
| 可观测信号 | eval pass/flaky/cost、artifact drift、control allow/block/override、triage outcome |
| 失败自诊断入口 | 每个失败必须输出 schema/control/case ID 和修复/批准路径 |
| 人工确认项 | live model 凭据/成本、外部平台 adapter、生产监控和发布权限 |

## 2. Loop Evidence

| 项 | 内容 |
|----|------|
| Goal observed | 证明新能力能机械约束生命周期，而不只是增加文档文字 |
| Done Signal | 所有 deterministic suites GREEN，live/adapter 未启用时返回明确 capability 状态 |
| Guardrail checks | 不删除 legacy fixtures，不放宽 Full risk，不把 unsupported 当 PASS，不让 triage 绕过人工门禁 |
| Fallback exercised | live eval → non-blocking；hook unsupported → CI；schema legacy → compatibility reader |
| Memory update | 新事故/误路由/误拦截分别进入 eval case、policy fixture 或 knowledge |

## P0 核心合同测试

### TC-P0-01：Artifact Chain 非法上游

**操作**：构造缺失 upstream、hash 漂移和非法 status transition 的新 schema fixtures。
**预期结果**：checker 非零退出并指出 artifact ID、字段和期望；合法新链和 legacy fixture 通过。
**RED 证据**：实施 S1 时记录。
**GREEN 证据**：实施 S1 时记录。

### TC-P0-02：Agent eval schema 与离线 runner

**操作**：运行 validate-only/offline eval。
**预期结果**：无网络和模型凭据时至少 15 个 case 可被解析、评分并生成结构化报告；非法 case RED。
**RED/GREEN 证据**：实施 S1 时记录。

### TC-P0-03：高风险路由与单向升级

**操作**：运行 security、permission、database、deployment、state-machine 和 mid-task promotion cases。
**预期结果**：全部选择 Full；promotion 在继续编辑前发生；没有合同不得写代码。

### TC-P0-04：确定性 Guardrail

**操作**：对 secret/sensitive diff、protected path、fix 中测试变更运行 fixtures。
**预期结果**：违规 RED 且给出原因/批准路径；合法变更 GREEN；override 产生审计记录。

### TC-P0-05：Triage 权限边界

**操作**：输入 CI failure/incident fixture。
**预期结果**：生成合法 draft design-brief；不执行 apply、push、PR、deploy、rollback 或生产写入。

## P1 集成测试

### TC-P1-01：S1→S2→S3 合同兼容

验证下游只凭 roadmap 和上游 log.summary 即可解析 schema/policy，完整过程日志不是隐含依赖。

### TC-P1-02：Router/Skill/Legacy fallback 一致性

验证 router、skill、workflow modules、SessionStart 菜单、legacy `copilot-prompt.md` 和 README 命令集合不漂移。

### TC-P1-03：README 双语同步

验证 AI-native、artifact/eval/guardrail/triage 核心章节在 README.md 和 README-CN.md 同步存在。

## P2 端到端测试

### TC-P2-01：事件到可审批 Intent

以 fixture CI failure 触发：event validate → deterministic threshold → read-only diagnosis → draft design-brief → artifact chain validate → human triage gate。验证没有外部写入。

## 不测试项

| 项目 | 原因 | 风险接受人/确认方式 |
|------|------|-------------------|
| 真实生产监控和自动回滚 | 本变更不授权生产接入或生产动作 | 用户确认 Spec |
| Claude managed settings/Claude Tag | 平台专属且不是核心依赖 | 用户确认 Spec |
| live eval 作为 blocking gate | 首期先收集稳定性与成本基线 | 用户确认 Spec |
| 历史 changes 批量迁移 | 明确采用 legacy compatibility | 用户确认 Spec |

## 实际测试结果

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `bash scripts/check_framework.sh` | PASS | `progressive-sdd: policy and module checks passed`；`ai-code-copilot framework check passed`；exit code 0 |
