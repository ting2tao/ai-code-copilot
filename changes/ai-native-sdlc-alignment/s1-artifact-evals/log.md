<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:log
artifactType: log
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s1:spec
upstreamHash: sha256:c8d85cfea2d4422e223fe9a712679e404b7b725c170b5e359c9d9ad9635c3c12
-->

# S1 Log：Artifact Chain + Agent Eval Baseline

## Summary

| 字段 | 内容 |
|------|------|
| 状态 | in-apply |
| 上游 | parent Complex Spec / Roadmap S1 |
| 分支 | feat/ai-native-sdlc |
| workIssue | pending（on-publish） |
| 确认 | 继承用户 2026-08-24 的 Complex Spec 确认 |
| commit | 无 |

## Decisions

- artifact contract 作为 `workflow-policy.json` 的向后兼容扩展，暂不升级顶层 policy version。
- Full artifact 使用统一 HTML metadata block；Quick Card 复用既有 YAML front matter。
- offline eval 是可重复的 policy oracle；真实模型输出通过外部 results 文件评分，runner 不执行任意 provider command。

## Verification

### 2026-08-24 - S1 contract RED

```text
command: bash scripts/check_framework.sh
exit code: 1
output: FAIL: missing file: scripts/check_artifact_chain.py
```

### 2026-08-24 - Artifact Chain GREEN

```text
command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --change-dir changes/ai-native-sdlc-alignment --require-chain
exit code: 0
output: PASS 12 artifacts

command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --templates changes/templates --fixtures tests/fixtures/artifact-chain --transition draft:approved
exit code: 0
output: PASS 7 artifact-chain fixtures; PASS 9 artifact templates; PASS transition draft -> approved
```

### 2026-08-24 - Artifact illegal transition RED

```text
command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --transition draft:finished
exit code: 1
output: artifact-chain: FAIL: illegal artifact transition: draft -> finished
```

### 2026-08-24 - Agent eval GREEN/RED

```text
command: python3 scripts/run_agent_evals.py --policy config/workflow-policy.json --schema evals/schema.json --cases evals/cases --self-check-external
exit code: 0
output: PASS offline policy oracle (18 cases); PASS external scorer self-check (18 cases); live capability=external-results-required, mode=non-blocking

command: python3 scripts/run_agent_evals.py ... --results tests/fixtures/agent-evals/invalid-results.json
exit code: 1
output: rejected wrong tier, wrong module, writesBeforeContract=True, and missing results
```

### 2026-08-24 - Framework integration GREEN

```text
command: bash scripts/check_framework.sh
exit code: 0
output: progressive-sdd checks passed; artifact/eval checks passed; ai-code-copilot framework check passed
```

## Review

待执行。
