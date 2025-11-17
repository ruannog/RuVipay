from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.investment import InvestmentCreate, InvestmentUpdate, InvestmentResponse
from app.services.investment_service import (
    get_investments_by_user, get_investment_by_id, create_investment,
    update_investment, delete_investment, get_investments_summary
)

# User ID padrão (sem autenticação)
DEFAULT_USER_ID = 1

router = APIRouter()

@router.get("/", response_model=List[InvestmentResponse])
def get_user_investments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Obter todos os investimentos do usuário"""
    return get_investments_by_user(db, DEFAULT_USER_ID, skip, limit)

@router.get("/summary")
def get_investment_summary(
    db: Session = Depends(get_db)
):
    """Obter resumo dos investimentos"""
    return get_investments_summary(db, DEFAULT_USER_ID)

@router.get("/{investment_id}", response_model=InvestmentResponse)
def get_investment(
    investment_id: int,
    db: Session = Depends(get_db)
):
    """Obter um investimento específico"""
    investment = get_investment_by_id(db, investment_id, DEFAULT_USER_ID)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return investment

@router.post("/", response_model=InvestmentResponse)
def create_new_investment(
    investment: InvestmentCreate,
    db: Session = Depends(get_db)
):
    """Criar um novo investimento"""
    return create_investment(db, investment, DEFAULT_USER_ID)

@router.put("/{investment_id}", response_model=InvestmentResponse)
def update_existing_investment(
    investment_id: int,
    investment_update: InvestmentUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar um investimento"""
    investment = update_investment(db, investment_id, investment_update, DEFAULT_USER_ID)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return investment

@router.delete("/{investment_id}")
def delete_existing_investment(
    investment_id: int,
    db: Session = Depends(get_db)
):
    """Deletar um investimento"""
    success = delete_investment(db, investment_id, DEFAULT_USER_ID)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return {"message": "Investment deleted successfully"}
