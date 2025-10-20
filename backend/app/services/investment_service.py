from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from typing import List, Optional
from datetime import datetime
from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentUpdate

def get_investments_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Investment]:
    return db.query(Investment).filter(
        Investment.user_id == user_id
    ).order_by(desc(Investment.purchase_date)).offset(skip).limit(limit).all()

def get_investment_by_id(db: Session, investment_id: int, user_id: int) -> Optional[Investment]:
    return db.query(Investment).filter(
        and_(Investment.id == investment_id, Investment.user_id == user_id)
    ).first()

def create_investment(db: Session, investment: InvestmentCreate, user_id: int) -> Investment:
    db_investment = Investment(**investment.dict(), user_id=user_id)
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment

def update_investment(
    db: Session, 
    investment_id: int, 
    investment_update: InvestmentUpdate, 
    user_id: int
) -> Optional[Investment]:
    db_investment = get_investment_by_id(db, investment_id, user_id)
    if not db_investment:
        return None
    
    update_data = investment_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_investment, field, value)
    
    db.commit()
    db.refresh(db_investment)
    return db_investment

def delete_investment(db: Session, investment_id: int, user_id: int) -> bool:
    db_investment = get_investment_by_id(db, investment_id, user_id)
    if not db_investment:
        return False
    
    db.delete(db_investment)
    db.commit()
    return True

def get_investments_summary(db: Session, user_id: int) -> dict:
    """Obtém resumo dos investimentos do usuário"""
    
    # Total investido
    total_invested = db.query(func.sum(Investment.amount_invested)).filter(
        Investment.user_id == user_id
    ).scalar() or 0
    
    # Valor atual total
    total_current_value = db.query(func.sum(Investment.current_value)).filter(
        Investment.user_id == user_id
    ).scalar() or 0
    
    # Lucro/Prejuízo
    profit_loss = float(total_current_value) - float(total_invested)
    
    # Percentual de lucro/prejuízo
    profit_loss_percentage = 0
    if total_invested > 0:
        profit_loss_percentage = (profit_loss / float(total_invested)) * 100
    
    # Investimentos por tipo
    investments_by_type = db.query(
        Investment.type,
        func.sum(Investment.amount_invested).label('invested'),
        func.sum(Investment.current_value).label('current'),
        func.count(Investment.id).label('count')
    ).filter(Investment.user_id == user_id).group_by(Investment.type).all()
    
    return {
        "total_invested": float(total_invested),
        "total_current_value": float(total_current_value),
        "profit_loss": profit_loss,
        "profit_loss_percentage": profit_loss_percentage,
        "investments_by_type": [
            {
                "type": inv.type,
                "invested": float(inv.invested),
                "current_value": float(inv.current),
                "count": inv.count,
                "profit_loss": float(inv.current) - float(inv.invested),
                "profit_loss_percentage": ((float(inv.current) - float(inv.invested)) / float(inv.invested) * 100) if inv.invested > 0 else 0
            }
            for inv in investments_by_type
        ]
    }