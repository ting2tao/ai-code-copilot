<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:tasks
artifactType: tasks
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s1:spec
upstreamHash: sha256:720319fb33aeb12c5dad81513ba541a11f813fb55553aef88367f4142400a289
-->

# S1 Tasks：Artifact Chain + Agent Eval Baseline

## T6 — 2026-09-03 R6/main 集成增量（用户“继续”）

- [x] R6 mixed metadata fixtures RED → GREEN，11 个 fixtures 通过；不强制附属 Markdown 产物化。
- [x] 使用 main 的 should_activate/classify_activated 适配 Native/Compact/Full；21 cases 通过。
- [x] 4 个 model-first eval 回归；policy/case 同时引用已删除模块的反例 RED → GREEN。
- [x] VERSION 0.2.0，双语 README/AGENTS 同步；版本文档检查动态读取 VERSION，保留 main 安装与同步门禁。
- [x] 集成后独立 Stage 1/Stage 2 重审通过；补齐 eval 输入边界、guardrail policy selector 与 binary-marker 精确识别，37 tests GREEN。
- [ ] 当前快照人工批准与 commit/PR。
- [x] Stage 2 首轮两个 Important：untracked 行为文件版本假绿与畸形 facts 未捕获异常，分别补真实 RED → GREEN 回归。

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
- [x] 运行定向测试、`git diff --check` 和全量 framework check。
- [x] 回填 log、summary、parent tasks/log，并执行本地 Spec Compliance/Code Quality review。
