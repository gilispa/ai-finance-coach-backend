from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseResponse, ExpenseCreate

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/", response_model=ExpenseResponse)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = Expense(
        amount=expense.amount,
        category=expense.category,
        description=expense.description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    category: Optional[str] = Query(default=None),
    min_amount: Optional[float] = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    if min_amount:
        query = query.filter(Expense.amount >= min_amount)

    return query.all()
