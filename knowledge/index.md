---
description: 知识库索引模板 — /init 时复制到项目，/archive 时更新
alwaysApply: false
---

# 知识库索引

> 本文件由 AI 在 `/archive` 时自动维护。格式规范：`- **关键词**: 一句话摘要 → \`文件名.md\``
> 关键词用于 AI 按需加载：当对话涉及该关键词时，AI 读取对应知识文档补充上下文。

## 业务知识

<!-- 示例（初始化后删除）：
- **订单状态机**: 状态流转只能通过 OrderStateMachine，禁止直接 set → `order-state-machine.md`
- **库存扣减**: 扣减必须走 InventoryService.deduct()，不可绕过锁机制 → `inventory-rules.md`
-->

（暂无，通过 /archive 沉淀）

## 技术约定

<!-- 示例（初始化后删除）：
- **分布式锁**: 统一用 RedisLockHelper，TTL 默认 30s → `redis-lock.md`
- **分页查询**: 禁止 SELECT *，必须显式列字段，超过 1000 条必须分批 → `query-rules.md`
-->

（暂无，通过 /archive 沉淀）

## 踩坑记录

<!-- 示例（初始化后删除）：
- **MyBatis 批量插入**: 超过 1000 条需分批，否则 OOM → `mybatis-batch-insert.md`
- **事务嵌套**: @Transactional 在同类内部调用不生效，必须注入自身或拆服务 → `transaction-pitfalls.md`
-->

（暂无，通过 /archive 沉淀）

## 架构决策

<!-- 示例（初始化后删除）：
- **异步通知**: 选用 RocketMQ 而非 Kafka，原因：现有基础设施已有 RocketMQ → `async-design.md`
-->

（暂无，通过 /archive 沉淀）
