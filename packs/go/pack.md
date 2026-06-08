# 规则包：go

## 检测规则

以下任一文件存在则命中本包：
- `go.mod`
- `go.work`

命中后继续识别细分信号：
- Go module / Go workspace
- `internal/` 私有代码布局
- `cmd/` 可执行入口
- `api/`、`proto/`、OpenAPI 合约目录
- `golangci-lint` 配置

## 项目扫描命令

```bash
find . -name "*.go" -not -path "./vendor/*" -not -path "./.git/*" | head -100
```

## 规则文件

`/init` 命中本包时，复制以下规则到项目级 `.ai_code_copilot/rules/`：

- `packs/go/rules/coding-style.md`
- `packs/go/rules/project-structure.md`
- `packs/go/rules/verification.md`

## 常见架构

```
cmd/                  ← 可执行入口
internal/             ← 私有业务代码
pkg/                  ← 可复用公共库（谨慎新增）
api/                  ← OpenAPI/proto/接口定义
configs/              ← 配置样例
```

## 构建与测试命令

| 操作 | 命令 |
|------|------|
| 依赖整理 | `go mod tidy` |
| 编译检查 | `go test ./...` |
| 跑全量测试 | `go test ./...` |
| 跑单包测试 | `go test ./path/to/pkg` |
| 格式化 | `gofmt -w <files>` |

## 变更验证矩阵

| 改动场景 | 建议验证 |
|----------|----------|
| 导出类型、接口、package API | `go test ./...`；配置了 `go vet` 时一并执行 |
| 业务逻辑或错误处理 | 目标 package 测试 + `go test ./...` |
| 并发、context、取消/超时 | `go test -race ./path/to/pkg` + 针对性超时/取消测试 |
| 持久化、外部 IO、生成合约 | `go test ./...`；有生成器时重新生成合约 |
| 格式化或 lint 敏感改动 | `gofmt -w <files>`；配置了 golangci-lint 时执行 |

## 依赖读取命令

```bash
cat go.mod
```
