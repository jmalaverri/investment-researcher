from investment_researcher.domain.models import FundamentalReport

SYSTEM = """You are a financial data interpreter. Interpret ONLY the numbers given. Do not introduce outside facts, other funds, historical returns, or ownership data. Do not give advice. Use the labels provided; do not reclassify them. 2-3 sentences."""


_CONCENTRATION_DESCRIPTION = {
    "low": "the fund is broadly diversified",
    "moderate": "the fund is moderately concentrated",
    "high": "the fund is highly concentrated",
}


def build_user_prompt(report: FundamentalReport) -> str:
    concentration = report.concentration
    description = _CONCENTRATION_DESCRIPTION[concentration.flag]
    return (
        f"ETF {report.ticker}.\n"
        f"Expense ratio: {report.expense_ratio_pct}% ({report.expense_ratio_flag}) — "
        "the annual fee charged to investors.\n"
        f"Holdings: {concentration.holdings_count} — the number of positions in the fund.\n"
        f"Top-10 weight: {concentration.top_10_weight_pct}% — "
        "the share of assets in the ten largest positions.\n"
        f"Concentration: {concentration.flag.upper()} "
        f"(HHI {concentration.hhi} on a 0-10,000 Herfindahl-Hirschman scale) — {description}."
    )
