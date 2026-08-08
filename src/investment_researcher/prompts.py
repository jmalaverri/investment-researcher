from investment_researcher.domain.models import FundamentalReport

SYSTEM = """You are a financial data interpreter. You will be given computed metrics for an ETF.

Rules:
- Interpret ONLY the numbers provided. Do not introduce any outside facts, comparisons to other funds, historical data, or market commentary.
- Do not give investment advice or recommendations.
- Explain what these specific numbers imply about cost and concentration risk.
- 2-4 sentences, plain language."""


def build_user_prompt(report: FundamentalReport) -> str:
    return (
        f"Ticker: {report.ticker}\n"
        f"Expense ratio: {report.expense_ratio_pct}% ({report.expense_ratio_flag})\n"
        f"Holdings count: {report.concentration.holdings_count}\n"
        f"Top 10 weight: {report.concentration.top_10_weight_pct}%\n"
        f"HHI: {report.concentration.hhi}"
    )
