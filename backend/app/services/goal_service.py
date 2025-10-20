from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func, extract
from typing import List, Optional
from datetime import datetime, timedelta
from app.models.goal import Goal
from app.models.transaction import Transaction
from app.schemas.goal import GoalCreate, GoalUpdate

def get_goals_by_user(db: Session, user_id: int, is_active: bool = None) -> List[Goal]:
    query = db.query(Goal).filter(Goal.user_id == user_id)
    if is_active is not None:
        query = query.filter(Goal.is_active == is_active)
    return query.order_by(desc(Goal.created_at)).all()

def get_goal_by_id(db: Session, goal_id: int, user_id: int) -> Optional[Goal]:
    return db.query(Goal).filter(
        and_(Goal.id == goal_id, Goal.user_id == user_id)
    ).first()

def create_goal(db: Session, goal: GoalCreate, user_id: int) -> Goal:
    db_goal = Goal(**goal.dict(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: int, goal_update: GoalUpdate, user_id: int) -> Optional[Goal]:
    db_goal = get_goal_by_id(db, goal_id, user_id)
    if not db_goal:
        return None
    
    update_data = goal_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_goal, field, value)
    
    db.commit()
    db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int, user_id: int) -> bool:
    db_goal = get_goal_by_id(db, goal_id, user_id)
    if not db_goal:
        return False
    
    db.delete(db_goal)
    db.commit()
    return True

def update_goal_progress(db: Session, user_id: int):
    """Atualiza o progresso de todas as metas baseado nas transações"""
    
    goals = get_goals_by_user(db, user_id, is_active=True)
    
    for goal in goals:
        current_amount = 0
        
        if goal.goal_type == "expense_limit":
            # Para meta de limite de gastos, somar despesas no período
            query = db.query(func.sum(Transaction.amount)).filter(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.type == "expense",
                    Transaction.date >= goal.start_date,
                    Transaction.date <= goal.end_date
                )
            )
            
            # Se tem categoria específica, filtrar por ela
            if goal.category_id:
                query = query.filter(Transaction.category_id == goal.category_id)
            
            current_amount = query.scalar() or 0
            
        elif goal.goal_type == "savings_target":
            # Para meta de economia, somar receitas menos despesas no período
            income = db.query(func.sum(Transaction.amount)).filter(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.type == "income",
                    Transaction.date >= goal.start_date,
                    Transaction.date <= goal.end_date
                )
            ).scalar() or 0
            
            expenses = db.query(func.sum(Transaction.amount)).filter(
                and_(
                    Transaction.user_id == user_id,
                    Transaction.type == "expense",
                    Transaction.date >= goal.start_date,
                    Transaction.date <= goal.end_date
                )
            ).scalar() or 0
            
            current_amount = income - expenses
            
        elif goal.goal_type == "investment_goal":
            # Para meta de investimento, somar investimentos no período
            from app.models.investment import Investment
            current_amount = db.query(func.sum(Investment.amount_invested)).filter(
                and_(
                    Investment.user_id == user_id,
                    Investment.purchase_date >= goal.start_date,
                    Investment.purchase_date <= goal.end_date
                )
            ).scalar() or 0
        
        # Atualizar o progresso da meta
        goal.current_amount = current_amount
        db.commit()

def get_goals_summary(db: Session, user_id: int) -> dict:
    """Obtém resumo das metas do usuário"""
    
    # Atualizar progresso antes de calcular resumo
    update_goal_progress(db, user_id)
    
    goals = get_goals_by_user(db, user_id, is_active=True)
    
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g.current_amount >= g.target_amount])
    in_progress_goals = total_goals - completed_goals
    
    # Metas por tipo
    goals_by_type = {}
    for goal in goals:
        if goal.goal_type not in goals_by_type:
            goals_by_type[goal.goal_type] = {
                "count": 0,
                "completed": 0,
                "total_target": 0,
                "total_current": 0
            }
        
        goals_by_type[goal.goal_type]["count"] += 1
        goals_by_type[goal.goal_type]["total_target"] += float(goal.target_amount)
        goals_by_type[goal.goal_type]["total_current"] += float(goal.current_amount)
        
        if goal.current_amount >= goal.target_amount:
            goals_by_type[goal.goal_type]["completed"] += 1
    
    # Metas próximas do vencimento (próximos 7 dias)
    next_week = datetime.now() + timedelta(days=7)
    expiring_soon = [g for g in goals if g.end_date <= next_week and g.current_amount < g.target_amount]
    
    return {
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "in_progress_goals": in_progress_goals,
        "completion_rate": (completed_goals / total_goals * 100) if total_goals > 0 else 0,
        "goals_by_type": goals_by_type,
        "expiring_soon": len(expiring_soon)
    }