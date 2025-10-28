# Arquivo para criar endpoints básicos sem banco de dados
from fastapi import APIRouter
from typing import List, Dict, Any
from datetime import datetime, date
import json

router = APIRouter()

# Mock data para desenvolvimento
mock_transactions = [
    {
        "id": "1",
        "description": "Salário Janeiro",
        "amount": 3500.00,
        "type": "income",
        "category": "Salário",
        "date": "2024-01-15",
        "status": "completed"
    },
    {
        "id": "2",
        "description": "Supermercado Pão de Açúcar",
        "amount": 280.50,
        "type": "expense",
        "category": "Alimentação",
        "date": "2024-01-14",
        "status": "completed"
    },
    {
        "id": "3",
        "description": "Freelance Website",
        "amount": 1200.00,
        "type": "income",
        "category": "Trabalho",
        "date": "2024-01-13",
        "status": "pending"
    },
    {
        "id": "4",
        "description": "Combustível Shell",
        "amount": 120.00,
        "type": "expense",
        "category": "Transporte",
        "date": "2024-01-12",
        "status": "completed"
    },
    {
        "id": "5",
        "description": "Academia Smart Fit",
        "amount": 89.90,
        "type": "expense",
        "category": "Saúde",
        "date": "2024-01-11",
        "status": "completed"
    }
]

mock_categories = [
    {
        "id": "1",
        "name": "Alimentação",
        "type": "expense",
        "color": "#ef4444",
        "transactionCount": 15,
        "totalAmount": 890.50
    },
    {
        "id": "2",
        "name": "Transporte",
        "type": "expense",
        "color": "#f97316",
        "transactionCount": 8,
        "totalAmount": 420.00
    },
    {
        "id": "3",
        "name": "Saúde",
        "type": "expense",
        "color": "#06b6d4",
        "transactionCount": 3,
        "totalAmount": 280.00
    },
    {
        "id": "4",
        "name": "Salário",
        "type": "income",
        "color": "#10b981",
        "transactionCount": 1,
        "totalAmount": 3500.00
    },
    {
        "id": "5",
        "name": "Freelance",
        "type": "income",
        "color": "#06b6d4",
        "transactionCount": 2,
        "totalAmount": 1800.00
    }
]

@router.get("/transactions")
async def get_transactions():
    """Obter todas as transações"""
    return {
        "status": "success",
        "data": mock_transactions,
        "total": len(mock_transactions)
    }

@router.get("/transactions/{transaction_id}")
async def get_transaction(transaction_id: str):
    """Obter transação específica"""
    transaction = next((t for t in mock_transactions if t["id"] == transaction_id), None)
    if transaction:
        return {"status": "success", "data": transaction}
    return {"status": "error", "message": "Transação não encontrada"}

@router.post("/transactions")
async def create_transaction(transaction: Dict[Any, Any]):
    """Criar nova transação"""
    new_transaction = {
        "id": str(len(mock_transactions) + 1),
        "description": transaction.get("description", ""),
        "amount": transaction.get("amount", 0),
        "type": transaction.get("type", "expense"),
        "category": transaction.get("category", ""),
        "date": transaction.get("date", str(date.today())),
        "status": "completed"
    }
    mock_transactions.append(new_transaction)
    return {"status": "success", "data": new_transaction, "message": "Transação criada com sucesso!"}

@router.get("/categories")
async def get_categories():
    """Obter todas as categorias"""
    return {
        "status": "success",
        "data": mock_categories,
        "total": len(mock_categories)
    }

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Obter estatísticas do dashboard"""
    total_income = sum(t["amount"] for t in mock_transactions if t["type"] == "income")
    total_expense = sum(t["amount"] for t in mock_transactions if t["type"] == "expense")
    
    return {
        "status": "success",
        "data": {
            "totalIncome": total_income,
            "totalExpense": total_expense,
            "balance": total_income - total_expense,
            "transactionCount": len(mock_transactions),
            "recentTransactions": mock_transactions[:5]
        }
    }

@router.get("/dashboard/chart-data")
async def get_chart_data():
    """Obter dados para gráficos"""
    # Mock data para gráficos
    chart_data = {
        "labels": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"],
        "income": [3200, 2800, 3500, 4200, 3800, 3240],
        "expense": [2100, 1900, 2300, 2800, 2200, 1890]
    }
    
    return {
        "status": "success",
        "data": chart_data
    }

@router.get("/users/profile")
async def get_user_profile():
    """Obter perfil do usuário"""
    return {
        "status": "success",
        "data": {
            "id": "1",
            "name": "Usuário Demo",
            "email": "usuario@ruviopay.com",
            "avatar": "https://ui-avatars.com/api/?name=Usuario+Demo&background=3b82f6&color=fff"
        }
    }