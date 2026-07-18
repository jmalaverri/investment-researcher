from investment_researcher.domain.models import FundData


class FakeFundDataSource:
    """In-memory test double for FundDataSource — no network.

    Formal unknown-ticker error semantics are deferred to the real-adapter step.
    """

    def __init__(self, funds: dict[str, FundData]) -> None:
        self._funds = funds

    def fetch(self, ticker: str) -> FundData:
        return self._funds[ticker]
