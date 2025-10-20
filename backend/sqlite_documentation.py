"""
DOCUMENTAÇÃO COMPLETA DO SQLite NO RUVIOPAY
===========================================

Este arquivo explica como o SQLite está implementado no sistema RuVioPay
"""

import sqlite3
import os

def show_database_structure():
    """Mostra a estrutura completa do banco SQLite"""
    
    print("=" * 80)
    print("🗄️  SQLITE NO RUVIOPAY - DOCUMENTAÇÃO TÉCNICA")
    print("=" * 80)
    
    # Verificar se existe o banco
    db_path = "ruviopay.db"
    if not os.path.exists(db_path):
        print("❌ Banco de dados não encontrado!")
        return
        
    print(f"📍 Localização do Banco: {os.path.abspath(db_path)}")
    print(f"📏 Tamanho do arquivo: {os.path.getsize(db_path)} bytes")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n" + "=" * 80)
        print("📋 ESTRUTURA DAS TABELAS")
        print("=" * 80)
        
        # Listar todas as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n🔹 TABELA: {table_name.upper()}")
            print("-" * 50)
            
            # Obter informações das colunas
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print(f"{'Campo':<20} {'Tipo':<15} {'Null':<6} {'Padrão':<15} {'Chave'}")
            print("-" * 70)
            
            for col in columns:
                field_name = col[1]
                field_type = col[2]
                not_null = "NÃO" if col[3] else "SIM"
                default_val = col[4] if col[4] else "-"
                primary_key = "PK" if col[5] else "-"
                
                print(f"{field_name:<20} {field_type:<15} {not_null:<6} {default_val:<15} {primary_key}")
            
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\n📊 Total de registros: {count}")
        
        print("\n" + "=" * 80)
        print("🔍 COMANDOS SQL USADOS NO SISTEMA")
        print("=" * 80)
        
        sql_commands = {
            "CRIAR TABELAS": """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'completed'
            );
            
            CREATE TABLE IF NOT EXISTS investments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                investment_type TEXT NOT NULL,
                amount_invested REAL NOT NULL,
                current_value REAL NOT NULL,
                purchase_date TEXT NOT NULL
            );
            
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
            );
            """,
            
            "INSERIR DADOS": """
            -- Inserir transação
            INSERT INTO transactions (description, amount, type, category, date) 
            VALUES ('Salário', 3500.0, 'income', 'Salário', '2024-01-15');
            
            -- Inserir investimento
            INSERT INTO investments (name, investment_type, amount_invested, current_value, purchase_date)
            VALUES ('ITUB4', 'acao', 1000.0, 1150.0, '2024-01-10');
            
            -- Inserir meta
            INSERT INTO goals (title, goal_type, target_amount, current_amount, period_type, start_date, end_date)
            VALUES ('Reserva Emergency', 'economia', 10000.0, 2500.0, 'anual', '2024-01-01', '2024-12-31');
            """,
            
            "CONSULTAR DADOS": """
            -- Listar transações por tipo
            SELECT * FROM transactions WHERE type = 'income' ORDER BY date DESC;
            
            -- Calcular saldo total
            SELECT 
                (SELECT SUM(amount) FROM transactions WHERE type = 'income') as receitas,
                (SELECT SUM(amount) FROM transactions WHERE type = 'expense') as despesas,
                (SELECT SUM(amount) FROM transactions WHERE type = 'income') - 
                (SELECT SUM(amount) FROM transactions WHERE type = 'expense') as saldo;
            
            -- Investimentos com lucro/prejuízo
            SELECT name, 
                   amount_invested, 
                   current_value,
                   (current_value - amount_invested) as profit_loss,
                   ROUND(((current_value - amount_invested) / amount_invested) * 100, 2) as percentage
            FROM investments;
            """,
            
            "ATUALIZAR DADOS": """
            -- Atualizar valor atual do investimento
            UPDATE investments 
            SET current_value = 1200.0 
            WHERE id = 1;
            
            -- Atualizar valor atual da meta
            UPDATE goals 
            SET current_amount = current_amount + 500.0 
            WHERE id = 1;
            """,
            
            "DELETAR DADOS": """
            -- Deletar transação
            DELETE FROM transactions WHERE id = 1;
            
            -- Deletar investimento
            DELETE FROM investments WHERE id = 1;
            """
        }
        
        for category, commands in sql_commands.items():
            print(f"\n🔸 {category}:")
            print("-" * 40)
            print(commands.strip())
        
        print("\n" + "=" * 80)
        print("🏗️  COMO O SQLITE É USADO NO CÓDIGO")
        print("=" * 80)
        
        implementation_details = """
        1. CONEXÃO COM O BANCO:
           - Arquivo: native_server.py
           - Método: sqlite3.connect('ruviopay.db')
           - Tipo: Arquivo local SQLite
        
        2. OPERAÇÕES CRUD:
           ✅ CREATE: Inserir novos registros via POST /api/v1/[endpoint]
           ✅ READ: Listar dados via GET /api/v1/[endpoint]  
           ✅ UPDATE: Atualizar via PUT /api/v1/[endpoint]/{id}
           ✅ DELETE: Deletar via DELETE /api/v1/[endpoint]/{id}
        
        3. ENDPOINTS QUE USAM O BANCO:
           📊 GET /api/v1/transactions - Lista todas as transações
           💰 POST /api/v1/transactions - Cria nova transação  
           📈 GET /api/v1/investments - Lista investimentos
           💎 POST /api/v1/investments - Cria novo investimento
           🎯 GET /api/v1/goals - Lista metas
           🏆 POST /api/v1/goals - Cria nova meta
           📋 GET /api/v1/dashboard/stats - Estatísticas calculadas
        
        4. VANTAGENS DO SQLITE NESTE PROJETO:
           ✅ Zero configuração - arquivo local
           ✅ Não precisa de servidor de banco 
           ✅ Ideal para desenvolvimento e projetos pequenos
           ✅ Suporte completo ao SQL padrão
           ✅ Transações ACID
           ✅ Backup simples (copiar arquivo .db)
        
        5. FLUXO DE DADOS:
           Frontend React → API HTTP → SQLite → Resposta JSON → Frontend
           
           Exemplo completo:
           1. Usuário clica "Nova Transação" no frontend
           2. Modal abre com formulário
           3. Usuário preenche e clica "Salvar"
           4. Frontend faz POST para /api/v1/transactions
           5. Backend recebe dados e executa INSERT no SQLite
           6. SQLite salva no arquivo ruviopay.db
           7. Backend retorna sucesso para frontend
           8. Frontend atualiza a lista automaticamente
        """
        
        print(implementation_details)
        
        conn.close()
        
        print("\n" + "=" * 80)
        print("🎯 RESUMO TÉCNICO")
        print("=" * 80)
        print("🔹 Banco: SQLite (arquivo local)")
        print("🔹 Arquivo: ruviopay.db")  
        print("🔹 Tabelas: 3 (transactions, investments, goals)")
        print("🔹 Linguagem: Python com módulo sqlite3")
        print("🔹 Interface: API REST HTTP")
        print("🔹 Frontend: React consumindo APIs")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Erro ao analisar banco: {e}")

def show_live_data():
    """Mostra dados em tempo real do banco"""
    print("\n" + "🔴 DADOS EM TEMPO REAL")
    print("=" * 50)
    
    try:
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        # Últimas transações
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT 3")
        transactions = cursor.fetchall()
        
        print("💰 ÚLTIMAS TRANSAÇÕES:")
        for t in transactions:
            emoji = "💚" if t[3] == 'income' else "❤️"
            print(f"   {emoji} {t[1]} - R$ {t[2]:,.2f} ({t[4]})")
        
        # Total de registros
        cursor.execute("SELECT COUNT(*) FROM transactions")
        trans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM investments")  
        invest_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM goals")
        goals_count = cursor.fetchone()[0]
        
        print(f"\n📊 TOTAIS: {trans_count} transações, {invest_count} investimentos, {goals_count} metas")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    show_database_structure()
    show_live_data()