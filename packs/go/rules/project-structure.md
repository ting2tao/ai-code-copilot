---
trigger: always_on
name: go-project-structure
description: Go 项目结构与依赖边界
globs: "*.go,go.mod,go.work"
---
# Go 项目结构

- `cmd/<app>/main.go` 只做启动组装，不写业务逻辑。
- `internal/<domain>/` 放业务核心，避免跨 domain 直接访问内部细节。
- `internal/<domain>/repository` 或等价目录只做数据访问，不承载业务编排。
- 配置读取、日志、指标、数据库连接等基础设施应在启动阶段组装并注入。
- 不要引入全局可变状态，除非 spec 说明生命周期和并发安全策略。
