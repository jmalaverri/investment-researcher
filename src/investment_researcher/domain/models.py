from typing import Literal
from pydantic import BaseModel, Field


class Holding(BaseModel):
    name: str
    ticker: str | None
    weight_pct: float = Field(ge=0, le=100)


class FundData(BaseModel):
    ticker: str
    name: str
    expense_ratio_pct: float = Field(ge=0, le=100)
    holdings: list[Holding]


class Concentration(BaseModel):
    top_10_weight_pct: float = Field(ge=0, le=100)
    holdings_count: int = Field(ge=1)
    hhi: float = Field(ge=0, le=1)


class FundamentalReport(BaseModel):
    ticker: str
    expense_ratio_pct: float = Field(ge=0, le=100)
    expense_ratio_flag: Literal["low", "moderate", "high"]
    concentration: Concentration
    interpretation: str | None = None
