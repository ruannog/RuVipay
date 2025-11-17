from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func, extract
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_transactions_by_user(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    transaction_type: Optional[str] = None,
    category_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    query = db.query(
        Transaction,
        Category.name.label('category_name')
    ).outerjoin(
        Category, Transaction.category_id == Category.id
    ).filter(Transaction.user_id == user_id)
    
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    
    results = query.order_by(desc(Transaction.date)).offset(skip).limit(limit).all()
    
    # Transformar resultados para incluir o nome da categoria
    transactions = []
    for transaction, category_name in results:
        transaction_dict = {
            "id": transaction.id,
            "description": transaction.description,
            "amount": transaction.amount,
            "type": transaction.type,
            "date": transaction.date,
            "notes": transaction.notes,
            "category_id": transaction.category_id,
            "user_id": transaction.user_id,
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
            "category": category_name or "Sem categoria"
        }
        transactions.append(transaction_dict)
    
    return transactions

def get_transaction_by_id(db: Session, transaction_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    result = db.query(
        Transaction,
        Category.name.label('category_name')
    ).outerjoin(
        Category, Transaction.category_id == Category.id
    ).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == user_id)
    ).first()
    
    if not result:
        return None
    
    transaction, category_name = result
    return {
        "id": transaction.id,
        "description": transaction.description,
        "amount": transaction.amount,
        "type": transaction.type,
        "date": transaction.date,
        "notes": transaction.notes,
        "category_id": transaction.category_id,
        "user_id": transaction.user_id,
        "created_at": transaction.created_at,
        "updated_at": transaction.updated_at,
        "category": category_name or "Sem categoria"
    }

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int) -> Dict[str, Any]:
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Buscar o nome da categoria
    category = db.query(Category).filter(Category.id == db_transaction.category_id).first()
    category_name = category.name if category else "Sem categoria"
    
    return {
        "id": db_transaction.id,
        "description": db_transaction.description,
        "amount": db_transaction.amount,
        "type": db_transaction.type,
        "date": db_transaction.date,
        "notes": db_transaction.notes,
        "category_id": db_transaction.category_id,
        "user_id": db_transaction.user_id,
        "created_at": db_transaction.created_at,
        "updated_at": db_transaction.updated_at,
        "category": category_name
    }

def update_transaction(
    db: Session, 
    transaction_id: int, 
    transaction_update: TransactionUpdate, 
    user_id: int
) -> Optional[Dict[str, Any]]:
    # Buscar a transação diretamente do banco
    db_transaction = db.query(Transaction).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == user_id)
    ).first()
    
    if not db_transaction:
        return None
    
    update_data = transaction_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.commit()
    db.refresh(db_transaction)
    
    # Buscar o nome da categoria
    category = db.query(Category).filter(Category.id == db_transaction.category_id).first()
    category_name = category.name if category else "Sem categoria"
    
    return {
        "id": db_transaction.id,
        "description": db_transaction.description,
        "amount": db_transaction.amount,
        "type": db_transaction.type,
        "date": db_transaction.date,
        "notes": db_transaction.notes,
        "category_id": db_transaction.category_id,
        "user_id": db_transaction.user_id,
        "created_at": db_transaction.created_at,
        "updated_at": db_transaction.updated_at,
        "category": category_name
    }

def delete_transaction(db: Session, transaction_id: int, user_id: int) -> bool:
    # Buscar a transação diretamente do banco
    db_transaction = db.query(Transaction).filter(
        and_(Transaction.id == transaction_id, Transaction.user_id == user_id)
    ).first()
    
    if not db_transaction:
        return False
    
    db.delete(db_transaction)
    db.commit()
    return True

def get_user_balance(db: Session, user_id: int) -> Dict[str, float]:
    """Calcula o saldo total do usuário"""
    income = db.query(func.sum(Transaction.amount)).filter(
        and_(Transaction.user_id == user_id, Transaction.type == "income")
    ).scalar() or 0
    
    expense = db.query(func.sum(Transaction.amount)).filter(
        and_(Transaction.user_id == user_id, Transaction.type == "expense")
    ).scalar() or 0
    
    return {
        "income": float(income),
        "expense": float(expense),
        "balance": float(income - expense)
    }

def get_monthly_summary(db: Session, user_id: int, year: int, month: int) -> Dict[str, Any]:
    """Resumo mensal das transações"""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Total de receitas e despesas do mês
    income = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == "income",
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).scalar() or 0
    
    expense = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).scalar() or 0
    
    # Gastos por categoria
    expenses_by_category = db.query(
        Category.name,
        func.sum(Transaction.amount).label("total")
    ).join(Transaction).filter(
        and_(
            Transaction.user_id == user_id,
            Transaction.type == "expense",
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).group_by(Category.name).all()
    
    return {
        "month": month,
        "year": year,
        "income": float(income),
        "expense": float(expense),
        "balance": float(income - expense),
        "expenses_by_category": [
            {"category": cat.name, "amount": float(cat.total)}
            for cat in expenses_by_category
        ]
    }

def get_recent_transactions(db: Session, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    """Obtém as transações mais recentes"""
    results = db.query(
        Transaction,
        Category.name.label('category_name')
    ).outerjoin(
        Category, Transaction.category_id == Category.id
    ).filter(
        Transaction.user_id == user_id
    ).order_by(desc(Transaction.date)).limit(limit).all()
    
    # Transformar resultados para incluir o nome da categoria
    transactions = []
    for transaction, category_name in results:
        transaction_dict = {
            "id": transaction.id,
            "description": transaction.description,
            "amount": transaction.amount,
            "type": transaction.type,
            "date": transaction.date,
            "notes": transaction.notes,
            "category_id": transaction.category_id,
            "user_id": transaction.user_id,
            "created_at": transaction.created_at,
            "updated_at": transaction.updated_at,
            "category": category_name or "Sem categoria"
        }
        transactions.append(transaction_dict)
    
    return transactions