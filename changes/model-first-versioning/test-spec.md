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

## Actual Evidence

| Priority | Result | Evidence |
|---|---|---|
| P0 | PASS | Version/activation checks, progressive policy checks, repeated install overwrite (including invalid-source preservation), and the full Java/Go/Python/Frontend/Monorepo fixture matrix exited 0. |
| P1 | PASS | Bash syntax, Python compile, documentation drift, managed/project-owned sync boundaries, invalid-config failure, and `git diff --check origin/main` exited 0. |
| P2 | LIMITED | `pwsh` is unavailable in the current macOS environment; PowerShell received static contract review, while Windows runtime smoke remains for CI or a Windows host. |

Fresh verification:

```text
python3 scripts/check_model_first_versioning.py . &&
python3 scripts/check_progressive_sdd.py . &&
bash scripts/test_install_overwrite.sh &&
bash scripts/check_framework.sh &&
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh scripts/test_install_overwrite.sh install.sh install-wsl.sh &&
python3 -c 'compile both Python checker sources in memory' &&
git diff --check origin/main

exit: 0
```
