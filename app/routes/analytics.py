from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.expense import Expense
from app.models.income import Income
from app.models.category import Category
from sqlalchemy import extract
from app.services.insights import get_top_spending_category
from app.services.insights import get_micro_expenses
from app.services.insights import get_negative_months
from app.services.insights import get_spending_risk
from app.services.ai import generate_financial_advice

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/summary")
def get_summary(
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db)
):
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    total_income = (
        db.query(func.sum(Income.amount))
        .filter(Income.created_at >= cutoff_date)
        .scalar()
    ) or 0

    total_expenses = (
        db.query(func.sum(Expense.amount))
        .filter(Expense.created_at >= cutoff_date)
        .scalar()
    ) or 0

    savings = total_income - total_expenses

    expense_ratio = 0
    if total_income > 0:
        expense_ratio = round((total_expenses / total_income) * 100, 2)

    return {
        "period_days": days,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings,
        "expense_ratio": expense_ratio
    }

@router.get("/expenses-by-category")
def expenses_by_category(db: Session = Depends(get_db)):
    results = (
        db.query(
            Category.name.label("category"),
            func.sum(Expense.amount).label("total")
        )
        .join(Expense, Expense.category_id == Category.id)
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    return [
        {
            "category": category,
            "total": total
        }
        for category, total in results
    ]

@router.get("/monthly")
def monthly_overview(db: Session = Depends(get_db)):
    income_data = (
        db.query(
            extract("year", Income.created_at).label("year"),
            extract("month", Income.created_at).label("month"),
            func.sum(Income.amount).label("total_income")
        )
        .group_by("year", "month")
        .all()
    )

    expense_data = (
        db.query(
            extract("year", Expense.created_at).label("year"),
            extract("month", Expense.created_at).label("month"),
            func.sum(Expense.amount).label("total_expenses")
        )
        .group_by("year", "month")
        .all()
    )

    summary = {}

    for year, month, total_income in income_data:
        key = f"{int(year)}-{int(month):02d}"
        summary[key] = {
            "month": key,
            "income": total_income,
            "expenses": 0,
            "savings": total_income
        }

    for year, month, total_expenses in expense_data:
        key = f"{int(year)}-{int(month):02d}"
        if key not in summary:
            summary[key] = {
                "month": key,
                "income": 0,
                "expenses": total_expenses,
                "savings": -total_expenses
            }
        else:
            summary[key]["expenses"] = total_expenses
            summary[key]["savings"] -= total_expenses

    return list(summary.values())

@router.get("/top-category")
def top_spending_category(db: Session = Depends(get_db)):
    insight = get_top_spending_category(db)

    if not insight:
        return {"message": "No expense data available"}

    return insight

@router.get("/micro-expenses")
def micro_expenses(db: Session = Depends(get_db)):
    return get_micro_expenses(db)

@router.get("/negative-months")
def negative_months(db: Session = Depends(get_db)):
    return get_negative_months(db)

@router.get("/spending-risk")
def spending_risk(db: Session = Depends(get_db)):
    return get_spending_risk(db)

@router.get("/ai-advice")
def ai_advice(db: Session = Depends(get_db)):
    insights = {
        "top_spending_category": get_top_spending_category(db),
        "spending_risk": get_spending_risk(db)
    }

    advice = generate_financial_advice(insights)

    return {
        "insights": insights,
        "advice": advice
    }