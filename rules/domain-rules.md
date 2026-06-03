---
alwaysApply: false
description: "当涉及业务领域特定逻辑、金额计算、状态流转时应用本规则"
---
# 业务领域约束

> 本文件是模板，各项目应在 .ai_code_copilot/rules/domain-rules.md 中覆盖为项目特定规则。

## 1. 通用领域规则

- 金额必须使用精确数值模型，禁止使用浮点数表达货币金额；单位和舍入策略必须写入 spec。
- 时间必须使用明确时区和格式，禁止在不同层随意用字符串传递时间语义。
- 外部接口调用必须设置超时，并说明失败处理、重试和降级策略。
- 状态变更必须通过显式状态机或等价的领域方法，禁止绕过规则直接改状态字段。

## 2. 项目特定规则

（各项目在 /init 后，在 .ai_code_copilot/rules/domain-rules.md 中补充）

示例格式：
- **订单状态机**：状态流转只能通过领域状态机方法，合法路径：CREATED→PAID→SHIPPED→DONE / CREATED→CANCELLED
- **幂等策略**：所有写接口以 outBizNo（外部业务单号）作为幂等 key
- **金额校验**：actualPaidFee 必须 ≤ orderAmount，否则返回明确业务错误
