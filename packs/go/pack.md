# 规则包：go

## 检测规则

以下任一文件存在则命中本包：
- `go.mod`
- `go.work`

## 项目扫描命令

```bash
find . -name "*.go" -not -path "./vendor/*" -not -path "./.git/*" | head -100
```

## 规则文件

`/init` 命中本包时，复制以下规则到项目级 `.ai_code_copilot/rules/`：

- `packs/go/rules/coding-style.md`
- `packs/go/rules/project-structure.md`

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

## 依赖读取命令

```bash
cat go.mod
```
