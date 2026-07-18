import json
from pathlib import Path

import httpx
import pytest

from investment_researcher.adapters.alphavantage import AlphaVantageFundData
from investment_researcher.errors import FundDataUnavailable, TickerNotFound

VOO_RAW = json.loads((Path(__file__).parent / "fixtures" / "etf_voo.json").read_text())


def _adapter(handler) -> AlphaVantageFundData:
    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    return AlphaVantageFundData(api_key="dummy", client=client)


def test_success():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=VOO_RAW)

    adapter = _adapter(handler)
    fund = adapter.fetch("VOO")

    assert fund.ticker == "VOO"
    assert len(fund.holdings) > 400


def test_rate_limited():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"Information": "rate limit reached"})

    adapter = _adapter(handler)

    with pytest.raises(FundDataUnavailable):
        adapter.fetch("VOO")


def test_error_message():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"Error Message": "invalid api call"})

    adapter = _adapter(handler)

    with pytest.raises(FundDataUnavailable):
        adapter.fetch("VOO")


def test_unknown_ticker():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={})

    adapter = _adapter(handler)

    with pytest.raises(TickerNotFound):
        adapter.fetch("ZZZZ")


def test_http_500():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    adapter = _adapter(handler)

    with pytest.raises(FundDataUnavailable):
        adapter.fetch("VOO")


def test_network_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection failed", request=request)

    adapter = _adapter(handler)

    with pytest.raises(FundDataUnavailable):
        adapter.fetch("VOO")
