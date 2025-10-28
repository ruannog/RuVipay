"""
RuViPay API - Sistema de Gestão Financeira Pessoal
FastAPI backend com PostgreSQL
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

from app.api.router import api_router
from app.database import engine, Base
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar tabelas do banco de dados
@app.on_event("startup")
async def startup_event():
    """Inicializar banco de dados na startup"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Incluir rotas da API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return JSONResponse(content={
        "message": f"🚀 {settings.PROJECT_NAME} está funcionando!",
        "version": settings.VERSION,
        "docs": "/docs",
        "status": "running",
        "endpoints": {
            "docs": f"http://localhost:{settings.PORT}/docs",
            "health": f"http://localhost:{settings.PORT}/health"
        }
    })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(content={"status": "healthy", "message": "API is running"})

@app.get(f"{settings.API_V1_STR}/test")
async def test_endpoint():
    """Endpoint de teste"""
    return {"message": "Backend conectado com sucesso!", "timestamp": "2024-01-01"}

if __name__ == "__main__":
    import uvicorn
    print(f"🚀 Iniciando {settings.PROJECT_NAME}...")
    uvicorn.run(
        app, 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )