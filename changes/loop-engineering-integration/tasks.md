# 任务列表：loop-engineering-integration

> **关联 Spec**：`spec.md`
> **关联 Test Spec**：`test-spec.md`
> **零偏差原则**：Spec 是合同，tasks 是执行计划，不得擅自增删功能。
> 遇到 Spec 不足或逻辑冲突 → 立即停止，触发 Reverse Sync（先修 spec 再修代码）。

## Preflight

- [x] `git status --short` 已检查，未覆盖用户无关改动
- [x] spec.md 已记录关联 Issue：https://github.com/ting2tao/ai-code-copilot/issues/28
- [x] 当前分支不是 master/main
- [x] 本仓库无 `.ai_code_copilot/project-context.md`；使用框架自检命令 `bash scripts/check_framework.sh`
- [x] 本文件列出的目标文件路径仍匹配当前代码
- [x] 无数据库/接口/状态机/权限/资金相关风险；本次触发框架级 DDD-lite Domain Check，用于约束复杂业务场景的未来模板

## 进度概览

| Task | 描述 | 状态 | commit hash |
|------|------|------|--------|
| T1 | 定义 Loop Engineering 文档入口 | ✅ | 未提交 |
| T2 | 将 Goal Contract 嵌入 prompt、模板和 reviewer | ✅ | 未提交 |
| T3 | 更新 README/AGENTS 和自检脚本 | ✅ | 未提交 |
| T4 | 运行自检并回填证据 | ✅ | 未提交 |
| T5 | 读取用户下载的文章并校准定义/证据 | ✅ | 未提交 |
| T6 | 加入 DDD-lite Domain Check | ✅ | 未提交 |

---

## T1：定义 Loop Engineering 文档入口

**功能点**：F1
**文件**：
- 新建：`docs/loop-engineering.md`
- 修改：`docs/harness-engineering.md`

**完成标准**：
- [x] 文档说明 Loop Engineering 与 Harness Engineering 的关系。
- [x] 明确 loop 不是无限重试，而是有 Goal、Done Signal、Guardrails、Fallback、Memory。

**完成证据**：
```
bash scripts/check_framework.sh
ai-code-copilot framework check passed

rg -n "Loop Engineering|Goal Contract|Loop Evidence" docs README.md README-CN.md AGENTS.md agents changes/templates scripts
输出覆盖 docs/loop-engineering.md、docs/harness-engineering.md、README.md、README-CN.md、AGENTS.md、agents/copilot-prompt.md、reviewer、changes/templates 和 scripts/check_framework.sh。
```

**commit**：未提交

---

## T2：将 Goal Contract 嵌入 prompt、模板和 reviewer

**功能点**：F2/F3/F4
**文件**：
- 修改：`agents/copilot-prompt.md`
- 修改：`agents/spec-reviewer.md`
- 修改：`agents/code-quality-reviewer.md`
- 修改：`changes/templates/spec.md`
- 修改：`changes/templates/quick-card.md`
- 修改：`changes/templates/test-spec.md`
- 修改：`changes/templates/log.md`

**完成标准**：
- [x] propose 阶段会要求 Goal Contract。
- [x] apply/review/archive 阶段会使用 Loop Evidence。
- [x] 模板包含可填写的 Goal Contract/Loop Evidence 字段。
- [x] reviewer 能检查 loop 可验证性、可读性和 Goodhart 风险。

**完成证据**：
```
bash scripts/check_framework.sh
ai-code-copilot framework check passed

rg marker 输出显示：
- agents/copilot-prompt.md 包含 Goal Contract / Loop Evidence
- agents/spec-reviewer.md 包含 Loop Readiness / Goal Contract / Goodhart
- agents/code-quality-reviewer.md 包含 Loop 可观察性 / Loop 可调性
- changes/templates/spec.md、quick-card.md、test-spec.md、log.md 包含 Goal Contract / Loop Evidence
```

**commit**：未提交

---

## T3：更新 README/AGENTS 和自检脚本

**功能点**：F5/F6
**文件**：
- 修改：`README.md`
- 修改：`README-CN.md`
- 修改：`AGENTS.md`
- 修改：`scripts/check_framework.sh`

**完成标准**：
- [x] README 中英文同步说明 Loop Engineering。
- [x] AGENTS.md 保持短索引，并指向 `docs/loop-engineering.md`。
- [x] 自检脚本检查 Loop markers。

**完成证据**：
```
bash scripts/check_framework.sh
ai-code-copilot framework check passed

wc -l AGENTS.md
81 AGENTS.md
```

**commit**：未提交

---

## T4：运行自检并回填证据

**功能点**：F6
**文件**：
- 修改：`changes/loop-engineering-integration/test-spec.md`
- 修改：`changes/loop-engineering-integration/log.md`
- 修改：`changes/loop-engineering-integration/tasks.md`

**完成标准**：
- [x] `bash scripts/check_framework.sh` 通过。
- [x] `rg` markers 检查有输出。
- [x] 变更文档记录外部材料可读性限制和验证证据。

**完成证据**：
```
bash scripts/check_framework.sh
ai-code-copilot framework check passed

git status --short
显示本次修改集中在 AGENTS/README/agents/templates/docs/scripts 和 changes/loop-engineering-integration。
```

**commit**：未提交

---

## T5：读取用户下载的文章并校准定义/证据

**功能点**：F1/F5
**文件**：
- 修改：`docs/loop-engineering.md`
- 修改：`changes/loop-engineering-integration/spec.md`
- 修改：`changes/loop-engineering-integration/log.md`
- 视原文内容决定是否修改：`README.md`、`README-CN.md`、`agents/copilot-prompt.md`

**完成标准**：
- [x] 读取用户提供的文章文件或路径。
- [x] 将外部材料读取证据从“平台不可读/摘要可读”更新为“本地文件已读”。
- [x] 若原文对 Loop Engineering 的定义、组成或流程有更精确表述，校准 `docs/loop-engineering.md` 和 prompt/template 字段。
- [x] 重新运行 `bash scripts/check_framework.sh`。

**完成证据**：
```
sed -n '1,220p' /Users/tsnowy/Downloads/微信公众号文章.json
sed -n '1,220p' /Users/tsnowy/Downloads/tweet_2064127981161959567.json

读取结论：
- Addy：五件套 + memory，强调 verification、token cost、comprehension debt。
- 微信：核心是目标定义，完成标准、边界、失败降级、目标分层，提醒 Goodhart 风险。

bash scripts/check_framework.sh
ai-code-copilot framework check passed
```

**commit**：未提交

---

## T6：加入 DDD-lite Domain Check

**功能点**：F7
**文件**：
- 修改：`rules/domain-rules.md`
- 修改：`changes/templates/spec.md`
- 修改：`changes/templates/quick-card.md`
- 修改：`agents/copilot-prompt.md`
- 修改：`agents/spec-reviewer.md`
- 修改：`agents/code-quality-reviewer.md`
- 修改：`scripts/check_framework.sh`
- 修改：`changes/loop-engineering-integration/spec.md`
- 修改：`changes/loop-engineering-integration/tasks.md`
- 修改：`changes/loop-engineering-integration/test-spec.md`
- 修改：`changes/loop-engineering-integration/log.md`

**完成标准**：
- [x] Domain Check 只在金额、库存、额度、权限、状态机、跨模块业务协作、强一致性或领域词混淆时触发。
- [x] 字段收敛为 Language、Boundary、Invariants、State Transitions、Owner。
- [x] 明确不强制完整 DDD 分层或 Entity/Aggregate/Repository 命名。
- [x] propose/apply/review、spec/quick-card 模板和自检脚本都能识别 Domain Check。

**完成证据**：
```
bash scripts/check_framework.sh
RED: rules/domain-rules.md missing Domain Check markers: Domain Check, Language, Boundary, Invariants, State Transitions, Owner

bash scripts/check_framework.sh
GREEN: ai-code-copilot framework check passed
```

**commit**：未提交

---

## 变更完成检查

- [x] 所有 Task 均有完成证据（禁止"应该没问题"）
- [x] 无未解决的 TODO/FIXME
- [x] spec.md §9 待澄清事项已全部解决
- [ ] 已触发 /review
