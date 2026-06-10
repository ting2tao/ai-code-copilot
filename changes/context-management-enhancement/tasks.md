# 任务列表：context-management-enhancement

> **关联 Spec**：`spec.md`
> **关联 Test Spec**：`test-spec.md`

## Preflight

- [x] `git status --short` 已检查
- [x] 当前分支不是 master/main
- [x] 上游 spec 已读取：`/Users/tsnowy/Downloads/文档-其他/context-management-tech-spec.md`

## 进度概览

| Task | 描述 | 状态 | commit hash |
|------|------|------|-------------|
| T1 | L0 hook + context freshness state | ✅ | |
| T2 | command-level prompt policy + knowledge/log/Complex rules | ✅ | |
| T3 | templates and knowledge index schema | ✅ | |
| T4 | framework self-check and README sync | ✅ | |
| T5 | review feedback hardening | ✅ | |
| T6 | archive-independent runtime state | ✅ | |

## 完成证据

```text
bash scripts/check_framework.sh
ai-code-copilot framework check passed

bash -n hooks/session-start
exit code: 0

bash -n scripts/init_project.sh
exit code: 0

hooks/session-start | python3 -m json.tool
exit code: 0

review feedback hardening:
- summary.md validation fallback added to session-start
- logCompression thresholds moved to config defaults
- small knowledge indexes use direct loading path
- roadmap requires owner review of upstream log.summary.md
- install scripts warn when Python is missing

archive-independent runtime state:
- /finish now owns summary.md status: finished
- SessionStart ignores finished changes
- /finish generates Complex log.summary.md
- /finish can capture Knowledge candidates before archive
```
