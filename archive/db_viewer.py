"""
Visualizador Web do Banco de Dados RuVioPay
Interface profissional para apresentação
"""
import sqlite3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

class DatabaseViewerHandler(BaseHTTPRequestHandler):
    
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
        
        if path == '/':
            self.serve_html()
        elif path == '/api/schema':
            self.serve_schema()
        elif path == '/api/data':
            self.serve_data()
        else:
            self.send_response(404)
            self.end_headers()
    
    def serve_html(self):
        """Página HTML para visualizar o banco"""
        html = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 RuVioPay - Visualizador de Banco de Dados</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            color: white; 
            padding: 30px; 
            text-align: center;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .header p { font-size: 1.2rem; opacity: 0.9; }
        .content { padding: 30px; }
        .section { margin-bottom: 40px; }
        .section h2 { 
            color: #374151; 
            border-bottom: 3px solid #4f46e5; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
            font-size: 1.5rem;
        }
        table { 
            width: 100%; 
            border-collapse: collapse; 
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        th { 
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            color: white; 
            padding: 15px; 
            font-weight: 600;
            text-align: left;
        }
        td { 
            padding: 12px 15px; 
            border-bottom: 1px solid #f3f4f6;
        }
        tr:hover { background-color: #f8fafc; }
        .positive { color: #10b981; font-weight: bold; }
        .negative { color: #ef4444; font-weight: bold; }
        .status { 
            padding: 4px 12px; 
            border-radius: 20px; 
            font-size: 0.85rem; 
            font-weight: 500;
        }
        .status.income { background: #dcfce7; color: #166534; }
        .status.expense { background: #fee2e2; color: #991b1b; }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px;
        }
        .stat-card { 
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 20px; 
            border-radius: 15px; 
            text-align: center;
            border: 1px solid #e2e8f0;
        }
        .stat-card h3 { color: #4f46e5; font-size: 2rem; margin-bottom: 5px; }
        .stat-card p { color: #64748b; font-weight: 500; }
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4f46e5, #06b6d4);
            transition: width 0.3s ease;
        }
        .loading { text-align: center; padding: 40px; color: #64748b; }
        .refresh-btn {
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 20px;
        }
        .refresh-btn:hover { opacity: 0.9; transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 RuVioPay Database</h1>
            <p>Visualizador Profissional do Banco de Dados</p>
        </div>
        
        <div class="content">
            <button class="refresh-btn" onclick="loadData()">🔄 Atualizar Dados</button>
            
            <div id="stats" class="stats">
                <div class="loading">Carregando estatísticas...</div>
            </div>
            
            <div class="section">
                <h2>💰 Transações</h2>
                <div id="transactions">
                    <div class="loading">Carregando transações...</div>
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Investimentos</h2>
                <div id="investments">
                    <div class="loading">Carregando investimentos...</div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 Metas</h2>
                <div id="goals">
                    <div class="loading">Carregando metas...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function formatCurrency(value) {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value);
        }

        function formatDate(dateStr) {
            return new Date(dateStr).toLocaleDateString('pt-BR');
        }

        function loadData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => {
                    renderStats(data);
                    renderTransactions(data.transactions);
                    renderInvestments(data.investments);
                    renderGoals(data.goals);
                })
                .catch(error => {
                    console.error('Erro:', error);
                });
        }

        function renderStats(data) {
            const totalIncome = data.transactions
                .filter(t => t.type === 'income')
                .reduce((sum, t) => sum + t.amount, 0);
            
            const totalExpense = data.transactions
                .filter(t => t.type === 'expense')
                .reduce((sum, t) => sum + t.amount, 0);
            
            const balance = totalIncome - totalExpense;
            
            document.getElementById('stats').innerHTML = `
                <div class="stat-card">
                    <h3>${formatCurrency(totalIncome)}</h3>
                    <p>Total Receitas</p>
                </div>
                <div class="stat-card">
                    <h3>${formatCurrency(totalExpense)}</h3>
                    <p>Total Despesas</p>
                </div>
                <div class="stat-card">
                    <h3 class="${balance >= 0 ? 'positive' : 'negative'}">${formatCurrency(balance)}</h3>
                    <p>Saldo Atual</p>
                </div>
                <div class="stat-card">
                    <h3>${data.transactions.length}</h3>
                    <p>Transações</p>
                </div>
            `;
        }

        function renderTransactions(transactions) {
            if (transactions.length === 0) {
                document.getElementById('transactions').innerHTML = '<p>Nenhuma transação encontrada</p>';
                return;
            }

            const html = `
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Descrição</th>
                            <th>Valor</th>
                            <th>Tipo</th>
                            <th>Categoria</th>
                            <th>Data</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${transactions.map(t => `
                            <tr>
                                <td>${t.id}</td>
                                <td>${t.description}</td>
                                <td class="${t.type === 'income' ? 'positive' : 'negative'}">
                                    ${t.type === 'income' ? '+' : '-'}${formatCurrency(Math.abs(t.amount))}
                                </td>
                                <td><span class="status ${t.type}">${t.type === 'income' ? 'Receita' : 'Despesa'}</span></td>
                                <td>${t.category}</td>
                                <td>${formatDate(t.date)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
            document.getElementById('transactions').innerHTML = html;
        }

        function renderInvestments(investments) {
            if (investments.length === 0) {
                document.getElementById('investments').innerHTML = '<p>Nenhum investimento encontrado</p>';
                return;
            }

            const html = `
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Tipo</th>
                            <th>Investido</th>
                            <th>Valor Atual</th>
                            <th>Resultado</th>
                            <th>%</th>
                            <th>Data Compra</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${investments.map(i => {
                            const profitLoss = i.current_value - i.amount_invested;
                            const percentage = (profitLoss / i.amount_invested * 100).toFixed(1);
                            return `
                                <tr>
                                    <td>${i.id}</td>
                                    <td>${i.name}</td>
                                    <td>${i.investment_type}</td>
                                    <td>${formatCurrency(i.amount_invested)}</td>
                                    <td>${formatCurrency(i.current_value)}</td>
                                    <td class="${profitLoss >= 0 ? 'positive' : 'negative'}">
                                        ${profitLoss >= 0 ? '+' : ''}${formatCurrency(profitLoss)}
                                    </td>
                                    <td class="${percentage >= 0 ? 'positive' : 'negative'}">
                                        ${percentage >= 0 ? '+' : ''}${percentage}%
                                    </td>
                                    <td>${formatDate(i.purchase_date)}</td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            `;
            document.getElementById('investments').innerHTML = html;
        }

        function renderGoals(goals) {
            if (goals.length === 0) {
                document.getElementById('goals').innerHTML = '<p>Nenhuma meta encontrada</p>';
                return;
            }

            const html = `
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Título</th>
                            <th>Tipo</th>
                            <th>Meta</th>
                            <th>Atual</th>
                            <th>Progresso</th>
                            <th>Período</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${goals.map(g => {
                            const progress = (g.current_amount / g.target_amount * 100).toFixed(1);
                            return `
                                <tr>
                                    <td>${g.id}</td>
                                    <td>${g.title}</td>
                                    <td>${g.goal_type}</td>
                                    <td>${formatCurrency(g.target_amount)}</td>
                                    <td>${formatCurrency(g.current_amount)}</td>
                                    <td>
                                        ${progress}%
                                        <div class="progress-bar">
                                            <div class="progress-fill" style="width: ${Math.min(progress, 100)}%"></div>
                                        </div>
                                    </td>
                                    <td>${formatDate(g.start_date)} → ${formatDate(g.end_date)}</td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
            `;
            document.getElementById('goals').innerHTML = html;
        }

        // Carregar dados ao iniciar
        loadData();
        
        // Atualizar a cada 30 segundos
        setInterval(loadData, 30000);
    </script>
</body>
</html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_schema(self):
        """Retorna o esquema do banco"""
        try:
            conn = sqlite3.connect('ruviopay.db')
            cursor = conn.cursor()
            
            # Obter esquema das tabelas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            schema = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                schema[table_name] = [
                    {
                        "name": col[1],
                        "type": col[2],
                        "notnull": col[3],
                        "default": col[4],
                        "pk": col[5]
                    } for col in columns
                ]
            
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(schema).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def serve_data(self):
        """Retorna todos os dados do banco"""
        try:
            conn = sqlite3.connect('ruviopay.db')
            cursor = conn.cursor()
            
            # Transações
            cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
            transactions = [
                {
                    "id": row[0], "description": row[1], "amount": row[2],
                    "type": row[3], "category": row[4], "date": row[5]
                } for row in cursor.fetchall()
            ]
            
            # Investimentos
            cursor.execute("SELECT * FROM investments")
            investments = [
                {
                    "id": row[0], "name": row[1], "investment_type": row[2],
                    "amount_invested": row[3], "current_value": row[4], "purchase_date": row[5]
                } for row in cursor.fetchall()
            ]
            
            # Metas
            cursor.execute("SELECT * FROM goals")
            goals = [
                {
                    "id": row[0], "title": row[1], "goal_type": row[2],
                    "target_amount": row[3], "current_amount": row[4], "period_type": row[5],
                    "start_date": row[6], "end_date": row[7]
                } for row in cursor.fetchall()
            ]
            
            conn.close()
            
            data = {
                "transactions": transactions,
                "investments": investments,
                "goals": goals
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

def run_db_viewer():
    print("🗄️ Iniciando Visualizador do Banco de Dados...")
    server = HTTPServer(('localhost', 9000), DatabaseViewerHandler)
    print("✅ Visualizador rodando em http://localhost:9000")
    print("📊 Acesse no navegador para ver as tabelas!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Visualizador parado pelo usuário")
        server.server_close()

if __name__ == "__main__":
    run_db_viewer()