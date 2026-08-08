from typing import Literal

from investment_researcher.domain.models import Concentration


def compute_concentration(weights: list[float]) -> Concentration:
    """Return concentration metrics for a list of weight_pct values (0–100 each).

    Raises ValueError if weights is empty, any weight is outside [0, 100], or
    the sum of weights exceeds 105.0.
    top_10_weight_pct: sum of the largest 10 weights (or all, if fewer than 10).
    hhi: sum of squared weights on the 0–100 scale (range 0–10,000).
    """
    if not weights:
        raise ValueError("weights must not be empty")
    if any(w < 0 or w > 100 for w in weights):
        raise ValueError("each weight must be in [0, 100]")

    total = sum(weights)
    if total > 105.0:
        raise ValueError(
            f"weights sum to {total:.2f}, far above 100 — check adapter units"
        )

    sorted_weights = sorted(weights, reverse=True)
    top_10 = sorted_weights[:10]

    return Concentration(
        holdings_count=len(weights),
        top_10_weight_pct=sum(top_10),
        hhi=sum(w * w for w in weights),
    )


def classify_expense_ratio(
    expense_ratio_pct: float,
) -> Literal["low", "moderate", "high"]:
    """Classify an expense ratio (percent convention, e.g. 0.03 for VOO).

    Raises ValueError for negative input.
    low:      < 0.20
    moderate: 0.20 – 0.50 (inclusive)
    high:     > 0.50
    """
    if expense_ratio_pct < 0:
        raise ValueError("expense_ratio_pct must be >= 0")
    if expense_ratio_pct < 0.20:
        return "low"
    if expense_ratio_pct <= 0.50:
        return "moderate"
    return "high"


def classify_concentration(hhi: float) -> Literal["low", "moderate", "high"]:
    """Classify a Herfindahl-Hirschman Index value (0–10,000 scale).

    low:      < 1500
    moderate: 1500 – 2500 (inclusive)
    high:     > 2500
    """
    if hhi < 1500:
        return "low"
    if hhi <= 2500:
        return "moderate"
    return "high"
