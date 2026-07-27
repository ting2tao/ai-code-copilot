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

## Task 6: Project sync ownership and version state

```text
command: bash scripts/check_framework.sh
exit: 1
summary: expected RED — init_project.sh missing def framework_version()

command: bash -n scripts/init_project.sh && python3 scripts/check_model_first_versioning.py . && bash scripts/check_framework.sh
exit: 0
summary: every fixture recorded frameworkVersion/frameworkCommit; managed rules/templates/state were overwritten; config/context/domain/knowledge/active changes/archives were preserved; invalid configs failed; no .new files were created

command: bash scripts/init_project.sh --project tests/fixtures/go --upgrade --dry-run
exit: 0
summary: dry-run listed versioned managed writes and left the fixture unchanged
```

## Task 7: Runtime and documentation synchronization

```text
command: python3 scripts/check_model_first_versioning.py .
exit: 1
summary: expected RED — README.md missing Model-first, automatic activation, VERSION, 0.1.0, full replacement, frameworkVersion, and frameworkCommit

command: python3 scripts/check_model_first_versioning.py . && python3 scripts/check_progressive_sdd.py .
exit: 0
summary: model-first version/update documentation and Native -> Compact/Full runtime checks passed

command: bash scripts/check_framework.sh
exit: 0
summary: bilingual README, AGENTS, current architecture/flow/team-talk docs, policy, templates, and full fixture matrix passed

decision: removed the remaining legacy issuePolicy default so strict project sync and activated runtime now both reject missing policy instead of disagreeing.
```

## Task 8: Final verification and review

```text
command: python3 scripts/check_model_first_versioning.py . && python3 scripts/check_progressive_sdd.py . && bash scripts/test_install_overwrite.sh
exit: 0
summary: version, activation, Compact/Full routing, full-replacement install, invalid-source preservation, and static documentation contracts passed

command: bash scripts/check_framework.sh
exit: 0
summary: progressive-sdd, model-first-versioning, install overwrite, and all project fixture checks passed

command: bash -n hooks/session-start scripts/check_framework.sh scripts/init_project.sh scripts/test_install_overwrite.sh install.sh install-wsl.sh && compile both Python checker sources in memory && git diff --check origin/main
exit: 0
summary: Bash syntax, Python syntax, and full worktree diff whitespace checks passed

command: command -v pwsh
exit: 1
summary: PowerShell runtime unavailable; install.ps1 received static marker and manual code review only

command: final combined gate (first attempt)
exit: 1
summary: skill discovery description exceeded the existing 500-character budget (537); wording was shortened without broadening activation

command: final combined gate (rerun after correction)
exit: 0
summary: targeted checks, full framework gate, Bash/Python syntax, complete diff check, and explicit PowerShell limitation all passed
```

### Spec Compliance

- PASS: all ten Acceptance items are represented in runtime policy, installers, project sync, versioned state, synchronized docs, and fresh mechanical evidence.
- PASS: project-owned assets remain outside direct overwrite; installation-local edits are intentionally removed.
- PASS: no compatibility migration, old runtime fallback, automatic rollback, tag, push, or PR action was added.

### Code Quality

- Critical: none found.
- Important: none found.
- Minor/limitation: Windows/PowerShell runtime smoke is not available on this host; static checks and cross-platform symmetry are present.
- Review method: independent inline second pass against the approved Spec because this session disallows sub-Agent delegation.

## Post-install verification

The first local `0.1.0` installation exposed stale onboarding text claiming a generic coding request would activate the framework. The macOS/Linux, WSL, and PowerShell completion messages were corrected to model-first wording, a regression assertion was added, and the focused plus full framework gates passed before reinstalling.

## GitHub handoff

```text
workIssue: https://github.com/ting2tao/ai-code-copilot/issues/34
issueRelationship: standalone
closeTarget: workIssue
state: OPEN
summary: the approved model-first/versioning change summary, acceptance checklist, test plan, and PowerShell limitation were published as the unique work Issue
```

## /finish record

| Item | Result |
|------|--------|
| Work Issue | https://github.com/ting2tao/ai-code-copilot/issues/34 (OPEN, standalone) |
| Pull Request | https://github.com/ting2tao/ai-code-copilot/pull/35 (OPEN, ready for review) |
| Branch | `feat/model-first-versioning` |
| Base | `main` |
| Remote | `origin` |
| Closing keyword | `Closes #34` |
| Push result | `git push -u origin feat/model-first-versioning` succeeded after retrying with HTTP/1.1 and a larger post buffer |
| Verification | `bash scripts/check_framework.sh` PASS; Bash syntax PASS; Python checker compilation PASS; `git diff --check origin/main...HEAD` PASS |
| Limitation | Windows PowerShell runtime smoke unavailable on this macOS host; static validation passed |
| Knowledge extraction | No `Knowledge candidates` or `知识发现` entries were present; promotion skipped |
