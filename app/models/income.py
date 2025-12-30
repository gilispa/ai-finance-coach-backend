from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime

from app.database import Base


class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
