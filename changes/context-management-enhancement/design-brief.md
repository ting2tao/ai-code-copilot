# Design Brief：context-management-enhancement

> **复杂度预判**：[ ] Quick / [x] Standard / [ ] Complex
> **来源**：`/Users/tsnowy/Downloads/文档-其他/context-management-tech-spec.md`

## 背景

当前框架已经具备 Spec、Review、Archive 和 Harness 规则，但上下文加载策略还偏粗：主提示词要求启动时读取所有 rules，knowledge index 仍是自由文本，log.md 缺少压缩边界，Complex 子项目隔离也没有模板级约束。

## 目标

把上下文管理增强方案落到框架核心文件中，形成可安装、可同步、可自检的机制：
- SessionStart 只注入 L0 安全与摘要信息
- 命令阶段按需加载 rules/packs/knowledge/change docs
- knowledge/index.md 改为可检索表格 schema
- log.md 支持安全压缩，不丢审计证据
- Complex roadmap 明确独立会话和上游 summary
- project-context 过期时软提醒用户执行 sync

## 方案

采用 Claude spec 中的四层边界：
- hook 负责唤醒、安全、软提醒和 active change 摘要
- prompt 负责命令阶段加载策略
- templates 负责长期结构约束
- state 负责机器维护事实

## 非目标

- 不实现真实命令级 hook 路由
- 不改变 hard gate
- 不删除 audit trail
- 不自动覆盖项目主权文件

