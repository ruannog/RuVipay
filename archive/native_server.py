"""
Backend ultra-simplificado usando apenas Python built-in e HTTP simples
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from urllib.parse import urlparse, parse_qs
import threading
from datetime import datetime

class RuVioPayHandler(BaseHTTPRequestHandler):
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        response = {"status": "error", "message": "Endpoint not found"}
        
        if path == '/':
            response = {
                "message": "🚀 RuViPay API está funcionando!",
                "version": "1.0.0",
                "status": "running"
            }
        elif path == '/api/v1/health':
            response = {"status": "healthy"}
        elif path == '/api/v1/transactions':
            response = self.get_transactions()
        elif path == '/api/v1/investments':
            response = self.get_investments()
        elif path == '/api/v1/goals':
            response = self.get_goals()
        elif path == '/api/v1/dashboard/stats':
            response = self.get_dashboard_stats()
        elif path == '/api/v1/categories':
            response = self.get_categories()
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self._send_cors_headers()
        self.end_headers()
        
        response = {"status": "error", "message": "Endpoint not found"}
        
        if path == '/api/v1/transactions':
            response = self.create_transaction(data)
        elif path == '/api/v1/investments':
            response = self.create_investment(data)
        elif path == '/api/v1/goals':
            response = self.create_goal(data)
        
        self.wfile.write(json.dumps(response).encode())
    
    def get_transactions(self):
        conn = sqlite3.connect('ruviopay.db')
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
                "status": "completed"
            })
        
        return {"data": transactions, "status": "success"}
    
    def create_transaction(self, data):
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
            (data.get('description', ''), data.get('amount', 0), 
             data.get('type', ''), data.get('category', ''), data.get('date', ''))
        )
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "data": {
                "id": transaction_id,
                "description": data.get('description', ''),
                "amount": data.get('amount', 0),
                "type": data.get('type', ''),
                "category": data.get('category', ''),
                "date": data.get('date', ''),
                "status": "completed"
            }
        }
    
    def get_investments(self):
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM investments")
        rows = cursor.fetchall()
        conn.close()
        
        investments = []
        for row in rows:
            profit_loss = row[4] - row[3]
            profit_loss_percentage = (profit_loss / row[3] * 100) if row[3] > 0 else 0
            
            investments.append({
                "id": row[0],
                "name": row[1],
                "investment_type": row[2],
                "amount_invested": row[3],
                "current_value": row[4],
                "purchase_date": row[5],
                "profit_loss": profit_loss,
                "profit_loss_percentage": profit_loss_percentage
            })
        
        return {"data": investments, "status": "success"}
    
    def create_investment(self, data):
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO investments (name, investment_type, amount_invested, current_value, purchase_date) VALUES (?, ?, ?, ?, ?)",
            (data.get('name', ''), data.get('investment_type', ''), 
             data.get('amount_invested', 0), data.get('current_value', 0), data.get('purchase_date', ''))
        )
        
        investment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        profit_loss = data.get('current_value', 0) - data.get('amount_invested', 0)
        profit_loss_percentage = (profit_loss / data.get('amount_invested', 1) * 100) if data.get('amount_invested', 0) > 0 else 0
        
        return {
            "status": "success",
            "data": {
                "id": investment_id,
                "name": data.get('name', ''),
                "investment_type": data.get('investment_type', ''),
                "amount_invested": data.get('amount_invested', 0),
                "current_value": data.get('current_value', 0),
                "purchase_date": data.get('purchase_date', ''),
                "profit_loss": profit_loss,
                "profit_loss_percentage": profit_loss_percentage
            }
        }
    
    def get_goals(self):
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goals")
        rows = cursor.fetchall()
        conn.close()
        
        goals = []
        for row in rows:
            progress_percentage = (row[4] / row[3] * 100) if row[3] > 0 else 0
            remaining_amount = max(row[3] - row[4], 0)
            is_completed = row[4] >= row[3]
            
            goals.append({
                "id": row[0],
                "title": row[1],
                "goal_type": row[2],
                "target_amount": row[3],
                "current_amount": row[4],
                "period_type": row[5],
                "start_date": row[6],
                "end_date": row[7],
                "progress_percentage": progress_percentage,
                "remaining_amount": remaining_amount,
                "is_completed": is_completed
            })
        
        return {"data": goals, "status": "success"}
    
    def create_goal(self, data):
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO goals (title, goal_type, target_amount, current_amount, period_type, start_date, end_date, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (data.get('title', ''), data.get('goal_type', ''), data.get('target_amount', 0),
             data.get('current_amount', 0), data.get('period_type', ''), 
             data.get('start_date', ''), data.get('end_date', ''), data.get('category_id'))
        )
        
        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        progress_percentage = (data.get('current_amount', 0) / data.get('target_amount', 1) * 100) if data.get('target_amount', 0) > 0 else 0
        remaining_amount = max(data.get('target_amount', 0) - data.get('current_amount', 0), 0)
        is_completed = data.get('current_amount', 0) >= data.get('target_amount', 0)
        
        return {
            "status": "success",
            "data": {
                "id": goal_id,
                "title": data.get('title', ''),
                "goal_type": data.get('goal_type', ''),
                "target_amount": data.get('target_amount', 0),
                "current_amount": data.get('current_amount', 0),
                "period_type": data.get('period_type', ''),
                "start_date": data.get('start_date', ''),
                "end_date": data.get('end_date', ''),
                "progress_percentage": progress_percentage,
                "remaining_amount": remaining_amount,
                "is_completed": is_completed
            }
        }
    
    def get_dashboard_stats(self):
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
        total_income = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
        total_expense = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0] or 0
        
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
    
    def get_categories(self):
        categories = [
            # Categorias de Receita
            {"id": "1", "name": "Receita", "type": "income", "color": "#10B981", "transactionCount": 1, "totalAmount": 3500},
            {"id": "2", "name": "Salário", "type": "income", "color": "#059669", "transactionCount": 1, "totalAmount": 1200},
            {"id": "3", "name": "Freelance", "type": "income", "color": "#047857", "transactionCount": 1, "totalAmount": 45.30},
            # Categorias de Despesa (como você pediu)
            {"id": "4", "name": "Lazer", "type": "expense", "color": "#8B5CF6", "transactionCount": 1, "totalAmount": 350.00},
            {"id": "5", "name": "Alimentação", "type": "expense", "color": "#EF4444", "transactionCount": 1, "totalAmount": 280.50},
            {"id": "6", "name": "Transporte", "type": "expense", "color": "#F97316", "transactionCount": 1, "totalAmount": 420.00},
            {"id": "7", "name": "Saúde", "type": "expense", "color": "#06B6D4", "transactionCount": 1, "totalAmount": 280.00},
        ]
        
        return {"status": "success", "data": categories}

def init_database():
    """Inicializar banco de dados SQLite"""
    conn = sqlite3.connect('ruviopay.db')
    cursor = conn.cursor()
    
    # Criar tabelas
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
    
    # Inserir dados de exemplo
    cursor.execute("SELECT COUNT(*) FROM transactions")
    if cursor.fetchone()[0] == 0:
        sample_transactions = [
            ("Salário Janeiro", 3500.0, "income", "Salário", "2024-01-15"),
            ("Supermercado", 280.50, "expense", "Alimentação", "2024-01-14"),
            ("Projeto Freelance", 1200.0, "income", "Freelance", "2024-01-12"),
            ("Uber", 35.00, "expense", "Transporte", "2024-01-11"),
            ("Cinema", 45.30, "expense", "Lazer", "2024-01-10"),
            ("Farmácia", 80.00, "expense", "Saúde", "2024-01-09"),
            ("Restaurante", 120.00, "expense", "Alimentação", "2024-01-08"),
            ("Netflix", 29.90, "expense", "Lazer", "2024-01-07"),
        ]
        cursor.executemany(
            "INSERT INTO transactions (description, amount, type, category, date) VALUES (?, ?, ?, ?, ?)",
            sample_transactions
        )
    
    conn.commit()
    conn.close()

def run_server():
    print("🚀 Inicializando banco de dados...")
    init_database()
    
    print("🚀 Iniciando RuViPay API na porta 8000...")
    server = HTTPServer(('localhost', 8000), RuVioPayHandler)
    print("✅ Servidor rodando em http://localhost:8000")
    print("📖 Acesse http://localhost:8000 para testar")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado pelo usuário")
        server.server_close()

if __name__ == "__main__":
    run_server()