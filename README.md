# Agent Reliability Lab

Explore how an AI application limits tool use, cites a source and handles failures. Run the fictional preview without credentials, then optionally connect Mistral or a local Ollama model.

This is an engineering learning reference, not a production service or a model-quality benchmark.

## Try the credential-free preview

- **How many vacation days do employees receive?** The preview looks up the fictional policy and cites its *Vacation and Leave Policy* section. Full-time employees receive 25 paid vacation days per calendar year.
- **What is the weather in Munich?** The preview recognizes a weather request and explains that live observations are unavailable offline.

Both examples run without a model call. [Inspect the evaluation cases](evals/cases.json) or run them in the app.

Use Git, Python 3.12 or later, and [uv](https://docs.astral.sh/uv/getting-started/installation/).

```sh
git clone https://github.com/Andreasniss/agent-reliability-lab.git
cd agent-reliability-lab
uv sync --locked --dev
uv run streamlit run demo_streamlit.py
```

With no provider key configured, open [localhost:8501](http://localhost:8501). Confirm the **Credential-free preview** label and select either sample question. The response shows the route, tool and **No provider call**. Use **Clear conversation** in the sidebar to start again. [See the UI tests](tests/test_streamlit_app.py).

## What to inspect

- **Tool control:** tools have declared argument schemas; the application allows only named tool functions.
- **Grounding:** answers cite a small, fictional policy document.
- **Tool-task usage:** logs and spans count provider attempts (including retries), tool batches and executor calls started. Observed token sums include every reported field. Missing usage or interrupted work is marked partial, or unknown when nothing was reported. Final-response span fields retain their original meaning.
- **Failure handling:** retries are bounded; logs contain operational metadata rather than prompts, responses or tool content.

Trace each control to its implementation in the [technical guide](GUIDE.md), or explore the design in the [project walkthrough](https://andreasnissen.dev/projects/agent-reliability-lab/).

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
