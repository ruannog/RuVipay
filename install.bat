@echo off
REM Script de instalação automática do RuViPay para Windows

echo 🚀 Instalando RuViPay...

REM Verificar se Docker está instalado
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado. Instalando dependências manualmente...
    
    REM Verificar Python
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Python não encontrado. Por favor, instale Python 3.11+
        pause
        exit /b 1
    )
    
    REM Verificar Node.js
    node --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Node.js não encontrado. Por favor, instale Node.js 18+
        pause
        exit /b 1
    )
    
    echo ✅ Dependências encontradas. Configurando projeto...
    
    REM Instalar dependências do backend
    cd backend
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    cd ..
    
    REM Instalar dependências do frontend
    cd frontend
    npm install
    cd ..
    
    echo ✅ Projeto configurado! Execute 'npm run start' para iniciar.
    pause
    
) else (
    echo ✅ Docker encontrado. Usando configuração com containers...
    docker-compose up --build
)

pause