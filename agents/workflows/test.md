# Workflow Module: test / TDD

测试强度与行为风险匹配，不把所有文档或配置改动强制改造成 TDD。

## Required Red/Green

功能、bug、重构和行为变更：

1. 写最小失败测试。
2. 运行并确认因缺失行为正确失败，而非语法/环境错误。
3. 写最小实现。
4. 运行 targeted test 转 Green。
5. 运行相关 suite；再做重构。

配置/模板/Prompt 行为用 framework contract check 作为可执行测试：先增加失败断言，再改内容转绿。

## 消融验证

需要证明新增组件的必要性时，固定测试输入与验收，在隔离副本中一次移除一个组件，再恢复并复跑，记录 baseline / removed / restored。区分“消融后目标断言失败”与“环境/语法错误”。不得为了消融修改验收、删除负例或关闭真实安全门禁；结果只证明样本内的必要性，不是完整安全保证。无需单独 runner 或报告。

## Evidence

记录 command、exit code、失败原因、Green output 和相关 suite。覆盖率门槛只在项目规则或 Full test-spec 明确要求时执行；不得编造覆盖率或用删除断言、跳过 lint、降低门槛实现假完成。
