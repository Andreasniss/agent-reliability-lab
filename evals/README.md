# Evaluation contract

These checks cover the deterministic boundary around the model: request routing,
tool selection, grounded policy evidence, and honest handling of unavailable live
data. They run without credentials and block regressions in CI.

```bash
uv run python -m evals.run_evals
```

This is deliberately not presented as a model-quality benchmark. A production
extension should add versioned provider runs, human-reviewed labels, failure
taxonomy, and cost/latency thresholds.

From the repository root, run `uv sync --locked --dev` before this command. No preview server is needed. The evaluation covers the deterministic preview contract, not connected model quality.
