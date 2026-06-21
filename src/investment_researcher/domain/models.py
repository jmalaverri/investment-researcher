# src/investment_researcher/domain/models.py
from pydantic import BaseModel, Field
from typing import Literal

class Holding(BaseModel):
    name: str
    ticker: str | None = Field(default=None, description="None for cash or unlisted positions")
    weight_pct: float = Field(ge=0, le=100, description="Percent of fund assets, 0–100")

class FundData(BaseModel):
    """Returned by a FundDataSource adapter — a trust boundary, so validate here."""
    ticker: str
    name: str
    expense_ratio_pct: float = Field(
        ge=0,
        description="Annual expense ratio as a percent. VOO ≈ 0.03 (meaning 0.03%, not 3%).",
    )
    holdings: list[Holding]

class Concentration(BaseModel):
    """Computed by the analytics core (not external input)."""
    top_10_weight_pct: float = Field(ge=0, le=100)
    holdings_count: int = Field(ge=0)
    hhi: float = Field(
        ge=0, le=10_000,
        description="Herfindahl-Hirschman Index on percent weights; standard 0–10,000 scale (>2500 ≈ highly concentrated).",
    )

class FundamentalReport(BaseModel):
    ticker: str
    expense_ratio_pct: float
    expense_ratio_flag: Literal["low", "moderate", "high"]
    concentration: Concentration
    interpretation: str | None = None