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

        Failure semantics (e.g. unknown ticker) are defined at the adapter step.
        """
        ...
