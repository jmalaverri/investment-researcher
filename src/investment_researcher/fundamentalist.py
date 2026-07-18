from investment_researcher.analytics import (
    classify_expense_ratio,
    compute_concentration,
)
from investment_researcher.domain.models import FundamentalReport
from investment_researcher.ports import FundDataSource


class Fundamentalist:
    """Orchestrates a fund fetch through the analytics core into a FundamentalReport."""

    def __init__(self, data_source: FundDataSource) -> None:
        self._data_source = data_source

    def analyze(self, ticker: str) -> FundamentalReport:
        fund = self._data_source.fetch(ticker)
        weights = [holding.weight_pct for holding in fund.holdings]

        return FundamentalReport(
            ticker=fund.ticker,
            expense_ratio_pct=fund.expense_ratio_pct,
            expense_ratio_flag=classify_expense_ratio(fund.expense_ratio_pct),
            concentration=compute_concentration(weights),
        )
