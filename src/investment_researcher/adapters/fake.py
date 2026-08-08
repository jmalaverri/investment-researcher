from investment_researcher.domain.models import FundData
from investment_researcher.errors import LLMUnavailable


class FakeFundDataSource:
    """In-memory test double for FundDataSource — no network.

    Formal unknown-ticker error semantics are deferred to the real-adapter step.
    """

    def __init__(self, funds: dict[str, FundData]) -> None:
        self._funds = funds

    def fetch(self, ticker: str) -> FundData:
        return self._funds[ticker]


class FakeLLMClient:
    """In-memory test double for LLMClient — no Ollama, no network."""

    def __init__(self, response: str = "...", fail: bool = False) -> None:
        self._response = response
        self._fail = fail
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        if self._fail:
            raise LLMUnavailable("FakeLLMClient configured to fail")
        return self._response
