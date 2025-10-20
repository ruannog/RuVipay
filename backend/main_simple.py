from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from simple_api import router

# Criar instância do FastAPI
app = FastAPI(
    title="RuViPay API",
    description="API para sistema de gerenciamento financeiro",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api", tags=["transactions"])

@app.get("/")
async def root():
    return {
        "message": "RuViPay API está funcionando!",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RuViPay API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)