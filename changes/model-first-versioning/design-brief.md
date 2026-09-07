# Model-First Versioning Design Brief

status: confirmed
design: docs/superpowers/specs/2026-07-27-model-first-versioning-design.md
confirmed-by: user
confirmed-at: 2026-07-27

## Decision

Use model-first adaptive activation, semantic version `0.1.0`, direct full replacement for the global framework installation, and direct overwrite for framework-managed project files.

## Alternatives rejected

- Always load a micro-router: still charges every coding request.
- Explicit activation only: cannot escalate hidden material risk.
- Compatibility migration and rollback: explicitly excluded by the user.
