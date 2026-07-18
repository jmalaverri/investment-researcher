import os

import httpx

from investment_researcher.domain.models import FundData, Holding
from investment_researcher.errors import FundDataUnavailable, TickerNotFound

_BASE_URL = "https://www.alphavantage.co/query"
_DEFAULT_TIMEOUT = 10.0

_ADVISORY_KEYS = ("Information", "Note", "Error Message")


def parse_etf_profile(raw: dict, ticker: str) -> FundData:
    """Parse an Alpha Vantage ETF_PROFILE response into a FundData contract.

    Fractional strings (expense ratio, holding weights) are converted to
    percent by multiplying by 100, with no rounding. Holdings whose parsed
    weight is 0.0 are dropped (dead/expired rows). A holding's symbol of
    "n/a" maps to ticker=None. A holding's name comes from its description,
    falling back to its symbol, then to "UNKNOWN" if both are "n/a".
    """
    holdings = []
    for row in raw["holdings"]:
        weight_pct = float(row["weight"]) * 100
        if weight_pct == 0.0:
            continue

        symbol = row["symbol"]
        description = row["description"]

        holding_ticker = None if symbol == "n/a" else symbol
        if description != "n/a":
            name = description
        elif symbol != "n/a":
            name = symbol
        else:
            name = "UNKNOWN"

        holdings.append(
            Holding(name=name, ticker=holding_ticker, weight_pct=weight_pct)
        )

    return FundData(
        ticker=ticker,
        name=None,
        expense_ratio_pct=float(raw["net_expense_ratio"]) * 100,
        holdings=holdings,
    )


class AlphaVantageFundData:
    """FundDataSource adapter backed by the Alpha Vantage ETF_PROFILE endpoint."""

    def __init__(self, api_key: str, client: httpx.Client | None = None) -> None:
        self._api_key = api_key
        self._client = client or httpx.Client(timeout=_DEFAULT_TIMEOUT)

    @classmethod
    def from_env(cls) -> "AlphaVantageFundData":
        return cls(api_key=os.environ["FUND_API_KEY"])

    def fetch(self, ticker: str) -> FundData:
        """Return fund data for *ticker* via Alpha Vantage's ETF_PROFILE endpoint.

        Raises TickerNotFound if the ticker is unknown. Raises FundDataUnavailable
        for transport errors, non-2xx responses, invalid JSON, Alpha Vantage's
        throttle/advisory/error envelopes (all returned with HTTP 200), or a
        partial body missing exactly one of "holdings"/"net_expense_ratio".
        """
        params = {
            "function": "ETF_PROFILE",
            "symbol": ticker,
            "apikey": self._api_key,
        }
        try:
            response = self._client.get(_BASE_URL, params=params)
        except httpx.RequestError as exc:
            raise FundDataUnavailable(f"request failed for {ticker}") from exc

        if not response.is_success:
            raise FundDataUnavailable(f"HTTP {response.status_code} for {ticker}")

        try:
            body = response.json()
        except ValueError as exc:
            raise FundDataUnavailable(f"invalid JSON for {ticker}") from exc

        if any(key in body for key in _ADVISORY_KEYS):
            raise FundDataUnavailable(f"provider advisory for {ticker}: {body}")

        has_holdings = "holdings" in body
        has_expense = "net_expense_ratio" in body
        if not has_holdings and not has_expense:
            raise TickerNotFound(ticker)  # empty response → unknown symbol
        if not (has_holdings and has_expense):
            raise FundDataUnavailable(
                f"partial response for {ticker}: {body}"
            )  # partial payload → untrustworthy

        return parse_etf_profile(body, ticker)
