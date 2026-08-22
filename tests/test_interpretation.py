from investment_researcher.adapters.fake import FakeFundDataSource, FakeLLMClient
from investment_researcher.domain.models import FundData, Holding
from investment_researcher.fundamentalist import Fundamentalist


def _fund() -> FundData:
    return FundData(
        ticker="TEST",
        name="Test Fund",
        expense_ratio_pct=0.03,
        holdings=[Holding(name="A", ticker="A", weight_pct=60.0)],
    )


def test_no_llm_leaves_interpretation_none():
    fundamentalist = Fundamentalist(FakeFundDataSource({"TEST": _fund()}))

    report = fundamentalist.analyze("TEST")

    assert report.interpretation is None


def test_llm_success_sets_interpretation():
    llm = FakeLLMClient("Costs are low...")
    fundamentalist = Fundamentalist(FakeFundDataSource({"TEST": _fund()}), llm=llm)

    report = fundamentalist.analyze("TEST")

    assert report.interpretation == "Costs are low..."
    assert report.concentration.hhi == 3600.0
    _system, user_prompt = llm.calls[0]
    assert "36" in user_prompt or str(report.concentration.hhi) in user_prompt


def test_llm_failure_leaves_interpretation_none_but_metrics_populated():
    llm = FakeLLMClient(fail=True)
    fundamentalist = Fundamentalist(FakeFundDataSource({"TEST": _fund()}), llm=llm)

    report = fundamentalist.analyze("TEST")

    assert report.interpretation is None
    assert report.expense_ratio_flag == "low"
    assert report.concentration.holdings_count == 1
    assert report.concentration.hhi == 3600.0
