from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.investment import InvestmentCreate, InvestmentUpdate, InvestmentResponse
from app.services.investment_service import (
    get_investments_by_user, get_investment_by_id, create_investment,
    update_investment, delete_investment, get_investments_summary
)
from app.api.endpoints.auth import get_current_user

router = APIRouter(prefix="/investments", tags=["investments"])

@router.get("/", response_model=List[InvestmentResponse])
def get_user_investments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter todos os investimentos do usuário"""
    return get_investments_by_user(db, current_user.id, skip, limit)

@router.get("/summary")
def get_investment_summary(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter resumo dos investimentos"""
    return get_investments_summary(db, current_user.id)

@router.get("/{investment_id}", response_model=InvestmentResponse)
def get_investment(
    investment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obter um investimento específico"""
    investment = get_investment_by_id(db, investment_id, current_user.id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return investment

@router.post("/", response_model=InvestmentResponse)
def create_new_investment(
    investment: InvestmentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar um novo investimento"""
    return create_investment(db, investment, current_user.id)

@router.put("/{investment_id}", response_model=InvestmentResponse)
def update_existing_investment(
    investment_id: int,
    investment_update: InvestmentUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualizar um investimento"""
    investment = update_investment(db, investment_id, investment_update, current_user.id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return investment

@router.delete("/{investment_id}")
def delete_existing_investment(
    investment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletar um investimento"""
    success = delete_investment(db, investment_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return {"message": "Investment deleted successfully"}