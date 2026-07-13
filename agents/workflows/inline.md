# Workflow Module: Inline SDD

Inline SDD 用于明确、低风险、可直接回滚的本地小改动。它降低持久化成本，不降低安全、范围和验证标准。

## Entry contract

编辑前在会话中明确：

```text
Goal: 要改变的单一结果
Scope: 最多两个预计文件和目标符号
Done Signal: 可观察的完成条件
Verify: 至少一个可执行 targeted command
```

用户输入已明确覆盖四项时，无需增加一轮形式化确认；否则只问一个阻塞问题或进入 Compact。

## Eligibility

必须全部满足：

- 预计不超过 policy 的 `maxFiles`、`maxPurposes`、`maxCommits`。
- 有 executable verification 和 direct rollback。
- 不涉及 public API、schema、DB、依赖、CI、部署、generated artifact、安全、权限、认证、敏感数据、资金、状态机、跨模块业务规则或 residual risk。
- 不需要跨会话、持久决策、多 commit、PR 或独立审查单元。
- 当前 `issuePolicy` 不要求 implementation 前解析 work Issue。

## Execution

1. 检查 git status，确认用户无关改动。
2. 读取真实代码路径和最近相关实现。
3. 修改 Scope 内文件。
4. 运行 Verify；失败时先定位根因，不叠加猜测修复。
5. 检查 diff 未越界。
6. 用实际 command、exit code、output summary 报告结果。

Inline 不创建 `quick-card.md`、`log.md`、`summary.md` 或 Issue。

## Runtime promotion

出现 policy `inlineToCompact` trigger 时，停止新增编辑并执行 `Inline -> Compact`。发现 full risk、material Reverse Sync 或高风险人工门禁时直接执行 `Inline -> Full`。

升级必须保留已有合同、diff 和验证证据；不得把已运行结果改写成未验证声明。活动变更不得自动降级。
