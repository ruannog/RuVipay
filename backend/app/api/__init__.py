from fastapi import APIRouter
from app.api.endpoints import categories, transactions, goals, investments, dashboard

api_router = APIRouter()

api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

__all__ = ["api_router"]