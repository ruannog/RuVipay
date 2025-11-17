"""
Configurações centralizadas do RuViPay Backend
"""

import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações da aplicação"""
    
    # API Settings
    PROJECT_NAME: str = "RuViPay API"
    PROJECT_DESCRIPTION: str = "Sistema de Gestão Financeira Pessoal"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server
        "http://192.168.0.16:3000",  # Network access
    ]
    
    # Database Settings - SQLite (simples, sem Docker)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./ruviopay.db"
    )
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "ruviopay-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Instância global das configurações
settings = Settings()