---
trigger: always_on
name: python-coding-style
description: Python 编码规范
globs: "*.py"
---
# Python 编码规范

## 类型与边界

- 新增公共函数、服务方法、复杂数据结构必须写类型标注。
- 领域对象优先使用 dataclass、Pydantic model 或项目既有模式表达。
- 避免把业务逻辑写在脚本入口、路由函数或 notebook 中。

## 错误处理

- 不得裸 `except:` 或吞异常；捕获时必须处理或补充上下文后抛出。
- 自定义异常应表达业务语义，避免到处抛 `Exception`。
- 外部 IO 调用必须设置 timeout，并在 spec 中说明重试/降级策略。

## 依赖与环境

- 不在代码中动态修改 `sys.path`，除非项目已有明确约定。
- 新依赖必须写入项目依赖文件，并说明引入原因。
- 脚本类代码必须可重复执行，避免隐藏全局状态。

## 测试

- 使用 pytest 时，测试名表达行为而不是实现细节。
- fixture 只承载准备数据，不隐藏断言。
- 修改核心逻辑必须覆盖正常路径、错误路径和边界条件。
