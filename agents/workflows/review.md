# Workflow Module: review

Auditable review 需要持久合同。原生执行收到 review/commit/publish 请求时先自动激活并执行 `Native -> Compact`，再开始审查。

## Stage 0: Artifact Chain

- 对新建/升级记录运行 `scripts/check_artifact_chain.py`，验证 ID 唯一、上游存在、source of truth 唯一、hash 无漂移、状态合法。
- Full/新 Compact 缺 metadata 或使用 approved/active 的 `upstreamHash: pending` 时为 FAIL。
- legacy 记录允许明确 SKIP，但不得把新记录伪装成 legacy；显式 `--require-chain` 时缺 metadata 必须 FAIL。
- Artifact Chain 未通过不得进入 Spec Compliance。

## Stage 1: Spec Compliance

- Compact：对照 Quick Card 的 Goal、Scope、Non-goals、Acceptance、风险、Harness 和实际 diff/commits/evidence。
- Full：逐条对照 spec/tasks/test-spec 和实际代码。
- 验证 promotion 时机、顺序、provenance、证据复制和 material confirmation。
- 范围外实现、验收缺证据、未执行应升级 trigger 均为 FAIL/NEEDS_INFO。

## Stage 2: Code Quality

在 Spec Compliance PASS 后独立检查安全、正确性、异常、并发、可维护性、Agent 可读性、Harness、Goodhart 风险和 Git/Issue contract。

- Guardrail：对照 `config/guardrail-policy.json` 检查实际 event/diff 的 eventHash、control IDs、adapter coverage、批准证据与降级补位；CLI PASS 不是人类身份认证，也不是语义安全证明。未解决 block/ask 不得 PASS；不可用 hook 不得报已执行。
- 消融审查：新增抽象/规则/产物有无当前 Acceptance 或 Guardrail 依据？对可疑项比较直接实现或移除后的证据，固定验收、单因素改变；无证据的预留扩展点建议删除/延后。区分实测与反事实；安全门禁只在隔离测试中消融。复用现有 Review record，不加独立报告。

## Agent / Harness 审查纪律

- 分别核对实际 outcome（产物/用户行为/环境状态）与 trace（调用、交接、门禁、失败）；只看到脚本 exit 0 或 Agent 文字报告不能完成验收。
- 明确记录 reviewer 身份与方式：本地 self-review、独立 Agent、人工；不得把 self-review 写成独立审查。独立 evaluator 也需用反例及人工判例校准，未授权不自动启动多个 Agent。
- 消融保留固定 model/version、policy/revision、测试集和验收基线；同时比较质量、失败率和成本/时延。模型升级后复查原支架的必要性，不因新模型宣传就删门禁。
- 检查恢复点是否包含已发生副作用、未决批准和下一步验证；检查平台支持、实现、验证与启用有无混淆。完整来源与边界见 `docs/harness-engineering.md`。

## Results

- Compact 写 Review record；Full 写 log Review outcomes。
- Important/Critical correction 或 residual risk 使 Compact 在修复/接受前升级 Full。
- Issue lifecycle 只按 `issuePolicy` 当前阶段检查；publish 时校验 close target 为有票时 `workIssue`，或 `manual`/no-Issue 时 `none`，后者不得出现 closing keyword。
- 没有新鲜证据不得 PASS。
