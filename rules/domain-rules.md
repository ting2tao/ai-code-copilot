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

## 2. Domain Check（DDD-lite，可选）

Domain Check 只用于复杂业务边界，不是完整 DDD 仪式。普通 CRUD、UI 调整、脚本、基础设施变更可填"不适用"。

触发条件：
- 涉及金额、库存、额度、权限、状态生命周期等强业务约束
- 涉及跨模块业务协作或强一致性边界
- 领域词含义不清，容易让 Agent 把业务概念写偏
- 实现需要维护业务不变量或状态流转规则

触发后，spec 或 quick-card 必须补齐以下字段：

| 字段 | 说明 |
|------|------|
| Language | 核心领域词及其精确定义，避免同词异义 |
| Boundary | 本次变更所属业务边界，以及明确不跨越的边界 |
| Invariants | 必须永远成立的业务不变量，如金额、权限、额度、唯一性约束 |
| State Transitions | 合法状态、合法流转、禁止流转和失败处理 |
| Owner | 领域规则负责人或需要人工确认的角色 |

禁止为满足 Domain Check 强行引入 Entity/Aggregate/Repository 等 DDD 结构名；只有项目已有 DDD 分层或复杂度真实需要时，才按项目既有风格落地。

## 3. 项目特定规则

（各项目在 /init 后，在 .ai_code_copilot/rules/domain-rules.md 中补充）

示例格式：
- **订单状态机**：状态流转只能通过领域状态机方法，合法路径：CREATED→PAID→SHIPPED→DONE / CREATED→CANCELLED
- **幂等策略**：所有写接口以 outBizNo（外部业务单号）作为幂等 key
- **金额校验**：actualPaidFee 必须 ≤ orderAmount，否则返回明确业务错误
