from investment_researcher.domain.models import FundData, Holding


def parse_etf_profile(raw: dict, ticker: str) -> FundData:
    """Parse an Alpha Vantage ETF_PROFILE response into a FundData contract.

    Fractional strings (expense ratio, holding weights) are converted to
    percent by multiplying by 100, with no rounding. Holdings whose parsed
    weight is 0.0 are dropped (dead/expired rows). A holding's symbol of
    "n/a" maps to ticker=None. A holding's name comes from its description,
    falling back to its symbol, then to "UNKNOWN" if both are "n/a".
    """
    holdings = []
    for row in raw["holdings"]:
        weight_pct = float(row["weight"]) * 100
        if weight_pct == 0.0:
            continue

        symbol = row["symbol"]
        description = row["description"]

        holding_ticker = None if symbol == "n/a" else symbol
        if description != "n/a":
            name = description
        elif symbol != "n/a":
            name = symbol
        else:
            name = "UNKNOWN"

        holdings.append(
            Holding(name=name, ticker=holding_ticker, weight_pct=weight_pct)
        )

    return FundData(
        ticker=ticker,
        name=None,
        expense_ratio_pct=float(raw["net_expense_ratio"]) * 100,
        holdings=holdings,
    )
