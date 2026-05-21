from decimal import Decimal
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    description: str = Field(..., max_length=255)
    amount: Decimal
    category: str | None = None


class ExpenseRead(BaseModel):
    id: int
    description: str
    amount: Decimal
    category: str | None = None
    owner_id: int

    model_config = {"from_attributes": True}
