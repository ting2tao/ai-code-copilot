# Agent eval baseline

Agent evals protect the configuration that steers coding agents: router, workflow policy, skills, prompts, hooks and review contracts. They are separate from application tests.

The current baseline follows workflow policy v2: ordinary low-risk work stays `native` with no workflow modules; explicit lifecycle intent or material signals activate Compact/Full. `tier: native` is an eval route label, not a third framework-owned SDD tier. Risk facts and detected risk signals feed the same activation and human-gate checks. Required modules must exist, even when policy and case expectations agree. Historical Inline results must be rerun against this baseline, not relabeled as current evidence. `writesBeforeContract: false` prohibits premature writes at an activated gate; it does not require a persisted Spec for native work.

## Two evidence levels

1. **Offline policy oracle (blocking)** validates case structure and checks expected tier, required module, human gate and `No Contract, No Code` against `config/workflow-policy.json`. It is deterministic, local and free.
2. **External live results (non-blocking initially)** score outputs produced by a model/provider outside the runner. The runner never executes an arbitrary provider command and never treats missing live results as a pass; it reports `capability=external-results-required`.

Run the baseline:

```bash
python3 scripts/run_agent_evals.py \
  --policy config/workflow-policy.json \
  --schema evals/schema.json \
  --cases evals/cases
```

Score external results:

```bash
python3 scripts/run_agent_evals.py \
  --policy config/workflow-policy.json \
  --schema evals/schema.json \
  --cases evals/cases \
  --results /path/to/results.json
```

Each external result must contain `caseId`, `tier`, `modules`, `humanGate`, and `writesBeforeContract`. Provider invocation, credentials, budget and sandboxing belong to a separate adapter and human-approved CI configuration.

New incidents, repeated routing errors and guardrail false positives should become cases. Do not inflate the suite with near-duplicates merely to increase the case count.

## Outcome, trace, and evidence provenance

Following the [OpenAI workflow evaluation guide](https://developers.openai.com/api/docs/guides/agent-evals) (checked 2026-09-03), distinguish the actual outcome from the trace of tool calls, handoffs, guardrails, and failures. Inspect traces to diagnose behavior; use fixed datasets to compare revisions. Passing a policy oracle or a scorer self-check does not prove that a live agent obeyed the rules.

For real runs, record model/version, harness/policy revision, task/acceptance revision, environment, outcome, trace/evidence reference, reviewer method, and cost/latency when available in the existing log or external result provenance. This is a review checklist, not a new mandatory JSON schema: the current scorer does not validate these provenance fields. Preserve privacy; record observable actions and redacted results, not private chain-of-thought.

After model/tool changes, repeat representative runs and one-component-at-a-time ablations against the same baseline. A single stochastic run or a curated passing example is not proof of improvement. Calibrate model graders against human judgments and failure cases. Independent review is different from self-review; neither replaces executable outcome checks.
