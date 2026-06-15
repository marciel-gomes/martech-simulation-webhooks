from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re
from app.workers.consumer import sqs_queue_simulation  # <-- Importando a fila simulada

router = APIRouter(prefix="/webhook", tags=["Martech Ingestion"])

class WhatsAppMessagePayload(BaseModel):
    event_id: str = Field(..., description="ID único do evento gerado pela Meta API")
    phone_number: str = Field(..., description="Número de telefone do cliente")
    customer_name: str = Field(..., description="Nome do perfil do cliente")
    message_text: str = Field(..., description="Conteúdo de texto da mensagem")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("phone_number")
    @classmethod
    def validate_phone_format(cls, value: str) -> str:
        pattern = r"^\+\d{11,15}$"
        if not re.match(pattern, value):
            raise ValueError("O número de telefone deve estar no formato internacional (ex: +5511999999999)")
        return value

def mask_pii_data(phone: str) -> str:
    return f"{phone[:5]}*****{phone[-4:]}"

@router.post("/whatsapp", status_code=status.HTTP_202_ACCEPTED)
async def receive_whatsapp_webhook(payload: WhatsAppMessagePayload):
    try:
        masked_phone = mask_pii_data(payload.phone_number)
        
        # Prepara o payload interno
        internal_event = payload.model_dump()
        internal_event["phone_number_masked"] = masked_phone
        internal_event["retries"] = 0  # Inicializa o contador de tentativas
        
        # --- O PULO DO GATO DA ARQUITETURA ASSÍNCRONA ---
        # Coloca o evento na fila de processamento de forma não-bloqueante
        await sqs_queue_simulation.put(internal_event)
        
        print(f"[INGESTÃO] Evento {payload.event_id} enfileirado com sucesso.")
        
        return {
            "status": "Event enqueued for asynchronous processing",
            "event_id": payload.event_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao enfileirar o evento."
        )
