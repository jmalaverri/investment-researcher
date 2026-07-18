# src/investment_researcher/ports.py
from typing import Protocol

from investment_researcher.domain.models import FundData


class FundDataSource(Protocol):
    """Port for fetching fund data.

    Synchronous by deliberate decision (see CLAUDE.md). Concurrency, if needed,
    is added at the orchestration boundary by running sync calls in threads.
    """

    def fetch(self, ticker: str) -> FundData:
        """Return fund data for *ticker* given as a plain symbol (e.g. 'VOO').

        Raises TickerNotFound if the ticker is unknown, and FundDataUnavailable
        for transient failures (network errors, rate limits, provider errors).
        See investment_researcher.errors.
        """
        ...
