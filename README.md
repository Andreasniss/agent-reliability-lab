# Agent Reliability Lab

Explore how an AI application limits tool use, cites a source and handles failures. Run the fictional preview without credentials, then optionally connect Mistral or a local Ollama model.

This is an engineering learning reference, not a production service or a model-quality benchmark.

## Try the credential-free preview

Use Git, Python 3.12 or later, and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```sh
git clone https://github.com/Andreasniss/agent-reliability-lab.git
cd agent-reliability-lab
uv sync --locked --dev
uv run streamlit run demo_streamlit.py
```

With no provider key configured, open [localhost:8501](http://localhost:8501). Confirm the **Credential-free preview** label.

1. Select **How many vacation days do employees receive?** Expect a summary citing the fictional policy, a named tool and **No provider call**.
2. Select **What is the weather in Munich?** Expect an explanation that live weather is disabled in preview.
3. Use **Clear conversation** in the sidebar to start again.

Preview mode makes no model or live-weather call. No local runtime? Inspect the [UI tests](tests/test_streamlit_app.py) and [evaluation cases](evals/cases.json).

## What to inspect

- **Tool control:** tools have declared argument schemas; the application allows only named tool functions.
- **Grounding:** answers cite a small, fictional policy document.
- **Failure handling:** retries are bounded; logs contain operational metadata rather than prompts, responses or tool content.

The [technical guide](GUIDE.md) links each control to its implementation. The [project walkthrough](https://andreasnissen.dev/projects/mistral-playground/) explains the reviewer path; its URL retains the former project name.

## Connected mode

After the preview, follow the [Mistral or Ollama setup](GUIDE.md#connected-mode). Cloud mode needs your own API key. A pip-compatible setup is also available through `requirements.txt` in a Python 3.12 virtual environment; the quick start above uses the lockfile.

## Configuration

See the [configuration reference](GUIDE.md#configuration) for environment variables. `config.py` owns executable defaults and validation.

## Checks and limits

[CONTRIBUTING.md](CONTRIBUTING.md) lists the verification commands. The [evaluation contract](GUIDE.md#evaluation-contract) checks deterministic behavior around the model; it does not measure model quality.

The policy corpus is tiny and synthetic. Weather is the only live external tool. Authentication is for a local demo, not a public multi-user service. Read [SECURITY.md](SECURITY.md) before extending it.

## Contribute and reuse

Follow [AGENTS.md](AGENTS.md), [CONTRIBUTING.md](CONTRIBUTING.md) and the upload checks in [PRIVACY.md](PRIVACY.md).

Built by [Andreas Nissen](https://andreasnissen.dev), with AI-assisted implementation and documentation. Andreas owns requirements, architecture, evaluation, risk and release decisions. Personal project and views; no employer endorsement.

Copyright 2026 Andreas Nissen. Original code and technical documentation: [Apache-2.0](LICENSE), except where indicated. See [NOTICE](NOTICE); third-party material retains its own terms.
