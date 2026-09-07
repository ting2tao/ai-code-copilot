<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s2:tasks
artifactType: tasks
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s2:spec
upstreamHash: sha256:40e32575c0a9b9f9945c46817265b919f544ab4a9a48aa3bddd65dd314ff6f5f
-->

# S2 Tasks：Deterministic Guardrail Layers

## T1 — 合同 RED

- [x] 在 `check_framework.sh` 先声明 policy/checker/adapter/fixtures，运行得到缺失文件 RED。
- [x] 记录 command、exit code 和首个实际错误。

## T2 — Policy 与标准事件

- [x] 新增 `config/guardrail-policy.json` 三层控制与 capability matrix。
- [x] 新增 `scripts/check_guardrails.py`，校验 policy 和标准 event。
- [x] 输出只包含 control ID、action、path、owner/route，不回显 matched content。

## T3 — Deterministic RED/GREEN

- [x] 增加 secret、PII、protected path、fix-test integrity fixtures。
- [x] 增加未批准 RED、批准 GREEN 和不可覆盖 secret RED。
- [x] 增加 high-risk Human Gate RED/GREEN。

## T4 — Adapter 与 fallback

- [x] 新增 Claude `PreToolUse` Write/Edit adapter 和 hook fixture。
- [x] 支持 Git diff 模式供 local/CI 复用。
- [x] 明确 Codex unavailable/degraded capability 和 fallback，禁止伪造 hook PASS。

## T5 — Workflow 集成与审查

- [x] 更新 Full/debug/review/finish/security 与 legacy fallback 最小合同。
- [x] 扩展 progressive/framework checker 防止合同漂移。
- [x] 运行定向 RED/GREEN、py_compile、bash -n、artifact chain、git diff check 和全量 framework check。
- [x] 用户增补：消融原则接入现有 design-brief/YAGNI、Full/test/review 与 Code Quality reviewer；四个控制做隔离 baseline/removed/restored 对照。
- [x] 最终独立 Stage 1/Stage 2 review 通过；adapter 仍仅为仓库内合成验证，未启用。
- [ ] 当前最终快照人工批准与 commit/PR。

## T6 — 2026-09-03 官方原则与用户要求的审查

- [x] 核验 OpenAI/Anthropic 官方来源并标记日期；复用 harness/loop、Full/review、eval README 和 security 说明。
- [x] 2 个新增测试方法保护原则与平台能力说明；19 tests GREEN。
- [x] 执行本地审查，临时隔离复现 R1/R2；结论 FAIL，不冒充独立审查。
- [x] R1：用户“修复”授权后，Git 审批绑定完整 patch/base 与扫描文件字节/权限；6 组真实 Git 回归 RED → GREEN。
- [x] R2：event/hook 拒绝 Git-only flags，包含显式默认值；10 个组合 RED → GREEN。
- [x] Git flags 兼容及不支持文件 fail-closed 补充验证；23 tests GREEN，不缩减既有断言/控制。
- [ ] 最终完整 diff 的独立/人工审查、真实宿主验证及启用批准仍另行处理；本地修复不等于发布 READY。

## T7 — 用户要求的独立审查

- [x] 独立 Spec reviewer 复验实际代码与反例；Stage 0 PASS、Stage 1 FAIL，详见 log。
- [x] R3(P1)：用户授权修复；Git 根定位与双路径保护，32 组合通过；根未知/缺 Git/查询超时 fail-closed。
- [x] R4(P2)：base tree 旧模式纳入检查；symlink/gitlink 删除/替换四个 RED 场景已 GREEN。
- [x] Stage 1 修复重审后执行独立 Code Quality Stage 2；结论 NEEDS_INFO，R6(P2) 与人工门禁见 log，不代表发布通过。
- [x] 用户要求独立重审：R1–R4 功能验收通过；Stage 1 因 R5(P2) FAIL，Stage 2 未启动。
- [x] R5(P2)：用户确认修复；缺 Git、超时、执行失败诊断断言 RED → GREEN，保持 fail-closed/脱敏；28 tests OK。
- [x] R6(P2)：用户“继续”授权后修复，mixed-present/missing 回归 RED → GREEN，11 artifact fixtures 通过。
- [x] main 三方集成已本地通过；独立 Stage 1/Stage 2 重审通过。
- [x] policy selector 封闭集合校验与 eval case/expected 输入边界经相邻反例 RED → GREEN。
- [x] 发布扫描发现纯文本中的 binary-marker 字样被误拦截；限制为 diff hunk 前的真实 marker，纯文本/真实二进制回归 RED → GREEN。
- [ ] 当前 review/commit/publish 事件人工批准、commit、push 与 main PR；不创建冲突 Draft PR。
