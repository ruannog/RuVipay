#!/usr/bin/env python3
"""
Script para atualizar a estrutura do banco de dados existente.
Adiciona a nova tabela de investimentos com a estrutura correta.
"""

import sqlite3
import os

def update_database():
    # Caminho do banco de dados
    db_path = "ruviopay.db"
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar se a tabela investments existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='investments'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("Tabela 'investments' existe. Removendo tabela antiga...")
            cursor.execute("DROP TABLE investments")
        
        # Criar nova tabela de investimentos com a estrutura correta
        cursor.execute("""
            CREATE TABLE investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(50) NOT NULL,
                initial_amount DECIMAL(10, 2) NOT NULL,
                current_amount DECIMAL(10, 2) NOT NULL,
                purchase_date DATE NOT NULL,
                description TEXT,
                status VARCHAR(20) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("Nova tabela 'investments' criada com sucesso!")
        
        print("Tabela de investimentos criada com sucesso! (sem dados de exemplo)")
        
        # Verificar se a tabela transactions existe, caso contrário criar
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        if not cursor.fetchone():
            print("Criando tabela 'transactions'...")
            cursor.execute("""
                CREATE TABLE transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description VARCHAR(200) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    type VARCHAR(10) NOT NULL CHECK (type IN ('income', 'expense')),
                    category VARCHAR(50) NOT NULL,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("Tabela 'transactions' criada com sucesso! (sem dados de exemplo)")
        
        # Commit das mudanças
        conn.commit()
        print("\nBanco de dados atualizado com sucesso!")
        
        # Mostrar estatísticas
        cursor.execute("SELECT COUNT(*) FROM investments")
        inv_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        trans_count = cursor.fetchone()[0]
        
        print(f"Total de investimentos: {inv_count}")
        print(f"Total de transações: {trans_count}")
        
    except Exception as e:
        print(f"Erro ao atualizar banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    update_database()