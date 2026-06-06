from fastapi import FastAPI
from app.database import db, unique_email
from app.api.auth import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {
        "title": "API de Contabilidade",
        "description": "API para gerenciamento de clientes, fornecedores, contas a pagar e receber",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    await unique_email()