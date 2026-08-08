from investment_researcher.analytics import (
    classify_expense_ratio,
    compute_concentration,
)
from investment_researcher.domain.models import FundamentalReport
from investment_researcher.errors import LLMUnavailable
from investment_researcher.ports import FundDataSource, LLMClient
from investment_researcher.prompts import SYSTEM, build_user_prompt


class Fundamentalist:
    """Orchestrates a fund fetch through the analytics core into a FundamentalReport."""

    def __init__(
        self, data_source: FundDataSource, llm: LLMClient | None = None
    ) -> None:
        self._data_source = data_source
        self._llm = llm

    def analyze(self, ticker: str) -> FundamentalReport:
        fund = self._data_source.fetch(ticker)
        weights = [holding.weight_pct for holding in fund.holdings]

        report = FundamentalReport(
            ticker=fund.ticker,
            expense_ratio_pct=fund.expense_ratio_pct,
            expense_ratio_flag=classify_expense_ratio(fund.expense_ratio_pct),
            concentration=compute_concentration(weights),
        )

        if self._llm is None:
            return report

        try:
            report.interpretation = self._llm.complete(
                SYSTEM, build_user_prompt(report)
            )
        except LLMUnavailable:
            pass

        return report
