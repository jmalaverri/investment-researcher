import json

import httpx
import pytest

from investment_researcher.adapters.ollama import OllamaClient
from investment_researcher.errors import LLMUnavailable


def _client(handler) -> OllamaClient:
    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    return OllamaClient(client=client)


def test_success():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"message": {"content": "Costs are low."}})

    client = _client(handler)
    result = client.complete("sys", "usr")

    assert result == "Costs are low."


def test_request_body():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["json"] = json.loads(request.content)
        return httpx.Response(200, json={"message": {"content": "ok"}})

    client = _client(handler)
    client.complete("sys", "usr")

    body = captured["json"]
    assert body["model"] == "llama3.2:latest"
    assert body["stream"] is False
    assert body["messages"] == [
        {"role": "system", "content": "sys"},
        {"role": "user", "content": "usr"},
    ]


def test_non_200_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    client = _client(handler)

    with pytest.raises(LLMUnavailable):
        client.complete("sys", "usr")


def test_connect_error_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    client = _client(handler)

    with pytest.raises(LLMUnavailable):
        client.complete("sys", "usr")


def test_read_timeout_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out", request=request)

    client = _client(handler)

    with pytest.raises(LLMUnavailable):
        client.complete("sys", "usr")


def test_missing_message_key_raises():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    client = _client(handler)

    with pytest.raises(LLMUnavailable):
        client.complete("sys", "usr")
