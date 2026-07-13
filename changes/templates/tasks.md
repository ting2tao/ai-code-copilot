# 任务列表：{变更名}

<!-- If this change is a Complex sub-project, load only this sub-project's
     spec/tasks/test-spec/log and the upstream log.summary declared in roadmap.md.
     See changes/templates/roadmap.md for the full isolation rules. -->

> **关联 Spec**：`spec.md`
> **关联 Test Spec**：`test-spec.md`
> **零偏差原则**：Spec 是合同，tasks 是执行计划，不得擅自增删功能。
> 遇到 Spec 不足或逻辑冲突 → 立即停止，触发 Reverse Sync（先修 spec 再修代码）。

## Preflight

- [ ] `git status --short` 已检查，未覆盖用户无关改动
- [ ] spec.md 或 quick-card.md 已记录已解析的 workIssue（#ID 或 URL）；或 manual/no-Issue 已显式记录 none
- [ ] parentIssue 已记录为 none / #ID / URL；有 workIssue 的合同中，parentIssue 存在时，workIssue 必须是 native sub-issue；standalone 仅在 parentIssue=none 时合法
- [ ] closeTarget 为 workIssue 且 PR closing keyword 只关闭工作 Issue；或 manual/no-Issue 时 closeTarget 为 none 且无 closing keyword；父 Issue 始终仅引用
- [ ] branch 已记录且符合 `type/scope` 格式（例如 `feat/issue-workflow`）
- [ ] 当前分支不是 master/main
- [ ] project-context.md 中的编译/测试命令可执行
- [ ] 本文件列出的目标文件路径仍匹配当前代码
- [ ] 数据库/接口/状态机/权限/资金相关风险已在 spec.md 标注，且有回滚说明

## 进度概览

| Task | 描述 | 状态 | commit hash |
|------|------|------|--------|
| T1 | {任务描述} | ⏳/✅/❌ | |
| T2 | | | |

---

## T1：{任务标题}

**功能点**：F1（对应 spec.md §2）
**文件**：
- 新建：`{路径}`
- 修改：`{路径}`

**完成标准**：
- [ ] {可验证的完成条件，例如：mvn test -pl xxx 通过}
- [ ] 代码可编译

**完成证据**：
```
见 log.md ## Verification log：{YYYY-MM-DD} - T1 {验证标题}
```

**commit**：`{hash} <type>(<scope>): {中文简述}`

---

## T2：{任务标题}

**功能点**：F2
**文件**：
- 修改：`{路径}`

**完成标准**：
- [ ] {可验证条件}

**完成证据**：
```
见 log.md ## Verification log：{YYYY-MM-DD} - T2 {验证标题}
```

**commit**：`{hash} <type>(<scope>): {中文简述}`

---

## 变更完成检查

- [ ] 所有 Task 均有完成证据（禁止"应该没问题"）
- [ ] 每个 Task 均已在 `log.md ## Verification log` 写入 command、exit code、output 摘要
- [ ] 无未解决的 TODO/FIXME
- [ ] spec.md §6 待澄清事项已全部解决
- [ ] 已触发 /review
