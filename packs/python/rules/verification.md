---
trigger: always_on
name: python-verification
description: Python 变更验证要求
globs: "*.py,pyproject.toml,requirements.txt,setup.py,*.ini,*.toml"
---
# Python 变更验证

## 验证原则

- 优先使用项目已有工具链；没有 pytest、ruff、mypy/pyright 时，不为单次验证临时引入新工具。
- 修改公开函数签名、数据模型、schema 或序列化逻辑时，必须验证调用方和类型检查。
- 修改 async、重试、超时、外部 IO 或错误处理时，必须覆盖失败路径。
- 修改 CLI 或脚本时，必须用安全输入运行入口命令，避免真实写入生产资源。

## 场景矩阵

| 改动场景 | 最低验证 |
|----------|----------|
| 类型、schema、公开 API | 类型检查；`pytest` |
| 业务逻辑、数据转换 | 目标测试；必要时全量 `pytest` |
| async、重试、外部 IO | 针对性成功/失败路径测试 |
| CLI、脚本、运维入口 | 安全 fixture 运行命令；`pytest` |
| 格式化、lint | `ruff check .`；配置了 formatter 时执行 |
