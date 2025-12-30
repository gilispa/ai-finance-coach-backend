from pydantic import BaseModel
from datetime import datetime


class IncomeBase(BaseModel):
    amount: float
    source: str


class IncomeCreate(IncomeBase):
    pass


class IncomeResponse(IncomeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
