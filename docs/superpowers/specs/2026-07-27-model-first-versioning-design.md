# Model-First Activation and Semantic Versioning Design

> Status: approved
> Date: 2026-07-27
> Scope: skill activation, SessionStart routing hints, workflow policy, semantic versioning, installers, project sync state, documentation, and framework checks
> Parent Issue: none
> Work Issue: none
> Issue Relationship: standalone local design; Issue handling is deferred until publish policy requires it
> Branch: `feat/model-first-versioning`
> Confirmed By: user
> Confirmed At: 2026-07-27 +0800

## 1. Context

The current progressive SDD runtime reduced prompt weight by replacing the mandatory monolithic prompt with `agents/router.md` and focused workflow modules. Its skill description still treats most development requests—implementation, debugging, refactoring, testing, and review—as unconditional activation signals. As a result, a strong coding model still enters the framework before deciding whether the framework adds value.

The installation and project-sync paths also identify the framework by a Git short commit. The repository has historical tags through `v0.0.3`, but no version file is used by installers or `.copilot-state.json`. Users can see that two commits differ without knowing the framework release they installed.

This design makes the model the default reasoning and execution engine. The framework becomes an adaptive control plane for risk, persistence, audit, and delivery. It also introduces a strict semantic version as the release identity and replaces installed framework files as one managed unit during updates.

## 2. Confirmed Decisions

The user confirmed the following:

1. Use a complete semantic-version solution rather than a display-only version.
2. Let the model decide whether `ai-code-copilot` is needed before activating it.
3. Allow automatic activation when the model detects risk, persistence, audit, or delivery needs.
4. Do not activate the skill merely because a request asks to implement, debug, refactor, or test code.
5. Update installed framework files by direct full replacement.
6. Do not add compatibility migration or automatic rollback.
7. Preserve project-owned assets while replacing framework-managed project files during explicit sync.

## 3. Goals

1. Keep ordinary low-risk development on the model-native path without loading ai-code-copilot workflow instructions.
2. Automatically activate the framework when semantic risk or lifecycle needs justify its cost.
3. Keep activation rules small, inspectable, and regression-tested.
4. Establish root `VERSION` as the single release-version source.
5. Make all installers perform the same full-replacement update and report the installed semantic version.
6. Record both framework version and commit in initialized business projects.
7. Detect version, activation-policy, installer, project-state, and documentation drift through executable checks.

## 4. Non-goals

- No online latest-version check or background update prompt.
- No automatic update without an explicit install/update command.
- No compatibility migration for old installation layouts, workflow policy, project state, or project config.
- No three-way merge, `.new` candidate, or preservation of local modifications inside the global framework installation.
- No automatic rollback or retained previous release.
- No changelog generator or release-service dependency.
- No replacement of project-owned context, domain rules, configuration, knowledge, active changes, or archives.
- No deterministic keyword-only classifier that attempts to replace model judgment.
- No measurement or exposure of hidden model reasoning.

## 5. Alternatives

### 5.1 Always load a smaller router

Keep the current broad skill discovery rules and optimize only router size. This is safer than a monolithic prompt but still pays a fixed activation cost for every coding request and does not satisfy the model-first goal.

### 5.2 Explicit invocation only

Activate only when the user names commands such as `init`, `review`, `finish`, or `archive`. This minimizes overhead but prevents the model from escalating when a request contains hidden production, security, permission, or data risk.

### 5.3 Model-first adaptive activation — selected

The platform model performs an initial semantic triage using a compact skill description and SessionStart policy. Low-risk work remains native. Explicit lifecycle intent and detected risk automatically activate the framework, which then loads only the required module.

## 6. Activation Architecture

### 6.1 Native path is the default

The following work normally remains model-native:

- Explanation, discussion, and read-only repository analysis.
- A clear local edit with bounded scope and direct executable verification.
- An obvious local bug whose root cause and regression test can be established without durable coordination.
- Isolated documentation or refactoring work without public-contract, deployment, security, or state implications.

The native path may inspect files, edit code, and run verification. It does not load `agents/router.md`, create Quick Cards or Specs, or invoke Issue and archive workflows. It must still preserve unrelated user changes, respect tool authorization boundaries, and show fresh evidence before claiming completion.

### 6.2 Automatic activation

The model must activate ai-code-copilot when it detects any of these conditions:

- Security, authentication, authorization, permission, sensitive-data, money, or destructive-operation risk.
- Production, deployment, CI, dependency, database, schema, generated-artifact, public-contract, or state-machine impact.
- Cross-module business rules or material ambiguity whose impact cannot be bounded safely.
- Work that must survive a session boundary or preserve durable decisions and evidence.
- Auditable review, commit, publish, PR, finish, or archive lifecycle requirements.
- Repeated investigation or missing verification that makes the native path unreliable.
- Explicit user intent for `init`, `brainstorm`, `propose`, `apply`, `fix-ci`, `review`, `finish`, `test`, or `archive`.

The user may request a direct native path for low-risk work. That preference cannot bypass confirmation required for destructive actions, external writes, security, permission, money, state-transition, or production risk.

### 6.3 Runtime components

`skill/SKILL.md` becomes a discovery and activation contract rather than a generic coding trigger. Its description names explicit workflow intents and semantic escalation signals, while removing unconditional phrases such as any request to implement, debug, refactor, or test.

`hooks/session-start` injects only a compact model-first policy:

- Native by default for bounded low-risk work.
- Activate on explicit lifecycle intent or material risk.
- Never bypass safety confirmations.

It does not load the router, policy JSON, workflow modules, or active change documents merely to make this decision.

`config/workflow-policy.json` records the canonical activation categories and the behavior after activation. The skill description, SessionStart message, router, documentation, and checks must agree with that policy.

Once activated, `agents/router.md` continues selective loading. The change removes the framework-owned Inline tier as the mandatory path for ordinary work; low-risk work happens before framework activation. Compact and Full remain available for persisted and high-risk work.

## 7. Semantic Version Contract

The repository root contains a text file named `VERSION`.

- The file contains exactly one SemVer value plus a trailing newline.
- The value does not include a `v` prefix.
- The first release of this design is `0.1.0`, advancing from the latest historical tag `v0.0.3`.
- Release tags use `v${VERSION}`, for example `v0.1.0`.
- Git commit remains diagnostic build identity, not the framework version.

Framework behavior, installation logic, runtime policy, managed templates, or project-sync behavior must not change in a release branch without changing `VERSION` relative to its merge base. Documentation-only changes that do not change framework behavior do not require a version bump.

## 8. Full-Replacement Update

All three installer surfaces—macOS/Linux, PowerShell, and WSL—use the same logical update:

1. Resolve a complete source tree from the invoking local checkout or the configured repository.
2. Require a valid `VERSION` and required framework structure in that source tree.
3. Stop before modifying the installation if validation fails.
4. Replace the global framework installation as a managed unit.
5. Discard local changes and files that are absent from the new framework source.
6. Re-register the skill link or Junction and SessionStart hook.
7. Run the framework self-check against the installed tree.
8. Print the installed semantic version and Git commit when a commit is available.

There is no per-file merge, compatibility branch, legacy commit-as-version fallback, retained previous release, or automatic rollback. If replacement or post-install validation fails, the installer reports a hard failure and instructs the user to rerun a clean installation.

The implementation may stage and validate the new source before replacement to avoid starting with a known-invalid package. Staging is not a rollback mechanism; the previous installed release is not retained as a supported recovery path.

## 9. Project Sync Ownership

Global installation does not automatically modify business projects. An explicit `init --sync` or `--upgrade` operation applies the installed framework version.

Framework-managed project files are directly overwritten:

- Managed templates under `.ai_code_copilot/changes/templates/`.
- Generic core rules other than the project-owned exceptions below.
- Matched pack rules.
- Other generated framework control files.

Project-owned assets remain untouched:

- `.ai_code_copilot/config.json`.
- `.ai_code_copilot/rules/project-context.md`.
- `.ai_code_copilot/rules/domain-rules.md`.
- `.ai_code_copilot/knowledge/`.
- Active and archived change records.

The sync operation writes a fresh `.copilot-state.json` containing at least:

```json
{
  "frameworkVersion": "0.1.0",
  "frameworkCommit": "<short-commit>",
  "lastSyncedAt": "<timestamp>"
}
```

No old state or config migration is performed. Invalid project-owned configuration is reported rather than rewritten.

## 10. Data Flow

### 10.1 Request execution

```text
user request
  -> platform model semantic triage
       -> bounded low-risk: native inspect/edit/verify
       -> explicit lifecycle or material risk: activate ai-code-copilot
            -> router selects required workflow module
            -> Compact or Full record only when persistence/risk requires it
```

### 10.2 Framework update

```text
install/update command
  -> resolve complete source
  -> validate VERSION + required structure
  -> replace managed installation
  -> re-register skill + hook
  -> run installed self-check
  -> report VERSION + optional commit
```

### 10.3 Business-project sync

```text
explicit init --sync
  -> read installed VERSION
  -> detect packs
  -> overwrite framework-managed project files
  -> preserve project-owned assets
  -> write frameworkVersion + frameworkCommit
  -> report sync evidence
```

## 11. Failure Behavior

- Missing or invalid source `VERSION`: fail before replacement or sync.
- Missing required framework files: fail before replacement.
- Replacement failure: stop with a hard error; do not claim the prior installation is usable.
- Skill/Junction or hook registration failure: fail installation.
- Installed self-check failure: fail installation and instruct a clean rerun.
- Invalid project-owned config: fail project sync without rewriting it.
- Activation uncertainty with potentially material impact: activate the framework and choose the safer persisted tier.
- Native work that grows into risk or lifecycle scope: stop the native path and activate before further edits.

## 12. Verification Strategy

### 12.1 Activation contract

Add deterministic checks for policy consistency and scenario fixtures:

- Explanation, read-only analysis, bounded local edit, and simple verified bugfix are native-path examples.
- Security, permission, money, production, database, deployment, public-contract, publish, and archive scenarios are activation examples.
- Broad generic coding phrases must not reappear as unconditional discovery triggers.
- Skill description, SessionStart policy, router, workflow policy, AGENTS, and bilingual README content must retain the same boundary.

These checks validate the published contract, not hidden model reasoning. Scenario-level manual evaluation remains necessary because activation is semantic.

### 12.2 Version and installation

- Validate strict SemVer syntax and the expected one-line `VERSION` format.
- Require installer references to the root version source.
- Exercise macOS/Linux and WSL replacement against temporary installation directories.
- Validate PowerShell syntax and static contract markers; run a Windows smoke test when a Windows environment is available.
- Confirm replacement removes an obsolete framework-managed file.
- Confirm post-install output reports `0.1.0`.
- Confirm local modifications inside the installation are discarded.

### 12.3 Project sync

- Run existing Java, Go, Python, frontend, and monorepo fixtures.
- Assert framework-managed rules and templates are overwritten.
- Assert project-owned configuration, context, domain rules, knowledge, and change records are preserved.
- Assert `.copilot-state.json` contains `frameworkVersion` and `frameworkCommit`.
- Assert an invalid or missing installed version fails clearly.

### 12.4 Final gates

Run:

```bash
bash scripts/check_framework.sh
python3 scripts/check_progressive_sdd.py
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh install.sh install-wsl.sh
git diff --check
```

PowerShell validation is required when `pwsh` or a Windows runner is available; otherwise the limitation must be stated explicitly.

## 13. Expected Change Surface

The implementation is expected to touch:

- `VERSION`.
- `skill/SKILL.md`.
- `hooks/session-start`.
- `agents/router.md` and relevant workflow modules.
- `config/workflow-policy.json`.
- `install.sh`, `install.ps1`, and `install-wsl.sh`.
- `scripts/init_project.sh`.
- `scripts/check_framework.sh` and focused policy/version checks.
- `README.md`, `README-CN.md`, `AGENTS.md`, and architecture documentation.
- Full SDD records and implementation plan for this change.

No unrelated pack coding conventions, historical archives, or business-project artifacts are in scope.

## 14. Risks and Trade-offs

- Semantic activation is model-dependent and cannot be made perfectly deterministic. The design mitigates this with conservative high-risk signals, compact always-visible guidance, and scenario regression checks.
- Narrowing the skill description could under-trigger on ambiguously worded risk. Uncertainty with material impact therefore activates rather than staying native.
- Full replacement destroys installation-local edits. This is intentional: the global installation is managed content.
- No rollback increases the cost of a bad release. Pre-replacement validation and post-install self-check reduce, but do not eliminate, that risk.
- Direct project sync can replace team edits made in framework-managed files. Ownership boundaries must therefore be explicit and documented.
- Manual SemVer bumps can drift from code. The framework check compares behavior changes with the base version and blocks an unchanged version.

## 15. Acceptance Criteria

1. A normal bounded coding request can be handled without activating ai-code-copilot.
2. Explicit workflow commands and material risk automatically activate it.
3. Activation does not preload unrelated workflow modules.
4. Root `VERSION` is `0.1.0` and is the version source used by installers and project sync.
5. All installers replace the managed framework installation and report the semantic version.
6. Global update preserves no installation-local framework modifications and offers no compatibility migration or rollback.
7. Explicit project sync overwrites framework-managed content while preserving the listed project-owned assets.
8. Project state records both framework version and commit.
9. Bilingual documentation and AGENTS describe the same behavior.
10. Framework, activation-policy, version, installer, sync-fixture, syntax, and diff checks pass with fresh evidence.
