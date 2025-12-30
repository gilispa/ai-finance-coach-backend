from pydantic import BaseModel, Field


class ExpenseRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Expense amount must be greater than zero")
    category: str = Field(..., min_length=3, description="Expense category")
