# Model-First Activation and Semantic Versioning Spec

status: confirmed
design: docs/superpowers/specs/2026-07-27-model-first-versioning-design.md

## Goal Contract

- Goal: Make low-risk work model-native and publish versioned full-replacement framework updates.
- Done Signal: Acceptance criteria 1-10 in the approved design pass with fresh command output.
- Guardrails: Preserve project-owned assets; require framework activation and human confirmation for material risk; do not preserve global installation edits.
- Fallback: Fail before replacement when the source is invalid; after replacement failure require a clean reinstall.
- Memory: Record only stable version, activation, ownership, and verification lessons at finish/archive.

## Scope

Implement sections 6-13 of the approved design:

- Model-first native execution and automatic risk/lifecycle activation.
- Compact/Full routing after activation.
- Root `VERSION` and semantic release checks.
- Full-replacement installers for macOS/Linux, PowerShell, and WSL.
- Versioned direct overwrite for framework-managed project files.
- Executable policy, install, sync, syntax, and documentation checks.

## Non-goals

- Compatibility migration or automatic rollback.
- Online update checks or automatic updates.
- Release service or changelog automation.
- Replacement of project-owned config, context, domain rules, knowledge, active changes, or archives.
- Changes to historical approved design documents or archives.

## Acceptance

1. A bounded low-risk coding request can remain model-native.
2. Explicit workflow requests and material risk automatically activate ai-code-copilot.
3. Activation loads no unrelated workflow modules.
4. Root `VERSION` is `0.1.0` and drives installers and project sync.
5. All installers replace the managed installation and report the semantic version.
6. Global update preserves no installation-local edits and offers no migration or rollback.
7. Explicit project sync overwrites managed content and preserves named project assets.
8. Project state records `frameworkVersion` and `frameworkCommit`.
9. README, README-CN, AGENTS, and architecture docs agree.
10. Policy, version, installer, sync, syntax, and diff checks pass with fresh evidence.
