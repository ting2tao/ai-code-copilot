# Workflow Module: debug / fix / fix-ci

## Root-cause loop

1. 完整读取错误和失败命令，建立稳定复现。
2. 检查近期变更和正常工作的相似实现。
3. 写出一个可证伪假设：`问题是 X，因为证据 Y`。
4. 一次只做一个最小验证。
5. 对 bug 写复现测试并观察 Red，再做最小修复观察 Green。
6. 三次失败停止叠加修改，讨论架构或 Harness gap。

## Persistence and promotion

- 未激活时由模型原生完成低风险、单轮诊断；需要 durable decision、重复调查或多文件扩展时自动激活并执行 `Native -> Compact`。
- 发现 full risk 或 material contract change 触发 Full。
- `/fix` 同步当前档位记录；不得向不存在的 log 写入。
- `/fix-ci` 读取失败 job 的实际日志、workflow trigger、branch protection 和可复现本地命令；修复后记录 run URL/status 和验证输出。

不得用重跑掩盖确定性失败，不得在未确认根因时宣称修复。
