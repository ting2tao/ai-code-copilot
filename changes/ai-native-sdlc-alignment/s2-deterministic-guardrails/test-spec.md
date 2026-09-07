<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s2:test-spec
artifactType: test-spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s2:spec
upstreamHash: sha256:40e32575c0a9b9f9945c46817265b919f544ab4a9a48aa3bddd65dd314ff6f5f
-->

# S2 Test Spec：Deterministic Guardrail Layers

## P0

| ID | 场景 | 预期 |
|----|------|------|
| G1 | safe edit | PASS |
| G2 | 新增 literal secret | FAIL；不可 override；输出无 secret |
| G3 | 新增手机号/身份证测试数据 | FAIL；输出无 PII |
| G4 | 编辑 protected path | 缺 approval FAIL；指定 approval PASS 并记录 override |
| G5 | `fix` 模式编辑测试 | 缺 approval FAIL；指定 approval PASS |
| G6 | high-risk operation | 缺 owner approval FAIL；批准后 PASS |
| G7 | 未知 event version/control approval | FAIL |
| G8 | Claude Write/Edit hook payload | 正确映射；block 时进程 exit 2 |
| G9 | Codex repo hook capability | 明确 unavailable，fallback 非空 |
| G10 | Git diff mode | 与标准 event 使用同一 controls/evaluator |

## 验证命令

```text
python3 -m unittest discover -s tests -p 'test_guardrails.py'
python3 scripts/check_guardrails.py --policy config/guardrail-policy.json --event <fixture>
bash hooks/pre-tool-guardrail < <hook-fixture>
bash scripts/check_framework.sh
```

## Guardrails

- 不通过删除高风险类别、降低 action 或允许 secret override 转绿。
- RED fixture 的原始 secret/PII 不得出现在 stdout/stderr。
- adapter 缺失/runtime 故障必须报告 degraded；不得把未执行写成 PASS。
- Git diff 使用参数列表调用 Git，不拼接 shell command。

## 初次实现结果（历史证据）

- 17 个 unittest 方法通过，含 12 个 JSON 场景、4 个单因素消融对照、审批失效、不可覆盖 secret、hook 原生 ask/exit 2、无 Python degraded、symlink、binary/untracked/deleted Git paths。
- policy 缺失 RED exit 1；首次 11 项失败；新增空 selector/alias 路径两项 RED 后修复 GREEN。
- 无异常/敏感内容回显；py_compile、bash -n、git diff --check exit 0。
- 真实 diff 扫描 exit 1（预期 ask：受保护路径与安全人工门禁）；不得将未获批准写成 PASS。
- 消融仅在内存副本执行，未新增 runtime disable flag、独立报告或流程。

## 2026-09-03 本轮新增证据与验收缺口

- 官方原则/平台说明文档合同先 RED（19 tests 中 6 项断言失败），补齐后 19 tests GREEN。
- R1 临时真实 Git 复现：不同纯删除 diff，eventHash 相同，旧批准错误放行；违反原审批失效验收。
- R2 CLI 复现：`--event - --risk security --operation deploy` 被当作普通 edit event，exit 0；显式风险参数未生效。
- R1/R2 不是 suite 已覆盖的成功案例；review FAIL。修复前必须补永久回归，不能通过调整断言/忽略风险转绿。

## 2026-09-03 修复验收（替代上述当前缺口状态）

| ID | 永久回归 | 结果 |
|----|----------|------|
| R1a | 同一受保护路径删除不同内容；旧批准不得复用 | RED → GREEN |
| R1b | 相同新增文本插入不同位置 | RED → GREEN |
| R1c | 相同 tree/patch，不同 base commit | RED → GREEN |
| R1d | core.filemode=false 下可执行位变化；扫描文件权限继续变化 | RED → GREEN |
| R1e | untracked mode 改变 | RED → GREEN |
| R1f | untracked LF/CRLF 原始字节不同但 splitlines 相同 | RED → GREEN |
| R2 | event/hook × operation/task-mode/risk；含显式默认值，共 10 个组合 | RED → GREEN |
| C1 | Git 默认值、显式高风险/部署、apply 与 unknown 测试路径策略 | 兼容回归 GREEN |
| C2 | tracked 路径替换为 symlink、目录、binary | 补充边界测试 GREEN，exit 1 且内容脱敏 |

- 首次 22 tests：16 个子场景断言失败；R1 单独修复后 6 个碰撞/漏检场景消失，R2 的 10 个组合仍失败；R2 修复后 22 tests OK。
- C2 补充后：23 tests OK。C1/C2 是兼容/边界覆盖，不冒充新缺陷的 RED 证据。
- 相同 Git 快照可复验人工 fixture approval，不同快照被拒绝；fixture 审批只用于临时 Git 仓库。
- 真实工作树检查仍 exit 1 / ask（protected-path-edit、fix-test-integrity、high-risk-human-gate），没有伪造真实批准。无新增依赖/签名服务/快照引擎。

## 独立审查 R3 / R4 修复验收

- R3：`test_hook_subdirectory_keeps_repository_path` 固定相同目标与内容，覆盖 infra/tests × 真实根/根别名 × 根/子目录 cwd × 绝对/相对输入 × Write/Edit，共 32 组合。首次 16 个子目录场景缺 ask，修复后全部保留原 control ID 与 ask。
- 根未知/运行时边界：非 Git cwd、缺 Git 均 exit 2，stdout 空；根查询 timeout=5 秒，注入 TimeoutExpired 验证转换为可处理 ValueError。仅超时外部边界用 mock，Git 路径和类型行为均用真实临时仓库。
- R4：`test_git_rejects_old_unsupported_modes` 的 symlink/gitlink × delete/replace 共 4 个场景首次误 PASS，修复后 exit 1、stdout 空、内容脱敏。
- 既有 alias fixture 只补 `git init` 以满足可信根前提，保留原 ask 断言；没有将失败保护断言改成成功。
- 首次 26 tests / 21 failures；额外缺 Git 测试单独 RED。R3 修复后 hook 子集 8 tests OK；R4 修复后全量 27 tests OK，framework PASS。
- 原独立 probe 复验：root/subdir 四个 hook 请求现在全部 ask；120000 → 100644 原临时 diff 现在 exit 1，不再返回 passed:true。本地验证不替代独立重审。

## R5 诊断回归

缺 Git 的真实 PATH 隔离测试新增 degraded/Git/human review 断言，先 RED；超时和 Git 非零返回仅 mock 外部 subprocess 边界，主 CLI 的读取/evaluator/错误输出保持真实，两个诊断子场景先 RED。修复后 28 tests OK；exit 2、空 stdout、底层命令/私密 stderr 不回显的断言均保留。JSON/策略错误仍走 invalid，不伪造 fallback 已执行。
