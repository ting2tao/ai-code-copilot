# fix-guardrail-selfcheck Log

## 基线证据（修复前，安装目录）

```text
command: cd ~/.claude/ai_code_copilot && bash scripts/check_framework.sh
exit: 1
summary: Ran 30 tests, FAILED (failures=2):
  test_hook_blocks_secrets_and_asks_for_protected_path
  test_hook_safe_pii_and_outside_root
root cause: 两测试以安装目录为 cwd，hook_event 依赖 git rev-parse --show-toplevel；
  install.sh staged 安装删除 .git（install.sh:104），安装目录必非 git 仓库 → degraded 拦截。
  源码仓库中同命令通过（.git 存在），确认是测试环境假设与安装设计冲突，非 hook 逻辑缺陷。
```

## 修复实施

- `tests/test_guardrails.py`：两个用例改为在 `tempfile.TemporaryDirectory` 中
  `git init` 的隔离仓库内执行（沿用文件内 `test_hook_preserves_protected_alias_path`
  等既有写法）；hook 逻辑、`install.sh`、`check_guardrails.py` 均未改动。
- `VERSION`：0.2.0 → 0.2.1（patch bump）；`README.md` / `README-CN.md` 版本引用同步。

## 验证证据

```text
command: bash scripts/check_framework.sh（源码仓库）
exit: 0
summary: ai-code-copilot framework check passed

command: cd ~/.claude/ai_code_copilot && python3 -m unittest tests.test_guardrails
exit: 0
summary: Ran 30 tests in 5.185s — OK（安装目录 = 无 .git 的托管树，即模拟安装环境）

command: bash install.sh --claude（重新部署 0.2.1）
exit: 0
summary: 直接覆盖更新: 0.2.0 → 0.2.1；symlink/hook 自检正常

command: cd ~/.claude/ai_code_copilot && bash scripts/check_framework.sh
exit: 0
summary: ai-code-copilot framework check passed
```

## Quick Review（轻量合规 + Code Quality）

- Spec Compliance: PASS — 改动范围与 quick-card 第 2 节一致；验收三项均以 exit 0 证据达成；未触碰 hook fail-closed 语义与 install.sh。
- Code Quality: PASS — 复用文件既有 temp-repo 惯用法，注释语言/密度与周边一致，无生产代码变更。
- 遗留：无。
