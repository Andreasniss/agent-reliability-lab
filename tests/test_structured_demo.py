import json
import logging
from unittest.mock import MagicMock

import pytest

import demo_structured


@pytest.mark.parametrize("raw,expected_type", [
    ("SYNTHETIC_STRUCTURED_CONTENT_8c0a", "JSONDecodeError"),
    (json.dumps({"score": "SYNTHETIC_STRUCTURED_CONTENT_8c0a"}), "ValidationError"),
    ([{"type": "text", "text": "SYNTHETIC_STRUCTURED_CONTENT_8c0a"}], "TypeError"),
    (json.dumps(["SYNTHETIC_STRUCTURED_CONTENT_8c0a"]), "TypeError"),
])
def test_invalid_structured_output_is_not_logged(monkeypatch, caplog, raw, expected_type):
    provider = MagicMock()
    provider.chat.complete.return_value.choices[0].message.content = raw
    monkeypatch.setattr(demo_structured, "get_client", lambda: provider)
    with caplog.at_level(logging.DEBUG, logger="demo_structured"):
        demo_structured.run_structured_demo()

    assert "SYNTHETIC_STRUCTURED_CONTENT_8c0a" not in caplog.text
    assert f"error_type={expected_type}" in caplog.text
    assert all(record.exc_info is None for record in caplog.records if record.name == "demo_structured")


def test_valid_structured_output_remains_visible_without_content_logging(monkeypatch, caplog, capsys):
    marker = "SYNTHETIC_STRUCTURED_CONTENT_8c0a"
    provider = MagicMock()
    provider.chat.complete.return_value.choices[0].message.content = json.dumps({
        "title": marker, "sentiment": "positive", "score": 8.5, "summary": "synthetic review",
    })
    monkeypatch.setattr(demo_structured, "get_client", lambda: provider)
    with caplog.at_level(logging.DEBUG, logger="demo_structured"):
        demo_structured.run_structured_demo()

    output = capsys.readouterr().out
    assert marker in output
    assert "Score:     8.5/10" in output
    assert marker not in caplog.text
