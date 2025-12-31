from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ExpenseCreate(BaseModel):
    amount: float
    category_id: int
    description: Optional[str] = None



class ExpenseResponse(BaseModel):
    id: int
    amount: float
    category: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
