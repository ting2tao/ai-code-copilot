# Progressive SDD Runtime Design

> Status: approved
> Date: 2026-07-13
> Scope: ai-code-copilot routing, SDD contracts, runtime promotion, GitHub policy, reviewers, templates, documentation, and framework checks
> Parent Issue: none
> Work Issue: https://github.com/ting2tao/ai-code-copilot/issues/32
> Issue Relationship: standalone
> Branch: `feat/progressive-sdd`
> Confirmed By: user
> Confirmed At: 2026-07-13 14:08:24 +0800
> Confirmed Design Commit: `c493a2e`

## 1. Context

GPT-5.6-class coding models can usually perform local reasoning, code exploration, and straightforward implementation without a long process prompt. The framework still provides value where model intelligence cannot replace organization-specific contracts: project rules, risk boundaries, validation evidence, cross-session recovery, Issue relationships, PR close targets, and durable knowledge.

The current framework pays too much fixed cost for those controls:

- `skill/SKILL.md` requires every activation to load the complete `agents/copilot-prompt.md`, currently more than 800 lines.
- All code changes require a persisted Quick Card or full Spec before editing.
- Quick, Standard, and Complex repeat routing, confirmation, evidence, Issue, and finish instructions in several files.
- Superpowers overlaps with brainstorming, planning, TDD, debugging, review, verification, and branch finishing when both systems are active.
- Runtime promotion exists only from compact Quick to full Quick; there is no lower-cost contract for a clear, low-risk edit.

This design keeps one ai-code-copilot framework, makes Spec-Driven Development the common substrate, and varies only the persistence and detail of the Spec. The framework becomes a delivery-control layer rather than a second reasoning engine.

## 2. Goals

1. Make Inline SDD the default for clear, low-risk work.
2. Promote work monotonically from Inline to Compact to Full as scope, uncertainty, lifecycle, or risk increases.
3. Load only the workflow modules required for the current command and tier.
4. Preserve safety, evidence-before-claims, user-change protection, and GitHub close-target contracts at every tier where they apply.
5. Reuse existing compact/full artifacts and archived changes without migration.
6. Make deterministic rules executable in scripts instead of duplicating them as prose.
7. Treat Superpowers as an explicitly selected specialist library, not a second default orchestrator.

## 3. Non-goals

- No separate `ai-code-copilot-lite` distribution.
- No new runtime service, database, or general workflow engine.
- No automatic downgrade within an active change.
- No automatic merge, parent-Issue closure, label management, milestone management, or Project board automation.
- No deletion or rewrite of existing archived changes.
- No requirement that every local edit create a GitHub Issue.
- No attempt to measure model chain-of-thought or expose hidden reasoning.

## 4. Alternatives

### 4.1 Trim the monolithic prompt

This reduces the immediate token count but leaves one routing and maintenance surface. New commands would cause the prompt to grow again.

### 4.2 Remove ai-code-copilot and use only `AGENTS.md`

This has the lowest prompt cost but removes durable change state, promotion, Issue/PR contracts, cross-session recovery, review records, and knowledge archival.

### 4.3 Modular single framework with progressive SDD — selected

One router selects a Spec tier and loads focused workflow modules. Contracts grow only when risk or lifecycle needs them. Existing Quick and Full artifacts remain valid.

## 5. Progressive SDD Model

SDD is not a fourth workflow or a new slash command. It defines the requirement contract used by all tiers.

### 5.1 Inline SDD

Inline SDD is an in-conversation contract with no change-directory artifact. Before editing, the agent states or derives:

```text
Goal:
Scope:
Done Signal:
Verify:
```

Inline eligibility requires all of the following:

- At most two predicted files.
- One purpose and one directly reversible change.
- Clear acceptance behavior already present in the user request or code contract.
- At least one executable targeted validation command.
- No public API, schema, database, dependency, CI, deployment, generated-artifact, security, permission, authentication, sensitive-data, money, state-machine, or cross-module business-rule impact.
- No need for cross-session handoff, durable decisions, multiple commits, or independent review units.
- No GitHub mutation is required before implementation.

Inline SDD may edit code after the contract is visible. It does not create `quick-card.md`, `log.md`, `summary.md`, or an Issue. It must still preserve unrelated user changes and record actual verification output in the conversation before claiming completion.

If eligibility is uncertain, start at Compact SDD.

### 5.2 Compact SDD

Compact SDD is the existing compact Quick contract stored in `quick-card.md`. It extends the Inline contract with:

- Non-goals.
- Acceptance criteria.
- Guardrails and risk.
- Fallback and rollback.
- Agent-visible evidence and diagnostic entry points.
- Optional lifecycle fields for branch, commit, review, and finish.

Compact SDD is required when any of these are true:

- The work must survive a session boundary or be handed off.
- A commit, PR, or auditable review is expected.
- Acceptance has multiple independent conditions.
- Implementation needs bounded investigation or more than one validation command.
- Project policy requires a persisted change contract.

The current compact Quick record format remains compatible. `recordMode: compact` continues to identify this tier.

### 5.3 Full SDD

Full SDD uses the complete change record:

- `design-brief.md` for confirmed design exploration when needed.
- `spec.md` for behavior and boundaries.
- `tasks.md` for implementation units.
- `test-spec.md` for acceptance evidence.
- `log.md` for decisions, failures, and review evidence.
- `summary.md` for low-cost session recovery.
- `roadmap.md` and child Specs for Complex work.

Full SDD is mandatory for public API or schema changes, database changes, dependencies, CI/deployment, generated artifacts, security/permission/authentication, sensitive data, money, state machines, cross-module business rules, more than five files, multiple independently deliverable goals, or accepted residual risk.

## 6. Runtime Promotion

Promotion is monotonic:

```text
Inline -> Compact -> Full
Inline -----------> Full
```

No active change automatically downgrades. A new later task may start at a lower tier.

### 6.1 Inline to Compact

Promote before further edits when:

- More than two files become necessary.
- A second purpose, commit, or acceptance unit appears.
- The targeted validation command is missing, unavailable, or insufficient.
- Debugging requires a durable decision or repeated investigation.
- Scope or acceptance is no longer explicit.
- The work needs a session handoff, commit, PR, or auditable review.
- The user asks to persist the contract.

Promotion performs these steps:

1. Stop new edits.
2. Capture the Inline contract, current diff, commands already run, and observed results.
3. Create `quick-card.md` with `recordMode: compact` and provenance `promotedFrom: inline`.
4. Copy evidence without inventing results or re-running successful commands solely for documentation.
5. Recompute the contract hash.
6. Ask for confirmation only when Goal, Scope, Acceptance, Guardrails, or external actions materially changed.
7. Resume after the Compact record is valid.

### 6.2 Compact to Full

Keep the existing Runtime promotion behavior and add direct alignment with the SDD contract. Promotion is required when:

- Compact eligibility is violated.
- The confirmed contract materially changes.
- Review finds an Important or Critical correction.
- Durable knowledge or unresolved/accepted risk appears.
- Multiple implementation or review units are needed.
- Full-tier risk is discovered.

Promotion stops edits, creates `log.md` and `summary.md`, copies the Quick Card evidence, switches `recordMode` to `full`, updates the hash, and requests confirmation only for a material contract change.

### 6.3 Direct Inline to Full

When Inline investigation immediately discovers a full-tier risk, skip Compact. Generate the Full record from the Inline contract and current evidence, then require confirmation before implementation continues.

## 7. Spec Lifecycle and Reverse Sync

All tiers use the same logical lifecycle:

```text
Draft -> Confirmed -> Implementing -> Validating -> Completed
                         |
                         v
                      Diverged -> Reverse Sync -> Implementing
```

Inline contracts are considered confirmed without a separate confirmation round when the user request already makes Goal, Scope, Done Signal, and Verify unambiguous.

Reverse Sync distinguishes two cases:

- Mechanical correction: paths, symbol names, commands, and implementation details that do not change user-visible behavior or risk. Update automatically and record the change.
- Material correction: Goal, Scope, Acceptance, Guardrails, risk, or external actions change. Stop and request confirmation.

`Goal Contract` is no longer a separate concept to duplicate. It becomes the leading section of every Spec tier:

- Goal.
- Done Signal.
- Guardrails.
- Fallback.
- Memory.

Harness fields derive from the Spec: Acceptance maps to tests, Done Signal maps to verification, Guardrails map to mechanical checks or human gates, and Fallback maps to rollback/stop behavior.

## 8. Modular Loading Architecture

Replace the mandatory complete prompt load with a small router and focused workflow modules:

```text
skill/SKILL.md
  -> agents/router.md
       -> agents/workflows/inline.md
       -> agents/workflows/compact.md
       -> agents/workflows/full.md
       -> agents/workflows/debug.md
       -> agents/workflows/review.md
       -> agents/workflows/test.md
       -> agents/workflows/finish.md
       -> agents/workflows/archive.md
```

`router.md` should contain only:

- Intent classification.
- Tier eligibility and promotion rules.
- Always-on safety boundaries.
- Module loading instructions.
- Compatibility fallback for legacy command references.

`agents/copilot-prompt.md` remains as a compatibility index during migration, not the mandatory full runtime prompt. Commands load only their module plus required project rules and active change records.

SessionStart continues to inject only L0 safety and bounded active-change metadata. It must not preload workflow modules.

## 9. Policy Placement

Rules are separated by enforcement type.

### 9.1 Always-on semantic safety

- Preserve unrelated and uncommitted user changes.
- Never expose secrets or sensitive information.
- Require explicit authority for external or destructive actions.
- Require evidence before completion claims.
- Require human confirmation for material money, permission, state-transition, security, or production-risk changes.

### 9.2 On-demand semantic modules

- SDD tier behavior.
- Debugging and TDD.
- Domain Check.
- Review and finish.
- Knowledge archival.

### 9.3 Mechanical policy

Move deterministic contracts into a canonical machine-readable policy consumed by framework checks and referenced by prompts. Initial fields include:

- Tier thresholds and excluded risk categories.
- Allowed branch and commit types.
- Required Issue relationship and PR close target when Issue tracking applies.
- Required record sections per tier.
- Promotion trigger identifiers.

Prompts and documentation describe behavior; scripts validate the canonical values. Do not generate all prose documentation from policy in this change.

## 10. Issue and GitHub Policy

Issue creation is decoupled from the right to perform a low-risk local edit. Add project configuration:

```json
{
  "githubWorkflow": {
    "issuePolicy": "on-publish"
  }
}
```

Supported values:

- `always`: preserve the current mandatory work-Issue behavior before implementation.
- `on-commit`: resolve the work Issue before creating the first commit.
- `on-publish`: resolve the work Issue before push/PR; recommended default for new projects.
- `manual`: never create an Issue automatically; validate a user-supplied Issue when present.

Existing project configuration without `issuePolicy` keeps legacy `always` behavior to avoid silently weakening established policy. New projects default to `on-publish` only after the migration is documented and framework checks cover it.

Whenever an Issue is used, existing contracts remain unchanged:

- Reuse the recorded open work Issue and never create a duplicate.
- Parent Issue is context only.
- When a work Issue exists, the PR closes only `workIssue`; `manual` with no Issue omits closing keywords and records `closeTarget: none`.
- Parent is referenced only with `Refs`.
- Pending or contradictory relationships block publish.

`finishMode` continues to control PR handoff only.

## 11. Superpowers Boundary

ai-code-copilot is the only default orchestrator for software-project work. Superpowers remains available through explicit selection for specialist techniques:

- Systematic debugging for difficult or repeatedly failing defects.
- Verification before completion.
- Requesting or receiving code review.
- TDD for high-risk behavior where Red/Green evidence is valuable.
- Worktrees or subagents when isolation or parallelism is explicitly beneficial.

The framework must not require the Superpowers `using-superpowers` global 1% invocation rule, mandatory brainstorming for every creative task, or mandatory TDD for every feature/bug fix. Equivalent safety and evidence contracts live in the appropriate ai-code-copilot modules without loading a second workflow stack.

## 12. Compatibility and Migration

- Existing `recordMode: compact` Quick Cards remain Compact SDD.
- Existing `recordMode: full` and Standard/Complex records remain Full SDD.
- Existing archived changes are read-only and require no migration.
- Commands and natural-language aliases remain supported during the modular-prompt transition.
- The install and project-sync flow distributes new modules and policy without overwriting project-owned context, domain rules, or configuration.
- Global installation and project copies must report framework-version drift through the existing upgrade check.
- If a modular file is missing in an older installation, the compatibility index falls back to the legacy prompt and emits an upgrade warning.

## 13. Error Handling

- Ambiguous Inline contract: ask one question or start Compact; do not guess.
- Promotion artifact creation fails: preserve the diff and stop before new edits.
- Material confirmation is unavailable: keep the promoted record in draft state and stop.
- Validation unavailable: promote or record a blocking Harness gap; never claim completion.
- Policy file is missing or invalid: fall back to the safer tier and fail framework self-check.
- Issue provider is unavailable: local work follows `issuePolicy`; publish remains blocked when the selected policy requires an Issue.
- Legacy record cannot be classified: treat it as Full and preserve all files.

## 14. Verification Strategy

Framework checks must verify:

1. `skill/SKILL.md` loads the router rather than the entire legacy prompt.
2. Router fixtures classify discussion, Inline, Compact, and Full examples deterministically.
3. Every excluded risk promotes directly to Full.
4. Inline-to-Compact promotion preserves contract, diff provenance, and command evidence.
5. Compact-to-Full promotion preserves existing Quick evidence.
6. Mechanical Reverse Sync does not require confirmation; material Reverse Sync does.
7. Existing compact/full fixtures remain valid.
8. Missing or invalid policy falls back safely.
9. Each `issuePolicy` value gates edit, commit, and publish at the correct lifecycle point.
10. PR text closes only the work Issue and only references the parent.
11. SessionStart injects bounded metadata and no workflow-module bodies.
12. English and Chinese documentation remain behaviorally aligned.
13. Installer and upgrade dry-runs include new modules without overwriting project-owned files.

Primary validation:

```text
bash scripts/check_framework.sh
bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh install.sh install-wsl.sh
git diff --check
```

## 15. Rollout

The current implementation scope covers Phase 1 and Phase 2 as independently reviewable work units on the same feature branch. Phase 3 is a post-adoption follow-up because meaningful tier distribution, false-promotion, rework, and token measurements do not exist before the new router is used in real projects.

### Phase 1: loading and tier foundation

- Add the router and workflow modules.
- Add Inline SDD and monotonic promotion.
- Keep legacy prompt compatibility.
- Preserve current Issue behavior while collecting classification evidence.

### Phase 2: policy and lifecycle

- Add canonical machine-readable workflow policy.
- Add configurable `issuePolicy` with legacy-safe migration.
- Route review, finish, and archive through modules.
- Make specialist Superpowers integration explicit rather than default.

### Phase 3: measurement and simplification

- Measure initial prompt characters, time/turns before first edit, tier distribution, promotion rate, false promotion rate, verification coverage, rework, and cross-session recovery.
- Remove duplicated legacy prose only after modular parity and migration checks pass.
- Adjust thresholds from repository evidence instead of fixed 80/15/5 assumptions.

Phase 3 must not block the Phase 1/2 release. The Phase 1/2 implementation adds only the stable signals needed for later measurement; it does not invent benchmark results.

## 16. Acceptance Criteria

- A clear low-risk two-file task can complete through Inline SDD without creating change documents or an Issue under a compatible project policy.
- The same task promotes before further editing when scope, uncertainty, lifecycle, or risk exceeds Inline eligibility.
- Full-risk work cannot remain Inline or Compact.
- A promoted contract preserves existing evidence and asks for confirmation only for material changes.
- Runtime activation loads the router and relevant modules rather than the complete monolithic prompt.
- Existing compact/full changes and archived records continue to work.
- Issue creation follows project policy without weakening legacy projects; PRs close only the work Issue when one exists, and manual/no-Issue delivery never closes the parent.
- Framework self-check, shell syntax checks, and documentation alignment pass.

## 17. Phase 1/2 Implementation Evidence

Verified on 2026-07-13 against `feat/progressive-sdd`:

| Acceptance criterion | Implementation evidence | Fresh verification |
|---|---|---|
| Low-risk two-file work can remain Inline without artifacts or Issue under a compatible policy | `config/workflow-policy.json`, `agents/workflows/inline.md` | `python3 scripts/check_progressive_sdd.py .` classified the two-file executable/reversible fixture as Inline and passed |
| Scope, uncertainty, lifecycle, or risk promotes before more edits | `agents/workflows/inline.md`, `agents/workflows/compact.md`, `agents/workflows/full.md` | Focused checker validated router modules and promotion contracts; full framework check passed |
| Full-risk work cannot remain Inline or Compact | canonical `full.riskCategories`, Compact `maxFiles`, and routing in `scripts/check_progressive_sdd.py` | Focused checks classified every canonical risk, a six-file change, and multiple deliverable goals as Full |
| Promotion preserves evidence and confirms only material change | `changes/templates/quick-card.md`, `agents/spec-reviewer.md`, `agents/code-quality-reviewer.md` | Focused promotion-marker checks and bounded SessionStart fixture passed |
| Activation loads router/modules instead of the monolith | `skill/SKILL.md`, `agents/router.md`, `agents/workflows/` | Focused module-reference check passed; legacy prompt remains conditional fallback |
| Existing records and archives remain compatible | unchanged record identifiers, legacy fallback, existing templates, install/sync behavior | `bash scripts/check_framework.sh` passed all Java/Go/Python/Frontend/Monorepo fixtures |
| Issue lifecycle is configurable without weakening legacy projects | `config/project-config.json`, `scripts/init_project.sh`, `agents/workflows/finish.md`, templates, GitHub rules | fixtures preserved old config bytes and reported legacy `always`; disposable Python init produced `issuePolicy: on-publish`; manual/no-Issue uses three explicit `none` values and no closing keyword |
| Syntax, framework, docs, and scope checks pass | synchronized README/AGENTS/overview/flow/Harness/Loop docs and mechanical checks | shell syntax, focused checker, full framework check, and `git diff --check origin/main...HEAD` all exited 0 |

The disposable installation check used `init_project.sh --upgrade --dry-run`, confirmed that dry-run created no `.ai_code_copilot` directory, then performed a real initialization and found `"issuePolicy": "on-publish"` in the generated config.

Phase 3 remains a post-adoption follow-up: measure prompt characters, turns before first edit, tier distribution, promotion quality, verification coverage, rework, token use, and cross-session recovery from real projects before removing additional legacy prose or retuning thresholds.

## 18. Completion Review Corrections

Final contract review found and corrected two inconsistencies before delivery:

1. The mechanical classifier originally sent changes above five files to Compact. It now routes `files > compact.maxFiles`, multiple deliverable goals, multiple review units, every canonical full-risk category, and accepted residual risk to Full; focused regression checks cover these cases.
2. `manual` without a supplied Issue originally conflicted with an unconditional PR closing statement. The runtime, templates, rules, metrics, and public docs now record `workIssue: none`, `issueRelationship: none`, and `closeTarget: none`, omit all closing keywords, and never promote the parent to a close target.
