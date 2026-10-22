<!-- artifact
artifactVersion: 1
artifactId: workflow-codex-alignment:tasks
artifactType: tasks
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: workflow-codex-alignment:spec
upstreamHash: sha256:ee105371c7d521490630c040836f468cccab4b690a89343190a07e35a6dff72c
-->

# Tasks

- T1: Add independent production-only and native/authorized-local behavior regressions, then fix policy. Files: config/workflow-policy.json, evals/cases/core.json, tests/test_workflow_alignment.py.
- T2: Add Codex patch adapter and isolated subprocess regressions. Files: scripts/check_guardrails.py, hooks/pre-tool-codex, config/guardrail-policy.json, tests/test_workflow_alignment.py.
- T3: Add shared platform registration and installer round-trip tests, wire all three installers. Files: scripts/register_hooks.py, install.sh, install-wsl.sh, install.ps1, scripts/test_install_overwrite.sh.
- T4: Align bilingual docs/current reference/version and run all checks; self-review Spec Compliance then Code Quality; commit and PR to main closing #39. Files: README.md, README-CN.md, AGENTS.md, agents/copilot-prompt.md, rules/security.md, scripts/check_framework.sh, VERSION, this record set.

All tests use disposable state. No unrelated edits included. Exact commands/results and commit IDs are recorded in log.md.

Implementation T1-T4 and local checks complete; protected-path owner approval received; commit/publish next. Detailed verification and limitations: log.md.
