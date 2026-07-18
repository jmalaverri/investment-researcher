from investment_researcher.adapters.fake import FakeFundDataSource
from investment_researcher.domain.models import FundData, Holding
from investment_researcher.fundamentalist import Fundamentalist


def test_analyze_test_ticker():
    fund = FundData(
        ticker="TEST",
        name="Test Fund",
        expense_ratio_pct=0.03,
        holdings=[
            Holding(name="A", ticker="A", weight_pct=40.0),
            Holding(name="B", ticker="B", weight_pct=30.0),
            Holding(name="C", ticker="C", weight_pct=20.0),
            Holding(name="D", ticker="D", weight_pct=10.0),
        ],
    )
    fundamentalist = Fundamentalist(FakeFundDataSource({"TEST": fund}))

    report = fundamentalist.analyze("TEST")

    assert report.expense_ratio_flag == "low"
    assert report.concentration.hhi == 3000.0
    assert report.concentration.holdings_count == 4
    assert report.interpretation is None
