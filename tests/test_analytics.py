import pytest

from investment_researcher.analytics import (
    classify_expense_ratio,
    compute_concentration,
)


# ---------------------------------------------------------------------------
# compute_concentration
# ---------------------------------------------------------------------------


class TestComputeConcentration:
    def test_fixture_a(self):
        weights = [40.0, 30.0, 20.0, 10.0]
        result = compute_concentration(weights)
        assert result.holdings_count == 4
        assert result.top_10_weight_pct == pytest.approx(100.0)
        assert result.hhi == pytest.approx(3000.0)  # 1600+900+400+100

    def test_fixture_b(self):
        # one 20 + ten 8s  → 11 holdings
        weights = [20.0] + [8.0] * 10
        result = compute_concentration(weights)
        assert result.holdings_count == 11
        assert result.top_10_weight_pct == pytest.approx(92.0)  # 20 + 9*8
        assert result.hhi == pytest.approx(1040.0)  # 400 + 10*64

    def test_edge_single_holding(self):
        result = compute_concentration([100.0])
        assert result.holdings_count == 1
        assert result.top_10_weight_pct == pytest.approx(100.0)
        assert result.hhi == pytest.approx(10000.0)

    def test_edge_empty_raises(self):
        with pytest.raises(ValueError):
            compute_concentration([])


# ---------------------------------------------------------------------------
# classify_expense_ratio
# ---------------------------------------------------------------------------


class TestClassifyExpenseRatio:
    def test_low(self):
        assert classify_expense_ratio(0.03) == "low"

    def test_moderate(self):
        assert classify_expense_ratio(0.30) == "moderate"

    def test_high(self):
        assert classify_expense_ratio(0.75) == "high"

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            classify_expense_ratio(-0.01)
