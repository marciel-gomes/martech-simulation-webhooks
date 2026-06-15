import uvicorn
import asyncio
from fastapi import FastAPI
from app.api.webhook import router as webhook_router
from app.workers.consumer import martech_worker_consumer
from app.databases.db import init_db  # <-- Importa a inicialização do banco

app = FastAPI(title="Martech Webhook Ingestion API", version="1.0.0")

app.include_router(webhook_router)

@app.on_event("startup")
async def startup_event():
    init_db()  # <-- Inicializa o DuckDB (Cria a tabela se não existir)
    asyncio.create_task(martech_worker_consumer())

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
