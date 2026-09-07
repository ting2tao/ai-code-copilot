<!-- artifact
artifactVersion: 1
artifactId: ai-native-sdlc-alignment:s2:log
artifactType: log
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: ai-native-sdlc-alignment:s2:spec
upstreamHash: sha256:40e32575c0a9b9f9945c46817265b919f544ab4a9a48aa3bddd65dd314ff6f5f
-->

# S2 Log：Deterministic Guardrail Layers

## 2026-09-03 当前恢复点：R6/main 集成后的重审

用户“继续”确认先修 R6、适配最新 main、重审后提交 PR。parent Spec 增补及 S1 log 是本次集成范围/RED-GREEN 的记录源；R1–R5 实现没有改动。Git merge --no-commit 的文本冲突已解决，MERGE_HEAD=ee028aa4，未创建 commit/push/PR；安全 stash 093bea9a 保留。

新鲜集成验证：framework exit 0（28 guardrail tests、4 eval regression tests、11 artifact fixtures、9 templates、21 oracle/scorer cases、model-first 0.2.0、install-overwrite）；实际链 PASS 17；git diff --check exit 0。真实 review diff 仍为 protected-path-edit/high-risk-human-gate ask，未伪造 approval。独立 Stage 1 `/root/integrated_spec_review` 进行中；Stage 2 必须后续另一 reviewer 执行。No merge PR / No hook or CI enable / No S3。

随后 Stage 1 PASS；Stage 2 实施质量 PASS（0 Critical）但发现 2 个 ordinary Important，已按 S1 log 的真实 RED → GREEN 修复：版本检查纳入 untracked 行为文件，eval 对消费的 facts 字段先做类型诊断。修改发生于审查后，当前重新进入最终双阶段审查；人工批准仍未解决。

## Summary

| 字段 | 内容 |
|------|------|
| 状态 | active |
| 上游 | parent Complex Spec / Roadmap S2 / S1 reviewed summary |
| 分支 | feat/ai-native-sdlc |
| workIssue | pending（on-publish） |
| 确认 | 继承用户 2026-08-24 的 Complex Spec 确认及“继续”指令 |

## Decisions

- Claude adapter 遵循官方 `PreToolUse`：stdin JSON；`Write|Edit`；退出码 2 阻断并从 stderr 返回原因。
- Codex 不声明不存在的 repo hook；平台能力为 unavailable，fallback 是 sandbox/permission + local/CI checker + Human Gate。
- 所有 adapter 共享 versioned policy 和标准 event，输出不得回显 secret/PII。
- 2026-09-03 用户明确增补消融原理；在 S2 Spec 增补并同步下游 hash，保留 parent/S1 已确认合同不变。
- Hook 的确定性 block 使用 exit 2，需人工判断使用原生 ask（不是自动 override）；runtime 缺失 fail-closed 并显式 degraded。只交付代码，不安装/启用用户环境 hook。
- CLI approval 是调用方提供的声明，绑定精确 eventHash；不实现身份认证或自动授予审批。当前变更最终 diff 仍需人工审查。
- 消融测试复用 unittest 和 JSON fixtures，不增加生产 `--fixtures`/禁用控制开关；原计划 fixture CLI 命令机械同步为 unittest。
- 合成 secret fixtures 分段存储并在测试时拼接，避免把完整凭据形状写入仓库；运行时负例内容未改变，无扫描器白名单或放宽规则。

## Verification

### 2026-09-03 — RED

```text
command: bash scripts/check_framework.sh
exit: 1
output: FAIL: missing file: config/guardrail-policy.json

command: python3 -m unittest discover -s tests -p 'test_guardrails.py'
exit: 1
output: 11 failures; missing guardrail checker implementation
```

### 2026-09-03 — 边界回归 RED → GREEN

- 初版核心测试通过后，新增两项负例复现缺口：空 selector 被接受；symlink resolve 丢失受保护 lexical path。17 项最终测试覆盖修复和原路径。
- 根因：policy 只编译已有 regex，未拒绝空列表；hook 只保留 canonical path。
- 修复：校验必需 selector 与 control semantics；同时检查 lexical/resolved 两个相对路径，外部路径拒绝。

```text
command: python3 -m unittest discover -s tests -p 'test_guardrails.py'
exit: 0
output: Ran 17 tests; OK

command: python3 -m py_compile scripts/check_guardrails.py tests/test_guardrails.py
exit: 0

command: bash -n hooks/pre-tool-guardrail
exit: 0

command: git diff --check
exit: 0
```

### 消融证据

| 对象 | 方法 | 结果与决策 |
|------|------|------------|
| secret / PII / protected path / fix-test control | 固定四个负例，内存 policy 单次移除一个 control，再恢复 | baseline 拦截；removed 漏检；restored 拦截，四项保留。只证明样本内检测有效，不证明完整安全性 |
| 通用策略插件引擎 | 反事实设计分析，未搭建后假称实测 | 六个固定 control 用函数即可；无当前扩展需求，延后 |
| 独立审批系统 | 反事实设计分析 | 本项目不是身份服务；复用原生 ask 与人工 evidence，不自行认证/授权 |
| 独立消融 workflow/schema/report | 反事实设计分析 | 现有 design-brief/YAGNI、test/review/log 可承载，删除新增层计划 |

### 2026-09-03 — 最终本地集成证据

```text
command: shellcheck hooks/pre-tool-guardrail
exit: 0

command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --change-dir changes/ai-native-sdlc-alignment --require-chain
exit: 0
output: PASS 17 artifacts

command: bash scripts/check_framework.sh
exit: 0
output: progressive-sdd checks passed; Ran 17 tests / OK;
        PASS 7 artifact-chain fixtures; PASS 9 artifact templates;
        PASS transition draft -> approved;
        PASS offline policy oracle (18 cases);
        PASS external scorer self-check (18 cases);
        live capability=external-results-required, mode=non-blocking;
        ai-code-copilot framework check passed
```

## 本地自查（非独立 Agent Review）

- Spec：六类 control、三层 policy、event/Git/Claude 入口、capability fallback、消融约束均有对应实现与测试。
- Quality：标准库，无联网或任意 shell 执行；输出不回显匹配内容；批准绑定事件；失效输入拒绝；路径别名和删除文件纳入检查。
- 真实 diff：`python3 scripts/check_guardrails.py --git-diff HEAD --task-mode apply --risk security` exit 1；没有 secret/PII block，protected-path-edit 与 high-risk-human-gate 为 ask。此为未批准的预期结果，不伪造 PASS。
- GitHub：workIssue pending（on-publish）；本次未 commit/push/PR，未改写个人 settings，未部署 CI。
- 尚需：最终 diff 人工/独立 review、启用 adapter 的显式确认；S3 尚未实施。

## Loop Evidence

- Done Signal：fixture/ablation/adapter/invalid-input/Git 实验有可重复测试；最终 framework/chain 证据如上，均 exit 0。
- Guardrails：安全控制仅在内存测试副本消融；真实配置未关闭控制；未创建新的并行编排或报告层。
- Fallback：live adapter 未启用明确为未执行；本地测试不等于 live integration；生产启用需要单独审批。
- Memory：保留抽象的依据是当前验收/安全边界证据，不是未来可能；负例灵敏度不等同证明整个架构最优。

## 2026-09-03 — 用户要求的本轮审查与官方原则更新

**结论：FAIL，不能发布/启用自动门禁。** 本次是同一主 Agent 的本地审查，不冒充独立 Agent Review。此前本地自查与测试通过的记录保留作为历史证据，本节覆盖当前审查结论。

### Stage 0 / Stage 1

- Artifact Chain：审查开始前 `PASS 17 artifacts`。
- Spec Compliance：FAIL。Spec 声明精确事件审批及变更后审批失效，但 Git adapter 的 event 丢失删除内容；见 R1。文档不能代替此合同的实现。
- S2 六类控制、CLI/hook 入口、消融和最新原则文档均存在；未发现新增 runtime 或外部服务部署。
- 正式 Stage 2 Code Quality 依流程暂不进入（Stage 1 未 PASS），也不宣称独立 review。以下缺陷是在验收边界复现中确认的。

### R1 [P1 / Critical] 纯删除 diff 可复用旧批准

- 位置：`scripts/check_guardrails.py:176`、`:184`、`:107`。
- 根因：Git adapter 仅保留 changedPaths 和新增行，不包含删除行、完整 patch 或 base snapshot；hash 对这个有损 event 计算。
- 隔离复现：临时 Git 仓库，受保护 `infra/config.txt` 基线为 alpha/beta/gamma 三行。A 删除 alpha；B 恢复 alpha 并删除 beta。两份真实 diff 不同，但新增行都为空，eventHash 相同；把 A 的 fixture approval 用到 B，得到 passed=true。
- 实际输出：`differentDiffs=true, sameEventHash=true, staleApprovalPassed=true`。
- 影响：审批无法证明人类确认的是当前完整变更；对不同删除内容或位置的改动可能误用同一批准。
- 建议修复：将完整动作快照（含 base、增删改、路径/模式及 untracked 内容摘要）绑定审批，增加 A/B deletion、mode-only、位置变化的负例；不要降低验收为“只确认新增行”。本轮未改生产 checker。

### R2 [P1] 非 Git 输入模式静默忽略风险/动作 flags

- 位置：`scripts/check_guardrails.py:195`、`:205` 至 `:208`。
- 最小输入：合法 event v1，operation=edit，taskMode=apply，普通源码路径，risks=[]，approvals=[]；CLI 同时指定 `--event - --risk security --operation deploy`。
- 实际输出：`exit=0, passed=true, decisionCount=0`。
- 根因：argparse 接受 flags，但只有 git-diff 分支消费；event/hook 分支静默丢弃显式参数。
- 建议修复：拒绝不适用的 flag 组合，或明确合并显式值并重新绑定审批；增加 event/hook × risk/operation/task-mode 组合测试。本轮未改生产 checker。

### 官方资料核验与范围内修改

- OpenAI：2026-08-19 Codex as a platform、2026-08-25 Automating repetitive work，以及当前 Agent eval/Hook 文档；Anthropic：2026-03-24 harness design、2026-04-08 Managed Agents、2025-09-29 context engineering。已打开页面，完整链接/日期/映射集中在 `docs/harness-engineering.md` 和 `rules/security.md`。
- 更新既有 harness/loop 文档、Full/review、eval README 与安全兼容说明；不新增 schema、runtime、文档体系或强制多 Agent。
- 更新 Codex 表述：平台已有 PreToolUse；apply_patch payload 使用 tool_input.command；当前文档的 ask 尚不支持且会继续工具调用。Claude adapter 不可直接复用。仓库 adapter 仍未实现，真实宿主仍未验证/启用。
- 新原则要求固定 model/policy/任务/验收基线、实测与反事实分开、模型升级后重新消融；self-review 与独立评价分开，outcome 与 trace 分开；恢复先核验副作用，预算与停止条件复用 Goal Contract。
- Spec 新增本次用户确认来源；下游 metadata hash 同步，不改 parent/S1 冻结合同。

### 本轮验证

```text
diagnostic command: python3 /tmp/copilot-review.6uhAZr/probe.py <repo-root>
exit: 0 (probe completed, not safety PASS)
output: deletion-approval-collision: differentDiffs=true, sameEventHash=true, staleApprovalPassed=true
        event-cli-flags-ignored: exit=0, passed=true, decisionCount=0

command: python3 -m unittest discover -s tests -p 'test_guardrails.py'
RED: exit 1, Ran 19 tests, 6 missing-principle/platform-documentation assertions
GREEN: exit 0, Ran 19 tests, OK

command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --change-dir changes/ai-native-sdlc-alignment --require-chain
exit: 0; output: PASS 17 artifacts

command: bash scripts/check_framework.sh
exit: 0; output: 19 tests OK; 18 offline policy oracle/scorer self-check cases PASS; framework check passed

command: git diff --check
exit: 0
```

probe 只写临时 synthetic Git 仓库，不接触用户凭据或外部系统。19 个 tests 是现有行为和文档合同回归，不覆盖已记录的 R1/R2；suite GREEN 不能覆盖 review FAIL。下一次 fix 应先把这些复现转成永久失败回归，再实现修复。

### 当前停止边界

- 已完成本轮审查及用户要求的官方原则融入。
- R1/R2 未修复；当前自动审批/发布门禁禁止启用。需要用户确认继续安全协议修复后再进入 fix。
- 未 commit/push/PR，未改个人 settings、未启动多 Agent，未实现 S3。workIssue pending(on-publish)。

## 2026-09-03 — 用户确认“修复”：R1 / R2 本地修复与复核

本节更新当前状态；前轮 FAIL 与停止记录保留为历史证据。用户本次明确授权 R1/R2 的代码、测试和合同修复，未授权提交/发布或启用 hook/CI。沿用 Full SDD；调试/TDD/verification 仅作为专项检查表，不引入第二套编排。

### 根因与最小修改

- R1：有损新增行 event 无法描述完整 Git 变更。现在由 Git adapter 计算 `gitSnapshotHash`，纳入 eventHash；摘要覆盖解析后的 base commit、每路径完整 patch（含删除/位置/模式）、扫描文件原始字节/权限和删除标记。untracked 同样绑定；强制检测 Git 可执行位，避免 `core.filemode=false` 隐藏它。
- R2：argparse 默认值掩盖“未指定”与“显式指定”，而 event/hook 不消费这些 flags。现在以 None 区分显式参数，在读取输入前拒绝非 Git 模式混用；Git 分支随后才应用 edit/unknown/空 risks 默认值。
- 仅修改既有 checker，不新增依赖、签名服务、快照框架或执行锁。原 event v1 兼容，但只证明调用方声明的 JSON；修复前 Git approval 不再适用。
- 文档明确扫描不是原子执行：只覆盖 Git 可见最终 diff 与 untracked，不覆盖忽略文件/中间 index；不支持类型拒绝；人工身份和执行前状态须独立核验。

### RED → GREEN 证据

```text
command: python3 -m unittest discover -s tests -p 'test_guardrails.py'
RED: exit 1; Ran 22 tests; FAILED (failures=16)
  R1: deletion / position / base / mode / untracked-mode / untracked-newline，共 6 个失败
  R2: event/hook × operation(deploy/edit) / task-mode(fix/unknown) / risk(security)，共 10 个失败

R1 单独修复后:
command: python3 -m unittest discover -s tests -p 'test_guardrails.py' -k git
exit 1; Ran 5 tests; 仅剩 R2 的 10 个失败（名称 non_git 同样被选中）

R2 修复后:
command: python3 -m unittest discover -s tests -p 'test_guardrails.py'
exit 0; Ran 22 tests; OK

补充 unsupported-file 边界后:
command: python3 -m unittest discover -s tests -p 'test_guardrails.py'
exit 0; Ran 23 tests; OK

command: bash scripts/check_framework.sh
exit 0; progressive-sdd checks passed; Ran 23 tests / OK;
  PASS 7 artifact-chain fixtures; PASS 9 artifact templates;
  PASS transition draft -> approved;
  PASS offline policy oracle (18 cases);
  PASS external scorer self-check (18 cases);
  live capability=external-results-required, mode=non-blocking;
  ai-code-copilot framework check passed

command: python3 -m py_compile scripts/check_guardrails.py tests/test_guardrails.py
exit 0
command: bash -n hooks/pre-tool-guardrail
exit 0
command: git diff --check
exit 0
command: python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --change-dir changes/ai-native-sdlc-alignment --require-chain
exit 0; PASS 17 artifacts
```

### 本地复核（self-review，不是独立 Agent Review）

- Stage 0：17 artifacts 合同链通过；更新 S2 Spec 的用户授权及四个直接依赖 hash，未修改 parent/S1 冻结合同。
- Stage 1：R1/R2 修复验收 PASS。真实临时 Git 复现从误放行变为拒绝；同一快照可复验 fixture approval；显式默认值不再绕过参数校验。测试没有删减原 Acceptance。
- Stage 2：本次两处修复的代码自查未发现新增阻塞项；标准库、参数列表调用、脱敏输出、二进制/符号链接/目录 fail-closed、向后兼容与边界说明均已检查。此结论仅限本地修复，整体独立/人工审查与启用门禁仍待完成。
- 真实工作树：`python3 scripts/check_guardrails.py --git-diff HEAD --task-mode fix --risk security` exit 1，`passed=false`，protected-path-edit / fix-test-integrity / high-risk-human-gate 均为 ask；无 secret/PII block。没有编造审批或将其记为安全 PASS，eventHash 随后续记录修改会变化，不作为执行凭证保存。
- 消融依据：固定回归基线下，先仅增加 R1 绑定，R2 仍失败；随后仅加参数组合校验，全绿。这证明两处检查对各自反例有必要性，不证明整个框架最优或生产风险不存在；没有关闭真实门禁，也没有声称测得模型质量/成本改善。
- Git：当前分支 `feat/ai-native-sdlc`；本次未 commit/push/PR，workIssue 仍 pending(on-publish)，未到发布门禁。未改个人设置、未启用 hook/CI、未执行 live eval、未启动多 Agent，S3 未实施。

### Loop / 交接

- Done Signal：两处 P1 已有永久 RED/GREEN 与 23 tests、framework、artifact chain 新鲜证据。
- Guardrails：当前实际 diff 仍需最终人工确认；非可信 event JSON、不支持文件类型、并发修改均不能凭 PASS 推导授权。
- Fallback：若后续适配不能保证受控执行点，保持人工门禁，不启用自动批准；不能回退到旧有损 hash 作为安全方案。
- Memory：审批必须绑定被批准对象的完整表示；模式专用参数必须显式拒绝不适用组合，不能静默忽略。

## 2026-09-03 — 用户要求独立审查：Stage 1 FAIL

确认来源：用户“进行独立审查”。Reviewer：`/root/independent_spec_review`，独立上下文（fork_turns=none），非实现者 self-review。主 Agent 负责基线验证、复验反例与记录；未修改实现/测试、未提交或启用 hook/CI。

### 审查基线与过程

- 分支 `feat/ai-native-sdlc`，HEAD `4b16be6`；S2 为当前未提交工作树，不能只检查 Git tracked diff，已包含新增 checker/policy/hook/tests。
- checker SHA256：`f2ea3b3d5431b4b42b28478dacb6ddf198f3f3f6448bb999767563e9f4fcc59d`。
- policy SHA256：`561e37b98a19495639832d82216eab2641aae58dbe3c57299fe862f495aa51df`。
- tests SHA256：`705e73fded309e439f8c17e94eefeb07c4179dd7e00635335796f5fe7416400a`。
- S2 Spec SHA256：`969eaba8ddeccd53ab790888552e631851133b2cb2904360651a10162f0290f0`。
- Stage 0：主 Agent 与独立 reviewer 均复验 `check_artifact_chain.py --require-chain`，exit 0 / PASS 17 artifacts。
- 新鲜 suite：23 tests OK；全量 framework PASS，含 18 offline oracle/scorer cases；`git diff --check` exit 0。新缺口不在现有 suite 中，全绿不能覆盖 review FAIL。
- Stage 1：独立 Spec Compliance FAIL。按 review workflow 停在这里，未启动 Stage 2 Code Quality reviewer，也不声称完成双阶段审查。

### R3 [P1] Hook 以 cwd 代替仓库根，子目录漏掉路径门禁

- 位置：`scripts/check_guardrails.py:137-149`，尤其以 cwd 构建 logical_root 并据此生成相对路径。
- 同一真实临时 Git 仓库、同一绝对目标和相同 Edit 内容，只改变 payload.cwd。`infra/main.tf` 在 repo root cwd 返回 `protected-path-edit` ask，在 repo/infra cwd 返回 exit 0 / stdout 空；`tests/helper.py` 同理从 `fix-test-integrity` ask 变为空输出。
- 根因：被评估路径分别变成 main.tf/helper.py，丢失仓库相对路径的 infra/tests 前缀，避开路径模式。子目录启动是已实现 adapter 的输入边界，不是未启用、身份认证或并发非目标。
- reviewer 与主 Agent 均运行 `python3 /tmp/s2-spec-review.9Y6FJ5/probe.py` 复现以上四个结果。临时 probe 仅发送 synthetic payload，不实际编辑业务文件。
- 修复方向：从可信仓库/项目根解析路径，不把任意 cwd 当安全边界；无法确定时显式拒绝或转人工。补 repo root/subdir × absolute/relative target 对照，不能放宽 path policy 转绿。

### R4 [P2] 只核验新文件类型，旧 symlink 删除/替换未阻断

- 位置：`scripts/check_guardrails.py:189-196`；缺失当前路径时直接记 deleted，普通当前文件直接继续，均未检查 base tree 的旧模式。
- 真实临时仓库 base 的 link.txt 为 Git mode 120000；删除或替换为 100644 普通文本文件，checker 返回 exit 0 / passed:true / decisions:[]。与 security 的“不支持类型变更阻断”及 S2 修复边界不一致。
- reviewer 复验删除和替换；主 Agent 独立复验替换：在 `/tmp/s2-spec-review.9Y6FJ5/repo` 运行 checker `--git-diff HEAD` 得到 passed:true，`git diff --summary HEAD` 同时显示 `mode change 120000 => 100644 link.txt`。
- 定为 P2 合同偏差；没有据此宣称审批 hash 再次碰撞或额外安全影响。修复方向是在 base 与工作树两侧检查文件类型，并增加删除/替换负例。

### 其余核验与当前门禁

- R1 六组 Git 快照绑定、R2 十个显式参数拒绝场景均通过；原两处修复没有被本次反例否定。
- 三层 policy、基础 secret/PII 脱敏、不可普通 override、hook ask/exit2、不输出 allow、workflow 集成和隔离消融均有实现/测试；未发现新增无需求的引擎/流程。
- Harness / Loop Readiness 为 READY（反例可复验、失败停止条件明确），不等于功能验收 PASS。无复杂业务 Domain Check；控制不变量存在上述缺口。
- 官方原则文档合同存在，本轮未重新研究最新外部资料；不冒充宿主集成证据。workIssue pending(on-publish) 不单独阻断本地 review。
- 当前结论：S2 独立 Stage 1 FAIL，R3/R4 待修复；Stage 2 未执行。保持禁止启用自动门禁，不提交、不发布，不以真实 diff 的未解决 ask 伪造授权。

## 2026-09-03 — 用户“修复”：R3 / R4 本地验证完成

本节更新实现状态，保留上节独立 FAIL 为历史；本次未重跑独立审查，不将其标成 PASS。用户确认仅覆盖两处修复和必要合同/测试同步，未授权提交、发布、启用 hook/CI。沿用 Full SDD，调试/TDD/verification 作为专项检查表。

### 修改与根因对应

- R3：cwd 仅定位相对输入；通过限时 5 秒的 Git rev-parse 获取工作树根，再寻找其 lexical spelling，继续同时保护 lexical/resolved 路径。根缺失、非 Git、缺 Git或超时失败关闭；不引入根配置协议，不把 cwd 作为 fallback。
- R4：在生成每个已跟踪路径的 patch 前，使用 literal pathspec + NUL 分隔的 ls-tree 检查 base 旧模式，只接受普通 blob 模式 100644/100755；当前侧仍保留 lstat/二进制/符号链接拒绝。因此删除/替换旧 symlink/gitlink 不再绕过类型门禁。
- 兼容说明：Claude adapter 明确需要 Git 工作树；非 Git 输入不可冒称 repo 路径，需要显式切换可信 event + 人工门禁。policy/security 同步。旧 alias fixture 只增加 Git 初始化，没有删改保护断言。无新增第三方依赖、审批服务或通用框架。
- Spec 记录本次确认，四个依赖 upstreamHash 更新为 `sha256:2a6b021842c609507eaa6b5adbd8bb3d586890f3ec741f14835bf957c0d7e3bc`；parent/S1 冻结合同未修改。

### 证据

```text
python3 -m unittest discover -s tests -p 'test_guardrails.py'
RED: exit 1; Ran 26 tests; failures=21
  16 个子目录路径漏 ask + 非 Git 根误通过 + 4 个旧类型删除/替换误通过
python3 -m unittest discover -s tests -p 'test_guardrails.py' -k root_lookup
RED: exit 1; 缺 Git 未阻断
python3 -m unittest discover -s tests -p 'test_guardrails.py' -k hook
R3 GREEN: exit 0; Ran 8 tests; OK
python3 -m unittest discover -s tests -p 'test_guardrails.py'
R4/全量 GREEN: exit 0; Ran 27 tests; OK

python3 /tmp/s2-spec-review.9Y6FJ5/probe.py
exit 0; 原 root/subdir 四个请求全部返回对应 control 的 ask
在原临时 repo 中运行 checker --git-diff HEAD
exit 1; unsupported diff，stdout 无 passed:true（旧 symlink → regular）

bash scripts/check_framework.sh
exit 0; progressive-sdd passed; Ran 27 tests / OK;
PASS 7 artifact fixtures; PASS 9 artifact templates; PASS transition;
PASS offline policy oracle (18 cases); PASS external scorer self-check (18 cases);
live capability=external-results-required, mode=non-blocking;
ai-code-copilot framework check passed

python3 scripts/check_artifact_chain.py --policy config/workflow-policy.json --change-dir changes/ai-native-sdlc-alignment --require-chain
exit 0; PASS 17 artifacts
python3 -m py_compile scripts/check_guardrails.py tests/test_guardrails.py
bash -n hooks/pre-tool-guardrail
git diff --check
各 exit 0
```

### 本地复核 / Loop

- Done Signal：R3/R4 原反例及扩展边界已有永久回归；27 tests/17 artifacts/framework 通过。原 R1/R2 回归未削弱。
- Guardrails：真实仓库 checker `--git-diff HEAD --task-mode fix --risk security` 仍 exit 1 / passed=false，protected-path-edit、fix-test-integrity、high-risk-human-gate 为 ask；未伪造审批。未提交、未发布、未启用 hook/CI，未改个人配置。
- 消融：单独修正根定位后 hook 回归通过，再修正旧模式检查使剩余类型负例通过；两个检查各对应当前失败验收，无额外预留抽象。未关闭真实安全控制。
- Fallback：无法确定可信根时阻断而非假定覆盖；独立 Stage 1 重审及 Stage 2 仍待执行，本地自查不能替代。S3 未实施。
- Memory：路径安全规则的坐标系必须是受信任的仓库根；删除/替换的类型验证必须包含旧对象，不能只检查仍然存在的新对象。

## 2026-09-03 — 独立重审：R1–R4 验收通过，Stage 1 因 R5(P2) FAIL

用户明确请求“独立重审”。Reviewer：`/root/spec_rereview`，fork_turns=none、独立上下文；主 Agent 负责基线检查、缺陷复验与记录。未修改实现/测试、未提交或启用 hook/CI。

### 基线与新鲜验证

- 分支 feat/ai-native-sdlc，HEAD 4b16be6，含未提交与 untracked S2 文件。
- checker SHA256：`ecc174b0711570f5faf0fdf4e5caf613cd9aa274d478f329602e4057b9bcdf70`。
- tests SHA256：`df33493259a3595693617792a722a091349007010fce3631426b0669a08b8ac9`。
- policy SHA256：`770dd0235be16ae2fff916541f9c1f59a22a2b2beb530f823bcc08cf7b7f72fe`。
- Spec SHA256：`2a6b021842c609507eaa6b5adbd8bb3d586890f3ec741f14835bf957c0d7e3bc`。
- Artifact Chain：exit 0 / PASS 17 artifacts；guardrail suite：27 tests OK；framework：exit 0，27 tests、7 artifact fixtures、9 templates、transition、18 offline oracle/scorer cases 全部通过；git diff --check exit 0。
- 独立 reviewer 亲自核验 R1–R4 实现与回归，功能修复验收通过，未发现这些项的残留绕过。三层控制、脱敏、审批约束、范围与消融仍有实现/测试支撑。

### R5 [P2] Git 运行时缺失未报告可诊断的 degraded 状态

- 位置：`scripts/check_guardrails.py:260-262`；缺 Git 的 FileNotFoundError 被 OSError 总捕获归类为 invalid input/policy/unsupported diff。Git 查询超时也折叠进相同通用错误。wrapper 仅保持 exit 2，不补充原因。
- 明确合同依据：S2 spec 第 26 行、test-spec 第 43 行及 rules/security.md 第 55 行均要求缺运行时/故障明确报告 degraded；Git 是 R3 新声明的必要运行时。这不是未启用宿主的非目标，也不只是要求某个特定单词。
- reviewer 与主 Agent 分别真实复验缺 Git：使用绝对 Python 可执行路径调用 checker --hook-input -，仅将子进程 PATH 设为不存在目录；发送正常 Git 仓库 cwd、Write src/safe.py、content=safe。
- 结果：exit 2、stdout 空；stderr 为 `guardrails: invalid input/policy or unsupported diff; correct input or request human review (content redacted)`，没有表明 Git 依赖不可用或恢复方式。安全失败关闭正确，不是 P1 权限绕过。
- 影响：Agent/用户无法区分输入错误与 adapter runtime 不可用，不能按声明的恢复/切换路径诊断；现有缺 Git 测试只断言 exit 2/空 stdout，漏掉诊断验收。
- 修复方向：保留退出码与脱敏规则，仅区分可诊断的运行时降级和输入错误，输出安全原因及人工恢复/fallback 指引；补缺 Git/超时输出断言，不需要新错误框架或适配服务。本轮未实施。

### 当前结论与范围

- Stage 0 PASS；独立 Stage 1 FAIL，唯一新发现为 R5(P2)。R1–R4 的通过不等于整体 Spec 合规。
- 按当前 review workflow，Stage 1 未通过，不启动 Stage 2 Code Quality reviewer；没有把单阶段重审写成双阶段完成。
- 真实宿主启用、人工授权及发布门禁仍未解除。workIssue pending(on-publish) 不是本地审查阻断原因。官方来源本轮未重新研究。
- 只更新现有审查记录与状态，不降低 Acceptance、不修实现、不提交/发布或启用 hook/CI。

## 2026-09-03 — 用户确认 R5 修复、独立审查及 Issue/PR

用户“是的”授权 ting2tao 身份、R5 修复、独立双阶段审查及向 main 提交 PR；不包含合并或启用 hook/CI。已创建 https://github.com/ting2tao/ai-code-copilot/issues/36，standalone、closeTarget=workIssue，仅交付 S1/S2，S3 不在本票内。

- R5 根因：Git 运行能力故障与输入校验共同使用 ValueError/OSError 总分支，丢失恢复所需分类。增加一个窄范围 GitUnavailable 异常，固定安全原因区分不可执行、超时、查询失败；专门输出 degraded/blocked/恢复 Git 或显式可信 event + human review，退出码不变。不回显原始底层异常或 stderr；不增加通用错误框架。
- RED：缺 Git 输出断言 1 项失败；timeout/非零返回诊断断言 2 项失败（运行 degraded 子集 2 methods，2 failures）。
- GREEN：`python3 -m unittest discover -s tests -p 'test_guardrails.py'` exit 0，Ran 28 tests / OK。保留原 27 tests，不削弱 fail-closed/敏感内容断言。
- 合同更新：S2 Spec 记录用户本次授权与 Issue；parent Spec 只机械解析当前交付工作票并将原确认 hash 标明历史，后续 S3 验收未变；依赖 upstreamHash 同步。
- 当前等待独立 Stage 1/2；不以本地通过覆盖历史审查结果。

## 2026-09-03 — 独立 Stage 1 PASS 与最新 main 集成风险

- Reviewer：`/root/release_spec_review`，独立上下文、只读审查；当前分支 S1/S2 Spec Compliance PASS，R1–R5 均通过独立复验，无新增阻断性合规发现。
- 新鲜证据：28 tests OK；framework check passed；Artifact Chain PASS 17 artifacts；git diff --check exit 0。额外 CLI 探针覆盖缺 Git、TimeoutExpired、Git 非零执行，均 exit 1、stdout 空、明确 degraded/恢复指引且不回显原始错误。
- 结论不代替 Stage 2、人工批准或最新 main 集成验证。已启动另一独立 reviewer `/root/release_quality_review`，尚未收到结论。
- fetch 发现 origin/main 为 `ee028aa4bbeba35247b32fa63d6a66bf6e9145e6`，PR #35 已合入 model-first-versioning；共同基线为 `d5b44d4fd80b23f27f67d68f9f4d4149a3ebcf3e`。main 侧 45 文件变更包括 policy v2、删除 Inline workflow；read-only merge-tree 已显示当前已提交 S1 与 main 有文本冲突，未评估完整 S2 的合并结果。
- 未 merge/rebase/reset，不自动扩展到 model-first 适配；已向用户询问先交付标明冲突的 Draft PR 还是先适配 main。无 GitHub Actions/CodeQL 配置，PR 必须明示缺口，不静默合并。
- 整个 S1/S2 diff 的发布预检（共同基线、operation=publish、taskMode=finish、risk=security）exit 1 / passed=false，仅 protected-path-edit 与 high-risk-human-gate 为 ask；没有伪造 approval 或 PASS。后续变更会使 eventHash 变化，最终快照必须重新扫描与确认。

## 2026-09-03 — 独立 Stage 2：NEEDS_INFO，R6(P2) 与人工门禁

- Reviewer：`/root/release_quality_review`，独立上下文、只读审查。无 Critical；一项 Important/P2；Guardrail 人工批准 NEEDS_INFO，不能无条件 PASS。
- R6 位于 `scripts/check_artifact_chain.py:153-161`：循环忽略无 metadata 的 Markdown；require_chain 仅在整个目录零 artifact 时失败。对于新 Full 中无下游引用的 tasks.md，移除 metadata 会让其脱离 hash/status/source 校验而静默通过，违反 review Stage 0 的缺 metadata FAIL 合同。
- Reviewer 与主 Agent 各自复验：在 unittest.mock.patch 的 Path.read_text 包装中仅对 S2 tasks.md 内存移除 ARTIFACT_BLOCK，磁盘不变。baseline `PASS 17 artifacts`；变体 `PASS 16 artifacts`。建议仅覆盖已识别标准 artifact 文件并补 mixed-present/missing 负例，不强制任意附属 Markdown 成为 artifact。尚未修改实现/测试。
- 独立验证仍为 28 tests OK、framework PASS、实际链 PASS 17、git diff --check exit 0；这些绿色结果未覆盖 R6，不能作为整体完成证明。R1–R5 无残留发现。
- 实际完整 diff 审查扫描（共同基线 d5b44d4、operation=review、taskMode=review、risk=security）exit 1，4 个 protected-path-edit ask、high-risk-human-gate ask、review-context warn；无 secret/PII block。没有当前 eventHash 的人工批准凭据；用户此前确认仅是工作范围授权，未包装为机器审批。
- Stage 1 的历史 PASS 保留，但 Stage 2 新发现使整体发布不可用；不将 R6 藏入 S3，也不以重复全绿检查覆盖反例。主 Agent 首次复验误用了不存在的 load_policy API（AttributeError），改用实际 artifact_policy API 后复验成功。
- 当前 Issue #36 已创建；本轮没有 commit/push/PR、merge/rebase 或启用 hook/CI。下一步需确认 R6 修复，以及先适配最新 main 还是先准备冲突 Draft PR；修复后需新鲜验证、重新审查和精确差异人工批准。

## 2026-09-07 — 最终独立双阶段重审 PASS

- `origin/main` ee028aa4 的三方集成冲突已解决，保留 main 的 Native/Compact/Full、policy v2、安装覆盖/同步合同；VERSION 为 0.2.0。merge 仍未提交，安全 stash `093bea9a7773063d5d38bbf34cec2418b20b6e61` 保留。
- 独立 Stage 1 reviewer `/root/final_spec_rereview` 复验 R1–R6、I1/I2 与 main 集成，结论 PASS。独立 Stage 2 reviewer `/root/release_quality_final` 对最新相邻修复复验后结论 PASS：0 Critical、0 Important、0 Minor。
- Stage 2 首轮新发现的数值 case id、可选 expected 字段和 policy selector 拼写问题，均先由反例确认 RED，再通过现有 validator 最小修复。guardrail risks/operations/taskModes 采用支持值封闭集合；paths/patterns 仍可扩展，防止 typo 静默失效而不建立新策略语言。
- 新鲜验证：guardrail 30 tests、eval 6 tests、version 1 test，全量 37 tests OK；11 artifact fixtures、9 templates、17 当前 artifacts、21 offline oracle/scorer 与 framework 全部 PASS；`py_compile`、hook `bash -n`、Git diff checks 无错误。
- Git/Issue review READY；Publish NEEDS_INFO 仅因最终未变快照仍需 `protected-path-edit` 与 `high-risk-human-gate` 的精确 eventHash 人工批准。旧 hash 已因修复/记录更新失效，不复用。批准前不 commit/push/PR；不合并、不启用 hook/CI、不实施 S3。

### 发布扫描自举误拦截修复

- 最终扫描首次运行时，checker 将测试源码 hunk 内的字符串 `GIT binary patch` 误认为真实二进制补丁并 fail-closed，未生成 eventHash；仓库没有二进制 diff，未绕过门禁。
- 新增 tracked 纯文本同时包含 `GIT binary patch` 与 `Binary files` 字样的回归，修复前稳定 RED。最小修复只在首个 diff hunk 之前识别 Git 的真实 binary marker；hunk 内文本继续作为普通新增行扫描。原真实二进制负例与新纯文本正例均 GREEN。
- 此修复不增加文件格式抽象或自定义 patch parser，仅校正现有 Git unified diff 的结构边界；完成后重新暂存、全量验证、独立增量复核并重新生成全部 eventHash。
