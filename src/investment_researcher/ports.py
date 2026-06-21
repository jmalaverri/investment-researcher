# src/investment_researcher/ports.py
from typing import Protocol
from investment_researcher.domain.models import FundData

class FundDataSource(Protocol):
    """Port for fetching fund data.

    Synchronous by deliberate decision (see CLAUDE.md): v0 performs a single fetch.
    Concurrency, if needed, is added at the orchestration boundary by running these
    sync calls in threads — not by making the port async.
    """
    def fetch(self, ticker: str) -> FundData: ...