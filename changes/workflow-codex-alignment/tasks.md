<!-- artifact
artifactVersion: 1
artifactId: workflow-codex-alignment:tasks
artifactType: tasks
artifactStatus: finished
sourceOfTruth: repository
sourceRef: self
sourceRevision: git:36c926e82c5fa57c86c3d92125d3732679903d3c
upstream: workflow-codex-alignment:spec
upstreamHash: sha256:c8cff41c1b8c2b5b05b36e5bb62b06fbff4acd37474d2d926b1ec9357681e450
-->

# Tasks

- T1: Add independent production-only and native/authorized-local behavior regressions, then fix policy. Files: config/workflow-policy.json, evals/cases/core.json, tests/test_workflow_alignment.py.
- T2: Add Codex patch adapter and isolated subprocess regressions. Files: scripts/check_guardrails.py, hooks/pre-tool-codex, config/guardrail-policy.json, tests/test_workflow_alignment.py.
- T3: Add shared platform registration and installer round-trip tests, wire all three installers. Files: scripts/register_hooks.py, install.sh, install-wsl.sh, install.ps1, scripts/test_install_overwrite.sh.
- T4: Align bilingual docs/current reference/version and run all checks; self-review Spec Compliance then Code Quality; commit and PR to main closing #39. Files: README.md, README-CN.md, AGENTS.md, agents/copilot-prompt.md, rules/security.md, scripts/check_framework.sh, VERSION, this record set.

All tests use disposable state. No unrelated edits included. Exact commands/results and commit IDs are recorded in log.md.

Implementation T1-T4 and local checks complete; protected-path owner approval received; commit/publish and PR #40 complete. Detailed verification and limitations: log.md.

All T1-T4 acceptance complete. GitHub handoff evidence is recorded in log.md Finish record.
