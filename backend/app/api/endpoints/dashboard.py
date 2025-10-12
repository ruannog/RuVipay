from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime, date
from typing import List

from app.database import get_db
from app.models.models import Transaction, Category
from app.schemas.schemas import DashboardData, DashboardSummary, MonthlyData, CategorySum
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=DashboardData)
async def get_dashboard_data(
    year: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obter dados para o dashboard"""
    if year is None:
        year = datetime.now().year
    
    # Summary do ano atual
    total_receitas = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "receita",
        extract('year', Transaction.date) == year
    ).scalar() or 0
    
    total_despesas = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "despesa",
        extract('year', Transaction.date) == year
    ).scalar() or 0
    
    saldo = total_receitas - total_despesas
    
    transacoes_mes = db.query(Transaction).filter(
        Transaction.user_id == current_user.id,
        extract('year', Transaction.date) == year,
        extract('month', Transaction.date) == datetime.now().month
    ).count()
    
    summary = DashboardSummary(
        total_receitas=total_receitas,
        total_despesas=total_despesas,
        saldo=saldo,
        transacoes_mes=transacoes_mes
    )
    
    # Dados mensais
    monthly_data = []
    for month in range(1, 13):
        receitas_mes = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "receita",
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).scalar() or 0
        
        despesas_mes = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == "despesa",
            extract('year', Transaction.date) == year,
            extract('month', Transaction.date) == month
        ).scalar() or 0
        
        monthly_data.append(MonthlyData(
            month=f"{year}-{month:02d}",
            receitas=receitas_mes,
            despesas=despesas_mes,
            saldo=receitas_mes - despesas_mes
        ))
    
    # Receitas por categoria
    receitas_by_category = db.query(
        Category.name,
        Category.color,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "receita",
        extract('year', Transaction.date) == year
    ).group_by(Category.name, Category.color).all()
    
    receitas_categories = [
        CategorySum(category_name=item.name, total=item.total, color=item.color)
        for item in receitas_by_category
    ]
    
    # Despesas por categoria
    despesas_by_category = db.query(
        Category.name,
        Category.color,
        func.sum(Transaction.amount).label('total')
    ).join(Transaction).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "despesa",
        extract('year', Transaction.date) == year
    ).group_by(Category.name, Category.color).all()
    
    despesas_categories = [
        CategorySum(category_name=item.name, total=item.total, color=item.color)
        for item in despesas_by_category
    ]
    
    return DashboardData(
        summary=summary,
        monthly_data=monthly_data,
        receitas_by_category=receitas_categories,
        despesas_by_category=despesas_categories
    )

@router.get("/summary")
async def get_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obter resumo rápido"""
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Total do mês atual
    receitas_mes = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "receita",
        extract('year', Transaction.date) == current_year,
        extract('month', Transaction.date) == current_month
    ).scalar() or 0
    
    despesas_mes = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.type == "despesa",
        extract('year', Transaction.date) == current_year,
        extract('month', Transaction.date) == current_month
    ).scalar() or 0
    
    return {
        "receitas_mes": receitas_mes,
        "despesas_mes": despesas_mes,
        "saldo_mes": receitas_mes - despesas_mes,
        "mes": f"{current_year}-{current_month:02d}"
    }