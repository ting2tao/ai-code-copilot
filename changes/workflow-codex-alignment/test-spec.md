<!-- artifact
artifactVersion: 1
artifactId: workflow-codex-alignment:test-spec
artifactType: test-spec
artifactStatus: finished
sourceOfTruth: repository
sourceRef: self
sourceRevision: git:36c926e82c5fa57c86c3d92125d3732679903d3c
upstream: workflow-codex-alignment:spec
upstreamHash: sha256:c8cff41c1b8c2b5b05b36e5bb62b06fbff4acd37474d2d926b1ec9357681e450
-->

# Test specification

P0: production-only risk and declared risk equivalent to detected signal; native ordinary work; safe/secret/PII/protected/test patch; move/delete and lexical/resolved paths; malformed patch and unsupported tools; missing runtime and no embedded approval bypass.
P1: installed hook command round trip; repeated registration preserves unrelated hooks/config, spaces in paths, correct platform destination and required trust warning; invalid configuration leaves bytes unchanged.
P2: shell syntax and PowerShell source contract; actual host smoke if supported/trusted. macOS cannot prove Windows/WSL host execution. No added application coverage percentage: this is a framework change with targeted behavioral checks and existing full checks.

Commands: python3 -m unittest discover -s tests -p test_workflow_alignment.py; python3 -m unittest discover -s tests -p test_guardrails.py; bash scripts/check_framework.sh; python3 scripts/check_artifact_chain.py --help (use supported CLI); git diff --check.
