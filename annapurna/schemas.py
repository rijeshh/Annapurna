# apps/api/schemas.py

from pydantic import BaseModel, field_validator, ConfigDict
from typing import Literal
from datetime import datetime

INCOME_CATEGORIES = ["photo_services", "photocopy", "mobile_and_repairs", "other"]

# ── Input schema (what client sends) ──────────────────────────
class TransactionCreate(BaseModel):
    amount: float
    type: Literal["income", "expense"]
    category: str
    note: str | None = None

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return v

    @field_validator("category")
    @classmethod
    def validate_category(cls, v, info):
        # if type is income, category must be from the fixed list
        if info.data.get("type") == "income" and v not in INCOME_CATEGORIES:
            raise ValueError(f"Income category must be one of {INCOME_CATEGORIES}")
        return v

# ── Response schema (what API returns) ────────────────────────
class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # reads SQLAlchemy objects

    id: int
    amount: float
    type: str
    category: str
    note: str | None
    created_at: datetime

# ── Auth schema ────────────────────────────────────────────────
class LoginRequest(BaseModel):
    password: str