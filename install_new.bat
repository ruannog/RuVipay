@echo off
echo.
echo ===============================================
echo    🚀 RuViPay - Instalacao Automatica
echo    Sistema de Gestao Financeira Pessoal
echo ===============================================
echo.

REM Verificar se Node.js está instalado
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js nao encontrado!
    echo    Por favor, instale Node.js 18+ em: https://nodejs.org
    pause
    exit /b 1
)

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado!
    echo    Por favor, instale Python 3.11+ em: https://python.org
    pause
    exit /b 1
)

echo ✅ Verificacao de pre-requisitos completa!
echo.

REM Criar ambiente virtual Python
echo 📦 Criando ambiente virtual Python...
python -m venv .venv
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instalar dependências do backend
echo 📥 Instalando dependencias do backend...
cd backend
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependencias do backend
    pause
    exit /b 1
)
cd ..

REM Instalar dependências do frontend
echo 📥 Instalando dependencias do frontend...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependencias do frontend
    pause
    exit /b 1
)
cd ..

echo.
echo ===============================================
echo           🎉 INSTALACAO CONCLUIDA!
echo ===============================================
echo.
echo Para iniciar o projeto:
echo.
echo   Backend (Terminal 1):
echo   cd backend
echo   .venv\Scripts\activate
echo   uvicorn main:app --reload
echo.
echo   Frontend (Terminal 2):
echo   cd frontend
echo   npm run dev
echo.
echo URLs de acesso:
echo   🎨 Frontend: http://localhost:3000
echo   ⚡ Backend:  http://localhost:8000
echo   📚 API Docs: http://localhost:8000/docs
echo.
echo ===============================================

REM Perguntar se quer iniciar automaticamente
set /p start="Deseja iniciar o projeto agora? (y/n): "
if /i "%start%"=="y" (
    echo.
    echo 🚀 Iniciando RuViPay...
    echo.
    
    REM Iniciar backend em nova janela
    start "RuViPay Backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    
    REM Aguardar 3 segundos
    timeout /t 3 /nobreak >nul
    
    REM Iniciar frontend em nova janela
    start "RuViPay Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
    
    REM Aguardar 5 segundos e abrir navegador
    timeout /t 5 /nobreak >nul
    echo 🌐 Abrindo navegador...
    start http://localhost:3000
    
    echo ✅ RuViPay iniciado com sucesso!
) else (
    echo 👍 Execute os comandos acima quando quiser iniciar o projeto
)

echo.
pause