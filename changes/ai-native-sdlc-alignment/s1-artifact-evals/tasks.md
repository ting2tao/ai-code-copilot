<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:tasks
artifactType: tasks
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s1:spec
upstreamHash: sha256:c8d85cfea2d4422e223fe9a712679e404b7b725c170b5e359c9d9ad9635c3c12
-->

# S1 Tasks：Artifact Chain + Agent Eval Baseline

## T1 — 失败合同

- [x] 在 `check_framework.sh` 先声明新 policy/scripts/evals 与命令，运行得到缺失文件 RED。
- [x] 记录 RED command、exit code 和实际错误。

## T2 — Artifact policy 与 checker

- [x] 扩展 `config/workflow-policy.json` artifact 合同。
- [x] 新增 `scripts/check_artifact_chain.py`。
- [x] 新增 valid/invalid/legacy fixtures。
- [x] 验证 invalid RED、valid/legacy GREEN、transition RED/GREEN。

## T3 — Templates 与 workflows

- [x] 更新 Full templates 和 Quick Card metadata。
- [x] 更新 Full/Compact/Review workflow。
- [x] 为当前 S1/parent change 建立具体 artifact chain。

## T4 — Agent eval baseline

- [x] 新增 `evals/schema.json`, `evals/README.md`, `evals/cases/core.json`。
- [x] 新增 `scripts/run_agent_evals.py`。
- [x] 18 个 offline cases GREEN；invalid result RED。

## T5 — 集成与审查

- [x] 更新 `scripts/check_framework.sh` 与 legacy fallback 最小合同。
- [ ] 运行定向测试、`git diff --check` 和全量 framework check。
- [ ] 回填 log、summary、parent tasks/log，并执行 Spec Compliance/Code Quality review。
