# Workflow Module: Full SDD

Full SDD 用于高风险、跨模块、超过五文件、多目标或需要完整审计的变更。

## Issue lifecycle

```text
always     -> resolve workIssue before implementation
on-commit  -> local edits allowed; resolve workIssue before first commit
on-publish -> local edits and commits allowed; resolve workIssue before push/PR
manual     -> never auto-create; validate supplied Issue when present
missing    -> invalid configuration; stop and report
```

全量记录从提案开始保存 Issue 状态，但只在策略门禁到达时执行创建。已存在的 open work Issue 必须复用；部分成功后不得创建替代票；有 work Issue 时 `closeTarget` 为 workIssue，manual/no-Issue 时为 none，parent 永不由子变更关闭。

## Record set

- `design-brief.md`: 需求理解、现状、2-3 方案、风险、YAGNI 和确认。
- `spec.md`: Goal Contract、行为、范围、Non-goals、Acceptance、Harness、Domain Check。
- `tasks.md`: 精确文件、符号、依赖顺序、验证和 commit 单元。
- `test-spec.md`: P0/P1/P2、无需测试项、命令和可见证据。
- `log.md`: 决策、失败、验证、review、knowledge candidates。
- `summary.md`: 不超过约定预算的 active change 摘要。
- `roadmap.md`: Complex 子变更依赖、集成顺序和上游 summary。

## Artifact Chain

新建或升级的 Full 记录必须使用 `workflow-policy.json.artifacts` 的 versioned metadata：`artifactVersion / artifactId / artifactType / artifactStatus / sourceOfTruth / sourceRef / sourceRevision / upstream / upstreamHash`。`design-brief.md` 是 intent-equivalent 根产物，`tasks.md + test-spec.md` 是 plan-equivalent 产物；不额外创建同义 `intent.md` 或 `plan.md`。

- 每阶段开始前运行 `scripts/check_artifact_chain.py`，确认上游存在、类型允许且 hash 未漂移。
- draft 可暂用 `upstreamHash: pending`；approved/active/reviewed/finished 必须固定真实 `sha256:`。
- material 上游变化先 Reverse Sync 并重新确认；metadata/path/hash 的机械同步保留原确认来源并记录 provenance。
- `sourceOfTruth` 必须唯一声明为 repository/GitHub/external；副本只存链接和 revision，不形成双权威。
- repository artifact 在工作区使用 `sourceRef: self / sourceRevision: working-tree`；提交或 finish 后把 revision 更新为 `git:<sha>`，形成 Git audit linkage。
- 无 metadata 的历史记录走 legacy skip；新建 Full 或显式 `--require-chain` 不得跳过。

## brainstorm

读取项目现状和可用 Harness；一次只问一个问题；给 2-3 方案和推荐；逐段确认需求、方案、风险；生成 design brief。涉及父 Issue 时先读整体需求和已完成 sibling。

## propose

从已确认设计和真实代码生成完整记录。Goal Contract 是 Spec 首部：Goal、Done Signal、Guardrails、Fallback、Memory，不再创建独立文档。Harness 从 Acceptance/Done Signal/Guardrails/Fallback 派生。复杂领域补充 Language、Boundary、Invariants、State Transitions、Owner。生成每个 artifact 后立即写入上游 ID/hash；Spec 确认后将相关 draft 状态与 hash 同步为 approved/active。

## apply

1. 校验 Spec 确认、hash、Issue policy、branch、dirty worktree 和所有目标路径。
2. 按 tasks 原子执行；行为变更采用 Red/Green。
3. 每个 task 运行验证并写 command、exit code、output summary。
4. 遇到 Spec 与现实不符先 Reverse Sync。
5. mechanical Reverse Sync 自动记录；material Reverse Sync 停止并重新确认。
6. commit message 使用 `type(scope): description`，并立即写入记录源。

## 恢复检查与有界执行

依据 `docs/harness-engineering.md`，开始或恢复时核验合同、Git revision/dirty diff、最近验证、未决批准与已发生副作用；summary 只是索引，不能代替当前事实。在现有 Fallback 记录长任务的预算与停止条件，每轮推进一个可验证步骤。副作用结果不明时先查询或请求人工判断，不盲目重放；handoff 复用 summary/log，包含下一条验证命令。复用宿主循环和权限设施，不因这些原则新增 runtime 或强制多 Agent。

## Guardrail execution

读取 `config/guardrail-policy.json`：advisory 提示、deterministic 检测、human 判断互补，不互相冒充。按 `rules/security.md` 的 CLI 合同验证当前 event/diff，记录 command、exit code、eventHash、control IDs、capability 和人工 evidence。Hook 只覆盖声明的工具，不能代替最终 diff 扫描；不得由 Agent 自行填写 approval 获得授权。

## 消融优先（Ablation）

对新增抽象、规则和产物，先问“拿掉它、用直接实现替代，会破坏哪个当前验收或安全边界？”固定输入和 Acceptance，单次只减少一个因素；可执行时在隔离环境比较 baseline / removed / restored 的证据。无法执行只写反事实分析，不冒充实验。

没有当前需求或失败证据支撑的扩展点优先删除/延后；证据不足写明待验证。保留有边界隔离、实际复用或风险控制证据的必要抽象，不追求层数最少。结论复用 design-brief 的 YAGNI 和现有 log；小改动一句理由即可，不新增消融文档或审批阶段。禁止以消融为名删除测试、弱化 Acceptance、关闭真实安全/权限/生产门禁；离线样本全绿也不等于风险不存在。

## Native -> Full

原生调查直接发现 full risk 时跳过 Compact：停止编辑，生成完整记录，复制 Native contract/diff/evidence，标记 promotion provenance，等待 material confirmation 后继续。
