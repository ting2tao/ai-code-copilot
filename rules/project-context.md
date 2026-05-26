---
alwaysApply: true
---
# 工程上下文

> 首次使用时在项目根目录执行 /init，AI 会分析工程并填充本文件的项目级版本。
> 全局此文件仅为占位模板。

## 1. 应用概况

- 应用名：（待 /init 填充）
- 简介：（一句话描述）
- 技术栈：（待 /init 填充，如：Java 21 / Spring Boot 3.x / Maven）
- 主要中间件：（待填充：MySQL、Redis、MQ 等）

## 2. 目录结构与模块职责

> 执行 `tree -d -L 3 src/` 后填充。

## 3. 分层架构

```
Controller (web/)      ← 入口层，参数校验 + 协议转换
    ↓
Service (service/)     ← 业务编排，事务边界
    ↓
Manager (manager/)     ← 领域能力，单一职责，可复用
    ↓
DAO (dao/)             ← 纯数据访问
```

## 4. 关键依赖

| 中间件 | 用途 | 备注 |
|--------|------|------|
| （待 /init 填充） | | |

## 5. 构建与测试命令

> /init 时由 AI 根据技术栈自动填充，也可手动修改。

| 操作 | 命令 |
|------|------|
| 编译检查 | `mvn compile -q` |
| 跑全量测试 | `mvn test` |
| 跑单模块测试 | `mvn test -pl <module>` |
