from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "AI Finance Coach API is running"}


@app.post("/expenses")
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = Expense(
        description=expense.description,
        amount=expense.amount
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense
