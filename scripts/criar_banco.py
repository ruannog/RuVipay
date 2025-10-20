import sqlite3
from pathlib import Path

def criar_banco_simples():
    """Cria o banco SQLite com as tabelas básicas"""
    
    db_path = Path("backend/ruviopay.db")
    
    # Conectar ao banco (cria se não existir)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Criando banco de dados SQLite...")
    
    # Criar tabela Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT 1,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Criar tabela Categories
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL,
        description VARCHAR(255),
        type VARCHAR(20) NOT NULL CHECK (type IN ('income', 'expense')),
        color VARCHAR(7) DEFAULT '#3B82F6',
        icon VARCHAR(50) DEFAULT '💰',
        is_active BOOLEAN DEFAULT 1,
        user_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Criar tabela Transactions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description VARCHAR(255) NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        type VARCHAR(20) NOT NULL CHECK (type IN ('income', 'expense')),
        date DATETIME NOT NULL,
        notes TEXT,
        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')
    
    # Inserir usuário de exemplo
    cursor.execute('''
    INSERT OR IGNORE INTO users (id, username, email, full_name, hashed_password)
    VALUES (1, 'admin', 'admin@ruviopay.com', 'Administrador', 'hashed_password_example')
    ''')
    
    # Inserir categorias de exemplo
    categorias_exemplo = [
        (1, 'Salário', 'Salário mensal', 'income', '#10B981', '💼', 1, 1),
        (2, 'Freelance', 'Trabalhos freelancer', 'income', '#059669', '💻', 1, 1),
        (3, 'Alimentação', 'Gastos com comida', 'expense', '#EF4444', '🍕', 1, 1),
        (4, 'Transporte', 'Gastos com transporte', 'expense', '#DC2626', '🚗', 1, 1),
        (5, 'Moradia', 'Aluguel e contas da casa', 'expense', '#B91C1C', '🏠', 1, 1),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO categories (id, name, description, type, color, icon, is_active, user_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', categorias_exemplo)
    
    # Inserir transações de exemplo
    from datetime import datetime, timedelta
    
    transacoes_exemplo = [
        (1, 'Salário Outubro', 5000.00, 'income', '2025-10-01', 'Salário mensal', 1, 1),
        (2, 'Freelance Website', 1500.00, 'income', '2025-10-05', 'Desenvolvimento de site', 1, 2),
        (3, 'Supermercado', 350.00, 'expense', '2025-10-02', 'Compras mensais', 1, 3),
        (4, 'Uber', 45.00, 'expense', '2025-10-03', 'Transporte para trabalho', 1, 4),
        (5, 'Aluguel', 1200.00, 'expense', '2025-10-01', 'Aluguel mensal', 1, 5),
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO transactions (id, description, amount, type, date, notes, user_id, category_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', transacoes_exemplo)
    
    # Confirmar e fechar
    conn.commit()
    conn.close()
    
    print(f"✅ Banco de dados criado: {db_path.absolute()}")
    print("✅ Tabelas criadas: users, categories, transactions")
    print("✅ Dados de exemplo inseridos")
    
if __name__ == "__main__":
    criar_banco_simples()