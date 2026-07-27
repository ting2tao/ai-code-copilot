# Workflow Module: init / sync / upgrade

## Purpose

初始化或同步业务项目的 `.ai_code_copilot/` 上下文。项目主权文件不得被框架升级静默覆盖。

## Required context

- `<COPILOT_HOME>/scripts/init_project.sh`
- `packs/*/pack.json` 和命中的 pack
- 项目构建描述文件
- 现有 `.ai_code_copilot/.copilot-state.json` 与 `config.json`

## Commands

```text
init:              bash <COPILOT_HOME>/scripts/init_project.sh --project <project>
sync:              bash <COPILOT_HOME>/scripts/init_project.sh --project <project> --sync
upgrade preview:   bash <COPILOT_HOME>/scripts/init_project.sh --project <project> --upgrade --dry-run
upgrade:           bash <COPILOT_HOME>/scripts/init_project.sh --project <project> --upgrade
```

## Contract

- 自动识别 Java/Go/Python/Frontend pack 和 monorepo 模块。
- `project-context.md`、`domain-rules.md`、现有 `config.json` 是 project-owned，保留原字节。
- 框架托管 core rules、命中 pack rules、templates 和 state 直接覆盖；项目主权资产保持不动。
- dry-run 不写文件。
- 完成后运行 `<COPILOT_HOME>/scripts/check_framework.sh`，并报告命中 pack、变更和候选文件。
