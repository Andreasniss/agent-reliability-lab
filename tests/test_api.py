import logging

import httpx
import pytest
from fastapi.testclient import TestClient
from mistralai.client.errors import SDKError
from mistralai.client.models import ChatCompletionResponse

import api
import config

client = TestClient(api.app)


def test_health_is_public_and_contains_no_secret(monkeypatch):
    monkeypatch.setattr(config, "API_KEY", "server-secret")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model": config.MISTRAL_MODEL}
    assert "server-secret" not in response.text


def test_chat_rejects_missing_or_invalid_api_key(monkeypatch):
    monkeypatch.setattr(config, "API_KEY", "server-secret")
    assert client.post("/chat", json={"message": "hello"}).status_code == 401
    response = client.post(
        "/chat",
        headers={"X-API-Key": "wrong"},
        json={"message": "hello"},
    )
    assert response.status_code == 401


@pytest.mark.parametrize("endpoint,payload", [
    ("/chat", {"message": "synthetic request"}),
    ("/summarize", {"text": "synthetic request"}),
])
@pytest.mark.parametrize("error_kind", ["message", "sdk_body", "unprintable"])
def test_api_error_logs_preserve_metadata_without_error_content(monkeypatch, caplog, endpoint, payload, error_kind):
    marker = "SYNTHETIC_PROVIDER_ERROR_CONTENT_47d9"

    class UnprintableError(Exception):
        def __str__(self):
            raise AssertionError("exception text must not be formatted")

    if error_kind == "sdk_body":
        error = SDKError("API error occurred", httpx.Response(400, json={"message": marker}))
        assert marker in str(error)
    elif error_kind == "unprintable":
        error = UnprintableError(marker)
    else:
        error = RuntimeError(marker)

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(config, "API_KEY", "server-secret")
    monkeypatch.setattr(api.llm_client, "chat", fail)
    with caplog.at_level(logging.ERROR, logger="api"):
        response = client.post(endpoint, headers={"X-API-Key": "server-secret"}, json=payload)

    assert response.status_code == 502
    assert response.json() == {"detail": "Mistral API error — check logs for details"}
    assert marker not in caplog.text
    records = [record for record in caplog.records if record.name == "api"]
    assert len(records) == 1
    assert f"POST {endpoint}" in records[0].getMessage()
    assert f"error_type={type(error).__name__}" in records[0].getMessage()
    assert records[0].exc_info is None


@pytest.mark.parametrize("endpoint,payload,field", [
    ("/chat", {"message": "hello", "system": "synthetic system"}, "reply"),
    ("/summarize", {"text": "hello"}, "summary"),
])
def test_api_success_response_is_unchanged(monkeypatch, endpoint, payload, field):
    calls = []

    def chat(*args, **kwargs):
        calls.append((args, kwargs))
        return "synthetic answer"

    monkeypatch.setattr(config, "API_KEY", "server-secret")
    monkeypatch.setattr(api.llm_client, "chat", chat)
    response = client.post(endpoint, headers={"X-API-Key": "server-secret"}, json=payload)
    assert response.status_code == 200
    assert response.json() == {field: "synthetic answer", "model": config.MISTRAL_MODEL}
    assert len(calls) == 1
    if endpoint == "/chat":
        assert calls[0][0] == ("hello",)
        assert calls[0][1] == {"system_message": "synthetic system"}


@pytest.mark.parametrize("endpoint,payload", [
    ("/chat", {"message": "synthetic request"}),
    ("/summarize", {"text": "synthetic request"}),
])
def test_api_response_validation_does_not_expose_sdk_content(monkeypatch, caplog, endpoint, payload):
    from unittest.mock import MagicMock

    marker = "SYNTHETIC_RESPONSE_CHUNK_CONTENT_60aa"
    sdk_response = ChatCompletionResponse.model_validate({
        "id": "synthetic-completion",
        "object": "chat.completion",
        "created": 0,
        "model": "synthetic-model",
        "choices": [{"index": 0, "finish_reason": "stop", "message": {
            "role": "assistant", "content": [{"type": "text", "text": marker}],
        }}],
        "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
    })
    provider = MagicMock()
    provider.chat.complete.return_value = sdk_response
    monkeypatch.setattr(api.llm_client, "get_client", lambda: provider)
    monkeypatch.setattr(config, "API_KEY", "server-secret")
    with caplog.at_level(logging.ERROR, logger="api"):
        response = client.post(endpoint, headers={"X-API-Key": "server-secret"}, json=payload)

    assert response.status_code == 502
    assert response.json() == {"detail": "Mistral API error — check logs for details"}
    assert marker not in caplog.text
    assert "error_type=ValidationError" in caplog.text
    assert all(record.exc_info is None for record in caplog.records if record.name == "api")
