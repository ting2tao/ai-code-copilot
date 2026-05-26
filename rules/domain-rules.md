---
alwaysApply: false
description: "当涉及业务领域特定逻辑、金额计算、状态流转时应用本规则"
---
# 业务领域约束

> 本文件是模板，各项目应在 ai_code_copilot/rules/domain-rules.md 中覆盖为项目特定规则。

## 1. 通用领域规则

- 所有金额使用 Long 类型，单位为分（100 = 1元）
- 时间字段统一使用 Date 类型（或 LocalDateTime），禁止用 String 存储时间
- 外部接口调用必须设置超时（默认 connect 1s，read 3s）并做降级处理
- 状态变更必须通过状态机，禁止直接调用 setter 修改状态字段

## 2. 项目特定规则

（各项目在 /init 后，在 ai_code_copilot/rules/domain-rules.md 中补充）

示例格式：
- **订单状态机**：状态流转只能通过 OrderStateMachine.transition()，合法路径：CREATED→PAID→SHIPPED→DONE / CREATED→CANCELLED
- **幂等策略**：所有写接口以 outBizNo（外部业务单号）作为幂等 key
- **金额校验**：actualPaidFee 必须 ≤ orderAmount，否则抛 BizException(AMOUNT_OVERFLOW)
