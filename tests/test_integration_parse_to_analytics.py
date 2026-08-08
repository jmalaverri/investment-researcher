# tests/test_integration_parse_to_analytics.py
import json
import pytest
from investment_researcher.adapters.alphavantage import parse_etf_profile
from investment_researcher.analytics import compute_concentration


def test_real_voo_data_flows_through_analytics():
    raw = json.load(open("tests/fixtures/etf_voo.json"))

    fund = parse_etf_profile(raw, "VOO")  # step 1: the adapter
    weights = [h.weight_pct for h in fund.holdings]
    conc = compute_concentration(weights)  # step 2: the analytics — THE SEAM

    assert sum(weights) == pytest.approx(100, abs=2)
    assert conc.holdings_count == 509
    assert 30 < conc.top_10_weight_pct < 45
    assert 50 < conc.hhi < 500
