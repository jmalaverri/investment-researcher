from investment_researcher.domain.models import Concentration, FundamentalReport
from investment_researcher.prompts import build_user_prompt


def test_build_user_prompt_voo_like():
    report = FundamentalReport(
        ticker="VOO",
        expense_ratio_pct=0.03,
        expense_ratio_flag="low",
        concentration=Concentration(
            top_10_weight_pct=30.0, holdings_count=507, hhi=193.4, flag="low"
        ),
    )
    prompt = build_user_prompt(report)
    assert "Concentration: LOW" in prompt
    assert "broadly diversified" in prompt
