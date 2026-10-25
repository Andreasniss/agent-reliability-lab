# TASKS.md

In-flight and backlog items for this repo.

---

## In Progress





<!-- Add items here when you start working on them -->

---

## Backlog

### Observability
- [ ] Prometheus metrics — add `prometheus-client` instrumentation to `llm_client.py` (latency histogram, error counter, token usage gauge); add Grafana dashboard config
- [ ] Langfuse integration — per-request traces, cost tracking, prompt versioning (`mlflow.mistral.autolog()` alternative)
- [ ] MLflow tracing — one-line `mlflow.mistral.autolog()` setup + experiment tracking

### API / Backend
- [ ] Async endpoints in `api.py` — swap blocking `chat()` calls for `client.chat.complete_async()` to support concurrent requests

### RAG
- [ ] Expand RAG demo beyond `hr_policy.md` — add chunking strategy comparison (fixed-size vs. sentence vs. semantic), evaluate retrieval quality

### Models / Capabilities
- [ ] `random_seed` reproducibility demo — show deterministic outputs for the same prompt across runs
- [ ] `safe_prompt` / content moderation demo — test guardrailing with and without system prompt

### Developer Experience
- [ ] Pre-commit hook for `ruff` / `black` linting

---

## Done

- [x] Updated filelock to 4.2.1 on the repaired dependency baseline in PR #18. Locked installation, package consistency, Ruff, 64 tests, six deterministic evals, strict installed-dependency audit and a CacheControl concurrent file-cache/lock smoke check passed. The changed SoftReadWriteLock protocol is not used by this dependency path.

- [x] Combined the compatible OpenTelemetry 1.45.1 and Pillow 13/Streamlit 1.66.1 updates from PRs #16 and #17 with certifi 2026.10.19 to resolve the coupled dependency-audit findings. Locked installation, compile, Ruff, 64 tests, six deterministic evals, package consistency, in-memory telemetry and strict runtime audit passed; review and merge evidence remain in PR #17.

- [x] Consolidated guide ownership and configuration, corrected current repository links and separated preview from verification. Local link checks, Ruff, 64 tests and six deterministic evaluation cases passed; PR records the reviewed revision.

- [x] Refreshed the reviewed immutable AI SDLC Skill v0.5.2 source pin to `06581dab44162674234f2150a6e7120cc3f17eb7`; the canonical skill bundle is unchanged, and verification is recorded in pull request #14.

- [x] Upgraded locked urllib3 from 2.7.0 to 2.8.0 to address the dependency-audit findings; verification and release evidence are recorded in the adoption pull request.

- [x] Added the reviewed immutable AI SDLC Skill v0.5.2 source link while preserving repository checks and authorization. Adoption evidence is recorded in its pull request.

- [x] Aligned the README reviewer path, setup commands, related writing, and contribution links; verified relative links, privacy checks, Ruff, 64 tests, and six deterministic evaluation cases.

- [x] Aligned Apache-2.0 notices, README attribution, and contribution guidance; lint, 64 tests, and six deterministic evaluations passed.

- [x] Publication privacy checks, optional Git hooks, notebook output cleanup, environment-file exclusions, and pinned CI Actions; local privacy tests, lint, 37 application tests, and six deterministic evaluations passed.

- [x] Public project identity synchronization — renamed the product, application, API, notebook, and package surfaces to Agent Reliability Lab while retaining the Mistral-playground repository slug and Mistral and Ollama as explicit supported providers
- [x] Evidence-led repository handoff — dated verified gate snapshot, reciprocal companion-article links, and explicit human ownership and AI-assistance disclosure
- [x] Dependency security gate — export the locked runtime set and fail CI on known
  vulnerabilities or incomplete dependency collection with `pip-audit`
- [x] Portfolio hardening — reviewer-first Streamlit UI, credential-free preview,
  multi-turn history, explicit tool allow-list, synthetic-data labelling, versioned
  eval contract, locked dependencies, linting, interaction tests, security notes,
  and concise evidence-led README
- [x] Structured JSON output demo — `demo_structured.py` (Pydantic + `response_format`)
- [x] `MISTRAL_MODEL` in `.env.example` — already present
- [x] Streamlit web demo with weather tool integration
- [x] OpenTelemetry tracing with Jaeger
- [x] FastAPI server with `X-API-Key` auth and `/health`, `/chat`, `/summarize` endpoints
- [x] Ollama local backend (`LLM_BACKEND=local`)
- [x] Retry with exponential backoff + `Retry-After` header support
- [x] `demo.ipynb` — 19-section interactive notebook
- [x] Function / tool calling with Open-Meteo weather demo
- [x] Streaming tokens demo (`demo_stream.py`)
- [x] Model comparison demo (`demo_compare.py`)
- [x] Tests with mocks — no API key or model call needed
