<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s1:log
artifactType: log
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s1:spec
upstreamHash: sha256:720319fb33aeb12c5dad81513ba541a11f813fb55553aef88367f4142400a289
-->

# S1 Log：Artifact Chain + Agent Eval Baseline

## 2026-09-03 R6 修复与 main 集成（当前增量）

- 授权：用户在修复 P2、适配 main、重审后提交 PR 建议后回复“继续”；parent Spec 已 Reverse Sync。workIssue #36，关闭目标仅 S1/S2。
- 根因：validate_change 只检查全目录零 artifact，静默跳过缺 metadata 的单个标准文件。先加 4 个 fixtures，出现 `mixed-default expected FAIL, got PASS 1 artifacts`，再增加标准 artifact 缺失列表检查，11 fixtures GREEN；辅助 notes.md 不需 metadata。
- 保存完整未提交安全快照 `093bea9a7773063d5d38bbf34cec2418b20b6e61`（stash，含 untracked）。普通三方 merge --no-commit origin/main；基线 d5b44d4，main ee028aa4。用原快照/base/main 合并 S1/S2 内容，保留 main 侧安装、同步、Native 激活与 policy v2；尚未创建 merge commit。安全快照保留，不 drop。
- eval 集成 RED：旧 runner 导入 classify 失败（main 已拆 should_activate/classify_activated）。改用两阶段 oracle；risk facts/检测信号一致进入风险与人工门禁；21 cases GREEN。新增 4 个 unittest，其中“policy 与 case 同时指向已删除 module”先失败，再增加实际文件存在检查后 GREEN。
- 版本门禁 RED：行为变化未 bump；升 VERSION 0.2.0 并同步双语文档后，旧 checker 硬编码 0.1.0 再次失败。改为 read_version 动态校验后 GREEN，不放宽文档一致性要求。
- 已运行合并后 framework：28 guardrail tests、11 fixtures、9 templates、21 oracle/scorer、model-first version、local install overwrite 均通过。安装测试 cp 遇 fsmonitor socket 输出两条“not copied”提示，测试 exit 0，非个人安装执行。随后新增的 4 eval tests 另行 GREEN，最终全量待重跑。
- 先前一次检查与 stash 启动时间相邻，不作为集成后证据；上述合并后独立新运行才用于判断。所有行为变更都来自当前验收或实际 RED，无新增通用迁移/审批/编排抽象。
- 当前暂停在独立审查与精确差异批准前；S3/live eval/真实宿主启用不在范围内。

### Stage 2 首轮 Important 修复

- 独立 reviewer `/root/final_quality_review`：0 Critical、2 ordinary Important，实施质量按阈值 PASS，但指出两个当前 Harness 边界；发布因人工 diff ask 仍 NEEDS_INFO。
- I1 版本门禁只用 tracked diff。新增真实临时 Git 仓库测试，仅创建 untracked `scripts/new_behavior.py` 且不 bump VERSION；修复前 `behavior_changed_from_base` 返回 false。最小修复增加同一行为路径的 `git ls-files --others --exclude-standard`，Git 查询异常按 fail-closed 视为行为变化；回归 GREEN。
- I2 eval facts 类型不受约束。新增 signals=1、risks=字符串、files="6"、布尔字段="yes" 四个反例；修复前 1 个 uncaught TypeError + 3 个无诊断。最小修复在 set/数值比较前验证实际消费字段，返回稳定 case errors；5 eval tests GREEN。
- 无新抽象：直接扩展现有两个边界与测试，未新增 schema 版本、路由层或异常框架。由于实现已在首轮 Stage 2 后改变，必须重新执行独立 Stage 1/2，首轮报告不作为最终实现 PASS。

### 2026-09-07 最终独立重审与输入边界收口

- 独立 Stage 1 reviewer `/root/final_spec_rereview` 对 main 集成后的实现复验 R1–R6、I1/I2、model-first 兼容与 fail-closed 行为，结论 PASS。
- 独立 Stage 2 reviewer `/root/release_quality_final` 先发现三个相邻输入边界：数值 case id、未校验的可选 expected 字段、guardrail selector 拼写错误。均以现有 validator 的最小扩展修复：新增反例先 RED，再进入永久测试 GREEN；未引入新的 schema 层或策略 DSL。
- Stage 2 对最终修复重审：Spec/Code Quality 均 PASS，0 Critical、0 Important、0 Minor；Git/Issue READY，Publish 仅因最终快照 `protected-path-edit` 与 `high-risk-human-gate` 尚待人工批准而 NEEDS_INFO。
- 新鲜验证：`python3 -m unittest discover -s tests` 为 37 tests / OK；framework 为 30 guardrail、6 eval、1 version test、11 artifact fixtures、9 templates、21 offline oracle/scorer 全通过；当前 Artifact Chain 为 17 artifacts。
- 旧 eventHash 在任何文件变化后失效，不沿用历史授权。下一步只对完成记录后的最终暂存快照重新扫描并请求精确批准；批准前不 commit/push/PR，不启用 hook/CI。

## Summary

| 字段 | 内容 |
|------|------|
| 状态 | reviewed |
| 上游 | parent Complex Spec / Roadmap S1 |
| 分支 | feat/ai-native-sdlc |
| workIssue | pending（on-publish） |
| 确认 | 继承用户 2026-08-24 的 Complex Spec 确认 |
| commit | `6be53b8 feat(sdlc): add artifact chain and agent eval baseline` |

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

### Spec Compliance

**结论**：PASS

- Artifact policy、checker、模板 metadata、Full/Compact/Review 集成均在确认范围内。
- 18 个 eval cases 超过最低 15 个，覆盖 tier、human gate、promotion、No Contract No Code 和 unsupported capability。
- Inline 不落盘、legacy 默认 skip、live result 非阻塞和无外部写入 Guardrails 均保持。

### Code Quality

**结论**：PASS

- 两个 Python runner 只使用标准库，不联网、不读取凭据、不执行任意 provider command。
- schema/manual validator 有漂移检查；artifact parser 拒绝重复键、非法 source/status/type/hash/transition。
- `shellcheck scripts/check_framework.sh` 只报告既有 SC2317/SC2016 信息，新增区段无新 finding。

### GitHub Readiness

**结论**：NEEDS_INFO

- branch 与 commit 合同 READY：`feat/ai-native-sdlc`；`6be53b8 feat(sdlc): add artifact chain and agent eval baseline`。
- `workIssue` 依据 `issuePolicy=on-publish` 仍为 pending；本地 commit 合法，push/PR 前必须解析。

### Harness / Loop Readiness

**结论**：READY

- 新鲜证据：current chain、fixtures、templates、transition、offline eval、external scorer 和 framework check。
- live model eval 未执行，明确报告 `capability=external-results-required, mode=non-blocking`，未伪造 PASS。
