---
trigger: always_on
description: 新增项目或使用中间件时，必须优先选用【公司自定义组件&脚手架】，禁止直接引入外部开源组件
globs: "*.java"
alwaysApply: true
---
## AI 编程规则：公司自定义组件优先原则

### 规则核心

**新增项目或使用中间件时，必须优先选用【公司自定义组件&脚手架】，禁止直接引入外部开源组件。**

### 思维链（决策流程）

```
1. 【需求识别】→ 明确当前需要什么功能/中间件
   ↓
2. 【组件匹配】→ 对照公司组件清单查找对应解决方案
   ↓
3. 【版本确认】→ 统一使用最新版本 1.5.7.RELEASE
   ↓
4. 【验证检查】→ 确保没有遗漏可用组件
   ↓
5. 【实施应用】→ 按组件使用说明集成
```

### 完整组件映射表（必须按此选择）

| 功能场景 | 必须选用的公司组件 | 版本 | 备注 |
|---------|-------------------|------|------|
| **1. 项目初始化** | | | |
| - 依赖管理 | `zt-digital-dependencies` | 1.5.7.RELEASE | 顶级父依赖 |
| - 单体应用创建 | `zt-digital-springboot-parent` | 1.5.7.RELEASE | 单体应用父依赖 |
| - 微服务创建 | `zt-digital-springcloud-parent` | 1.5.7.RELEASE | 分布式微服务父依赖 |
| - 统一启动类 | `zt-digital-common-boot-starter` | 1.5.7.RELEASE | 必须使用 |
| **2. 基础框架** | | | |
| - API通用封装 | `zt-digital-common-api-base` | 1.5.7.RELEASE | API标准化 |
| - 工具类 | `zt-digital-common-utils` | 1.5.7.RELEASE | 通用工具集 |
| - API文档 | `zt-digital-common-swagger-starter` | 1.5.7.RELEASE | Swagger集成 |
| **3. 日志与监控** | | | |
| - 日志组件 | `zt-digital-common-log-starter` | 1.5.7.RELEASE | Logback+审计+SLA |
| - 监控组件 | `zt-digital-common-micrometer-starter` | 1.5.7.RELEASE | 服务治理监控 |
| - 字节码增强 | `zt-digital-common-agent-starter` | 1.5.7.RELEASE | AOP拦截组件 |
| **4. 配置与注册** | | | |
| - 配置中心 | `zt-digital-common-config-starter` | 1.5.7.RELEASE | 封装Apollo |
| - 注册中心(Nacos) | `zt-digital-common-register-starter` | 1.5.7.RELEASE | 首选Nacos |
| - 注册中心(Consul) | `zt-digital-common-register-consul-starter` | 1.5.7.RELEASE | 备选Consul |
| **5. 熔断限流与调用链** | | | |
| - 熔断限流降级 | `zt-digital-common-fuse-starter` | 1.5.7.RELEASE | 含调用链 |
| **6. 数据持久化** | | | |
| - MyBatis集成 | `zt-digital-mybatis-starter` | 1.5.7.RELEASE | |
| - 分库分表/读写分离 | `zt-digital-common-sharding-jdbc-starter` | 1.5.7.RELEASE | 含数据加密 |
| **7. 缓存** | | | |
| - Redis缓存 | `zt-digital-common-cache-starter` | 1.5.7.RELEASE | 封装Redis |
| **8. 消息队列** | | | |
| - RocketMQ | `zt-digital-common-message-starter` | 1.5.7.RELEASE | 首选 |
| - RabbitMQ | `zt-digital-common-message-rabbitmq-starter` | 1.5.7.RELEASE | 备选 |
| - Kafka | `zt-digital-common-message-kafka-starter` | 1.5.7.RELEASE | 备选 |
| **9. 安全与认证** | | | |
| - 安全认证 | `zt-digital-common-security-starter` | 1.5.7.RELEASE | Jwt+Oauth2.0 |
| - SSO单点登录 | `zt-digital-common-sso-starter` | 1.5.7.RELEASE | Cas集成 |
| - 网关安全 | `zt-digital-gateway-security-starter` | 1.5.7.RELEASE | |
| - 网关签名 | `zt-digital-gateway-sign-starter` | 1.5.7.RELEASE | |
| **10. 网关** | | | |
| - 网关API | `zt-digital-gateway-api-starter` | 1.5.7.RELEASE | |
| **11. 任务调度** | | | |
| - 分布式任务 | `zt-digital-common-job-starter` | 1.5.7.RELEASE | XXL-Job集成 |
| **12. 高级特性** | | | |
| - 灰度发布 | `zt-digital-common-grayscale-starter` | 1.5.7.RELEASE | |
| - 国际化 | `zt-digital-common-i18n-starter` | 1.5.7.RELEASE | |

### 关键检查点（防遗漏）

1. **版本一致性**：所有组件必须统一为 `1.5.7.RELEASE`
2. **功能覆盖检查**：每个技术领域都对应有公司组件
3. **禁止绕过**：不得以"公司组件没有"为由引入外部依赖，必须先确认清单
4. **README优先**：集成时先阅读对应组件的README说明

### 💡 使用示例

```
错误做法：直接引入 spring-boot-starter-data-redis
正确做法：引入 zt-digital-common-cache-starter 1.5.7.RELEASE

错误做法：直接引入 spring-cloud-starter-gateway
正确做法：引入 zt-digital-gateway-api-starter 1.5.7.RELEASE
```

### 验证清单（每次选型时核对）

- [ ] 是否已检查所有25个公司组件？
- [ ] 是否存在功能重叠需要选择的情况？
- [ ] 是否已阅读对应组件的README？
- [ ] 版本是否统一为1.5.7.RELEASE？
- [ ] 是否需要组合多个组件满足需求？

**记住：公司组件已经封装了最佳实践和企业规范，直接使用可确保架构统一、维护可控、技术栈一致。**
