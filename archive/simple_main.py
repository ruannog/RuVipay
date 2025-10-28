"""
Versão simplificada do backend para garantir funcionamento
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date
import sqlite3
import os

app = FastAPI(
    title="RuVioPay API",
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

class TransactionResponse(BaseModel):
    id: int
    description: str
    amount: float
    type: str
    category: str
    date: str
    status: str = "completed"

class InvestmentCreate(BaseModel):
    name: str
    investment_type: str
    amount_invested: float
    current_value: float
    purchase_date: str

class InvestmentResponse(BaseModel):
    id: int
    name: str
    investment_type: str
    amount_invested: float
    current_value: float
    purchase_date: str
    profit_loss: float
    profit_loss_percentage: float

class GoalCreate(BaseModel):
    title: str
    goal_type: str
    target_amount: float
    current_amount: float = 0.0
    period_type: str
    start_date: str
    end_date: str
    category_id: Optional[int] = None

class GoalResponse(BaseModel):
    id: int
    title: str
    goal_type: str
    target_amount: float
    current_amount: float
    period_type: str
    start_date: str
    end_date: str
    progress_percentage: float
    remaining_amount: float
    is_completed: bool

# Banco de dados simples
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
    
    # Criar tabela de investimentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        investment_type TEXT NOT NULL,
        amount_invested REAL NOT NULL,
        current_value REAL NOT NULL,
        purchase_date TEXT NOT NULL
    )
    ''')
    
    # Criar tabela de metas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        goal_type TEXT NOT NULL,
        target_amount REAL NOT NULL,
        current_amount REAL DEFAULT 0.0,
        period_type TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        category_id INTEGER
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
        "status": "running"
    }

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

# Endpoints de Transações
@app.get("/api/v1/transactions", response_model=List[TransactionResponse])
async def get_transactions():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    transactions = []
    for row in rows:
        transactions.append(TransactionResponse(
            id=row[0],
            description=row[1],
            amount=row[2],
            type=row[3],
            category=row[4],
            date=row[5],
            status=row[6] if len(row) > 6 else "completed"
        ))
    
    return {"data": transactions, "status": "success"}

@app.post("/api/v1/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
        (transaction.description, transaction.amount, transaction.type, transaction.category, transaction.date)
    )
    
    transaction_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return TransactionResponse(
        id=transaction_id,
        description=transaction.description,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        date=transaction.date
    )

# Endpoints de Investimentos
@app.get("/api/v1/investments", response_model=List[InvestmentResponse])
async def get_investments():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM investments")
    rows = cursor.fetchall()
    conn.close()
    
    investments = []
    for row in rows:
        profit_loss = row[4] - row[3]  # current_value - amount_invested
        profit_loss_percentage = (profit_loss / row[3] * 100) if row[3] > 0 else 0
        
        investments.append(InvestmentResponse(
            id=row[0],
            name=row[1],
            investment_type=row[2],
            amount_invested=row[3],
            current_value=row[4],
            purchase_date=row[5],
            profit_loss=profit_loss,
            profit_loss_percentage=profit_loss_percentage
        ))
    
    return {"data": investments, "status": "success"}

@app.post("/api/v1/investments", response_model=InvestmentResponse)
async def create_investment(investment: InvestmentCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO investments (name, investment_type, amount_invested, current_value, purchase_date) VALUES (?, ?, ?, ?, ?)",
        (investment.name, investment.investment_type, investment.amount_invested, investment.current_value, investment.purchase_date)
    )
    
    investment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    profit_loss = investment.current_value - investment.amount_invested
    profit_loss_percentage = (profit_loss / investment.amount_invested * 100) if investment.amount_invested > 0 else 0
    
    return InvestmentResponse(
        id=investment_id,
        name=investment.name,
        investment_type=investment.investment_type,
        amount_invested=investment.amount_invested,
        current_value=investment.current_value,
        purchase_date=investment.purchase_date,
        profit_loss=profit_loss,
        profit_loss_percentage=profit_loss_percentage
    )

# Endpoints de Metas
@app.get("/api/v1/goals", response_model=List[GoalResponse])
async def get_goals():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals")
    rows = cursor.fetchall()
    conn.close()
    
    goals = []
    for row in rows:
        progress_percentage = (row[4] / row[3] * 100) if row[3] > 0 else 0
        remaining_amount = max(row[3] - row[4], 0)
        is_completed = row[4] >= row[3]
        
        goals.append(GoalResponse(
            id=row[0],
            title=row[1],
            goal_type=row[2],
            target_amount=row[3],
            current_amount=row[4],
            period_type=row[5],
            start_date=row[6],
            end_date=row[7],
            progress_percentage=progress_percentage,
            remaining_amount=remaining_amount,
            is_completed=is_completed
        ))
    
    return {"data": goals, "status": "success"}

@app.post("/api/v1/goals", response_model=GoalResponse)
async def create_goal(goal: GoalCreate):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO goals (title, goal_type, target_amount, current_amount, period_type, start_date, end_date, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (goal.title, goal.goal_type, goal.target_amount, goal.current_amount, goal.period_type, goal.start_date, goal.end_date, goal.category_id)
    )
    
    goal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    progress_percentage = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
    remaining_amount = max(goal.target_amount - goal.current_amount, 0)
    is_completed = goal.current_amount >= goal.target_amount
    
    return GoalResponse(
        id=goal_id,
        title=goal.title,
        goal_type=goal.goal_type,
        target_amount=goal.target_amount,
        current_amount=goal.current_amount,
        period_type=goal.period_type,
        start_date=goal.start_date,
        end_date=goal.end_date,
        progress_percentage=progress_percentage,
        remaining_amount=remaining_amount,
        is_completed=is_completed
    )

# Endpoints de Dashboard
@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
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
    categories = [
        {"id": "1", "name": "Salário", "type": "income", "color": "#10B981", "transactionCount": 1, "totalAmount": 3500},
        {"id": "2", "name": "Trabalho Extra", "type": "income", "color": "#059669", "transactionCount": 1, "totalAmount": 1200},
        {"id": "3", "name": "Investimentos", "type": "income", "color": "#047857", "transactionCount": 1, "totalAmount": 45.30},
        {"id": "4", "name": "Alimentação", "type": "expense", "color": "#EF4444", "transactionCount": 1, "totalAmount": 280.50},
        {"id": "5", "name": "Utilidades", "type": "expense", "color": "#DC2626", "transactionCount": 1, "totalAmount": 145.30},
    ]
    
    return {"status": "success", "data": categories}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando RuViPay API Simplificada...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)