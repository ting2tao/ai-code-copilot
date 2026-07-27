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
