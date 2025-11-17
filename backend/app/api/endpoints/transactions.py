from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import (
    get_transactions_by_user, get_transaction_by_id, create_transaction,
    update_transaction, delete_transaction, get_user_balance,
    get_monthly_summary, get_recent_transactions
)

# User ID padrão (sem autenticação)
DEFAULT_USER_ID = 1

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
def get_user_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    transaction_type: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obter todas as transações do usuário"""
    return get_transactions_by_user(
        db, DEFAULT_USER_ID, skip, limit, 
        start_date, end_date, transaction_type, category_id
    )

@router.get("/recent", response_model=List[TransactionResponse])
def get_recent_user_transactions(
    limit: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Obter as transações mais recentes"""
    return get_recent_transactions(db, DEFAULT_USER_ID, limit)

@router.get("/balance")
def get_balance(
    db: Session = Depends(get_db)
):
    """Obter saldo do usuário"""
    return get_user_balance(db, DEFAULT_USER_ID)

@router.get("/summary/{year}/{month}")
def get_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """Obter resumo mensal"""
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Month must be between 1 and 12"
        )
    return get_monthly_summary(db, DEFAULT_USER_ID, year, month)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """Obter uma transação específica"""
    transaction = get_transaction_by_id(db, transaction_id, DEFAULT_USER_ID)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@router.post("/", response_model=TransactionResponse)
def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Criar uma nova transação"""
    return create_transaction(db, transaction, DEFAULT_USER_ID)

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_existing_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar uma transação"""
    transaction = update_transaction(db, transaction_id, transaction_update, DEFAULT_USER_ID)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

@router.delete("/{transaction_id}")
def delete_existing_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """Deletar uma transação"""
    success = delete_transaction(db, transaction_id, DEFAULT_USER_ID)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return {"message": "Transaction deleted successfully"}
