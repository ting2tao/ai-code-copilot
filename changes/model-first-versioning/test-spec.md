# Model-First Versioning Test Spec

## P0

- `VERSION` is strict one-line SemVer.
- Ordinary bounded work remains native; explicit lifecycle and material risk activate.
- Activated work selects Compact or Full without an Inline workflow.
- macOS/Linux installation replaces obsolete and locally modified framework files.
- Project sync overwrites managed rules/templates and preserves config, project context, domain rules, knowledge, active changes, and archives.
- `.copilot-state.json` records `frameworkVersion` and `frameworkCommit`.
- `bash scripts/check_framework.sh` passes.

## P1

- Skill, SessionStart, router, policy, reviewers, templates, AGENTS, and bilingual README wording stay aligned.
- Bash scripts pass `bash -n`.
- `git diff --check origin/main...HEAD` passes.
- Invalid source version and invalid project config fail clearly before mutation.

## P2

- PowerShell parses when `pwsh` is available locally.
- A Windows runtime smoke test is recorded when a Windows runner is available; otherwise the limitation is explicit.

## Required Commands

```text
python3 scripts/check_model_first_versioning.py .
python3 scripts/check_progressive_sdd.py .
bash scripts/test_install_overwrite.sh
bash scripts/check_framework.sh
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh scripts/test_install_overwrite.sh install.sh install-wsl.sh
git diff --check origin/main...HEAD
```
