# Agent eval baseline

Agent evals protect the configuration that steers coding agents: router, workflow policy, skills, prompts, hooks and review contracts. They are separate from application tests.

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
