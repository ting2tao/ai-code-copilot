<!-- artifact
artifactVersion: 1
artifactId: workflow-codex-alignment:spec
artifactType: spec
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: workflow-codex-alignment:design-brief
upstreamHash: sha256:5ace88e00228951fa812e1b382d4da07edb0b193f7ebf2db431617604fd129f8
-->

# Approved Spec: workflow-codex-alignment

status: confirmed
confirmedBy: user
confirmationSource: User's explicit instruction to implement the preceding four-item plan and create Issue/PR.
parentIssue: none
workIssue: 39
issueRelationship: standalone
closeTarget: workIssue
branch: fix/workflow-codex-alignment
issuePolicy: on-publish (repository default config/project-config.json; this framework repository is not initialized as a client project)

## Goal Contract
- Goal: fix production risk routing, align current docs, implement minimal Codex hook integration and meaningful regressions.
- Done Signal: focused RED/GREEN evidence, framework self-check, adapter/install round trips, and an open PR to main closing #39.
- Guardrails: preserve unrelated workspace edits and PR #38; no secret logging, implicit approvals, host trust bypass, production access or model reasoning capture.
- Fallback: block malformed/unsupported adapter inputs and runtime failures; report untrusted/unavailable host capability explicitly. Do not claim synthetic checks prove actual host integration.
- Memory: keep regressions and evidence in existing tests and this log.

## Acceptance
1. Production risk alone activates Full and a human gate; low-risk native and already authorized local work stay native without artificial workflow confirmation.
2. Current README/README-CN, AGENTS, runtime reference and policy agree: at most five changed implementation files, one purpose/review unit and no Full risk may use Compact; task scale is separate from record mode. VERSION is the release source.
3. macOS/Linux, WSL and PowerShell use Codex hooks.json and Claude settings.json. Register SessionStart plus Codex apply_patch guardrail idempotently, preserve unrelated configuration/handlers, quote commands and explain required trust. No automatic migration of old settings.
4. Codex apply_patch add/update/delete/move paths are evaluated by existing controls, including lexical/resolved path protection and redaction. Safe patch returns no allow; secret/PII, protected/test paths requiring approval, malformed payloads and unavailable runtime block. Codex never emits unsupported ask. Claude retains its existing ask semantics.
5. Focused isolated tests cover actual adapter subprocess and installed commands, unsupported payload/runtime and stale approval rejection. Run full framework checks. Attempt actual host verification when available and record precise limits if unavailable/untrusted; do not bypass trust or consume paid model calls without a bounded need.
6. Bump VERSION for behavior changes, create/reuse #39, commit conventionally and open PR against main with Closes #39. Do not merge.

## Scope and risk
Policy/evals, check_guardrails.py, Codex wrapper, shared registration helper, three installers, current runtime/docs and focused tests/self-check integration. Security-sensitive: fail closed on owner-required operations; host sandbox/permissions and final diff scanning remain required. Unregistered Bash/MCP writes are outside this adapter. Rollback is a reviewed git revert/reinstall, no automated rollback. No business state/DB/money changes; DDD-lite not applicable.

## Harness
Python unittest, shell syntax, artifact-chain checker, run_agent_evals.py, check_framework.sh, temporary HOME/repositories. Official protocol checked 2026-10-22: https://learn.chatgpt.com/docs/hooks .
