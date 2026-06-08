---
trigger: always_on
name: java-spring-verification
description: Java/Spring 变更验证要求
globs: "*.java,pom.xml,build.gradle,build.gradle.kts,application*.yml,application*.yaml,application*.properties"
---
# Java / Spring 变更验证

## 验证原则

- 优先使用项目已有 Maven/Gradle 命令；多模块项目必须验证受影响模块及其调用方。
- 修改 Controller、DTO、参数校验或接口响应时，必须验证请求/响应契约。
- 修改 Service 业务逻辑、事务边界、状态流转时，必须覆盖成功路径和失败/回滚路径。
- 修改 DAO、mapper、SQL 或持久化模型时，必须执行 repository/mapper 级验证。
- 涉及权限、资金、状态机、删除、发布等敏感流程时，必须执行正反用例并人工审查。

## 场景矩阵

| 改动场景 | 最低验证 |
|----------|----------|
| Controller、DTO、接口契约 | Controller/API 测试；必要时契约回归 |
| Service 业务逻辑、事务 | Service 单测；全量测试 |
| DAO/mapper、SQL、持久化模型 | mapper/repository 集成测试 |
| 配置、profile、启动链路 | 编译检查；可用时启动 smoke test |
| 权限、状态流转、资金、破坏性操作 | 正反权限用例；人工审查 |
