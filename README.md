# 💰 RuViPay - Sistema de Gestão Financeira Pessoal

<div align="center">

![RuViPay Logo](https://img.shields.io/badge/RuViPay-Financial%20Management-blue?style=for-the-badge&logo=wallet)

**Sistema completo de gestão financeira pessoal com SQLite - Simples e Rápido!**

[![Frontend](https://img.shields.io/badge/Frontend-React%2018-61DAFB?style=flat&logo=react)](http://localhost:3000)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](http://localhost:8000)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=flat&logo=sqlite)](https://sqlite.org)

[🌐 Frontend](http://localhost:3000) | [📚 API Docs](http://localhost:8000/docs) | [🐛 Issues](https://github.com/ruannog/RuViPay/issues)

</div>

---

## 🎯 **Visão Geral**

RuViPay é uma aplicação moderna para gestão financeira pessoal, desenvolvida com **SQLite** para máxima simplicidade. Não precisa de Docker, PostgreSQL ou configurações complexas!

### ✨ **Principais Funcionalidades**

- 💰 **Controle de Receitas e Despesas** - Registro completo de transações
- 🏷️ **Categorização Inteligente** - Organize suas finanças por categoria
- 📊 **Dashboard Interativo** - Visualize suas finanças em tempo real
- 📈 **Gráficos Dinâmicos** - Charts.js para análises visuais
- 🎯 **Metas Financeiras** - Defina e acompanhe objetivos
- 📱 **Design Responsivo** - Funciona em desktop, tablet e mobile
- 🔐 **Autenticação Segura** - Sistema de login protegido
- 🚀 **Performance Otimizada** - React Query para cache inteligente

---

## 🏗️ **Arquitetura do Sistema**

```mermaid
graph TB
    A[React Frontend] --> B[FastAPI Backend]
    B --> C[PostgreSQL Database]
    A --> D[TailwindCSS]
    A --> E[Chart.js]
    B --> F[SQLAlchemy ORM]
    B --> G[Pydantic Validation]
```

### 🛠️ **Stack Tecnológica**

#### **Frontend**
- ⚛️ **React 18** - Biblioteca para interfaces
- 🎨 **TypeScript** - Tipagem estática
- 🎯 **Vite** - Build tool ultra-rápido
- 🎨 **TailwindCSS** - Framework CSS utility-first
- 📊 **Chart.js** - Gráficos interativos
- 🔄 **React Query** - Gerenciamento de estado servidor
- 🧭 **React Router** - Navegação SPA

#### **Backend**
- 🐍 **Python 3.11+** - Linguagem de programação
- ⚡ **FastAPI** - Framework web moderno
- 🗃️ **SQLAlchemy** - ORM Python
- ✅ **Pydantic** - Validação de dados
- 🔒 **JWT** - Autenticação segura
- 📚 **OpenAPI** - Documentação automática

#### **Banco de Dados**
- 🐘 **PostgreSQL 15** - Banco relacional
- 🔄 **Alembic** - Migrações de schema

#### **DevOps**
- 🐳 **Docker** - Containerização
- 🐙 **Docker Compose** - Orquestração
- 🔧 **GitHub Actions** - CI/CD (em breve)

---

## 🚀 **Como Executar o Projeto**

### ⚡ **Instalação Rápida (Recomendada)**

**Windows:**
```cmd
git clone https://github.com/VitorFeuser/RuViPay.git
cd RuViPay
install.bat
```

**Linux/macOS:**
```bash
git clone https://github.com/VitorFeuser/RuViPay.git
cd RuViPay
chmod +x install.sh
./install.sh
```

### 🐳 **Docker (Mais Fácil)**

```bash
# Clonar repositório
git clone https://github.com/VitorFeuser/RuViPay.git
cd RuViPay

# Executar com Docker
docker-compose up --build

# Acessar aplicação
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 💻 **Desenvolvimento Manual**

#### **Pré-requisitos**
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Git

#### **Backend**
```bash
cd backend

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente (Windows)
.venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### **Frontend**
```bash
cd frontend

# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Build para produção
npm run build
```

---

## 🌐 **URLs de Acesso**

| Serviço | URL | Descrição |
|---------|-----|-----------|
| 🎨 **Frontend** | http://localhost:3000 | Interface do usuário |
| ⚡ **Backend API** | http://localhost:8000 | API REST |
| 📚 **Documentação** | http://localhost:8000/docs | Swagger UI |
| 🔄 **ReDoc** | http://localhost:8000/redoc | Documentação alternativa |
| ❤️ **Health Check** | http://localhost:8000/health | Status da API |

---

## 📁 **Estrutura do Projeto**

```
RuViPay/
├── 📁 frontend/              # React TypeScript App
│   ├── 📁 src/
│   │   ├── 📁 components/    # Componentes reutilizáveis
│   │   ├── 📁 pages/         # Páginas da aplicação
│   │   ├── 📁 hooks/         # Hooks personalizados
│   │   ├── 📁 services/      # Integração com API
│   │   └── 📁 contexts/      # Contextos React
│   ├── 📄 package.json       # Dependências Node.js
│   └── 📄 vite.config.ts     # Configuração Vite
├── 📁 backend/               # FastAPI Python App
│   ├── 📁 app/
│   │   ├── 📁 api/           # Endpoints da API
│   │   ├── 📁 models/        # Modelos SQLAlchemy
│   │   ├── 📁 schemas/       # Schemas Pydantic
│   │   └── 📁 services/      # Lógica de negócio
│   ├── 📄 main.py            # Entry point da API
│   └── 📄 requirements.txt   # Dependências Python
├── 📁 database/              # Scripts PostgreSQL
├── 🐳 docker-compose.yml     # Orquestração Docker
├── 📄 install.bat            # Instalador Windows
├── 📄 install.sh             # Instalador Linux/Mac
└── 📖 README.md              # Este arquivo
```

---

## 📊 **Capturas de Tela**

### 🏠 Dashboard Principal
![Dashboard](https://via.placeholder.com/800x400?text=Dashboard+Screenshot)

### 💰 Gestão de Transações
![Transações](https://via.placeholder.com/800x400?text=Transactions+Screenshot)

### 🏷️ Categorias
![Categorias](https://via.placeholder.com/800x400?text=Categories+Screenshot)

---

## 🔧 **Configuração Avançada**

### 🌍 **Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ruviopay
POSTGRES_DB=ruviopay
POSTGRES_USER=ruviopay_user
POSTGRES_PASSWORD=ruviopay_pass

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_STR=/api/v1
PROJECT_NAME=RuViPay

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

---

## 🧪 **Testes**

```bash
# Testes do Backend
cd backend
pytest

# Testes do Frontend
cd frontend
npm test

# Cobertura de testes
npm run test:coverage
```

---

## 🚀 **Deploy em Produção**

### 🌐 **Vercel + Railway**

1. **Frontend no Vercel:**
   ```bash
   npm run build
   vercel --prod
   ```

2. **Backend no Railway:**
   ```bash
   railway login
   railway init
   railway up
   ```

### 🐳 **Docker Production**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🤝 **Contribuindo**

Contribuições são muito bem-vindas! 

1. 🍴 **Fork** o projeto
2. 🌿 **Crie** sua feature branch (`git checkout -b feature/AmazingFeature`)
3. ✨ **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. 📤 **Push** para a branch (`git push origin feature/AmazingFeature`)
5. 🎉 **Abra** um Pull Request

### 📋 **Roadmap**

- [ ] 🔐 Sistema de autenticação completo
- [ ] 📱 Progressive Web App (PWA)
- [ ] 📊 Relatórios avançados em PDF
- [ ] 🎯 Sistema de metas financeiras
- [ ] 📈 Integração com bancos (Open Banking)
- [ ] 🤖 IA para categorização automática
- [ ] 📧 Notificações por email
- [ ] 📱 App mobile React Native

---

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 **Autor**

**Vitor Feuser**
- 🐙 GitHub: [@VitorFeuser](https://github.com/VitorFeuser)
- 💼 LinkedIn: [Vitor Feuser](https://linkedin.com/in/vitorfeuser)
- 📧 Email: vitor@ruviopay.com

---

## 🙏 **Agradecimentos**

- 💙 **React Team** pela incrível biblioteca
- ⚡ **FastAPI** pelo framework moderno
- 🎨 **TailwindCSS** pelo design system
- 📊 **Chart.js** pelos gráficos
- 🐘 **PostgreSQL** pela robustez

---

<div align="center">

**⭐ Se este projeto te ajudou, dê uma estrela! ⭐**


</div>
```

✅ **Acesse:** 
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Docs API: http://localhost:8000/docs

### 🛠️ Opção 2: Instalação Manual

**Sistemas compatíveis:**
- ✅ Windows 10/11
- ✅ macOS 12+ (Intel/Apple Silicon)
- ✅ Ubuntu 20.04+
- ✅ Debian 11+
- ✅ CentOS 8+
- ✅ Fedora 35+

### Configuração manual

#### Backend (Python/FastAPI)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend (React/TypeScript)

```bash
cd frontend
npm install
npm run dev
```

#### Banco de Dados

```bash
# Usando Docker
docker run --name ruviopay-postgres -e POSTGRES_PASSWORD=senha123 -e POSTGRES_DB=ruviopay -p 5432:5432 -d postgres:15

# Executar migrações
cd backend
alembic upgrade head
```

## 📚 Endpoints da API

- `GET /api/v1/transactions` - Lista transações
- `POST /api/v1/transactions` - Cria transação
- `GET /api/v1/categories` - Lista categorias
- `GET /api/v1/dashboard` - Dados do dashboard
- `GET /api/v1/reports` - Relatórios financeiros

## 🧪 Testes

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 📁 Estrutura do Projeto

```
ruviopay/
├── frontend/           # React + TypeScript
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/            # FastAPI + SQLAlchemy
│   ├── app/
│   ├── alembic/
│   └── requirements.txt
├── database/           # Scripts SQL e migrações
├── docker-compose.yml  # Configuração Docker
└── README.md
```

## 🛠️ Tecnologias Utilizadas

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Query
- React Router
- Chart.js
- Axios

### Backend
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- JWT Authentication
- Pytest

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
