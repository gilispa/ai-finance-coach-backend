from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc

from app.database import get_db
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.expense import ExpenseCreate, ExpenseResponse

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
        category_id=expense.category_id,
        description=expense.description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return ExpenseResponse(
        id=new_expense.id,
        amount=new_expense.amount,
        category=new_expense.category.name,
        description=new_expense.description,
        created_at=new_expense.created_at
    )


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    category_id: Optional[int] = Query(default=None),
    min_amount: Optional[float] = Query(default=None),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)

    if category_id:
        query = query.filter(Expense.category_id == category_id)

    if min_amount:
        query = query.filter(Expense.amount >= min_amount)

    expenses = (
        query
        .order_by(desc(Expense.created_at))
        .limit(limit)
        .all()
    )

    return [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            category=e.category.name,
            description=e.description,
            created_at=e.created_at
        )
        for e in expenses
    ]
