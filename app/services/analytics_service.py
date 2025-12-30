from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense


def get_expense_summary(db: Session):
    # Total spent
    total_spent = db.query(func.sum(Expense.amount)).scalar() or 0.0

    # Group by category
    results = (
        db.query(
            Expense.category,
            func.sum(Expense.amount)
        )
        .group_by(Expense.category)
        .all()
    )

    by_category = {
        category: float(amount)
        for category, amount in results
    }

    return {
        "total_spent": float(total_spent),
        "by_category": by_category
    }
