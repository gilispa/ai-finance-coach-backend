from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import extract
from app.models.income import Income
from app.models.category import Category
from app.models.expense import Expense


def get_top_spending_category(db):
    result = (
        db.query(
            Category.name.label("category"),
            func.sum(Expense.amount).label("total")
        )
        .join(Expense, Expense.category_id == Category.id)
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .first()
    )

    if not result:
        return None

    category, total = result

    return {
        "category": category,
        "total": round(total, 2)
    }


def get_micro_expenses(db, threshold: float = 50):
    results = (
        db.query(
            Category.name.label("category"),
            func.count(Expense.id).label("count"),
            func.sum(Expense.amount).label("total")
        )
        .join(Expense, Expense.category_id == Category.id)
        .filter(Expense.amount <= threshold)
        .group_by(Category.name)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    return [
        {
            "category": category,
            "count": count,
            "total": round(total, 2)
        }
        for category, count, total in results
    ]

def get_negative_months(db: Session):
    income_data = (
        db.query(
            extract("year", Income.created_at).label("year"),
            extract("month", Income.created_at).label("month"),
            func.sum(Income.amount).label("income")
        )
        .group_by("year", "month")
        .all()
    )

    expense_data = (
        db.query(
            extract("year", Expense.created_at).label("year"),
            extract("month", Expense.created_at).label("month"),
            func.sum(Expense.amount).label("expenses")
        )
        .group_by("year", "month")
        .all()
    )

    income_map = {
        f"{int(y)}-{int(m):02d}": income
        for y, m, income in income_data
    }

    negative_months = []

    for y, m, expenses in expense_data:
        key = f"{int(y)}-{int(m):02d}"
        income = income_map.get(key, 0)

        if expenses > income:
            negative_months.append({
                "month": key,
                "income": income,
                "expenses": expenses,
                "loss": expenses - income
            })

    return negative_months

def get_spending_risk(db: Session, warning_ratio: float = 0.7):
    total_income = db.query(func.sum(Income.amount)).scalar() or 0
    total_expenses = db.query(func.sum(Expense.amount)).scalar() or 0

    if total_income == 0:
        return {"risk": "unknown"}

    ratio = total_expenses / total_income

    if ratio >= warning_ratio:
        return {
            "risk": "high",
            "ratio": round(ratio * 100, 2)
        }

    return {
        "risk": "low",
        "ratio": round(ratio * 100, 2)
    }