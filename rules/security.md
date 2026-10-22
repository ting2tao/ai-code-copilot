---
alwaysApply: true
---
# 安全红线

任何违反以下规则的代码，/review 阶段直接 Critical 阻塞。

## 1. 代码安全

- ❌ 禁止在代码中硬编码密钥、AK/SK、数据库密码、Token（必须从配置中心/环境变量读取）
- ❌ 禁止提交包含用户个人信息的测试数据（手机号、身份证、真实姓名）
- ❌ 禁止在日志中打印：手机号、身份证、银行卡号、密码、Token
- ❌ 禁止拼接未转义的 SQL、Shell 命令、模板、HTML 或 URL 参数；必须使用对应技术栈的参数绑定/转义 API

## 2. 业务安全

- ⚠️ 涉及资金变更的逻辑 → spec 中必须明确标注，人工审查确认后方可编码
- ⚠️ 涉及状态流转 → 必须检查状态机合法性，禁止跳状态
- ⚠️ 涉及权限变更 → 必须显式校验操作人权限，不能只靠调用方自觉

## 3. 接口安全

- 对外接口必须鉴权；内部接口也必须明确可信边界和调用方身份
- 涉及用户数据的查询必须校验数据归属（不能 A 查到 B 的数据）
- 批量接口必须有上限保护（防止超大参数 OOM）

## 4. 三层 Guardrail 执行合同

**S2 实施与审查状态以变更 log/summary 为准。** 快照绑定、CLI 参数、hook 子目录路径、旧文件类型和运行时降级诊断已有永久回归；本地 self-review 不代替独立/人工审查或真实宿主验证。`approved/PASS` 不能单独授予 commit/publish/deploy 权限，人工仍须核验完整 diff、风险与审批来源。历史发现和修复证据见 S2 log。

事实源：`config/guardrail-policy.json`。advisory 是提示，deterministic 检测可执行模式，human 负责语义风险与授权；正则未命中不是安全证明。

```text
python3 <COPILOT_HOME>/scripts/check_guardrails.py --event event.json
python3 <COPILOT_HOME>/scripts/check_guardrails.py --git-diff <base-commit> --operation review --task-mode apply --risk security
python3 <COPILOT_HOME>/scripts/check_guardrails.py --git-diff <base-commit> --operation publish --task-mode finish --approvals /trusted/approvals.json
```

- event v1 必填：`eventVersion`、`operation`、`taskMode`、`changedPaths`（仓库相对路径）、`diffAddedLines`（`{path,line}` 数组）、`risks`、`approvals`。风险由确认的 Spec 提供，不能凭扫描未命中就省略。
- Git 模式从一个 base commit/ref 扫到整个当前工作树，包括 staged/unstaged 合成后的最终 diff、untracked 文本与删除路径，不单独授权中间 index 状态。忽略文件不扫描；变更涉及二进制、符号链接、目录/submodule 或不可读取文件时阻断要求人工处理。类型校验同时检查 base tree 旧模式及当前文件，旧 symlink/gitlink 的删除或替换也会拒绝。发布前工作树应干净并明确 base；不是任意 revision range。
- 输出 `eventHash`、control ID、action、path 和 owner/approvalRoute；不输出匹配内容。secret/PII 必须去除，不能普通 override。
- local/CI approval 数组项为 `{controlId, reviewer, evidenceRef, eventHash}`；必须由有权人明确批准当前事件，原始 evidence 写入现有变更记录。审批文件放在受信任、非待扫描工作树中。Agent 不得自行编造；CLI 仅验证格式/hash，无法认证人类身份，CI owner 必须独立核验来源。
- Git adapter 将 `gitSnapshotHash` 纳入 eventHash：摘要绑定解析后的 base commit、各路径完整 patch（含增删、位置与 Git 文件模式）、扫描文件原始字节及权限、删除标记和 untracked 文件。Git 可执行位检测不受 `core.filemode=false` 隐藏；扫描列表之外的普通 chmod、忽略文件不在覆盖范围。完整快照或 operation/taskMode/risks 改变后旧批准失效；修复前 Git 批准需重新获取。
- 标准 event v1 保持兼容，其 hash 只绑定调用方所提供的 JSON；手工填入 gitSnapshotHash 不证明真实仓库状态。需要完整 Git 审批时必须由可信 checker 用 `--git-diff` 重新生成事件，不接受 Agent 自行精简/伪造的输入。
- `--operation/--task-mode/--risk` 仅允许搭配 `--git-diff`；与 `--event/--hook-input` 混用（包括显式默认值）会报错且不产生 PASS。event 风险从 JSON 读取；hook 无效组合 exit 2。Git 默认值为 edit/unknown/无声明风险，不代表语义上无风险。
- 快照读取与实际操作不是原子事务，不提供并发写锁。审批后、执行前须在受控且无并发写入的工作树重新扫描核对 eventHash；发生变更重新审批。提交 index 与被扫描最终工作树不一致时不得据此提交。此工具不是执行授权服务。
- `block/ask` 未解决时 CLI exit 1；`warn/approved` 不单独阻断。批准不覆盖平台权限或现有人工门禁。
- CI 必须从受保护、已审查的版本加载 checker/policy，并独立保护 job/approval 来源；不要让待审查分支自行改门禁后用自己的 PASS 证明安全。此 CLI 不是对恶意 Agent/仓库作者的隔离安全边界。

### 平台覆盖与降级

- Claude 插件 `hooks/hooks.json` 提供 `Write|Edit` PreToolUse adapter；需要 Python 3.9+、Git 工作树与插件启用。此变更不改写个人 settings，Claude 传统 install 脚本仍只注册 SessionStart；Codex install 额外配置独立适配器，不能假定已信任/执行。
- hook 的 cwd 仅用于解析相对输入，规则路径由 `git rev-parse --show-toplevel` 的工作树根确定，保留 lexical/resolved 双路径保护；子目录启动不会丢失 infra/tests 前缀。Git 根查询超时为 5 秒；非 Git、缺 Git、超时或无法确定根/路径别名边界时 exit 2，禁止回退到 cwd 冒充仓库根。非 Git 项目本适配不覆盖，需明确切换可信结构化 event + 人工门禁。
- Write 扫写入内容，Edit 扫 new_string；缺少可信 taskMode 时对测试编辑保守 ask。不信任 tool_input 内的 approvals。secret/PII 或无效输入 exit 2；需要 owner 判断时返回原生 `permissionDecision: ask`，从不返回 allow 跳过平台检查。协议依据：[Claude Code hooks](https://code.claude.com/docs/en/hooks)。
- 缺运行时/执行错误时明确 degraded 并阻断；人工恢复 adapter，或明确切换到 local/CI + Human Gate 后再继续，不能假装 fallback 已执行。Bash/MCP 写入不在该 hook 覆盖内，最终 diff 扫描仍必需。
- Git 不可用、查询超时或失败使用固定安全原因报告 degraded，并给出恢复 Git/runtime 或显式使用可信 event + 人工审查的指引；不回显底层异常/命令/stderr。JSON/policy/路径格式错误仍为 invalid，不能把失败误报为已执行的 fallback。
- `codex-repo-hook: supported-with-runtime` 表示已实现独立 apply_patch adapter，需要 Python 3.9+、Git 工作树、宿主支持、Hook 配置与用户信任；它不表示本地已启用或已完成真实宿主验证。Bash/MCP 写入不覆盖，最终 diff 扫描仍必需。

### 最新平台支持与本仓库事实（查阅 2026-10-22）

必须分开描述 **平台支持 / 仓库实现 / 测试验证 / 本地启用**。

- [Codex Hooks 文档](https://learn.chatgpt.com/docs/hooks) 列出 PreToolUse；apply_patch 输入仍报告 `tool_name: apply_patch`，补丁来自 `tool_input.command`。使用 `hooks/pre-tool-codex`，不把 Claude adapter 直接注册给 Codex。
- Codex 配置入口为 hooks.json 或 config.toml。三平台安装器使用 hooks.json 配置 SessionStart 与 `^apply_patch$` PreToolUse，保留无关 handler。旧 settings.json 不自动迁移；管理员需按平台清理旧注册，避免未来重复执行。
- Codex owner-required 决策使用 exit 2 阻断并转明确 local/CI + event-bound 人工审核，不发送未支持的 ask，也不发送 allow。Agent 不得自行填写 approval 解锁；需要人工确认后走可信 diff 检查和明确的操作路径。
- 安装/更新后必须通过 `/hooks` 审核并信任当前定义；定义变化后可能需重新信任。安装器不修改 trust store、不绕过信任。未信任时宿主跳过 Hook，不能声称 guardrail 已执行；缺失运行时/错误由适配器阻断。
- 适配器本地测试使用真实 subprocess + 临时 Git 仓库，覆盖正常/违规/失败分支；具体宿主、模型执行和 Windows/WSL 测试证据见变更 log。合成测试不冒充真实宿主证据。
