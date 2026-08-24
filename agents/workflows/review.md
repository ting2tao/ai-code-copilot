# Workflow Module: review

Auditable review 需要持久合同。Inline 收到 review/commit/publish 请求时先执行 `Inline -> Compact`，再开始审查。

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

## Results

- Compact 写 Review record；Full 写 log Review outcomes。
- Important/Critical correction 或 residual risk 使 Compact 在修复/接受前升级 Full。
- Issue lifecycle 只按 `issuePolicy` 当前阶段检查；publish 时校验 close target 为有票时 `workIssue`，或 `manual`/no-Issue 时 `none`，后者不得出现 closing keyword。
- 没有新鲜证据不得 PASS。
