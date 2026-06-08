---
trigger: always_on
name: go-verification
description: Go 变更验证要求
globs: "*.go,go.mod,go.work,*.proto,*.yaml,*.yml"
---
# Go 变更验证

## 验证原则

- 所有 Go 代码改动必须对受影响 package 执行测试；跨 package 契约变化必须执行 `go test ./...`。
- 修改导出类型、接口、错误语义或 package API 时，必须检查调用方是否同步调整。
- 修改 context、goroutine、channel、锁、重试或超时逻辑时，必须增加或执行针对并发/取消路径的测试。
- 修改持久化、外部 IO、协议合约或生成代码时，必须验证生成物和调用方一致。

## 场景矩阵

| 改动场景 | 最低验证 |
|----------|----------|
| package API、导出类型、接口 | `go test ./...` |
| 业务逻辑、错误处理 | 目标 package 测试；必要时全量测试 |
| 并发、context、取消/超时 | `go test -race` 或针对性并发测试 |
| DAO、外部 IO、协议合约 | 集成/契约测试；生成器可用时重新生成 |
| 格式化、lint | `gofmt -w <files>`；配置了 golangci-lint 时执行 |
