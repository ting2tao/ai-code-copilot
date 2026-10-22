<!-- artifact
artifactVersion: 1
artifactId: workflow-codex-alignment:test-spec
artifactType: test-spec
artifactStatus: active
sourceOfTruth: repository
sourceRef: self
sourceRevision: working-tree
upstream: workflow-codex-alignment:spec
upstreamHash: sha256:ee105371c7d521490630c040836f468cccab4b690a89343190a07e35a6dff72c
-->

# Test specification

P0: production-only risk and declared risk equivalent to detected signal; native ordinary work; safe/secret/PII/protected/test patch; move/delete and lexical/resolved paths; malformed patch and unsupported tools; missing runtime and no embedded approval bypass.
P1: installed hook command round trip; repeated registration preserves unrelated hooks/config, spaces in paths, correct platform destination and required trust warning; invalid configuration leaves bytes unchanged.
P2: shell syntax and PowerShell source contract; actual host smoke if supported/trusted. macOS cannot prove Windows/WSL host execution. No added application coverage percentage: this is a framework change with targeted behavioral checks and existing full checks.

Commands: python3 -m unittest discover -s tests -p test_workflow_alignment.py; python3 -m unittest discover -s tests -p test_guardrails.py; bash scripts/check_framework.sh; python3 scripts/check_artifact_chain.py --help (use supported CLI); git diff --check.
