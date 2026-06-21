from typing import Protocol

from investment_researcher.domain.models import FundData


class FundDataSource(Protocol):
    def fetch(self, ticker: str) -> FundData: ...


class LLMClient(Protocol):
    def complete(self, prompt: str) -> str: ...
