# Model-First Versioning Log

## Confirmed decisions

- Model-native is the default for bounded low-risk work.
- The model may automatically activate ai-code-copilot for lifecycle or material risk.
- `VERSION` is the release identity; the first release is `0.1.0`.
- Global framework updates replace the full managed tree.
- Project sync overwrites framework-managed files and preserves project-owned assets.
- Compatibility migration and automatic rollback are out of scope.

## Baseline evidence

```text
command: bash scripts/check_framework.sh
exit: 0
summary: progressive-sdd policy and module checks passed; ai-code-copilot framework check passed
```

## Task 2: Semantic version contract

```text
command: bash scripts/check_framework.sh
exit: 1
summary: expected RED — FAIL: missing file: VERSION

command: python3 scripts/check_model_first_versioning.py .
exit: 0
summary: model-first-versioning version 0.1.0 checks passed

command: bash scripts/check_framework.sh
exit: 0
summary: progressive SDD, semantic version, and full framework checks passed
```

## Task 3: Model-first activation

```text
command: python3 scripts/check_model_first_versioning.py .
exit: 1
summary: expected RED — activation.defaultPath must be native

command: python3 scripts/check_model_first_versioning.py . && python3 scripts/check_progressive_sdd.py . && bash hooks/session-start | python3 -m json.tool >/dev/null
exit: 0
summary: model-first activation, Compact/Full routing, and SessionStart JSON checks passed

command: bash scripts/check_framework.sh
exit: 0
summary: full framework gate passed after removing framework-owned Inline
```

## Task 4: Native escalation records

```text
command: python3 scripts/check_progressive_sdd.py .
exit: 1
summary: expected RED — quick-card missing promotedFrom: native

command: python3 scripts/check_progressive_sdd.py . && bash scripts/check_framework.sh
exit: 0
summary: active workflows, reviewers, and templates consistently use Native -> Compact/Full; full framework gate passed
```

## Task 5: Full-replacement installers

```text
command: python3 scripts/check_model_first_versioning.py .
exit: 1
summary: expected RED — install.sh missing validate_source_tree and replace_install_tree

command: bash -n install.sh && bash -n install-wsl.sh && python3 scripts/check_model_first_versioning.py . && bash scripts/test_install_overwrite.sh
exit: 0
summary: installer contract and Bash syntax passed; two local installs removed stale/modified managed files and preserved VERSION, skill link, and one SessionStart hook

command: bash scripts/check_framework.sh
exit: 0
summary: full framework gate passed with install overwrite smoke included

note: PowerShell was checked by static contract only because pwsh is not installed in the current macOS environment.
```
