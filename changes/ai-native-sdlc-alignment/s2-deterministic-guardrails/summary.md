<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s2:summary
artifactType: summary
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s2:spec
upstreamHash: sha256:40e32575c0a9b9f9945c46817265b919f544ab4a9a48aa3bddd65dd314ff6f5f
-->

# S2 Summary：Deterministic Guardrail Layers

- 状态：R1–R6、输入边界与 policy selector 已修复，独立 Stage 1/2 PASS；等待当前快照人工批准与 commit/PR
- Policy version：v1
- 公开合同：三层控制、标准 event、adapter capability、approval evidence
- 兼容：Claude 有 PreToolUse adapter；Codex 明确 unavailable/degraded 并使用 fallback
- 安全：secret 不可普通 override；所有匹配内容必须 redact
- 验证：30 guardrail tests PASS（含永久 RED → GREEN 与隔离消融）；实际审批须依据最终 eventHash，未伪造 PASS
- 集成：37 tests、17 artifacts、21 offline evals、framework check、hook shellcheck 均 PASS
- 消融：复用 YAGNI/test/review/log，固定验收单因素对比；不新增引擎/审批系统/报告
- 外部状态：工作 Issue #36（standalone、closeTarget=workIssue）；用户已授权 ting2tao 提交 PR 到 main，独立审查后执行；不合并/启用 hook/CI
- 最新复核：独立 Stage 1 PASS；最终 Stage 2 PASS（0 Critical / 0 Important / 0 Minor）；Publish 仅因最终快照人工门禁 NEEDS_INFO
- main 集成：用户“继续”后已解决 ee028aa4（PR #35）的三方冲突并本地验证；保留 Native/policy v2/安装同步合同，VERSION 0.2.0，Git merge 尚未提交
- 修复边界：Git snapshot hash 绑定 base、完整 patch 与扫描文件字节/权限；event JSON 仅为调用方声明；非 Git 输入拒绝 Git-only flags；扫描与执行不具备原子锁
- 官方原则：按需 context、恢复/副作用、outcome/trace、控制面边界、模型升级后消融；来源与日期见 harness 文档
- 下游：S3 将消费 guardrail decision/evidence，但不依赖单一平台 hook
