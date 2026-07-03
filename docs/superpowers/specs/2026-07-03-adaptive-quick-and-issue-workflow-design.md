# Adaptive Quick and Issue Workflow Design

> Status: approved design
> Date: 2026-07-03
> Scope: ai-code-copilot workflow rules, templates, documentation, and framework checks
> Work Issue: https://github.com/ting2tao/ai-code-copilot/issues/30
> Parent Issue: none

## 1. Context

The current three-level workflow treats every Quick change as a tracked change with `quick-card.md`, `log.md`, and `summary.md`. That preserves evidence, but it makes a one- or two-file low-risk edit carry nearly the same record-keeping cost as a normal Quick change.

Issue handling is also split across lifecycle stages. `/apply` prohibits ticketless development, while automatic Issue creation is mainly described under `/finish`. The framework records only one related Issue, so it cannot reliably distinguish the parent requirement from the Issue that a PR should close.

This design keeps the existing Quick / Standard / Complex levels, makes Quick record keeping adaptive, and moves work-Issue creation to the point immediately after a Quick Card or Spec is confirmed.

## 2. Decisions

1. Keep three complexity levels. Do not add a Micro level.
2. Split Quick internally into `compact` and `full` record modes using deterministic eligibility rules.
3. A compact Quick uses `quick-card.md` as its requirement contract, runtime record, review record, and finish record. It does not create `log.md` or `summary.md`.
4. Ask for or detect a parent Issue while understanding the requirement. Read the parent requirement before drafting the Quick Card or Spec.
5. Create a work Issue automatically after the user confirms the Quick Card or Spec. Issue creation is mandatory behavior, not project configuration.
6. When a parent Issue exists, attach the work Issue as a GitHub sub-issue. Otherwise, the work Issue is standalone.
7. A PR closes only the work Issue. It references, but never automatically closes, the parent Issue.
8. Commit messages must use `type(scope): description`.
9. Branch names must use `type/scope`.
10. PR automation remains independently controlled by the existing `finishMode`; Issue creation does not.

## 3. Alternatives Considered

### 3.1 Add a Micro complexity level

This makes the smallest path explicit, but increases the public workflow vocabulary, templates, routing rules, and documentation burden. It also creates a fuzzy boundary between Micro and Quick.

### 3.2 Adaptive Quick records — selected

This preserves the current public complexity model. A deterministic classifier selects a compact or full evidence record, and runtime promotion prevents a deceptively small change from bypassing stronger controls.

### 3.3 Replace change documents with a universal state machine

A unified machine-readable record could support more automation, but it would require a broad migration and would make a prompt-and-template framework unnecessarily runtime-heavy.

## 4. Adaptive Quick Model

### 4.1 Compact eligibility

A Quick change is `compact` only when all conditions are true:

- The predicted change touches no more than two files.
- It has one purpose and is expected to produce one commit.
- It does not change public APIs, database schemas, dependencies, CI workflows, deployment behavior, or generated artifacts.
- It does not involve money, permissions, authentication, security controls, sensitive data, state machines, or cross-module business rules.
- It has at least one executable validation command and a direct rollback path.
- It does not require a full test strategy or multiple independent review units.

If classification is uncertain, use full Quick. Standard and Complex classification rules remain unchanged.

### 4.2 Runtime promotion

A compact Quick is promoted to full Quick before continuing when any of the following occurs:

- More than two files become necessary.
- A second independent purpose or commit appears.
- A risk excluded by compact eligibility is discovered.
- Reverse Sync materially changes the confirmed scope.
- Review finds an Important or Critical issue requiring a correction cycle.
- The process produces knowledge or unresolved risk that needs a durable log.

Promotion creates `log.md` and `summary.md`, copies existing execution evidence from `quick-card.md`, updates `recordMode` to `full`, and asks the user to confirm the expanded scope when the confirmation hash changes.

### 4.3 Compact Quick Card

The compact template contains these sections:

- Metadata: status, `recordMode`, confirmation details, and confirmation hash.
- Requirement: goal, files, non-goals, acceptance, risk, rollback, Agent Harness, and Goal Contract.
- GitHub context: `parentIssue`, `workIssue`, relationship, close target, and branch.
- Execution record: validation command, exit code, output summary, and Loop Evidence.
- Commit record: hash and exact message.
- Review record: lightweight compliance, code quality, and GitHub readiness conclusions.
- Finish record: PR URL, base, remote, closing/reference statements, and final validation.

For SessionStart and command routing, the compact Quick Card's metadata header acts as the change summary. Commands must not require a separate `summary.md` when `recordMode: compact`.

## 5. Requirement and Issue Lifecycle

### 5.1 Requirement context resolution

At the start of `/brainstorm` or `/propose`, the framework asks once whether the request belongs to a parent Issue unless a parent is already present in the user input or active change context.

When a parent Issue exists, the framework reads its title, body, acceptance checklist, relationship metadata, and decision-bearing comments before drafting the requirement contract. It summarizes:

- Why the parent requirement exists.
- The overall goal and acceptance conditions.
- The boundary assigned to this change.
- Existing sub-issues or completed work that constrain the change.
- Open decisions or contradictions that require user clarification.

An unreadable or contradictory parent Issue blocks automatic work-Issue creation. The framework must not invent missing parent context.

### 5.2 Confirmation and automatic creation

Before confirmation, the Quick Card or Spec records `parentIssue` and leaves `workIssue` empty. No GitHub mutation occurs.

Immediately after confirmation:

1. Recheck the confirmation hash.
2. If `workIssue` already exists, reuse it and do not create another Issue.
3. Build the Issue title and body from the confirmed contract.
4. Create the work Issue automatically.
5. If `parentIssue` exists, establish the native sub-issue relationship.
6. Write the work Issue URL/number and relationship status back to the confirmed document.
7. Derive the primary `type` and `scope`, then create or validate the `type/scope` branch.
8. Only after the Issue and branch preflight succeeds may `/apply` begin.

The work-Issue body includes background, goal, in-scope work, out-of-scope work, acceptance criteria, risk/rollback, parent reference when present, and a link or path to the local change contract when meaningful.

### 5.3 Data contract

All Quick Cards and Specs use the following logical fields:

```yaml
parentIssue: "#123 | URL | none"
workIssue: "#456 | URL | pending"
issueRelationship: "sub-issue | standalone | pending"
closeTarget: "workIssue"
branch: "type/scope"
```

`workIssue: pending` is valid only between contract confirmation and successful Issue creation. `/apply`, `/review`, and `/finish` reject a pending work Issue.

### 5.4 Idempotency and partial failure

- Existing `workIssue` data is authoritative and prevents duplicate creation.
- If Issue creation succeeds but sub-issue linking fails, persist the created Issue immediately, set `issueRelationship: pending`, and retry the relationship operation. Never create a replacement Issue.
- If the GitHub account is unauthenticated or the repository is unreachable, keep the confirmed contract intact and stop before coding.
- If a recorded work Issue is closed, missing, or belongs to another repository, stop and require repair instead of silently creating a new Issue.

## 6. Git Contract

### 6.1 Allowed types

The allowed types are:

```text
feat fix docs refactor test chore perf ci build
```

### 6.2 Scope

`scope` identifies the module or capability, uses lowercase kebab-case, and must be stable across the branch and its primary commits. Issue numbers and bracketed prefixes are not scopes.

### 6.3 Branch validation

Branch names must match:

```regex
^(feat|fix|docs|refactor|test|chore|perf|ci|build)/[a-z0-9]+(?:-[a-z0-9]+)*$
```

Example:

```text
feat/issue-workflow
```

If the branch already exists, the framework stops and asks whether to reuse it or resolve the collision. It must not append timestamps or silently change the naming contract.

### 6.4 Commit validation

Commit subjects must match:

```regex
^(feat|fix|docs|refactor|test|chore|perf|ci|build)\([a-z0-9]+(?:-[a-z0-9]+)*\): .+$
```

Example:

```text
feat(issue-workflow): 支持确认后自动创建 sub-issue
```

The branch type represents the primary change. Follow-up commits may use another valid type, such as `fix(issue-workflow): ...`, while retaining the same capability scope.

## 7. Review and Finish

Quick compact review reads the confirmed requirement and all evidence from `quick-card.md`. It performs the existing lightweight Quick compliance review plus full Code Quality review, then appends its conclusions to the same file.

`/finish` resolves Issue behavior exclusively from the recorded data contract:

- Always include `Closes #<workIssue>`.
- Include `Refs #<parentIssue>` only when a parent exists.
- Never emit a closing keyword for the parent Issue.
- Reject a missing or pending relationship instead of guessing.
- Preserve existing `finishMode=ask | auto-pr | manual` behavior for validation, push, and PR creation.

The obsolete `githubWorkflow.issueWhenMissing` configuration is no longer consulted. New project configuration templates omit it. Existing project-owned config files may retain the field after sync; the framework ignores it and emits a migration note rather than rewriting project-owned configuration.

## 8. Error Handling

- Parent context unavailable: stop before contract confirmation or Issue creation and explain what could not be read.
- Work Issue creation unavailable: preserve the confirmed document and stop before `/apply`.
- Sub-issue link unavailable: retain the created work Issue, mark the link pending, and block `/apply` until repaired.
- Wrong branch format: stop before edits or commits and provide the expected `type/scope` name.
- Wrong commit format: reject the commit subject before commit creation.
- Compact eligibility violated: promote to full Quick before further implementation.
- Dirty worktree: preserve unrelated changes and stop when isolation cannot be guaranteed.

## 9. Framework Surfaces

Implementation must keep these surfaces consistent:

- `agents/copilot-prompt.md`: classification, context resolution, confirmation-time Issue creation, branch creation, apply/review/finish gates, compact promotion, and archive behavior.
- `rules/commit-convention.md`: mandatory branch and commit formats plus Issue relationship semantics.
- `rules/github-metrics.md`: separate parent and work Issue signals and closing behavior.
- `agents/spec-reviewer.md` and `agents/code-quality-reviewer.md`: compact record support and Git contract checks.
- `changes/templates/quick-card.md`: record mode, Issue contract, execution/review/finish sections.
- `changes/templates/spec.md`, `tasks.md`, `summary.md`, and `log.md`: parent/work Issue terminology and branch contract.
- `config/project-config.json`: remove the Issue-creation option while retaining PR finish controls.
- `scripts/init_project.sh`: distribute the updated config and templates without overwriting project-owned config.
- `scripts/check_framework.sh` and fixtures: assert the new workflow contracts and migration behavior.
- `README.md`, `README-CN.md`, `AGENTS.md`, and workflow overview documentation: explain the same user-facing behavior in both languages where applicable.

## 10. Verification Strategy

Framework checks must cover:

1. Deterministic compact/full classification examples, including every disqualifying risk category.
2. Compact template completeness without `log.md` or `summary.md` dependencies.
3. Promotion from compact to full without losing confirmation or verification evidence.
4. No Issue mutation before confirmation and automatic work-Issue creation after confirmation.
5. Repeated execution reuses `workIssue` and cannot create duplicates.
6. Parent Issue produces sub-issue semantics; no parent produces standalone semantics.
7. PR text closes the work Issue and only references the parent Issue.
8. Branch and commit regexes accept valid examples and reject malformed examples.
9. Default config no longer contains `issueWhenMissing`, while stale project-owned configuration remains preserved and ignored.
10. English and Chinese README descriptions remain behaviorally aligned.

Primary repository validation remains:

```text
bash scripts/check_framework.sh
git diff --check
```

Network-mutating GitHub behavior should be verified through isolated command-contract tests or a disposable test Issue during implementation closeout, not against unrelated production Issues.

## 11. YAGNI Boundaries

This change does not add configurable Issue creation, automatic parent-Issue closure, automatic PR merge, label management, milestones, Project board automation, or a new runtime service. It does not replace Markdown change contracts with a database or general workflow engine.

## 12. Acceptance Criteria

- A qualifying two-file low-risk Quick change completes with one `quick-card.md` and no standalone log or summary.
- A Quick change that violates compact rules uses or is promoted to the full Quick record set.
- Confirming a Quick Card or Spec automatically creates exactly one work Issue before coding.
- A supplied parent Issue is read before contract drafting, and the work Issue is linked as its sub-issue.
- A PR closes only the work Issue and references the parent when present.
- Branches and commits are blocked unless they follow `type/scope` and `type(scope): description`.
- Existing PR automation modes continue to work independently of mandatory Issue creation.
- Framework checks and synchronized English/Chinese documentation describe and enforce the behavior.
