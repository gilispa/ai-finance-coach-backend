from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    normalized = name.strip().lower()

    existing = db.query(Category).filter(Category.name == normalized).first()
    if existing:
        return existing

    category = Category(
        name=normalized,
        is_custom=True
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category
