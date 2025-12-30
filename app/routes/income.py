from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.income import Income
from app.schemas.income import IncomeCreate, IncomeResponse

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


@router.post("/", response_model=IncomeResponse)
def create_income(
    income: IncomeCreate,
    db: Session = Depends(get_db)
):
    new_income = Income(
        amount=income.amount,
        source=income.source
    )

    db.add(new_income)
    db.commit()
    db.refresh(new_income)

    return new_income
