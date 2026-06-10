---
description: 知识库索引模板 — /init 时复制到项目，/archive 时更新
alwaysApply: false
---

# Knowledge Index

> Project-specific knowledge discovered by `/archive`.
> Read this index first; load only the relevant knowledge files selected by the current command.

| ID | Summary | Tags | Scope | Applies-To | Risk | Last-Verified | File |
|----|---------|------|-------|------------|------|---------------|------|
| K000 | 示例：删除本行后开始沉淀知识 | example | example | propose | low | 1970-01-01 | example.md |

## Field Rules

- `ID`: stable `K###` identifier; never reuse an ID after deletion.
- `Summary`: one short sentence for quick relevance judgment.
- `Tags`: comma-separated keywords used for retrieval.
- `Scope`: module, package, path, or domain boundary.
- `Applies-To`: command phases where this knowledge is useful, such as `propose`, `apply`, `review`, or `fix-ci`.
- `Risk`: `low`, `medium`, or `high`; high-risk knowledge is preferred when relevance ties.
- `Last-Verified`: `YYYY-MM-DD`; entries older than 180 days are candidates and need human judgment.
- `File`: path relative to `knowledge/`.
