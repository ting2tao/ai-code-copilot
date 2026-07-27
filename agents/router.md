# ai-code-copilot Router

你已根据显式生命周期意图或 material risk 激活 ai-code-copilot。先读取 `<COPILOT_HOME>/config/workflow-policy.json`，再只加载当前意图和当前持久化档位需要的模块；不得读取无关 workflow module，也不得回退加载 legacy 单体提示词。

`<COPILOT_HOME>` 按以下顺序定位：`AI_CODE_COPILOT_HOME`、当前 skill 父目录、Codex home、Claude home。项目级 `.ai_code_copilot/` 规则和配置优先于全局默认。

## Always-on rules

- 保留用户无关和未提交改动，不覆盖、不顺带提交。
- 不泄露密钥、凭据或敏感信息。
- 破坏性、外部写入、资金、权限、状态流转、安全或生产风险操作必须获得明确授权。
- 宣布完成前必须运行新鲜验证并展示实际证据。
- 资金、权限、状态机、安全或生产风险必须进入 Full SDD，并等待人工确认。

## Intent routing

| 已激活意图 | 必须加载 |
|---|---|
| init / sync / upgrade | `agents/workflows/init.md` |
| 需要持久化的低风险小变更 | `agents/workflows/compact.md` |
| brainstorm / propose / apply 或 material risk | `agents/workflows/full.md` |
| fix-ci / repeated investigation | `agents/workflows/debug.md` + 当前档位模块 |
| review | `agents/workflows/review.md` |
| test | `agents/workflows/test.md` |
| finish / commit / publish / PR | `agents/workflows/finish.md` + 当前档位模块 |
| archive | `agents/workflows/archive.md` |

可用流程：init / brainstorm / propose / apply / fix / fix-ci / review / finish / test / archive

普通低风险实现、调试、重构、测试、文档、讨论和只读分析应在 skill 激活前由模型原生处理。进入本 router 后不得为了“更轻”退回 Native；只能完成当前激活工作或明确停止。

## Tier routing

- Compact SDD：使用 `quick-card.md`，`recordMode: compact`。
- Full SDD：使用完整 Spec、tasks、test-spec、log、summary；Complex 再使用 roadmap。

命中 policy 的 full risk、超过 Compact 边界、出现多个交付/审查单元或 residual risk 时进入 Full。Compact 只能单向升级到 Full，活动变更不得自动降级。

## Native escalation

- Native 工作需要跨会话、提交发布、审计或持久决策时：停止新增编辑，创建 Compact，并记录 `promotedFrom: native`、当前 diff 和实际验证证据。
- Native 工作发现 material risk 时：停止新增编辑，创建 Full，并在继续前取得 material confirmation。

## Context loading

1. 读取当前任务直接相关的项目规则、代码和构建配置。
2. 持久档位只读取目标 active change 的当前记录源。
3. 知识加载先读 `knowledge/index.md`，再按相关性读取最多 5 条。
4. SessionStart metadata 只是提示；合同文件和实时仓库状态才是事实来源。
5. pack rules 只按命中技术栈和目标文件加载。

## Missing runtime

若 policy、router 或选中的 workflow module 缺失，停止执行，明确报告缺失路径并建议执行 framework upgrade 或 `init --sync`。不得加载单体 legacy prompt，也不得静默放宽门禁。
