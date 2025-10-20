from fastapi import APIRouter
from app.api.endpoints import auth, categories, transactions

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(transactions.router)

__all__ = ["api_router"]