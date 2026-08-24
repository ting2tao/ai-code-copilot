<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:spec
artifactType: spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: git:6be53b8
upstream: ai-native-sdlc-alignment:roadmap
upstreamHash: sha256:9ac6664cf068b955e9529307b7951d439e95757d8f36a0a7ff6b94d8a7be6ae6
-->

# S1 Spec：Artifact Chain + Agent Eval Baseline

> **状态**：[x] 已确认（继承 parent Complex Spec 2026-08-24 确认）
> **档位**：Standard / Full SDD
> **上游**：`../spec.md`, `../roadmap.md` S1
> **分支**：`feat/ai-native-sdlc`
> **确认范围 Hash**：`sha256:8832adc19fd6af99ec97f6c7bda1a7cbcab6f5f1d7cf761f6e7133a17ca2dd09`（动态 Artifact 字段归一化；继承 parent confirmation）

## Goal Contract

| 项 | 内容 |
|----|------|
| Goal | 建立阶段产物机器关系和 Agent 行为 eval 基线，为 S2/S3 提供可回归地基 |
| Done Signal | artifact checker 新链/legacy/非法 fixtures 通过；至少 15 个 offline eval cases 通过；全量 framework check 通过 |
| Guardrails | Inline 不落盘；Compact 只加最小 metadata；历史记录不迁移；offline eval 不宣称等同 live model eval；不执行网络和外部写入 |
| Fallback | 新 metadata 解析失败时保留 legacy skip；外部 live result 缺失时明确报告 capability unavailable，不伪造 PASS |
| Memory | artifact schema 兼容与高辨识度 eval case 设计进入后续 docs/knowledge |

## 功能范围

1. 在 `workflow-policy.json` 增加 artifact version/type/status/source/upstream/transition 合同，保留 policy version 1 兼容。
2. 新增 `check_artifact_chain.py`，支持模板 marker、活动 change chain、legacy skip 和显式 transition 检查。
3. Full 模板增加统一 artifact metadata block；Quick Card 在既有 front matter 加最小字段。
4. Full/Compact/Review workflow 说明 artifact chain 生成、同步和审查门禁。
5. 新增 eval JSON schema、至少 15 个 cases 和 `run_agent_evals.py`；offline 计算 policy oracle，外部 live results 独立评分。
6. `check_framework.sh` 将 artifact/eval offline checks 作为硬门禁。

## 非目标

- 不实现 S2 guardrail policy、PreToolUse hook 或 CI workflow。
- 不实现 S3 triage、生产事件 connector 或 lifecycle metrics。
- 不调用真实模型，不引入第三方 Python 包。

## 验收

- [ ] 新 artifact chain 能检测缺失 upstream、hash drift、非法 source/status/transition。
- [ ] legacy change 无 metadata 时默认跳过且 `--require-chain` 可阻塞。
- [ ] 15+ cases 覆盖 tier、promotion、human gate、No Contract No Code 和 unsupported capability。
- [ ] external results scorer 能识别 tier/module/human gate/writes-before-contract 偏差。
- [ ] `bash scripts/check_framework.sh` PASS。
