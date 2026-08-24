<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:test-spec
artifactType: test-spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: git:6be53b8
upstream: ai-native-sdlc-alignment:s1:spec
upstreamHash: sha256:fd8356f19b5553e2f1acca1eca4e1efca62991545043a5eb91fb2ae7a28f21dd
-->

# S1 Test Spec：Artifact Chain + Agent Eval Baseline

## P0

| ID | 场景 | 预期 |
|----|------|------|
| A1 | 新 chain 合法 | PASS |
| A2 | upstream 缺失 | FAIL，指出 artifact/upstream ID |
| A3 | upstream hash drift | FAIL，输出 expected/actual |
| A4 | 非法 source/status/type | FAIL，指出字段 |
| A5 | legacy 无 metadata | 默认 SKIP/PASS；`--require-chain` FAIL |
| A6 | 合法/非法 status transition | 分别 PASS/FAIL |
| E1 | eval schema/cases validate | 15+ cases PASS |
| E2 | offline policy oracle | expected tier 与 policy 一致 |
| E3 | external results 完全匹配 | PASS |
| E4 | writes-before-contract 或 tier 偏差 | FAIL |

## 验证命令

```text
python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --fixtures tests/fixtures/artifact-chain
python3 scripts/run_agent_evals.py --policy config/workflow-policy.json --cases evals/cases
bash scripts/check_framework.sh
```

## Guardrails

- 不通过删除 legacy fixture、放宽 Full risk 或降低 case 数量转绿。
- offline eval 报告必须标为 policy-oracle baseline，不冒充 live model 结果。
- 所有脚本只用 Python 标准库，默认不联网、不执行任意 adapter command。

## 实际结果

| 命令/场景 | 结果 | 证据摘要 |
|-----------|------|----------|
| Artifact current chain | PASS | `PASS 12 artifacts` |
| Artifact fixtures/templates/合法 transition | PASS | `PASS 7 artifact-chain fixtures`; `PASS 9 artifact templates`; `PASS transition draft -> approved` |
| 非法 transition | RED | exit 1；`illegal artifact transition: draft -> finished` |
| Offline Agent eval | PASS | `PASS offline policy oracle (18 cases)` |
| External scorer self-check | PASS | `PASS external scorer self-check (18 cases)` |
| Invalid external result | RED | exit 1；检测错误 tier/module/`writesBeforeContract=True` 及缺失结果 |
| Full framework check | PASS | `ai-code-copilot framework check passed` |
