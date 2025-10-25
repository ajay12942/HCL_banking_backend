from fastapi import FastAPI
from .database import engine, Base
from . import models
from .routers import auth_router, customers_router, admins_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HCL Banking Backend",
    description="Modular Banking Backend System for HCL Hackathon",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(admins_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to HCL Banking Backend API"}