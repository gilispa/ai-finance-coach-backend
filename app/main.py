from fastapi import FastAPI

from app.database import Base, engine

from app.routes.expenses import router as expenses_router
from app.routes.income import router as income_router
from app.routes.analytics import router as analytics_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(expenses_router)
app.include_router(income_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "AI Finance Coach API is running"}
