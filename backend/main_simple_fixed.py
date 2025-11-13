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

# Modelos para Investimentos
class InvestmentCreate(BaseModel):
    name: str
    type: str  # 'Renda Fixa', 'Ações', 'FII', 'Cripto', etc.
    initial_amount: float
    current_amount: float
    purchase_date: str
    description: Optional[str] = None

class InvestmentUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    initial_amount: Optional[float] = None
    current_amount: Optional[float] = None
    purchase_date: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class InvestmentResponse(BaseModel):
    id: str
    name: str
    type: str
    initial_amount: float
    current_amount: float
    purchase_date: str
    description: Optional[str] = None
    status: str = "active"

# Modelos para Metas
class GoalCreate(BaseModel):
    title: str
    goal_type: str  # 'economia', 'investimento', 'compra', 'viagem', 'outros'
    target_amount: float
    current_amount: float = 0.0
    period_type: str  # 'mensal', 'anual', 'livre'
    start_date: str
    end_date: str
    category_id: Optional[int] = None

class GoalUpdate(BaseModel):
    title: Optional[str] = None
    goal_type: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    period_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None

class GoalResponse(BaseModel):
    id: str
    title: str
    goal_type: str
    target_amount: float
    current_amount: float
    period_type: str
    start_date: str
    end_date: str
    category_id: Optional[int] = None
    status: str = "active"
    progress_percentage: float

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
    
    # Criar tabela de investimentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        initial_amount REAL NOT NULL,
        current_amount REAL NOT NULL,
        purchase_date TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'active'
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
        category_id INTEGER,
        status TEXT DEFAULT 'active'
    )
    ''')
    
    # Criar tabela de categorias
    # Tabela categories já existe, não precisa recriar
    
    # Verificar se as categorias básicas existem, se não, inserir
    default_categories = [
        # Despesas - apenas as 4 mencionadas  
        ('Alimentação', 'expense', '#EF4444'),
        ('Lazer', 'expense', '#8B5CF6'),
        ('Transporte', 'expense', '#06B6D4'),
        ('Saúde', 'expense', '#10B981'),
        # Receitas - categorias básicas
        ('Salário', 'income', '#059669'),
        ('Trabalho Extra', 'income', '#047857'),
        ('Outros', 'income', '#6B7280'),
    ]
    
    for name, type_, color in default_categories:
        # Verificar se já existe
        cursor.execute('SELECT id FROM categories WHERE name = ?', (name,))
        if not cursor.fetchone():
            # Se não existe, inserir (usando a estrutura atual da tabela)
            cursor.execute('''
            INSERT INTO categories (name, type, color, created_at) 
            VALUES (?, ?, ?, datetime('now'))
            ''', (name, type_, color))
    
    # Tabelas criadas - dados serão inseridos apenas quando o usuário adicionar
    
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
    """Buscar categorias com estatísticas reais"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Buscar todas as categorias
    cursor.execute("SELECT id, name, type, color FROM categories ORDER BY type, name")
    categories_data = cursor.fetchall()
    
    categories = []
    for cat_data in categories_data:
        cat_id, name, type_, color = cat_data
        
        # Calcular estatísticas reais para cada categoria
        cursor.execute(
            "SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM transactions WHERE category = ?",
            (name,)
        )
        count, total = cursor.fetchone()
        
        categories.append({
            "id": str(cat_id),
            "name": name,
            "type": type_,
            "color": color,
            "transactionCount": count or 0,
            "totalAmount": float(total or 0)
        })
    
    conn.close()
    return {"status": "success", "data": categories}

@app.post("/api/v1/categories")
async def create_category(request: dict):
    """Criar nova categoria"""
    try:
        name = request.get("name")
        type_ = request.get("type")
        color = request.get("color", "#3B82F6")
        
        if not name or not type_:
            return {"status": "error", "message": "Nome e tipo são obrigatórios"}
        
        if type_ not in ["income", "expense"]:
            return {"status": "error", "message": "Tipo deve ser 'income' ou 'expense'"}
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verificar se categoria já existe
        cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
        if cursor.fetchone():
            conn.close()
            return {"status": "error", "message": "Categoria já existe"}
        
        # Inserir nova categoria
        cursor.execute(
            "INSERT INTO categories (name, type, color, is_default) VALUES (?, ?, ?, 0)",
            (name, type_, color)
        )
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Categoria criada com sucesso"}
        
    except Exception as e:
        print(f"Erro ao criar categoria: {e}")
        return {"status": "error", "message": "Erro interno do servidor"}

@app.delete("/api/v1/categories/{category_id}")
async def delete_category(category_id: int):
    """Excluir categoria (apenas categorias não-padrão)"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verificar se é categoria padrão (não pode excluir as 4 fixas)
        cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return {"status": "error", "message": "Categoria não encontrada"}
        
        category_name = result[0]
        if category_name in ['Alimentação', 'Lazer', 'Transporte', 'Saúde']:
            conn.close()
            return {"status": "error", "message": "Não é possível excluir categorias padrão"}
        
        # Excluir categoria
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        
        conn.commit()
        conn.close()
        
        return {"status": "success", "message": "Categoria excluída com sucesso"}
        
    except Exception as e:
        print(f"Erro ao excluir categoria: {e}")
        return {"status": "error", "message": "Erro interno do servidor"}

# Endpoints de Investimentos
@app.get("/api/v1/investments")
async def get_investments():
    """Buscar todos os investimentos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM investments ORDER BY purchase_date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    investments = []
    for row in rows:
        profit_loss = row[4] - row[3]  # current_amount - initial_amount
        profit_percentage = (profit_loss / row[3]) * 100 if row[3] > 0 else 0
        
        investments.append({
            "id": str(row[0]),
            "name": row[1],
            "type": row[2],
            "initial_amount": row[3],
            "current_amount": row[4],
            "purchase_date": row[5],
            "description": row[6] if row[6] else "",
            "status": row[7] if len(row) > 7 else "active",
            "profit_loss": profit_loss,
            "profit_percentage": round(profit_percentage, 2)
        })
    
    return {"status": "success", "data": investments}

@app.post("/api/v1/investments")
async def create_investment(investment: InvestmentCreate):
    """Criar novo investimento"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(
        """INSERT INTO investments (name, type, initial_amount, current_amount, purchase_date, description) 
           VALUES (?, ?, ?, ?, ?, ?)""",
        (investment.name, investment.type, investment.initial_amount, 
         investment.current_amount, investment.purchase_date, investment.description)
    )
    
    investment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "status": "success", 
        "data": {
            "id": str(investment_id),
            "name": investment.name,
            "type": investment.type,
            "initial_amount": investment.initial_amount,
            "current_amount": investment.current_amount,
            "purchase_date": investment.purchase_date,
            "description": investment.description,
            "status": "active"
        }
    }

@app.get("/api/v1/investments/{investment_id}")
async def get_investment(investment_id: int):
    """Buscar investimento por ID"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM investments WHERE id = ?", (investment_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    
    profit_loss = row[4] - row[3]  # current_amount - initial_amount
    profit_percentage = (profit_loss / row[3]) * 100 if row[3] > 0 else 0
    
    return {
        "status": "success",
        "data": {
            "id": str(row[0]),
            "name": row[1],
            "type": row[2],
            "initial_amount": row[3],
            "current_amount": row[4],
            "purchase_date": row[5],
            "description": row[6] if row[6] else "",
            "status": row[7] if len(row) > 7 else "active",
            "profit_loss": profit_loss,
            "profit_percentage": round(profit_percentage, 2)
        }
    }

@app.put("/api/v1/investments/{investment_id}")
async def update_investment(investment_id: int, investment: InvestmentUpdate):
    """Atualizar um investimento"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Verificar se investimento existe
    cursor.execute("SELECT * FROM investments WHERE id = ?", (investment_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    
    # Construir query de update dinâmica
    update_fields = []
    update_values = []
    
    if investment.name is not None:
        update_fields.append("name = ?")
        update_values.append(investment.name)
    if investment.type is not None:
        update_fields.append("type = ?")
        update_values.append(investment.type)
    if investment.initial_amount is not None:
        update_fields.append("initial_amount = ?")
        update_values.append(investment.initial_amount)
    if investment.current_amount is not None:
        update_fields.append("current_amount = ?")
        update_values.append(investment.current_amount)
    if investment.purchase_date is not None:
        update_fields.append("purchase_date = ?")
        update_values.append(investment.purchase_date)
    if investment.description is not None:
        update_fields.append("description = ?")
        update_values.append(investment.description)
    if investment.status is not None:
        update_fields.append("status = ?")
        update_values.append(investment.status)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    
    update_values.append(investment_id)
    query = f"UPDATE investments SET {', '.join(update_fields)} WHERE id = ?"
    
    cursor.execute(query, update_values)
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Investimento atualizado com sucesso"}

@app.delete("/api/v1/investments/{investment_id}")
async def delete_investment(investment_id: int):
    """Deletar um investimento"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM investments WHERE id = ?", (investment_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Investimento não encontrado")
    
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Investimento deletado com sucesso"}

@app.get("/api/v1/investments/stats")
async def get_investment_stats():
    """Estatísticas dos investimentos"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Total investido
    cursor.execute("SELECT SUM(initial_amount) FROM investments WHERE status = 'active'")
    total_invested = cursor.fetchone()[0] or 0
    
    # Valor atual total
    cursor.execute("SELECT SUM(current_amount) FROM investments WHERE status = 'active'")
    total_current = cursor.fetchone()[0] or 0
    
    # Quantidade de investimentos
    cursor.execute("SELECT COUNT(*) FROM investments WHERE status = 'active'")
    investment_count = cursor.fetchone()[0] or 0
    
    # Maior rentabilidade
    cursor.execute("""
        SELECT name, ((current_amount - initial_amount) / initial_amount * 100) as profit_percentage
        FROM investments 
        WHERE status = 'active' AND initial_amount > 0
        ORDER BY profit_percentage DESC 
        LIMIT 1
    """)
    best_investment = cursor.fetchone()
    
    conn.close()
    
    profit_loss = total_current - total_invested
    profit_percentage = (profit_loss / total_invested * 100) if total_invested > 0 else 0
    
    return {
        "status": "success",
        "data": {
            "total_invested": total_invested,
            "total_current": total_current,
            "profit_loss": profit_loss,
            "profit_percentage": round(profit_percentage, 2),
            "investment_count": investment_count,
            "best_investment": {
                "name": best_investment[0] if best_investment else None,
                "profit_percentage": round(best_investment[1], 2) if best_investment else 0
            }
        }
    }

# ======================
# ENDPOINTS DE METAS
# ======================

@app.get("/api/v1/goals")
async def get_goals():
    """Buscar todas as metas"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals ORDER BY start_date DESC")
    rows = cursor.fetchall()
    conn.close()
    
    goals = []
    for row in rows:
        progress = (row[4] / row[3] * 100) if row[3] > 0 else 0  # current_amount / target_amount
        goals.append({
            "id": str(row[0]),
            "title": row[1],
            "goal_type": row[2],
            "target_amount": row[3],
            "current_amount": row[4],
            "period_type": row[5],
            "start_date": row[6],
            "end_date": row[7],
            "category_id": row[8],
            "status": row[9] if len(row) > 9 else "active",
            "progress_percentage": round(progress, 2)
        })
    
    return {"status": "success", "data": goals}

@app.post("/api/v1/goals")
async def create_goal(goal: GoalCreate):
    """Criar nova meta"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO goals (title, goal_type, target_amount, current_amount, period_type, start_date, end_date, category_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        goal.title,
        goal.goal_type,
        goal.target_amount,
        goal.current_amount,
        goal.period_type,
        goal.start_date,
        goal.end_date,
        goal.category_id
    ))
    
    goal_id = cursor.lastrowid
    conn.commit()
    
    # Buscar a meta criada
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        progress = (row[4] / row[3] * 100) if row[3] > 0 else 0
        return {
            "status": "success",
            "message": "Meta criada com sucesso",
            "data": {
                "id": str(row[0]),
                "title": row[1],
                "goal_type": row[2],
                "target_amount": row[3],
                "current_amount": row[4],
                "period_type": row[5],
                "start_date": row[6],
                "end_date": row[7],
                "category_id": row[8],
                "status": row[9],
                "progress_percentage": round(progress, 2)
            }
        }

@app.get("/api/v1/goals/{goal_id}")
async def get_goal(goal_id: str):
    """Buscar meta por ID"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    
    progress = (row[4] / row[3] * 100) if row[3] > 0 else 0
    return {
        "status": "success",
        "data": {
            "id": str(row[0]),
            "title": row[1],
            "goal_type": row[2],
            "target_amount": row[3],
            "current_amount": row[4],
            "period_type": row[5],
            "start_date": row[6],
            "end_date": row[7],
            "category_id": row[8],
            "status": row[9],
            "progress_percentage": round(progress, 2)
        }
    }

@app.put("/api/v1/goals/{goal_id}")
async def update_goal(goal_id: str, goal: GoalUpdate):
    """Atualizar meta"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Verificar se a meta existe
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    
    # Construir query de atualização dinamicamente
    update_fields = []
    update_values = []
    
    if goal.title is not None:
        update_fields.append("title = ?")
        update_values.append(goal.title)
    if goal.goal_type is not None:
        update_fields.append("goal_type = ?")
        update_values.append(goal.goal_type)
    if goal.target_amount is not None:
        update_fields.append("target_amount = ?")
        update_values.append(goal.target_amount)
    if goal.current_amount is not None:
        update_fields.append("current_amount = ?")
        update_values.append(goal.current_amount)
    if goal.period_type is not None:
        update_fields.append("period_type = ?")
        update_values.append(goal.period_type)
    if goal.start_date is not None:
        update_fields.append("start_date = ?")
        update_values.append(goal.start_date)
    if goal.end_date is not None:
        update_fields.append("end_date = ?")
        update_values.append(goal.end_date)
    if goal.category_id is not None:
        update_fields.append("category_id = ?")
        update_values.append(goal.category_id)
    if goal.status is not None:
        update_fields.append("status = ?")
        update_values.append(goal.status)
    
    if not update_fields:
        conn.close()
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    
    update_values.append(goal_id)
    query = f"UPDATE goals SET {', '.join(update_fields)} WHERE id = ?"
    
    cursor.execute(query, update_values)
    conn.commit()
    
    # Buscar meta atualizada
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        progress = (row[4] / row[3] * 100) if row[3] > 0 else 0
        return {
            "status": "success",
            "message": "Meta atualizada com sucesso",
            "data": {
                "id": str(row[0]),
                "title": row[1],
                "goal_type": row[2],
                "target_amount": row[3],
                "current_amount": row[4],
                "period_type": row[5],
                "start_date": row[6],
                "end_date": row[7],
                "category_id": row[8],
                "status": row[9],
                "progress_percentage": round(progress, 2)
            }
        }

@app.delete("/api/v1/goals/{goal_id}")
async def delete_goal(goal_id: str):
    """Deletar meta"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Verificar se a meta existe
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    
    # Deletar meta
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Meta deletada com sucesso"}

@app.get("/api/v1/goals/stats")
async def get_goals_stats():
    """Estatísticas das metas"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Total de metas ativas
    cursor.execute("SELECT COUNT(*) FROM goals WHERE status = 'active'")
    total_goals = cursor.fetchone()[0] or 0
    
    # Total target amount
    cursor.execute("SELECT SUM(target_amount) FROM goals WHERE status = 'active'")
    total_target = cursor.fetchone()[0] or 0
    
    # Total current amount
    cursor.execute("SELECT SUM(current_amount) FROM goals WHERE status = 'active'")
    total_current = cursor.fetchone()[0] or 0
    
    # Metas concluídas (100% ou mais)
    cursor.execute("SELECT COUNT(*) FROM goals WHERE status = 'active' AND current_amount >= target_amount")
    completed_goals = cursor.fetchone()[0] or 0
    
    # Meta com maior progresso
    cursor.execute("""
        SELECT title, (current_amount / target_amount * 100) as progress
        FROM goals 
        WHERE status = 'active' AND target_amount > 0
        ORDER BY progress DESC 
        LIMIT 1
    """)
    best_goal = cursor.fetchone()
    
    # Progresso médio
    cursor.execute("""
        SELECT AVG(current_amount / target_amount * 100) 
        FROM goals 
        WHERE status = 'active' AND target_amount > 0
    """)
    avg_progress = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "status": "success",
        "data": {
            "total_goals": total_goals,
            "completed_goals": completed_goals,
            "total_target_amount": total_target,
            "total_current_amount": total_current,
            "average_progress": round(avg_progress, 2),
            "best_goal": {
                "title": best_goal[0] if best_goal else None,
                "progress": round(best_goal[1], 2) if best_goal else 0
            }
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando RuViPay API Simplificada...")
    print("📁 Banco de dados: SQLite (ruviopay.db)")
    print("🌐 Acesse: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    uvicorn.run("main_simple_fixed:app", host="0.0.0.0", port=8000, reload=True)