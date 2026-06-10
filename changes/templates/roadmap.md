# Complex Roadmap：{变更名}

> **状态**：[ ] 草稿 / [ ] 已确认 / [ ] 实施中 / [ ] 已完成
> **创建时间**：{YYYY-MM-DD}
> **确认时间**：{YYYY-MM-DD HH:mm 或"未确认"}
> **确认人**：{用户/姓名}

---

## 1. 总目标

{描述整个 Complex 变更最终要达成的业务/技术目标}

## 2. 子变更拆分

| ID | 子变更 | Session scope | 依赖 | Upstream summary | 是否可并行 |
|----|--------|---------------|------|------------------|------------|
| S1 | {子变更A} | spec-S1/tasks-S1/test-spec-S1/log | — | — | 是/否 |
| S2 | {子变更B} | spec-S2/tasks-S2/test-spec-S2/log + S1 log.summary | S1 | S1 key decisions/contracts | 是/否 |

## 3. Session isolation rules

Each Standard sub-project is an independent session.

When starting sub-project `Sn`:
- Load this sub-project only: `spec-Sn.md`, `tasks-Sn.md`, `test-spec-Sn.md`, `log.md`
- Load this `roadmap.md` for dependency context
- Load only upstream `log.summary.md` files declared in the table above
- Do NOT load any other sub-project's full spec/tasks/log/knowledge
- Pass cross-project context through API contracts, key decisions, and upstream summaries, not raw process logs

Before starting a downstream sub-project:
- [ ] Owner reviewed the upstream `log.summary.md`
- [ ] External contracts are complete enough for downstream implementation
- [ ] Downstream risks and rollback notes are explicit
- [ ] Missing summary details are resolved before loading it as context

## 4. 集成顺序

1. {第一步}
2. {第二步}
3. {最终集成与总体验收}

## 5. 总体验收

- [ ] {跨子变更验收条件}
- [ ] {回归测试/联调/上线前检查}

## 6. 跨子变更风险

| 风险 | 影响 | 缓解措施 | 回滚方案 |
|------|------|----------|----------|
| {风险} | {影响} | {措施} | {回滚} |

## 7. log.summary.md format

Each sub-project `/finish` should generate a `log.summary.md` of no more than 30 lines:
- Include key decisions
- Include external API/schema/event/interface contracts
- Include known risks that affect downstream work
- Include verification snapshot when downstream work depends on it
- Exclude implementation details, failed attempts, and process notes

## 8. 监控与归档

- 监控指标：{日志/指标/告警}
- 知识沉淀方向：{预计 archive 时沉淀哪些主题}
