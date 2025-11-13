#!/usr/bin/env python3
"""
Script para limpar dados de exemplo do banco de dados.
Remove todos os registros das tabelas de transações e investimentos.
"""

import sqlite3
import os

def clean_database():
    # Caminho do banco de dados
    db_path = "ruviopay.db"
    
    if not os.path.exists(db_path):
        print(f"Banco de dados {db_path} não encontrado!")
        return
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Limpando dados de exemplo do banco de dados...")
        
        # Contar registros antes da limpeza
        cursor.execute("SELECT COUNT(*) FROM transactions")
        trans_before = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM investments")
        inv_before = cursor.fetchone()[0]
        
        print(f"Transações encontradas: {trans_before}")
        print(f"Investimentos encontrados: {inv_before}")
        
        # Limpar tabelas
        cursor.execute("DELETE FROM transactions")
        cursor.execute("DELETE FROM investments")
        
        # Reset dos IDs para começar do 1 novamente
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='investments'")
        
        # Commit das mudanças
        conn.commit()
        
        print("\n✅ Dados removidos com sucesso!")
        print("📊 Agora as tabelas estão vazias e prontas para receber os dados do usuário.")
        
        # Verificar se está vazio
        cursor.execute("SELECT COUNT(*) FROM transactions")
        trans_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM investments")
        inv_after = cursor.fetchone()[0]
        
        print(f"\n📈 Transações restantes: {trans_after}")
        print(f"💰 Investimentos restantes: {inv_after}")
        
    except Exception as e:
        print(f"❌ Erro ao limpar banco de dados: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    clean_database()