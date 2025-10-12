from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
backend_dir = Path(__file__).parent
sys.path.append(str(backend_dir))

try:
    from app.api.router import api_router
    from app.database import engine, Base
except ImportError as e:
    print(f"Import error: {e}")
    print("Creating basic API without database...")
    api_router = None
    engine = None
    Base = None

app = FastAPI(
    title="RuViPay API",
    description="API para sistema de gestão financeira pessoal",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000", 
    "http://localhost:5173",  # Vite dev server
    "http://192.168.0.16:3000",  # Network access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar tabelas do banco de dados
@app.on_event("startup")
async def startup_event():
    try:
        if Base and engine:
            Base.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")

# Incluir rotas da API
if api_router:
    app.include_router(api_router, prefix="/api/v1")
else:
    # Usar API simples sem banco de dados
    from simple_api import router as simple_router
    app.include_router(simple_router, prefix="/api/v1")

@app.get("/")
async def root():
    return JSONResponse(content={
        "message": "🚀 RuViPay API está funcionando!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "endpoints": {
            "docs": "http://localhost:8000/docs",
            "health": "http://localhost:8000/health"
        }
    })

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy", "message": "API is running"})

# Endpoints básicos para testar
@app.get("/api/v1/test")
async def test_endpoint():
    return {"message": "Backend conectado com sucesso!", "timestamp": "2024-01-01"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando RuViPay API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)