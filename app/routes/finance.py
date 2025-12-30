from fastapi import APIRouter
from app.schemas.finance import ExpenseRequest
from app.services.finance_service import analyze_expense

router = APIRouter()


@router.post("/analyze-expense")
def analyze(expense: ExpenseRequest):
    return analyze_expense(expense.amount, expense.category)
