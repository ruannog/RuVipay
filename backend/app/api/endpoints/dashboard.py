from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category

router = APIRouter()

DEFAULT_USER_ID = 1


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics: income, expenses, balance, and recent transactions"""
    
    # Calculate total income and expenses
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == DEFAULT_USER_ID,
        Transaction.type == "income"
    ).scalar() or 0.0
    
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == DEFAULT_USER_ID,
        Transaction.type == "expense"
    ).scalar() or 0.0
    
    # Count total transactions
    transaction_count = db.query(func.count(Transaction.id)).filter(
        Transaction.user_id == DEFAULT_USER_ID
    ).scalar() or 0
    
    # Get recent transactions with category names
    recent_transactions = (
        db.query(
            Transaction.id,
            Transaction.amount,
            Transaction.type,
            Transaction.description,
            Transaction.date,
            Transaction.category_id,
            Category.name.label('category_name')
        )
        .join(Category, Transaction.category_id == Category.id, isouter=True)
        .filter(Transaction.user_id == DEFAULT_USER_ID)
        .order_by(Transaction.date.desc())
        .limit(5)
        .all()
    )
    
    # Format recent transactions
    formatted_transactions = []
    for t in recent_transactions:
        formatted_transactions.append({
            "id": t.id,
            "amount": float(t.amount),
            "type": t.type,
            "description": t.description,
            "date": t.date.isoformat() if t.date else None,
            "category_id": t.category_id,
            "category": t.category_name or "Sem categoria"
        })
    
    return {
        "totalIncome": float(income),
        "totalExpense": float(expense),
        "balance": float(income - expense),
        "transactionCount": transaction_count,
        "recentTransactions": formatted_transactions
    }


@router.get("/chart-data")
def get_chart_data(db: Session = Depends(get_db)):
    """Get monthly aggregated data for charts"""
    
    # Get transactions from last 12 months
    twelve_months_ago = datetime.now() - timedelta(days=365)
    
    # Query monthly income
    monthly_income = (
        db.query(
            func.strftime('%Y-%m', Transaction.date).label('month'),
            func.sum(Transaction.amount).label('total')
        )
        .filter(
            Transaction.user_id == DEFAULT_USER_ID,
            Transaction.type == "income",
            Transaction.date >= twelve_months_ago
        )
        .group_by(func.strftime('%Y-%m', Transaction.date))
        .order_by(func.strftime('%Y-%m', Transaction.date))
        .all()
    )
    
    # Query monthly expenses
    monthly_expenses = (
        db.query(
            func.strftime('%Y-%m', Transaction.date).label('month'),
            func.sum(Transaction.amount).label('total')
        )
        .filter(
            Transaction.user_id == DEFAULT_USER_ID,
            Transaction.type == "expense",
            Transaction.date >= twelve_months_ago
        )
        .group_by(func.strftime('%Y-%m', Transaction.date))
        .order_by(func.strftime('%Y-%m', Transaction.date))
        .all()
    )
    
    # Create dictionaries for easy lookup
    income_dict = {row.month: float(row.total) for row in monthly_income}
    expense_dict = {row.month: float(row.total) for row in monthly_expenses}
    
    # Get all unique months
    all_months = sorted(set(income_dict.keys()) | set(expense_dict.keys()))
    
    # Format data for chart
    chart_data = []
    for month in all_months:
        chart_data.append({
            "month": month,
            "income": income_dict.get(month, 0.0),
            "expense": expense_dict.get(month, 0.0)
        })
    
    return chart_data
