from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    normalized = category.name.strip().lower()

    existing = db.query(Category).filter(Category.name == normalized).first()
    if existing:
        return existing

    new_category = Category(
        name=normalized,
        is_custom=True
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.name).all()
