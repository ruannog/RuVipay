"""
RuViPay API - Versão Simplificada e Funcional
Usar este arquivo temporariamente até resolver os problemas de dependências
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3
import os

app = FastAPI(
    title="RuViPay API",
    description="API para sistema de gestão financeira pessoal",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class TransactionCreate(BaseModel):
    description: str
    amount: float
    type: str  # 'income' ou 'expense'
    category: str
    date: str

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    status: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    description: str
    amount: float
    type: str
    category: str
    date: str
    status: str = "completed"

class CategoryResponse(BaseModel):
    id: str
    name: str
    type: str
    color: str
    transactionCount: int
    totalAmount: float

# Banco de dados SQLite
DATABASE = "ruviopay.db"

def init_db():
    """Inicializar banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Criar tabela de transações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT DEFAULT 'completed'
    )
    ''')
    
    # Inserir dados de exemplo se não existirem
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        sample_transactions = [
            ("Salário Janeiro", 3500.0, "income", "Salário", "2024-01-15"),
            ("Supermercado", 280.50, "expense", "Alimentação", "2024-01-14"),
            ("Freelance", 1200.0, "income", "Trabalho Extra", "2024-01-12"),
            ("Conta de Luz", 145.30, "expense", "Utilidades", "2024-01-11"),
            ("Dividendos", 45.30, "income", "Investimentos", "2024-01-10"),
        ]
        cursor.executemany(
            "INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
            sample_transactions
        )
    
    conn.commit()
    conn.close()

# Inicializar DB na startup
init_db()

@app.get("/")
async def root():
    return {
        "message": "🚀 RuViPay API está funcionando!",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "transactions": "/api/v1/transactions",
            "categories": "/api/v1/categories",
            "dashboard": "/api/v1/dashboard/stats",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/v1/test")
async def test_endpoint():
    return {"message": "Backend conectado com sucesso!", "timestamp": str(datetime.now())}

# Endpoints de Transações
@app.get("/api/v1/transactions")
async def get_transactions():
    """Buscar todas as transações"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    transactions = []
    for row in rows:
        transactions.append({
            "id": str(row[0]),
            "description": row[1],
            "amount": row[2],
            "type": row[3],
            "category": row[4],
            "date": row[5],
            "status": row[6] if len(row) > 6 else "completed"
        })
    
    return {"status": "success", "data": transactions}

@app.get("/api/v1/transactions/search")
async def search_transactions(q: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None, category: Optional[str] = None, type: Optional[str] = None):
    """Buscar transações com filtros"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Base query
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []
    
    # Adicionar filtros
    if q:
        query += " AND (description LIKE ? OR category LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    if type:
        query += " AND type = ?"
        params.append(type)
    
    query += " ORDER BY date DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    transactions = []
    for row in rows:
        transactions.append({
            "id": str(row[0]),
            "description": row[1],
            "amount": row[2],
            "type": row[3],
            "category": row[4],
            "date": row[5],
            "status": row[6] if len(row) > 6 else "completed"
        })
    
    return {"status": "success", "data": transactions}

@app.get("/api/v1/transactions/{transaction_id}")
async def get_transaction(transaction_id: int):
    """Buscar uma transação específica"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    return {
        "status": "success",
        "data": {
            "id": str(row[0]),
            "description": row[1],
            "amount": row[2],
            "type": row[3],
            "category": row[4],
            "date": row[5],
            "status": row[6] if len(row) > 6 else "completed"
        }
    }

@app.post("/api/v1/transactions")
async def create_transaction(transaction: TransactionCreate):
    """Criar uma nova transação"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
        (transaction.description, transaction.amount, transaction.type, transaction.category, transaction.date)
    )
    
    transaction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "data": {
            "id": str(transaction_id),
            "description": transaction.description,
            "amount": transaction.amount,
            "type": transaction.type,
            "category": transaction.category,
            "date": transaction.date,
            "status": "completed"
        }
    }

@app.put("/api/v1/transactions/{transaction_id}")
async def update_transaction(transaction_id: int, transaction: TransactionUpdate):
    """Atualizar uma transação (aceita atualizações parciais)"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Buscar transação atual
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    current_transaction = cursor.fetchone()
    
    if not current_transaction:
        conn.close()
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    # Preparar dados para atualização (manter valores atuais se não fornecidos)
    updated_data = {
        "description": transaction.description if transaction.description is not None else current_transaction[1],
        "amount": transaction.amount if transaction.amount is not None else current_transaction[2],
        "type": transaction.type if transaction.type is not None else current_transaction[3],
        "category": transaction.category if transaction.category is not None else current_transaction[4],
        "date": transaction.date if transaction.date is not None else current_transaction[5],
        "status": transaction.status if transaction.status is not None else (current_transaction[6] if len(current_transaction) > 6 else "completed")
    }
    
    cursor.execute(
        "UPDATE transactions SET description=?, amount=?, type=?, category=?, date=?, status=? WHERE id=?",
        (updated_data["description"], updated_data["amount"], updated_data["type"], 
         updated_data["category"], updated_data["date"], updated_data["status"], transaction_id)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "data": {
            "id": str(transaction_id),
            "description": updated_data["description"],
            "amount": updated_data["amount"],
            "type": updated_data["type"],
            "category": updated_data["category"],
            "date": updated_data["date"],
            "status": updated_data["status"]
        }
    }

@app.delete("/api/v1/transactions/{transaction_id}")
async def delete_transaction(transaction_id: int):
    """Deletar uma transação"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Transação deletada com sucesso"}

# Endpoints de Dashboard
@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
    """Estatísticas do dashboard"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Calcular estatísticas
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    total_expense = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0] or 0
    
    # Transações recentes
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT 5")
    recent_rows = cursor.fetchall()
    
    recent_transactions = []
    for row in recent_rows:
        recent_transactions.append({
            "id": str(row[0]),
            "description": row[1],
            "amount": row[2],
            "type": row[3],
            "category": row[4],
            "date": row[5]
        })
    
    conn.close()
    
    return {
        "status": "success",
        "data": {
            "totalIncome": total_income,
            "totalExpense": total_expense,
            "balance": total_income - total_expense,
            "transactionCount": transaction_count,
            "recentTransactions": recent_transactions
        }
    }

@app.get("/api/v1/categories")
async def get_categories():
    """Buscar categorias fixas"""
    categories = [
        # Receitas
        {"id": "1", "name": "Salário", "type": "income", "color": "#10B981", "transactionCount": 0, "totalAmount": 0},
        {"id": "2", "name": "Trabalho Extra", "type": "income", "color": "#059669", "transactionCount": 0, "totalAmount": 0},
        {"id": "3", "name": "Investimentos", "type": "income", "color": "#047857", "transactionCount": 0, "totalAmount": 0},
        {"id": "4", "name": "Outros", "type": "income", "color": "#065F46", "transactionCount": 0, "totalAmount": 0},
        
        # Despesas - Categorias que você solicitou
        {"id": "5", "name": "Alimentação", "type": "expense", "color": "#EF4444", "transactionCount": 0, "totalAmount": 0},
        {"id": "6", "name": "Transporte", "type": "expense", "color": "#DC2626", "transactionCount": 0, "totalAmount": 0},
        {"id": "7", "name": "Saúde", "type": "expense", "color": "#B91C1C", "transactionCount": 0, "totalAmount": 0},
        {"id": "8", "name": "Lazer", "type": "expense", "color": "#991B1B", "transactionCount": 0, "totalAmount": 0},
    ]
    
    # Calcular estatísticas reais das categorias
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    for category in categories:
        cursor.execute(
            "SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM transactions WHERE category = ?",
            (category["name"],)
        )
        count, total = cursor.fetchone()
        category["transactionCount"] = count
        category["totalAmount"] = total
    
    conn.close()
    
    return {"status": "success", "data": categories}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando RuViPay API Simplificada...")
    print("📁 Banco de dados: SQLite (ruviopay.db)")
    print("🌐 Acesse: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)