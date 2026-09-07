<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s2:spec
artifactType: spec
artifactStatus: approved
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:roadmap
upstreamHash: sha256:9ac6664cf068b955e9529307b7951d439e95757d8f36a0a7ff6b94d8a7be6ae6
-->

# S2 Spec：Deterministic Guardrail Layers

> **状态**：[x] 已确认（继承 parent Complex Spec 2026-08-24 确认）
> **档位**：Standard / Full SDD
> **上游**：`../spec.md`, `../roadmap.md` S2, `../s1-artifact-evals/summary.md`
> **分支**：`feat/ai-native-sdlc`
> **工作 Issue**：[#36](https://github.com/ting2tao/ai-code-copilot/issues/36)（parentIssue=none；issueRelationship=standalone；closeTarget=workIssue；S1/S2 交付）

## Goal Contract

| 项 | 内容 |
|----|------|
| Goal | 建立 advisory / deterministic / human 三层 Guardrail，使同一安全合同可由 Claude PreToolUse、local/CI diff checker 和人工门禁共同执行 |
| Done Signal | 统一 policy 可机械校验；secret、敏感数据、受保护路径、fix-test integrity 和高风险人工审批 fixtures 均有 RED/GREEN；Claude adapter 按官方协议阻断；全量 framework check 通过 |
| Guardrails | 不伪造 Codex repo hook 能力；不得输出匹配到的密钥/PII；安全密钥阻断不可由普通 approval 绕过；hook runtime 缺失必须显式 degraded 并由 local/CI fallback 补位；不新增网络或第三方依赖 |
| Fallback | Claude hook 不可用时以同一 checker 扫描 Git diff；Codex 使用 sandbox/permission + local/CI checker + Human Gate；adapter 故障不宣称 deterministic coverage |
| Memory | 平台 capability matrix、低误报规则、approval evidence 和 hook/CI 等价性进入 S3 metrics 与后续 knowledge |

## 功能范围

1. 新增 versioned `guardrail-policy.json`，声明三层控制、owner、触发条件、动作、approval route、evidence 和 adapter capability。
2. 新增标准库 `check_guardrails.py`，支持标准 event、Git diff、Claude PreToolUse stdin 和 fixture suite。
3. 至少实现五类控制：secret diff、敏感数据 diff、受保护路径、`fix` 模式测试完整性、高风险 Human Gate。
4. 新增 Claude Code `PreToolUse` adapter，仅匹配 `Write|Edit`；阻断时用退出码 2 且 stderr 只输出 control ID/path/route。
5. local/CI 使用同一 checker 扫描结构化 event 或 Git diff；本仓库 Codex adapter 未实现，不能冒充已执行（不等于 Codex 平台不支持 hook）。
6. Full/debug/review/finish/security 合同接入 guardrail evidence，并由 framework checker 防漂移。

## 决策语义

- `block`：确定性违规，操作不得继续；`secret-diff` 不接受普通 override。
- `ask`：需要声明的 owner approval；approval 必须包含 control ID，且验证结果保留 override evidence。
- `warn`：advisory，不单独阻断，但进入 review evidence。
- adapter 只能收紧权限，不得把平台 deny 转成 allow。

## Capability Matrix

| Adapter | 状态 | 执行点 | Fallback |
|---------|------|--------|----------|
| local-cli | supported | 结构化 event / Git diff | Human Gate |
| ci | supported | merge 前 Git diff | 人工 review 阻断 |
| claude-pretooluse | supported-with-runtime | `Write|Edit` 前 | local/CI checker |
| codex-repo-hook | unavailable（本仓库未实现） | 平台已有 PreToolUse，协议需单独适配验证 | Codex sandbox/permission + local/CI + Human Gate |

## 非目标

- 不创建 GitHub Actions workflow，不假设业务仓库使用 GitHub。
- 不实现完整 secret scanner、DLP 产品、AST taint analysis 或生产部署审批系统。
- 不自动授予安全/资金/权限/生产变更审批。
- 不修改 S1 artifact schema，不实现 S3 Maintain-to-Plan 或 metrics。

## 2026-09-03 用户增补：消融优先（Ablation）

用户明确要求“也加上消融原理，防止过度抽象和设计”，作为本次范围增补与确认来源。

- 设计与 review 对新增抽象/规则/产物问：移除或替换为直接实现后，哪个 Acceptance 或 Guardrail 会失败？固定输入与验收，单次只改变一个因素。
- 可执行时在隔离测试中对比 baseline / removed / restored；不可执行时只标为反事实分析，不能冒充实测。
- 没有当前需求或失败证据的层、扩展点和文档优先删除/延后；证据不足标记待验证，不强行宣称必要。
- 不增加独立 ablation workflow/schema/report；复用 design-brief 的 YAGNI、Full/test/review 和 log。
- 本次对确定性检测规则做内存副本消融；安全/权限/生产门禁不得在真实环境关闭，样本全绿也不证明风险不存在。
- local/CI approval 是人工提供的可审计声明，不是身份认证。Hook 不信任 tool_input/环境变量传入的批准；需要例外时走平台人工确认，发布仍重新核验 evidence。
- adapter 只交付仓库代码和注册配置，不改写个人安装或启用生产控制；缺运行时阻断并报告 degraded，不能用 fail-open 假装 fallback 已执行。

消融验收：保留与移除决策有具体理由；测试可证明去掉 secret/PII/path/fix 控制后对应负例漏检，恢复后通过；普通小改动不强制新增记录。

## 2026-09-03 用户增补：官方 Agent / Harness 原则与审查

确认来源：用户“审查一次，加入最新的claude和openai的agent驱动原理和harness原则”。

- 只采纳已打开核实的官方资料，标注发布日期或查阅日期，区分来源结论与本项目设计选择。
- 将 loop、按需 context、可恢复 handoff、可验证 outcome/trace、控制面与执行边界、模型升级后消融接入现有 harness/loop 文档、Full/review、eval README；不新增运行时、平台依赖或平行流程。
- Codex capability 改述为“平台支持 / 仓库实现 / 测试验证 / 本地启用”四个不同事实。记录当前 apply_patch 输入和 ask 协议差异，不直接复用 Claude adapter。
- 本轮执行本地审查与只读/临时隔离复现，不宣称独立 Agent Review。安全协议代码修复、启用 hook/CI、提交/发布均不包含在本轮授权中；审查缺口作为未完成门禁记录。
- Done Signal：官方来源可追溯，既有流程中的原则有文档合同测试；保留新复现缺口，不以 suite PASS 覆盖 review FAIL。

## 2026-09-03 用户确认：修复 R1 / R2

确认来源：用户“修复”。本节授权修复前轮审查发现的两处安全协议缺陷，替代前轮“仅审查、未授权代码修复”的停止边界；不授权提交、发布、安装或启用 hook/CI。

- R1：Git event 加入完整变更快照摘要，绑定解析后的 base commit、完整 patch（含删除、位置、路径与模式）及扫描文件原始字节/权限。untracked 内容与模式同样绑定；摘要不得泄露原始内容。原 event v1 调用保持兼容，但调用方提供的 JSON 只能证明所声明的事件，不能冒充可信 Git 快照或身份认证。
- R2：`--operation/--task-mode/--risk` 仅允许与 `--git-diff` 使用；与 event/hook 混用必须失败，包括显式传入默认值。event 的风险仍由 JSON 声明，hook 无效组合 exit 2，不能静默丢弃。
- 验证：真实临时 Git 仓库的纯删除、位置、base、mode-only、untracked 字节/权限变化使旧批准失效；同一快照可复验批准；event/hook 的三个 flags 均有拒绝回归，Git 默认/显式 flags 行为保持。
- 边界：拒绝不支持的文件类型/二进制；不实现原子执行锁或审批服务。扫描后到实际执行前必须重新验证同一快照并独立核验人工证据；并发写入环境不能只靠本次 CLI PASS 授权。
- 消融：只补快照绑定与参数组合校验，不增加通用快照引擎、签名服务或第二套流程；回归可直接证明移除任一修复会恢复对应绕过。

## 2026-09-03 用户确认：修复独立审查 R3 / R4

确认来源：独立审查报告后用户“修复”。仅授权两项修复及必要测试/合同同步，不授权提交、发布或启用 hook/CI。

- R3：hook 使用 Git 工作树根作为路径规则边界；cwd 仅解析相对输入，不作为根。保留 lexical/resolved 双路径保护。覆盖 root/subdir × absolute/relative × Write/Edit，以及仓库路径别名；非 Git、Git 不可用或根无法确定时 exit 2，不能退回 cwd 放行。Git 根查询有界超时并失败关闭。该最小适配明确依赖 Git，不新增根配置协议。
- R4：Git diff 路径同时验证 base tree 与当前文件类型；旧 symlink/submodule 删除或替换为普通文件仍拒绝；普通文本新增/修改/删除保持原合同。使用机器可读 Git mode，不解析展示用 patch 文本推断类型。
- 验收：独立审查的两个反例先转永久 RED，再分别修复 GREEN；R1/R2 与既有保护路径/别名断言不削弱。完成后如未重跑独立审查，只记本地修复验证，不覆盖历史独立 FAIL 为 PASS。
- 消融：只增加根定位和旧类型校验，不新增审批服务、通用适配框架或新的流程文档。

## 2026-09-03 用户确认：R5 修复、独立审查与 PR

用户答复“是的”，明确授权使用 ting2tao、修复 R5、独立双阶段审查并提交 PR 到 main。此确认替代此前“不提交/发布”的本轮边界；不授权合并或启用 hook/CI，不包含 S3。

- R5：缺 Git、Git 超时/执行失败明确报告 degraded 及安全原因、人工恢复/fallback 指引；输入/策略错误保留 invalid 分类。保持 hook exit 2、CLI 非零、stdout 无 PASS 和内容脱敏，不输出原始 exception/命令/内容。
- 回归：先验证缺 Git、超时、执行失败的诊断输出 RED，再最小修复 GREEN；不新增通用错误框架。
- 发布：R1–R5 验收与独立 Stage 1/2 通过后，关联唯一工作 Issue #36，PR base=main，记录真实验证及未启用能力；不自动合并。

## 原验收清单（不因新原则而降低）

- [ ] policy schema/markers 和 adapter capability 可机械验证。
- [ ] 至少两个 deterministic control 展示未批准 RED、合法/批准 GREEN。
- [ ] secret/PII 命中输出不含原始匹配内容。
- [ ] Claude Write/Edit fixture 能映射为标准 event，阻断退出码为 2。
- [ ] Codex unavailable/degraded 状态和 fallback 在 policy/workflow 中一致。
- [ ] `bash scripts/check_framework.sh` PASS。
