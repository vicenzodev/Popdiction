from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import router as api_router
import uvicorn

# Inicializa o aplicativo FastAPI
app = FastAPI(
    title="API Previsão de Sorvetes",
    version="1.0.0",
    description="API REST para previsão de demanda de vendas (Qtd Única)"
)

# Configuração de CORS (Essencial se a sua plataforma for um site Web/Frontend)
# Isso permite que outros domínios façam requisições para a sua API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, troque "*" pelo domínio da sua plataforma
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
    
# Inicia o servidor Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Uma rota básica apenas para checar se o servidor está online (Health Check)
@app.get("/")
def health_check():
    return {
        "status": "online",
        "mensagem": "A API de Previsão de Sorvetes está rodando perfeitamente!"
    }