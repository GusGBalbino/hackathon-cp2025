from fastapi import FastAPI
from routes.casos import router as casos_router
from routes.unidades import router as unidades_router
from routes.zonas import router as zonas_router
from fastapi.middleware.cors import CORSMiddleware
# --- Inicialização do FastAPI ---

app = FastAPI(
    title="API de Segurança da Mulher",
    description="API para relatar casos de assédio, visualizar zonas de risco e encontrar ajuda.",
    version="1.0.0"
)

#Cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", summary="health check", description="Verifica se a API está online.")
def read_root():
    """Endpoint raiz para verificar o status da API."""
    return {"status": "API de Segurança da Mulher funcionando!"}

app.include_router(casos_router)
app.include_router(unidades_router)
app.include_router(zonas_router)