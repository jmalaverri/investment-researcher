# tests/test_contract.py  — the golden HHI is hand-computed, not guessed
def test_fundamental_report_constructs():
    from investment_researcher.domain.models import Concentration, FundamentalReport

    # Fixture: 4 holdings at 40/30/20/10 % → HHI = 40²+30²+20²+10² = 3000
    report = FundamentalReport(
        ticker="TEST",
        expense_ratio_pct=0.03,
        expense_ratio_flag="low",
        concentration=Concentration(
            top_10_weight_pct=100.0, holdings_count=4, hhi=3000.0, flag="high"
        ),
    )
    assert report.concentration.hhi == 3000.0
    assert report.concentration.flag == "high"
    assert report.expense_ratio_flag == "low"
