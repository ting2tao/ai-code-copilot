<!-- artifact
artifactVersion: 1
artifactId: workflow-codex-alignment:design-brief
artifactType: design-brief
artifactStatus: finished
sourceOfTruth: repository
sourceRef: self
sourceRevision: git:36c926e82c5fa57c86c3d92125d3732679903d3c
upstream: none
upstreamHash: none
-->

# Workflow and Codex alignment

User approved the four-item plan on 2026-10-22 with “按上面的计划来实现，然后issue， pr到main”. This confirms implementation, security adapter changes, a work Issue and a PR targeting main; it does not authorize deployment or bypassing host trust.

Evidence: production alone activates Compact without a human gate; docs disagree on two/five files; Codex registration uses settings.json; Claude payloads differ from apply_patch.

Options: add a broad compatibility/eval platform; do nothing; or repair existing contracts and add bounded adapters. Selected: bounded repair. Reuse existing guardrail evaluation, local tests, install entrypoints and logs. No new doctor, runtime, auto-migration, rollback, plugin distribution or CI service. Temporary repositories isolate tests. Host trust remains a user action.
