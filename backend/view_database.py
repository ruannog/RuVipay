"""
Visualizador do banco de dados RuVioPay
Execute este script para ver todos os dados salvos no banco
"""
import sqlite3
import json
from datetime import datetime

def view_database():
    """Visualizar todos os dados do banco"""
    
    try:
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        print("=" * 60)
        print("🗄️  BANCO DE DADOS RUVIOPAY")
        print("=" * 60)
        
        # ===== TRANSAÇÕES =====
        print("\n💰 TRANSAÇÕES:")
        print("-" * 40)
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        transactions = cursor.fetchall()
        
        if transactions:
            print(f"{'ID':<3} {'Descrição':<20} {'Valor':<10} {'Tipo':<8} {'Categoria':<15} {'Data'}")
            print("-" * 70)
            
            total_income = 0
            total_expense = 0
            
            for row in transactions:
                amount = row[2]
                if row[3] == 'income':
                    total_income += amount
                    value_str = f"+R$ {amount:,.2f}"
                else:
                    total_expense += amount
                    value_str = f"-R$ {amount:,.2f}"
                
                print(f"{row[0]:<3} {row[1]:<20} {value_str:<10} {row[3]:<8} {row[4]:<15} {row[5]}")
            
            print("-" * 70)
            print(f"💚 Total Receitas: R$ {total_income:,.2f}")
            print(f"❤️  Total Despesas: R$ {total_expense:,.2f}")
            print(f"💙 Saldo: R$ {(total_income - total_expense):,.2f}")
        else:
            print("   Nenhuma transação encontrada")
        
        # ===== INVESTIMENTOS =====
        print("\n📈 INVESTIMENTOS:")
        print("-" * 40)
        cursor.execute("SELECT * FROM investments")
        investments = cursor.fetchall()
        
        if investments:
            print(f"{'ID':<3} {'Nome':<15} {'Tipo':<10} {'Investido':<12} {'Atual':<12} {'Resultado':<12} {'%':<8}")
            print("-" * 80)
            
            total_invested = 0
            total_current = 0
            
            for row in investments:
                invested = row[3]
                current = row[4]
                profit_loss = current - invested
                percentage = (profit_loss / invested * 100) if invested > 0 else 0
                
                total_invested += invested
                total_current += current
                
                result_str = f"+R$ {profit_loss:,.2f}" if profit_loss >= 0 else f"-R$ {abs(profit_loss):,.2f}"
                perc_str = f"+{percentage:.1f}%" if percentage >= 0 else f"{percentage:.1f}%"
                
                print(f"{row[0]:<3} {row[1]:<15} {row[2]:<10} R$ {invested:,.2f} R$ {current:,.2f} {result_str:<12} {perc_str:<8}")
            
            total_profit_loss = total_current - total_invested
            total_percentage = (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
            
            print("-" * 80)
            print(f"💰 Total Investido: R$ {total_invested:,.2f}")
            print(f"📊 Valor Atual: R$ {total_current:,.2f}")
            result_emoji = "💚" if total_profit_loss >= 0 else "❤️"
            print(f"{result_emoji} Resultado: R$ {total_profit_loss:,.2f} ({total_percentage:.1f}%)")
        else:
            print("   Nenhum investimento encontrado")
        
        # ===== METAS =====
        print("\n🎯 METAS:")
        print("-" * 40)
        cursor.execute("SELECT * FROM goals")
        goals = cursor.fetchall()
        
        if goals:
            print(f"{'ID':<3} {'Título':<20} {'Tipo':<12} {'Meta':<12} {'Atual':<12} {'Progresso':<10}")
            print("-" * 80)
            
            for row in goals:
                target = row[3]
                current = row[4]
                progress = (current / target * 100) if target > 0 else 0
                progress_str = f"{progress:.1f}%"
                
                status_emoji = "✅" if current >= target else "🔄"
                
                print(f"{row[0]:<3} {row[1]:<20} {row[2]:<12} R$ {target:,.2f} R$ {current:,.2f} {progress_str:<10} {status_emoji}")
                
                # Mostrar período
                print(f"    📅 {row[6]} → {row[7]} ({row[5]})")
                print()
        else:
            print("   Nenhuma meta encontrada")
        
        # ===== RESUMO GERAL =====
        print("\n📊 RESUMO GERAL:")
        print("-" * 40)
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        trans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM investments") 
        invest_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM goals")
        goals_count = cursor.fetchone()[0]
        
        print(f"💳 Transações: {trans_count}")
        print(f"📈 Investimentos: {invest_count}")
        print(f"🎯 Metas: {goals_count}")
        print(f"📅 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Visualização concluída!")
        print("🌐 Acesse também: http://localhost:8000/api/v1/transactions")
        print("=" * 60)
        
    except sqlite3.Error as e:
        print(f"❌ Erro ao acessar o banco: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")

def export_to_json():
    """Exportar dados para JSON"""
    try:
        conn = sqlite3.connect('ruviopay.db')
        cursor = conn.cursor()
        
        # Buscar todos os dados
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        
        cursor.execute("SELECT * FROM investments") 
        investments = cursor.fetchall()
        
        cursor.execute("SELECT * FROM goals")
        goals = cursor.fetchall()
        
        # Converter para formato JSON
        data = {
            "exported_at": datetime.now().isoformat(),
            "transactions": [
                {
                    "id": row[0], "description": row[1], "amount": row[2],
                    "type": row[3], "category": row[4], "date": row[5]
                } for row in transactions
            ],
            "investments": [
                {
                    "id": row[0], "name": row[1], "investment_type": row[2],
                    "amount_invested": row[3], "current_value": row[4], "purchase_date": row[5]
                } for row in investments
            ],
            "goals": [
                {
                    "id": row[0], "title": row[1], "goal_type": row[2],
                    "target_amount": row[3], "current_amount": row[4], "period_type": row[5],
                    "start_date": row[6], "end_date": row[7]
                } for row in goals
            ]
        }
        
        # Salvar arquivo JSON
        with open('ruviopay_backup.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        conn.close()
        print("✅ Dados exportados para 'ruviopay_backup.json'")
        
    except Exception as e:
        print(f"❌ Erro ao exportar: {e}")

if __name__ == "__main__":
    print("🚀 RuVioPay - Visualizador de Banco de Dados")
    print("\nOpções:")
    print("1. Ver dados no terminal")
    print("2. Exportar para JSON")
    
    choice = input("\nEscolha uma opção (1 ou 2): ").strip()
    
    if choice == "1":
        view_database()
    elif choice == "2":
        export_to_json()
    else:
        print("Opção inválida!")
        view_database()