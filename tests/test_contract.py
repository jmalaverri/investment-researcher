from investment_researcher.domain.models import Concentration, FundamentalReport


def test_fundamental_report_fields():
    report = FundamentalReport(
        ticker="SPY",
        expense_ratio_pct=0.09,
        expense_ratio_flag="low",
        concentration=Concentration(
            top_10_weight_pct=32.5,
            holdings_count=503,
            hhi=0.018,
        ),
    )

    assert report.ticker == "SPY"
    assert report.expense_ratio_flag == "low"
