#!/bin/bash

# Script de instalação automática do RuViPay
# Compatível com Linux e macOS

echo "🚀 Instalando RuViPay..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instalando dependências manualmente..."
    
    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
        exit 1
    fi
    
    # Verificar Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js não encontrado. Por favor, instale Node.js 18+"
        exit 1
    fi
    
    echo "✅ Dependências encontradas. Configurando projeto..."
    
    # Instalar dependências do backend
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
    
    # Instalar dependências do frontend
    cd frontend
    npm install
    cd ..
    
    echo "✅ Projeto configurado! Execute 'npm run start' para iniciar."
    
else
    echo "✅ Docker encontrado. Usando configuração com containers..."
    docker-compose up --build
fi