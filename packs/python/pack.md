# 规则包：python

## 检测规则

以下任一文件存在则命中本包：
- `pyproject.toml`
- `requirements.txt`
- `setup.py`
- `poetry.lock`
- `uv.lock`

## 项目扫描命令

```bash
find . -name "*.py" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./.git/*" | head -100
```

## 规则文件

`/init` 命中本包时，复制以下规则到项目级 `.ai_code_copilot/rules/`：

- `packs/python/rules/coding-style.md`
- `packs/python/rules/project-structure.md`

## 常见架构

```
src/<package>/        ← 应用代码
tests/                ← 测试
scripts/              ← 一次性脚本或运维脚本
pyproject.toml        ← 依赖、工具、构建配置
```

## 构建与测试命令

| 操作 | 命令 |
|------|------|
| 依赖安装 | `uv sync` 或 `pip install -r requirements.txt` |
| 类型检查 | `mypy .` 或 `pyright` |
| 跑全量测试 | `pytest` |
| 跑单文件测试 | `pytest path/to/test_file.py` |
| 格式化/Lint | `ruff check .` / `ruff format .` |

> `/init` 应根据项目实际工具链选择命令；没有对应工具时询问用户补齐。

## 依赖读取命令

```bash
cat pyproject.toml 2>/dev/null || cat requirements.txt
```
