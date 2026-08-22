import json
from pathlib import Path

import pytest

from investment_researcher.adapters.alphavantage import parse_etf_profile

# the raw shape Alpha Vantage returns, shrunk to 6 rows
SMALL = {
    "net_expense_ratio": "0.0003",
    "holdings": [
        {"symbol": "AAA", "description": "Alpha Corp", "weight": "0.10"},  # normal
        {
            "symbol": "n/a",
            "description": "US DOLLAR",
            "weight": "0.05",
        },  # cash: real weight, no symbol
        {
            "symbol": "BBB",
            "description": "n/a",
            "weight": "0.02",
        },  # name missing -> fall back to symbol
        {
            "symbol": "n/a",
            "description": "TRS:EXPIRED SWAP",
            "weight": "0.0",
        },  # dead row -> DROP
        {"symbol": "CCC", "description": "Gamma Inc", "weight": "0.03"},  # normal
        {
            "symbol": "n/a",
            "description": "n/a",
            "weight": "0.01",
        },  # nothing -> name "UNKNOWN"
    ],
}


class TestParseEtfProfileSmall:
    def test_fund_level_fields(self):
        fund = parse_etf_profile(SMALL, "TEST")
        assert fund.ticker == "TEST"
        assert fund.name is None
        assert fund.expense_ratio_pct == pytest.approx(0.03)

    def test_drops_dead_rows(self):
        fund = parse_etf_profile(SMALL, "TEST")
        assert len(fund.holdings) == 5

    def test_normal_row(self):
        fund = parse_etf_profile(SMALL, "TEST")
        holding = fund.holdings[0]
        assert holding.ticker == "AAA"
        assert holding.name == "Alpha Corp"
        assert holding.weight_pct == pytest.approx(10.0)

    def test_cash_row_no_symbol(self):
        fund = parse_etf_profile(SMALL, "TEST")
        holding = fund.holdings[1]
        assert holding.ticker is None
        assert holding.name == "US DOLLAR"
        assert holding.weight_pct == pytest.approx(5.0)

    def test_missing_name_falls_back_to_symbol(self):
        fund = parse_etf_profile(SMALL, "TEST")
        holding = fund.holdings[2]
        assert holding.ticker == "BBB"
        assert holding.name == "BBB"
        assert holding.weight_pct == pytest.approx(2.0)

    def test_another_normal_row(self):
        fund = parse_etf_profile(SMALL, "TEST")
        holding = fund.holdings[3]
        assert holding.ticker == "CCC"
        assert holding.name == "Gamma Inc"
        assert holding.weight_pct == pytest.approx(3.0)

    def test_missing_symbol_and_name_falls_back_to_unknown(self):
        fund = parse_etf_profile(SMALL, "TEST")
        holding = fund.holdings[4]
        assert holding.ticker is None
        assert holding.name == "UNKNOWN"
        assert holding.weight_pct == pytest.approx(1.0)


class TestParseEtfProfileVoo:
    @pytest.fixture
    def raw(self):
        fixture_path = Path(__file__).parent / "fixtures" / "etf_voo.json"
        return json.loads(fixture_path.read_text())

    def test_fund_level_fields(self, raw):
        fund = parse_etf_profile(raw, "VOO")
        assert fund.ticker == "VOO"
        assert fund.name is None
        assert fund.expense_ratio_pct == pytest.approx(0.03)

    def test_holdings_count(self, raw):
        fund = parse_etf_profile(raw, "VOO")
        assert len(fund.holdings) > 400

    def test_first_holding_is_nvda(self, raw):
        fund = parse_etf_profile(raw, "VOO")
        holding = fund.holdings[0]
        assert holding.ticker == "NVDA"
        assert holding.weight_pct == pytest.approx(7.5)

    def test_no_zero_weight_holdings(self, raw):
        fund = parse_etf_profile(raw, "VOO")
        assert all(holding.weight_pct != 0.0 for holding in fund.holdings)

    def test_every_holding_has_a_name(self, raw):
        fund = parse_etf_profile(raw, "VOO")
        assert all(holding.name for holding in fund.holdings)
