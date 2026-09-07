<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:test-spec
artifactType: test-spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s1:spec
upstreamHash: sha256:720319fb33aeb12c5dad81513ba541a11f813fb55553aef88367f4142400a289
-->

# S1 Test Spec：Artifact Chain + Agent Eval Baseline

## 2026-09-03 R6/main 新回归

- `--fixtures tests/fixtures/artifact-chain`：mixed-default/mixed-required/mixed-malformed 必须拒绝；mixed-attachment 允许。原 legacy 默认 SKIP、legacy-required FAIL、原链/模板断言不变。
- `python3 -m unittest discover -s tests -p 'test_agent_evals.py'`：Native/激活路由、tier/modules/humanGate/writesBeforeContract 偏差、已删除 module、external 结果偏差。
- `run_agent_evals.py ... --self-check-external`：21 个当前 policy v2 cases；历史 Inline 结果不得冒充当前 live 结果。
- `check_model_first_versioning.py .`：VERSION 0.2.0 和双语版本描述一致；原 main 的 Native、安装覆盖和同步检查保留。
- `test_model_first_versioning.py`：仅新增未跟踪 `scripts/new_behavior.py` 且 VERSION 不变时，版本行为检测必须为 true。
- eval 畸形 facts：signals/risks/unsupportedCapabilities、files、布尔路由字段和字符串意图字段须返回稳定诊断，不得泄漏 TypeError。
- eval case 合同：`id` 必须为匹配 schema 的字符串；expected tier/modules/humanGate/writesBeforeContract 及可选 capabilityStatus/promotion 必须在评分前完成类型与枚举校验。
- guardrail policy selector：risks/operations/taskModes 的拼写必须属于 checker 支持的封闭集合，防止策略拼写错误静默关闭控制；paths/patterns 保持可扩展。

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
| Artifact current chain | PASS | `PASS 17 artifacts` |
| Artifact fixtures/templates/合法 transition | PASS | `PASS 11 artifact-chain fixtures`; `PASS 9 artifact templates`; `PASS transition draft -> approved` |
| 非法 transition | RED | exit 1；`illegal artifact transition: draft -> finished` |
| Offline Agent eval | PASS | `PASS offline policy oracle (21 cases)` |
| External scorer self-check | PASS | `PASS external scorer self-check (21 cases)` |
| Invalid external result | RED | exit 1；检测错误 tier/module/`writesBeforeContract=True` 及缺失结果 |
| Full framework check | PASS | `37 tests OK`; `ai-code-copilot framework check passed` |
