from fastapi import APIRouter
from .endpoints import transactions, categories, dashboard, auth, investments, goals

api_router = APIRouter()

# Incluir rotas
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])
api_router.include_router(goals.router, prefix="/goals", tags=["goals"])