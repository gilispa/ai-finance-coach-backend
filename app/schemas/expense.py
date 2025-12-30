from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ExpenseBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
