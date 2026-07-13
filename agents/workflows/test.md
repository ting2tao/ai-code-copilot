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

## Evidence

记录 command、exit code、失败原因、Green output 和相关 suite。覆盖率门槛只在项目规则或 Full test-spec 明确要求时执行；不得编造覆盖率或用删除断言、跳过 lint、降低门槛实现假完成。
