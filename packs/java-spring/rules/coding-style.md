---
alwaysApply: true
---
# 编码规范（Java / Spring Boot）

## 1. 命名

- 类名：大驼峰，见名知意，动词+名词（CreateOrderService, OrderQueryManager）
- 方法名：小驼峰，动词开头（createOrder, queryById, handleTimeout）
- 常量：全大写下划线分隔（MAX_RETRY_TIMES, ORDER_STATUS_PAID）
- 抽象类以 Abstract 或 Base 开头
- 测试类以被测类名开头，Test 结尾（OrderServiceTest）
- ❌ 禁止拼音、中英混拼命名（如 dingdan, orderZhuangTai）

## 2. 异常处理

- 业务异常使用自定义 BizException，携带错误码
- 系统异常向上抛出，由统一异常处理器（GlobalExceptionHandler）兜底
- ❌ 禁止吞掉异常（空 catch {}）
- catch 中必须记录日志（log.error("xxx failed", e)）
- ❌ 禁止 catch (Exception e) { return null; } 这类静默失败

## 3. 日志

- Controller 入口打 INFO，包含请求关键参数（订单号、用户ID等）
- 异常打 ERROR，包含完整堆栈（log.error("msg", e)，不能只打 e.getMessage()）
- ❌ 禁止在日志中打印用户敏感信息（手机号、身份证、银行卡）
- 关键业务操作打 INFO（创建订单、状态变更、支付完成）

## 4. 接口设计

- 写接口必须考虑幂等（幂等 key 来源：业务单号、requestId 等）
- 涉及并发场景必须说明同步策略（数据库乐观锁/悲观锁/Redis 分布式锁）
- 魔法值必须定义为常量或枚举，禁止直接用字面量
- 方法体超过 80 行考虑拆分

## 5. 事务

- 事务边界在 Service 层，不在 Manager/DAO 层
- 事务方法必须是 public，不能通过内部调用触发（Spring AOP 限制）
- 涉及多表操作 → 必须在 spec 中说明事务策略

## 6. 其他

- 所有金额字段使用 Long 类型，单位为分，禁止 Double/Float
- 时间字段统一使用 Date 或 LocalDateTime，不用 String 存时间
- 外部接口调用必须设置超时（connect timeout ≤ 1s，read timeout ≤ 3s）并做降级处理
- 状态变更必须通过状态机，禁止直接 set 状态字段
